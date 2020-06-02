# -*- coding: utf-8 -*-
import scrapy
from ..items import B2B168Item


class B2bSpider(scrapy.Spider):
    name = 'b2b'
    allowed_domains = ['b2b168.org']
    start_urls = ['https://b2b168.org/']
    base_url = 'https://www.b2b168.org'
    base_area_url = 'https://www.b2b168.org/p-chanpin.html'

    def parse(self, response):
        ul_lists = response.xpath('//ul[@class="cate_list"]/li/div/a/@href').getall()
        for ul_list in ul_lists:
            yield scrapy.Request(url=self.base_url + ul_list, callback=self.parse_list1)

        yield scrapy.Request(url=self.base_area_url, callback=self.parse_area)

    def parse_list1(self, response):
        type_list = response.xpath('//div[@class="hyindL"]/ul/h2/a/@href').getall()

        for type_url in type_list:
            yield scrapy.Request(url=self.base_url + type_url, callback=self.parse_list2)

    def parse_list2(self, response):
        com_list = response.xpath('//div[@class="hyR2"]/ul/a/@href').getall()
        for com_url in com_list:
            yield scrapy.Request(url=self.base_url + com_url, callback=self.parse_detail)

        next_page = response.xpath('//div[@class="page"]/a[last()-1]/@aref').get()

        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse_list2)

    def parse_area(self, response):
        provinces = response.xpath('//ul[@class="adidqhy_c"]/a/@href').getall()[:-1]
        for province in provinces:
            yield scrapy.Request(url=self.base_url+province, callback=self.parse_countrys)
        com_list = response.xpath('//div[@class="hyR2"]/ul/a/@href').getall()
        for com_url in com_list:
            yield scrapy.Request(url=self.base_url + com_url, callback=self.parse_detail)

        next_page = response.xpath('//div[@class="page"]/a[last()-1]/@aref').get()
        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse_area)

    def parse_countrys(self, response):
        shis = response.xpath('//ul[@class="quyuhy"]/a/@href').getall()
        for shi in shis:
            yield scrapy.Request(url=self.base_url+shi)
        com_list = response.xpath('//div[@class="hyR2"]/ul/a/@href').getall()
        for com_url in com_list:
            yield scrapy.Request(url=self.base_url + com_url, callback=self.parse_detail)

        next_page = response.xpath('//div[@class="page"]/a[last()-1]/@aref').get()
        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse_countrys)

    def parse_shi(self, response):
        qus = response.xpath('//ul[@class="quyuhy"]/a/@href').getall()
        for qu in qus:
            yield scrapy.Request(url=self.base_url+qu, callback=self.parse_qu)
        com_list = response.xpath('//div[@class="hyR2"]/ul/a/@href').getall()
        for com_url in com_list:
            yield scrapy.Request(url=self.base_url + com_url, callback=self.parse_detail)

        next_page = response.xpath('//div[@class="page"]/a[last()-1]/@aref').get()
        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse_shi)

    def parse_qu(self, response):
        jiedaos = response.xpath('//ul[@class="quyuhy"]/a/@href').getall()
        for jiedao in jiedaos:
            yield scrapy.Request(url=self.base_url+jiedao, callback=self.parse_jiedao)
        com_list = response.xpath('//div[@class="hyR2"]/ul/a/@href').getall()
        for com_url in com_list:
            yield scrapy.Request(url=self.base_url + com_url, callback=self.parse_detail)

        next_page = response.xpath('//div[@class="page"]/a[last()-1]/@aref').get()
        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse_qu)

    def parse_jiedao(self, response):
        jiedaos = response.xpath('//ul[@class="quyuhy"]/a/@href').getall()
        for jiedao in jiedaos:
            yield scrapy.Request(url=self.base_url + jiedao, callback=self.parse_jiedao)
        com_list = response.xpath('//div[@class="hyR2"]/ul/a/@href').getall()
        for com_url in com_list:
            yield scrapy.Request(url=self.base_url + com_url, callback=self.parse_detail)

        next_page = response.xpath('//div[@class="page"]/a[last()-1]/@aref').get()
        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse_qu)

    def parse_detail(self, response):
        item = B2B168Item()
        com_name = response.xpath('//h1/text()').get()
        hangye = response.xpath('//li[@class="time"]/a/text()').getall()
        gongyingchangjia = response.xpath('//li[@class="l1"][1]/span[2]/text()').get()
        address = response.xpath('//li[@class="l1"][2]/span[2]/text()').get()
        product = response.xpath('//li[@class="l1"][4]/span[2]/text()').get()
        lianxiren = response.xpath('//li[@class="l2"]/span[@class="t1"]/text()').get()
        dianhua = response.xpath('//li[@class="l2"]/span[@class="t3"]/text()').get().strip()

        item['com_name'] = com_name
        item['hangye'] = ' '.join(hangye)
        item['gongyingchangjia'] = gongyingchangjia
        item['address'] = address
        item['product'] = product[:90]
        item['lianxiren'] = lianxiren
        item['dianhua'] = dianhua

        yield item

