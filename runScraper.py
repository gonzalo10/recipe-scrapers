from recipe_scrapers import scrape_me
import json

# give the url as a string, it can be url from any site listed below
scraper = scrape_me(
    'https://www.allrecipes.com/recipe/79543/fried-rice-restaurant-style/')

title = scraper.title()
data = {}

data['title'] = scraper.title()
data['tags'] = scraper.tags()
data['raiting'] = scraper.yields()
data['instructions'] = scraper.instructions()
data['full_nutrition_data'] = scraper.full_nutrition_data()
data['ingredients'] = scraper.ingredients()
data['recipe_summary'] = scraper.recipe_summary()

# print('title', scraper.title())
# print('tags', scraper.tags())
# print('raiting', scraper.raiting())
# print('instructions', scraper.instructions())
# print('full_nutrition_data', scraper.full_nutrition_data())
# print('ingredients', scraper.ingredients())
# print('recipe_summary', scraper.recipe_summary())

with open('../recipies/'+title+'.json', 'w') as outfile:
    json.dump(data, outfile)
