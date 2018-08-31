# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from main_platform.models  import Hotspot

class NewsItem(DjangoItem):
    django_model=Hotspot
    # define the fields for your item here like:
    # name = scrapy.Field()
   # name=scrapy.Field()

    #keywd=scrapy.Field()

    #content=scrapy.Field()

   # date=scrapy.Field( )


    pass
