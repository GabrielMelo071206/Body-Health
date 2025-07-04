CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS artigo (
    id_artigo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profissional INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    data_publicacao DATE NOT NULL,
    visualizacoes INTEGER DEFAULT 0,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    avaliacao FLOAT DEFAULT 0.0,
    FOREIGN KEY (id_profissional) REFERENCES profissional(id_profissional) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO artigo (id_profissional, titulo, conteudo, data_publicacao, visualizacoes, ativo, avaliacao)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ALTERAR = """
UPDATE artigo
SET titulo = ?, conteudo = ?, data_publicacao = ?, visualizacoes = ?, ativo = ?, avaliacao = ?
WHERE id_artigo = ?;
"""

EXCLUIR = """
DELETE FROM artigo
WHERE id_artigo = ?;
"""

OBTER_POR_ID = """
SELECT 
    a.id_artigo,
    a.id_profissional,
    a.titulo,
    a.conteudo,
    a.data_publicacao,
    a.visualizacoes,
    a.ativo,
    a.avaliacao,
    u.nome AS nome_profissional,
    u.email AS email_profissional
FROM artigo a
INNER JOIN profissional p ON a.id_profissional = p.id_profissional
INNER JOIN usuario u ON p.id_profissional = u.id
WHERE a.id_artigo = ?;
"""

OBTER_TODOS = """
SELECT 
    a.id_artigo,
    a.id_profissional,
    a.titulo,
    a.conteudo,
    a.data_publicacao,
    a.visualizacoes,
    a.ativo,
    a.avaliacao,
    u.nome AS nome_profissional
FROM artigo a
INNER JOIN profissional p ON a.id_profissional = p.id_profissional
INNER JOIN usuario u ON p.id_profissional = u.id
ORDER BY a.data_publicacao DESC;
"""

OBTER_POR_PROFISSIONAL = """
SELECT 
    a.id_artigo,
    a.id_profissional,
    a.titulo,
    a.conteudo,
    a.data_publicacao,
    a.visualizacoes,
    a.ativo,
    a.avaliacao,
    u.nome AS nome_profissional,
    u.email AS email_profissional
FROM artigo a
INNER JOIN profissional p ON a.id_profissional = p.id_profissional
INNER JOIN usuario u ON p.id_profissional = u.id
WHERE a.id_profissional = ?
ORDER BY a.data_publicacao DESC;
"""
