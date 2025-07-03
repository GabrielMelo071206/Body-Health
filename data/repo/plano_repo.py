from typing import Optional
from datetime import date
from data.models.plano_model import Plano
from data.sql.plano_sql import *
from data.util import get_connection



def criar_tabela_plano() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False


def inserir_plano(plano: Plano) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            plano.id_cliente,
            plano.tipo_plano,
            plano.valor,
            plano.duracao,
            plano.data_inicio.isoformat(),
            plano.data_fim.isoformat(),
            plano.ativo
        ))
        return cursor.lastrowid


def alterar_plano(plano: Plano) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            plano.id_cliente,
            plano.tipo_plano,
            plano.valor,
            plano.duracao,
            plano.data_inicio.isoformat(),
            plano.data_fim.isoformat(),
            plano.ativo,
            plano.id_plano
        ))
        return cursor.rowcount > 0


def excluir_plano(id_plano: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_plano,))
        return cursor.rowcount > 0


def obter_plano_por_id(id_plano: int) -> Optional[Plano]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_plano,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Plano(
            id_plano=row["id_plano"],
            id_cliente=row["id_cliente"],
            tipo_plano=row["tipo_plano"],
            valor=row["valor"],
            duracao=row["duracao"],
            data_inicio=date.fromisoformat(row["data_inicio"]),
            data_fim=date.fromisoformat(row["data_fim"]),
            ativo=bool(row["ativo"])
        )


def obter_todos_planos() -> list[Plano]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Plano(
                id_plano=row["id_plano"],
                id_cliente=row["id_cliente"],
                tipo_plano=row["tipo_plano"],
                valor=row["valor"],
                duracao=row["duracao"],
                data_inicio=date.fromisoformat(row["data_inicio"]),
                data_fim=date.fromisoformat(row["data_fim"]),
                ativo=bool(row["ativo"])
            )
            for row in rows
        ]


def obter_planos_por_cliente(id_cliente: int) -> list[Plano]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CLIENTE, (id_cliente,))
        rows = cursor.fetchall()
        return [
            Plano(
                id_plano=row["id_plano"],
                id_cliente=row["id_cliente"],
                tipo_plano=row["tipo_plano"],
                valor=row["valor"],
                duracao=row["duracao"],
                data_inicio=date.fromisoformat(row["data_inicio"]),
                data_fim=date.fromisoformat(row["data_fim"]),
                ativo=bool(row["ativo"])
            )
            for row in rows
        ]


def obter_planos_ativos() -> list[Plano]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PLANOS_ATIVOS)
        rows = cursor.fetchall()
        return [
            Plano(
                id_plano=row["id_plano"],
                id_cliente=row["id_cliente"],
                tipo_plano=row["tipo_plano"],
                valor=row["valor"],
                duracao=row["duracao"],
                data_inicio=date.fromisoformat(row["data_inicio"]),
                data_fim=date.fromisoformat(row["data_fim"]),
                ativo=bool(row["ativo"])
            )
            for row in rows
        ]


def desativar_plano(id_plano: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DESATIVAR_PLANO, (id_plano,))
        return cursor.rowcount > 0


def ativar_plano(id_plano: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATIVAR_PLANO, (id_plano,))
        return cursor.rowcount > 0