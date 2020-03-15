# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from products.models import Product, Price
from .url_settings import TOP_URL
import pdb; 

import json
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

delay = 20  # seconds

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Scrapes and stores product information
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("window-size=1024,768")
        # chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN', 'not-a-secret')
        # chrome_options.binary_location = '/usr/bin'
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(TOP_URL + "/OrderProductSelection.aspx")
        
        try:
            # wait for data to be loaded
            WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.brand-link'))
            )
        except TimeoutException:
            print('Loading took too much time!')
            sys.stdout.flush()
        else:
            html = browser.page_source
        finally:
            browser.quit()
        
        if html:
            soup_beers = BeautifulSoup(html, "html.parser")

            # raw_data = soup.select_one(selector).text
            # data = json.loads(raw_data)
        
            # import pprint
            # pprint.pprint(data)
        
            # get beer page html and make soup object
            # html = requests.get(
            #     TOP_URL + "/OrderProductSelection.aspx", 
            #     verify=False, 
            #     headers={
            #         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            #         "referer": "https://www.thebeerstore.ca/beers/",
            #         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            #         "accept-encoding": "gzip, deflate, br",
            #         "accept-language": "en-US,en;q=0.9",
            #         "upgrade-insecure-requests": "1"
            #     }).content
            # soup_beers = BeautifulSoup(html, "html.parser")
            # find all beers
            beers = soup_beers.find_all("a", "brand-link")

            for beer in beers:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument("window-size=1024,768")
                # chrome_options.binary_location = '/usr/bin'
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                browser = webdriver.Chrome(chrome_options=chrome_options)
                
                beer_url = beer["href"]

                try:
                    beer_html = browser.get(beer_url)
                except:
                    print("Trynna get:", beer_url)
                    print("Unexpected error:", sys.exc_info()[0])
                    browser.quit()
                    sys.stdout.flush()
                    continue

                try:
                    # wait for data to be loaded
                    WebDriverWait(browser, delay).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.product'))
                    )
                except TimeoutException:
                    print('Loading took too much time!')
                    sys.stdout.flush()
                else:
                    beer_html = browser.page_source
                finally:
                    browser.quit()
                
                if beer_html:
                    # get beer page and make soup object
                    soup_beer = BeautifulSoup(beer_html, "html.parser")
                    # get sizes
                    beer_product_tables = soup_beer.find_all("table", "product")
                    
                    beer_id = beer_url.split("/")[-1]
                    
                    # get name and image
                    beer_name = soup_beer.find("h2", "brand-title").get_text()
                    beer_image = TOP_URL + "/" + soup_beer.find("div","brand-img").img["src"]
        
                    # get country and type
                    beer_country =  soup_beer.find("h4","brand-brewed").get_text().split()[-1]
                    beer_type = soup_beer.find("h4","brand-brewed").get_text().split()[2]
                    attrs = soup_beer.find_all("span", "brand-description")
                    beer_category = ""
                    beer_abv = ""
                    beer_brewer = "" 
                        
                    for attr in attrs:
                        if attr.find('span').get_text().strip() == "Category :":
                            beer_category = attr.get_text().split('Category :')[-1].strip()
                        elif attr.find('span').get_text().strip() == "Brewer:":
                            beer_brewer = attr.get_text().split('Brewer:')[-1].strip()
                        elif attr.find('span').get_text().strip() == "Alcohol Content (ABV):":
                            beer_abv = attr.get_text().split('Alcohol Content (ABV):')[-1].split("%")[0].strip()
                    
                    # loop through beer products
                    for beer_product_table in beer_product_tables:
                        beer_products = beer_product_table.find_all("tr")[1:]
                        for beer_product in beer_products:

                            # print beer_id
                            beer_product_id = beer_product.get('id')
                        
                            # Comment to disable monitoring
                            beer_product_size = beer_product.find("td", "item").get_text()
                            beer_product_price =  ""
                            beer_on_sale = False
                            if beer_product.find_all("td", "rate")[1].get_text().strip() == '':
                                beer_product_price =  beer_product.find("td", "rate").get_text()
                            else:
                                beer_on_sale = True
                                beer_product_price = beer_product.find_all("td", "rate")[1].find('b').get_text()
                        
                            # check if product exists
                            # NOTE: used this custom solution because django get_or_create
                            # doesn't play nice with custom primary keys
                            try:
                                product_entry = Product.objects.get(product_id=int(beer_product_id.strip()))
                            except: 
                                product_entry = Product()
    
                            # set fields
                            product_entry.name = beer_name.strip()
                            product_entry.size = beer_product_size.strip()
                            product_entry.beer_id = int(beer_id.strip())
                            product_entry.product_id = int(beer_product_id.strip())
                            product_entry.image_url = beer_image.strip()
                            product_entry.country = beer_country.strip()
                            product_entry.type = ""
                            product_entry.category = beer_category
                            product_entry.abv = float(beer_abv)
                            product_entry.brewer= beer_brewer
                            product_entry.on_sale = beer_on_sale

                            price = float(beer_product_price.strip()[1:])

                            size = product_entry.size.replace('NEW', '').split()
                            units = int(size[0])
                            mls = int(size[-2])
                            product_entry.price_per_100ml = round((price / (units * mls / 100)), 2) if (units * mls / 100) > 0 else 0
                            product_entry.price_per_abv = round((price / (float(product_entry.abv) * units * mls / 100)), 2) if (float(product_entry.abv) * units * mls / 100) else 0
                            product_entry.current_price = price
                            product_entry.save()
                            
                            price_entry = Price()
                            price_entry.price = price
                            price_entry.product = product_entry
                            price_entry.save()
