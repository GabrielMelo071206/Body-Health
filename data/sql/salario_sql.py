CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS salario (
    id_salario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profissional INTEGER NOT NULL,
    mes_referencia INTEGER NOT NULL CHECK (mes_referencia BETWEEN 1 AND 12),
    ano_referencia INTEGER NOT NULL,
    total_visualizacoes INTEGER NOT NULL,
    visualizacoes_validas INTEGER NOT NULL,
    valor_por_visualizacao REAL NOT NULL,
    valor_total REAL NOT NULL,
    data_calculo DATE NOT NULL,
    status_pagamento TEXT NOT NULL CHECK (status_pagamento IN ('pendente', 'pago', 'cancelado')),
    data_pagamento DATE,
    observacoes TEXT,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (id_profissional) REFERENCES profissional(id_profissional) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO salario (
    id_profissional, mes_referencia, ano_referencia,
    total_visualizacoes, visualizacoes_validas,
    valor_por_visualizacao, valor_total,
    data_calculo, status_pagamento, data_pagamento,
    observacoes, ativo
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE salario
SET 
    mes_referencia = ?, ano_referencia = ?,
    total_visualizacoes = ?, visualizacoes_validas = ?,
    valor_por_visualizacao = ?, valor_total = ?,
    data_calculo = ?, status_pagamento = ?, data_pagamento = ?,
    observacoes = ?, ativo = ?
WHERE id_salario = ?
"""

EXCLUIR = """
DELETE FROM salario
WHERE id_salario = ?
"""

OBTER_POR_ID = """
SELECT 
    id_salario, id_profissional, mes_referencia, ano_referencia,
    total_visualizacoes, visualizacoes_validas,
    valor_por_visualizacao, valor_total,
    data_calculo, status_pagamento, data_pagamento,
    observacoes, ativo
FROM salario
WHERE id_salario = ?
"""

OBTER_TODOS = """
SELECT 
    id_salario, id_profissional, mes_referencia, ano_referencia,
    total_visualizacoes, visualizacoes_validas,
    valor_por_visualizacao, valor_total,
    data_calculo, status_pagamento, data_pagamento,
    observacoes, ativo
FROM salario
ORDER BY ano_referencia DESC, mes_referencia DESC
"""

OBTER_POR_PROFISSIONAL_E_PERIODO = """
SELECT 
    id_salario, id_profissional, mes_referencia, ano_referencia,
    total_visualizacoes, visualizacoes_validas,
    valor_por_visualizacao, valor_total,
    data_calculo, status_pagamento, data_pagamento,
    observacoes, ativo
FROM salario
WHERE id_profissional = ? AND mes_referencia = ? AND ano_referencia = ?
"""

# ================================
# QUERIES COM JOIN (usuário + profissional)
# ================================

OBTER_COM_DADOS_PROFISSIONAL = """
SELECT
    s.id_salario, s.id_profissional,
    u.nome, u.email,
    s.mes_referencia, s.ano_referencia,
    s.total_visualizacoes, s.visualizacoes_validas,
    s.valor_por_visualizacao, s.valor_total,
    s.data_calculo, s.status_pagamento,
    s.data_pagamento, s.observacoes, s.ativo
FROM
    salario s
INNER JOIN
    profissional p ON s.id_profissional = p.id_profissional
INNER JOIN
    usuario u ON p.id_profissional = u.id
WHERE
    s.id_salario = ?
"""

OBTER_TODOS_COM_DADOS_PROFISSIONAL = """
SELECT
    s.id_salario, s.id_profissional,
    u.nome, u.email,
    s.mes_referencia, s.ano_referencia,
    s.total_visualizacoes, s.visualizacoes_validas,
    s.valor_por_visualizacao, s.valor_total,
    s.data_calculo, s.status_pagamento,
    s.data_pagamento, s.observacoes, s.ativo
FROM
    salario s
INNER JOIN
    profissional p ON s.id_profissional = p.id_profissional
INNER JOIN
    usuario u ON p.id_profissional = u.id
ORDER BY
    s.ano_referencia DESC, s.mes_referencia DESC
"""

OBTER_POR_PROFISSIONAL_E_PERIODO_COM_DADOS = """
SELECT
    s.id_salario, s.id_profissional,
    u.nome, u.email,
    s.mes_referencia, s.ano_referencia,
    s.total_visualizacoes, s.visualizacoes_validas,
    s.valor_por_visualizacao, s.valor_total,
    s.data_calculo, s.status_pagamento,
    s.data_pagamento, s.observacoes, s.ativo
FROM
    salario s
INNER JOIN
    profissional p ON s.id_profissional = p.id_profissional
INNER JOIN
    usuario u ON p.id_profissional = u.id
WHERE
    s.id_profissional = ? AND s.mes_referencia = ? AND s.ano_referencia = ?
"""
