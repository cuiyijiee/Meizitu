# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy

from peewee import *

db = MySQLDatabase("qingcheng", host='47.99.116.76', port=3306, user='root', passwd='Abc,123.', charset='utf8')


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


class PW_Category(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'category'
        database = db


class PW_Album(Model):
    id = IntegerField(primary_key=True)
    origin_id = CharField()
    cover_url = CharField()
    album_url = CharField()
    title = CharField()
    category = IntegerField()
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'album'
        database = db


class PW_Picture(Model):
    id = IntegerField(primary_key=True)
    album_id = IntegerField()
    url = CharField()
    index = IntegerField()

    class Meta:
        db_table = 'picture'
        database = db
