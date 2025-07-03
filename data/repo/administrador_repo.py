from typing import Optional
from data.models.usuario_model import *
from data.models.administrador_model import *
from data.sql.administrador_sql import *
from data.models.usuario_model import Usuario
from data.repo import usuario_repo
from data.util import get_connection

def criar_tabela_administrador() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

def inserir_administrador(administrador: Administrador) -> Optional[int]:
    id_administrador = usuario_repo.inserir_usuario(administrador)
    if id_administrador is None:
        return None
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (id_administrador, administrador.master))
        return id_administrador

def alterar_administrador(administrador: Administrador) -> bool:
    if not usuario_repo.alterar_usuario(administrador):
        return False
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (administrador.id, administrador.master))
        return cursor.rowcount > 0

def excluir_administrador(id: int) -> bool:
    if not usuario_repo.excluir_usuario(id):
        return False
    return True

def obter_administrador_por_id(id: int) -> Optional[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Administrador(
            id=row["id_administrador"],
            master=row["master"],
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            data_nascimento=row["data_nascimento"],
            sexo=row["sexo"],
            tipo_usuario=row["tipo_usuario"]
        )



def obter_todos_administrador() -> list[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Administrador(
                id=row["id_administrador"],
                master=row["master"],
                nome=row["nome"],
                email=row["email"],
                senha_hash=row["senha_hash"],
                data_nascimento=row["data_nascimento"],
                sexo=row["sexo"],
                tipo_usuario=row["tipo_usuario"]
            )
            for row in rows
        ]
