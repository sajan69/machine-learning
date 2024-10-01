from datetime import datetime
import requests
import csv
import bs4
import concurrent.futures
from tqdm import tqdm



USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0"
REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.5"
}

NO_OF_THREADS = 10
def get_page_html(url):
    response = requests.get(url, headers=REQUEST_HEADERS)
    return response.text

def get_product_price(soup):
    main_price_span = soup.find("span", attrs={"class": "a-price a-text-price a-size-medium apexPriceToPay", "data-a-color": "price"})
    if main_price_span is None:
        return None
    price_spans=main_price_span.findAll("span")
    for span in price_spans:
        price = span.text.strip().replace("$", "").replace(",", "")
        if price.replace(".", "").isdigit():
            return float(price)
        else:
            print(f"Invalid price: {price}")
    return None

def get_product_rating(soup):
    rating_span = soup.find("span", attrs={"class": "a-icon-alt"})
    if rating_span is None:
        return None
    rating = rating_span.text.split(" ")[0]
    return float(rating)

def get_product_reviews(soup):
    reviews_span = soup.find("span", attrs={"id": "acrCustomerReviewText"})
    if reviews_span is None:
        return None
    reviews = reviews_span.text.split(" ")[0].replace(",", "")
    return int(reviews)

def get_product_feature(soup):
    description = soup.find("div", attrs={"id": "feature-bullets"})
    if description is None:
        return None
    return description.text.strip()

def get_product_information(soup):
    information = soup.find("div", attrs={"class": "a-row a-expander-container a-expander-extend-container"})
    if information is None:
        return None
    #make it more readable
    information = information.text.strip().replace("\n", " ")
    #remove everything other than readable text
    information = " ".join(information.split())
    return information



    

def extract_product_info(url,output):
    product_info = {}

    
    html = get_page_html(url)
    soup = bs4.BeautifulSoup(html, "lxml")
    product_info["title"] = soup.find("span", id="productTitle").text.strip()
    product_info["price"] = get_product_price(soup)
    product_info["rating"] = get_product_rating(soup)
    product_info["reviews"] = get_product_reviews(soup)
    product_info["description"] = get_product_feature(soup)
    product_info["information"] = get_product_information(soup)
    
    
    output.append(product_info)


if __name__ == "__main__":
    products_data = []
    urls = []

    with open("amazon_products_urls.csv", newline="") as csv_file:
        urls = list(csv.reader(csv_file, delimiter=","))
    with concurrent.futures.ThreadPoolExecutor(max_workers=NO_OF_THREADS) as executor:
        #AttributeError: 'tqdm' object has no attribute 'last_print_t'
        for url in tqdm(urls, desc="Extracting product info", unit="product"):
            executor.submit(extract_product_info, url[0], products_data)
    output_file_name = f"amazon_products_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    with open(output_file_name, mode="w", newline="", encoding="utf-8") as output_file_name:

        writer =csv.writer(output_file_name)
        #ndexError: list index out of range
        writer.writerow(products_data[0].keys())
        for product in products_data:
            #UnicodeEncodeError: 'charmap' codec can't encode character '\x9b' in position 3366: character maps to <undefined>
            writer.writerow(product.values())
    print(f"Output file: {output_file_name}")