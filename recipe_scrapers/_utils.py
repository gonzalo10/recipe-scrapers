# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup


TIME_REGEX = re.compile(
    r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H|óra))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M|perc))?'
)

SERV_REGEX_NUMBER = re.compile(
    r'(\D*(?P<items>\d+)?\D*)'
)

SERV_REGEX_ITEMS = re.compile(
    r'\bsandwiches\b |\btacquitos\b | \bmakes\b', flags=re.I | re.X
)

SERV_REGEX_TO = re.compile(
    r'\d+(\s+to\s+|-)\d+', flags=re.I | re.X
)


def scrape_second_website(url):
    page_data = requests.get(url).content
    soup = BeautifulSoup(page_data, "html.parser")

    return soup


def get_minutes(element):
    try:
        if isinstance(element, str):
            tstring = element
        else:
            tstring = element.get_text()
        if '-' in tstring:
            # sometimes formats are like this: '12-15 minutes'
            tstring = tstring.split('-')[1]
        if 'h' in tstring:
            tstring = tstring.replace('h', 'hours') + 'minutes'
        matched = TIME_REGEX.search(tstring)

        minutes = int(matched.groupdict().get('minutes') or 0)
        minutes += 60 * int(matched.groupdict().get('hours') or 0)

        return minutes
    except AttributeError:  # if dom_element not found or no matched
        return 0


def get_yields(element):
    """
    Will return a string of servings or items, if the receipt is for number of items and not servings
    the method will return the string "x item(s)" where x is the quantity.
    :param element: Should be BeautifulSoup.TAG, in some cases not feasible and will then be text.
    :return: The number of servings or items.
    """
    try:

        if isinstance(element, str):
            tstring = element
        else:
            tstring = element.get_text()

        if SERV_REGEX_TO.search(tstring):
            tstring = tstring.split(SERV_REGEX_TO.split(tstring)[1])[1]

        matched = SERV_REGEX_NUMBER.search(
            tstring).groupdict().get('items') or 0
        servings = "{} serving(s)".format(matched)

        if SERV_REGEX_ITEMS.search(tstring) is not None:
            # This assumes if object(s), like sandwiches, it is 1 person.
            # Issue: "Makes one 9-inch pie, (realsimple-testcase, gives "9 items")
            servings = "{} item(s)".format(matched)

        return servings

    except AttributeError as e:  # if dom_element not found or no matched
        print("get_serving_numbers error {}".format(e))
        return ''


def normalize_string(string):
    return re.sub(
        r'\s+', ' ',
        string.encode('utf-8', "ignore")
        .replace('\u00be', ' ').replace('\u2009', ' ')
        .replace('\u215b', ' ').replace('\u00bd', ' ')
        .replace('\u00be', ' ').replace('\u00ae', ' ')
        .replace('\xc2', ' ').replace('\xbc', ' ')
        .replace('\xbd', ' ').replace('\xbe', ' ')
        .replace('\xae', ' ').replace('\xbe', ' ')
        .replace('\xe2', ' ').replace('\x85', ' ')
        .replace('\x93', ' ').replace('\x94', ' ')
        .replace('\xa0', ' ').replace('\x9b', ' ')
        .replace('\xb0', ' ').replace('\x80', ' ')
        .replace('\x99', ' ').replace('\x81', ' ')
        .replace('\x84', ' ').replace('\x9c', ' ')
        .replace('\x9d', ' ').replace('\x8b', ' ')

    )
