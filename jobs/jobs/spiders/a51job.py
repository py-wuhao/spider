# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from ..items import JobsItem, JobsItemLoader


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['jobs.51job.com', 'search.51job.com']
    start_urls = ['https://search.51job.com/list/180200,000000,0000,00,9,99,python,2,1.html']
    custom_settings = {
        "ITEM_PIPELINES": {
            'jobs.pipelines.Mysql_51Job_Pipeline': 300,
        },
    }

    def parse(self, response):
        detailed_urls = response.xpath('//div[@id="resultList"]/div[@class="el"]/p//a/@href').extract()
        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)
        for url in detailed_urls:
            yield scrapy.Request(url, callback=self.detailed_parse)

    def detailed_parse(self, response):
        job = JobsItemLoader(item=JobsItem(), response=response)
        job.add_xpath('name', '//h1/@title')
        job.add_xpath('salary', '//h1/following-sibling::strong[1]/text()')
        job.add_xpath('address', '//span[contains(text(),"上班地址")]/../text()')
        job.add_xpath('company_name', '//h1/following-sibling::p[1]/a[1]/@title')
        job.add_xpath('job_info', '//span[contains(text(),"职位信息")]/../following-sibling::div[1]//text()')
        job.add_xpath('work_year', '//h1/following-sibling::p[2]/text()[2]')
        job.add_xpath('experience', '//h1/following-sibling::p[2]/text()[3]')
        msg = response.xpath('//h1/following-sibling::p/text()').extract()
        for m in msg:
            if '发布' in m:
                job.add_value('publish_time', m)
                break

        job.add_value('job_url', response.url)
        yield job.load_item()
