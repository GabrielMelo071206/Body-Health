from datetime import datetime
from data.repo import denuncia_repo
from data.repo.usuario_repo import criar_tabela_usuario, inserir_usuario
from data.repo.profissional_repo import criar_tabela_profissional, inserir_profissional
from data.repo.administrador_repo import criar_tabela_administrador, inserir_administrador
from data.repo.denuncia_repo import *
from data.sql import denuncia_sql
from tests.conftest import administrador_exemplo, denuncia_exemplo, profissional_exemplo, usuario_exemplo


class TestDenunciaRepo:

    def test_criar_tabela_denuncia(self, test_db):
        resultado = criar_tabela_denuncia()
        assert resultado is True, "Tabela de denúncia não foi criada corretamente"

    
    def test_inserir_denuncia(self,test_db,usuario_exemplo,profissional_exemplo,administrador_exemplo,denuncia_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_administrador()
        criar_tabela_denuncia()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_profissional = inserir_profissional(profissional_exemplo)
        id_admin = inserir_administrador(administrador_exemplo)

        denuncia_exemplo.id_denunciante = id_usuario
        denuncia_exemplo.id_denunciado = id_profissional
        denuncia_exemplo.id_admin_avaliador = id_admin

        id = inserir_denuncia(denuncia_exemplo)
        assert id is not None, "ID da denúncia inserida não pode ser None"

        denuncia_db = obter_denuncia_por_id(id)
        assert denuncia_db is not None, "Denúncia não encontrada após inserção"
        assert denuncia_db.status == "pendente", "Status não foi atualizado"
        assert denuncia_db.observacoes_admin == "Aguardando análise", "Observações não atualizadas"
        assert denuncia_db.id_denunciante == id_usuario, "ID do denunciante não corresponde"
        assert denuncia_db.id_denunciado == id_profissional, "ID do denunciado não corresponde"
        assert denuncia_db.tipo_denunciante == "cliente", "Tipo de denunciante incorreto"
        assert denuncia_db.tipo_denunciado == "nutricionista", "Tipo de denunciado incorreto"
        assert denuncia_db.motivo == "Conteúdo impróprio", "Motivo incorreto"
        assert denuncia_db.descricao == "O profissional compartilhou conteúdo inadequado no artigo.", "Descrição incorreta"
        assert denuncia_db.data_denuncia[:10] == datetime.now().strftime('%Y-%m-%d'), "Data da denúncia incorreta"
        assert denuncia_db.id_admin_avaliador == id_admin, "ID do admin avaliador não corresponde"
        assert denuncia_db.ativo == 1, "Denúncia deve estar ativa"

    
    def test_obter_denuncia_por_id_inexistente(self, test_db):
        criar_tabela_denuncia()
        denuncia = obter_denuncia_por_id(999)
        assert denuncia is None, "Deveria retornar None para denúncia inexistente"

    def test_alterar_denuncia(self, test_db, usuario_exemplo, profissional_exemplo, administrador_exemplo, denuncia_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_administrador()
        criar_tabela_denuncia()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_profissional = inserir_profissional(profissional_exemplo)
        id_admin = inserir_administrador(administrador_exemplo)

        denuncia_exemplo.id_denunciante = id_usuario
        denuncia_exemplo.id_denunciado = id_profissional
        denuncia_exemplo.id_admin_avaliador = id_admin

        id = inserir_denuncia(denuncia_exemplo)

        denuncia = obter_denuncia_por_id(id)
        denuncia.status = "avaliada"
        denuncia.observacoes_admin = "Denúncia foi avaliada e arquivada"

        resultado = alterar_denuncia(denuncia)
        denuncia_atualizada = obter_denuncia_por_id(id)

        assert resultado is True, "Alteração deveria retornar True"
        assert denuncia_atualizada.status == "avaliada", "Status não foi atualizado"
        assert denuncia_atualizada.observacoes_admin == "Denúncia foi avaliada e arquivada", "Observações não atualizadas"
        assert denuncia_atualizada.id_denunciante == id_usuario, "ID do denunciante não corresponde"
        assert denuncia_atualizada.id_denunciado == id_profissional, "ID do denunciado não corresponde"
        assert denuncia_atualizada.tipo_denunciante == "cliente", "Tipo de denunciante incorreto"
        assert denuncia_atualizada.tipo_denunciado == "nutricionista", "Tipo de denunciado incorreto"
        assert denuncia_atualizada.motivo == "Conteúdo impróprio", "Motivo incorreto"
        assert denuncia_atualizada.descricao == "O profissional compartilhou conteúdo inadequado no artigo.", "Descrição incorreta"
        assert denuncia_atualizada.data_denuncia[:10] == datetime.now().strftime('%Y-%m-%d'), "Data da denúncia incorreta"
        assert denuncia_atualizada.id_admin_avaliador == id_admin, "ID do admin avaliador não corresponde"
        assert bool(denuncia_atualizada.ativo) is True, "Denúncia deve estar ativa"


    def test_excluir_denuncia(self, test_db, denuncia_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_administrador()
        criar_tabela_denuncia()

        id = inserir_denuncia(denuncia_exemplo)
        resultado = excluir_denuncia(id)
        denuncia_excluida = obter_denuncia_por_id(id)
        assert resultado is True, "Exclusão deveria retornar True"
        assert denuncia_excluida is None, "Denúncia ainda existe após exclusão"

    def test_excluir_denuncia_inexistente(self, test_db):
        criar_tabela_denuncia()
        resultado = excluir_denuncia(999)
        assert resultado is False, "Excluir denúncia inexistente deveria retornar False"
        
    def test_obter_todas_denuncias(self, test_db, usuario_exemplo, profissional_exemplo, administrador_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_administrador()
        criar_tabela_denuncia()

        id_usuario = inserir_usuario(usuario_exemplo)
        profissional_exemplo.id = 0
        id_prof = inserir_profissional(profissional_exemplo)
        id_admin = inserir_administrador(administrador_exemplo)

        denuncia = Denuncia(
            id_denuncia=0,
            id_denunciante=id_usuario,
            id_denunciado=id_prof,
            tipo_denunciante="cliente",
            tipo_denunciado="nutricionista",
            motivo="Comportamento inadequado",
            descricao="O profissional foi ofensivo no atendimento.",
            data_denuncia=str(datetime.now()),
            status="pendente",
            id_admin_avaliador=id_admin,
            data_avaliacao=str(datetime.now()),
            observacoes_admin="Aguardando avaliação",
            ativo=True
        )

        inserir_denuncia(denuncia)
        denuncias = obter_todas_denuncias()
        assert isinstance(denuncias, list), "Deveria retornar uma lista"
        assert len(denuncias) > 0, "Lista de denúncias não deveria estar vazia"
        
    def test_obter_denuncia_por_id_existente(self, test_db, usuario_exemplo, profissional_exemplo, administrador_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_administrador()
        criar_tabela_denuncia()

        # Inserções reais
        id_usuario = inserir_usuario(usuario_exemplo)
        profissional_exemplo.id = 0  # Evita conflito com FK
        id_prof = inserir_profissional(profissional_exemplo)
        id_admin = inserir_administrador(administrador_exemplo)

        # Cria e insere denúncia
        denuncia = Denuncia(
            id_denuncia=0,
            id_denunciante=id_usuario,
            id_denunciado=id_prof,
            tipo_denunciante="cliente",
            tipo_denunciado="nutricionista",
            motivo="Informação falsa",
            descricao="O artigo publicado continha informações incorretas.",
            data_denuncia=str(datetime.now()),
            status="pendente",
            id_admin_avaliador=id_admin,
            data_avaliacao=str(datetime.now()),
            observacoes_admin="Será analisado em breve.",
            ativo=True
        )

        id_denuncia = inserir_denuncia(denuncia)

        # Testa busca por ID
        denuncia_encontrada = obter_denuncia_por_id(id_denuncia)
        assert denuncia_encontrada is not None, "Deveria retornar uma denúncia"
        assert denuncia_encontrada.id_denunciante == id_usuario
        assert denuncia_encontrada.id_denunciado == id_prof
        assert denuncia_encontrada.status == "pendente"
        assert denuncia_encontrada.observacoes_admin == "Será analisado em breve."
