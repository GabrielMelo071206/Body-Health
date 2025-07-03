CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS treino (
    id_treino INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_profissional INTEGER NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    especificacoes TEXT,
    tipo_treino TEXT,
    visibilidade TEXT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_profissional) REFERENCES profissional(id_profissional) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO treino (
    id_cliente, id_profissional, nome, descricao,
    data_inicio, data_fim, ativo, especificacoes, tipo_treino, visibilidade
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE treino
SET
    id_cliente = ?,
    id_profissional = ?,
    nome = ?,
    descricao = ?,
    data_inicio = ?,
    data_fim = ?,
    ativo = ?,
    especificacoes = ?,
    tipo_treino = ?,
    visibilidade = ?
WHERE id_treino = ?
"""

EXCLUIR = """
DELETE FROM treino
WHERE id_treino = ?
"""

OBTER_POR_ID = """
SELECT
    t.id_treino,
    t.id_cliente,
    t.id_profissional,
    t.nome,
    t.descricao,
    t.data_inicio,
    t.data_fim,
    t.ativo,
    t.especificacoes,
    t.tipo_treino,
    t.visibilidade,
    u.nome AS nome_cliente,
    p.registro_profissional
FROM
    treino t
INNER JOIN cliente c ON t.id_cliente = c.id_cliente
INNER JOIN usuario u ON c.id_cliente = u.id
INNER JOIN profissional p ON t.id_profissional = p.id_profissional
WHERE
    t.id_treino = ?
"""

OBTER_TODOS = """
SELECT
    t.id_treino
    ,
    t.id_cliente,
    t.id_profissional,
    t.nome,
    t.descricao,
    t.data_inicio,
    t.data_fim,
    t.ativo,
    t.especificacoes,
    t.tipo_treino,
    t.visibilidade,
    u.nome AS nome_cliente,
    p.registro_profissional
FROM
    treino t
INNER JOIN cliente c ON t.id_cliente = c.id_cliente
INNER JOIN usuario u ON c.id_cliente = u.id
INNER JOIN profissional p ON t.id_profissional = p.id_profissional
ORDER BY
    t.data_inicio DESC
"""
OBTER_POR_CLIENTE = """
SELECT
    t.id_treino
    ,
    t.id_cliente,
    t.id_profissional,
    t.nome,
    t.descricao,
    t.data_inicio,
    t.data_fim,
    t.ativo,
    t.especificacoes,
    t.tipo_treino,
    t.visibilidade,
    u.nome AS nome_cliente,
    p.registro_profissional
FROM
    treino t
INNER JOIN cliente c ON t.id_cliente = c.id_cliente
INNER JOIN usuario u ON c.id_cliente = u.id
INNER JOIN profissional p ON t.id_profissional = p.id_profissional
WHERE
    t.id_cliente = ?
ORDER BY
    t.data_inicio DESC
"""

OBTER_POR_PROFISSIONAL = """    
SELECT
    t.id_treino
    ,
    t.id_cliente,
    t.id_profissional,
    t.nome,
    t.descricao,
    t.data_inicio,
    t.data_fim,
    t.ativo,
    t.especificacoes,
    t.tipo_treino,
    t.visibilidade,
    u.nome AS nome_cliente,
    p.registro_profissional
FROM
    treino t
INNER JOIN cliente c ON t.id_cliente = c.id_cliente
INNER JOIN usuario u ON c.id_cliente = u.id
INNER JOIN profissional p ON t.id_profissional = p.id_profissional
WHERE
    t.id_profissional = ?
ORDER BY
    t.data_inicio DESC
"""
