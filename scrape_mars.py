# coding: utf-8
# # Mission to Mars

# Dependencies
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from selenium import webdriver


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_info = {}


    # ## NASA Mars News
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    # Scrape the page into soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Collect the latest News Title
    news_title = soup.find("div", class_="content_title").get_text()
    mars_info["news_title"] = news_title

    # Collect the latest News Paragraph Text
    news_p = soup.find("div", class_="article_teaser_body").get_text()
    mars_info["news_paragraph"] = news_p


    # ## JPL Mars Space Images - Featured Image
    # Visit the NASA JPL site 
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(2)

    # Navigate the site to find the full .jpg URL
    browser.find_by_css("a#full_image.button.fancybox").click()
    time.sleep(2)
    browser.find_by_css("div.buttons a.button").click()
    time.sleep(2)
    browser.find_by_css("img.main_image").click()
    time.sleep(2)

    # Scrape the page into soup
    html2 = browser.html
    soup2 = bs(html2, "html.parser")

    # Find the image URL for the current Featured Mars Image
    featured_image_url = soup2.find("img")["src"]
    mars_info["featured_image_url"] = featured_image_url


    # ## Mars Weather
    # Visit the Mars Weather Twitter account 
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    time.sleep(2)

    # Scrape the page into soup
    html3 = browser.html
    soup3 = bs(html3, "html.parser")

    # Find the tweet text for the weather report
    mars_weather = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    mars_info["mars_weather"] = mars_weather


    # ## Mars Facts
    # Visit the Mars Facts webpage
    url4 = "https://space-facts.com/mars/"
    browser.visit(url4)

    # Use Pandas to scrape the table containing facts about the planet
    mars_facts_table = pd.read_html(url4)
    mars_facts_table[0]

    # Data cleanup
    mars_facts = mars_facts_table[0]
    mars_facts.columns = ["Description", "Value"]
    mars_facts.set_index("Description", inplace=True)

    # Use Pandas to convert the data to a HTML table string
    mars_facts_html = mars_facts.to_html()
    mars_facts_html = mars_facts_html.replace('\n', '')

    return mars_info
