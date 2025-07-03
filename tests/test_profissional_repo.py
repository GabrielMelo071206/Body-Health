# tests/test_profissional_repo.py (versão final completa)

from data.repo.profissional_repo import *
from data.repo import usuario_repo
from data.models.profissional_model import *
from data.sql.profissional_sql import *

class TestProfissionalRepo:
    def test_criar_tabela_profissional(self, test_db):
        resultado = criar_tabela_profissional()
        assert resultado == True, "A tabela de usuários não foi criada corretamente."       

    def test_inserir_profissional(self, test_db, nutricionista_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        # Act
        id_inserido = inserir_profissional(nutricionista_exemplo)
        # Assert
        profissional_db = obter_profissional_por_id(id_inserido)
        assert profissional_db is not None, "O profissional inserido não deveria ser None"
        assert profissional_db.id == id_inserido, "O ID do profissional não confere"
        assert profissional_db.nome == nutricionista_exemplo.nome, "O nome não confere"
        assert profissional_db.tipo_usuario == nutricionista_exemplo.tipo_usuario, "O tipo de profissional não confere"

    def test_obter_profissional_por_id_existente(self, test_db, nutricionista_exemplo):
        criar_tabela_profissional()
        criar_tabela_usuario()
        id_inserido = inserir_profissional(nutricionista_exemplo)
        profissional_db = obter_profissional_por_id(id_inserido)
        assert profissional_db is not None, "O profissional inserido não deveria ser None"
        assert profissional_db.id == id_inserido, "O ID do profissional não confere"
        assert profissional_db.nome == nutricionista_exemplo.nome, "O nome não confere"
        assert profissional_db.tipo_usuario == nutricionista_exemplo.tipo_usuario, "O tipo de profissional não confere"

    def test_obter_profissional_por_id_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_profissional()
        profissional_db = obter_profissional_por_id(999)
        assert profissional_db is None, "Deveria retornar None para um ID inexistente"

    def test_alterar_profissional_existente(self, test_db, nutricionista_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        id_inserido = inserir_profissional(nutricionista_exemplo)
        profissional_db = obter_profissional_por_id(id_inserido)
        assert profissional_db is not None, "O profissional inserido não deveria ser None"
        assert profissional_db.id == id_inserido, "O ID do profissional não confere"
        assert profissional_db.nome == nutricionista_exemplo.nome, "O nome não confere"
        assert profissional_db.tipo_usuario == nutricionista_exemplo.tipo_usuario, "O tipo de profissional não confere"

        # Act
        profissional_db.nome = "Dra. Exemplo Alterada"
        profissional_db.ano_formacao = "inativo"
        profissional_db.registro_profissional = "123456-G/DF"
        profissional_db.ativo = False  # Alterando o status para inativo
        resultado = alterar_profissional(profissional_db)
        profissional_alterado_db = obter_profissional_por_id(id_inserido)

        # Assert
        assert resultado is True, "A operação de alterar deveria retornar True"
        assert profissional_alterado_db.nome == "Dra. Exemplo Alterada", "O nome não foi alterado corretamente"
        assert profissional_alterado_db.ano_formacao == "inativo", "O ano de formação não foi alterado corretamente"
        assert profissional_alterado_db.registro_profissional == "123456-G/DF", "O registro profissional não foi alterado corretamente"

    def test_alterar_profissional_inexistente(self, test_db, nutricionista_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()        
        nutricionista_exemplo.id = 999  # Um ID que não existe
        resultado = alterar_profissional(nutricionista_exemplo)
        assert resultado is False, "A tentativa de alterar um profissional inexistente deveria retornar False"






    def test_excluir_profissional_existente(self, test_db, nutricionista_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()

        # Arrange
        id_inserido = inserir_profissional(nutricionista_exemplo)

        # Act
        resultado = excluir_profissional(id_inserido)
        profissional_excluido = obter_profissional_por_id(id_inserido)

        # Assert
        assert resultado is True, "A operação de excluir deveria retornar True"
        assert profissional_excluido is None, "O registro na tabela 'profissional' deveria ter sido excluído"

    def test_excluir_profissional_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_profissional()
        resultado = excluir_profissional(999)
        assert resultado is False, "A tentativa de excluir um profissional inexistente deveria retornar False"

    def test_atualizar_senha_profissional_existente(self, test_db, nutricionista_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()  # <-- necessário para o contexto do teste
        """
        Testa a atualização da senha de um profissional existente.
        A funcionalidade reside no usuario_repo, mas é testada aqui por contexto.
        """
        # Arrange
        id_profissional = inserir_profissional(nutricionista_exemplo)
        nova_senha = "senha_profissional_nova_456"

        # Act
        resultado = usuario_repo.atualizar_senha_usuario(id_profissional, nova_senha)

        # Assert
        assert resultado is True, "A função de atualizar senha deveria retornar True"

        # Verificação extra
        usuario_com_senha_alterada = usuario_repo.obter_usuario_por_id(id_profissional)
        assert usuario_com_senha_alterada is not None, "Não foi possível encontrar o usuário após a atualização da senha"
        assert usuario_com_senha_alterada.senha_hash == nova_senha, "A senha no banco de dados não corresponde à nova senha"