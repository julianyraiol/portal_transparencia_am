#!/usr/bin/env python
import rows
from pathlib import Path


from collections import OrderedDict

import rows

class BrazilianMoneyField(rows.fields.DecimalField):
    """Parser for money in Brazilian notation

    "1.234,56" -> Decimal("1234.56")
    """

    @classmethod
    def deserialize(cls, value):
        value = (value or "").replace(".", "").replace(",", ".")
        return super().deserialize(value)


PDF_FIELD_TYPES = OrderedDict(
    [
        ("nome_lotacao", rows.fields.TextField),
        ("cargo", rows.fields.TextField),
        ("funcao_vinculo", rows.fields.TextField),
        ("remuneracao_legal_total", BrazilianMoneyField),
        ("desc_teto", BrazilianMoneyField),
        ("remuneracao_legal_devida", BrazilianMoneyField),
        ("descontos_legais", BrazilianMoneyField),
        ("liquido_disponivel", BrazilianMoneyField),
    ]
)


def convert_row(row):
    """Generate the final dict based on data from the PDF"""

    row = row._asdict()
    nome_lotacao = row.pop("nome_lotacao").splitlines()
    funcao_vinculo = row.pop("funcao_vinculo").splitlines()
    row["funcao"] = funcao_vinculo[0]
    row["lotacao"] = " ".join(nome_lotacao[1:])
    row["nome"] = nome_lotacao[0]
    row["vinculo"] = " ".join(funcao_vinculo[1:])

    return row


def parse_file(filename):
    """Parse Amazonas' PDF file containing state employee information"""

    total_pages = rows.plugins.pdf.number_of_pages(filename)
    result = []
    for page in range(1, total_pages + 1):
        table = rows.import_from_pdf(
            filename,
            page_numbers=(page,),
            starts_after="NOME",
            fields=PDF_FIELD_TYPES,
            skip_header=True,
        )
        for row in table:
            result.append(convert_row(row))

    return rows.import_from_dicts(result)


def get_entity():
    current_path = Path(__file__).parent
    csv = rows.import_from_csv(str(current_path / "data" / "entities.csv"))
    return csv


def get_years():
    return ['2014', '2015', '2016', '2017', '2018', '2019']

