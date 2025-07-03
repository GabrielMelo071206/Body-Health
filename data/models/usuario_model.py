from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha_hash: str
    data_nascimento:  str
    sexo: str
    tipo_usuario: str
