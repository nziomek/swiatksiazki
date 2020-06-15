# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from swiatksiazki.items import SwiatksiazkiItem

class SwiatksiazkiBooksSpider(CrawlSpider):
    name = 'swiatksiazki_books'
    allowed_domains = ['swiatksiazki.pl']
    start_urls = ['https://www.swiatksiazki.pl/Ksiazki/ksiazki-3799.html?p=1&product_list_limit=50']

    rules = (
        Rule(LinkExtractor(allow=('.+ksiazka\.html$'), restrict_xpaths='//a[@class="product-item-link"]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="action  next"]')),
    )

    custom_settings = {
        'DOWNLOAD_DELAY':.5,
        'FEED_FORMAT':'csv',
        'FEED_URI':'books.csv'
    }

    en_pl_dic = {
        "autor":"author",
        "kategorie":"categories",
        "typ okładki":"cover",
        "wydawca":"publisher",
        "wymiary":"size",
        "ilość stron":"pages_count",
        "seria":"series",
        "data wydania":"date_published",
        "EAN":"ean",
        }

    def parse_item(self, response):

        item = SwiatksiazkiItem()

        #table containing specific details, which may vary from product to product
        details_table = response.xpath('//ul[@class="product-info-attributes"]//li')

        #assigning values in table rows to the correct item fields based on the first column information
        for detail in details_table:
            #first column, indicator data
            info_val = detail.xpath('.//span//text()').extract_first().lower().strip()[:-1]
            #second column, data that will actually be stored
            info = detail.xpath('.//text()[not(parent::span or parent::div)]').extract()
            info = ''.join(list(filter(None, [x.strip() for x in info])))
            #translating indicator values from Polish to English
            for word_pl, word_en in self.en_pl_dic.items():
                info_val = info_val.replace(word_pl, word_en)
            #assigning selected values if present
            try:
                item[info_val] = info
            except:
                pass

        price_old_tag = item['price_old'] = response.xpath('//div[@class="product-info-main"]//span[contains(@id,"old-price")]//span')

        #checking if there is an old price and assigning proper value
        if price_old_tag:
            price_old = price_old_tag.xpath('.//text()').extract_first().replace('\xa0', ' ')
        else:
            price_old = None

        item['price_old'] = price_old

        #assigning values always present on page
        item['title'] = response.xpath('//h1//span[@itemprop="name"]//text()').extract_first().strip()
        item['price'] = response.xpath('//div[@class="product-info-main"]//span[contains(@id,"product-price")]//span//text()').extract_first().replace('\xa0', ' ')


        return item
