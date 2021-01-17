# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib.request
import pymongo

from meizi.items import ItubaccItem, EveriaItem, PW_Category, PW_Album, PW_Picture


class MeiziPipeline(object):
    base_save_dir = os.environ['HOME'] + "/meizi"
    myclient = pymongo.MongoClient('mongodb://cuiyijie:Abc,123.@localhost:27017/')
    mydb = myclient['meizi']

    exist_category = {}

    def __init__(self):
        if not os.path.exists(self.base_save_dir):
            os.mkdir(self.base_save_dir)

        if not PW_Category.table_exists():
            PW_Category.create_table(safe=True)
        else:
            print("category table already created!")

        if not PW_Album.table_exists():
            PW_Album.create_table(safe=True)
        else:
            print("album table already created!")

        if not PW_Picture.table_exists():
            PW_Picture.create_table(safe=True)
        else:
            print("picture table already created!")

        # 从数据库中取出所有的目录
        for category in PW_Category.select():
            self.exist_category[category.name] = category.id

    def process_item(self, item, spider):

        if type(item) is ItubaccItem:
            self.download_pic(item)
        elif type(item) is EveriaItem:
            # select_count = self.mydb['everia'].count({'origin_id': item['origin_id']})
            # if select_count == 0:
            #     insert_result = self.mydb['everia'].insert_one(dict(item))
            #     print(insert_result.inserted_id)
            # print(item)
            if item['category'] not in self.exist_category:
                insert_result = PW_Category.create(name=item['category'])
                self.exist_category[item['category']] = insert_result.id
                category_id = insert_result.id
            else:
                category_id = self.exist_category[item['category']]
            album, created = PW_Album.get_or_create(origin_id=item['origin_id'], defaults={
                'origin_id': item['origin_id'],
                'cover_url': item['cover_url'],
                'album_url': item['album_url'],
                'title': item['title'],
                'category': category_id
            })

            already_saved_pic_count = PW_Picture.select().where(PW_Picture.album_id == album.id).count()
            crawled_pics = item['pictures']
            if already_saved_pic_count != len(crawled_pics):
                PW_Picture.delete().where(PW_Picture.album_id == album.id)
                album_picture_data = []
                for pic in crawled_pics:
                    album_picture_data.append({
                        'album_id': album.id,
                        'url': pic['url'],
                        'index': pic['order']
                    })
                PW_Picture.insert_many(album_picture_data).execute()
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
