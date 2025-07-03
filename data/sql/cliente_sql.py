CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY,
    tipo_conta TEXT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES usuario(id) ON DELETE CASCADE
);
"""
INSERIR = """
INSERT INTO cliente (tipo_conta, id_cliente) 
VALUES (?, ?)
"""

ALTERAR = """
UPDATE cliente
SET tipo_conta=?
WHERE id_cliente=?
"""

EXCLUIR = """
DELETE FROM cliente
WHERE id_cliente=?
"""

OBTER_POR_ID = """
SELECT 
    c.id_cliente, c.tipo_conta, u.nome, u.email, u.senha_hash, u.data_nascimento, u.sexo, u.tipo_usuario
FROM cliente c
INNER JOIN usuario u ON c.id_cliente = u.id
WHERE c.id_cliente=?
"""

OBTER_TODOS = """
SELECT 
    c.id_cliente, c.tipo_conta, u.nome, u.email, u.senha_hash, u.data_nascimento, u.sexo, u.tipo_usuario
FROM cliente c
INNER JOIN usuario u ON c.id_cliente = u.id
ORDER BY u.nome
"""

