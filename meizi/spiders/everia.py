#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from scrapy import Spider, Request, Selector

from meizi.items import EveriaItem, EveriaPicItem, PW_Album


class everia(Spider):
    name = 'everia'
    start_urls = [
        'https://everia.club/category/aidol/',
        'https://everia.club/category/gravure/',
        'https://everia.club/category/magazine/',
        'https://everia.club/category/korea/',
        'https://everia.club/category/cosplay/',
        'https://everia.club/category/thailand/',
        'https://everia.club/category/chinese/',
    ]
    allow_domains = ['https://everia.club']

    def parse(self, response):
        album_list = response.xpath('//*[@id="content"]/div/div/div[1]/div[2]/article').extract()
        for album in album_list:
            album_selector = Selector(text=album)
            album_cover = album_selector.xpath('//article/div/div/div/a/img/@src').extract_first()
            album_detail_url = album_selector.xpath('//article/div/div/h2/a/@href').extract_first()
            album_id = album_selector.xpath('//article/@id').extract_first()
            yield Request(url=album_detail_url, callback=self.parse_detail, meta={
                'cover': album_cover,
                'url': album_detail_url,
                'origin_id': album_id
            })

        if len(album_list) > 0:
            # 判断当前页面的最后一个是否被采集了，如果已经采集过了，则不进行翻页操作
            last_album_of_this_page = album_list[-1]
            album_selector = Selector(text=last_album_of_this_page)
            album_id = album_selector.xpath('//article/@id').extract_first()
            if PW_Album.get_or_none(origin_id=album_id) is None:
                previous_page = response.xpath('//*[@id="content"]/div/div/div[1]/ul/li[6]/a').extract()
                if len(previous_page) > 0:
                    url = Selector(text=previous_page[0]).xpath('//a/@href').extract_first()
                    yield Request(url=url, callback=self.parse)

    def parse_detail(self, response):
        cover = response.meta['cover']
        url = response.meta['url']
        origin_id = response.meta['origin_id']

        category = "everia"
        article_class = response.xpath('//*[@id="content"]/div/div/article/@class').extract_first()
        article_class_arr = article_class.split(' ')
        for index in range(len(article_class_arr)):
            class_name = article_class_arr[index]
            if class_name.startswith('category-') and not class_name.endswith('everia'):
                category = class_name.split('-')[1]
                break
        category = category.capitalize()

        title = response.xpath('//*[@id="content"]/div/div/article/div[1]/div/h1/text()').extract_first()
        # category_list = response.xpath('//*[@id="main"]/article/header/div/ul/li[2]/a/text()').extract()
        # category = category_list[0]
        # if (category == 'EVERIA') & (len(category_list) == 2):
        #     category = category_list[1]
        everia_item = EveriaItem(origin_id=origin_id, cover_url=cover,
                                 album_url=url, title=title, category=category, pictures=[])
        pic_list = response.xpath('//*[@id="content"]/div/div/article/div[2]/div').extract()
        for index in range(len(pic_list)):
            pic_html = pic_list[index]
            pic_selector = Selector(text=pic_html)
            url = pic_selector.xpath('//a/@href').extract_first()

            everia_pic_item = EveriaPicItem(order=index, url=url)
            everia_item['pictures'].append(everia_pic_item)

        yield everia_item
        pass

