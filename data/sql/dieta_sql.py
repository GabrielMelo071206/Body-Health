CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS dieta (
    id_dieta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_profissional INTEGER NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    especificacoes TEXT,
    tipo_dieta TEXT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_profissional) REFERENCES profissional(id_profissional) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO dieta (
    id_cliente, id_profissional, nome, descricao,
    data_inicio, data_fim, ativo, especificacoes, tipo_dieta
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE dieta
SET
    id_cliente = ?,
    id_profissional = ?,
    nome = ?,
    descricao = ?,
    data_inicio = ?,
    data_fim = ?,
    ativo = ?,
    especificacoes = ?,
    tipo_dieta = ?
WHERE id_dieta = ?
"""

EXCLUIR = """
DELETE FROM dieta
WHERE id_dieta = ?
"""

OBTER_POR_ID = """
SELECT
    d.id_dieta,
    d.id_cliente,
    d.id_profissional,
    d.nome,
    d.descricao,
    d.data_inicio,
    d.data_fim,
    d.ativo,
    d.especificacoes,
    d.tipo_dieta,
    u.nome AS nome_cliente,
    p.registro_profissional
FROM
    dieta d
INNER JOIN cliente c ON d.id_cliente = c.id_cliente
INNER JOIN usuario u ON c.id_cliente = u.id
INNER JOIN profissional p ON d.id_profissional = p.id_profissional
WHERE
    d.id_dieta = ?
"""

OBTER_TODOS = """
SELECT
    d.id_dieta,
    d.id_cliente,
    d.id_profissional,
    d.nome,
    d.descricao,
    d.data_inicio,
    d.data_fim,
    d.ativo,
    d.especificacoes,
    d.tipo_dieta,
    u.nome AS nome_cliente,
    p.registro_profissional
FROM
    dieta d
INNER JOIN cliente c ON d.id_cliente = c.id_cliente
INNER JOIN usuario u ON c.id_cliente = u.id
INNER JOIN profissional p ON d.id_profissional = p.id_profissional
ORDER BY
    d.data_inicio DESC
"""
OBTER_POR_CLIENTE = """
SELECT
    d.id_dieta,
    d.id_cliente,
    d.id_profissional,
    d.nome,
    d.descricao,
    d.data_inicio,
    d.data_fim,
    d.ativo,
    d.especificacoes,
    d.tipo_dieta,
    u.nome AS nome_cliente,
    p.registro_profissional
FROM
    dieta d
INNER JOIN cliente c ON d.id_cliente = c.id_cliente
INNER JOIN usuario u ON c.id_cliente = u.id
INNER JOIN profissional p ON d.id_profissional = p.id_profissional
WHERE
    d.id_cliente = ?
ORDER BY
    d.data_inicio DESC
"""

OBTER_POR_PROFISSIONAL = """    
SELECT
    d.id_dieta,
    d.id_cliente,
    d.id_profissional,
    d.nome,
    d.descricao,
    d.data_inicio,
    d.data_fim,
    d.ativo,
    d.especificacoes,
    d.tipo_dieta,
    u.nome AS nome_cliente,
    p.registro_profissional
FROM
    dieta d
INNER JOIN cliente c ON d.id_cliente = c.id_cliente
INNER JOIN usuario u ON c.id_cliente = u.id
INNER JOIN profissional p ON d.id_profissional = p.id_profissional
WHERE
    d.id_profissional = ?
ORDER BY
    d.data_inicio DESC
"""
