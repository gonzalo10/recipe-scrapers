# -*- coding: utf-8 -*-
from runScraper import scrapeRecipeUrl, scrapeIngredientsList
import xml.etree.ElementTree as ET
tree = ET.parse('../all-recipes-xmls/recipedetail1.xml')
root = tree.getroot()

counter = 0
# for x in range(200):
#     url = root[x][0].text
#     recipeTitle = scrapeRecipeUrl(url)
#     print(counter, '%', url)
#     counter = counter + 1

totalIngredients = 0
for x in range(10000):
    url = root[x][0].text
    Ningrdients = scrapeIngredientsList(url)
    totalIngredients = totalIngredients + Ningrdients
    counter = counter + 1
    print(counter, '%', url)
    print("parsedIngredients = ", totalIngredients)
