# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymysql.cursors
import hashlib


class Mysql_51Job_Pipeline(object):
    jobs_list = []
    experiences = ('初中及以下', '高中', '中技', '中专', '大专', '本科', '硕士', '博士')

    def open_spider(self, spider):
        self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="123456", db="jobs", charset="utf8")
        self.cursor = self.conn.cursor()

    def bulk_update(self, bulk_data):
        try:
            sql = "replace into job(hash_url,job_url,name,max_salary,min_salary,settlement,address,company_name,job_info," \
                  "work_year,experience,publish_time) values(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s)"
            self.cursor.executemany(sql, bulk_data)
            self.conn.commit()
        except:
            self.conn.rollback()

    @staticmethod
    def process_salary(salary):
        num = salary.split('/')[0].split('-')
        settlement = salary.split('/')[1]
        if len(num) == 1:
            if num[0][-1] == '元':
                return int(num[0][0:-1]), int(num[0][0:-1]), settlement

        min_num = float(num[0])
        max_num = float(num[1][0:-1])
        unit = 1
        if num[1][-1] == '万':
            unit = 10000
        elif num[1][-1] == '千':
            unit = 1000

        min_num = int(min_num * unit)
        max_num = int(max_num * unit)
        return min_num, max_num, settlement

    @staticmethod
    def hash_url(url):
        md5 = hashlib.md5()
        md5.update(url.encode())
        return md5.hexdigest()

    @staticmethod
    def process_p_time(t):
        year = time.strftime('%Y', time.localtime())

    def process_item(self, item, spider):
        if item['experience'] not in self.experiences:
            item['experience'] = '无要求'
        try:
            min_salary, max_salary, settlement = self.process_salary(item['salary'])
        except KeyError:
            min_salary, max_salary, settlement = 0, 0, '月'
        if not item.get('address'):
            item['address'] = '武汉'
        hash_url = self.hash_url(item['job_url'])
        item['publish_time'] = time.strftime('%Y-', time.localtime()) + item['publish_time'][0:-2]
        self.jobs_list.append((
            hash_url,
            item['job_url'],
            item['name'],
            max_salary,
            min_salary,
            settlement,
            item['address'],
            item['company_name'],
            item['job_info'],
            item['work_year'],
            item['experience'],
            item['publish_time'],
        ))
        if len(self.jobs_list) >= 54:
            self.bulk_update(self.jobs_list)
            # 清空缓冲区
            self.jobs_list.clear()
        return item

    def close_spider(self, spider):
        self.bulk_update(self.jobs_list)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
