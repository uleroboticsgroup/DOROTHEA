#!/usr/bin/env python3

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

import datetime

def create_conections(meeting, connections):
	"""
	Create connections to Jitmeet

	Creates a "n" number of connections to a meetingcall @ Jitmeet
	Once joined, the connexion remains till expired

	Args:
		meeting(str): URL of the meeting
		connectios(int): Number of connections to create
	"""

	print("Timestamp: " + datetime.datetime.now().strftime("%D  %H:%M:%S"))
	
	# Selenium driver options for Firefox
	firefox_options = Options()
	firefox_options.add_argument("--headless")  #Headless mode
	firefox_options.add_argument("--disable-gpu")  # Required for Linux servers
	firefox_options.add_argument("--no-sandbox")  # Required for Linux servers
	

	for i in range(connections):

		# Creation of webdriver (Firefox)
		driver = webdriver.Firefox(options=firefox_options)
		driver.get(meeting) #Meeting page

		# User creation
		user = f"DOROTHEA-{i}"
		print(f"Joining jitmeet call as {user}")

		# Inputting user and connecting to meeting
		driver.implicitly_wait(8)
		bottom = driver.find_element(by=By.XPATH, value="//input[@id='premeeting-name-input']")
		bottom.send_keys(user)

		driver.implicitly_wait(8)

		bottom.send_keys(Keys.ENTER)
		driver.implicitly_wait(8)


if __name__ == "__main__":
    
    meeting = "https://meet.jit.si/test12gkdfgldfk"
    connections = 3
    
    create_conections(meeting, connections)
