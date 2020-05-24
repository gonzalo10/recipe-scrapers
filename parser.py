
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
    "inch"
]

extraText = [
    'to',
    "or"
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
    "granular"
]


def cleanIngrdient(ingredient):
    regex = re.compile(".*?\((.*?)\)")
    textToRemove = re.findall(regex, ingredient)
    if textToRemove:
        ingredient = ingredient.replace(textToRemove[0], "")
        ingredient = ingredient.replace("(", "")
        ingredient = ingredient.replace(")", "")
    if "chicken" in ingredient:
        return "chicken"
    removedDetails = ingredient.split(',')[0].split(' ')
    parsedIngredient = ''
    for item in removedDetails:
        if item in extraText:
            return parsedIngredient.strip()
        if not any(map(str.isdigit, item)) and item not in volumeUnits and item not in uselessText:
            parsedIngredient = parsedIngredient + ' ' + item
    if parseIngredients:
        return parsedIngredient.strip()
    return


def parseIngredients(ingredientsRaw):
    ingredientList = []
    for ingrdientItem in ingredientsRaw:
        parsedIngrdient = cleanIngrdient(ingrdientItem)
        ingredientList.append(parsedIngrdient)
    return ingredientList


def parseIngredientsToCreateList(ingredientsRaw):
    ingredientList = []
    for ingrdientItem in ingredientsRaw:
        parsedIngrdient = cleanIngrdient(ingrdientItem)
        ingredientList.append({"parsedIngrdient": parsedIngrdient,
                               "ingrdientItem": ingrdientItem})
    return ingredientList
