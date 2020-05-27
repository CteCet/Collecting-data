# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabruSpider(scrapy.Spider):
    name = 'labru'
    allowed_domains = ['labirint.ru']

    def __init__(self, book):
        self.start_urls = [f'https://www.labirint.ru/search/{book}/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']/a/@href").extract_first()
        book_links = response.xpath("//a[@class = 'product-title-link']/@href").extract()
        for link in book_links:
            yield response.follow(link, callback=self.book_parse)
        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//div/h1/text()").extract_first()
        price = response.xpath("//div[@class = 'buying-priceold-val']/span/text()").extract_first()
        if not price:
            price = response.xpath("//span[@class = 'buying-price-val-number']/text()").extract_first()
        discount = response.xpath("//div[@class = 'buying-pricenew-val']/span[1]/text()").extract_first()
        author = response.xpath("//div[@class = 'authors'][1]/a/text()").extract()
        rating = response.xpath("//div[@id = 'rate']/text()").extract_first()
        link = response.url
        yield BookparserItem(name=name, price=price, discount=discount, author=author, rating=rating, link=link)




