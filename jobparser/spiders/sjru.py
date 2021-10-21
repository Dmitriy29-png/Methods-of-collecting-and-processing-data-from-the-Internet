import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    search = 'python'
    start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a[rel="next"]').attrib['href']
        vacancy_links = response.xpath('div._2rfUm _2hCDz _21a7u a.icMQ_ _6AfZ9::attr(href)').extract()

        for link in vacancy_links:
            url = response.urljoin(link)
            yield response.Request(url, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(selfself, response: HtmlResponse):
        name_job = response.css('h1[class="rFbjy _2dazi _2hCDz _1RQyC"]::text').getall()
        salary_job = response.css('//span[class="_2Wp8I _2rfUm _2hCDz"]::text').extract()
        location_job = response.css('div[class="f-test-address _3AQrx"]::text()').extract()
        position_link = response.url
        company_job = response.css('div[class="_3zucV i4NN6 _2Pv5x"]::text').extract_first()
        yield JobparserItem(name=name_job, salary=salary_job, location=location_job,
                            link=position_link, company=company_job)
