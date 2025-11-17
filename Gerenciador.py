import json
import os
import sys
from datetime import datetime, timedelta

lista_tarefas = []
proximo_id = 1

ARQUIVO_TAREFAS = "tarefas.json"
ARQUIVO_HISTORICO = "tarefas_arquivadas.json"
PRIORIDADES_VALIDAS = ["Urgente", "Alta", "Média", "Baixa"]
STATUS_VALIDOS = ["Pendente", "Fazendo", "Concluída", "Arquivado", "Excluída"]
ORIGENS_VALIDAS = ["E-mail", "Telefone", "Chamado do Sistema"]

def verificar_criar_arquivos():
    print("Executando a função verificar_criar_arquivos")
    arquivos = [ARQUIVO_TAREFAS, ARQUIVO_HISTORICO]
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump([], f) 
                print(f"Arquivo '{arquivo}' não encontrado. Criado com sucesso.")
            except IOError as e:
                print(f"Erro crítico ao criar o arquivo '{arquivo}': {e}")
                sys.exit(f"Falha ao inicializar o arquivo {arquivo}. Encerrando.")

def carregar_dados():
    print("Executando a função carregar_dados")
    global lista_tarefas, proximo_id
    try:
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
            lista_tarefas = json.load(f)
        
        if lista_tarefas:
            max_id = max(tarefa['id'] for tarefa in lista_tarefas)
            proximo_id = max_id + 1
        else:
            proximo_id = 1
        print(f"Dados carregados. {len(lista_tarefas)} tarefas na lista. Próximo ID: {proximo_id}")

    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{ARQUIVO_TAREFAS}' está corrompido ou vazio. Iniciando com lista vazia.")
        lista_tarefas = []
        proximo_id = 1
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{ARQUIVO_TAREFAS}' não encontrado. Iniciando com lista vazia.")
        lista_tarefas = []
        proximo_id = 1
    except Exception as e:
        print(f"Erro inesperado ao carregar dados: {e}")
        sys.exit("Encerrando devido a erro de leitura de dados.")

def salvar_dados():
    print("Executando a função salvar_dados")
    try:
        with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
            json.dump(lista_tarefas, f, indent=4, ensure_ascii=False)
        print("Dados salvos com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar dados no '{ARQUIVO_TAREFAS}': {e}")
    except Exception as e:
        print(f"Erro inesperado ao salvar dados: {e}")

def arquivar_no_historico(tarefa):
    print(f"Executando a função arquivar_no_historico para ID {tarefa.get('id')}")
    try:
        historico = []
        if os.path.exists(ARQUIVO_HISTORICO):
            with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as f:
                try:
                    historico = json.load(f)
                    if not isinstance(historico, list):
                        historico = []
                except json.JSONDecodeError:
                    historico = []
        
        historico.append(tarefa)

        with open(ARQUIVO_HISTORICO, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=4, ensure_ascii=False)
        print(f"Tarefa ID {tarefa.get('id')} registrada no histórico.")

    except IOError as e:
        print(f"Erro de E/S ao atualizar histórico: {e}")
    except Exception as e:
        print(f"Erro inesperado ao arquivar no histórico: {e}")

def validar_input(mensagem_prompt, tipo='str', opcoes_validas=None):
    print("Executando a função validar_input")
    while True:
        if opcoes_validas:
            print(f"Opções válidas: {', '.join(opcoes_validas)}")
        
        entrada = input(mensagem_prompt)

        if tipo == 'int':
            try:
                valor_int = int(entrada)
                return valor_int
            except ValueError:
                print("Erro: Por favor, digite um número inteiro válido.")
                continue 

        elif tipo == 'str':
            if not entrada.strip(): 
                print("Erro: Esta informação é obrigatória e não pode ficar em branco.")
                continue
            
            if opcoes_validas:
                entrada_padronizada = entrada.strip().capitalize()
                opcoes_padronizadas = [op.capitalize() for op in opcoes_validas]
                
                if entrada_padronizada in opcoes_padronizadas:
                    return entrada_padronizada 
                else:
                    print(f"Erro: Opção '{entrada}' inválida. Tente novamente.")
            else:
                return entrada.strip() 

def buscar_tarefa_por_id(id_tarefa):
    print(f"Executando a função buscar_tarefa_por_id para ID {id_tarefa}")
    for tarefa in lista_tarefas:
        if tarefa['id'] == id_tarefa:
            return tarefa
    return None

