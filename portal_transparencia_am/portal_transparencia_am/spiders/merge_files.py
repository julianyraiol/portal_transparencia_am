import scrapy
from scrapy import signals
from scrapy.http import Request

import io
import rows
import json
import pandas as pd
from glob import glob
from pathlib import Path
import csv
from portal_transparencia_am import pipelines

from portal_transparencia_am.spiders import utils
import portal_transparencia_am.settings as settings
from portal_transparencia_am.items import ResponsePortal

class MergeFilesSpider(scrapy.Spider):

	name = 'merge_files'

	def __init__(self):
		self.start_urls = glob(settings.FILES_STORE + '/*/csv/*.csv')

	def start_requests(self):
		for csv_name in self.start_urls:
			path = "file://" + str(Path(csv_name).absolute())
			yield Request(url=path, callback=self.parse, meta={"name":csv_name})

	def parse(self, response):
		name = response.request.meta["name"]
		table = rows.import_from_csv(name, encoding='latin-1')
		data_dict = {field_name: table[field_name] for field_name in table.field_names}
		df = pd.DataFrame.from_dict(data_dict)

		yield df.to_dict('records')[0]
