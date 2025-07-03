from data.repo import treino_repo, cliente_repo, profissional_repo, usuario_repo
from data.models.treino_model import *
from data.models.cliente_model import *
from data.models.profissional_model import *
from datetime import date


class TestTreinoRepo:

    def test_criar_tabela_treino(self, test_db):
        resultado = treino_repo.criar_tabela_treino()
        assert resultado is True, "A tabela treino não foi criada corretamente"

    def test_inserir_treino(self, test_db, cliente_exemplo, profissional_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_profissional = profissional_repo.inserir_profissional(profissional_exemplo)

        treino = Treino(
            id_treino=0,
            id_cliente=id_cliente,
            id_profissional=id_profissional,
            nome="Treino Teste",
            descricao="Descrição do treino teste",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 31),
            ativo=True,
            especificacoes="",
            tipo_treino="Hipertrofia",
            visibilidade="Privado"
        )

        id_treino = treino_repo.inserir_treino(treino)
        treino_db = treino_repo.obter_treino_por_id(id_treino)

        assert treino_db is not None
        assert treino_db.nome == "Treino Teste"
        assert treino_db.tipo_treino == "Hipertrofia"
        assert treino_db.ativo is True
        assert treino_db.visibilidade == "Privado"

    def test_obter_treinos_por_cliente(self, test_db, cliente_exemplo, profissional_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_profissional = profissional_repo.inserir_profissional(profissional_exemplo)

        treino = Treino(
            id_treino=0,
            id_cliente=id_cliente,
            id_profissional=id_profissional,
            nome="Treino Cliente",
            descricao="Descrição",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 10),
            ativo=True,
            especificacoes="",
            tipo_treino="Funcional",
            visibilidade="Publico"
        )

        treino_repo.inserir_treino(treino)
        treinos = treino_repo.obter_treinos_por_cliente(id_cliente)

        assert len(treinos) >= 1
        assert treinos[0].tipo_treino == "Funcional"
        assert treinos[0].visibilidade == "Publico"

    def test_obter_treinos_por_profissional(self, test_db, cliente_exemplo, profissional_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_profissional = profissional_repo.inserir_profissional(profissional_exemplo)

        treino = Treino(
            id_treino=0,
            id_cliente=id_cliente,
            id_profissional=id_profissional,
            nome="Treino Profissional",
            descricao="Descrição",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 10),
            ativo=True,
            especificacoes="",
            tipo_treino="Cardio",
            visibilidade="Profissional"
        )

        treino_repo.inserir_treino(treino)
        treinos = treino_repo.obter_treinos_por_profissional(id_profissional)

        assert len(treinos) >= 1
        assert treinos[0].tipo_treino == "Cardio"
        assert treinos[0].visibilidade == "Profissional"

    def test_alterar_treino(self, test_db, cliente_exemplo, profissional_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_profissional = profissional_repo.inserir_profissional(profissional_exemplo)

        treino = Treino(
            id_treino=0,
            id_cliente=id_cliente,
            id_profissional=id_profissional,
            nome="Treino Inicial",
            descricao="Descrição",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 10),
            ativo=True,
            especificacoes="",
            tipo_treino="Resistência",
            visibilidade="Privado"
        )

        id_treino = treino_repo.inserir_treino(treino)
        treino_editado = treino_repo.obter_treino_por_id(id_treino)
        treino_editado.nome = "Treino Alterado"
        treino_editado.tipo_treino = "Força"
        treino_editado.visibilidade = "Publico"

        resultado = treino_repo.alterar_treino(treino_editado)
        assert resultado is True

        treino_novo = treino_repo.obter_treino_por_id(id_treino)
        assert treino_novo.nome == "Treino Alterado"
        assert treino_novo.tipo_treino == "Força"
        assert treino_novo.visibilidade == "Publico"

    def test_excluir_treino(self, test_db, cliente_exemplo, profissional_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_profissional = profissional_repo.inserir_profissional(profissional_exemplo)

        treino = Treino(
            id_treino=0,
            id_cliente=id_cliente,
            id_profissional=id_profissional,
            nome="Treino a Excluir",
            descricao="Descrição",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 10),
            ativo=True,
            especificacoes="",
            tipo_treino="Alongamento",
            visibilidade="Privado"
        )

        id_treino = treino_repo.inserir_treino(treino)
        resultado = treino_repo.excluir_treino(id_treino)
        treino_excluido = treino_repo.obter_treino_por_id(id_treino)

        assert resultado is True
        assert treino_excluido is None

    # Testes para treinos inexistentes:

    def test_obter_treino_por_id_inexistente(self, test_db):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        treino = treino_repo.obter_treino_por_id(9999)
        assert treino is None, "Deveria retornar None para treino inexistente"

    def test_alterar_treino_inexistente(self, test_db, cliente_exemplo, profissional_exemplo):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        treino_fake = Treino(
            id_treino=9999,
            id_cliente=1,
            id_profissional=1,
            nome="Treino Inexistente",
            descricao="Descrição",
            data_inicio=date(2025, 1, 1),
            data_fim=date(2025, 1, 31),
            ativo=True,
            especificacoes="",
            tipo_treino="Teste",
            visibilidade="Privado"
        )

        resultado = treino_repo.alterar_treino(treino_fake)
        assert resultado is False, "Alterar treino inexistente deveria retornar False"

    def test_excluir_treino_inexistente(self, test_db):
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        resultado = treino_repo.excluir_treino(9999)
        assert resultado is False, "Excluir treino inexistente deveria retornar False"

    def test_obter_treino_por_id(self, test_db, cliente_exemplo, profissional_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        cliente_repo.criar_tabela_cliente()
        profissional_repo.criar_tabela_profissional()
        treino_repo.criar_tabela_treino()

        id_cliente = cliente_repo.inserir_cliente(cliente_exemplo)
        id_prof = profissional_repo.inserir_profissional(profissional_exemplo)

        treino = Treino(
            id_treino=0,
            id_cliente=id_cliente,
            id_profissional=id_prof,
            nome="Treino A",
            descricao="Descrição do Treino A",
            data_inicio=date(2025, 7, 1),
            data_fim=date(2025, 7, 31),
            ativo=True,
            especificacoes="Exercícios A e B",
            tipo_treino="Funcional",
            visibilidade="Privado"
        )

        id_treino = treino_repo.inserir_treino(treino)

        # Act
        treino_db = treino_repo.obter_treino_por_id(id_treino)

        # Assert
        assert treino_db is not None
        assert treino_db.id_treino == id_treino
        assert treino_db.nome == "Treino A"
        assert treino_db.tipo_treino == "Funcional"
        assert treino_db.visibilidade == "Privado"
