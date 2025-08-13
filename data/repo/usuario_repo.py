from typing import Any, Optional
from data.models.usuario_model import Usuario
from data.sql.usuario_sql import *
from data.util import *

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Insere na tabela usuarios
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha_hash,
            usuario.data_nascimento,
            usuario.sexo,
            usuario.tipo_usuario
        ))
        usuario_id = cursor.lastrowid
        
        # Debug: imprimir o tipo de usuário
        print(f"DEBUG: tipo_usuario = '{usuario.tipo_usuario}'")
        
        # Se for cliente, insere na tabela cliente
        if usuario.tipo_usuario == "cliente":
            print("DEBUG: Inserindo cliente")
            cursor.execute("INSERT INTO cliente (id_cliente, tipo_conta) VALUES (?, ?)", (usuario_id, "cliente"))
        
        # Se for profissional, insere na tabela profissional
        elif usuario.tipo_usuario in ["profissional", "educador_fisico", "nutricionista"]:
            print(f"DEBUG: Inserindo profissional com tipo: {usuario.tipo_usuario}")
            cursor.execute("INSERT INTO profissional (id_profissional, ativo, ano_formacao, registro_profissional) VALUES (?, ?, ?, ?)", 
                         (usuario_id, 1, 2024, "PENDENTE"))
        else:
            print(f"DEBUG: Tipo não reconhecido: '{usuario.tipo_usuario}'")
        
        conn.commit()
        return usuario_id

def alterar_usuario(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            usuario.nome,
            usuario.email,
            usuario.data_nascimento,
            usuario.sexo,
            usuario.tipo_usuario,
            usuario.id))
        return (cursor.rowcount > 0)

def atualizar_senha_usuario(id: int, senha_hash: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_SENHA, (senha_hash, id))
        return (cursor.rowcount > 0)

def excluir_usuario(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        conn.commit()
        return cursor.rowcount > 0

def obter_usuario_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        usuario = Usuario(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            data_nascimento=row["data_nascimento"],
            sexo=row["sexo"],
            tipo_usuario=row["tipo_usuario"]
        )
        return usuario

def obter_todos_usuarios() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha_hash=row["senha_hash"],
                data_nascimento=row["data_nascimento"],
                sexo=row["sexo"],
                tipo_usuario=row["tipo_usuario"]
            )
            for row in rows]
        return usuarios