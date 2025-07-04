import pytest
from data.repo.artigo_repo import *
from data.repo.profissional_repo import *
from data.repo.usuario_repo import *
from data.models.artigo_model import Artigo

class TestArtigoRepo:
    def test_criar_tabela_artigo(self, test_db):
        resultado = criar_tabela_artigo()
        assert resultado == True, "A tabela de artigo não foi criada corretamente."

    def test_inserir_artigo(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()

        id_profissional = inserir_profissional(profissional_exemplo)

        artigo = Artigo(
            id_artigo=0,
            id_profissional=id_profissional,
            titulo="Exemplo de Artigo",
            conteudo="Conteúdo de teste para o artigo",
            data_publicacao="2025-07-01",
            visualizacoes=0,
            ativo=True,
            avaliacao=4.5
        )

        id_artigo = inserir_artigo(artigo)
        artigo_db = obter_artigo_por_id(id_artigo)

        assert artigo_db is not None
        assert artigo_db.id_artigo == id_artigo
        assert artigo_db.titulo == artigo.titulo
        assert artigo_db.conteudo == artigo.conteudo

    def test_alterar_artigo(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()

        id_profissional = inserir_profissional(profissional_exemplo)

        artigo = Artigo(
            id_artigo=0,
            id_profissional=id_profissional,
            titulo="Artigo Original",
            conteudo="Conteúdo original",
            data_publicacao="2025-07-01",
            visualizacoes=10,
            ativo=True,
            avaliacao=3.0
        )

        id_artigo = inserir_artigo(artigo)

        artigo.id_artigo = id_artigo
        artigo.titulo = "Artigo Alterado"
        artigo.conteudo = "Novo conteúdo"
        artigo.visualizacoes = 50
        artigo.avaliacao = 4.8
        resultado = alterar_artigo(artigo)

        artigo_alterado = obter_artigo_por_id(id_artigo)

        assert resultado is True
        assert artigo_alterado.titulo == "Artigo Alterado"
        assert artigo_alterado.conteudo == "Novo conteúdo"
        assert artigo_alterado.visualizacoes == 50
        assert artigo_alterado.avaliacao == 4.8

    def test_excluir_artigo(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()

        id_profissional = inserir_profissional(profissional_exemplo)

        artigo = Artigo(
            id_artigo=0,
            id_profissional=id_profissional,
            titulo="Artigo para Excluir",
            conteudo="Este artigo será excluído",
            data_publicacao="2025-07-01",
            visualizacoes=0,
            ativo=True,
            avaliacao=2.5
        )

        id_artigo = inserir_artigo(artigo)
        resultado = excluir_artigo(id_artigo)
        artigo_excluido = obter_artigo_por_id(id_artigo)

        assert resultado is True
        assert artigo_excluido is None

    def test_obter_artigos_por_profissional(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()

        id_profissional = inserir_profissional(profissional_exemplo)

        artigo1 = Artigo(0, id_profissional, "Artigo 1", "Texto 1", "2025-07-01", 10, True, 4.0)
        artigo2 = Artigo(0, id_profissional, "Artigo 2", "Texto 2", "2025-07-02", 5, True, 3.5)

        inserir_artigo(artigo1)
        inserir_artigo(artigo2)

        artigos = obter_artigos_por_profissional(id_profissional)

        assert len(artigos) >= 2
        titulos = [a.titulo for a in artigos]
        assert "Artigo 1" in titulos
        assert "Artigo 2" in titulos

    def test_obter_todos_artigos(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()

        id_profissional = inserir_profissional(profissional_exemplo)

        artigo = Artigo(0, id_profissional, "Artigo Global", "Texto global", "2025-07-01", 12, True, 4.7)
        inserir_artigo(artigo)

        artigos = obter_todos_artigos()

        assert any(a.titulo == "Artigo Global" for a in artigos)

    def test_obter_artigo_por_id_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        
        artigo = obter_artigo_por_id(9999)
        assert artigo is None, "Esperava None ao buscar um artigo inexistente"

    def test_excluir_artigo_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        
        resultado = excluir_artigo(9999)
        assert resultado is False, "Esperava False ao tentar excluir um artigo inexistente"

    def test_alterar_artigo_inexistente(self, test_db, artigo_exemplo):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()

        artigo_exemplo.id = 999

        resultado = alterar_artigo(artigo_exemplo)

        # Assert
        assert resultado is False, "A tentativa de alterar um cliente inexistente deveria retornar False"
    def test_obter_artigos_por_profissional_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_artigo()
        
        artigos = obter_artigos_por_profissional(9999)
        assert isinstance(artigos, list), "Esperava uma lista"
        assert len(artigos) == 0, "Esperava lista vazia ao buscar artigos de profissional inexistente"
