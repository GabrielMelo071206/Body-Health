import sys
import os
from data.repo.cliente_repo import *
from data.models.cliente_model import *
from data.sql.cliente_sql import *
from data.repo.usuario_repo import *

class TestClienteRepo:
    def test_criar_tabela_cliente(self, test_db):
        resultado = criar_tabela_cliente()
        assert resultado == True, "A tabela de usuários não foi criada corretamente."

    def test_inserir_cliente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        cliente_teste = Cliente(0, "Cliente Teste", "Cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_usuario_db = inserir_cliente(cliente_teste)
        cliente_db = obter_cliente_por_id(id_usuario_db)
        assert cliente_db is not None
        assert cliente_db.id == 1
        assert cliente_db.nome == "Cliente Teste"
        assert cliente_db.email == "Cliente@gmail.com"
        assert cliente_db.senha_hash == "senha123"
        assert cliente_db.data_nascimento == "1990-01-01"
        assert cliente_db.sexo == "M"
        assert cliente_db.tipo_usuario == "cliente"
        assert cliente_db.tipo_conta == "gratuita"

    def test_obter_cliente_por_id_existente(self, test_db, cliente_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        id_cliente_inserido = inserir_cliente(cliente_exemplo)
        cliente_db = obter_cliente_por_id(id_cliente_inserido)
        assert cliente_db is not None
        assert cliente_db.id == id_cliente_inserido
        assert cliente_db.nome == cliente_exemplo.nome

    def test_obter_cliente_por_id_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        cliente_db = obter_cliente_por_id(999)
        assert cliente_db is None

    def test_excluir_cliente_existente(self, test_db, cliente_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        id_cliente_inserido = inserir_cliente(cliente_exemplo)
        resultado = excluir_cliente(id_cliente_inserido)
        assert resultado == True
        cliente_excluido = obter_cliente_por_id(id_cliente_inserido)
        assert cliente_excluido is None

    def test_excluir_cliente_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        resultado = excluir_cliente(999)
        assert resultado == False

    def test_atualizar_senha_cliente_existente(self, test_db, cliente_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()

        # Arrange
        id_cliente = inserir_cliente(cliente_exemplo)
        nova_senha = "nova_senha_cliente_456"

        # Act
        resultado = usuario_repo.atualizar_senha_usuario(id_cliente, nova_senha)

        # Assert
        assert resultado is True, "A função de atualizar senha deveria retornar True"

        # Verificação extra
        cliente_modificado = usuario_repo.obter_usuario_por_id(id_cliente)
        assert cliente_modificado is not None, "Não foi possível encontrar o usuário após a atualização da senha"
        assert cliente_modificado.senha_hash == nova_senha, "A senha no banco de dados não corresponde à nova senha"

    def test_alterar_cliente_existente(self, test_db, cliente_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()

        # Arrange
        id_cliente = inserir_cliente(cliente_exemplo)
        cliente_para_alterar = obter_cliente_por_id(id_cliente)

        # Act
        cliente_para_alterar.nome = "Cliente Alterado"
        cliente_para_alterar.tipo_conta = "premium"
        resultado = alterar_cliente(cliente_para_alterar)
        cliente_alterado_db = obter_cliente_por_id(id_cliente)

        # Assert
        assert resultado is True, "A operação de alterar deveria retornar True"
        assert cliente_alterado_db.nome == "Cliente Alterado", "O nome não foi alterado corretamente"
        assert cliente_alterado_db.tipo_conta == "premium", "O tipo de conta não foi alterado corretamente"
        assert cliente_alterado_db.email == "exemplo@teste.com", "O email não foi alterado corretamente"  
        assert cliente_alterado_db.senha_hash == "senha_super_segura_123", "A senha não foi alterada corretamente"  
        assert cliente_alterado_db.sexo == "F", "O sexo não foi alterado corretamente"
        assert cliente_alterado_db.tipo_usuario == "cliente", "O tipo de usuário não foi alterado corretamente"


    def test_alterar_cliente_inexistente(self, test_db, cliente_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()

        # Arrange
        cliente_exemplo.id = 999  # Um ID que não existe

        # Act
        resultado = alterar_cliente(cliente_exemplo)

        # Assert
        assert resultado is False, "A tentativa de alterar um cliente inexistente deveria retornar False"
