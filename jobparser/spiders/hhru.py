# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    search = 'Python'

    start_urls = [f'https://hh.ru/search/vacancy?area=&st=searchVacancy&text={search}']

    def parse(self, response: HtmlResponse):

        next_page = 'https://hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']

        print(next_page)
        response.follow(next_page, callback=self.parse)

        vacancy_links = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)').extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def vacancy_parse(self, response: HtmlResponse):
        name_job = response.css('h1[data-qa="vacancy-title"::text').extract_first()
        salary_job = response.css('span[data-qa="vacancy-serp__vacancy-compensation"]'
                                    '[class="bloko-header-section-3 bloko-header-section-3_lite"]::text').extract()
        location_job = response.xpath('div[@data-qa="vacancy-serp__vacancy-address"]//text()').extract()
        position_link = 'hh.ru'
        company_job = response.xpath('a[@class="bloko-link bloko-link_secondary"]/text()').extract()


        yield JobparserItem(name=name_job, salary=salary_job, location=location_job,
                            link=position_link, company=company_job)