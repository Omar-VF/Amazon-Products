import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_product_urls(page_num):
    url = f"https://www.amazon.in/s?i=computers&rh=n%3A1375424031&fs=true&page={page_num}&qid=1706254060&ref=sr_pg_{page_num}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        product_links = soup.find_all(
            "a",
            class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal",
        )
        product_links = product_links[3:]
        product_urls = []
        for product_link in product_links:
            product_urls.append(product_link["href"])
        return product_urls
    else:
        print(f"Status Code : {response.status_code} \nFailed to get data from {url}")
        return []


def get_details(url):
    url = f"https://www.amazon.in{url}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "lxml")

        try:
            model = soup.find("span", id="productTitle").text.strip()
        except:
            model = '-'

        try:
            if model.split()[0][0] == '(':
                company = model.split()[1]
            else:
                company = model.split()[0]
        except:
            company = '-'

        try:
            cost = soup.find("span", class_="a-price-whole").text
        except:
            cost = '-'

        try:
            offer = soup.find(
                "span",
                class_="a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage"
            ).text
        except:
            offer = '-'

        try:
            availabilitytxt = soup.find("div", id="availability").find('span').text
            availability = availabilitytxt == " In stock "
            
            if availability == False:
                if availabilitytxt.strip().split()[0] == 'Only':
                    availability = True
                else:
                    pass
            else:
                pass    

        except:
            availability = '-'

        try:
            rating = soup.find(
                "span", {'data-hook':"rating-out-of-text"}
            ).text.strip().split()[0]
        except:
            rating = '-'

        try:
            reviews = soup.find("span", id="acrCustomerReviewText").text.split()[0]
        except:
            reviews = '-'

        data_dict = {
            "Company": company,
            "Model": model,
            "Cost": cost,
            "Offer": offer,
            "In Stock": availability,
            "Rating": rating,
            "Reviews": reviews,
        }

        master_list.append(data_dict)

    else:
        print(f"Status Code : {response.status_code} \nFailed to get data from {url}")


def create_excel():
    dataframe = pd.DataFrame(master_list)
    dataframe.index += 1

    try:
        dataframe.to_csv("Amazon product data.csv")
        print("Csv Saved!")
    except Exception as e:
        print(f"Failed to save csv : {e}")

    timer = round(time.time() - start_time, 2)
    timer = time.strftime("%M:%S", time.gmtime(timer))
    print(f"The process has been completed.\nTime Taken :{timer}")


start_time = time.time()

master_list = []
pages = 2

print("Colecting Data...Please wait...")
for page in range(1,pages+1):
    product_urls = get_product_urls(page)
    for url in product_urls:
        get_details(url)
        time.sleep(1.5)

create_excel()
