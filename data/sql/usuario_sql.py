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

OBTER_POR_EMAIL = """
SELECT
    id, nome, email, senha_hash, data_nascimento, sexo, tipo_usuario
FROM
    usuarios
WHERE
    email = ?;
"""

CREEATE_TRIGGER = """
CREATE TRIGGER insere_cliente_ou_profissional
AFTER INSERT ON usuario
FOR EACH ROW
BEGIN
    IF NEW.tipo_usuario = 'cliente' THEN
        INSERT INTO clientes (id_usuario, nome, email, data_nascimento)
        VALUES (NEW.id, NEW.nome, NEW.email, NEW.data_nascimento);
    ELSEIF NEW.tipo_usuario IN ('educador_fisico', 'nutricionista') THEN
        INSERT INTO profissionais (id_usuario, nome, email, data_nascimento)
        VALUES (NEW.id, NEW.nome, NEW.email, NEW.data_nascimento);
    END IF;
END;
"""