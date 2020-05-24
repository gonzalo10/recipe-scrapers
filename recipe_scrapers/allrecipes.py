from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, get_yields, scrape_second_website


class AllRecipes(AbstractScraper):

    @classmethod
    def host(self):
        return 'allrecipes.com'

    def title(self):
        return normalize_string(self.soup.find('h1').get_text())

    def ingredients(self):
        ingredientsList = self.ingredients_new()
        if not ingredientsList:
            ingredientsList = self.ingredients_old()
        return ingredientsList

    def tags(self):
        tagsList = self.tags_new()
        if not tagsList:
            tagsList = self.tags_old()
        return tagsList

    def tags_new(self):
        breadcrumbsRaw = self.soup.findAll(
            'span',
            {"class": "breadcrumbs__title"}
        )
        if not breadcrumbsRaw:
            return
        tags = []
        for tag in breadcrumbsRaw:
            tags.append(normalize_string(tag.get_text()))
        return tags

    def tags_old(self):
        breadcrumbsRaw = self.soup.find(
            'ol',
            {"class": "breadcrumbs breadcrumbs"}
        )
        if not breadcrumbsRaw:
            return
        tags = []
        tagElements = breadcrumbsRaw.findAll('li')
        for tag in tagElements:
            tags.append(normalize_string(tag.get_text()).strip())
        return tags

    def raiting(self):
        raitingScoreRaw = self.soup.find(
            'span',
            {"class": "review-star-text"}
        )
        raitingScore = 0
        if raitingScoreRaw:
            raitingScore = normalize_string(
                raitingScoreRaw.get_text().split(':')[1].split()[0])
        if not raitingScore:
            raitingRaw = self.soup.find(
                'div',
                {"class": "rating-stars"})
            if raitingRaw:
                raitingScore = raitingRaw['data-ratingstars']

        return raitingScore

    def images(self):
        image = self.images_new()
        if not image:
            image = self.images_old()
        return image

    def images_old(self):
        ingredientsContianer = self.soup.find(
            'img',
            {"class": "rec-photo"}
        )
        if not ingredientsContianer:
            return
        image_src = ingredientsContianer['src']
        return image_src

    def images_new(self):
        imageContainer = self.soup.find(
            "div", {"class": "image-container"})
        if not imageContainer:
            return
        imageTag = imageContainer.find('img')
        if not imageTag:
            return
        image_src = imageTag['src']
        return image_src

    def ingredients_old(self):
        ingredientsContianer = self.soup.find(
            'div',
            {"id": "polaris-app"}
        )

        ingredientColumns = ingredientsContianer.findAll('ul')
        ingredientsList = []
        for column in ingredientColumns:
            ingredients = column.findAll(
                'span', {'itemprop': "recipeIngredient"})
            for ingredient in ingredients:
                ingredientsList.append(normalize_string(ingredient.get_text()))
        return ingredientsList

    def ingredients_new(self):
        ingredients = self.soup.findAll(
            'li',
            {"class": "ingredients-item"}
        )
        if not ingredients:
            return
        ingredientsList = []
        for ingredientRaw in ingredients:
            ingredient = ingredientRaw.find('span',
                                            {"class": "ingredients-item-name"})
            ingredientsList.append(normalize_string(ingredient.get_text()))

        return ingredientsList

    def recipe_summary(self):
        summary = self.recipe_summary_new()
        if not summary:
            summary = self.recipe_summary_old()
        return summary

    def recipe_summary_new(self):
        recipeSummaryRaw = self.soup.find(
            'aside',
            {"class": "recipe-info-section"}
        )
        macrosContainer = self.soup.find(
            'div', {"class": "partial recipe-nutrition-section"})
        if not macrosContainer:
            return
        macrosSummaryRaw = macrosContainer.find(
            'div', {"class": "section-body"})
        macrosText = macrosSummaryRaw.get_text().strip()
        removedTitle = macrosText.replace("Full Nutrition", "").strip()

        correctSodiumTypo = removedTitle.replace('sodium.', "sodium;")
        parsedMacros = normalize_string(correctSodiumTypo).split(';')
        withouWhiteSpaces = []
        for macro in parsedMacros:
            withouWhiteSpaces.append(macro.strip())
        macrosSummary = {}
        for macro in withouWhiteSpaces:
            if not macro:
                break
            splitedMacro = macro.split(" ")
            value = splitedMacro[0]
            unit = splitedMacro[1]
            if unit == 'calories':
                unit = "Kcal"
            title = splitedMacro[len(splitedMacro) - 1]
            macrosSummary[title] = value+' '+unit

        if not recipeSummaryRaw:
            return

        recipeSummary = recipeSummaryRaw.findAll(
            'div',
            {"class": "recipe-meta-item"}
        )
        summary = {}
        for item in recipeSummary:
            nameRaw = item.find(
                'div',
                {"class": "recipe-meta-item-header"}
            )
            name = normalize_string(nameRaw.get_text()).strip()
            name = name.replace(":", "")
            valueRaw = item.find(
                'div',
                {"class": "recipe-meta-item-body"}
            )
            if name == 'total':
                name = "total_time"
            value = normalize_string(valueRaw.get_text()).strip()
            summary[name.lower()] = value
        for item in summary:
            macrosSummary[item] = summary[item]
        return macrosSummary

    def recipe_summary_old(self):
        macrosSummaryRaw = self.soup.find(
            'div', {"class": "nutrition-summary-facts"})

        macrosSpanText = macrosSummaryRaw.get_text()
        removedTitle = macrosSpanText.replace("Per Serving:", "")
        removedEnding = removedTitle.replace("Full nutrition", "")
        parsedMacros = normalize_string(removedEnding).split(';')
        withouWhiteSpaces = []
        for macro in parsedMacros:
            withouWhiteSpaces.append(macro.strip())
        macrosSummary = {}
        for macro in withouWhiteSpaces:
            if not macro:
                break
            splitedMacro = macro.split(" ")
            value = splitedMacro[0]
            unit = splitedMacro[1]
            if unit == 'calories':
                unit = "Kcal"
            title = splitedMacro[len(splitedMacro) - 1]
            macrosSummary[title] = value+' '+unit
        recipeSummary = self.soup.find(
            'span',
            {"class": "recipe-ingredients__header__toggles"}
        )
        timeRaw = recipeSummary.find('span',
                                     {"class": "ready-in-time"})
        if not timeRaw:
            time = ''
        if timeRaw:
            time = normalize_string(timeRaw.get_text())

        servingNumberRaw = recipeSummary.find('meta',
                                              {"id": "metaRecipeServings"})
        if not servingNumberRaw:
            servings = ''
        if servingNumberRaw:
            servings = normalize_string(servingNumberRaw['content'])

        macrosSummary["total_time"] = time
        macrosSummary["servings"] = servings
        return macrosSummary

    def recipe_time(self):
        timeContainer = self.soup.find(
            'ul',
            {"class": "prepTime"}
        )
        prepTimeRaw = timeContainer.find(
            'time',
            {"itemprop": "prepTime"}
        )
        cookTimeRaw = timeContainer.find(
            'time',
            {"itemprop": "cookTime"}
        )
        totalTimeRaw = timeContainer.find(
            'time',
            {"itemprop": "totalTime"}
        )

        prepTime = normalize_string(prepTimeRaw["datetime"])
        cookTime = normalize_string(cookTimeRaw["datetime"])
        totalTime = normalize_string(totalTimeRaw["datetime"])

        return {"prep_time": prepTime, "cookTime": cookTime, "totalTime": totalTime}

    def scrape_full_nutrition(self):
        return scrape_second_website(
            self.url+'/fullrecipenutrition/')

    def full_nutrition_data(self):

        soup = self.scrape_full_nutrition()

        nutritionContianer = soup.find(
            'div',
            {"class": "nutrition-body"}
        )
        if not nutritionContianer:
            return

        nutritionRows = nutritionContianer.findAll(
            'div',
            {"class": "nutrition-row"}
        )
        nutritionList = []
        for row in nutritionRows:
            nutrition = row.findAll(
                'span',
                {"class": "nutrient-name"}
            )
            nutritionList.append(normalize_string(
                nutrition[0].get_text()).strip())
        return nutritionList

    def instructions(self):
        instructionsData = self.instructions_old()
        if not instructionsData:
            instructionsData = self.instructions_new()
        return instructionsData

    def instructions_old(self):
        instructionsRaw = self.soup.findAll(
            'span',
            {"class": "recipe-directions__list--item"}
        )
        instructionsList = []
        for instruction in instructionsRaw:
            instructionsList.append(normalize_string(instruction.get_text()))
        return instructionsList

    def instructions_new(self):
        instructionsContainer = self.soup.find(
            'ul',
            {"class": "instructions-section"}
        )
        instructionsRaw = instructionsContainer.findAll(
            'div',
            {"class": "paragraph"}
        )
        instructionsList = []
        for instruction in instructionsRaw:
            instructionsList.append(normalize_string(instruction.get_text()))
        return instructionsList
