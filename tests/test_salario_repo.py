from data.repo.salario_repo import *
from data.models.salario_model import *
from data.sql.salario_sql import *
from datetime import date

class TestSalarioRepo:

    def test_criar_tabela_salario(self, test_db):
        resultado = criar_tabela_salario()
        assert resultado is True, "A tabela de salários não foi criada corretamente."

    def test_inserir_salario(self, test_db, profissional_exemplo, salario_exemplo):
        from data.repo.profissional_repo import inserir_profissional, criar_tabela_profissional
        from data.repo.usuario_repo import criar_tabela_usuario

        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_salario()

        id_profissional = inserir_profissional(profissional_exemplo)
        salario_exemplo.id_profissional = id_profissional

        id_salario = inserir_salario(salario_exemplo)
        salario_db = obter_salario_por_id(id_salario)

        assert salario_db is not None, "O salário inserido não deve ser None"
        assert salario_db.id_salario == 1, "ID do salário inserido não confere"
        assert salario_db.valor_total == salario_exemplo.valor_total, "Valor total calculado não confere"
        assert salario_db.id_profissional == salario_exemplo.id_profissional, "ID do profissional não confere"
        assert salario_db.mes_referencia == salario_exemplo.mes_referencia, "Mês de referência não confere"
        assert salario_db.ano_referencia == salario_exemplo.ano_referencia, "Ano de referência não confere"
        assert salario_db.total_visualizacoes == salario_exemplo.total_visualizacoes, "Total de visualizações não confere"
        assert salario_db.visualizacoes_validas == salario_exemplo.visualizacoes_validas, "Visualizações válidas não confere"
        assert salario_db.observacoes == salario_exemplo.observacoes, " As observações não conferem"
        assert salario_db.status_pagamento == salario_exemplo.status_pagamento, "O status de pagamento não confere"
        assert salario_db.data_pagamento == salario_exemplo.data_pagamento, "A data de pagamento não confere"
        
   
    
    def test_obter_salario_por_profissional_e_periodo(self, test_db, profissional_exemplo, salario_exemplo):
        from data.repo.profissional_repo import inserir_profissional, criar_tabela_profissional
        from data.repo.usuario_repo import criar_tabela_usuario

        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_salario()

        id_prof = inserir_profissional(profissional_exemplo)
        salario_exemplo.id_profissional = id_prof
        salario_exemplo.mes_referencia = 7
        salario_exemplo.ano_referencia = 2025
        salario_exemplo.valor_total = 2.60

        inserir_salario(salario_exemplo)

        salario_encontrado = obter_salario_por_profissional_e_periodo(id_prof, 7, 2025)
        assert salario_encontrado is not None, "O salário deveria ter sido encontrado"
        assert salario_encontrado.valor_total == 2.60, "O valor do salário buscado está incorreto"

    def test_alterar_salario_existente(self, test_db, profissional_exemplo, salario_exemplo):
        from data.repo.profissional_repo import inserir_profissional, criar_tabela_profissional
        from data.repo.usuario_repo import criar_tabela_usuario

        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_salario()

        id_prof = inserir_profissional(profissional_exemplo)
        salario_exemplo.id_profissional = id_prof

        id_salario = inserir_salario(salario_exemplo)
        salario_db = obter_salario_por_id(id_salario)

        # Alteração
        salario_db.total_visualizacoes = 200
        salario_db.visualizacoes_validas = 180
        salario_db.valor_total = 3.60
        salario_db.observacoes = "atualizado"
        salario_db.status_pagamento = "pago"
        salario_db.data_pagamento =  None  # Atualizando a data de pagamento
        salario_db.id_salario = id_salario  # Necessário para a atualização
        salario_db.mes_referencia = 7
        salario_db.ano_referencia = 2025
        salario_db.id_profissional = id_prof
        salario_db.data_calculo = date.today()
        salario_db.valor_por_visualizacao = 0.02
        salario_db.ativo = False
        
        
        resultado = alterar_salario(salario_db)
        salario_atualizado = obter_salario_por_id(id_salario)

        assert resultado is True, "A operação de alteração deveria retornar True"
        assert salario_atualizado.valor_total == 3.60, "O valor total não foi atualizado corretamente"
        assert salario_atualizado.status_pagamento == "pago", "O status do pagamento não foi atualizado"
        assert salario_atualizado.observacoes == "atualizado", "As observações não foram atualizadas"
        assert salario_atualizado.data_pagamento ==  None, "A data de pagamento deveria ter sido atualizada"
        assert salario_atualizado.total_visualizacoes == 200, "O total de visualizações não foi atualizado"
        assert salario_atualizado.visualizacoes_validas == 180, "As visualizações válidas não foram atualizadas"
        assert salario_atualizado.mes_referencia == 7, "O mês de referência não foi atualizado"
        assert salario_atualizado.ano_referencia == 2025, "O ano de referência não foi atualizado"
        assert salario_atualizado.id_profissional == id_prof, "O ID do profissional não foi atualizado"
        from datetime import datetime
        assert datetime.strptime(salario_atualizado.data_calculo, "%Y-%m-%d").date() == date.today(), \
"A data de cálculo não foi atualizada"
        assert salario_atualizado.valor_por_visualizacao == 0.02, "O valor por visualização não foi atualizado"
        assert bool(salario_atualizado.ativo) is False, "O status ativo não foi atualizado corretamente"
        assert salario_atualizado.id_salario == id_salario, "O ID do salário não foi atualizado corretamente"
        
    
    def test_excluir_salario_existente(self, test_db, profissional_exemplo, salario_exemplo):
        from data.repo.profissional_repo import inserir_profissional, criar_tabela_profissional
        from data.repo.usuario_repo import criar_tabela_usuario

        criar_tabela_usuario()
        criar_tabela_profissional()
        criar_tabela_salario()

        id_prof = inserir_profissional(profissional_exemplo)
        salario_exemplo.id_profissional = id_prof

        id_salario = inserir_salario(salario_exemplo)
        resultado = excluir_salario(id_salario)
        salario_excluido = obter_salario_por_id(id_salario)

        assert resultado is True, "A exclusão do salário deveria retornar True"
        assert salario_excluido is None, "O salário deveria ter sido excluído"

    def test_excluir_salario_inexistente(self, test_db):
        criar_tabela_salario()
        resultado = excluir_salario(999)
        assert resultado is False, "Excluir um salário inexistente deveria retornar False"

    def test_obter_salario_por_id_inexistente(self, test_db):
        criar_tabela_salario()
        salario = obter_salario_por_id(999)
        assert salario is None, "Deveria retornar None ao buscar um salário inexistente"
