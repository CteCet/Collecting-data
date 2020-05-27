# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Bk24ruSpider(scrapy.Spider):
    name = 'bk24ru'
    allowed_domains = ['book24.ru']

    def __init__(self, book):
        self.start_urls = [f'https://book24.ru/search/?q={book}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class = 'catalog-pagination__list']//a[last()]/@href").extract_first()
        book_links = response.xpath("//div[@class = 'book__title ']//a/@href").extract()
        for link in book_links:
            yield response.follow(link, callback=self.book_parse)
        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//div/h1/text()").extract_first()
        discount = response.xpath("//div[@class = 'item-actions__price']/b/text()").extract_first()
        price = response.xpath("//div[@class = 'item-actions__price-old']/text()").extract_first()
        if not price:
            price = discount
            discount = None
        elif 'р.' in price:
            price = price.replace(' р.', '')
        author = response.xpath("//div[@class = 'item-tab__chars-list']/div[1]/span[2]/a[contains(@class,'item-tab__chars-link')]/text()").extract()
        rating = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()
        link = response.url
        yield BookparserItem(name=name, price=price, discount=discount, author=author, rating=rating, link=link)
