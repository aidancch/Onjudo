from selenium import webdriver
import time
import os.path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import os.path
import sys

# Path to the ChromeDriver executable. You might need to change this based on your setup.
CHROMEDRIVER_PATH = "chromedriver"



# Initialize the Chrome webdriver
driver = webdriver.Chrome()

# create Chromeoptions instance 
options = webdriver.ChromeOptions() 
 
# adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
 
# exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 
 
# setting the driver path and requesting a page 
driver = webdriver.Chrome(options=options) 
 
# changing the property of the navigator value for webdriver to undefined 
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

# Create a request interceptor
def interceptor(request):
    del request.headers['Referer']  # Delete the header first
    request.headers['Referer'] = 'https://www.coches.net/'
    request.headers['method'] = 'GET'

# Set the interceptor on the driver
driver.request_interceptor = interceptor



# Navigate to Google
a = 1

url = "https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.31605737020666%2C%22east%22%3A-122.0544454317301%2C%22south%22%3A37.32629838658831%2C%22north%22%3A37.50490613257139%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22sche%22%3A%7B%22value%22%3Afalse%7D%2C%22schm%22%3A%7B%22value%22%3Afalse%7D%2C%22schc%22%3A%7B%22value%22%3Afalse%7D%2C%22schu%22%3A%7B%22value%22%3Afalse%7D%2C%22sch%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22pagination%22%3A%7B%7D%7D"

# url = "https://www.zillow.com/"

driver.get(f"{url}")



# driver.find_element(By.XPATH, '//*[@id="grid-search-results"]/ul').find_elements(By.TAG_NAME, 'li')[0].find_element(By.TAG_NAME, 'address').text

house_list = driver.find_element(By.XPATH, '//*[@id="grid-search-results"]/ul').find_elements(By.TAG_NAME, 'li')

for house in house_list:
    print(house.find_element(By.TAG_NAME, 'address').text)

breakpoint()