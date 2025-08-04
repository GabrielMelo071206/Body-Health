from datetime import datetime, time
import pytest
import os
import sys
import tempfile
from data.models.cliente_model import *
from data.models.usuario_model import *
from data.repo.usuario_repo import *
from data.models.profissional_model import *
from data.repo.profissional_repo import *
from data.models.administrador_model import *
from data.repo.administrador_repo import *
from data.repo.administrador_repo import *
from datetime import date
from data.models.plano_model import *
from data.repo.plano_repo import *
from data.models.treino_model import *
from data.repo.treino_repo import *
from data.models.artigo_model import *
from data.models.salario_model import Salario
from data.models.denuncia_model import Denuncia
from datetime import datetime
from data.models.avaliacao_artigo_model import AvaliacaoArtigo
from data.models.visualizacao_artigo_model import VisualizacaoArtigo
from data.models.assinatura_model import *  
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


# from data.repo.treino_repo import *


# Configuração do ambiente de teste
# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


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
    """Objeto padrão de usuário para uso em testes."""
    return Administrador(
        id=0,
        nome="Usuario Exemplo",
        email="exemplo@teste.com",
        senha_hash="senha_super_segura_123",
        data_nascimento="2000-01-15",
        sexo="F",
        tipo_usuario="cliente",
        master= True
    )

@pytest.fixture
def cliente_exemplo() -> Cliente:
    """Objeto padrão de usuário para uso em testes."""
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

# @pytest.fixture
# def educador_exemplo() -> EducadorFisico:
#     """Objeto de exemplo do tipo Educador Físico."""
#     return EducadorFisico(
#         id=0,
#         nome="Educador Físico Exemplo",
#         email="educador@teste.com",
#         senha_hash="senha_super_segura_123",
#         data_nascimento="1990-05-15",
#         sexo="M",
#         tipo_usuario="profissional",
#         tipo_profissional="educador_fisico",
#         status="ativo",
#         cref="123456-G/DF"
#     )

      
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

import pytest
from datetime import date
from data.models.dieta_model import Dieta

@pytest.fixture
def dieta_exemplo(cliente_exemplo, nutricionista_exemplo):
    """
    Fixture para criar um objeto Dieta de exemplo.
    Assume que cliente_exemplo e nutricionista_exemplo já existem e têm id definidos.
    """
    # Normalmente, o id será definido após inserção no banco, aqui colocamos 0 como placeholder
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
        tipo_usuario="educador_fisico",  # ✅ AGORA VÁLIDO
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

import pytest
from datetime import date
from data.models.salario_model import Salario

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
def denuncia_exemplo(usuario_exemplo, profissional_exemplo, administrador_exemplo)-> Denuncia:
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
        id_assinatura=0,                 # Id fictício, normalmente criado no banco
        id_cliente=cliente_exemplo.id,  # Usa fixture cliente_exemplo
        id_plano=plano_exemplo.id_plano, # Usa fixture plano_exemplo
        data_inicio=date(2024, 1, 1),
        data_fim=date(2024, 1, 31),
        status="ativa",
        valor_pago=49.90,
        ativo=True
    )