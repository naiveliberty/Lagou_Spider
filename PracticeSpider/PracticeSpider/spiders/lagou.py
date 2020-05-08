# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from PracticeSpider.items import LagouJobItem, LagouJobItemLoader
from PracticeSpider.utils.common import get_md5
from datetime import datetime



class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com']

    rules = (
        Rule(LinkExtractor(allow=('.*zhaopin/.*')), follow=True),
        Rule(LinkExtractor(allow=('gongsi/j\d+.html')), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_lagou', follow=True, ),
    )

    def parse_lagou(self, response):
        # 解析拉钩网职位内容
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_xpath('title', '//h1[@class="name"]/text()')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_xpath('lowest_salary', '//span[@class="salary"]/text()')
        item_loader.add_xpath('highest_salary', '//span[@class="salary"]/text()')
        item_loader.add_xpath('job_city', '//dd[@class="job_request"]/h3/span[2]/text()')
        item_loader.add_xpath('work_years', '//dd[@class="job_request"]/h3/span[3]/text()')
        item_loader.add_xpath('degree_need', '//dd[@class="job_request"]/h3/span[4]/text()')
        item_loader.add_xpath('job_type', '//dd[@class="job_request"]/h3/span[5]/text()')
        item_loader.add_xpath('tags', '//ul[@class="position-label clearfix"]/li/text()')
        item_loader.add_xpath('publish_time', '//*[@class="publish_time"]/text()')
        item_loader.add_xpath('job_advantage', '//dd[@class="job-advantage"]/p/text()')
        item_loader.add_xpath('job_desc', '//dd[@class="job_bt"]')
        item_loader.add_xpath('job_addr', '//div[@class="work_addr"]/a/text()')
        item_loader.add_xpath('company_name', '//dl[@class="job_company"]/dt/a/img/@alt')
        item_loader.add_xpath('company_url', '//dl[@class="job_company"]/dt/a/@href')
        item_loader.add_value('crawl_time', datetime.now())

        job_item = item_loader.load_item()
        if job_item.get("lowest_salary"):
            yield job_item
