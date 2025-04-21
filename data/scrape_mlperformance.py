from requests_html import HTMLSession
from curl_cffi import requests as cureq
import json
import pandas as pd

def scrape_product(category, max_page):
    prod = []
    print('----------------------------')
    print(f'Category - {category}')
    for page in range(1,(max_page+1)):
        print(f'scraping page {page}/{max_page}')
        baseurl = f'https://www.mlperformance.co.uk/collections/{category}/products.json?limit=250&page={page}'

        resp = cureq.get(baseurl, impersonate='chrome')
        data = resp.json()
        for item in data['products']:
            id = item['id']
            title = item['title']
            vendor = item['vendor']
            prod_type = item['product_type']
            publish = item['published_at']
            for variant in item['variants']:
                price = variant['price']
                gram = variant['grams']
                compare_at_price = variant['compare_at_price']
                availability = variant['available']
                sku = variant['sku']
                prod.append({
                    'id':id,
                    'title':title,
                    'vendor':vendor,
                    'prod_type':prod_type,
                    'publish':publish,
                    'price (MYR)':price,
                    'compare_at_price (MYR)':compare_at_price,
                    'weight (grams)':gram,
                    'available':availability,
                    'sku':sku
                })

    df = pd.DataFrame(prod)
    df.to_csv(f'C:/Users/farea/Documents/PythonWorkspace/webscrape/{category}.csv')
    print(f'saved to file - {category}.csv')

if __name__ == "__main__":
    category = ['engine-oil-recommender', 'car-batteries', 'tyre-recommender',
                'wiper-blades', 'tuning-remap', 'car-performance-intake-ramair-eventuri-mst-afe',
                'car-brakes-brake-parts', 'suspension-parts-ml-performance', 'exhaust-parts-ml-performance',
                'chargepipe-valves-ml-performance', 'intercoolers-chargecoolers-radiators-ml-performance', 
                'filter-recommender', 'sensor-recommender', 'spark-plug-recommender', 'car-care-accessories']
    max_page = [27,16,184,42,2,14,1102,677,158,3,24,200,56,21,22]
    for i in range(len(category)):
        scrape_product(category[i], max_page[i])