from datetime import datetime, date
import pytest
import os
import sys
import tempfile
import sqlite3
import gc
import time
from contextlib import closing

# Imports dos seus modelos
from data.models.cliente_model import *
from data.models.usuario_model import *
from data.repo.usuario_repo import *
from data.models.profissional_model import *
from data.repo.profissional_repo import *
from data.models.administrador_model import *
from data.repo.administrador_repo import *
from data.models.plano_model import *
from data.repo.plano_repo import *
from data.models.treino_model import *
from data.repo.treino_repo import *
from data.models.artigo_model import *
from data.models.salario_model import Salario
from data.models.denuncia_model import Denuncia
from data.models.avaliacao_artigo_model import AvaliacaoArtigo
from data.models.visualizacao_artigo_model import VisualizacaoArtigo
from data.models.assinatura_model import *
from data.models.dieta_model import Dieta

# Configuração do ambiente de teste
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def _safe_remove_db_file(db_path):
    """
    Remove o arquivo de banco de dados de forma segura,
    com múltiplas tentativas para lidar com locks do Windows.
    """
    if not os.path.exists(db_path):
        return
    
    max_attempts = 10
    wait_time = 0.1
    
    for attempt in range(max_attempts):
        try:
            # Tenta conectar e fechar explicitamente para liberar locks
            with closing(sqlite3.connect(db_path)) as conn:
                pass
            
            # Força garbage collection
            gc.collect()
            
            # Tenta remover o arquivo
            os.unlink(db_path)
            return
            
        except PermissionError:
            if attempt < max_attempts - 1:
                time.sleep(wait_time)
                wait_time *= 1.2  # Aumenta o tempo de espera progressivamente
                gc.collect()
            else:
                print(f"Warning: Não foi possível deletar {db_path} após {max_attempts} tentativas")
        except Exception as e:
            print(f"Warning: Erro inesperado ao deletar {db_path}: {e}")
            return


@pytest.fixture
def test_db():
    """
    Fixture que cria um banco de dados SQLite temporário para testes
    e garante a limpeza adequada dos recursos no Windows.
    """
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['TEST_DATABASE_PATH'] = db_path
    
    try:
        yield db_path
    finally:
        # Força garbage collection para fechar conexões não referenciadas
        gc.collect()
        
        # Fecha o file descriptor original
        try:
            os.close(db_fd)
        except Exception:
            pass
        
        # Aguarda um momento para que o SO libere recursos
        time.sleep(0.05)
        
        # Remove o arquivo de forma segura
        _safe_remove_db_file(db_path)


# Suas fixtures existentes
@pytest.fixture
def usuario_exemplo() -> Usuario:
    """Objeto padrão de usuário para uso em testes."""
    return Usuario(
        id=0,
        nome="Usuario Exemplo",
        email="exemplo@teste.com",
        senha_hash="senha_super_segura_123",
        data_nascimento="2000-01-15",
        sexo="F",
        tipo_usuario="cliente"
    )


@pytest.fixture
def nutricionista_exemplo() -> Profissional:    
    return Profissional(
        id=0,
        nome="Profissional Exemplo",
        email="profissional@teste.com",
        senha_hash="senha_super_segura_123",
        data_nascimento="1990-05-15",
        sexo="M",
        tipo_usuario="nutricionista",
        ativo=True,
        ano_formacao=2015,
        registro_profissional="123456-G/DF"
    )


@pytest.fixture
def administrador_exemplo() -> Administrador:
    """Objeto padrão de administrador para uso em testes."""
    return Administrador(
        id=0,
        nome="Usuario Exemplo",
        email="exemplo@teste.com",
        senha_hash="senha_super_segura_123",
        data_nascimento="2000-01-15",
        sexo="F",
        tipo_usuario="cliente",
        master=True
    )


@pytest.fixture
def cliente_exemplo() -> Cliente:
    """Objeto padrão de cliente para uso em testes."""
    return Cliente(
        id=0,
        nome="Usuario Exemplo",
        email="exemplo@teste.com",
        senha_hash="senha_super_segura_123",
        data_nascimento="2000-01-15",
        sexo="F",
        tipo_usuario="cliente",
        tipo_conta="padrão"
    )


@pytest.fixture
def plano_exemplo() -> Plano:
    """Objeto padrão de plano para uso em testes."""
    return Plano(
        id_plano=0,
        id_cliente=1,  # Será substituído nos testes conforme necessário
        tipo_plano="mensal",
        valor=49.90,
        duracao=30,
        data_inicio=date(2024, 1, 1),
        data_fim=date(2024, 1, 31),
        ativo=True
    )


