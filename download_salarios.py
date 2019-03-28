#!/usr/bin/env python
# coding: utf-8

import requests
import rows
import os

path_root = 'results/'
os.mkdir(path_root)

years = ["2014", "2015", "2016", "2017", "2018", "2019"]

def make_request(year, org_id):

    route = 'get_meses_docs'
    url = "http://www.transparencia.am.gov.br/wp-admin/admin-ajax.php"
    data = { 'action':route, 'ano':year, 'orgao_id':org_id}

    response = requests.post(url, data=data)

    return response.json()

organizations = rows.import_from_csv("organizations.csv")
for org in organizations:

    name_org = org.nome_orgao

    path_dir = path_root + name_org + '/'
    os.mkdir(path_dir)

    print('Acessando arquivos de {}'.format(name_org))

    for year in years:

        print(year)

        path_year = path_dir + year + '/'
        os.mkdir(path_year)
        os.mkdir(path_year + 'pdf')
        os.mkdir(path_year + 'csv')

        response = make_request(year, org.id)

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
