#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
from scrapy import Spider, Request, Selector

from meizi.items import MeiziItem


class zol_cpu(Spider):
    name = 'meizi'
    start_urls = ['https://www.ituba.cc/meinvtupian/']
    allow_domains = ['https://www.ituba.cc']

    def parse(self, response):
        page_size = response.xpath('//*[@id="pageinfo"]/strong[1]/text()').extract()[0]

        for index in range(1, int(page_size) + 1):
            page_url = 'https://www.ituba.cc/meinvtupian/p' + str(index) + '.html'
            yield Request(url=page_url, callback=self.parseAlbumn)

    def parseAlbumn(self, response):
        albumn_list = response.xpath('//div[@id="NewList"][1]/ul/li').extract()

        sort_1 = "美女图片"

        for albumn in albumn_list:
            albumn_selector = Selector(text=albumn)

            sort_2 = albumn_selector.xpath('//span/em/a/text()').extract()[0]
            name = albumn_selector.xpath('//a[@class="PicTxt"]/@title').extract()[0]
            albumn_first_url = albumn_selector.xpath('//a[1]/@href').extract()[0]
            id = re.findall(r'\d+?\d*', albumn_first_url)[0]
            base_url = albumn_selector.xpath('//span/em/a/@href').extract()[0]
            size_temp = albumn_selector.xpath('//p[@class="Click"]/i[2]/text()').extract()[0]
            try:
                size = re.findall(r'\d+?\d*', size_temp)[0]
            except IndexError as e:
                print(albumn)

            for index in range(1, int(size)):
                pic_url = base_url + str(id) + '_' + str(index) + '.html'
                yield Request(url=pic_url, callback=self.parseOriginUrl, meta={
                    'sort_1': sort_1,
                    'sort_2': sort_2,
                    'name': name,
                    'order': index,
                })

    def parseOriginUrl(self, response):
        origin_url = response.xpath('//a[@tt]/img/@src').extract()[0]
        item = MeiziItem()
        item['sort_1'] = response.meta['sort_1']
        item['sort_2'] = response.meta['sort_2']
        item['name'] = response.meta['name']
        item['order'] = response.meta['order']
        item['origin_url'] = origin_url
        yield item





