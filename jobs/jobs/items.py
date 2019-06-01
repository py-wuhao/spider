# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import re


class JobsItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip, lambda s: re.sub(r'\s', '', s))
    default_output_processor = TakeFirst()


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 岗位
    salary = scrapy.Field()  # 薪水
    work_year = scrapy.Field()  # 工作经验
    address = scrapy.Field()  # 地址
    experience = scrapy.Field()  # 学历
    publish_time = scrapy.Field()  # 发布时间
    job_info = scrapy.Field(output_processor=Join('\n'))  # 职位信息
    company_name = scrapy.Field()  # 公司
    job_url = scrapy.Field()
