#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
from scrapy import Spider, Request, Selector

from meizi.items import EveriaItem, EveriaPicItem


class everia(Spider):
    name = 'everia'
    start_urls = [
         'https://everia.club/category/aidol/',
         'https://everia.club/category/gravure/',
         'https://everia.club/category/magazine/',
        #'https://everia.club/category/thailand/',
         'https://everia.club/category/chinese/',
    ]
    allow_domains = ['https://everia.club']

    def parse(self, response):
        album_list = response.xpath('//*[@id="main"]/div/div').extract()
        for album in album_list:
            album_selector = Selector(text=album)
            album_cover = album_selector.xpath('//article/div[1]/a/noscript/img/@src').extract_first()
            album_detail_url = album_selector.xpath('//article/div[1]/a/@href').extract_first()
            album_id = album_selector.xpath('//article/@id').extract_first()
            yield Request(url=album_detail_url, callback=self.parse_detail, meta={
                'cover': album_cover,
                'url': album_detail_url,
                'origin_id': album_id
            })

        previous_page = response.xpath('//*[@class="nav-previous"]').extract()
        if len(previous_page) > 0:
            url = Selector(text=previous_page[0]).xpath('//a/@href').extract_first()
            yield Request(url=url, callback=self.parse)

    def parse_detail(self, response):
        cover = response.meta['cover']
        url = response.meta['url']
        origin_id = response.meta['origin_id']
        title = response.xpath('//*[@id="main"]/article/header/div/h1/text()').extract_first()
        category = response.xpath('//*[@id="main"]/article/header/div/ul/li[2]/a/text()').extract_first()
        everia_item = EveriaItem(origin_id=origin_id, cover_url=cover,
                                 album_url=url, title=title, category=category, pictures=[])
        pic_list = response.xpath('//*[@id="main"]/article/div/div').extract()
        for index in range(len(pic_list)):
            pic_html = pic_list[index]
            pic_selector = Selector(text=pic_html)
            url = pic_selector.xpath('//a/@href').extract_first()

            everia_pic_item = EveriaPicItem(order=index, url=url)
            everia_item['pictures'].append(everia_pic_item)

        yield everia_item
        pass
