from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Assinaturas:
    id_assinatura: int
    id_cliente: int # Fk
    id_plano: int   # Fk
    data_inicio: date
    data_fim: date
    status: str
    valor_pago: float
    ativo: bool