@pytest.fixture
def dieta_exemplo(cliente_exemplo, nutricionista_exemplo):
    """Fixture para criar um objeto Dieta de exemplo."""
    return Dieta(
        id_dieta=0,
        id_cliente=cliente_exemplo.id,
        id_profissional=nutricionista_exemplo.id,
        nome="Dieta Low Carb",
        descricao="Plano alimentar com baixo consumo de carboidratos.",
        data_inicio=date.today(),
        data_fim=date.today().replace(year=date.today().year + 1),
        ativo=True,
        especificacoes="Sem glúten, sem lactose.",
        tipo_dieta="Low Carb"
    )


@pytest.fixture
def treino_exemplo(cliente_exemplo, nutricionista_exemplo):
    return Treino(
        id_treino=0,
        id_cliente=cliente_exemplo.id,
        id_profissional=nutricionista_exemplo.id,
        nome="Treino Exemplo",
        descricao="Treino básico para exemplo.",
        data_inicio=date.today(),
        data_fim=date.today().replace(year=date.today().year + 1),
        ativo=True,
        especificacoes="Nenhuma especificação especial.",
        tipo_treino="Hipertrofia",
        visibilidade="Privado"
    )


@pytest.fixture
def profissional_exemplo() -> Profissional:
    return Profissional(
        id=0,
        nome="Profissional Exemplo",
        email="profissional@teste.com",
        senha_hash="senha_segura",
        data_nascimento="1990-06-20",
        sexo="M",
        tipo_usuario="educador_fisico",
        ativo=True,
        ano_formacao=2014,
        registro_profissional="EDU123456-G/SP"
    )


@pytest.fixture
def artigo_exemplo(profissional_exemplo):
    """Fixture para artigo de exemplo."""
    return Artigo(
        id_artigo=0,
        id_profissional=profissional_exemplo.id,
        titulo="Importância da Hidratação",
        conteudo="Beber água é essencial para manter o corpo funcionando corretamente.",
        data_publicacao=date.today(),
        visualizacoes=0,
        ativo=True,
        avaliacao=1
    )


@pytest.fixture
def salario_exemplo(profissional_exemplo) -> Salario:
    return Salario(
        id_salario=0,
        id_profissional=profissional_exemplo.id,
        mes_referencia=6,
        ano_referencia=2025,
        total_visualizacoes=120,
        visualizacoes_validas=100,
        valor_por_visualizacao=0.02,
        valor_total=2.00,
        data_calculo=date.today(),
        status_pagamento="pendente",
        data_pagamento=None,
        observacoes="Pagamento em análise",
        ativo=True
    )


@pytest.fixture
def denuncia_exemplo(usuario_exemplo, profissional_exemplo, administrador_exemplo) -> Denuncia:
    """Retorna uma denúncia de exemplo entre dois usuários fictícios."""
    return Denuncia(
        id_denuncia=0,
        id_denunciante=usuario_exemplo.id,
        id_denunciado=profissional_exemplo.id,
        tipo_denunciante="cliente",
        tipo_denunciado="nutricionista",
        motivo="Conteúdo impróprio",
        descricao="O profissional compartilhou conteúdo inadequado no artigo.",
        data_denuncia=str(datetime.now()),
        status="pendente",
        id_admin_avaliador=administrador_exemplo.id,
        data_avaliacao=str(datetime.now()),
        observacoes_admin="Aguardando análise",
        ativo=True
    )


@pytest.fixture
def avaliacao_artigo_exemplo(usuario_exemplo, artigo_exemplo) -> AvaliacaoArtigo:
    """Fixture para uma avaliação de artigo feita por um usuário."""
    return AvaliacaoArtigo(
        id_avaliacao=0,
        id_artigo=artigo_exemplo.id_artigo,
        id_usuario=usuario_exemplo.id,
        nota=4.5,
        Data_avaliacao=date.today(),
        Ativo=True
    )


@pytest.fixture
def visualizacao_artigo_exemplo(usuario_exemplo, artigo_exemplo) -> VisualizacaoArtigo:
    """Fixture para uma visualização de artigo feita por um usuário."""
    data_visualizacao = date.today()
    return VisualizacaoArtigo(
        id_visualizacao=0,
        id_artigo=artigo_exemplo.id_artigo,
        id_usuario=usuario_exemplo.id,
        Data_visualizacao=data_visualizacao,
        mes_referencia=data_visualizacao.month,
        ano_referencia=data_visualizacao.year,
        Ativo=True
    )


@pytest.fixture
def assinatura_exemplo(cliente_exemplo, plano_exemplo) -> Assinaturas:
    """Objeto padrão de assinatura para uso em testes."""
    return Assinaturas(
        id_assinatura=0,
        id_cliente=cliente_exemplo.id,
        id_plano=plano_exemplo.id_plano,
        data_inicio=date(2024, 1, 1),
        data_fim=date(2024, 1, 31),
        status="ativa",
        valor_pago=49.90,
        ativo=True
    )