import sys
import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
from io import BytesIO
from pprint import pprint

url = sys.argv[1]
# 1. Get the html page
html = requests.get(url).content

# 2. Parse the html page
soup = BeautifulSoup(html, 'lxml')

# 3. Extract relevant information
id = soup.select_one('.numero > .description_span').text
number_views = soup.find('label', text='Nombre de vues : ').find_next_sibling().text
created_at = soup.find('label', text='Déposée le : ').find_next_sibling().text
name = soup.select_one('#Title').text
description = soup.select_one('#GetDescription').text
price = soup.find(attrs={'itemprop': 'price'}).text

# 4. Decode the phone number image
phone_img = soup.select_one('.Phone > img')
response = requests.get(phone_img['src'])
img = Image.open(BytesIO(response.content))
number = pytesseract.image_to_string(img)

# 5. Print the results
print({
    'id': id,
    'number_views': number_views,
    'name': name,
    'price': price,
    'number': number
})
