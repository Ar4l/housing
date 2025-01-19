from .model import House

# todo: consider selenium-stealth
from selenium import webdriver
from selenium.webdriver.common.by import By 

def scrape_page(url: str): 

	driver = webdriver.Safari()
	driver.implicitly_wait(2)
	driver.get(url)

	house_list = (driver
		.find_element(By.CLASS_NAME, 'gap-3') # get the list 
		.find_elements(By.XPATH, './div') # each item in list
	)
	print(f'found {len(house_list)} houses on page')

	houses = [House(web_element) for web_element in house_list]
	for house in houses: print(house)
	return houses

