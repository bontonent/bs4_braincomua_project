# One page parsing site brain.com.ua with bs4

It is project made for view how I use instrument bs4


On this project have avaliable get all necessary data from <script> with json data

![](./pictures_md/describe_info)

![](./pictures_md/pictures_info)

### Info

url-site : https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html 

install during project

```
asgiref==3.11.1
beautifulsoup4==4.14.3
bs4==0.0.2
certifi==2026.2.25
charset-normalizer==3.4.4
Django==6.0.3
dotenv==0.9.9
idna==3.11
lxml==6.0.2
psycopg2==2.9.11
python-dotenv==1.2.2
requests==2.32.5
soupsieve==2.8.3
sqlparse==0.5.5
typing_extensions==4.15.0
urllib3==2.6.3
```

result: [result_csv](./results.result.csv)

---

## How run project

### Base setting

#### Create environment
```
python -m venv .venv
source ./.../activate
pip install -r requirements.txt
```

#### Create .env
```
name_db=brain_com_ua
user_name=postgres
password=koldronok
port=5432
host=127.0.0.1
```

### Setting django


#### Refine or create tables
```python
python manage.py makemigrations
python manage.py migrate
```


### Run project

```
python ./modules/1_get_info.py
```

---

# Describe project

# Code Description (BeautifulSoup Parser)

This project demonstrates how to parse a **product page from brain.com.ua** using:

- `requests`
- `BeautifulSoup`
- `Django ORM`
- `PostgreSQL`

The parser collects product information from a single page and stores the structured data in a database.

---

# Workflow

The script performs the following steps:

1. Send an HTTP request to the product page
2. Parse HTML using BeautifulSoup
3. Extract product information
4. Clean and normalize the data
5. Save the result to PostgreSQL using Django ORM

---

# Imports

The project uses several Python libraries:

```python
import requests
from bs4 import BeautifulSoup
import re
import uuid
from pprint import pprint
```

Additionally, Django is loaded to allow database interaction:

```python
from load_django import *
from parser_app.models import Product
```

`load_django` initializes the Django environment so the script can access the Django models outside the web server.

---

# HTTP Request

The parser sends a request to the product page using `requests`.

```python
r = requests.get(url, headers=headers)
```

Custom headers are used to simulate a real browser and avoid blocking:

```python
headers = {
 "User-Agent": "Mozilla/5.0 ...",
 "cookie": "session data..."
}
```

---

# HTML Parsing

After receiving the page, it is parsed using **BeautifulSoup**:

```python
soup = BeautifulSoup(r.text, "lxml")
```

The `lxml` parser is used because it is:

- faster than the default parser
- more tolerant to broken HTML

---

# Product Data Container

All parsed data is stored in a dictionary:

```python
product = {}
```

This dictionary collects all extracted product attributes before saving them to the database.

Example structure:

```python
{
 "product_name": "...",
 "price": "...",
 "color": "...",
 "memory": "...",
 "photos": [...],
 "describe": {...}
}
```

---

# Extracting Product Code

The product code (article) is extracted from the product page:

```python
product["prodcut_code"] = soup.find(
    "div", {"class": "product-code-num"}
).find_all("span")[1].text
```

If the element is missing, the script safely handles the error:

```python
except AttributeError:
    product["prodcut_code"] = None
```

---

# Extracting Product Name

The product title is located in the `<h1>` tag:

```python
product["product_name"] = soup.find(
    "h1",
    {"class": "main-product_name"}
).text.strip()
```

`.strip()` removes unnecessary whitespace.

---

# Extracting Product Images

All product images are collected into a list.

```python
photos = []

br_main_imgs = soup.find_all("img", {"class": "br-main-img"})

for br_main_img in br_main_imgs:
    photos.append(br_main_img["src"])
```

Result example:

```python
[
 "image1.jpg",
 "image2.jpg",
 "image3.jpg"
]
```

---

# Extracting Product Price

The product ID is extracted from the URL using regex:

```python
id = re.search(r"(\d+)\.html", url).group(1)
```

Then the price is located using the `data-pid` attribute.

```python
search_prices = soup.find(
    "div",
    {"class": "br-pr-np", "data-pid": id}
)
```

Finally, the price is cleaned:

```python
product["price"] = search_prices.find("span").text.strip().replace(" ", "")
```

Example:

```
45 999 → 45999
```

---

# Extracting Feedback Count

The number of reviews is extracted from the rating block:

```python
product["count_feadback"] = soup.find(
    "div",
    class_="br-pt-rt-main-mark"
).find("a").find("span").text
```

---

# Extracting Product Characteristics

Most product information is located in the **characteristics table**.

Example fields:

- Color
- Memory
- Display size
- Display resolution
- Manufacturer

Each characteristic is stored in a dictionary.

```python
describe = {}
```

The parser iterates through all characteristic blocks:

```python
chr_items = soup.find_all("div", {"class": "br-pr-chr-item"})
```

Each block contains several rows with keys and values.

Example HTML structure:

```
Name: Color
Value: Black Titanium
```

The parser extracts both parts:

```python
name_describe = under_category.find_all("span")[0].text
key_describe = keys
```

And stores them:

```python
describe[name_describe] = key_describe
```

Example result:

```python
{
 "Колір": "Black Titanium",
 "Вбудована пам'ять": "256 GB",
 "Діагональ екрану": "6.7",
 "Роздільна здатність екрану": "2868x1320",
 "Виробник": "Apple"
}
```

---

# Extracting Important Fields

Several important attributes are derived from the characteristics dictionary.

```python
product["color"] = product["describe"]["Колір"]
product["memory"] = product["describe"]["Вбудована пам'ять"]
product["display_diagonal"] = product["describe"]["Діагональ екрану"]
product["display_resolution"] = product["describe"]["Роздільна здатність екрану"]
product["brand"] = product["describe"]["Виробник"]
```

---

# Debug Output

Before saving the data, the script prints the parsed result:

```python
pprint(product)
```

This helps verify that the parser extracted the correct values.

---

# Saving Data to Database

The script stores parsed data in PostgreSQL using **Django ORM**.

First, a product record is created:

```python
db_product, created = Product.objects.get_or_create(
    id=str(uuid.uuid4())
)
```

Then fields are assigned:

```python
db_product.product_name = product["product_name"]
db_product.color = product["color"]
db_product.memory = product["memory"]
db_product.brand = product["brand"]
db_product.price = product["price"]
```

Additional data:

```python
db_product.photos = product["photos"]
db_product.prodcut_code = product["prodcut_code"]
db_product.count_feadback = product["count_feadback"]
```

Finally the object is saved:

```python
db_product.save()
```

---

# Example Parsed Data

Example result of the parser:

```python
{
 "product_name": "Apple iPhone 16 Pro Max 256GB Black Titanium",
 "brand": "Apple",
 "color": "Black Titanium",
 "memory": "256GB",
 "price": "45999",
 "display_diagonal": "6.7",
 "display_resolution": "2868x1320",
 "photos": [...],
 "describe": {...}
}
```

---

# Possible Improvements

The parser could be improved by:

- remove static cookies
- remove static user-agent
- add proxy
- add mutlitreading
- make better parser row
