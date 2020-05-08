# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import time
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Compose, TakeFirst, Identity, Join
from datetime import datetime


class PracticespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def get_newstime(value):
    regex_obj = re.match('.*?(\d.*)', value)
    if regex_obj:
        return regex_obj.group(1)
    else:
        return "1970-01-01"


def get_lowest_salary(salary):
    salary_li = re.findall('\d+', salary, re.S)
    if salary_li:
        return int(salary_li[0]) * 1000
    return 0


def get_highest_salary(salary):
    salary_li = re.findall('\d+', salary, re.S)
    if salary_li:
        return int(salary_li[1]) * 1000
    return 0


def get_job_city(value):
    return value.strip('/').strip()


def get_degree_need(degree):
    return degree.strip('/').strip()


def get_publish_time(value):
    time1 = re.match('.*?(\d+:\d+).*?', value)
    time2 = re.match('.*?(\d+-\d+-\d+).*?', value)
    time3 = re.match('.*?(\d+)天前.*?', value)
    time4 = re.match('.*?(\d+)小时前.*?', value)
    time5 = re.match('.*?(\d+)分钟前.*?', value)
    now = datetime.now()
    if time1:
        return time.strftime("%Y-%m-%d", time.localtime()) + " " + time1.group(1) + ":00"
    elif time2:
        return time2.group(1) + " 00:00:00"
    elif time3:
        return datetime(now.year, now.month, now.day - int(time3.group(1)), now.hour, now.minute)
    elif time4:
        return datetime(now.year, now.month, now.day, now.hour - int(time4.group(1)), now.minute)
    elif time5:
        return datetime(now.year, now.month, now.day, now.hour, now.minute - int(time5.group(1)))


def get_job_addr(value):
    return value.replace(",查看地图", "")


def clear_params(value):
    if "?" in value:
        return value.split("?")[0]
    return value


class LagouJobItemLoader(ItemLoader):
    # 自定义 itemloader
    default_output_processor = TakeFirst()


# lagou_job_tab
class LagouJobItem(scrapy.Item):
    # 职位名称
    title = scrapy.Field()
    # 职位详情页 url
    url = scrapy.Field(input_processor=MapCompose(clear_params))
    # 职位详情页 url，经过 md5 加密之后的值
    url_object_id = scrapy.Field()
    # 薪水
    lowest_salary = scrapy.Field(input_processor=MapCompose(get_lowest_salary))
    highest_salary = scrapy.Field(input_processor=MapCompose(get_highest_salary))
    # 工作城市
    job_city = scrapy.Field(input_processor=MapCompose(get_job_city))
    # 工作年限
    work_years = scrapy.Field()
    # 学历要求
    degree_need = scrapy.Field(input_processor=MapCompose(get_degree_need))
    # 职位类型
    job_type = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field(input_processor=MapCompose(get_publish_time))
    # 职位福利
    job_advantage = scrapy.Field()
    # 职位需求内容
    job_desc = scrapy.Field()
    # 工作地点
    job_addr = scrapy.Field(input_processor=Join(separator=","), output_processor=MapCompose(get_job_addr))
    # 公司名称
    company_name = scrapy.Field()
    # 公司url
    company_url = scrapy.Field()
    # 标签
    tags = scrapy.Field(input_processor=Join(separator=","))
    # 爬取时间
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    insert into lagou_job_tab(title, url, url_object_id, lowest_salary, highest_salary, job_city, 
                    work_years, degree_need, job_type, publish_time, job_advantage, job_desc,job_addr,company_name,
                    company_url,tags,crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON 
                    DUPLICATE KEY UPDATE lowest_salary=VALUES(lowest_salary),highest_salary=VALUES(highest_salary),
                    work_years=VALUES(work_years),degree_need=VALUES(degree_need),publish_time=VALUES(publish_time),
                    job_advantage=VALUES(job_advantage),job_desc=VALUES(job_desc);
        """
        params = list()
        params.append(self.get("title", ""))
        params.append(self.get("url"))
        params.append(self.get("url_object_id"))
        params.append(self.get("lowest_salary"))
        params.append(self.get("highest_salary"))
        params.append(self.get("job_city"))
        params.append(self.get("work_years"))
        params.append(self.get("degree_need"))
        params.append(self.get("job_type"))
        params.append(self.get("publish_time"))
        params.append(self.get("job_advantage"))
        params.append(self.get("job_desc"))
        params.append(self.get("job_addr"))
        params.append(self.get("company_name"))
        params.append(self.get("company_url"))
        params.append(self.get("tags"))
        params.append(self.get("crawl_time"))
        return insert_sql, params
