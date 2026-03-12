from load_django import *
from parser_app.models import Product

import requests
from bs4 import BeautifulSoup

from pprint import pprint
import re
import uuid

# necessary data (maybe better call preview all items with None)
product = {}

headers = {
	"cookie" :	"PHPSESSID=9fk9utinhihpulrc4t50krgk05; Lang=ua; CityID=23562; entryRef=docs.google.com; entryPage=%2Fukr%2FMobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html; _gcl_au=1.1.1908483809.1772551173; sc=9B71D166-0453-2A73-CF90-378A2F5DC148"
	, "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
} # HTTP/3
urls = ["https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"]


db_product, created = Product.objects.get_or_create(
     id = str(uuid.uuid4())
)


for url in urls:
     r = requests.get(url, headers=headers)
     #print(r)
     soup = BeautifulSoup(r.text, "lxml")
     
     try: # Product article = Code product
          product["prodcut_code"] = soup.find("div", attrs={"class": "product-code-num"}).find_all("span")[1].text
     except AttributeError:
          product["prodcut_code"] = None

     try: # product_name
          product["product_name"] = soup.find("h1", attrs={"class": "main-product_name"}).text.strip()
     except AttributeError:
          product["product_name"] = None

     try: # photos
          photos = []
          
          br_main_imgs = soup.find_all("img", attrs={"class": "br-main-img"})
          for br_main_img in br_main_imgs:
               photos.append(br_main_img["src"])

          product["photos"] = photos
     except AttributeError:
          product["photos"] = None

     try: # price
          id = re.search(r"(\d+)\.html", url).group(1)
          search_prices = soup.find("div", attrs={"class": "br-pr-np", "data-pid": id})
          product["price"] = search_prices.find("span").text.strip().replace(" ","")
     except AttributeError:
          product["price"] = None

     try: # Fead back
          product["count_feadback"] = soup.find("div",class_="br-pt-rt-main-mark").find("a").find("span").text
          print(product["count_feadback"])
     except AttributeError:
          product["count_feadback"] = None


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

     # Better get data from this items
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
     db_product.product_name = product["product_name"]
     db_product.color = product["color"]
     db_product.memory = product["memory"]
     db_product.brand = product["brand"]
     db_product.price = product["price"]
     db_product.dis_price = None
     db_product.photos = product["photos"]

     db_product.prodcut_code = product["prodcut_code"]
     db_product.count_feadback = product["count_feadback"]
     db_product.display_diag = product["display_diagonal"]
     db_product.display_resol = product["display_resolution"]
     db_product.dict_charact = product["describe"]
     db_product.save()
