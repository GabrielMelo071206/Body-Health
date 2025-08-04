from typing import Optional
from datetime import date
from data.models.assinatura_model import Assinaturas
from data.sql.assinatura_sql import *
from data.util import get_connection

def criar_tabela_assinatura() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_ASSINATURA)
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao criar tabela assinatura: {e}")
        return False
    
def inserir_assinatura(assinatura: Assinaturas) -> Optional[int]:
    # Garantir que as tabelas necessárias existem
    from data.repo.cliente_repo import criar_tabela_cliente
    from data.repo.plano_repo import criar_tabela_plano
    from data.repo.usuario_repo import criar_tabela_usuario
    criar_tabela_usuario()
    criar_tabela_cliente()
    criar_tabela_plano()
    criar_tabela_assinatura()

    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(INSERIR_ASSINATURA, (
                assinatura.id_cliente,
                assinatura.id_plano,
                assinatura.data_inicio,
                assinatura.data_fim,
                assinatura.status,
                assinatura.valor_pago,
                assinatura.ativo
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao inserir assinatura: {e}")
            return None

def alterar_assinatura(assinatura: Assinaturas) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(ALTERAR_ASSINATURA, (
                assinatura.id_cliente,
                assinatura.id_plano,
                assinatura.data_inicio,
                assinatura.data_fim,
                assinatura.status,
                assinatura.valor_pago,
                assinatura.ativo,
                assinatura.id_assinatura
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao alterar assinatura: {e}")
            return False

def excluir_assinatura(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(EXCLUIR_ASSINATURA, (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir assinatura: {e}")
            return False

def obter_assinatura_por_id(id: int) -> Optional[Assinaturas]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ASSINATURA_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Assinaturas(
                id_assinatura=row["id_assinatura"],
                id_cliente=row["id_cliente"],
                id_plano=row["id_plano"],
                data_inicio=date.fromisoformat(row["data_inicio"]) if isinstance(row["data_inicio"], str) else row["data_inicio"],
                data_fim=date.fromisoformat(row["data_fim"]) if isinstance(row["data_fim"], str) else row["data_fim"],
                status=row["status"],
                valor_pago=row["valor_pago"],
                ativo=bool(row["ativo"])
            )
        return None

def obter_todas_assinaturas() -> list[Assinaturas]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS_ASSINATURAS)
        rows = cursor.fetchall()
        return [Assinaturas(
            id_assinatura=row["id_assinatura"],
            id_cliente=row["id_cliente"],
            id_plano=row["id_plano"],
            data_inicio=date.fromisoformat(row["data_inicio"]) if isinstance(row["data_inicio"], str) else row["data_inicio"],
            data_fim=date.fromisoformat(row["data_fim"]) if isinstance(row["data_fim"], str) else row["data_fim"],
            status=row["status"],
            valor_pago=row["valor_pago"],
            ativo=bool(row["ativo"])
        ) for row in rows]

def obter_assinaturas_por_cliente(id_cliente: int) -> list[Assinaturas]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ASSINATURAS_POR_CLIENTE, (id_cliente,))
        rows = cursor.fetchall()
        return [Assinaturas(
            id_assinatura=row["id_assinatura"],
            id_cliente=row["id_cliente"],
            id_plano=row["id_plano"],
            data_inicio=date.fromisoformat(row["data_inicio"]) if isinstance(row["data_inicio"], str) else row["data_inicio"],
            data_fim=date.fromisoformat(row["data_fim"]) if isinstance(row["data_fim"], str) else row["data_fim"],
            status=row["status"],
            valor_pago=row["valor_pago"],
            ativo=bool(row["ativo"])
        ) for row in rows]