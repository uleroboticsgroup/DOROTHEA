#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


firefox_options = Options()
firefox_options.add_argument("--headless")  #Headless mode

# Create a new Firefox browser instance with headless options
driver = webdriver.Firefox(options=firefox_options)

# Open Wikipedia's homepage
driver.get("https://www.wikipedia.org")

# Find the search input field by its name and type the search query
search_input = driver.find_element("name", "search")
search_input.send_keys("Python programming")

# Press Enter to perform the search
search_input.send_keys(Keys.ENTER)

# Wait for the search results to load (adjust the wait time as needed)
driver.implicitly_wait(5)

# Close the browser
driver.quit()
