# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy

from meizi.settings import *

from peewee import *

db = PostgresqlDatabase(DATABASE_NAME,
                        host=DATABASE_IP,
                        port=DATABASE_PORT,
                        user=DATABASE_USERNAME,
                        password=DATABASE_PASSWORD)


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
    id = AutoField(primary_key=True)
    name = CharField()
    created_at = DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'category'
        database = db
        schema = DATABASE_SCHEMA


class PW_Album(Model):
    id = BigAutoField(primary_key=True)
    origin_id = CharField()
    cover_url = CharField()
    album_url = CharField()
    title = CharField()
    category = IntegerField()
    created_at = DateTimeField(default=datetime.now())
    enabled = BooleanField()

    class Meta:
        table_name = 'album'
        database = db
        schema = DATABASE_SCHEMA


class PW_Picture(Model):
    id = BigAutoField(primary_key=True)
    album_id = IntegerField()
    url = CharField()
    pic_index = IntegerField()

    class Meta:
        table_name = 'picture'
        database = db
        schema = DATABASE_SCHEMA
