# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from pathlib import Path
import scrapy

from scrapy.exceptions import DropItem
from scrapy.http import Request

class FilePipeline(object):

    def process_item(self, item, spider):

        # Request pdf file
        self.download_file(item, spider, type='pdf')

        # Request csv file
        if item.get('csv'):
            self.download_file(item, spider, type='csv')

        return item

    def download_file(self, item, spider, type):

        try:
            request = Request(item[type]['url'])
            dfd = spider.crawler.engine.download(request, spider)
            dfd.addBoth(self.save_file, item, type)

            message = 'Saving {} file'.format(type)
            print(message)
            return True
        except e:
            message = 'Failed to save {}'.format(type)
            raise DropItem(message)

    def save_file(self, response, item, type):

        url = item[type]['url']
        filename = url.split('/')[-1]
        with open(filename, 'wb') as current_file:
            current_file.write(response.body)

        return filename
