CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS admin (
id_administrador INTEGER PRIMARY KEY ,
master BOOLEAN NOT NULL DEFAULT 0,
FOREIGN KEY (id_administrador) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO admin (master, id_administrador) 
VALUES (?, ?)
"""

ALTERAR = """
UPDATE admin
SET master=?
WHERE id_administrador=?
"""

EXCLUIR = """
DELETE FROM admin
WHERE id_administrador=?
"""

OBTER_POR_ID = """
SELECT 
    a.id_administrador, 
    a.master, 
    u.nome, 
    u.email, 
    u.senha_hash, 
    u.data_nascimento, 
    u.sexo, 
    u.tipo_usuario
FROM admin a
INNER JOIN usuario u ON a.id_administrador = u.id
WHERE a.id_administrador=?
"""
OBTER_TODOS = """
SELECT 
a.id_administrador, a.master, u.nome, u.email, u.senha_hash
FROM admin a
INNER JOIN usuario u ON a.id_administrador = u.id
ORDER BY u.nome
""" 