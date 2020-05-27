# -*- coding: utf-8 -*-
from runScraper import scrapeRecipeUrl, scrapeIngredientsList
import xml.etree.ElementTree as ET
tree = ET.parse('../sitemaps/healthyfitnessmeals.xml')
root = tree.getroot()

counter = 0
for x in range(len(root)):
    url = root[x][0].text
    print(counter, '%', url)
    recipeTitle = scrapeRecipeUrl(url)
    print("success")
    counter = counter + 1

# totalIngredients = 0
# for x in range(10000):
#     url = root[x][0].text
#     Ningrdients = scrapeIngredientsList(url)
#     totalIngredients = totalIngredients + Ningrdients
#     counter = counter + 1
#     print(counter, '%', url)
#     print("parsedIngredients = ", totalIngredients)
