#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

# import pandas
import pandas as pd
import datetime as dt
import os

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
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
    # remove last punctuation (easy to expand)
    punctuations = [':', '.', '?']
    df['description'] = list(
        map(lambda s: s[:-1] if s[-1] in punctuations else s, df['description']))
    # Convert dataframe into HTML format, add bootstrap
    html = df.to_html(index=False, justify='center', classes=[
                      'table table-striped table-bordered table-hover table-condensed'])

    return html

# -----------------------------------------------------------------------------
#  Mars Hemispheres

# get the full size image url: class="container" / class="wide-image"
def get_hemi_img_url(img_soup):
    img_url = ""
    for container in img_soup.find_all(class_='container'):
        t = container.find(class_='wide-image')
        if t:
            img_url = t.get('src')
            break
    return img_url

# get the title: class="content" / class="title"
def get_hemi_title(img_soup):
    title = ""
    for content in img_soup.find_all(class_='content'):
        if not title:
            t = content.find(class_='title')
            if t:
                title = t.get_text()
            break
    return title


def mars_hemispheres(browser):
    # Visit the usgs mars site
    usgs_base_url = 'https://astrogeology.usgs.gov'
    usgs_url = f'{usgs_base_url}/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    # Optional delay for loading the page
    browser.is_element_present_by_id("product-section", wait_time=10)
    #time.sleep(0.1)

    # get the href for splinter find.
    prod_soup = BeautifulSoup(
        browser.html, 'html.parser').find(id='product-section')

    # thumbs url
    thumbs = []
    for thumb in prod_soup.find_all(class_='thumb'):
        thumbs.append(thumb.get('src'))
    # hrefs
    hrefs = []
    for a in prod_soup.find_all('a', href=True):
        if a['href'] in hrefs:
            continue
        hrefs.append(a['href'])

    # get the img_urls, titles.
    img_urls = []
    for thumb, href in zip(thumbs, hrefs):
        # Optional delay for loading the page
        browser.visit(usgs_url)
        browser.is_element_present_by_id("product-section", wait_time=10)
        #time.sleep(0.1)
        browser.links.find_by_href(href)[1].click()

        # up to 10 sec.
        browser.is_element_present_by_id("wide-image", wait_time=10)
        img_soup = BeautifulSoup(browser.html, 'html.parser')
        # get title
        title = get_hemi_title(img_soup)
        # get url
        img_url = get_hemi_img_url(img_soup)
        # save it
        if (title and img_url):
            img_urls.append(
                {'img_url': usgs_base_url + img_url, 'title': title, 'thumb': usgs_base_url + thumb})

    n = len(img_urls)
    print(f"get {n} Mars hemispeheres images.")
    return img_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
