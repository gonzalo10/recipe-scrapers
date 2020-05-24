from recipe_scrapers import scrape_me
import json
from parser import parseIngredients, parseIngredientsToCreateList

# give the url as a string, it can be url from any site listed below


def scrapeRecipeUrl(url):
    scraper = scrape_me(url)
    rawIngredients = scraper.ingredients()

    ingredients = parseIngredients(rawIngredients)
    title = scraper.title()
    data = {}
    data['title'] = title
    data['img_src'] = scraper.images()
    data['url'] = url
    data['tags'] = scraper.tags()
    data['raiting'] = scraper.raiting()
    data['instructions'] = scraper.instructions()
    data['full_nutrition_data'] = scraper.full_nutrition_data()
    data['parsed_ingredients'] = ingredients
    data['ingredients'] = scraper.ingredients()
    data['recipe_summary'] = scraper.recipe_summary()

    savedPath = '../recipes/'+title+'.json'

    with open(savedPath, 'w') as outfile:
        json.dump(data, outfile)
    return title


def test(url):
    scraper = scrape_me(url)
    print(scraper.recipe_summary_old())


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
