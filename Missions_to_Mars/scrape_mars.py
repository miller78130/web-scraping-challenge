# Seting up dependacies for MongoDB and Flask application

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo
import requests
import time

def init_browser():
    executable_path = {"executable_path": "C:\\Program Files\\chromdriver_win32\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News define and retrive
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    mysoup = bs(html, "html.parser")
    # Scrape for title and text
    news_title = mysoup.find('li', class_='slide').find('div', class_='content_title').text
    news_p = mysoup.find('li', class_='slide').find('div', class_='article_teaser_body').text

    # Mars Images define and retrive
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    



    # Mars Facts
    # readtables on mars facts page
    facts_url = 'https://space-facts.com/mars/'
    fact_table = pd.read_html(facts_url)
    # Filter to table I want to work with
    fact_df = fact_table[0]
    # Rename columns
    fact_df.columns = ["Description", "Mars"]
    # Remove Index/set new
    facts = fact_df.set_index("Description")
    # Convert to html string & clean
    html_facts = facts.to_html()
    html_facts = html_facts.replace('\n', '')

    # Mars Hemispheres
    # Set up for retriving browser
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')
    # Set up for dictionaries
    hemi_image_urls = []
    # Original url for images
    base_url ='https://astrogeology.usgs.gov/'
    # Soup set up
    hemis = hemi_soup.find_all('div', class_='item')
    # Loop set up for each title and image
    for hemi in hemis:
        title = hemi.find('h3').text
        browser.links.find_by_partial_text("Hemisphere Enhanced")
        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
        imgs_url = img_soup.find('img', class_="thumb")['src']
        image_url = base_url+imgs_url
        hemi_image_urls.append({"title": title, "image_url": image_url})

    # Close browser after scraping
    browser.quit()
    
    # Creating dictionary for all of the scrapped info
    mars_data={
        "Mars_News_Headline": news_title,
        "Mars_News_Tease": news_p,
        "Featured_Mars_Image": "N/A",
        "Mars_Facts": html_facts,
        "Mars_Hemispheres": hemi_image_urls,
    }
    return mars_data

if __name__ == "__main__":
    data = scrape()
    print(data)