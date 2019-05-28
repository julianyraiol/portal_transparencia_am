import scrapy
from scrapy.http import Request
import rows
import json

from pathlib import Path
from portal_transparencia_am.spiders import utils
from portal_transparencia_am.items import ResponsePortal

class ListaServidorSpider(scrapy.Spider):

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
							ano = '2018',
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
