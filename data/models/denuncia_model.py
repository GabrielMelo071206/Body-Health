from dataclasses import dataclass
from typing import Optional

@dataclass
class Denuncia:
    id_denuncia: int
    id_denunciante: int  
    id_denunciado: int
    tipo_denunciante: str
    tipo_denunciado: str
    motivo: str
    descricao: str
    data_denuncia: str
    status: str
    id_admin_avaliador: int
    data_avaliacao: str
    observacoes_admin: str
    ativo: bool