import scrapy
import pandas as pd
import urllib.parse as urlparse
from urllib.parse import parse_qs

class ImmoSpider(scrapy.Spider):
    name = 'immo_spider'
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 3, # to avoid '429 Too Many Requests'
        'RETRY_TIMES': 10,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0
    }

    def __init__(self, flat_house=None, rent_buy=None, place_lvl=None, place=None, *args, **kwargs):
        super(ImmoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.immoscout24.ch/de/{flat_house}/{rent_buy}/{place_lvl}-{place}']
        self.data = []  # List to store data for DataFrame

    def parse(self, response):
        # Navigate through each listing on the page to gather links to detail pages
        links = response.css('a.HgCardElevated_content_uir_2.HgCardElevated_link_EHfr7::attr(href)').getall()
        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_details)

        # Follow the pagination link to the next page of listings
        next_page = response.css('a.HgPaginationSelector_nextPreviousArrow__Mlz2[aria-label="Zur nächsten Seite"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        # Extract detailed information from each listing's detail page
        price = response.xpath("//div[@data-test='costs']//dd/strong/span/text()").extract_first(default='').replace('CHF', '').replace('’', '')
        street = response.css("address.AddressDetails_address_i3koO .AddressDetails_street_nXScL::text").get()
        plz_city = response.css("address.AddressDetails_address_i3koO span:not(.AddressDetails_street_nXScL)::text").get()
        features_list = response.css('ul.FeaturesFurnishings_list_S54KV li p::text').getall()

                
        # Extracting core attributes from the details page
        core_attributes = response.css("div.CoreAttributes_coreAttributes_e2NAm dl dt")
        details = {
            'type_search': flat_house,
            'place_search': place, 
            'street': street,
            'PLZ': plz_city,
            'price': price,
            'features': ', '.join(features_list),
            'availability': '',
            'object_type': '',
            'number_of_rooms': '',
            'number_of_floors': '',
            'living_area': '',
            'land_area': '',
            'volume': '',
            'construction_year': '',
            'last_rennovation': '',
            'number_of_appartments': '',
            'height_rooms':''
        }
        

        for dt in core_attributes:
            label = dt.xpath("normalize-space(text())").get()
            value = dt.xpath("following-sibling::dd[1]/text()").get() or dt.xpath("following-sibling::dd[1]/span/text()").get()
            if label == 'Verfügbarkeit:':
                details['availability'] = value.strip()
            elif label == 'Objekttyp:':
                details['object_type'] = value.strip()
            elif label == 'Anzahl Zimmer:':
                details['number_of_rooms'] = value.strip()
            elif label == 'Anzahl Etagen:':
                details['number_of_floors'] = value.strip()
            elif label == 'Anzahl Wohnungen:':
                details['number_of_appartments'] = value.strip()
            elif label == 'Wohnfläche:':
                details['living_area'] = value.strip()
            elif label == 'Grundstückfläche:':
                details['land_area'] = value.strip()
            elif label == 'Kubatur:':
                details['volume'] = value.strip()
            elif label == 'Baujahr:':
                details['construction_year'] = value.strip()
            elif label == 'Letztes Renovationsjahr:':
                details['last_rennovation'] = value.strip()
            elif label == 'Raumhöhe:':
                details['height_rooms'] = value.strip()
                
        # Append the extracted data to the list
        self.data.append(details)

        # Follow pagination if necessary
        next_page = response.css('a.HgPaginationSelector_nextPreviousArrow__Mlz2[aria-label="Zur nächsten Seite"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_details)


    def closed(self, reason):
        # When spider is closed, convert collected data to a DataFrame and print/save it
        df = pd.DataFrame(self.data)
        print(df)
        df.to_csv('immobilien_appenzell-ar.csv', index=False)  # Optionally save to CSV

        
        
# Run crawler
from scrapy import crawler
from scrapy.utils.project import get_project_settings

process = crawler.CrawlerProcess(get_project_settings())

# Example parameters
flat_house = "immobilien"
rent_buy = "kaufen"
place_lvl = "kanton"
place = "appenzell-ar"


process.crawl(ImmoSpider, flat_house=flat_house, rent_buy=rent_buy, place=place, place_lvl=place_lvl)
process.start()
process.closed()