import os
import unittest

from recipe_scrapers.bbcfood import BBCFood


class TestBBCFoodScraper(unittest.TestCase):
    def setUp(self):
        # tests are run from tests.py
        with open(os.path.join(
            os.getcwd(),
            'recipe_scrapers',
            'tests',
            'test_data',
            'bbc_food.html'
        )) as file_opened:
            self.harvester_class = BBCFood(file_opened, test=True)

    def test_host(self):
        self.assertEqual(
            'bbc.co.uk',
            self.harvester_class.host()
        )

    def test_publisher_site(self):
        self.assertEqual(
            'http://bbc.co.uk/',
            self.harvester_class.publisher_site()
        )

    def test_title(self):
        self.assertEqual(
            self.harvester_class.title(),
            'Irish cream and chocolate cheesecake'
        )

    def test_total_time(self):
        self.assertEqual(
            130,
            self.harvester_class.total_time()
        )

    def test_ingredients(self):
        self.assertListEqual(
            [
                '100g/3½oz butter',
                '250g/8¾oz digestive biscuits, crushed',
                '600g/1lb 5oz cream cheese',
                '25ml/1fl oz Baileys or other Irish cream liqueur',
                '100ml/3½oz icing sugar',
                '300ml/10½oz double cream, whipped',
                '100g/3½oz grated chocolate',
                '200ml/7¼oz double cream, whipped',
                'cocoa powder, to dust'
            ],
            self.harvester_class.ingredients()
        )

    def test_instructions(self):
        return self.assertEqual(
            'Melt the butter in a pan and add the crushed digestive biscuits. Mix well until the biscuits have absorbed all the butter.\nRemove from the heat and press into the bottom of a\n lined 18cm/7in springform tin. Place in the refrigerator and allow to \nset for one hour.\nMeanwhile, prepare the filling. Lightly whip the \ncream cheese then beat in the Irish cream and icing sugar. Fold in the \nwhipped cream and grated chocolate. When smooth, spoon evenly onto the \nbiscuits.\nRefrigerate and allow to set for a further two \nhours. Once set, remove and decorate with whipped cream and cocoa powder\n dusted over the top. Serve.',
            self.harvester_class.instructions()
        )
