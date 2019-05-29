# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from pathlib import Path
import scrapy

from scrapy.http import Request

class PdfPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):

        try:
            request = Request(item['pdf']['url'])
            dfd = spider.crawler.engine.download(request, spider)
            dfd.addBoth(self.save_pdf_file, item)
        except:
            pass

        return item

    def save_pdf_file(self, response, item):
        filename = 'teste.pdf'
        with open(filename, 'wb') as current_file:
            current_file.write(response.body)

        return filename


class CsvPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        url = item['csv']
        if url:
            request = Request(url['url'])
            dfd = spider.crawler.engine.download(request, spider)
            dfd.addBoth(self.save_csv_file, item)
            return dfd

    def save_csv_file(self, response, item):
        filename = 'teste.csv'
        with open(filename, 'wb') as current_file:
            current_file.write(response.body)

        return filename
