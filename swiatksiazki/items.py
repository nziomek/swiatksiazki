# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SwiatksiazkiItem(scrapy.Item):
    title = scrapy.Field()
    categories = scrapy.Field()
    cover = scrapy.Field()
    publisher = scrapy.Field()
    size = scrapy.Field()
    pages_count = scrapy.Field()
    series = scrapy.Field()
    date_published = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    price_old = scrapy.Field()
    ean = scrapy.Field()
