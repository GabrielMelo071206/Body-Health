from typing import Optional
from datetime import date
from data.models.salario_model import Salario
from data.sql import salario_sql
from data.util import get_connection


def criar_tabela_salario() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(salario_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela salario: {e}")
        return False


def inserir_salario(salario: Salario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(salario_sql.INSERIR, (
            salario.id_profissional,
            salario.mes_referencia,
            salario.ano_referencia,
            salario.total_visualizacoes,
            salario.visualizacoes_validas,
            salario.valor_por_visualizacao,
            salario.valor_total,
            salario.data_calculo,
            salario.status_pagamento,
            salario.data_pagamento,
            salario.observacoes,
            salario.ativo
        ))
        return cursor.lastrowid


def alterar_salario(salario: Salario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(salario_sql.ALTERAR, (
            salario.mes_referencia,
            salario.ano_referencia,
            salario.total_visualizacoes,
            salario.visualizacoes_validas,
            salario.valor_por_visualizacao,
            salario.valor_total,
            salario.data_calculo,
            salario.status_pagamento,
            salario.data_pagamento,
            salario.observacoes,
            salario.ativo,
            salario.id_salario
        ))
        return cursor.rowcount > 0


def excluir_salario(id_salario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(salario_sql.EXCLUIR, (id_salario,))
        return cursor.rowcount > 0


def obter_salario_por_id(id_salario: int) -> Optional[Salario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(salario_sql.OBTER_POR_ID, (id_salario,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Salario(
            id_salario=row["id_salario"],
            id_profissional=row["id_profissional"],
            mes_referencia=row["mes_referencia"],
            ano_referencia=row["ano_referencia"],
            total_visualizacoes=row["total_visualizacoes"],
            visualizacoes_validas=row["visualizacoes_validas"],
            valor_por_visualizacao=row["valor_por_visualizacao"],
            valor_total=row["valor_total"],
            data_calculo=row["data_calculo"],
            status_pagamento=row["status_pagamento"],
            data_pagamento=row["data_pagamento"],
            observacoes=row["observacoes"],
            ativo=row["ativo"]
        )


def obter_todos_salarios() -> list[Salario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(salario_sql.OBTER_TODOS)
        rows = cursor.fetchall()
        return [Salario(
            id_salario=row["id_salario"],
            id_profissional=row["id_profissional"],
            mes_referencia=row["mes_referencia"],
            ano_referencia=row["ano_referencia"],
            total_visualizacoes=row["total_visualizacoes"],
            visualizacoes_validas=row["visualizacoes_validas"],
            valor_por_visualizacao=row["valor_por_visualizacao"],
            valor_total=row["valor_total"],
            data_calculo=row["data_calculo"],
            status_pagamento=row["status_pagamento"],
            data_pagamento=row["data_pagamento"],
            observacoes=row["observacoes"],
            ativo=row["ativo"]
        ) for row in rows]


def obter_salario_por_profissional_e_periodo(id_profissional: int, mes: int, ano: int) -> Optional[Salario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(salario_sql.OBTER_POR_PROFISSIONAL_E_PERIODO, (id_profissional, mes, ano))
        row = cursor.fetchone()
        if row is None:
            return None
        return Salario(
            id_salario=row["id_salario"],
            id_profissional=row["id_profissional"],
            mes_referencia=row["mes_referencia"],
            ano_referencia=row["ano_referencia"],
            total_visualizacoes=row["total_visualizacoes"],
            visualizacoes_validas=row["visualizacoes_validas"],
            valor_por_visualizacao=row["valor_por_visualizacao"],
            valor_total=row["valor_total"],
            data_calculo=row["data_calculo"],
            status_pagamento=row["status_pagamento"],
            data_pagamento=row["data_pagamento"],
            observacoes=row["observacoes"],
            ativo=row["ativo"]
        )
