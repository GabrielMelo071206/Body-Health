CRIAR_TABELA_ASSINATURA = """
CREATE TABLE IF NOT EXISTS assinatura (
    id_assinatura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_plano INTEGER NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    status TEXT NOT NULL,
    valor_pago FLOAT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_plano) REFERENCES plano(id_plano) ON DELETE CASCADE
);
"""

INSERIR_ASSINATURA = """
INSERT INTO assinatura (id_cliente, id_plano, data_inicio, data_fim, status, valor_pago, ativo)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ALTERAR_ASSINATURA = """
UPDATE assinatura
SET id_cliente = ?, id_plano = ?, data_inicio = ?, data_fim = ?, status = ?, valor_pago = ?, ativo = ?
WHERE id_assinatura = ?;
"""

EXCLUIR_ASSINATURA = """
DELETE FROM assinatura
WHERE id_assinatura = ?;
"""

OBTER_ASSINATURA_POR_ID = """
SELECT 
    id_assinatura,
    id_cliente,
    id_plano,
    data_inicio,
    data_fim,
    status,
    valor_pago,
    ativo
FROM assinatura
WHERE id_assinatura = ?;
"""

OBTER_TODAS_ASSINATURAS = """
SELECT 
    id_assinatura,
    id_cliente,
    id_plano,
    data_inicio,
    data_fim,
    status,
    valor_pago,
    ativo
FROM assinatura
ORDER BY data_inicio DESC;
"""

OBTER_ASSINATURAS_POR_CLIENTE = """
SELECT 
    id_assinatura,
    id_cliente,
    id_plano,
    data_inicio,
    data_fim,
    status,
    valor_pago,
    ativo
FROM assinatura
WHERE id_cliente = ?
ORDER BY data_inicio DESC;
"""