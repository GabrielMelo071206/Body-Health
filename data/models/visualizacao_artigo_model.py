from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class VisualizacaoArtigo:
    id_visualizacao: int
    id_artigo: int       
    id_usuario: int      
    Data_visualizacao: date
    mes_referencia: int
    ano_referencia: int
    Ativo: bool