# Clustering Amsterdam house market on:
# 1. Median price 
# 2. n Sold/month
import re, dataclasses as dc, datetime as dt

from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement

@dc.dataclass 
class Address: 
	street:   str
	number:   str
	postcode: str
	city:     str
	# todo: buurt

	def __str__(self): 
		return f'{self.street} {self.number}'

	def __hash__(self): 
		return hash((self.street, self.number))

@dc.dataclass
class House: 
	url:     str
	img_url: str
	address: Address

	price:   int
	sqm:     int
	beds:    int
	energy:  str

	# todo: listed_since: dt.datetime  
	seen:         dt.datetime = dt.datetime.now()

	def __init__(self, web_element: WebElement):
		''' 
		Given html webelement, extract all the necessary info 
		note: need to follow link to extract the listed_since date
		'''

		house = BeautifulSoup(web_element.get_attribute('innerHTML'), features='lxml')
		#	 element.div.div.div (flex) has 
		#	 div (relative items-center): the image
		#	 div (relative flex) has 
		#	 a.div(flex).span (truncate)		address 
		#	 a.div(truncate)					postcode & city 
		#	 div(mt-2).div(truncate)	price 
		#	 div(flex).ul 
		#		li[1].span						sqm 
		#		li[2].span						bed s
		#		li[3].span						energy
		# todo: listed date

		self.url = 'https://funda.nl' + house.find('a')['href']
		self.img_url = house.find('img')['srcset'].split(', ')[-1].split()[0]

		_address_line = house.find('span', class_='truncate').get_text()
		street = re.search('([a-zA-Z]+\s)*[a-zA-Z]+', _address_line)[0]
		number = re.search('\d+.*', _address_line)[0]
		postcode, city = house.find('div', class_='truncate').get_text().split()
		self.address = Address(street, number, postcode, city)

		self.price = int(re.search(
			'[\d\.]*\d', 
			house.find('div', class_='mt-2').get_text()
		)[0].replace('.', ''))

		_attrs = house.find('ul').find_all('li')
		self.sqm = int(_attrs[0].span.get_text().split()[0])
		self.beds = int(_attrs[1].span.get_text())
		self.energy = _attrs[2].span.get_text() if len(_attrs) > 2 else None

	def __str__(self): 

		red = lambda s: f'\033[0;31m{s}\033[0m' 
		yellow = lambda s: f'\033[0;33m{s}\033[0m' 
		green = lambda s: f'\033[0;32m{s}\033[0m' 
		gray = lambda s: f'\033[0;90m{s}\033[0m' 

		price = (
			gray   if self.price > 600_000 else
			red    if self.price > 550_000 else
			yellow if self.price > 500_000 else
			green
		)(f'{self.price//1000:4,}')

		sqm = (
			gray   if self.sqm < 30 else
			red    if self.sqm < 40 else
			yellow if self.sqm < 50 else
			green
		)(f'{self.sqm:3}')

		energy = (
			gray if self.energy is None else 
			green if any(l in self.energy for l in 'ABC') else
			yellow if any(l in self.energy for l in 'DE') else
			red 
		)(f'{self.energy if self.energy is not None else "na":>2}')

		return f'{price} {sqm} {energy} \t{self.address}'

	def __hash__(self): 
		return hash(vars(self).values())

