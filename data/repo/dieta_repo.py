from typing import Optional, List
from data.models.dieta_model import Dieta
from data.sql.dieta_sql import *
from data.util import get_connection

def criar_tabela_dieta() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de dieta: {e}")
        return False

def inserir_dieta(dieta: Dieta) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            dieta.id_cliente,
            dieta.id_profissional,
            dieta.nome,
            dieta.descricao,
            dieta.data_inicio,
            dieta.data_fim,
            dieta.ativo,
            dieta.especificacoes,
            dieta.tipo_dieta
        ))
        return cursor.lastrowid

def alterar_dieta(dieta: Dieta) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            dieta.id_cliente,
            dieta.id_profissional,
            dieta.nome,
            dieta.descricao,
            dieta.data_inicio,
            dieta.data_fim,
            dieta.ativo,
            dieta.especificacoes,
            dieta.tipo_dieta,
            dieta.id_dieta
        ))
        return cursor.rowcount > 0

def excluir_dieta(id_dieta: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_dieta,))
        return cursor.rowcount > 0

from data.models.dieta_model import Dieta
from data.util import get_connection  # ou seu método para conexão
from typing import Optional

OBTER_DIETA_POR_ID_SQL = """
SELECT * FROM dieta WHERE id_dieta = ?
"""

def obter_dieta_por_id(id_dieta: int) -> Optional[Dieta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_DIETA_POR_ID_SQL, (id_dieta,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Dieta(
            id_dieta=row["id_dieta"],
            id_cliente=row["id_cliente"],
            id_profissional=row["id_profissional"],
            nome=row["nome"],
            descricao=row["descricao"],
            data_inicio=row["data_inicio"],
            data_fim=row["data_fim"],
            ativo=bool(row["ativo"]),
            especificacoes=row["especificacoes"],
            tipo_dieta=row["tipo_dieta"]
        )

def obter_dietas_por_cliente(id_cliente: int) -> List[Dieta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CLIENTE, (id_cliente,))
        rows = cursor.fetchall()
        return [
            Dieta(
                id_dieta=row["id_dieta"],
                id_cliente=row["id_cliente"],
                id_profissional=row["id_profissional"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                ativo=row["ativo"],
                especificacoes=row["especificacoes"],
                tipo_dieta=row["tipo_dieta"]
            )
            for row in rows
        ]

def obter_todas_dietas() -> List[Dieta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Dieta(
                id_dieta=row["id_dieta"],
                id_cliente=row["id_cliente"],
                id_profissional=row["id_profissional"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                ativo=row["ativo"],
                especificacoes=row["especificacoes"],
                tipo_dieta=row["tipo_dieta"]
            )
            for row in rows
        ]

def obter_dietas_por_profissional(id_profissional: int) -> List[Dieta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PROFISSIONAL, (id_profissional,))
        rows = cursor.fetchall()
        return [
            Dieta(
                id_dieta=row["id_dieta"],
                id_cliente=row["id_cliente"],
                id_profissional=row["id_profissional"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_inicio=row["data_inicio"],
                data_fim=row["data_fim"],
                ativo=row["ativo"],
                especificacoes=row["especificacoes"],
                tipo_dieta=row["tipo_dieta"]
            )
            for row in rows
        ]
