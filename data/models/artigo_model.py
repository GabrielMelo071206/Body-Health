from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Artigo:
    id_artigo: int
    id_profissional: int
    titulo: str
    conteudo: str
    data_publicacao: date
    visualizacoes: int
    ativo: bool
    avaliacao: float