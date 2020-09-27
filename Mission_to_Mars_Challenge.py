# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# %%
# Windows users
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# %%
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem.find("div", class_='content_title')


# %%
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### Featured Images

# %%
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# %%
# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# %%
# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# %%
# the 0 pulls the first table it reads
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# %%
df.to_html()


# %%
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# %%
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
soup_hemi = soup(html, 'html.parser')

hemisphere_names = []

# Search for the names of all four hemispheres
results = soup_hemi.find_all('div', class_="collapsible results")
hemispheres = results[0].find_all('h3')

# Get text and store in list
for name in hemispheres:
    hemisphere_names.append(name.text)

# Search for links
link_results = results[0].find_all('a')
links = []

for link in link_results:
    if (link.img):
        
        # then grab the attached link
        link_url = 'https://astrogeology.usgs.gov/' + link['href']
        
        # Append list with links
        hemisphere_image_urls.append(link_url)


# %%
img_url = []

for url in hemisphere_image_urls:
    
    # Click through each link
    browser.visit(url)
    
    html_sub = browser.html
    soup_jpg = soup(html_sub, 'html.parser')
    
    # Scrape each page for the relative image path
    jpg_image_link = soup_jpg.find_all('img', class_='wide-image')
    img_path = jpg_image_link[0]['src']
    
    # Combine the reltaive image path to get the full url
    img_link = 'https://astrogeology.usgs.gov/' + img_path
    
    # Add full image links to a list
    img_url.append(img_link)

img_url


# %%
# Zip the names and images together
mars_hemisphere_zip = zip(img_url, hemisphere_names)

hemisphere_image_urls = []

# Iterate through the zipped object
for img, title in mars_hemisphere_zip:
    
    mars_title = {}
    
    mars_title['img_url'] = img
    mars_title['title'] = title
    
    
    # Append the list with dictionaries
    hemisphere_image_urls.append(mars_title)


# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# %%
browser.quit()


# %%



