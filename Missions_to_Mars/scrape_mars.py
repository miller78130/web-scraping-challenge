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

# NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    mysoup = bs(html, "html.parser")
    # Scrape for title and text
    news_title = mysoup.find('li', class_='slide').find('div', class_='content_title').text
    news_p = mysoup.find('li', class_='slide').find('div', class_='article_teaser_body').text

# Mars Images define and retrive
    #image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    



# Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    fact_table = pd.read_html(facts_url)
    # Filter
    fact_df = fact_table[0]
    # Rename columns
    fact_df.columns = ["Description", "Mars"]
    # Remove Index/set new
    facts = fact_df.set_index("Description")
    # Convert to html string & clean
    html_facts = facts.to_html()
    html_facts = html_facts.replace('\n', '')

# Mars Hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)    
    # Updating Beautiful Soup
    html = browser.html
    soup = bs(html, "html.parser")
    #Find image titles
    hemi_image_urls = []
    # Base image url
    base_img_url = "https://astrogeology.usgs.gov/"
    # Set up soup
    hemis = soup.find_all('div', class_='item')
    # Setting up loop to get title and url
    for hemi in hemis:
        title = hemi.find('h3').text    
        browser.links.find_by_partial_text("Hemisphere Enhanced")
        jpg_html = browser.html
        jpg_soup = bs(jpg_html, "html.parser")
        jpgs_url = jpg_soup.find("img", class_="wide-image")['src']    
        images_url = base_img_url+jpgs_url
        hemi_image_urls.append({"title": title, 'img_url': images_url})

# Close browser after scraping
    browser.quit()
    
# Creating dictionary
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