from dataclasses import dataclass
from datetime import date

@dataclass
class Plano:
    id_plano: int
    id_cliente: int
    tipo_plano: str
    valor: float
    duracao: int
    data_inicio: date
    data_fim: date
    ativo: bool