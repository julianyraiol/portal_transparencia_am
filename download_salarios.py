#!/usr/bin/env python
# coding: utf-8

import requests
import os

path_root = 'results/'
os.mkdir(path_root)

years = ["2014", "2015", "2016", "2017", "2018", "2019"]
organizations =[
		 {"nome_orgao":"ADAF","id":"76"},
		 {"nome_orgao":"ADS","id":"445"},
		 {"nome_orgao":"ALFREDO DA MATA","id":"92"},
		 {"nome_orgao":"AMAZONPREV","id":"127"},
		 {"nome_orgao":"ARSAM","id":"93"},
		 {"nome_orgao":"CASA CIVIL DO GOVERNO","id":"77"},
		 {"nome_orgao":"CASA MILITAR","id":"94"},
		 {"nome_orgao":"CB-CIVIS","id":"95"},
		 {"nome_orgao":"CBMAM","id":"96"},
		 {"nome_orgao":"CETAM","id":"74"},
		 {"nome_orgao":"CGE","id":"75"},
		 {"nome_orgao":"CGL","id":"97"},
		 {"nome_orgao":"DETRAN","id":"98"},
		 {"nome_orgao":"ERGSP","id":"99"},
		 {"nome_orgao":"FAPEAM","id":"100"},
		 {"nome_orgao":"FCECON","id":"101"},
		 {"nome_orgao":"FEH","id":"86"},
		 {"nome_orgao":"FEI","id":"396"},
		 {"nome_orgao":"FHAJ","id":"102"},
		 {"nome_orgao":"FHEMOAM","id":"103"},
		 {"nome_orgao":"FMT-AM","id":"104"},
		 {"nome_orgao":"FUNDA\u00c7\u00c3O AMAZONPREV","id":"87"},
		 {"nome_orgao":"FUNDA\u00c7\u00c3O VILA OLIMPICA","id":"105"},
		 {"nome_orgao":"FUNTEC","id":"106"},
		 {"nome_orgao":"FVS","id":"17"},
		 {"nome_orgao":"IDAM","id":"107"},
		 {"nome_orgao":"IMPRENSA OFICIAL","id":"108"},
		 {"nome_orgao":"IPAAM","id":"109"},
		 {"nome_orgao":"IPEM-AM","id":"110"},
		 {"nome_orgao":"JUCEA","id":"111"},
		 {"nome_orgao":"OUVIDORIA GERAL","id":"112"},
		 {"nome_orgao":"PENSIONISTAS","id":"128"},
		 {"nome_orgao":"PGE","id":"80"},
		 {"nome_orgao":"PM-ATIVOS","id":"113"},
		 {"nome_orgao":"PM-CIVIS","id":"114"},
		 {"nome_orgao":"POLICIA CIVIL","id":"115"},
		 {"nome_orgao":"PRODAM","id":"136"},
		 {"nome_orgao":"SEAD","id":"90"},

         {"nome_orgao":"SEAD-PENSAO ESPECIAL I","id":"129"},
         {"nome_orgao":"SEAD-PENSAO ESPECIAL II","id":"133"},
         {"nome_orgao":"SEAD-PENS\u00c3O HANSENIANOS","id":"132"},
         {"nome_orgao":"SEAP","id":"73"},
         {"nome_orgao":"SEAS","id":"82"},
         {"nome_orgao":"SEC","id":"126"},
         {"nome_orgao":"SECOM","id":"72"},
         {"nome_orgao":"SEDUC","id":"91"},
         {"nome_orgao":"SEFAZ","id":"89"},
         {"nome_orgao":"SEIND","id":"22"},
         {"nome_orgao":"SEINFRA","id":"116"},
         {"nome_orgao":"SEJEL","id":"117"},
         {"nome_orgao":"SEJUSC","id":"84"},
         {"nome_orgao":"SEMA","id":"81"},
         {"nome_orgao":"SEPED","id":"118"},
         {"nome_orgao":"SEPLANCTI","id":"83"},
         {"nome_orgao":"SEPROR","id":"119"},
         {"nome_orgao":"SERGB","id":"79"},
         {"nome_orgao":"SERIRA","id":"397"},
         {"nome_orgao":"SETRAB","id":"120"},
         {"nome_orgao":"SNPH","id":"121"},
         {"nome_orgao":"SPF","id":"122"},
         {"nome_orgao":"SRMM","id":"71"},
         {"nome_orgao":"SSP","id":"123"},
         {"nome_orgao":"SUHAB","id":"124"},
         {"nome_orgao":"SUSAM","id":"88"},
         {"nome_orgao":"UEA","id":"125"},
         {"nome_orgao":"UGPE","id":"85"},
         {"nome_orgao":"VICE-GOVERNADORIA","id":"78"}] 

def make_request(year, org_id):
    
    route = 'get_meses_docs'    
    url = "http://www.transparencia.am.gov.br/wp-admin/admin-ajax.php"
    data = { 'action':route, 'ano':year, 'orgao_id':org_id}
    
    response = requests.post(url, data=data)
    
    return response.json()

for org in organizations:
    
    name_org = org["nome_orgao"]
    
    path_dir = path_root + name_org + '/'
    os.mkdir(path_dir)
    
    print('Acessando arquivos de {}'.format(name_org))
    
    for year in years:
        
        print(year)
        
        path_year = path_dir + year + '/'
        os.mkdir(path_year)
        os.mkdir(path_year + 'pdf')
        os.mkdir(path_year + 'csv')
        
        response = make_request(year, org['id'])
        
        for json in response:
            month = json['mes_descricao'].lower()

            for extention in json['arquivos']:    
                
                print(extention)
                
                ext_file = extention['extensao']
                path = ext_file[1:] + '/'
                
                print(extention['url'])
              
                r = requests.get(extention['url'], stream=True)
                file = path_year + path + month + ext_file
                
                with open(file, 'wb') as f:
                    f.write(r.content)
                
                if (os.path.exists(file)):
                    
                    print('O arquivo de {} foi baixado'.format(month))
                else:
                    print('Falha ao baixar {}'.format(month))
                    
    print("\n\n=======================================================================\n\n")

