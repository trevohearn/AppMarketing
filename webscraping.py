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



### REQUESTS ###
#get new page
def getPage(url):
    #add try catch block with error protection
    return requests.get(url)



### SELENIUM METHODS ###

### BEAUTIFULSOUP METHODS ###
#https://www.restapitutorial.com/httpstatuscodes.html
def requestResponse(page):
    code = page.status_code
    cat = code // 100
    spec = code % 100
    if (cat == 4): #client error
        if (spec == 0):
            return 'Client Error'
        elif (spec == 1):
            return 'Unauthorized'
        elif (spec == 2):
            return 'payment required'
        elif (spec == 3):
            return 'forbidden'
        elif (spec == 4):
            return 'not found'
        elif (spec == 5):
            return 'method not found'
        elif (spec == 6):
            return 'not acceptable'
        elif (spec == 7):
            return 'proxy authentication required'
        elif (spec == 8):
            return 'request timeout'
        elif (spec == 9):
            return 'conflict'
        elif (spec == 10):
            return 'gone'
        elif (spec == 11):
            return 'length required'
        elif (spec == 12):
            return 'precondition failed'
        elif (spec == 13):
            return 'reqest entity too large'
        elif (spec == 14):
            return 'request-URI too long'
        elif (spec == 15):
            return 'Unsupported Media Type'
        elif (spec == 16):
            return 'requested range not satisfiable'
        elif (spec == 17):
            return 'expectation failed'
        elif (spec == 18):
            return 'im a teapot (RFC 2324)'
        elif (spec == 20):
            return 'enhance your calm (twitter)'
        elif (spec == 22):
            return 'Unprocessable Entity (WebDAV)'
        elif (spec == 23):
            return 'locked (webDAV)'
        elif (spec == 24):
            return 'Failed dependency (WebDAV)'
        elif (spec == 25):
            return 'reserved for webdav'
        elif (spec == 26):
            return 'upgrade required'
        elif (spec == 28):
            return 'precondition requried'
        elif (spec == 29):
            return 'too many requests'
        elif (spec == 31):
            return 'request header fields too large'
        elif (spec == 44):
            return 'no response (nginx)'
        elif (spec == 49):
            return 'retry with microsoft'
        elif (spec == 50):
            return 'blocked by windows parental controls (microsoft)'
        elif (spec  == 51):
            return 'unavailable for legal reasons'
        elif (spec == 99):
            return 'client closed request (nginx)'
        else:
            return 'unkown client error response'
    elif (cat == 3): #redirection
        if (spec == 0):
            return 'multiple choices'
        elif (spec == 1):
            return 'moved permanently'
        elif (spec == 2):
            return 'found'
        elif (spec == 3):
            return 'see other'
        elif (spec == 4):
            return 'not modified'
        elif (spec == 5):
            return 'use proxy'
        elif (spec == 6):
            return 'unused'
        elif (spec == 7):
            return 'temporary redirect'
        elif (spec == 8):
            return 'permanent redirect (experimental)'
        else:
            return 'redirect with other subcategory'
    elif (cat == 2): #success
        if (spec == 0):
            return 'Success'
        elif (spec == 1):
            return 'Success - created'
        elif (spec == 2):
            return 'Success - Accepted'
        elif (spec == 3):
            return 'Success - Non-Authoritative Information'
        elif (spec == 4):
            return 'Success - No content'
        elif (spec == 5):
            return 'Success - Reset Content'
        elif (spec == 6):
            return 'Success - partial content'
        elif (spec == 7):
            return 'Success - Multi-Status (WebDAV)'
        elif (spec == 8):
            return 'Success - Already Reported (WebDAV)'
        elif (spec == 26):
            return 'Success - IM Used'
        else
            return 'Success - other status code involved'
    elif (cat == 1): #informational
        if (spec == 0):
            return 'Continue'
        elif (spec == 1):
            return 'switching protocols'
        elif (spec == 2):
            return 'processing (webDAV)'
        else:
            return 'general informational other subcategory'
    elif (cat == 5): #Server Error
        if (spec == 0):
            return 'Internal Server Error'
        elif (spec == 1):
            return 'not implemented'
        elif (spec == 2):
            return 'bad gateway'
        elif (spec == 3):
            return 'service unavailable'
        elif (spec == 4):
            return 'gateway timeout'
        elif (spec == 5):
            return 'HTTP Version Not Supported'
        elif (spec == 6):
            return 'variant also negotiates (experimental)'
        elif (spec == 7):
            return 'insufficient storage (WebDAV)'
        elif (spec == 8):
            return 'Loop Detected (WebDAV)'
        elif (spec == 9):
            return 'Bandwidth Limit Exceeded (Apache)'
        elif (spec == 10):
            return 'Not extended'
        elif (spec == 11):
            return 'Network Authentication Required'
        elif (spec == 98):
            return 'Network read timeout error'
        elif (spec == 99):
            return 'network connect timeout error'
        else:
            return 'server error - unknown subcategory'

    else: #unknown code from http status codes
        return 'unknown code error'

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
