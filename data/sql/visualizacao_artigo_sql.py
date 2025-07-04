CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS visualizacao_artigo (
    id_visualizacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_artigo INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    data_visualizacao DATE NOT NULL DEFAULT (DATE('now')),
    mes_referencia INTEGER NOT NULL,
    ano_referencia INTEGER NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (id_artigo) REFERENCES artigo(id_artigo) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO visualizacao_artigo (
    id_artigo, id_usuario, data_visualizacao, mes_referencia, ano_referencia, ativo
) VALUES (?, ?, ?, ?, ?, ?);
"""

ALTERAR = """
UPDATE visualizacao_artigo
SET data_visualizacao = ?, mes_referencia = ?, ano_referencia = ?, ativo = ?
WHERE id_visualizacao = ?;
"""

EXCLUIR = """
DELETE FROM visualizacao_artigo
WHERE id_visualizacao = ?;
"""

OBTER_POR_ID = """
SELECT 
    v.id_visualizacao,
    v.id_artigo,
    v.id_usuario,
    v.data_visualizacao,
    v.mes_referencia,
    v.ano_referencia,
    v.ativo
FROM visualizacao_artigo v
WHERE v.id_visualizacao = ?;
"""
OBTER_TODAS_POR_ARTIGO = """
SELECT * FROM visualizacao_artigo
WHERE id_artigo = ?;
"""

OBTER_TODAS_POR_MES_ANO = """
SELECT * FROM visualizacao_artigo
WHERE mes_referencia = ? AND ano_referencia = ?;
"""
