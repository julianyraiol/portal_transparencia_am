# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from pathlib import Path
import scrapy
import csv

from scrapy.exceptions import DropItem
from scrapy.http import Request

class FilePipeline(object):

    def open_spider(self, spider):
        self.file = csv.writer(open('portal.csv', 'w'))

        self.current_path = Path('results')
        if not self.current_path.exists():
            self.current_path.mkdir()

    def close_spider(self, spider):
        self.file.close()

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
            self.file.writerow([response.body])

        return filename

class RequestsPipeline(object):

    def open_spider(self, spider):
        self.file = csv.writer(open('requests.csv', 'w'))

    def close_spider(self, spider):
        self.file.close()

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
        self.file.writerow([(item[type_request]['url']), name])
