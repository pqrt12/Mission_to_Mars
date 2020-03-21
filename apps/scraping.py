#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

# import pandas
import pandas as pd
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

# executable_path = {'executable_path': get_fullname("chromedriver.exe")}
# browser = Browser('chrome', **executable_path)
# browser.quit()

# return a filename (with path) such that it is accessible.


def get_fullname(filename):
    # as long as it is accessible.
    if os.path.isfile(filename):
        return filename

    # search current working directory.
    cur_working_dir = os.getcwd()
    for i in range(50):
        for (path, dir, files) in os.walk(cur_working_dir):
            if filename in files:
                return os.path.join(path, filename)

        # check parent directory
        parent = os.path.dirname(cur_working_dir)
        if cur_working_dir == parent:
            break
        cur_working_dir = parent

    # did not found, simply return.
    print(f"file {filename} not found !!!")
    return filename


def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path=get_fullname(
        "chromedriver.exe"), headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    return data

# -----------------------------------------------------------------------------
# Headline News


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=2)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            'div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# -----------------------------------------------------------------------------
# Featured Images
# Visit URL


def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    # Use the base URL (from browser) to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# -----------------------------------------------------------------------------
# Facts
# /html/body/div[1]/div[1]/section[2]/aside[1]/div[2]/table
# df = pd.read_html('http://space-facts.com/mars/')[0]
# df.head()


def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())