#Trevor O'Hearn
#5/6/2020
#Python file for webscraping methods


#installs
#!pip install Selenium

import Selenium as sl
from bs4 import BeautifulSoup
import requests

#Get webpage
page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
bs = BeautifulSoup(page.content, 'html.parser')
#requests attributes
#page.status_code
#page.content
#



### SELENIUM METHODS ###

### BEAUTIFULSOUP METHODS ###
#beautiful soup methods
#bs.prettify()
#bs.children
#bs.find_all('p')
#bs.find_all('p', class_='example-stuff')
#bs.find('p')
#bs.find() -> finds entire page
#bs.select('div p') -> uses css tags



#given HTML element
#get parent elements

#return specific child elements

#parse text out of given elements

#change webpage to scrape
