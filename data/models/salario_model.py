from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Salario:
    id_salario: int
    id_profissional: int
    mes_referencia: int
    ano_referencia: int
    total_visualizacoes: int
    visualizacoes_validas: int
    valor_por_visualizacao: float
    valor_total: float
    data_calculo: date
    status_pagamento: str
    data_pagamento: date
    observacoes: str
    ativo: bool