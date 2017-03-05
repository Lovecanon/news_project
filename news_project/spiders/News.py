# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_project import MongoUtils


class NewsSpider(CrawlSpider):
    name = "news"
    allowed_domains = ["news.163.com"]
    start_urls = ['http://news.163.com/']

    mongo = MongoUtils.MongoDB()
    coll = mongo.db['news_163']

    item_buff = []

    rules = [
        Rule(LinkExtractor(allow=(r'http://news.163.com/[a-zA-Z]+/$'))),
        Rule(LinkExtractor(allow=(r'http://news.163.com/\d+/\d+/\d+/[a-zA-Z0-9]+\.html')), callback="parse_item"),
    ]

    def parse_item(self, response):
        self.logger.info('+++Visiting %s website.' % response.url)
        buff = ''
        title = response.xpath('//div[@id="epContentLeft"]/h1/text()').extract()
        content = response.xpath('//div[@id="endText" and p]/*[not(self::scrip|self::style)]/text()').extract()
        if len(title) == 0 or len(content) == 0:
            yield

        for i in content:
            if i and not i.startswith('\n'):
                buff += i.strip().replace('\n', '')
        result = {'title': title[0].strip(), 'content': buff}
        self.item_buff.append(result)
        if len(self.item_buff) > 50:
            self.log('++++Title is' + title[0])
            self.coll.insert_many(self.item_buff)
            self.item_buff.clear()
        yield
