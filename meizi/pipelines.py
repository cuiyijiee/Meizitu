# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib.request
import pymongo

from meizi.items import ItubaccItem, EveriaItem


class MeiziPipeline(object):
    base_save_dir = os.environ['HOME'] + "/meizi"
    myclient = pymongo.MongoClient('mongodb://cuiyijie:cuiyijie987@172.17.0.5:27017/')
    mydb = myclient['meizi']

    def __init__(self):
        if not os.path.exists(self.base_save_dir):
            os.mkdir(self.base_save_dir)

    def process_item(self, item, spider):

        if type(item) is ItubaccItem:
            self.download_pic(item)
        elif type(item) is EveriaItem:
            # select_count = self.mydb['everia'].count({'origin_id': item['origin_id']})
            # if select_count == 0:
            #     insert_result = self.mydb['everia'].insert_one(dict(item))
            #     print(insert_result.inserted_id)
            print(item)
        return item

    def download_pic(self, item):
        img_url = item['origin_url']
        file_suffix = os.path.splitext(img_url)[1]

        albumn_dir_path = self.base_save_dir + "/" + item['sort_1'] + "/" + item['sort_2'] + '/' + item['name']
        if not os.path.exists(albumn_dir_path):
            os.makedirs(albumn_dir_path)

        img_save_path = albumn_dir_path + '/' + str(item['order']) + file_suffix
        if not os.path.exists(img_save_path):
            if item['origin_url'].startswith('http'):
                urllib.request.urlretrieve(item['origin_url'], filename=img_save_path)
            else:
                urllib.request.urlretrieve("http:" + item['origin_url'], filename=img_save_path)
