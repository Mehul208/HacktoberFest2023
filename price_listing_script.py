from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from pynput.keyboard import Key, Controller
import time
import re

URL = 'https://www.myntra.com/'
driver = None
items = []
keyboard = Controller()
opt = Options() #-------------------setting defaults of the browsers--------------------
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
opt.add_argument('--ignore-certificate-errors')
opt.add_argument('--ignore-ssl-errors')
search_for = None
budget_price = None

def get_inputs():
	global search_for, budget_price
	search_for = input("Product Search Name >>> ")
	budget_price = input("Your Budget >>> ")
	print("Starting App ...")
	time.sleep(2)

def start_browser():
	global driver
	driver = webdriver.Chrome(chrome_options=opt,service_log_path='NUL')
	driver.get(URL)
	WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
	time.sleep(2)


def enter_product():
	site_search = driver.find_element_by_class_name('desktop-searchBar')
	# search_string = input("Please enter the product you want to scrap : ")
	time.sleep(2)
	site_search.click()
	site_search.send_keys(str(search_for))
	# site_search.submit()
	keyboard.tap(Key.enter)
	time.sleep(2)


def get_products_info():
	items_list = []
	pr_brand = driver.find_elements_by_class_name('product-brand')
	pr_price = driver.find_elements_by_class_name('product-price')
	print("Brands: " + str(len(pr_brand))) 
	for i in range(len(pr_brand)):
		info = {"brand": pr_brand[i].get_attribute('innerText'), "price":pr_price[i].get_attribute('innerText')}
		items_list.append(info)
	return items_list


def get_price(p):
	search_pattern = re.search(r"(?:\. )(\w*)(?:R)|(?:\. )(\w*)", p)
	if search_pattern:
	    if search_pattern.group(1)!= None:
		    return str(search_pattern.group(1))
	    elif search_pattern.group(2)!= None:
		    return str(search_pattern.group(2))
	else:
		return None


def print_products(items):
	for i in range(len(items)):
		pr = get_price(items[i]["price"])
		try:
			if int(pr) <= int(budget_price):
				print("\n\t\t\t"+str(items[i]["brand"])+"\t\t\t"+str(items[i]["price"]))
		except TypeError as e:
			continue


get_inputs()
start_browser()
enter_product()
print_products(get_products_info())
