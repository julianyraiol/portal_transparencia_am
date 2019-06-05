# Crawler dos arquivos referentes ao Portal da Transparência do Amazonas

Baixa os arquivos referentes aos salários dos funcionários do governo do estado do Amazonas nos formatos CSV e PDF.

Fonte: [Portal da Transparência do Estado do Amazonas](http://www.transparencia.am.gov.br/pessoal/)

### Instalação
Este projeto requer **Python 3.+** e outras bibliotecas. Utilize o arquivo **requirements.txt** para instalar as dependências

```bash
$ git clone https://github.com/julianyraiol/portal_transparencia_am.git
$ cd portal_transparencia_am
$ pip install -r requirements.txt
```

### Executar

No seu terminal, já tendo executado o arquivo de instalação, execute o seguinte comando:

```bash
$ scrapy crawl download_files
```


Para transformar todos os arquivos em um único csv, basta executar o seguinte comando:

```bash
$ scrapy crawl merge_files -o <NOME_ARQUIVO>.csv
```
