CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS avaliacao_artigo (
    id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_artigo INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 5),
    data_avaliacao DATE NOT NULL DEFAULT (DATE('now')),
    ativo BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (id_artigo) REFERENCES artigo(id_artigo) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO avaliacao_artigo (id_artigo, id_usuario, nota, data_avaliacao, ativo)
VALUES (?, ?, ?, ?, ?);
"""

ALTERAR = """
UPDATE avaliacao_artigo
SET nota = ?, data_avaliacao = ?, ativo = ?
WHERE id_avaliacao = ?;
"""

EXCLUIR = """
DELETE FROM avaliacao_artigo
WHERE id_avaliacao = ?;
"""

OBTER_POR_ID = """
SELECT 
    a.id_avaliacao,
    a.id_artigo,
    art.titulo AS titulo_artigo,
    a.id_usuario,
    u.nome AS nome_usuario,
    a.nota,
    a.data_avaliacao,
    a.ativo
FROM avaliacao_artigo a
JOIN artigo art ON a.id_artigo = art.id_artigo
JOIN usuario u ON a.id_usuario = u.id
WHERE a.id_avaliacao = ?;
"""

OBTER_TODAS_POR_ARTIGO = """
SELECT * FROM avaliacao_artigo
WHERE id_artigo = ?
"""

OBTER_MEDIA_POR_ARTIGO = """
SELECT 
    AVG(a.nota) AS media_nota
FROM avaliacao_artigo a
WHERE a.id_artigo = ? AND a.ativo = 1;
"""
