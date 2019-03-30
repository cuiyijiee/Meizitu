# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os,stat
import urllib.request


class MeiziPipeline(object):
    def process_item(self, item, spider):
        img_url = item['origin_url']
        file_suffix = os.path.splitext(img_url)[1]

        file_sort_1_path = 'D:/meizi/' + item['sort_1']
        if not os.path.exists(file_sort_1_path):
            os.mkdir(file_sort_1_path)

        file_sort_2_path = file_sort_1_path + '/' + item['sort_2']
        if not os.path.exists(file_sort_2_path):
            os.mkdir(file_sort_2_path)

        albumn_dir_path = file_sort_2_path + '/' + item['name']
        if not os.path.exists(albumn_dir_path):
            os.mkdir(albumn_dir_path)

        img_save_path = albumn_dir_path + '/' + str(item['order']) + file_suffix
        img_url = item['origin_url']
        if not os.path.exists(img_save_path):
            urllib.request.urlretrieve(img_url, filename=img_save_path)

        return item

