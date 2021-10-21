# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    search = 'python'

    start_urls = [f'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={search}&showClusters=true']

    def parse(self, response: HtmlResponse):

        next_page = 'https://hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']
        print(next_page)
        vacancy_links = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)').extract()
        for link in vacancy_links:
            url = response.urljoin(link)
            yield response.Request(url, callback=self.vacancy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def vacancy_parse(self, response: HtmlResponse):
        name_job = response.css('h1[data-qa="vacancy-title"]::text').getall()
        salary_job = response.css('div.vacancy-salary::text').extract()
        location_job = response.css('span[data-qa="vacancy-view-raw-address"]::text').extract()
        position_link = response.url
        company_job = response.css('span[class="bloko-section-header-2 bloko-section-header-2_lite"]::text').extract()

        yield JobparserItem(name=name_job, salary=salary_job, location=location_job,
                            link=position_link, company=company_job)

