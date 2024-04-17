from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome('./chromedriver', chrome_options=options)

BRAND_LINKS = [
    'https://www.mobiledokan.com/samsung/',
    'https://www.mobiledokan.com/samsung-page2/',
    'https://www.mobiledokan.com/samsung-page3/',

    'https://www.mobiledokan.com/xiaomi/',
    'https://www.mobiledokan.com/xiaomi-page2/',
    'https://www.mobiledokan.com/xiaomi-page3/',

    'https://www.mobiledokan.com/realme/',
    'https://www.mobiledokan.com/realme-page2/',

    'https://www.mobiledokan.com/vivo/',
    'https://www.mobiledokan.com/vivo-page2/',

    'https://www.mobiledokan.com/oppo/',
    'https://www.mobiledokan.com/oppo-page2/',

    'https://www.mobiledokan.com/apple/',
    'https://www.mobiledokan.com/apple-page2/',

    'https://www.mobiledokan.com/symphony/',
    'https://www.mobiledokan.com/symphony-page2/',

    'https://www.mobiledokan.com/tecno/',
    'https://www.mobiledokan.com/tecno-page2/',

    'https://www.mobiledokan.com/walton/',
    'https://www.mobiledokan.com/walton-page2/',

    'https://www.mobiledokan.com/itel/',

    'https://www.mobiledokan.com/infinix/',

    'https://www.mobiledokan.com/oneplus/',

    'https://www.mobiledokan.com/motorola/',

    'https://www.mobiledokan.com/nokia/',
    'https://www.mobiledokan.com/nokia-page2/',

]

CSV_COLUMNS_HEADERS = []


def scroll_down_the_page(driver, duration=5):
    """
    Sometimes the URLs don't properly load unless they are visited. So we try
    to visit them and make the browser load them.
    """
    for _ in range(duration):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


def get_product_details(driver, product_link):
    """This method fetches detailed information of the product and store those into a list of dictionaries and returns that

    Args:
        driver (obj): Passing the chromedriver that was initalized
        product_link (str): The link of the product details page
    """

    driver.get(product_link)
    scroll_down_the_page(driver)
    data = {}
    name = driver.find_element_by_css_selector('.entry-header').text
    data['Name'] = name
    data['Brand'] = product_link.split('/')[3]
    data['Link'] = product_link
    try:
        spec_tables = driver.find_elements_by_css_selector(
            '.table-is-responsive')
        print('Table paisi')
        price_tds = spec_tables[0].find_elements_by_tag_name('td')
        data[price_tds[0].text] = price_tds[1].text
        rows = spec_tables[1].find_elements_by_tag_name('tr')

        print(len(rows))
        for row in rows:
            try:
                tds = row.find_elements_by_tag_name('td')
                data[tds[0].text] = tds[1].text
            except:
                print('Could not find the data')
                continue

    except:
        print('No product details found for {}'.format(product_link))

    print(data)
    return data


def get_product_links_from_brand(driver, brand_link):
    """This method fetches the product links from the brand page and returns them

    Args:
        driver (obj): Passing the chromedriver that was initalized
        brand_link (str): The link of the brand page
    """

    driver.get(brand_link)
    scroll_down_the_page(driver)
    links = []
    try:
        spec_tables = driver.find_elements_by_css_selector(
            '.table-is-responsive')
        print('Table paisi')
        rows = spec_tables[0].find_elements_by_tag_name('td')
        print(len(rows))
        for row in rows:
            try:
                link = row.find_element_by_tag_name('a').get_attribute('href')
                print(link)
                links.append(link)
            except:
                print('Could not find link')
                continue

    except:
        print('No product details found for {}'.format(link))

    return links


# Fetching all product links from brand pages
all_products_links = []

print('##########Starting Scrape##########\n\n\n')

for brand in BRAND_LINKS:
    print('##########Fetching product links from {}##########\n\n\n'.format(brand))
    links = get_product_links_from_brand(driver, brand)
    print('##########Fetched {} product links from {}##########\n\n\n'.format(
        len(links), brand))
    all_products_links.extend(links)

print('##########Total {} products found##########\n\n\n'.format(
    len(all_products_links)))


# Fetching all product details from product links

raw_data = []
count = 0
for link in all_products_links:
    count += 1
    print('Fetching {}/{} product details'.format(count, len(all_products_links)))
    data = get_product_details(driver, link)
    raw_data.append(data)

# Writing raw data to json file

with open('raw_data.json', 'w') as fout:
    json.dump(raw_data, fout)


driver.close()