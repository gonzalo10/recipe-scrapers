from recipe_scrapers import scrape_me

# give the url as a string, it can be url from any site listed below
scraper = scrape_me(
    'https://www.yummly.com/recipe/Cajun-Shrimp-Pasta-2025206')


scraper.title()
scraper.ratings()
scraper.attribution()
scraper.mainImage()
scraper.recipeTags()
scraper.nutrition()
scraper.ingredients()
scraper.total_time()
scraper.yields()
scraper.ingredients()
scraper.instructions()
scraper.image()
scraper.links()
