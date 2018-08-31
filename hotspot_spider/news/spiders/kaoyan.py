# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import NewsItem
import re
class KaoyanSpider(CrawlSpider):
    name = 'kaoyan'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://edu.sina.com.cn']

    rules = (
        Rule(LinkExtractor(allow=('.*?/[0-9]{4}.[0-9]{2}.[0-9]{2}.doc-.*?shtml'),allow_domains=('edu.sina.com.cn')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = NewsItem()
        patt='[0-9]{4}-[0-9]{2}-[0-9]{2}'
        i["title"]=response.xpath("/html/head/title/text()").extract( )

       # i["keywd"]=response.xpath("/html/head/meta[@name='keywords']/@content").extract()

        i["content"]=response.xpath("//div[@id='artibody']/p/text()").extract( )
        i["content"]="\n".join(i["content"])
       # number=len(response.xpath("/html/head/m  eta[@property='org:url']/@content").extract())
       # print(number)
        i["date"]=re.search(patt,response.xpath("/html/head/meta[@property='og:url']/@content").extract()[0]).group()

       # print(i["date"])

        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
