from dataclasses import dataclass
from datetime import date

@dataclass
class Dieta:
    id_dieta: int #PK
    id_cliente: int #FK Cliente
    id_profissional: int #FK Profissional
    nome: str
    descricao: str 
    data_inicio: date
    data_fim: date
    ativo: bool
    especificacoes: str 
    tipo_dieta: str # Ex: Low Carb, Cetogênica, Mediterrânea, etc