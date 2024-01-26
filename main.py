import requests
from bs4 import BeautifulSoup

def get_product_urls(page_num):
    url = f'https://www.amazon.in/s?i=computers&rh=n%3A1375424031&fs=true&page={page_num}&qid=1706254060&ref=sr_pg_{page_num}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT":"1",
        "Connection":"close",
        "Upgrade-Insecure-Requests":"1"
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, 'lxml')
        product_links = soup.find_all(
            'a',
            class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
        )
        product_links = product_links[3:]
        product_urls = []
        for product_link in product_links:
            product_urls.append(product_link['href'])
        return product_urls
    else:
        print(f'Failed to get data from {url}')
        return []
    
def get_details(url):
    url = f'https://www.amazon.in{url}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT":"1",
        "Connection":"close",
        "Upgrade-Insecure-Requests":"1"
        }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html,'lxml')

        model = soup.find(
            'span',
            id='productTitle'
        ).text.strip()
        print(model)
        company = model.split()[0]
        print(company)

        price = soup.find('span', class_="a-price-whole").text
        print(price)
        offer = soup.find(
            'span',
            class_="a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage"
        ).text
        print(offer)

        availability = soup.find(
            'span',
            class_="a-size-medium a-color-success"
        ).text
        availability =  availability == ' In stock '
        print(f'In Stock : {availability}')

        rating = soup.find(
            'span',
            class_="a-size-base a-color-base",
            id=None
        ).text.strip()
        print(rating)

        reviews = soup.find(
            'span',
            id="acrCustomerReviewText"
        ).text.split()[0]
        print(reviews)


pages = 1
for page in range(pages):
    product_urls = get_product_urls(page)
    for url in product_urls:
        get_details(url)
        break