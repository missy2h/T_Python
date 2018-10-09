# -*- coding: utf-8 -*-
import json
import os

import scrapy

from HN_picture.items import HnPictureItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

all_page_link = [] #存储每个分类的路径
final_page_link=[] #存储每张图片的路径
list = []

trantab = str.maketrans('\/:*?"<>|', 'abcdefghi')

class HpcSpider(scrapy.Spider):
    name = 'hpc'
    allowed_domains = ['www.haoniu520.com']
    start_urls = ['http://www.haoniu520.com/news/list_63.html']

    rules = [
        Rule(LinkExtractor(allow=(r'news/list_63_\[2-4]\.html')), callback='parse')
    ]

    def parse(self, response):
        print('--------开始--------')
        root_path = 'D:/pics'
        d_name = []
        if response.url not in all_page_link:
            all_page_link.append(response.url)
            detail_page = response.xpath('//ul[@class="list-item"]//a/@href').extract()
            detail_name = response.xpath('//ul[@class="list-item"]//a/text()').extract()
            # 去除list[detail_name]中的空行
            detail_name = [x for x in detail_name if x != ' ']
            for de_name in detail_name:
                d_name.append(de_name.replace(" ",""))
            # list[detail_page]与list[d_name]长度需对应，否则建立对应的文件夹不全
            for page,name in zip(detail_page,d_name):
                name = name.translate(trantab)
                dir_path = '%s/%s'%(root_path,name)
                if not os.path.exists(dir_path):
                    list.append(dir_path)
                    os.mkdir(dir_path)
                yield scrapy.Request(response.urljoin(page),callback =self.pic_download)

    def pic_download(self,response):
        item = HnPictureItem()
        pic_name = response.xpath('//div[@class="content-wrap"]/h1/text()').extract()[0]
        pic_name = pic_name.replace(" ","")
        # item['pic_name'] = pic_name.translate(trantab)
        item['pic_url'] = response.xpath('//div[@class="content-wrap"]//img/@src').extract()[1:]
        # yield item
        print(item['pic_url'])
        for e_pic_url in item['pic_url']:
            item['pic_name'] = pic_name.translate(trantab)
            item['pic_url'] = response.urljoin(e_pic_url)
            yield item
            # print(item)

        # for e_pic_url in item['pic_url']:
        #     yield scrapy.Request(response.urljoin(e_pic_url), callback=self.pic_download_next)


    # def pic_download_next(self,response):
    #     item = HnPictureItem()
    #     pic_name = response.xpath('//h1/text()').extract()[0]
    #     pic_name = pic_name.replace(" ", "")
    #     print(pic_name)
    #     item['pic_name'] = pic_name.translate(trantab)
    #     item['pic_url'] = response.xpath('//div[@class="content-wrap"]//img/@src').extract()[1:]
    #     yield item