def formatar_tarefa_para_exibicao(tarefa):
    print(f"Executando a função formatar_tarefa_para_exibicao para ID {tarefa.get('id')}")
    
    try:
        data_criacao = datetime.fromisoformat(tarefa['data_criacao']).strftime('%d/%m/%Y %H:%M')
    except (ValueError, TypeError):
        data_criacao = "N/A"
        
    data_conclusao = "N/A"
    tempo_execucao = "N/A"

    if tarefa.get('data_conclusao'):
        try:
            data_concl_obj = datetime.fromisoformat(tarefa['data_conclusao'])
            data_conclusao = data_concl_obj.strftime('%d/%m/%Y %H:%M')
            
            data_criacao_obj = datetime.fromisoformat(tarefa['data_criacao'])
            delta = data_concl_obj - data_criacao_obj
            tempo_execucao = str(delta)
        except (ValueError, TypeError):
            pass 

    info = (
        f"--- TAREFA ID: {tarefa['id']} ---\n"
        f"  Título:     {tarefa['titulo']}\n"
        f"  Descrição:  {tarefa['descricao']}\n"
        f"  Status:     {tarefa['status']}\n"
        f"  Prioridade: {tarefa['prioridade']}\n"
        f"  Origem:     {tarefa['origem']}\n"
        f"  Criada em:  {data_criacao}\n"
        f"  Concluída:  {data_conclusao}\n"
    )
    
    if tarefa['status'] in ["Concluída", "Arquivado"]:
        info += f"  Tempo de Execução: {tempo_execucao}\n"
        
    return info

def criar_tarefa():
    print("Executando a função criar_tarefa")
    global lista_tarefas, proximo_id

    titulo = validar_input("Digite o Título (obrigatório): ", 'str')
    descricao = input("Digite a Descrição (opcional): ")
    prioridade = validar_input("Digite a Prioridade (obrigatório): ", 'str', PRIORIDADES_VALIDAS)
    origem = validar_input("Digite a Origem (obrigatório): ", 'str', ORIGENS_VALIDAS)

    nova_tarefa = {
        "id": proximo_id,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": "Pendente", 
        "origem": origem,
        "data_criacao": datetime.now().isoformat(),
        "data_conclusao": None
    }

    lista_tarefas.append(nova_tarefa)
    proximo_id += 1

    print(f"\nSucesso! Tarefa ID {nova_tarefa['id']} ('{titulo}') criada.")

def pegar_proxima_tarefa():
    print("Executando a função pegar_proxima_tarefa")
    
    em_execucao = [t for t in lista_tarefas if t['status'] == "Fazendo"]
    if em_execucao:
        print("\nErro: Já existe uma tarefa em execução.")
        print(formatar_tarefa_para_exibicao(em_execucao[0]))
        return

    for prioridade in PRIORIDADES_VALIDAS:
        for tarefa in lista_tarefas:
            if tarefa['status'] == "Pendente" and tarefa['prioridade'] == prioridade:
                tarefa['status'] = "Fazendo"
                print(f"\nPróxima tarefa (ID {tarefa['id']}) definida como 'Fazendo':")
                print(formatar_tarefa_para_exibicao(tarefa))
                return 
    
    print("\nNão há tarefas pendentes para serem executadas.")

def atualizar_prioridade():
    print("Executando a função atualizar_prioridade")
    
    try:
        id_busca = validar_input("Digite o ID da tarefa para atualizar a prioridade: ", 'int')
        tarefa = buscar_tarefa_por_id(id_busca)

        if tarefa:
            print(f"Tarefa encontrada. Prioridade atual: {tarefa['prioridade']}")
            nova_prioridade = validar_input("Digite a nova Prioridade: ", 'str', PRIORIDADES_VALIDAS)
            
            tarefa['prioridade'] = nova_prioridade
            print(f"Sucesso! Prioridade da Tarefa ID {id_busca} atualizada para '{nova_prioridade}'.")
        else:
            print(f"Erro: Tarefa com ID {id_busca} não encontrada.")
            
    except Exception as e:
        print(f"Erro ao processar a atualização: {e}")

def concluir_tarefa():
    print("Executando a função concluir_tarefa")

    try:
        id_busca = validar_input("Digite o ID da tarefa a ser concluída: ", 'int')
        tarefa = buscar_tarefa_por_id(id_busca)

        if tarefa:
            if tarefa['status'] == "Concluída":
                print(f"Aviso: Tarefa ID {id_busca} já está 'Concluída'.")
                return

            tarefa['status'] = "Concluída"
            tarefa['data_conclusao'] = datetime.now().isoformat()
            print(f"Sucesso! Tarefa ID {id_busca} marcada como 'Concluída'.")
            print(formatar_tarefa_para_exibicao(tarefa))
        else:
            print(f"Erro: Tarefa com ID {id_busca} não encontrada.")
            
    except Exception as e:
        print(f"Erro ao processar a conclusão: {e}")

