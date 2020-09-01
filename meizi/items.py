# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItubaccItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    sort_1 = scrapy.Field()
    # sort_1_url = scrapy.Field()
    sort_2 = scrapy.Field()
    name = scrapy.Field()
    # page_url = scrapy.Field()
    order = scrapy.Field()
    origin_url = scrapy.Field()

    pass


class EveriaItem(scrapy.Item):
    origin_id = scrapy.Field()
    cover_url = scrapy.Field()
    album_url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    pictures = scrapy.Field()
    pass


class EveriaPicItem(scrapy.Item):
    url = scrapy.Field()
    order = scrapy.Field()
    pass
