from dataclasses import dataclass
from datetime import date

@dataclass
class Treino:
    id_treino: int #PK
    id_cliente: int #FK Cliente
    id_profissional: int #FK Profissional
    nome: str
    descricao: str 
    data_inicio: date
    data_fim: date
    ativo: bool
    especificacoes: str 
    tipo_treino: str # Ex: Low Carb, Cetogênica, Mediterrânea, etc
    visibilidade: str # Ex: Publico, Privado, Profissional