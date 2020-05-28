
# -*- coding: utf-8 -*-
import re

volumeUnits = [
    'teaspoon',
    'teaspoons',
    'dessertspoon',
    "dessertspoons",
    "tablespoons",
    'tablespoon',
    'fluid ounce',
    'cup',
    'cups',
    'pint',
    'pints',
    'quart',
    'gallon',
    'gallons',
    'ounces',
    'ounce',
    'lb',
    'pinch',
    'pinchs',
    'strip',
    "bunch",
    "eaches",
    "canned",
    "cans"
    "can whole",
    "jar",
    "pounds",
    "pound",
    "bag",
    "bottle",
    "container",
    "sprig",
    "scoops",
    "quarts",
    "dash",
    "inch",
    "milliliter",
]

extraText = [
    'to',
    "or",
    "for"
]

uselessText = [
    'chopped',
    'enriched',
    "all-purpose",
    "shredded",
    "lukewarm",
    "⅓",
    "optional",
    "warm",
    "degrees",
    "thick",
    "slices",
    "sliced",
    "ounce)",
    "½",
    "¼",
    "⅞",
    "⅔",
    "¾",
    "⅛",
    "¾",
    "peeled",
    "large",
    "sharp",
    "package",
    "medium",
    "evaporated",
    "diced",
    "can",
    "uncooked",
    "hard-cooked",
    "small",
    "prepared",
    "cubes",
    "cubed",
    "firm",
    "bouillon granules",
    "packet",
    "skinless",
    "fresh",
    "minced",
    "grated",
    "for decoration",
    "sliced",
    "crushed",
    "roughly",
    "finely",
    "parts",
    "peel",
    "creamy",
    "shoestring",
    "boiling",
    "from",
    "extra",
    "thinly",
    "packages",
    "®",
    "granular",
    "cracked",
    "cube",
    "finely",
    "mild",
    "-",
    "ripe",
    "cans",
    "refrigerated",
    "container",
    "to taste",
    ")",
    "(",
    "()",
    "thin"
]


def cleanIngrdient(ingredient):
    regex = re.compile(".*?\((.*?)\)")
    textToRemove = re.findall(regex, ingredient)
    if textToRemove:
        ingredient = ingredient.replace(textToRemove[0], "")

    parsedIngredient = ''
    for text in uselessText:
        ingredient.replace(text, "")

    ingredient = ingredient.split(" ")
    for item in ingredient:
        if item in extraText:
            return parsedIngredient.strip()
        if not any(map(str.isdigit, item)):
            if item not in volumeUnits:
                if item not in uselessText:
                    parsedIngredient = parsedIngredient + ' ' + item
    if parsedIngredient:
        return parsedIngredient.strip()
    return


def parseIngredients(ingredientsRaw):
    ingredientList = []
    ingredientsRaw = removeAnds(ingredientsRaw)
    for ingrdientItem in ingredientsRaw:
        parsedIngrdient = cleanIngrdient(ingrdientItem)
        if parsedIngrdient and parsedIngrdient not in ingredientList:
            ingredientList.append(parsedIngrdient)
    return ingredientList


def removeAnds(ingredientsRaw):
    ingredientList = []
    for ingredient in ingredientsRaw:
        ingredient = ingredient.lower()
        splitedIngredient = ingredient.split(',')
        ingredient = splitedIngredient[0]
        if len(splitedIngredient) > 1 and "chicken" in splitedIngredient[1]:
            ingredientList.append("chicken")
        else:
            if "and" in ingredient:
                splitedIngredient = ingredient.split(" and ")
                for item in splitedIngredient:
                    if len(item) > 0:
                        ingredientList.append(item.strip())
            elif len(ingredient) > 0:
                ingredientList.append(ingredient.strip())
    return ingredientList


def parseIngredientsToCreateList(ingredientsRaw):
    ingredientList = []
    for ingrdientItem in ingredientsRaw:
        parsedIngrdient = cleanIngrdient(ingrdientItem)
        ingredientList.append({"parsedIngrdient": parsedIngrdient,
                               "ingrdientItem": ingrdientItem})
    return ingredientList
