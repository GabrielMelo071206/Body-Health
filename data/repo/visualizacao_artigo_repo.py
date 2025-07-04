from typing import Optional
from datetime import date
from data.models.visualizacao_artigo_model import VisualizacaoArtigo
from data.repo.artigo_repo import criar_tabela_artigo
from data.sql import visualizacao_artigo_sql
from data.util import get_connection


def criar_tabela_visualizacao_artigo() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(visualizacao_artigo_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela visualizacao_artigo: {e}")
        return False


def inserir_visualizacao_artigo(visualizacao: VisualizacaoArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(visualizacao_artigo_sql.INSERIR, (
            visualizacao.id_artigo,
            visualizacao.id_usuario,
            visualizacao.Data_visualizacao,
            visualizacao.mes_referencia,
            visualizacao.ano_referencia,
            int(visualizacao.Ativo)
        ))
        return cursor.lastrowid


def alterar_visualizacao_artigo(visualizacao: VisualizacaoArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(visualizacao_artigo_sql.ALTERAR, (
            visualizacao.Data_visualizacao,
            visualizacao.mes_referencia,
            visualizacao.ano_referencia,
            int(visualizacao.Ativo),
            visualizacao.id_visualizacao
        ))
        conn.commit()
        return cursor.rowcount > 0


def excluir_visualizacao_artigo(id_visualizacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(visualizacao_artigo_sql.EXCLUIR, (id_visualizacao,))
        return cursor.rowcount > 0



def obter_visualizacao_artigo_por_id(id_visualizacao: int) -> Optional[VisualizacaoArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(visualizacao_artigo_sql.OBTER_POR_ID, (id_visualizacao,))
        row = cursor.fetchone()
        if row is None:
            return None
        return VisualizacaoArtigo(
            id_visualizacao=row["id_visualizacao"],
            id_artigo=row["id_artigo"],
            id_usuario=row["id_usuario"],
            Data_visualizacao=row["data_visualizacao"],
            mes_referencia=row["mes_referencia"],
            ano_referencia=row["ano_referencia"],
            Ativo=bool(row["ativo"])
        )

def obter_visualizacoes_por_artigo(id_artigo: int) -> list[VisualizacaoArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(visualizacao_artigo_sql.OBTER_TODAS_POR_ARTIGO, (id_artigo,))
        rows = cursor.fetchall()
        return [
            VisualizacaoArtigo(
                id_visualizacao=row["id_visualizacao"],
                id_artigo=row["id_artigo"],
                id_usuario=row["id_usuario"],
                Data_visualizacao=row["data_visualizacao"],
                mes_referencia=row["mes_referencia"],
                ano_referencia=row["ano_referencia"],
                Ativo=bool(row["ativo"])
            ) for row in rows
        ]





def obter_visualizacoes_por_mes_ano(mes: int, ano: int) -> list[VisualizacaoArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(visualizacao_artigo_sql.OBTER_TODAS_POR_MES_ANO, (mes, ano))
        rows = cursor.fetchall()
        return [VisualizacaoArtigo(
                id_visualizacao=row["id_visualizacao"],
                id_artigo=row["id_artigo"],
                id_usuario=row["id_usuario"],
                Data_visualizacao=row["data_visualizacao"],
                mes_referencia=row["mes_referencia"],
                ano_referencia=row["ano_referencia"],
                Ativo=bool(row["ativo"])
            ) for row in rows
        ]
