from data.repo.visualizacao_artigo_repo import *
from data.repo.usuario_repo import criar_tabela_usuario, inserir_usuario
from data.repo.profissional_repo import criar_tabela_profissional, inserir_profissional
from data.repo.artigo_repo import criar_tabela_artigo, inserir_artigo
from data.models.visualizacao_artigo_model import VisualizacaoArtigo
from datetime import date


class Test_visualizacao_artigo_repo:

    def test_criar_tabela_visualizacao_artigo(self, test_db):
        resultado = criar_tabela_visualizacao_artigo()
        assert resultado is True

    def test_inserir_visualizacao_artigo(self, test_db, usuario_exemplo, profissional_exemplo, artigo_exemplo):
    
    
    
    def obter_visualizacao_artigo_por_id(id_visualizacao: int) -> Optional[VisualizacaoArtigo]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(visualizacao_artigo_sql.OBTER_POR_ID, (id_visualizacao,))
            row = cursor.fetchone()
            if row is None:
                return None
            return VisualizacaoArtigo(
                id_visualizacao=row["id_visualizacao"],
                id_artigo=row["id_artigo"],
                id_usuario=row["id_usuario"],
                Data_visualizacao=row["data_visualizacao"],
                mes_referencia=row["mes_referencia"],
                ano_referencia=row["ano_referencia"],
                Ativo=bool(row["ativo"])
            )

    def test_alterar_visualizacao_artigo(self, test_db, usuario_exemplo, profissional_exemplo, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_visualizacao_artigo()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_profissional = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_profissional
        id_artigo = inserir_artigo(artigo_exemplo)

        # Inserção inicial
        visualizacao = VisualizacaoArtigo(
            id_visualizacao=0,
            id_artigo=id_artigo,
            id_usuario=id_usuario,
            Data_visualizacao=date.today(),
            mes_referencia=7,
            ano_referencia=2025,
            Ativo=True
        )
        id_visualizacao = inserir_visualizacao_artigo(visualizacao)
        assert isinstance(id_visualizacao, int)

        # Obter e editar
        visualizacao_editada = obter_visualizacao_artigo_por_id(id_visualizacao)
        assert visualizacao_editada is not None

        visualizacao_editada.mes_referencia = 8
        visualizacao_editada.ano_referencia = 2026
        visualizacao_editada.Ativo = False
        visualizacao_editada.id_visualizacao = id_visualizacao  # Necessário para a atualização
        visualizacao_editada.id_artigo = id_artigo  # Necessário para a atualização
        visualizacao_editada.id_usuario = id_usuario  # Necessário para a atualização
        visualizacao_editada.Data_visualizacao = date.today()  # Necessário para a atualização
        # Alterar
        sucesso = alterar_visualizacao_artigo(visualizacao_editada)
        assert sucesso is True

        # Validar atualização
        atualizado = obter_visualizacao_artigo_por_id(id_visualizacao)
        assert atualizado is not None
        assert atualizado.mes_referencia == 8
        assert atualizado.ano_referencia == 2026
        assert atualizado.Ativo is False
        assert atualizado.id_artigo == id_artigo
        assert atualizado.id_usuario == id_usuario
        assert atualizado.Data_visualizacao == date.today()
        assert atualizado.id_visualizacao == id_visualizacao, "ID da visualização alterada não confere"
        

    def test_excluir_visualizacao_artigo(self, test_db, visualizacao_artigo_exemplo, usuario_exemplo, profissional_exemplo, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_visualizacao_artigo()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_profissional = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_profissional
        id_artigo = inserir_artigo(artigo_exemplo)

        visualizacao = VisualizacaoArtigo(
            0, id_artigo, id_usuario, date.today(), 7, 2025, True
        )
        id_visualizacao = inserir_visualizacao_artigo(visualizacao)

        sucesso = excluir_visualizacao_artigo(id_visualizacao)
        assert sucesso is True

        resultado = obter_visualizacao_artigo_por_id(id_visualizacao)
        assert resultado is None

    def test_obter_visualizacoes_por_artigo(self, test_db, usuario_exemplo, profissional_exemplo, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_visualizacao_artigo()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_profissional = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_profissional
        id_artigo = inserir_artigo(artigo_exemplo)

        for _ in range(3):
            visualizacao = VisualizacaoArtigo(
                0, id_artigo, id_usuario, date.today(), 7, 2025, True
            )
            inserir_visualizacao_artigo(visualizacao)

        visualizacoes = obter_visualizacoes_por_artigo(id_artigo)
        assert len(visualizacoes) == 3
        assert all(visualizacao.id_artigo == id_artigo for visualizacao in visualizacoes)

    def test_obter_visualizacoes_por_mes_ano(self, test_db, usuario_exemplo, profissional_exemplo, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_visualizacao_artigo()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_profissional = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_profissional
        id_artigo = inserir_artigo(artigo_exemplo)

        for _ in range(2):
            visualizacao = VisualizacaoArtigo(
                0, id_artigo, id_usuario, date.today(), 7, 2025, True
            )
            inserir_visualizacao_artigo(visualizacao)

        visualizacao = VisualizacaoArtigo(
            0, id_artigo, id_usuario, date.today(), 6, 2025, True
        )
        inserir_visualizacao_artigo(visualizacao)

        julho = obter_visualizacoes_por_mes_ano(7, 2025)
        junho = obter_visualizacoes_por_mes_ano(6, 2025)

        assert len(julho) == 2
        assert len(junho) == 1

    def test_excluir_visualizacao_inexistente(self, test_db):
        criar_tabela_visualizacao_artigo()
        resultado = excluir_visualizacao_artigo(999)
        assert resultado is False

    def test_obter_visualizacao_por_id_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_visualizacao_artigo()
        resultado = obter_visualizacao_artigo_por_id(999)
        assert resultado is None

    def test_obter_visualizacoes_por_artigo_inexistente(self, test_db):
        criar_tabela_visualizacao_artigo()
        visualizacoes = obter_visualizacoes_por_artigo(999)
        assert visualizacoes == [] or len(visualizacoes) == 0

    def test_obter_visualizacoes_por_mes_ano_sem_registros(self, test_db):
        criar_tabela_visualizacao_artigo()
        visualizacoes = obter_visualizacoes_por_mes_ano(12, 2099)  # Mês e ano futuros
        assert visualizacoes == [] or len(visualizacoes) == 0

    def test_alterar_visualizacao_artigo_inexistente(self, test_db):
        criar_tabela_visualizacao_artigo()
        visualizacao = VisualizacaoArtigo(
            id_visualizacao=999,
            id_artigo=1,
            id_usuario=1,
            Data_visualizacao=date.today(),
            mes_referencia=7,
            ano_referencia=2025,
            Ativo=True
        )
        sucesso = alterar_visualizacao_artigo(visualizacao)
        assert sucesso is False

    def test_inserir_visualizacao_com_artigo_inexistente(self, test_db, usuario_exemplo):
        criar_tabela_usuario()
        criar_tabela_visualizacao_artigo()
        id_usuario = inserir_usuario(usuario_exemplo)

        visualizacao = VisualizacaoArtigo(
            id_visualizacao=0,
            id_artigo=999,  # artigo inexistente
            id_usuario=id_usuario,
            Data_visualizacao=date.today(),
            mes_referencia=7,
            ano_referencia=2025,
            Ativo=True
        )

        try:
            inserir_visualizacao_artigo(visualizacao)
            assert False, "Deveria lançar exceção por chave estrangeira (artigo inexistente)"
        except Exception:
            assert True

    def test_inserir_visualizacao_com_usuario_inexistente(self, test_db, artigo_exemplo, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_visualizacao_artigo()

        id_profissional = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_profissional
        id_artigo = inserir_artigo(artigo_exemplo)

        visualizacao = VisualizacaoArtigo(
            id_visualizacao=0,
            id_artigo=id_artigo,
            id_usuario=999,  # usuário inexistente
            Data_visualizacao=date.today(),
            mes_referencia=7,
            ano_referencia=2025,
            Ativo=True
        )

        try:
            inserir_visualizacao_artigo(visualizacao)
            assert False, "Deveria lançar exceção por chave estrangeira (usuário inexistente)"
        except Exception:
            assert True
