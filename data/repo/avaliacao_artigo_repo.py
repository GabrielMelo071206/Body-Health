from typing import Optional
from datetime import date
from data.models.avaliacao_artigo_model import AvaliacaoArtigo
from data.sql import avaliacao_artigo_sql
from data.util import get_connection

def criar_tabela_avaliacao_artigo() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(avaliacao_artigo_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela avaliacao_artigo: {e}")
        return False

def inserir_avaliacao_artigo(avaliacao: AvaliacaoArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(avaliacao_artigo_sql.INSERIR, (
            avaliacao.id_artigo,
            avaliacao.id_usuario,
            avaliacao.nota,
            avaliacao.Data_avaliacao,
            avaliacao.Ativo
        ))
        return cursor.lastrowid

def alterar_avaliacao_artigo(avaliacao: AvaliacaoArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(avaliacao_artigo_sql.ALTERAR, (
            avaliacao.nota,
            avaliacao.Data_avaliacao,
            int(avaliacao.Ativo),  # converte para 0/1
            avaliacao.id_avaliacao
        ))
        conn.commit()
        return cursor.rowcount > 0


def excluir_avaliacao_artigo(id_avaliacao: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(avaliacao_artigo_sql.EXCLUIR, (id_avaliacao,))
        return cursor.rowcount > 0

def obter_avaliacao_artigo_por_id(id_avaliacao: int) -> Optional[AvaliacaoArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(avaliacao_artigo_sql.OBTER_POR_ID, (id_avaliacao,))
        row = cursor.fetchone()
        if row is None:
            return None
        return AvaliacaoArtigo(
            id_avaliacao=row["id_avaliacao"],
            id_artigo=row["id_artigo"],
            id_usuario=row["id_usuario"],
            nota=row["nota"],
            Data_avaliacao=row["data_avaliacao"],
            Ativo=bool(row["ativo"])
        )

def obter_todas_avaliacoes_artigo() -> list[AvaliacaoArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(avaliacao_artigo_sql.OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            AvaliacaoArtigo(
                id_avaliacao=row["id_avaliacao"],
                id_artigo=row["id_artigo"],
                id_usuario=row["id_usuario"],
                nota=row["nota"],
                Data_avaliacao=row["data_avaliacao"],
                Ativo=bool(row["ativo"])
            ) for row in rows
        ]

def obter_avaliacoes_por_artigo(id_artigo: int) -> list[AvaliacaoArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(avaliacao_artigo_sql.OBTER_TODAS_POR_ARTIGO, (id_artigo,))
        rows = cursor.fetchall()
        return [
            AvaliacaoArtigo(
                id_avaliacao=row["id_avaliacao"],
                id_artigo=row["id_artigo"],
                id_usuario=row["id_usuario"],
                nota=row["nota"],
                Data_avaliacao=row["data_avaliacao"],
                Ativo=bool(row["ativo"])
            ) for row in rows
        ]

def obter_media_avaliacoes_por_artigo(id_artigo: int) -> Optional[float]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(avaliacao_artigo_sql.OBTER_MEDIA_POR_ARTIGO, (id_artigo,))
        row = cursor.fetchone()
        if row and row["media_nota"] is not None:
            return float(row["media_nota"])
        return None
