# import os
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from urllib3.contrib.emscripten import fetch
#
#
# def fetch_products(baseurl, headers=None):
#     legumelist = []
#     image_directory = 'product_images'
#
#     # Create an images directory if it doesn't exist
#     if not os.path.exists(image_directory):
#         os.makedirs(image_directory)
#
#     response = requests.get(baseurl, headers=headers)
#     if response.status_code != 200:
#         print(f"Failed to retrieve the base URL: {baseurl}")
#         return pd.DataFrame()  # Return empty DataFrame if request fails
#
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     # Debug: print the fetched HTML content
#     print(f"Fetched HTML content from {baseurl}")
#
#     # Update this selector to match the actual structure
#     product_links = [a['href'] for a in soup.find_all('a', class_='product-grid-item__title')]
#
#     # Debug: print the found product links
#     print(f"Found {len(product_links)} product links")
#
#     for link in product_links:
#         full_link = requests.compat.urljoin(baseurl, link)
#         print(f"Processing product link: {full_link}")  # Debug statement
#
#         response = requests.get(full_link, headers=headers)
#         if response.status_code != 200:
#             print(f"Failed to retrieve product page: {full_link}")
#             continue
#
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         try:
#             name = soup.find('h1', class_='product-single__title').text.strip()
#             price = soup.find('span', class_='price-item price-item--regular').text.strip()
#         except AttributeError as e:
#             print(f"Error parsing product details: {e}")
#             continue
#
#         # Extract image URL
#         image_tag = soup.find('img', class_='product-single__photo')
#         if image_tag:
#             image_url = image_tag['src']
#             if image_url.startswith('//'):
#                 image_url = 'https:' + image_url
#
#             # Download the image
#             image_response = requests.get(image_url)
#             if image_response.status_code == 200:
#                 image_name = f"{name.replace(' ', '_')}.jpg"
#                 image_path = os.path.join(image_directory, image_name)
#
#                 with open(image_path, 'wb') as img_file:
#                     img_file.write(image_response.content)
#
#                 print(f"Saved image: {image_path}")
#             else:
#                 image_path = None
#                 print(f"Failed to download image: {image_url}")
#         else:
#             image_path = None
#             print(f"No image found for product: {name}")
#
#         legume = {
#             'name': name,
#             'price': price,
#             'image_path': image_path
#         }
#
#         print(f"Product details: {legume}")  # Debug statement
#         legumelist.append(legume)
#         print('Saving:', legume['name'])
#
#     # Convert list of dictionaries to a DataFrame
#     df = pd.DataFrame(legumelist)
#     return df
#
#
# # Example usage
# baseurl = 'https://gradinacraciun.ro/collections/legume'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }
#
# product_df = fetch
#
