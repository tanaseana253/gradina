import django
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradinaCraciun.settings')
django.setup()

# Import Django models
from store.models import Product

# Fetch the content of the page
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 '
                  'Safari/537.36'
}


def fetch_product_links(baseurl, start_page=1, end_page=2):
    productlinks = []

    for x in range(start_page, end_page + 1):
        response = requests.get(f'{baseurl}?page={x}', headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        productlist = soup.find_all('div', class_='card-wrapper product-card-wrapper underline-links-hover')

        for item in productlist:
            link = item.find('a', href=True)
            if link:
                product_url = urljoin(baseurl, link['href'])
                if product_url not in productlinks:
                    productlinks.append(product_url)

    return productlinks


def fetch_product_details(productlinks, category, headers=None):
    products_data = []

    for link in productlinks:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        name_tag = soup.find('h1', class_='')
        price_tag = soup.find('span', class_='price-item price-item--regular')

        if not name_tag or not price_tag:
            print(f"Skipping link due to missing name or price: {link}")
            continue

        name = name_tag.text.strip()
        price = price_tag.text.strip().removesuffix(' lei RON')

        product_info = {
            'name': name,
            'price': price,
            'category': category
        }

        products_data.append(product_info)

    return pd.DataFrame(products_data)


def main():
    baseurls = [
        ('https://gradinacraciun.ro/collections/legume', 'legume'),
        ('https://gradinacraciun.ro/collections/fructe', 'fructe'),
        ('https://gradinacraciun.ro/collections/conserve-de-legume-%C8%99i-fructe', 'conserve'),
        ('https://gradinacraciun.ro/collections/alte-bunata%C8%9Bi', 'alte_bunatati')
    ]

    all_product_links = []
    product_df = pd.DataFrame()

    for baseurl, category in baseurls:
        product_links = fetch_product_links(baseurl)
        all_product_links.extend(product_links)
        product_details_df = fetch_product_details(product_links, category, headers)
        product_df = pd.concat([product_df, product_details_df], ignore_index=True)

    # Save the data to the database
    for index, row in product_df.iterrows():
        Product.objects.create(name=row['name'], price=row['price'], category=row['category'])

    # Confirm the data is saved
    products_from_db = Product.objects.all()
    for product in products_from_db:
        print(f"Saved product: {product.name} - {product.price} - {product.category}")


if __name__ == "__main__":
    main()
