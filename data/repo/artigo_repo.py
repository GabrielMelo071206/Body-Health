from typing import Optional
from data.models.artigo_model import Artigo
from data.sql.artigo_sql import *
from data.util import get_connection

def criar_tabela_artigo() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela artigo: {e}")
        return False

def inserir_artigo(artigo: Artigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(INSERIR, (
                artigo.id_profissional,
                artigo.titulo,
                artigo.conteudo,
                artigo.data_publicacao,
                artigo.visualizacoes,
                artigo.ativo,
                artigo.avaliacao
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao inserir artigo: {e}")
            return None

def alterar_artigo(artigo: Artigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(ALTERAR, (
                artigo.titulo,
                artigo.conteudo,
                artigo.data_publicacao,
                artigo.visualizacoes,
                artigo.ativo,
                artigo.avaliacao,
                artigo.id_artigo
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao alterar artigo: {e}")
            return False

def excluir_artigo(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(EXCLUIR, (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir artigo: {e}")
            return False

def obter_artigo_por_id(id: int) -> Optional[Artigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Artigo(
                id_artigo=row["id_artigo"],
                id_profissional=row["id_profissional"],
                titulo=row["titulo"],
                conteudo=row["conteudo"],
                data_publicacao=row["data_publicacao"],
                visualizacoes=row["visualizacoes"],
                ativo=row["ativo"],
                avaliacao=row["avaliacao"]
            )
        return None

def obter_artigos_por_profissional(id_profissional: int) -> list[Artigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PROFISSIONAL, (id_profissional,))
        rows = cursor.fetchall()
        return [Artigo(
            id_artigo=row["id_artigo"],
            id_profissional=row["id_profissional"],
            titulo=row["titulo"],
            conteudo=row["conteudo"],
            data_publicacao=row["data_publicacao"],
            visualizacoes=row["visualizacoes"],
            ativo=row["ativo"],
            avaliacao=row["avaliacao"]
        ) for row in rows]

def obter_todos_artigos() -> list[Artigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [Artigo(
            id_artigo=row["id_artigo"],
            id_profissional=row["id_profissional"],
            titulo=row["titulo"],
            conteudo=row["conteudo"],
            data_publicacao=row["data_publicacao"],
            visualizacoes=row["visualizacoes"],
            ativo=row["ativo"],
            avaliacao=row["avaliacao"]
        ) for row in rows]
