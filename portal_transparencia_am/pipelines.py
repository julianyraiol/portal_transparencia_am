# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import csv
from functools import wraps
from pathlib import Path
import pandas as pd

import scrapy
from scrapy.exceptions import DropItem
from scrapy.http import Request

import portal_transparencia_am.settings as settings

def check_spider_pipeline(process_item_method):
    @wraps(process_item_method)
    def wrapper(self, item, spider):
        try:
            if self.__class__ in spider.pipeline:
                return process_item_method(self, item, spider)
        except AttributeError:
            pass
        return item
    return wrapper


class FilePipeline(object):

    def open_spider(self, spider):
        self.current_path = Path(settings.FILES_STORE)
        if not self.current_path.exists():
            self.current_path.mkdir()

    @check_spider_pipeline
    def process_item(self, item, spider):

        # Request pdf file
        self.download_file(item, spider, type_request='pdf')

        # Request csv file
        if item.get('csv'):
            self.download_file(item, spider, type_request='csv')

        return item

    def download_file(self, item, spider, type_request):
        try:
            request = Request(item[type_request]['url'])
            dfd = spider.crawler.engine.download(request, spider)
            dfd.addBoth(self.save_file, item, type_request)

            message = 'Saving {} file'.format(type_request)
            print(message)
            return True
        except:
            message = 'Failed to save {}'.format(type_request)
            raise DropItem(message)

    def save_file(self, response, item, type_request):

        name_folder = item.get('name')
        path = self.current_path / name_folder

        if not path.exists():
            path.mkdir()

        filepath = path / type_request
        if not filepath.exists():
            filepath.mkdir()

        url = item[type_request]['url']
        name = url.split('/')[-1]

        filename = filepath / name
        with filename.open('wb') as current_file:
            current_file.write(response.body)

        return filename

class RequestsPipeline(object):

    def open_spider(self, spider):
        self.response = csv.writer(open('requests.csv', 'w'))

    def close_spider(self, spider):
        self.response.close()

    @check_spider_pipeline
    def process_item(self, item, spider):

        # Save pdf url
        self.save_requests(item, type_request='pdf')

        # Save pdf url
        if item.get('csv'):
            self.save_requests(item, type_request='csv')

        return item

    def save_requests(self, item, type_request):
        url = item[type_request]['url']
        name = url.split('/')[-1]
        self.response.writerow([(item[type_request]['url']), name])
