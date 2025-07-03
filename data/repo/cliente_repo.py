from typing import Optional
from data.repo import usuario_repo
from data.models.cliente_model import Cliente
from data.sql.cliente_sql import *
from data.models.usuario_model import *
from data.util import get_connection


def criar_tabela_cliente() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False


def inserir_cliente(cliente: Cliente) -> Optional[int]:
    id_cliente = usuario_repo.inserir_usuario(cliente)
    if id_cliente is None:
        return None
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (cliente.tipo_conta, id_cliente))
        return id_cliente


def alterar_cliente(cliente: Cliente) -> bool:
    if not usuario_repo.alterar_usuario(cliente):
        return False
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (cliente.tipo_conta, cliente.id))
        return cursor.rowcount > 0


def excluir_cliente(id: int) -> bool:
    if not usuario_repo.excluir_usuario(id):
        return False
    return True


def obter_cliente_por_id(id: int) -> Optional[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Cliente(
            id=row["id_cliente"],
            tipo_conta=row["tipo_conta"],
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            data_nascimento=row["data_nascimento"],
            sexo=row["sexo"],
            tipo_usuario=row["tipo_usuario"]
        )

def obter_todos_clientes() -> list[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Cliente(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha_hash=row["senha_hash"],
                data_nascimento=row["data_nascimento"],
                sexo=row["sexo"],
                tipo_usuario=row["tipo_usuario"],
                tipo_conta=row["tipo_conta"]
            )
            for row in rows
        ]
