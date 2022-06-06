import scrapy
import re
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from scrapy.selector import Selector

#blocking chrome notifcations
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

class Facebook1Spider(scrapy.Spider):
    name = 'facebook1'
    allowed_domains = ['facebook.com']
    start_urls = ['https://www.facebook.com/Zara/reviews']

    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        time.sleep(10)

    def get_selenium_response(self, url):
        self.driver.get('https://www.facebook.com/Zara/reviews')
        time.sleep(5)

        try:
            #accepting cookies
            python_button = self.driver.find_elements_by_xpath('//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]')[0]
            python_button.click()
            time.sleep(10)
        except:
            pass

        #return encoded page that is accessable after the click
        return self.driver.page_source.encode('utf-8')

    def parse(self, response):
        #start scraping username, date and review
        url=response.url
        selenium_response = Selector(text=self.get_selenium_response(url))
        time.sleep(10)

        yield {
            'name': selenium_response.xpath('normalize-space(/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/span/h2/span/strong[1]/span/a)').extract(),
            'content': selenium_response.xpath('normalize-space(/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[3]/div/div)').extract(),
            'date': selenium_response.xpath('normalize-space(/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a)').extract(),
            #'likes': selenium_response.xpath('normalize-space(.//div[@class="content "])').extract(),
            #'comments': selenium_response.xpath('normalize-space(.//div[@class="content "])').extract(),
        }

          #scrolling down the page
        for j in range(0,5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)

        try:
            #closing log in pop up
            button = self.driver.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div')[0]
            button.click()
            time.sleep(10)
        except:
            pass

    
        #scrolling down the page
        #for j in range(0,5):
           # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #time.sleep(10)



   
