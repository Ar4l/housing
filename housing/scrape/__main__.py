from .data import DataBase
from .model import House 
from .scraper import scrape_page

# houses in areas of interest, sorted by newest first 
url = (
	'https://www.funda.nl/zoeken/koop'
	'?selected_area=%5B%22amsterdam'

	'/wijk-oude-pijp%22,%22amsterdam'
	'/wijk-nieuwe-pijp%22,%22amsterdam'
	'/bellamybuurt-noord%22,%22amsterdam'
	'/bellamybuurt-zuid%22,%22amsterdam'
	'/cremerbuurt-oost%22,%22amsterdam'
	'/wg-terrein%22,%22amsterdam'
	'/wijk-overtoomse-sluis%22,%22amsterdam'
	'/hercules-seghersbuurt%22,%22amsterdam'
	'/frans-halsbuurt%22,%22amsterdam'
	'/hemonybuurt%22,%22amsterdam'
	'/sarphatiparkbuurt%22,%22amsterdam'
	'/lizzy-ansinghbuurt%22,%22amsterdam'
	'/van-der-helstpleinbuurt%22,%22amsterdam'
	'/burgemeestertellegenbuurt-west%22,%22amsterdam'
	'/burgemeester-tellegenbuurt-oost%22,%22amsterdam'
	'/diamantbuurt%22%5D'

	'&price=%220-750000%22'
	'&object_type=%5B%22house%22,%22apartment%22%5D'
	'&availability=%5B%22available%22%5D'
	'&sort=%22date_down%22'
)
# given the typo in burgemeester-tellegen, I assume they are 
# also getting buurt information from the CBS.

houses = scrape_page(url)
with DataBase() as db: 
	db.add(*houses)

