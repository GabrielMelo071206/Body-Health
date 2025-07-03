CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS planos (
    id_plano INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    tipo_plano TEXT NOT NULL,
    valor REAL NOT NULL,
    duracao INTEGER NOT NULL,
    data_inicio TEXT NOT NULL,
    data_fim TEXT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO planos (id_cliente, tipo_plano, valor, duracao, data_inicio, data_fim, ativo)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE planos
SET id_cliente=?, tipo_plano=?, valor=?, duracao=?, data_inicio=?, data_fim=?, ativo=?
WHERE id_plano=?
"""

EXCLUIR = """
DELETE FROM planos
WHERE id_plano=?
"""

OBTER_POR_ID = """
SELECT 
    id_plano, id_cliente, tipo_plano, valor, duracao, data_inicio, data_fim, ativo
FROM planos
WHERE id_plano=?
"""

OBTER_TODOS = """
SELECT 
    id_plano, id_cliente, tipo_plano, valor, duracao, data_inicio, data_fim, ativo
FROM planos
ORDER BY data_inicio DESC
"""

OBTER_POR_CLIENTE = """
SELECT 
    id_plano, id_cliente, tipo_plano, valor, duracao, data_inicio, data_fim, ativo
FROM planos
WHERE id_cliente=?
ORDER BY data_inicio DESC
"""

OBTER_PLANOS_ATIVOS = """
SELECT 
    id_plano, id_cliente, tipo_plano, valor, duracao, data_inicio, data_fim, ativo
FROM planos
WHERE ativo=1
ORDER BY data_inicio DESC
"""

DESATIVAR_PLANO = """
UPDATE planos
SET ativo=0
WHERE id_plano=?
"""

ATIVAR_PLANO = """
UPDATE planos
SET ativo=1
WHERE id_plano=?
"""