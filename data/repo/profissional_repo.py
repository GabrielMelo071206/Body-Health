from typing import Optional
from data.models.usuario_model import *
from data.repo.usuario_repo import *
from data.sql.profissional_sql import *
from data.models.profissional_model import Profissional
from data.repo import usuario_repo
from data.util import get_connection


def criar_tabela_profissional() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False


def inserir_profissional(profissional: Profissional) -> Optional[int]:
    id_profissional = usuario_repo.inserir_usuario(profissional)
    if id_profissional is None:
        return None
    with get_connection() as conn:
        cursor = conn.cursor()        
        cursor.execute(INSERIR, (
            id_profissional,
            profissional.ativo,
            profissional.ano_formacao,
            profissional.registro_profissional)),
        return id_profissional


def alterar_profissional(profissional: Profissional) -> bool: 
    # Primeiro, atualiza os dados do usuário na tabela usuario
    if not usuario_repo.alterar_usuario(profissional):
        return False
    with get_connection() as conn:
        cursor = conn.cursor()        
        cursor.execute(ALTERAR, (
            profissional.ativo,
            profissional.ano_formacao,
            profissional.registro_profissional,
            profissional.id))
        return cursor.rowcount > 0    


def excluir_profissional(id: int) -> bool:
    if usuario_repo.excluir_usuario(id) is False:
        return False
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0

def obter_profissional_por_id(id: int) -> Optional[Profissional]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        # p.id_profissional, u.nome, u.email, u.senha_hash, u.data_nascimento, u.sexo, u.tipo_usuario, p.ativo, p.ano_formacao, p.registro_profissional
        return Profissional(
            id=row["id_profissional"],
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            data_nascimento=row["data_nascimento"],
            sexo=row["sexo"],
            tipo_usuario=row["tipo_usuario"],
            ativo=row["ativo"],
            ano_formacao=row["ano_formacao"],
            registro_profissional=row["registro_profissional"]
        )

def obter_todos_profissionais() -> list[Profissional]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [Profissional(
                    id=row["id_profissional"],
                    nome=row["nome"],
                    email=row["email"],
                    senha_hash=row["senha_hash"],
                    data_nascimento=row["data_nascimento"],
                    sexo=row["sexo"],
                    tipo_usuario=row["tipo_usuario"],
                    ativo=row["ativo"],
                    ano_formacao=row["ano_formacao"],
                    registro_profissional=row["registro_profissional"]
                )
                for row in rows
                ]
