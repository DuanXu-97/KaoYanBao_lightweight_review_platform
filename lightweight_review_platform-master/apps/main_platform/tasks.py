from celery import task
import os
import sys


path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),'hotspot_spider')
os.chdir(path)

@task()
def spider():
    os.system("scrapy crawl kaoyan")
