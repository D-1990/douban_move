# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import unicodedata

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']

    # 定义存储的数据
    sql_data = dict(
        name = '', # 电影名称
        intro = '', # 电影简介
        grade = '' , # 电影评分
        move_type = '', # 电影类型
        image_url = '', # 电影封面地址
        rank = '' ,# 电影排名
    )

    def start_requests(self):
        for i in range(10):
            url = 'https://movie.douban.com/top250' +'?start=%s&filter=' %(i*25)
            request = scrapy.Request(
                url=url,
                callback=self.parse
            )
            yield request

    def parse(self, response):
        # 每个电影详细页面地址
        url_href = response.xpath('//li//div[@class="hd"]/a/@href').extract()
        for url in url_href:
            request = scrapy.Request(
                        url=url,
                        callback = self.parse1
                    )
            yield request

    def parse1(self,response):
        sql_data = deepcopy(self.sql_data)
        # 电影名称
        sql_data['name'] = response.xpath('//h1/span[1]/text()').extract_first()
        # 电影排名
        sql_data['rank'] = response.xpath('//div[@class="top250"]/span[1]/text()').extract_first()
        # 电影评分
        sql_data['grade'] = response.xpath('//div[@class="rating_self clearfix"]/strong/text()').extract_first()
        # 电影类型
        move_type = response.xpath('//div[@id="info"]//span[@property="v:genre"]/text()').extract()
        sql_data['move_type'] = '/'.join(move_type)
        # 电影简介
        # 判断有没有需要展开的Js
        if response.xpath('//div[@id="link-report"]/span[@class="all hidden"]/text()'):
            intro_list = response.xpath('//div[@id="link-report"]/span[@class="all hidden"]/text()').extract()
            intro_str = ' '.join(intro_list)
            sql_data['intro'] = unicodedata.normalize('NFKC', intro_str).strip()
        else:
            intro_list = response.xpath('//div[@id="link-report"]/span[@property="v:summary"]/text()').extract()
            intro_str = ' '.join(intro_list)
            sql_data['intro'] = unicodedata.normalize('NFKC', intro_str).strip()
        # 电影封面地址
        sql_data['image_url'] = response.xpath('//div[@id="mainpic"]/a/img/@src').extract_first()
        yield sql_data



