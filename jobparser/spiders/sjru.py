import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    search = 'Python'
    start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        vacancy_links = response.xpath('//div.fDQrW iJCa5 f-test-vacancy-item _1fma_ _2nteL div.jNMYr GPKTZ _1tH7S '
                                       'a.icMQ_ _6AfZ9 f-test-link-Junior_Full_Stack_Python_Engineer _2JivQ _1UJAN::attr(href)').extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(selfself, response: HtmlResponse):
        name_job = response.xpath('//div[@class="_2rfUm _2hCDz _21a7u"]//text()').extract_first()
        salary_job = response.xpath('//span[@class="_1OuF_ _1qw9T f-test-text-company-item-salary"]//text()').extract()
        location_job = response.xpath('//div[@class="f-test-text-company-item-location e5P5i _2hCDz _2ZsgW _1RQyC"]//text()').extract()
        position_link = 'sjru.ru'
        company_job = response.xpath('//span[@class="_3Fsn4 f-test-text-vacancy-item-company-name e5P5i _2hCDz _2ZsgW _2SvHc"]/text() |'
                                     ' //a[@class="icMQ_ _205Zx f-test-link-FINPAY _25-u7"]/text()').extract_first()

        yield JobparserItem(name=name_job, salary=salary_job, location=location_job,
                            link=position_link, company=company_job)