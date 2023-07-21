#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import time
import random

def surffing_the_web():

    firefox_options = Options()
    firefox_options.add_argument("--headless")  #Headless mode
    #firefox_options.add_argument("--disable-gpu")  # Required for Linux servers
    #firefox_options.add_argument("--no-sandbox")  # Required for Linux servers

    # Create a new Firefox browser instance with headless options
    driver = webdriver.Firefox(options=firefox_options)

    search_terms_list = [                 
        "Python", "Java Array", "Event Handling", "Exception", "Stackoverflow", "Computer",
        "Hadoop", "Linux", "Printer", "Scanner", "Update", "Documentation", "Testing",
        "Programming", "Software Engineering", "Software Architecture", "Distributed System",
        "Word", "Excel formula", "Mechanical Keyboard", "Mathematical Induction", "Petabyte",
        "NAS Storage", "Server", "Office", "Compiler", "Eclipse", "Sorting Algorithm",
        "Logarithm", "Algorithm", "Bugfix", "Openstack", "Support", "Command", "Readme",
        "Free Download", "Licence", "Guideline", "Best Practice", "Coding", "JavaScript",
        "Firefox", "Git", "Training", "Repository", "Authorization", "Bash", "Class Path",
        "Plugin", "Error", "Automation", "Requirements Engineering", "Contract",
        "Design Pattern", "Registry", "Assembler", "C++", "Cloud", "Notice", "Infrastructure",
    ]

    for search_term in search_terms_list:
        
        print(f"Search term: {search_term}")
        driver.get(f"https://duckduckgo.com/?q={search_term}")
        
        driver.implicitly_wait(8)

        hrefs = []
        for n in range(0, random.randint(1, 3)):

            web = driver.find_element(by=By.XPATH, value=f"//article[@id='r1-{n}']//a[@class='eVNpHGjtxRBq_gLOfGDr LQNqh2U1kzYxREs65IJu']")
            driver.implicitly_wait(8)
            hrefs.append(web.get_attribute('href'))
            driver.implicitly_wait(5)
        
        for href in hrefs:

            print(f"\t- Visiting: {href}")
            driver.get(href)
            driver.implicitly_wait(8)
            #time.sleep(1)

        
    # Quitting
    driver.quit()


if __name__ == '__main__':
    surffing_the_web()