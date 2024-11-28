import django
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# de aici am inceput sa bag pt imagini
import sys

sys.stdout.reconfigure(encoding='utf-8')
# pana aici pt imagini


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradinaCraciun.settings')
django.setup()

# Import Django models
from store.models import Product
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

# Fetch the content of the page
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 '
                  'Safari/537.36'
}


def fetch_product_links(baseurl, start_page=1, end_page=2):
    productlinks = []

    for x in range(start_page, end_page + 1):
        response = requests.get(f'{baseurl}?page={x}')
        soup = BeautifulSoup(response.content, 'lxml')
        productlist = soup.find_all('div', class_='card-wrapper product-card-wrapper underline-links-hover')

        for item in productlist:

            link = item.find('a', href=True)  # Find only the first <a> tag within each product card
            if link:
                product_url = urljoin(baseurl, link['href'])
                if product_url not in productlinks:  # Check if the link is not already in the list
                    productlinks.append(product_url)
    return productlinks


def fetch_product_details(productlinks, category, headers=None):
    for link in productlinks:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        name = soup.find('h1', class_='').text.strip()
        price = soup.find('span', class_='price-item price-item--regular').text.strip().removesuffix(' lei RON')

        # Handle multiple products with the same name
        try:
            product = Product.objects.get(name=name, category=category)
        except MultipleObjectsReturned:
            products = Product.objects.filter(name=name, category=category)
            product = products.first()  # or handle duplicates in some other way
        except ObjectDoesNotExist:
            product = None

        if product:
            # Update the product in the database
            product.price = price
            product.save()

            # insert - update image with saved image

        else:
            # Create a new product if it doesn't exist
            Product.objects.create(name=name, price=price, category=category)


# Example usage
baseurls = [
    ('https://gradinacraciun.ro/collections/legume', 'legume'),
    ('https://gradinacraciun.ro/collections/fructe', 'fructe'),
    ('https://gradinacraciun.ro/collections/conserve-de-legume-%C8%99i-fructe', 'conserve'),
    ('https://gradinacraciun.ro/collections/alte-bunata%C8%9Bi', 'alte bunatati')
]

all_product_links = []
for baseurl, category in baseurls:
    product_links = fetch_product_links(baseurl)
    fetch_product_details(product_links, category, headers)

# Confirm the data is saved
products_from_db = Product.objects.all()
for product in products_from_db:
    print(product.name, product.price, product.category)


# de aici am inceput sa bag pt imagini
def imageDown(url, folder, order):
    original_directory = os.getcwd()
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except FileExistsError:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')

    for image in images:
        name = image.get('alt', 'default_name').replace('/', '_').strip()  # Sanitize the filename
        if name:
            link = image.get('src')
            if link.startswith('//'):
                link = 'https:' + link
            with open(order + '_' + name + '.jpg', 'wb') as f:
                f.write(requests.get(link).content)
            print(f"Saved: {name}.jpg")
            print('Writing:', name)
    os.chdir(original_directory)


# Create folders if they don't exist
folders = ['management/commands/photos']
for folder in folders:
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass


imageDown('https://gradinacraciun.ro/collections/legume', 'management/commands/photos', '1_')
imageDown('https://gradinacraciun.ro/collections/legume?page=2', 'management/commands/photos', '1_')
imageDown('https://gradinacraciun.ro/collections/fructe', 'management/commands/photos', '2_')
imageDown('https://gradinacraciun.ro/collections/conserve-de-legume-%C8%99i-fructe', 'management/commands/photos', '3_')
imageDown('https://gradinacraciun.ro/collections/conserve-de-legume-%C8%99i-fructe?page=2',
          'management/commands/photos', '3_')
imageDown('https://gradinacraciun.ro/collections/alte-bunata%C8%9Bi', 'management/commands/photos', '4_')
# de pana aici pt imagini
