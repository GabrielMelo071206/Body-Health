import pytest
from data.repo.assinatura_repo import *
from data.repo.cliente_repo import *
from data.repo.plano_repo import *
from data.repo.usuario_repo import *
from data.models.assinatura_model import Assinaturas
from datetime import date

def criar_tabela_profissional():
    from data.repo.profissional_repo import criar_tabela_profissional as criar_prof
    criar_prof()


class TestAssinaturaRepo:

    def test_criar_tabela_assinatura(self, test_db):
        resultado = criar_tabela_assinatura()
        assert resultado is True, "A tabela de assinatura não foi criada corretamente."

    def test_inserir_assinatura(self, test_db, cliente_exemplo, plano_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_profissional()
        criar_tabela_plano()
        criar_tabela_assinatura()

        id_cliente = inserir_cliente(cliente_exemplo)
        plano_exemplo.id_cliente = id_cliente
        id_plano = inserir_plano(plano_exemplo)

        assinatura = Assinaturas(
            id_assinatura=0,
            id_cliente=id_cliente,
            id_plano=id_plano,
            data_inicio=date(2024, 1, 1),
            data_fim=date(2024, 1, 31),
            status="ativa",
            valor_pago=49.90,
            ativo=True
        )

        id_assinatura = inserir_assinatura(assinatura)
        assinatura_db = obter_assinatura_por_id(id_assinatura)

        assert assinatura_db is not None
        assert assinatura_db.id_assinatura == id_assinatura
        assert assinatura_db.id_cliente == id_cliente
        assert assinatura_db.id_plano == id_plano
        assert assinatura_db.status == "ativa"
        assert assinatura_db.valor_pago == 49.90
        assert assinatura_db.data_inicio == date(2024, 1, 1)
        assert assinatura_db.data_fim == date(2024, 1, 31)
        assert assinatura_db.ativo is True


    def test_alterar_assinatura(self, test_db, cliente_exemplo, plano_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()
        criar_tabela_assinatura()

        id_cliente = inserir_cliente(cliente_exemplo)
        plano_exemplo.id_cliente = id_cliente
        id_plano = inserir_plano(plano_exemplo)

        assinatura = Assinaturas(
            id_assinatura=0,
            id_cliente=id_cliente,
            id_plano=id_plano,
            data_inicio=date(2024, 1, 1),
            data_fim=date(2024, 1, 31),
            status="ativa",
            valor_pago=49.90,
            ativo=True
        )

        id_assinatura = inserir_assinatura(assinatura)

        assinatura.id_assinatura = id_assinatura
        assinatura.status = "cancelada"
        assinatura.valor_pago = 0.0
        resultado = alterar_assinatura(assinatura)
        
        assinatura_alterada = obter_assinatura_por_id(id_assinatura)

        assert resultado is True
        assert assinatura_alterada.status == "cancelada"
        assert assinatura_alterada.valor_pago == 0.0

    def test_excluir_assinatura(self, test_db, cliente_exemplo, plano_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()
        criar_tabela_assinatura()

        id_cliente = inserir_cliente(cliente_exemplo)
        plano_exemplo.id_cliente = id_cliente
        id_plano = inserir_plano(plano_exemplo)

        assinatura = Assinaturas(
            id_assinatura=0,
            id_cliente=id_cliente,
            id_plano=id_plano,
            data_inicio=date(2024, 1, 1),
            data_fim=date(2024, 1, 31),
            status="ativa",
            valor_pago=49.90,
            ativo=True
        )

        id_assinatura = inserir_assinatura(assinatura)
        resultado = excluir_assinatura(id_assinatura)
        assinatura_excluida = obter_assinatura_por_id(id_assinatura)

        assert resultado is True
        assert assinatura_excluida is None

    def test_obter_assinaturas_por_cliente(self, test_db, cliente_exemplo, plano_exemplo):
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_plano()
        criar_tabela_assinatura()

        id_cliente = inserir_cliente(cliente_exemplo)
        plano_exemplo.id_cliente = id_cliente
        id_plano = inserir_plano(plano_exemplo)

        assinatura = Assinaturas(
            id_assinatura=0,
            id_cliente=id_cliente,
            id_plano=id_plano,
            data_inicio=date(2024, 1, 1),
            data_fim=date(2024, 1, 31),
            status="ativa",
            valor_pago=49.90,
            ativo=True
        )

        inserir_assinatura(assinatura)

        assinaturas = obter_assinaturas_por_cliente(id_cliente)

        assert isinstance(assinaturas, list)
        assert len(assinaturas) >= 1
        assert assinaturas[0].id_cliente == id_cliente

    def test_obter_assinatura_por_id_inexistente(self, test_db):
        criar_tabela_assinatura()
        assinatura = obter_assinatura_por_id(9999)
        assert assinatura is None, "Esperava None ao buscar uma assinatura inexistente"

    def test_excluir_assinatura_inexistente(self, test_db):
        criar_tabela_assinatura()
        resultado = excluir_assinatura(9999)
        assert resultado is False, "Esperava False ao tentar excluir assinatura inexistente"

    def test_alterar_assinatura_inexistente(self, test_db, assinatura_exemplo):
        criar_tabela_assinatura()
        assinatura_exemplo.id_assinatura = 9999
        resultado = alterar_assinatura(assinatura_exemplo)
        assert resultado is False, "A tentativa de alterar assinatura inexistente deveria retornar False"
