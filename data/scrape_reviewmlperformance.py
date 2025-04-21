import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

def scrape_review(session, productId, productType, productName, productSKU, take):
    url = "https://stamped.io/api/widget?"

    params = {
        "productId": productId,
        "productType": productType,
        "productName": productName,
        "productSKU": productSKU,
        "take":take,
        "sort":"recent",
        "apiKey": "pubkey-9E8H1Yw3Zom2V9RPGr9Blv1CReN2D2",
        "sId": 52805
    }

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mlperformance.co.uk',
        'Referer': 'https://www.mlperformance.co.uk/'
    }

    response = session.get(url, headers=headers, params=params)

    reviewList = []
    # Check the response
    if response.status_code == 200:
        try:
            data = response.json()
            hhtml = BeautifulSoup(data['widget'], 'html.parser')
            reviews = hhtml.findAll('p',{'class':'stamped-review-content-body'})
            for review in reviews:
                reviewList.append(review.text)
        except:
            pass
    else:
        print(f"Failed to fetch {productId}: {response.status_code} - {response.text}")
    return str(reviewList)


def scrape_rating_review_count(session, productId, productType, productTitle):
    url = "https://stamped.io/api/widget/badges"
    
    payload = {
        "productIds": [
            {
                "productId": productId,
                "productType": productType,
                "productTitle": productTitle
            }
        ],
        "apiKey": "pubkey-9E8H1Yw3Zom2V9RPGr9Blv1CReN2D2",
        "sId": 52805
    }

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json',
        'Origin': 'https://www.mlperformance.co.uk',
        'Referer': 'https://www.mlperformance.co.uk/'
    }

    response = session.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()[0]
        rating = data['rating']
        review_count = data['count']
        q_count = data['countQuestions']
    else:
        print(f"Failed to fetch {productId}: {response.status_code} - {response.text}")
        rating, review_count, q_count = None, None, None
    return rating, review_count, q_count

def main(category):
    df = pd.read_csv(f'C:/Users/farea/Documents/PythonWorkspace/webscrape/{category}.csv')
    # df['rating'], df['review_count'], df['questions'], df['review'] = None, None, None, None
    prod_count = df.shape[0]
    print('----------------------------')
    print(f'Updating Category - {category}')  
    s = requests.Session()
    for row in range(prod_count):
        productId = str(df['id'][row])
        productTitle = df['title'][row]
        productType = df['prod_type'][row]
        productSKU = df['sku'][row]
        take = 30
        # rating, review_count, q_count = scrape_rating_review_count(s,productId, productType, productTitle)
        review = scrape_review(s,productId, productType, productTitle, productSKU, take)
        print(f'scraping product {row+1}/{prod_count}') 
        # df.loc[row,'rating'], df.loc[row,'review_count'], df.loc[row,'questions'] = rating, review_count, q_count
        df.loc[row,'review'] = review
    df.to_csv(f'C:/Users/farea/Documents/PythonWorkspace/webscrape/COMPLETE_{category}.csv')
    print('Update complete!')

if __name__ == "__main__":
    #'engine-oil-recommender', 'car-batteries', 
    category = ['tyre-recommender',
                'wiper-blades', 'tuning-remap']
    
    # , 'car-performance-intake-ramair-eventuri-mst-afe',
    #             'car-brakes-brake-parts', 'suspension-parts-ml-performance', 'exhaust-parts-ml-performance',
    #             'chargepipe-valves-ml-performance', 'intercoolers-chargecoolers-radiators-ml-performance', 
    #             'filter-recommender', 'sensor-recommender', 'spark-plug-recommender', 'car-care-accessories'
    
    for cat in category:
        main(cat)