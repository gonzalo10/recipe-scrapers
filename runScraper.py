from recipe_scrapers import scrape_me
import json
from parser import parseIngredients, parseIngredientsToCreateList

titleUslessWords = [
    "and"
]


def createSearchableKeys(ingredients, title, tags):
    searchableKeys = []
    for ingredient in ingredients:
        if not ingredient:
            return
        if ingredient not in searchableKeys:
            searchableKeys.append(ingredient)

        splitedIngredient = ingredient.split(" ")

        for ingredientWord in splitedIngredient:
            if ingredientWord not in searchableKeys:
                searchableKeys.append(ingredientWord)

    title = title.split(" ")

    for titleWord in title:
        titleWord = titleWord.lower()
        if titleWord not in titleUslessWords:
            if titleWord not in searchableKeys:
                searchableKeys.append(titleWord)

    for tag in tags:
        tag = tag.lower()
        tag = tag.strip()
        if tag not in searchableKeys:
            searchableKeys.append(tag)
        splitedTag = tag.split(" ")
        for uniqueTag in splitedTag:
            uniqueTag = uniqueTag.strip()
            if uniqueTag not in searchableKeys:
                searchableKeys.append(uniqueTag)

    return searchableKeys


def scrapeRecipeUrl(url):
    scraper = scrape_me(url)

    rawIngredients = scraper.ingredients()
    ingredients = parseIngredients(rawIngredients['parsed_ingredients'])
    tags = scraper.tags()
    title = scraper.title()
    image = scraper.images()
    recipe_summary = scraper.recipe_summary()
    isRecipe = scraper.isRecipe()
    if not isRecipe:
        return
    data = {}
    data['title'] = title
    data['img_src'] = image
    data['url'] = url
    data['tags'] = tags
    data['raiting'] = scraper.raiting()
    data['instructions'] = scraper.instructions()
    data['full_nutrition_data'] = scraper.full_nutrition_data()
    data['parsed_ingredients'] = ingredients
    data['ingredients'] = rawIngredients['ingredients']
    data['recipe_summary'] = recipe_summary
    data['searchable_keys'] = createSearchableKeys(ingredients, title, tags)

    if not image or not recipe_summary:
        return "no image, not saved"
    if scraper.raiting() == 0:
        return 'no raiting, not saved'

    savedPath = '../recipes/'+title+'.json'

    with open(savedPath, 'w') as outfile:
        json.dump(data, outfile)
    return title


def test(url):
    scraper = scrape_me(url)

    rawIngredients = scraper.ingredients()
    ingredients = parseIngredients(rawIngredients['parsed_ingredients'])
    tags = scraper.tags()
    print(tags)

    return


def scrapeIngredientsList(url):
    scraper = scrape_me(url)
    rawIngredients = scraper.ingredients()

    ingredients = parseIngredientsToCreateList(rawIngredients)
    data = {}

    data['parsed_ingredients'] = ingredients

    savedPath = '../ingredientsList2.json'

    with open(savedPath, 'r+') as file:
        data = json.load(file)
        for ingredient in ingredients:
            data['ingredients'].append(ingredient)
        file.seek(0)
        json.dump(data, file)
    return len(ingredients)
