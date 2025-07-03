from data.repo import dieta_repo, cliente_repo, profissional_repo, usuario_repo
from data.models.dieta_model import *
from data.models.cliente_model import *
from data.models.profissional_model import *
from datetime import date


class TestDietaRepo:

    def test_criar_tabela_dieta(self, test_db):
        resultado = dieta_repo.criar_tabela_dieta()
        assert resultado is True, "A tabela dieta não foi criada corretamente"

    def test_inserir_dieta(self, test_db, cliente_exemplo, nutricionista_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        dieta_repo.criar_tabela_dieta()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_profissional = profissional_repo.inserir_profissional(nutricionista_exemplo)

        dieta = Dieta(
            id_dieta=0,
            id_cliente=id_cliente,
            id_profissional=id_profissional,
            nome="Dieta Teste",
            descricao="Descrição Teste",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 31),
            ativo=True,
            especificacoes="Especificações Teste",
            tipo_dieta="Low Carb"
        )

        # Act
        id_dieta = dieta_repo.inserir_dieta(dieta)
        dieta_db = dieta_repo.obter_dieta_por_id(id_dieta)

        # Assert
        assert dieta_db is not None
        assert dieta_db.nome == "Dieta Teste"
        assert dieta_db.tipo_dieta == "Low Carb"
        assert dieta_db.ativo is True

    def test_obter_dietas_por_cliente(self, test_db, cliente_exemplo, nutricionista_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        dieta_repo.criar_tabela_dieta()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_prof = profissional_repo.inserir_profissional(nutricionista_exemplo)

        dieta = Dieta(
            id_dieta=0,
            id_cliente=id_cliente,
            id_profissional=id_prof,
            nome="Dieta Cliente",
            descricao="desc",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 10),
            ativo=True,
            especificacoes="",
            tipo_dieta="Mediterrânea"
        )

        dieta_repo.inserir_dieta(dieta)

        dietas = dieta_repo.obter_dietas_por_cliente(id_cliente)

        assert len(dietas) >= 1
        assert dietas[0].tipo_dieta == "Mediterrânea"

    def test_obter_dietas_por_profissional(self, test_db, cliente_exemplo, nutricionista_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        dieta_repo.criar_tabela_dieta()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_prof = profissional_repo.inserir_profissional(nutricionista_exemplo)

        dieta = Dieta(
            id_dieta=0,
            id_cliente=id_cliente,
            id_profissional=id_prof,
            nome="Dieta Pro",
            descricao="desc",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 10),
            ativo=True,
            especificacoes="",
            tipo_dieta="Cetogênica"
        )

        dieta_repo.inserir_dieta(dieta)

        dietas = dieta_repo.obter_dietas_por_profissional(id_prof)

        assert len(dietas) >= 1
        assert dietas[0].tipo_dieta == "Cetogênica"

    def test_alterar_dieta(self, test_db, cliente_exemplo, nutricionista_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        dieta_repo.criar_tabela_dieta()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_prof = profissional_repo.inserir_profissional(nutricionista_exemplo)

        dieta = Dieta(
            id_dieta=0,
            id_cliente=id_cliente,
            id_profissional=id_prof,
            nome="Dieta Inicial",
            descricao="desc",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 10),
            ativo=True,
            especificacoes="",
            tipo_dieta="Vegana"
        )

        id_dieta = dieta_repo.inserir_dieta(dieta)

        dieta_editada = dieta_repo.obter_dieta_por_id(id_dieta)
        dieta_editada.nome = "Dieta Alterada"
        dieta_editada.tipo_dieta = "Mediterrânea"
        resultado = dieta_repo.alterar_dieta(dieta_editada)

        assert resultado is True
        dieta_nova = dieta_repo.obter_dieta_por_id(id_dieta)
        assert dieta_nova.nome == "Dieta Alterada"
        assert dieta_nova.tipo_dieta == "Mediterrânea"

    def test_excluir_dieta(self, test_db, cliente_exemplo, nutricionista_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        dieta_repo.criar_tabela_dieta()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_prof = profissional_repo.inserir_profissional(nutricionista_exemplo)

        dieta = Dieta(
            id_dieta=0,
            id_cliente=id_cliente,
            id_profissional=id_prof,
            nome="Dieta Apagar",
            descricao="desc",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 10),
            ativo=True,
            especificacoes="",
            tipo_dieta="Dash"
        )

        id_dieta = dieta_repo.inserir_dieta(dieta)
        resultado = dieta_repo.excluir_dieta(id_dieta)
        dieta_apagada = dieta_repo.obter_dieta_por_id(id_dieta)

        assert resultado is True
        assert dieta_apagada is None


        # ... seus outros testes ...

        
    def test_obter_dieta_por_id_inexistente(self, test_db):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        dieta_repo.criar_tabela_dieta()
        dieta = dieta_repo.obter_dieta_por_id(9999)
        assert dieta is None, "Deveria retornar None para dieta inexistente"

    def test_alterar_dieta_inexistente(self, test_db, cliente_exemplo, nutricionista_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        dieta_repo.criar_tabela_dieta()
        # Cria um objeto Dieta com ID que não existe
        dieta_fake = Dieta(
            id_dieta=9999,
            id_cliente=1,
            id_profissional=1,
            nome="Dieta Inexistente",
            descricao="desc",
            data_inicio=date(2025, 1, 1),
            data_fim=date(2025, 1, 31),
            ativo=True,
            especificacoes="",
            tipo_dieta="Teste"
        )

        resultado = dieta_repo.alterar_dieta(dieta_fake)
        assert resultado is False, "Alterar dieta inexistente deveria retornar False"

    def test_excluir_dieta_inexistente(self, test_db):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        dieta_repo.criar_tabela_dieta()
        resultado = dieta_repo.excluir_dieta(9999)
        assert resultado is False, "Excluir dieta inexistente deveria retornar False"
