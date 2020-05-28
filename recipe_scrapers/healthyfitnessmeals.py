# GreatBritishChefs.com scraper
# Written by G.D. Wallters
# Freely released the code to recipe_scraper group
# 6 February, 2020
# =======================================================
from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, get_yields
# ['title']
# ['img_src']
# ['url']
# ['tags']
# ['raiting']
# ['instructions']
# ['full_nutrition_data']
# ['parsed_ingredients']
# ['ingredients']
# ['recipe_summary']
# ['searchable_keys']


class HealthyFitnessMeals(AbstractScraper):

    @classmethod
    def host(self):
        return 'healthyfitnessmeals.com'

    def title(self):
        return normalize_string(self.soup.find('h1').get_text())

    def description(self):
        descriptionSummary = self.soup.find(
            'div', {'class': "wprm-recipe-summary wprm-block-text-normal"})

        if not descriptionSummary:
            return

        return normalize_string(descriptionSummary.get_text())

    def isRecipe(self):
        jumpToRecipeTag = self.soup.find(
            "span", {"class": "wprm-recipe-icon wprm-recipe-jump-icon"})
        if not jumpToRecipeTag:
            return False
        return True

    def tags(self):
        tagsRaw = self.soup.find(
            "div", {"class": "wprm-recipe-meta-container"})
        if not tagsRaw:
            return
        tagsContainer = self.soup.find('div', {"class": "entry-content"})
        taxomonyIndicator = tagsContainer.findAll(
            "a", {"class": "taxonomy-indicator"})
        curatedTags = []
        if taxomonyIndicator:
            for indicator in taxomonyIndicator:
                indicatorUrl = indicator['href']
                indicatorRaw = indicatorUrl.split("category")
                indicator = indicatorRaw[len(indicatorRaw)-1]
                parsedIndicator = indicator.replace("/", "")
                parsedIndicator = parsedIndicator.replace("-", " ")
                parsedIndicator = normalize_string(parsedIndicator.strip())
                if parsedIndicator not in curatedTags:
                    parsedIndicator = parsedIndicator.lower()
                    curatedTags.append(parsedIndicator)

        tagsDivs = tagsRaw.findAll("div")

        for tag in tagsDivs:
            tag = normalize_string(tag.get_text())
            tag = tag.split(":")[1].split(",")
            for word in tag:
                tagsText = normalize_string(word.strip())
                if tagsText not in curatedTags:
                    tagsText = tagsText.lower()
                    curatedTags.append(tagsText)
        return curatedTags

    def getTotalTime(self):
        totalTimeContainer = self.soup.find(
            "div", {"class": "wprm-recipe-total-time-container"})
        if totalTimeContainer:
            totalTime = normalize_string(totalTimeContainer.get_text())
            parsedTotalTime = totalTime.split(":")[1]
            if parsedTotalTime:
                return parsedTotalTime.strip()
            else:
                return
        else:
            return

    def getServings(self):
        servingsContainer = self.soup.find(
            "div", {"class": "wprm-recipe-servings-container"})
        if servingsContainer:
            servingsText = normalize_string(servingsContainer.get_text())
            parsedServings = servingsText.split(":")[1]
            if parsedServings:
                return parsedServings.strip()
            else:
                return
        else:
            return

    def getTotalCalores(self):
        caloresContainer = self.soup.find(
            "div", {"class": "wprm-recipe-calories-container"})
        if caloresContainer:
            caloresText = normalize_string(caloresContainer.get_text())
            parsedCalories = caloresText.split(":")[1]
            if parsedCalories:
                return parsedCalories.strip()
            else:
                return
        else:
            return

    def raiting(self):
        return 5

    def recipe_summary(self):
        summary = {}
        totalTime = self.getTotalTime()
        if totalTime:
            summary["total_time"] = totalTime
        servings = self.getServings()
        if servings:
            summary["servings"] = servings
        calories = self.getTotalCalores()
        if calories:
            summary["calories"] = calories
        return summary

    def getAllIngredientsRaw(self):
        ingredientsRaw = self.soup.findAll(
            "li", {"class": "wprm-recipe-ingredient"})
        curatedIngredients = []
        parsed_ingredients = []
        if ingredientsRaw:
            for ingredientRaw in ingredientsRaw:
                ingredient = ''
                amount = ingredientRaw.find(
                    "span", {"class": "wprm-recipe-ingredient-amount"})
                if amount:
                    amount = normalize_string(amount.get_text().strip())
                    ingredient = amount
                unit = ingredientRaw.find(
                    "span", {"class": "wprm-recipe-ingredient-unit"})
                if unit:
                    unit = normalize_string(unit.get_text().strip())
                    ingredient = ingredient+'||'+unit
                name = ingredientRaw.find(
                    "span", {"class": "wprm-recipe-ingredient-name"})
                if name:
                    name = normalize_string(name.get_text().strip())
                    ingredient = ingredient+'||'+name
                    parsed_ingredients.append(name)
                curatedIngredients.append(ingredient)

        return {"ingredients": curatedIngredients, "parsed_ingredients": parsed_ingredients}

    def ingredients(self):
        ingredients = self.getAllIngredientsRaw()
        return ingredients

    def getAllInstructions(self):
        instructions = self.soup.findAll(
            "div", {"class": "wprm-recipe-instruction-text"})
        if not instructions:
            return
        curatedInstructions = []
        for instruction in instructions:
            if instruction:
                instruction = normalize_string(instruction.get_text().strip())
                curatedInstructions.append(instruction)

        return curatedInstructions

    def instructions(self):
        instructions = self.getAllInstructions()
        return instructions

    def full_nutrition_data(self):
        nutrition = self.soup.find(
            'div', {"class": "wprm-nutrition-label-container-simple"})
        nutritionData = []
        if nutrition:
            nutritionContainer = nutrition.findAll(
                "span", {"class": "wprm-nutrition-label-text-nutrition-container"})
            for nutritionDataRaw in nutritionContainer:
                curatedNutrition = ''
                label = nutritionDataRaw.find(
                    "span", {"class": "wprm-nutrition-label-text-nutrition-label"})
                if label:
                    label = normalize_string(label.get_text().strip())
                    curatedNutrition = label

                value = nutritionDataRaw.find(
                    "span", {"class": "wprm-nutrition-label-text-nutrition-value"})
                if value:
                    value = normalize_string(value.get_text().strip())
                    curatedNutrition = curatedNutrition+'||'+value

                unit = nutritionDataRaw.find(
                    "span", {"class": "wprm-nutrition-label-text-nutrition-unit"})
                if unit:
                    unit = normalize_string(unit.get_text().strip())
                    curatedNutrition = curatedNutrition+'||'+unit

                nutritionData.append(curatedNutrition)
            return nutritionData
        else:
            return

    def images(self):
        imageContainer = self.soup.find(
            "img", {"class": "size-full"})
        if not imageContainer:
            return
        images = ""
        if imageContainer.has_attr("data-lazy-srcset"):
            images = imageContainer["data-lazy-srcset"]
        elif imageContainer.has_attr("data-lazy-src"):
            images = imageContainer["data-lazy-src"]
        if images:
            parsedImage = images.split(" ")[0]
            return parsedImage
        return
