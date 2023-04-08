import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('bever_products.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'price', 'url', 'review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # loop through all pages
    for page in range(0,5):
        url = f'https://www.bever.nl/c/uitrusting/rugzakken/wandelrugzakken.html?p=2&size=48&page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_tags = soup.find_all('div', {'class': 'as-m-product-tile'})

        # loop through all products
        for tag in product_tags:
            name = tag.find('div', {'class': 'as-m-product-tile__title-wrapper'}).text.strip()
            price = tag.find('div', {'class': 'as-a-price__value as-a-price__value--sell'}).text.strip()
            url = tag.find('a', {'class': 'as-m-product-tile__link'})['href']
            visit_url = f'https://www.bever.nl{url}'
            
            response = requests.get(visit_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            review_tags = soup.find_all('div', {'class': 'an_hy'})

            # loop through all reviews
            for tag in review_tags:
                review = tag.find('div', {'class': 'as_lt'}).text.strip()

                # write to csv
                writer.writerow({'name': name, 'price': price, 'url': url, 'review': review})
