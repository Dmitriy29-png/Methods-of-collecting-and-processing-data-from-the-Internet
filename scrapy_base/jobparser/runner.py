# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser.spiders.leroymerlin import LeroymerlinSpider
from jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, text='обои')
    process.start()