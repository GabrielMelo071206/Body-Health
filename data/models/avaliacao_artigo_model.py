from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class AvaliacaoArtigo:
    id_avaliacao: int #PK
    id_artigo: int    #FK
    id_usuario: int     #FK
    nota: float
    Data_avaliacao: date
    Ativo: bool