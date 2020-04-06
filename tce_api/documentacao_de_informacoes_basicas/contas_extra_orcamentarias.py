from tce_api.base import Base
from itertools import repeat
from datetime import datetime
from models.conta_extra_orcamentaria import ContaExtraOrcamentaria
from models.municipio import Municipio

class ContasExtraOrcamentarias(Base):
    def __init__(self):
        super().__init__()
        self.initialize_variables_by_method('contas_extra_orcamentarias')

    def execute(self):
        try:
            for municipio in Municipio.by_id_range(self.municipio_id):
                self.municipio_id = municipio.id
                contas_extra_orcamentarias = []
                for year in range(self.year, datetime.now().year):
                    self.year = year
                    response = self.request_tce_api(self.url_with_params(municipio.codigo, year))
                    for params in response.json()['rsp']['_content']:
                        contas_extra_orcamentarias.append(ContaExtraOrcamentaria(params))
                        ContaExtraOrcamentaria.save_multiple(contas_extra_orcamentarias)
            self.save_progress('', True)
        except Exception as e:
            self.save_progress(e, False)

    def url_with_params(self, codigo, year):
        return ('?codigo_municipio=' + codigo + '&exercicio_orcamento=' + str(year))