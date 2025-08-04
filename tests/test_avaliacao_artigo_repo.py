from data.repo.avaliacao_artigo_repo import *
from data.repo.usuario_repo import criar_tabela_usuario, inserir_usuario
from data.repo.profissional_repo import criar_tabela_profissional, inserir_profissional
from data.repo.artigo_repo import criar_tabela_artigo, inserir_artigo
from data.sql.avaliacao_artigo_sql import *

class Test_avaliacao_artigo_repo:

    def test_criar_tabela_avaliacao_artigo(self, test_db):
        resultado = criar_tabela_avaliacao_artigo()
        assert resultado is True

    def test_inserir_avaliacao_artigo(self, test_db, usuario_exemplo, profissional_exemplo, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_avaliacao_artigo()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_prof = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_prof
        id_artigo = inserir_artigo(artigo_exemplo)

        avaliacao = AvaliacaoArtigo(
            id_avaliacao=0,
            id_artigo=id_artigo,
            id_usuario=id_usuario,
            nota=4.0,
            Data_avaliacao=date.today(),
            Ativo=True
        )

        id_avaliacao = inserir_avaliacao_artigo(avaliacao)
        assert isinstance(id_avaliacao, int)

        resultado = obter_avaliacao_artigo_por_id(id_avaliacao)
        assert resultado is not None
        assert resultado.id_avaliacao == id_avaliacao
        assert resultado.id_usuario == id_usuario
        assert resultado.id_artigo == id_artigo
        assert resultado.nota == 4.0

        from datetime import datetime
        data_convertida = datetime.strptime(resultado.Data_avaliacao, "%Y-%m-%d").date()
        assert data_convertida == date.today(), "A data de avaliação não corresponde à data atual"


    def test_alterar_avaliacao_artigo(self, test_db, usuario_exemplo, profissional_exemplo, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_avaliacao_artigo()

        id_usuario = inserir_usuario(usuario_exemplo)
        usuario_exemplo.id = id_usuario 
        id_prof = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_prof
        id_artigo = inserir_artigo(artigo_exemplo)
        artigo_exemplo.id_artigo = id_artigo


        avaliacao = AvaliacaoArtigo(0, id_artigo, id_usuario, 3.0, date.today(), True)
        id_avaliacao = inserir_avaliacao_artigo(avaliacao)

        avaliacao_editada = obter_avaliacao_artigo_por_id(id_avaliacao)
        avaliacao_editada.nota = 5.0
        avaliacao_editada.Ativo = False

        sucesso = alterar_avaliacao_artigo(avaliacao_editada)
        assert sucesso is True

        atualizado = obter_avaliacao_artigo_por_id(id_avaliacao)
        assert atualizado.nota == 5.0
        assert atualizado.Ativo is False
        assert atualizado.id_usuario == usuario_exemplo.id
        
        from datetime import datetime
        data_convertida = datetime.strptime(atualizado.Data_avaliacao, "%Y-%m-%d").date()
        assert data_convertida == date.today(), "A data de avaliação não corresponde à data atual"
        assert atualizado.id_artigo == artigo_exemplo.id_artigo



    def test_excluir_avaliacao_artigo(self, test_db, avaliacao_artigo_exemplo, usuario_exemplo, profissional_exemplo, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_avaliacao_artigo()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_prof = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_prof
        id_artigo = inserir_artigo(artigo_exemplo)

        avaliacao = AvaliacaoArtigo(0, id_artigo, id_usuario, 4.2, date.today(), True)
        id_avaliacao = inserir_avaliacao_artigo(avaliacao)

        sucesso = excluir_avaliacao_artigo(id_avaliacao)
        assert sucesso is True

        resultado = obter_avaliacao_artigo_por_id(id_avaliacao)
        assert resultado is None

    def test_obter_avaliacoes_por_artigo(self, test_db, usuario_exemplo, profissional_exemplo, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_avaliacao_artigo()

        id_usuario = inserir_usuario(usuario_exemplo)
        id_prof = inserir_profissional(profissional_exemplo)
        artigo_exemplo.id_profissional = id_prof
        id_artigo = inserir_artigo(artigo_exemplo)

        for nota in [3.5, 4.0, 4.5]:
            inserir_avaliacao_artigo(AvaliacaoArtigo(0, id_artigo, id_usuario, nota, date.today(), True))

        avaliacoes = obter_avaliacoes_por_artigo(id_artigo)
        assert len(avaliacoes) == 3
        assert all(a.id_artigo == id_artigo for a in avaliacoes)

    def test_excluir_avaliacoes_artigos_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_avaliacao_artigo()
        resultado = excluir_avaliacao_artigo(999)
        assert resultado is False, "Excluir um salário inexistente deveria retornar False"

    def test_obter_avaliacao_artigo_por_id_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        criar_tabela_avaliacao_artigo()
        salario = obter_avaliacao_artigo_por_id(999)
        assert salario is None, "Deveria retornar None ao buscar um salário inexistente"
