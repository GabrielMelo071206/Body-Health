CRIAR_TABELA =  """
CREATE TABLE IF NOT EXISTS denuncia (
    id_denuncia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_denunciante INTEGER NOT NULL,
    id_denunciado INTEGER NOT NULL,
    tipo_denunciante TEXT NOT NULL,
    tipo_denunciado TEXT NOT NULL,
    motivo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data_denuncia DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    id_admin_avaliador INTEGER,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    observacoes_admin TEXT NOT NULL,
    ativo BOOLEAN NOT NULL, 
    FOREIGN KEY (id_denunciante) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_denunciado) REFERENCES usuario(id) ON DELETE CASCADE, 
    FOREIGN KEY (id_admin_avaliador) REFERENCES administrador(id) ON DELETE CASCADE
);"""

INSERIR = """
INSERT INTO denuncia (
    id_denuncia, id_denunciante, tipo_denunciante, tipo_denunciado,
    id_denunciado, motivo, descricao, status,
    id_admin_avaliador, observacoes_admin, ativo
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

ALTERAR = """
UPDATE denuncia
SET 
    id_denunciante = ?, 
    id_denunciado = ?, 
    tipo_denunciante = ?,
    tipo_denunciado = ?,
    motivo = ?, 
    descricao = ?, 
    status = ?, 
    id_admin_avaliador = ?,
    data_avaliacao = ?, 
    observacoes_admin = ?, 
    ativo = ?
WHERE id_denuncia = ?;
"""

EXCLUIR = """
DELETE FROM denuncia 
WHERE id_denuncia = ?;
"""

OBTER_POR_ID = """
SELECT 
    d.id_denuncia, 
    d.id_denunciante, 
    d.id_denunciado, 
    d.tipo_denunciante,
    d.tipo_denunciado,
    d.motivo,
    d.descricao,
    d.status,
    d.id_admin_avaliador,
    d.data_avaliacao,
    d.observacoes_admin,
    d.ativo
FROM denuncia d
WHERE d.id_denuncia = ?;
"""

OBTER_TODOS = """
SELECT
    d.id_denuncia, 
    d.id_denunciante, 
    d.id_denunciado, 
    d.tipo_denunciante,
    d.tipo_denunciado,
    d.motivo,
    d.descricao,
    d.status,
    d.id_admin_avaliador,
    d.data_avaliacao,
    d.observacoes_admin,
    d.ativo
FROM denuncia d
INNER JOIN usuario u ON d.id_denunciante = u.id
INNER JOIN usuario u2 ON d.id_denunciado = u2.id
ORDER BY d.data_denuncia DESC;
"""