from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, get_yields


class Yummly(AbstractScraper):

    @classmethod
    def host(self):
        return 'yummly.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def attribution(self):
        creator = self.soup.find('span', {'class': 'attribution'})
        return creator.get_text()

    def ratings(self):
        raitingContainter = self.soup.find(
            'a', {'class': 'recipe-details-rating'})
        stars = raitingContainter.findAll('span', {"class": "full-star"})
        numberOfRaitings = raitingContainter.findAll(
            'span', {"class": "count"})[0].get_text()
        return {"raiting": len(stars), "nRaitings": normalize_string(numberOfRaitings)}

    def mainImage(self):
        imageData = self.soup.find('img', {'class': 'recipe-image'})
        return imageData['src']

    def total_time(self):
        return get_minutes(
            self.soup.find('div', {'class': 'recipe-summary-item unit'})
        )

    def yields(self):
        return get_yields(
            self.soup.find('div', {'class': 'servings'}
                           ).find('input').get('value')
        )

    def ingredients(self):
        ingredients = self.soup.findAll(
            'li',
            {'class': "IngredientLine"}
        )
        ingredientList = []
        for ingredient in ingredients:
            value = []
            for span in ingredient.select("span[class^=amount],span[class^=unit],span[class^=ingredient]"):
                text = normalize_string(span.get_text())
                value.append(text)
            ingredientList.append(value)
        return ingredientList

    def nutrition(self):
        nutritionTable = self.soup.findAll(
            'div',
            {'class': "recipe-nutrition-full not-shown"}
        )
        nutritionData = nutritionTable[0].find_all('tr')
        parsedNutritionData = []
        for data in nutritionData:
            rawName = data.find('span')
            rawValue = data.find('span', {'class': "font-number"})
            rawPercentage = data.find('span', {'class': "percent font-number"})

            if rawValue and rawName and rawPercentage:
                name = normalize_string(rawName.get_text())
                value = normalize_string(rawValue.get_text())
                percentage = normalize_string(rawPercentage.get_text())
                parsedNutritionData.append([name, value, percentage])

        return parsedNutritionData

    def recipeTags(self):
        tagsList = self.soup.findAll(
            'ul',
            {'class': "recipe-tags"}
        )
        tags = tagsList[0].find_all('li')
        parsedTagList = []
        for tag in tags:
            parsedTagList.append(normalize_string(tag.get_text()))
        return parsedTagList

    def instructions(self):
        instructions = self.soup.find(
            'div', attrs={'class': 'directions-wrapper'})
        return '\n'.join([
            normalize_string(instr.get_text())
            for instr in instructions.findAll('span', attrs={'class': 'step'})
        ]) if instructions is not None else ''
