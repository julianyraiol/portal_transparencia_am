import scrapy
from scrapy.http import Request
import rows
import json


from pathlib import Path
from portal_transparencia_am.spiders import utils

class PortalSpider(scrapy.Spider):

	name = 'generate-csv'

	def __init__(self):
		self.url = 'http://www.transparencia.am.gov.br/wp-admin/admin-ajax.php'
		
		self.route = 'get_meses_docs'

		self.current_path = Path('portal_amazonas')
		if not self.current_path.exists():
			self.current_path.mkdir()

	def start_requests(self):
		entities = utils.get_entity()
		years = utils.get_years()

		for entity in entities:
			for year in years:
				formdata = dict(action=self.route, ano=year,
									orgao_id=str(entity.id))
									
				yield scrapy.FormRequest(url=self.url, 
									formdata = formdata,
									callback=self.parse,
									meta={'name':entity.nome_orgao, 'year':year})
		
	def parse(self, response):
		content_files = json.loads(response.body_as_unicode()) 
		dir_name = response.request.meta['name']
		file_path = self.current_path / dir_name
		
		if not file_path.exists():
			file_path.mkdir()	

		for content in content_files:
			pdf_file = content['arquivos'][0]['url']
			url_name = pdf_file.split('/')[-1]		
			filename = file_path / url_name
			
			yield Request(
				url=pdf_file,
				callback=self.save_pdf,
				meta={'filename':filename}
			)

	def save_pdf(self, response):

		filename = response.request.meta['filename']
	
		self.logger.info('Saving %s', filename)
		
		with filename.open('wb') as current_file:
			current_file.write(response.body)

		yield {
			"download_file" : filename,
			"url": response.url
		}