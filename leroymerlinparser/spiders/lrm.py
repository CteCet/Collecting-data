# -*- coding: utf-8 -*-
import scrapy
from leroymerlinparser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader

class LrmSpider(scrapy.Spider):
    name = 'lrm'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}']

    def parse(self, response):
        next_page = response.xpath("//div[@view-type='secondary']//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()
        links = response.xpath("//div[@class='product-name']/a/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.product_parse)
        yield response.follow(next_page, callback=self)

    def product_parse(self, response):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('photo', "//img[@alt = 'product image']/@src")
        loader.add_xpath('price', "//uc-pdp-price-view[@slot = 'primary-price']/span[@slot = 'price']/text()")
        loader.add_xpath('features', "//dl/div")

        yield loader.load_item()



