CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL,
senha_hash TEXT NOT NULL,
data_nascimento TEXT NOT NULL,
sexo TEXT NOT NULL,
tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('cliente', 'educador_fisico', 'nutricionista', 'administrador'))
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha_hash, data_nascimento, sexo, tipo_usuario)
VALUES (?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE usuario
SET nome=?, email=?, data_nascimento=?, sexo=?, tipo_usuario=?
WHERE id=?
"""

ALTERAR_SENHA = """
UPDATE usuario
SET senha_hash=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM usuario
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
id, nome, email, senha_hash, data_nascimento, sexo, tipo_usuario
FROM usuario
WHERE id=?
"""

OBTER_TODOS = """
SELECT 
id, nome, email, senha_hash, data_nascimento, sexo, tipo_usuario
FROM usuario
ORDER BY nome
"""