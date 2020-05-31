# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose, TakeFirst
import scrapy
from lxml import html

# def cleaner_photo(value):
#     if value[:2] == '//':
#         return f'http:{value}'
#     return value


def cleaner_price(value):
    if ',' in value:
        value = float(value)
    else:
        value = int(value.replace(u' ', u''))
    return value


def features_dic(param):
    keys = html.fromstring(param).xpath('//dt/text()')[0]
    values = html.fromstring(param).xpath('./dd/text()')[0]
    values = ' '.join(list(filter(None, values.replace('\n', '').split(' '))))
    param = {keys: values}
    return param


class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(cleaner_price))
    features = scrapy.Field(input_processor=MapCompose(features_dic))
