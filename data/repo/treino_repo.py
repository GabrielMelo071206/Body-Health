from typing import Optional, List
from data.models.treino_model import Treino
from data.repo.cliente_repo import criar_tabela_cliente, inserir_cliente
from data.repo.usuario_repo import criar_tabela_usuario
from data.sql.treino_sql import *
from data.util import get_connection
from data.repo.profissional_repo import criar_tabela_profissional, inserir_profissional
from datetime import date


def criar_tabela_treino() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de treino: {e}")
        return False

def inserir_treino(treino: Treino) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            treino.id_cliente,
            treino.id_profissional,
            treino.nome,
            treino.descricao,
            treino.data_inicio,
            treino.data_fim,
            treino.ativo,
            treino.especificacoes,
            treino.tipo_treino,
            treino.visibilidade
        ))
        return cursor.lastrowid

def alterar_treino(treino: Treino) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            treino.id_cliente,
            treino.id_profissional,
            treino.nome,
            treino.descricao,
            treino.data_inicio,
            treino.data_fim,
            treino.ativo,
            treino.especificacoes,
            treino.tipo_treino,
            treino.visibilidade,
            treino.id_treino
        ))
        return cursor.rowcount > 0

def excluir_treino(id_treino: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_treino,))
        return cursor.rowcount > 0

OBTER_TREINO_POR_ID_SQL = """
SELECT * FROM treino WHERE id_treino = ?
"""

def obter_treino_por_id(id_treino: int) -> Optional[Treino]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TREINO_POR_ID_SQL, (id_treino,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Treino(
            id_treino=row["id_treino"],
            id_cliente=row["id_cliente"],
            id_profissional=row["id_profissional"],
            nome=row["nome"],
            descricao=row["descricao"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"],
            ativo=bool(row["ativo"]),
            especificacoes=row["especificacoes"],
            tipo_treino=row["tipo_treino"],
            visibilidade=row["visibilidade"]
        )

def obter_treinos_por_cliente(id_cliente: int) -> List[Treino]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CLIENTE, (id_cliente,))
        rows = cursor.fetchall()
        return [
            Treino(
                id_treino=row["id_treino"],
                id_cliente=row["id_cliente"],
                id_profissional=row["id_profissional"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                ativo=bool(row["ativo"]),
                especificacoes=row["especificacoes"],
                tipo_treino=row["tipo_treino"],
                visibilidade=row["visibilidade"]
            )
            for row in rows
        ]

def obter_todos_treinos() -> List[Treino]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Treino(
                id_treino=row["id_treino"],
                id_cliente=row["id_cliente"],
                id_profissional=row["id_profissional"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                ativo=bool(row["ativo"]),
                especificacoes=row["especificacoes"],
                tipo_treino=row["tipo_treino"],
                visibilidade=row["visibilidade"]
            )
            for row in rows
        ]

def obter_treinos_por_profissional(id_profissional: int) -> List[Treino]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PROFISSIONAL, (id_profissional,))
        rows = cursor.fetchall()
        return [
            Treino(
                id_treino=row["id_treino"],
                id_cliente=row["id_cliente"],
                id_profissional=row["id_profissional"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                ativo=bool(row["ativo"]),
                especificacoes=row["especificacoes"],
                tipo_treino=row["tipo_treino"],
                visibilidade=row["visibilidade"]
            )
            for row in rows
        ]
