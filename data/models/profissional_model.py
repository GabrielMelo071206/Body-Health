from dataclasses import dataclass
from data.models.usuario_model import Usuario

@dataclass
class Profissional(Usuario):
    ativo: bool
    ano_formacao: int
    registro_profissional: str
