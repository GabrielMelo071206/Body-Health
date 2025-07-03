CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS profissional (
    id_profissional INTEGER PRIMARY KEY,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    ano_formacao INTEGER NOT NULL,
    registro_profissional TEXT NOT NULL,
    FOREIGN KEY (id_profissional) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO profissional (id_profissional, ativo, ano_formacao, registro_profissional) 
VALUES (?, ?, ?, ?)
"""

ALTERAR = """
UPDATE profissional
SET ativo = ?, ano_formacao = ?, registro_profissional = ?
WHERE id_profissional = ?
"""

EXCLUIR = """
DELETE FROM profissional
WHERE id_profissional=?
"""

OBTER_POR_ID = """
SELECT
    p.id_profissional, u.nome, u.email, u.senha_hash, u.data_nascimento, u.sexo, u.tipo_usuario, p.ativo, p.ano_formacao, p.registro_profissional
FROM
    profissional p
INNER JOIN
    usuario u ON p.id_profissional = u.id
WHERE
    p.id_profissional = ?
"""

OBTER_TODOS = """
SELECT
    p.id_profissional, u.nome, u.email, u.senha_hash, u.data_nascimento, u.sexo, u.tipo_usuario, p.ativo, p.ano_formacao, p.registro_profissional
FROM
    profissional p
INNER JOIN
    usuario u ON p.id_profissional = u.id
ORDER BY
    u.nome
"""