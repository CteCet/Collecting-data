from lxml import html
from pprint import pprint
import requests
from datetime import datetime, date, timedelta
import json

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                    Chrome/81.0.4044.138 Safari/537.36'}


def get_news_mail():
    main_link = 'https://news.mail.ru/'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)

    links = dom.xpath("//span/a[contains(@href, 'politics')]/@href")

    news = []

    for i in range(len(links)):
        data = {}
        data['links'] = main_link + links[i]
        link = data['links']
        response = requests.get(link, headers=header)
        dom = html.fromstring(response.text)

        text = dom.xpath("//h1[@class = 'hdr__inner']/text()")
        source = dom.xpath("//span[@class ='note']/a/span/text()")
        dates = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
        for j in range(len(source)):
            data['text'] = text[j]
            data['source'] = source[j]
            data['date'] = dates[j].replace(u'T', u' ')
            news.append(data)

    return news


def get_news_lenta():
    main_link = 'https://lenta.ru/'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)

    links = dom.xpath("//div/section[contains(@class, 'top-seven')]/div/div[@class = 'item']/a/@href")
    text = dom.xpath("//div/section[contains(@class, 'top-seven')]/div/div[@class = 'item']/a/text()")
    dates = dom.xpath("//div/section[contains(@class, 'top-seven')]/div/div[@class = 'item']/a/time/@datetime")

    news = []
    for i in range(len(links)):
        data = {}
        data['links'] = main_link + links[i]
        data['text'] = text[i].replace(u'\xa0', u' ')
        data['dates'] = dates[i]
        news.append(data)

    return news


def get_news_yandex():
    main_link = 'https://yandex.ru'
    response = requests.get(main_link + '/news/', headers=header)
    dom = html.fromstring(response.text)

    link = dom.xpath("//div[@aria-labelledby = 'politics']/a/@href")
    # link = 'https://yandex.ru/news/rubric/politics'

    response = requests.get(link[0], headers=header)
    dom = html.fromstring(response.text)

    links = dom.xpath("//h2[@class = 'story__title']/a/@href")
    text = dom.xpath("//h2[@class = 'story__title']/a/text()")
    source = dom.xpath("//div[@class = 'story__info']/div/text()")

    date_format = '%d-%m-%Y'

    news = []
    for i in range(len(links)):
        data = {}
        data['links'] = main_link + links[i]
        data['text'] = text[i].replace(u'\xa0', u' ')
        if 'вчера' in source[i]:
            data['dates'] = (date.today() - timedelta(days=1)).strftime(date_format)
        else:
            data['dates'] = date.today().strftime(date_format)
        data['source'] = source[i][:-6].replace(u'\xa0', u' ').replace('вчера в', '')

        news.append(data)

    return news


news_y = get_news_yandex()
pprint(news_y)

with open("news_yandex.json", "w") as write_file:
    json.dump(news_y, write_file)

news_m = get_news_mail()
pprint(news_m)

with open("news_mail.json","w") as write_file:
    json.dump(news_m, write_file)

news_l = get_news_lenta()
pprint(news_l)

with open("news_lenta.json", "w") as write_file:
    json.dump(news_l, write_file)