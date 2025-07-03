import sys
import os
from datetime import date
from data.repo.plano_repo import *
from data.models.plano_model import *
from data.sql.plano_sql import *
from data.repo.usuario_repo import *
from data.repo.cliente_repo import *
from data.models.cliente_model import Cliente


class TestPlanoRepo:
    def test_criar_tabela_plano(self, test_db):
        resultado = criar_tabela_plano()
        assert resultado == True, "A tabela de planos não foi criada corretamente."

    def test_inserir_plano(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()
        
        # Criar um cliente primeiro
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)
        
        # Criar um plano
        plano_teste = Plano(0, id_cliente, "mensal", 49.90, 30, date(2024, 1, 1), date(2024, 1, 31), True)
        id_plano_db = inserir_plano(plano_teste)
        plano_db = obter_plano_por_id(id_plano_db)
        
        assert plano_db is not None
        assert plano_db.id_plano == 1
        assert plano_db.id_cliente == id_cliente
        assert plano_db.tipo_plano == "mensal"
        assert plano_db.valor == 49.90
        assert plano_db.duracao == 30
        assert plano_db.data_inicio == date(2024, 1, 1)
        assert plano_db.data_fim == date(2024, 1, 31)
        assert plano_db.ativo == True

    def test_obter_plano_por_id_existente(self, test_db, plano_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()
        
        # Criar cliente para o plano
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)
        plano_exemplo.id_cliente = id_cliente
        
        id_plano_inserido = inserir_plano(plano_exemplo)
        plano_db = obter_plano_por_id(id_plano_inserido)
        
        assert plano_db is not None
        assert plano_db.id_plano == id_plano_inserido
        assert plano_db.id_cliente == id_cliente
        assert plano_db.tipo_plano == plano_exemplo.tipo_plano

    def test_obter_plano_por_id_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()
        
        plano_db = obter_plano_por_id(999)
        assert plano_db is None

    def test_excluir_plano_existente(self, test_db, plano_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()
        
        # Criar cliente para o plano
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)
        plano_exemplo.id_cliente = id_cliente
        
        id_plano_inserido = inserir_plano(plano_exemplo)
        resultado = excluir_plano(id_plano_inserido)
        
        assert resultado == True
        plano_excluido = obter_plano_por_id(id_plano_inserido)
        assert plano_excluido is None

    def test_excluir_plano_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()
        
        resultado = excluir_plano(999)
        assert resultado == False

    def test_alterar_plano_existente(self, test_db, plano_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Arrange
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)
        plano_exemplo.id_cliente = id_cliente
        
        id_plano = inserir_plano(plano_exemplo)
        plano_para_alterar = obter_plano_por_id(id_plano)

        # Act
        plano_para_alterar.tipo_plano = "anual"
        plano_para_alterar.valor = 499.90
        plano_para_alterar.duracao = 365
        resultado = alterar_plano(plano_para_alterar)
        plano_alterado_db = obter_plano_por_id(id_plano)

        # Assert
        assert resultado is True, "A operação de alterar deveria retornar True"
        assert plano_alterado_db.tipo_plano == "anual", "O tipo de plano não foi alterado corretamente"
        assert plano_alterado_db.valor == 499.90, "O valor não foi alterado corretamente"
        assert plano_alterado_db.duracao == 365, "A duração não foi alterada corretamente"

    def test_alterar_plano_inexistente(self, test_db, plano_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Arrange
        plano_exemplo.id_plano = 999  # Um ID que não existe

        # Act
        resultado = alterar_plano(plano_exemplo)

        # Assert
        assert resultado is False, "A tentativa de alterar um plano inexistente deveria retornar False"

    def test_obter_planos_por_cliente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Criar cliente
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)

        # Criar dois planos para o cliente
        plano1 = Plano(0, id_cliente, "mensal", 49.90, 30, date(2024, 1, 1), date(2024, 1, 31), True)
        plano2 = Plano(0, id_cliente, "anual", 499.90, 365, date(2024, 2, 1), date(2025, 1, 31), True)
        
        inserir_plano(plano1)
        inserir_plano(plano2)

        # Act
        planos_cliente = obter_planos_por_cliente(id_cliente)

        # Assert
        assert len(planos_cliente) == 2, "Deveria haver 2 planos para o cliente"
        assert all(plano.id_cliente == id_cliente for plano in planos_cliente), "Todos os planos devem pertencer ao cliente"

    def test_obter_planos_ativos(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Criar cliente
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)

        # Criar planos (um ativo e um inativo)
        plano_ativo = Plano(0, id_cliente, "mensal", 49.90, 30, date(2024, 1, 1), date(2024, 1, 31), True)
        plano_inativo = Plano(0, id_cliente, "anual", 499.90, 365, date(2024, 2, 1), date(2025, 1, 31), False)
        
        inserir_plano(plano_ativo)
        inserir_plano(plano_inativo)

        # Act
        planos_ativos = obter_planos_ativos()

        # Assert
        assert len(planos_ativos) == 1, "Deveria haver apenas 1 plano ativo"
        assert planos_ativos[0].ativo == True, "O plano retornado deve estar ativo"
        assert planos_ativos[0].tipo_plano == "mensal", "O plano ativo deve ser o mensal"

    def test_desativar_plano_existente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Criar cliente e plano
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)
        
        plano_teste = Plano(0, id_cliente, "mensal", 49.90, 30, date(2024, 1, 1), date(2024, 1, 31), True)
        id_plano = inserir_plano(plano_teste)

        # Act
        resultado = desativar_plano(id_plano)
        plano_desativado = obter_plano_por_id(id_plano)

        # Assert
        assert resultado is True, "A desativação deveria retornar True"
        assert plano_desativado.ativo == False, "O plano deveria estar inativo"

    def test_desativar_plano_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Act
        resultado = desativar_plano(999)

        # Assert
        assert resultado is False, "A desativação de um plano inexistente deveria retornar False"

    def test_ativar_plano_existente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Criar cliente e plano inativo
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)
        
        plano_teste = Plano(0, id_cliente, "mensal", 49.90, 30, date(2024, 1, 1), date(2024, 1, 31), False)
        id_plano = inserir_plano(plano_teste)

        # Act
        resultado = ativar_plano(id_plano)
        plano_ativado = obter_plano_por_id(id_plano)

        # Assert
        assert resultado is True, "A ativação deveria retornar True"
        assert plano_ativado.ativo == True, "O plano deveria estar ativo"

    def test_ativar_plano_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Act
        resultado = ativar_plano(999)

        # Assert
        assert resultado is False, "A ativação de um plano inexistente deveria retornar False"

    def test_obter_todos_planos(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()

        # Criar cliente
        cliente_teste = Cliente(0, "Cliente Teste", "cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente", tipo_conta="gratuita")
        id_cliente = inserir_cliente(cliente_teste)

        # Criar múltiplos planos
        plano1 = Plano(0, id_cliente, "mensal", 49.90, 30, date(2024, 1, 1), date(2024, 1, 31), True)
        plano2 = Plano(0, id_cliente, "anual", 499.90, 365, date(2024, 2, 1), date(2025, 1, 31), False)
        plano3 = Plano(0, id_cliente, "semanal", 19.90, 7, date(2024, 3, 1), date(2024, 3, 7), True)
        
        inserir_plano(plano1)
        inserir_plano(plano2)
        inserir_plano(plano3)

        # Act
        todos_planos = obter_todos_planos()

        # Assert
        assert len(todos_planos) == 3, "Deveria haver 3 planos no total"
        tipos_plano = [plano.tipo_plano for plano in todos_planos]
        assert "mensal" in tipos_plano, "Deveria conter plano mensal"
        assert "anual" in tipos_plano, "Deveria conter plano anual"
        assert "semanal" in tipos_plano, "Deveria conter plano semanal"