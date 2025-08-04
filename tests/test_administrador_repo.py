from data.repo.administrador_repo import *
from data.repo.usuario_repo import *
from data.models.administrador_model import *
from data.sql.administrador_sql import *

class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        resultado = criar_tabela_administrador()
        assert resultado == True, "A tabela de usuários não foi criada corretamente."       

    def test_inserir_administrador(self, test_db, administrador_exemplo):
        criar_tabela_usuario()
        criar_tabela_administrador()
        # Act
        id_inserido = inserir_administrador(administrador_exemplo)
        administrador_db = obter_administrador_por_id(id_inserido)
        
        # Assert
        assert administrador_db is not None, "O usuário inserido não deve ser None"
        assert administrador_db.id == id_inserido, "O ID do profissional não confere"
        assert administrador_db.master == administrador_exemplo.master, "O nome não confere"
        assert administrador_db.email == administrador_exemplo.email, "O email inserido não confere"
        assert administrador_db.senha_hash == administrador_exemplo.senha_hash, "A senha inserida não confere"
        assert administrador_db.data_nascimento == administrador_exemplo.data_nascimento, "A data inserida não confere"
        assert administrador_db.sexo == administrador_exemplo.sexo, "O sexo inserido não confere"
        assert administrador_db.tipo_usuario == administrador_exemplo.tipo_usuario, "O tipo de usuario inserido não confere"
        
              
    
    
    def test_obter_administrador_por_id_existente(self, test_db, administrador_exemplo):
        usuario_repo.criar_tabela_usuario()
        criar_tabela_administrador()
        id_administrador_inserido = inserir_administrador(administrador_exemplo)
        administrador_encontrado = obter_administrador_por_id(id_administrador_inserido)
        assert administrador_encontrado is not None
        assert administrador_encontrado.id == id_administrador_inserido
        assert administrador_encontrado.nome == administrador_exemplo.nome, "O nome não confere"
        assert administrador_encontrado.email == administrador_exemplo.email, "O email não confere"
        assert administrador_encontrado.senha_hash == administrador_exemplo.senha_hash, "A senha não confere"
        assert administrador_encontrado.sexo == administrador_exemplo.sexo, "O sexo não confere"
        assert administrador_encontrado.tipo_usuario == administrador_exemplo.tipo_usuario, "O tipo de usuário não confere"
        assert administrador_encontrado.master == administrador_exemplo.master, "O master não confere"

    def test_obter_administrador_por_id_inexistente(self, test_db):
        # Arrange: prepara o banco (sem inserir administradores)
        usuario_repo.criar_tabela_usuario()
        criar_tabela_administrador()
        # Act: tenta buscar um administrador com ID que não existe
        administrador_encontrado = obter_administrador_por_id(999)
        # Assert: verifica se retorna None
        assert administrador_encontrado is None, "Deveria retornar None para administrador inexistente"

    def test_atualizar_administrador_existente(self, test_db, administrador_exemplo):
        usuario_repo.criar_tabela_usuario()
        criar_tabela_administrador()
        
        id_administrador_inserido = inserir_administrador(administrador_exemplo)
        print(f"id_administrador_inserido: {id_administrador_inserido}")  # debug
        
        administrador_inserido = obter_administrador_por_id(id_administrador_inserido)
        print(f"administrador_inserido: {administrador_inserido}")  # debug
        
        assert administrador_inserido is not None, "Administrador inserido deve existir"
        
        administrador_inserido.nome = "Administrador Atualizado"
        administrador_inserido.email = "atualizado@example.com"
        administrador_inserido.sexo = "Feminino"
        administrador_inserido.tipo_usuario = "administrador"
        administrador_inserido.data_nascimento = "2000-01-15"
        administrador_inserido.senha_hash = "senha_super_segura_123"
        
        resultado = alterar_administrador(administrador_inserido)
        
        assert resultado is True, "Atualização deveria retornar True"
        
        administrador_atualizado = obter_administrador_por_id(administrador_inserido.id)
        
        assert administrador_atualizado.nome == "Administrador Atualizado", "Nome não atualizado"
        assert administrador_atualizado.email == "atualizado@example.com", "Email não atualizado"
        assert administrador_atualizado.sexo == "Feminino", "Sexo não atualizado"
        assert administrador_atualizado.tipo_usuario == "administrador", "Tipo usuário não atualizado"
        assert administrador_atualizado.master == administrador_exemplo.master, "Master não atualizado"
        assert administrador_atualizado.data_nascimento == administrador_exemplo.data_nascimento, "Data de nascimento não atualizada"
        assert administrador_atualizado.senha_hash == administrador_exemplo.senha_hash, "Senha  não atualizada"
        


    def test_atualizar_administrador_inexistente(self, test_db, administrador_exemplo):
        # Arrange: prepara o banco sem inserir administradores
        usuario_repo.criar_tabela_usuario()
        criar_tabela_administrador()
        administrador_exemplo.id = 999  # ID que não existe
        # Act: tenta atualizar um administrador inexistente
        resultado = alterar_administrador(administrador_exemplo)
        # Assert: verifica se retornou False
        assert resultado == False, "Deveria retornar False para administrador inexistente"

    def test_excluir_administrador_existente(self, test_db, administrador_exemplo, usuario_exemplo):
        # Arrange: insere um administrador para depois excluir
        usuario_repo.criar_tabela_usuario()
        usuario_repo.inserir_usuario(usuario_exemplo)
        criar_tabela_administrador()
        id_administrador_inserido = inserir_administrador(administrador_exemplo)
        # Act: exclui o administrador
        resultado = excluir_administrador(id_administrador_inserido)
        # Assert: verifica se a exclusão foi bem-sucedida
        assert resultado == True, "A exclusão deveria retornar True"
        # Verifica se o administrador foi realmente excluído
        administrador_excluido = obter_administrador_por_id(id_administrador_inserido)
        assert administrador_excluido is None, "O administrador deveria ter sido excluído"

    def test_excluir_administrador_inexistente(self, test_db):
        # Arrange: prepara o banco sem administradores
        usuario_repo.criar_tabela_usuario()
        criar_tabela_administrador()
        # Act: tenta excluir um administrador inexistente
        resultado = excluir_administrador(999)
        # Assert: verifica se retorna False
        assert resultado == False, "Deveria retornar False para administrador inexistente"


    def test_atualizar_senha_administrador_existente(self, test_db, administrador_exemplo):
        criar_tabela_usuario()
        criar_tabela_administrador()  # <-- necessário para o contexto do teste
        """
        Testa a atualização da senha de um profissional existente.
        A funcionalidade reside no usuario_repo, mas é testada aqui por contexto.
        """
        # Arrange
        id_administrador = inserir_administrador(administrador_exemplo)
        nova_senha = "senha_profissional_nova_456"

        # Act
        resultado = usuario_repo.atualizar_senha_usuario(id_administrador, nova_senha)

        # Assert
        assert resultado is True, "A função de atualizar senha deveria retornar True"

        # Verificação extra
        usuario_com_senha_alterada = usuario_repo.obter_usuario_por_id(id_administrador)
        assert usuario_com_senha_alterada is not None, "Não foi possível encontrar o usuário após a atualização da senha"
        assert usuario_com_senha_alterada.senha_hash == nova_senha, "A senha no banco de dados não corresponde à nova senha"