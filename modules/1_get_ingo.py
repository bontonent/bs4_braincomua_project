from load_django import *
from parser_app.models import *

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

# necessary data (maybe better call preview all items with None)
product = {}

headers = {
	"cookie" :	"PHPSESSID=9fk9utinhihpulrc4t50krgk05; Lang=ua; CityID=23562; entryRef=docs.google.com; entryPage=%2Fukr%2FMobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html; _gcl_au=1.1.1908483809.1772551173; sc=9B71D166-0453-2A73-CF90-378A2F5DC148"
	, "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
} # HTTP/3
urls = ["https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"]

for url in urls:
	r = requests.get(url, headers=headers)
	#print(r)
	soup = BeautifulSoup(r.text, "lxml")
	
	try: # Product article = Code product
		product["Product_article"] = soup.find("div", attrs={"class": "product-code-num"}).find_all("span")[1].text
	except AttributeError:
		product["Product_article"] = None

	try: # Title
		product["Title"] = soup.find("h1", attrs={"class": "main-title"}).text.strip()
	except AttributeError:
		product["Title"] = None

	try: # Images
		images = []
		
		br_main_imgs = soup.find_all("img", attrs={"class": "br-main-img"})
		for br_main_img in br_main_imgs:
			images.append(br_main_img["src"])

		product["Images"] = images
	except AttributeError:
		product["Images"] = None

	try: # Price
		id = re.search(r"(\d+)\.html", url).group(1)

		search_prices = soup.find("div", attrs={"class": "br-pr-np", "data-pid": id})
		product["Price"] = search_prices.find("span").text.strip().replace(" ","")
	except AttributeError:
		product["Price"] = None

	# Color and memory better get from under describe
	# we can't find with id product connection
	try: # Describe product
		describe = {}
		
		chr_items = soup.find_all("div", attrs={"class": "br-pr-chr-item"})		
		for chr_item in chr_items:
			
			under_categories = chr_item.find("div").find_all("div")
			for under_category in under_categories:
				
				# Try 2 times get category describe data
				chrs = under_category.find_all("span")[1].find_all("a")
				if len(list(chrs)) == 0:
					chrs = under_category.find_all("span")[1]

				# Clear key
				messy_key = ", ".join([chr.text for chr in chrs]).replace("\xa0","").replace("\n","")
				keys = ", ".join(messy_key.strip() for messy_key in messy_key.split(","))

				name_describe = under_category.find_all("span")[0].text
				key_describe = keys

				describe[name_describe] = key_describe
		
		product["describe"] = describe
	except AttributeError:
		product["describe"] = None
	
	try: # Fead back
		product["count_feadback"] = soup.find("div",class_="br-pt-rt-main-mark").find("a").find("span").text
		print(product["count_feadback"])
	except AttributeError:
		product["count_feadback"] = None

	# Better get data from this items(describe why in README.md)
	if product["describe"]:
		product["describe"] = product["describe"]
		product["color"] = product["describe"]["Колір"]
		product["memory"] = product["describe"]["Вбудована пам'ять"]
		product["display_diagonal"] = product["describe"]["Діагональ екрану"]
		product["display_resolution"] = product["describe"]["Роздільна здатність екрану"]
		product["brand"] = product["describe"]["Виробник"]
	
	# Step 3
	pprint(product)

	# Step 4
	# connect to database