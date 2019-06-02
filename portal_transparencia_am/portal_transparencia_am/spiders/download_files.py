import scrapy
from scrapy import signals
from scrapy.http import Request

import rows
import json
import pandas as pd
from glob import glob
from pathlib import Path

from portal_transparencia_am.spiders import utils
import portal_transparencia_am.settings as settings
from portal_transparencia_am.items import ResponsePortal

class DownloadFilesSpider(scrapy.Spider):

	name = 'portal'
	start_urls = 'http://www.transparencia.am.gov.br/wp-admin/admin-ajax.php'
	route = 'get_meses_docs'

	def start_requests(self):
		entities = utils.get_entity()
		years = utils.get_years()
		
		for entity in entities:
			for year in years:

				formdata = dict(
							action = self.route,
							ano = str(2018),
							orgao_id = str(entity.id)
				)

				yield scrapy.FormRequest(
							url = self.start_urls,
							formdata = formdata,
							callback = self.parse,
							meta = {'name':entity.nome_orgao}
				)

	def parse(self, response):
		files = json.loads(response.body_as_unicode())
		name = response.request.meta['name']

		for content in files:
			list_files = content['arquivos']
			yield ResponsePortal(
				name = name,
				month = content['mes_descricao'],
				pdf = list_files.pop(0),
				csv = list_files.pop() if list_files else None
			)

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(DownloadFilesSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider
	
	def spider_closed(self, spider):
		path = settings.FILES_STORE + '/*/csv/*.csv'
		csv_list = glob(path)
		
		if csv_list:
			portal_csv = pd.concat([self.rows_to_csv(csv_name) for csv_name in csv_list])
			drop_columns = [column for column in portal_csv.columns if ("field" in column) or ("portal" in column) or ("Unnamed" in column)]
			portal_csv.drop(drop_columns, axis=1, inplace=True)
			
			portal_csv.to_csv('portal.csv')

			spider.logger.info('Spider closed: %s', portal_csv)

	def rows_to_csv(self, name):

		table = rows.import_from_csv(name, encoding='latin-1') 
		data_dict = {field_name: table[field_name] for field_name in table.field_names}
		df = pd.DataFrame.from_dict(data_dict)

		return df