def arquivar_concluidas_antigas():
    print("Executando a função arquivar_concluidas_antigas")
    
    uma_semana_atras = datetime.now() - timedelta(weeks=1)
    tarefas_arquivadas_count = 0
    
    for tarefa in lista_tarefas:
        if tarefa['status'] == "Concluída":
            try:
                data_conclusao_obj = datetime.fromisoformat(tarefa['data_conclusao'])
                
                if data_conclusao_obj < uma_semana_atras:
                    arquivar_no_historico(tarefa)
                    tarefa['status'] = "Arquivado"
                    tarefas_arquivadas_count += 1
            except (TypeError, ValueError):
                continue
                
    if tarefas_arquivadas_count > 0:
        print(f"\nSucesso! {tarefas_arquivadas_count} tarefas antigas foram arquivadas.")
    else:
        print("\nNenhuma tarefa antiga para arquivar.")

def excluir_tarefa_logica():
    print("Executando a função excluir_tarefa_logica")

    try:
        id_busca = validar_input("Digite o ID da tarefa a ser excluída: ", 'int')
        tarefa = buscar_tarefa_por_id(id_busca)

        if tarefa:
            if tarefa['status'] == "Excluída":
                print(f"Aviso: Tarefa ID {id_busca} já está 'Excluída'.")
                return

            arquivar_no_historico(tarefa)
            
            tarefa['status'] = "Excluída"
            print(f"Sucesso! Tarefa ID {id_busca} marcada como 'Excluída' e registrada no histórico.")
        else:
            print(f"Erro: Tarefa com ID {id_busca} não encontrada.")
            
    except Exception as e:
        print(f"Erro ao processar a exclusão: {e}")

def relatorio_todas_tarefas():
    print("Executando a função relatorio_todas_tarefas")
    
    if not lista_tarefas:
        print("\nNão há nenhuma tarefa cadastrada.")
        return
        
    print("\n--- RELATÓRIO COMPLETO DE TAREFAS ---")
    
    lista_ordenada = sorted(lista_tarefas, key=lambda t: t['id'])
    
    for tarefa in lista_ordenada:
        print(formatar_tarefa_para_exibicao(tarefa))
        
    print("--- FIM DO RELATÓRIO ---")

def relatorio_arquivadas():
    print("Executando a função relatorio_arquivadas")

    tarefas_filtradas = [t for t in lista_tarefas if t['status'] == "Arquivado"]
    
    if not tarefas_filtradas:
        print("\nNão há nenhuma tarefa arquivada para exibir.")
        return
        
    print("\n--- RELATÓRIO DE TAREFAS ARQUIVADAS ---")
    
    for tarefa in tarefas_filtradas:
        print(formatar_tarefa_para_exibicao(tarefa))
        
    print("--- FIM DO RELATÓRIO ---")
    print(f"(Nota: O arquivo {ARQUIVO_HISTORICO} contém o histórico completo, incluindo excluídas.)")

def exibir_menu():
    print("\n--- GERENCIADOR DE TAREFAS ---")
    print("1. Criar nova tarefa")
    print("2. Pegar próxima tarefa (Definir 'Fazendo')")
    print("3. Atualizar prioridade de uma tarefa")
    print("4. Concluir uma tarefa")
    print("5. Arquivar tarefas concluídas (mais de 1 semana)")
    print("6. Excluir uma tarefa (exclusão lógica)")
    print("7. Relatório: Todas as tarefas")
    print("8. Relatório: Apenas tarefas arquivadas")
    print("9. Salvar e Sair")
    print("---------------------------------")

def main():
    print("Iniciando o sistema...")
    
    verificar_criar_arquivos()
    carregar_dados()
    
    while True:
        exibir_menu()
        
        try:
            opcao = validar_input("Escolha uma opção (1-9): ", 'int')
        except KeyboardInterrupt:
            print("\nOperação interrompida. Salvando dados antes de sair...")
            salvar_dados()
            sys.exit(0)
        except EOFError:
            print("\nEntrada encerrada (EOF). Salvando dados antes de sair...")
            salvar_dados()
            sys.exit(0)
        
        if opcao == 1:
            criar_tarefa()
        
        elif opcao == 2:
            pegar_proxima_tarefa()
            
        elif opcao == 3:
            atualizar_prioridade()
            
        elif opcao == 4:
            concluir_tarefa()
            
        elif opcao == 5:
            arquivar_concluidas_antigas()
            
        elif opcao == 6:
            excluir_tarefa_logica()
            
        elif opcao == 7:
            relatorio_todas_tarefas()
            
        elif opcao == 8:
            relatorio_arquivadas()
            
        elif opcao == 9:
            salvar_dados()
            print("Programa finalizado. Até logo!")
            sys.exit(0)
            
        else:
            print("Opção inválida. Por favor, escolha um número entre 1 e 9.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
