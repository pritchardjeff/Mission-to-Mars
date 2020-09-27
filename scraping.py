# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
import numpy as np


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere_images": hemisphere_image_urls(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_image_urls():
    # Visit Url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    browser.visit(url)

    hemisphere_image_urls = []

    html = browser.html
    soup_hemi = soup(html, 'html.parser')

    hemisphere_names = []

    results = soup_hemi.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

    for name in hemispheres:
        hemisphere_names.append(name.text)

    # Search for links
    link_results = results[0].find_all('a')
    links = []

    for link in link_results:
        if (link.img):
            
            link_url = 'https://astrogeology.usgs.gov/' + link['href']
            
            hemisphere_image_urls.append(link_url)
    
    img_jpg = []

    for url in hemisphere_image_urls:
        
        browser.visit(url)
        
        html_sub = browser.html
        soup_jpg = soup(html_sub, 'html.parser')
        
        jpg_image_link = soup_jpg.find_all('img', class_='wide-image')
        img_path = jpg_image_link[0]['src']
        
        img_link = 'https://astrogeology.usgs.gov/' + img_path
        
        img_jpg.append(img_link)
    
    
    mars_hemisphere_zip = zip(img_jpg, hemisphere_names)

    hemisphere_image_urls = []

    for img, title in mars_hemisphere_zip:
        
        mars_title = {}
        
        mars_title['img_jpg'] = img
        mars_title['title'] = title
        
        hemisphere_image_urls.append(mars_title)
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
