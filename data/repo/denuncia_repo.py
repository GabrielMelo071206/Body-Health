from typing import Optional, List
from data.models.denuncia_model import Denuncia
from data.sql import denuncia_sql
from data.util import get_connection


def criar_tabela_denuncia() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(denuncia_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de denúncia: {e}")
        return False


def inserir_denuncia(denuncia: Denuncia) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(denuncia_sql.INSERIR, (
            denuncia.id_denuncia,
            denuncia.id_denunciante,
            denuncia.tipo_denunciante,
            denuncia.tipo_denunciado,
            denuncia.id_denunciado,
            denuncia.motivo,
            denuncia.descricao,
            denuncia.status,
            denuncia.id_admin_avaliador,
            denuncia.observacoes_admin,
            denuncia.ativo
        ))
        return cursor.lastrowid


def alterar_denuncia(denuncia: Denuncia) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(denuncia_sql.ALTERAR, (
            denuncia.id_denunciante,
            denuncia.id_denunciado,
            denuncia.tipo_denunciante,
            denuncia.tipo_denunciado,
            denuncia.motivo,
            denuncia.descricao,
            denuncia.status,
            denuncia.id_admin_avaliador,
            denuncia.data_avaliacao,
            denuncia.observacoes_admin,
            denuncia.ativo,
            denuncia.id_denuncia
        ))
        return cursor.rowcount > 0


def excluir_denuncia(id_denuncia: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(denuncia_sql.EXCLUIR, (id_denuncia,))
        return cursor.rowcount > 0


def obter_denuncia_por_id(id_denuncia: int) -> Optional[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(denuncia_sql.OBTER_POR_ID, (id_denuncia,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Denuncia(
            id_denuncia=row["id_denuncia"],
            id_denunciante=row["id_denunciante"],
            id_denunciado=row["id_denunciado"],
            tipo_denunciante=row["tipo_denunciante"],
            tipo_denunciado=row["tipo_denunciado"],
            motivo=row["motivo"],
            descricao=row["descricao"],
            data_denuncia=row["data_avaliacao"],  # pode ajustar se estiver usando outro campo
            status=row["status"],
            id_admin_avaliador=row["id_admin_avaliador"],
            data_avaliacao=row["data_avaliacao"],
            observacoes_admin=row["observacoes_admin"],
            ativo=row["ativo"]
        )


def obter_todas_denuncias() -> List[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(denuncia_sql.OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Denuncia(
                id_denuncia=row["id_denuncia"],
                id_denunciante=row["id_denunciante"],
                id_denunciado=row["id_denunciado"],
                tipo_denunciante=row["tipo_denunciante"],
                tipo_denunciado=row["tipo_denunciado"],
                motivo=row["motivo"],
                descricao=row["descricao"],
                data_denuncia=row["data_avaliacao"],  # mesma observação acima
                status=row["status"],
                id_admin_avaliador=row["id_admin_avaliador"],
                data_avaliacao=row["data_avaliacao"],
                observacoes_admin=row["observacoes_admin"],
                ativo=row["ativo"]
            )
            for row in rows
        ]
