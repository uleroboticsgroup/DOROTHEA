import selenium, os, time, datetime, random, warnings, sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def main():

	warnings.filterwarnings("ignore", category=DeprecationWarning) 
	print("Timestamp: " + datetime.datetime.now().strftime("%D  %H:%M:%S"))


	options = Options()
	options.headless = True

	profile = webdriver.FirefoxProfile()
	#Habilitamos la camara y el micro
	profile.set_preference ('media.navigator.permission.disabled', True)
	profile.update_preferences()
	conexiones =0

	while conexiones < 4:
		driver = webdriver.Firefox(profile, executable_path='/opt/geckodriver' , options=options)
		driver.maximize_window()
		driver.get("https://meet.jit.si/test12gkdfgldfk")
		print("Cargando jitmeet")
		#Pinchamos en el boton para meternos en la reunion
		x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='prejoin.joinMeeting'][role='button']"))).click()
		conexiones = conexiones +1
		time.sleep(4)


if __name__ == "__main__":
    main()
