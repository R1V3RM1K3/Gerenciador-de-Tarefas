import json
import os
import sys
from datetime import datetime, timedelta


lista_tarefas = []
proximo_id = 1

# Constantes de configuração
[cite_start]ARQUIVO_TAREFAS = "tarefas.json" [cite: 103]
[cite_start]ARQUIVO_HISTORICO = "tarefas_arquivadas.json" [cite: 110]
[cite_start]PRIORIDADES_VALIDAS = ["Urgente", "Alta", "Média", "Baixa"] [cite: 16]
[cite_start]STATUS_VALIDOS = ["Pendente", "Fazendo", "Concluída", "Arquivado", "Excluída"] [cite: 16, 17]
[cite_start]ORIGENS_VALIDAS = ["E-mail", "Telefone", "Chamado do Sistema"] [cite: 17]

# [cite_start]--- 2. Definição de Funções [cite: 70] ---

# --- Funções de Persistência (JSON) ---

def verificar_criar_arquivos():
    """
    [cite_start][cite: 87]
    Propósito: Verifica se os arquivos JSON necessários existem. [cite_start]Se não, os cria com uma lista vazia. [cite: 114, 119]
    [cite_start]Parâmetros: Nenhum [cite: 91]
    [cite_start]Retorno: Nenhum [cite: 92]
    """
    [cite_start]print("Executando a função verificar_criar_arquivos") [cite: 80]
    [cite_start]arquivos = [ARQUIVO_TAREFAS, ARQUIVO_HISTORICO] [cite: 116, 117]
    for arquivo in arquivos:
        [cite_start]if not os.path.exists(arquivo): [cite: 119]
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    [cite_start]json.dump([], f) # Cria o arquivo com uma lista vazia [cite: 121]
                print(f"Arquivo '{arquivo}' não encontrado. Criado com sucesso.")
            except IOError as e:
                print(f"Erro crítico ao criar o arquivo '{arquivo}': {e}")
                sys.exit(f"Falha ao inicializar o arquivo {arquivo}. Encerrando.")

def carregar_dados():
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Carrega a lista de tarefas do 'tarefas.json' para a 'lista_tarefas' global. [cite: 104]
              Atualiza o contador 'proximo_id' com base nas tarefas carregadas.
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função carregar_dados") [cite: 80]
    global lista_tarefas, proximo_id
    try:
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
            [cite_start]lista_tarefas = json.load(f) [cite: 104]
        
        # [cite_start]Atualiza o próximo ID com base no ID mais alto encontrado [cite: 85]
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
        # A função verificar_criar_arquivos() já deve ter tratado isso, mas é uma boa prática.
        print(f"Aviso: Arquivo '{ARQUIVO_TAREFAS}' não encontrado. Iniciando com lista vazia.")
        lista_tarefas = []
        proximo_id = 1
    except Exception as e:
        print(f"Erro inesperado ao carregar dados: {e}")
        sys.exit("Encerrando devido a erro de leitura de dados.")

def salvar_dados():
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Salva a 'lista_tarefas' global no arquivo 'tarefas.json'. [cite: 105]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função salvar_dados") [cite: 80]
    try:
        with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
            [cite_start]json.dump(lista_tarefas, f, indent=4, ensure_ascii=False) [cite: 105]
        print("Dados salvos com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar dados no '{ARQUIVO_TAREFAS}': {e}")
    except Exception as e:
        print(f"Erro inesperado ao salvar dados: {e}")

def arquivar_no_historico(tarefa):
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Registra uma tarefa (copia) no arquivo de histórico 'tarefas_arquivadas.json'. [cite: 110]
              [cite_start]Esta função acumula o histórico. [cite: 111]
    Parâmetros: tarefa (dict) - A tarefa a ser arquivada.
    Retorno: Nenhum
    """
    [cite_start]print(f"Executando a função arquivar_no_historico para ID {tarefa.get('id')}") [cite: 80]
    try:
        # 1. Lê o histórico existente
        historico = []
        if os.path.exists(ARQUIVO_HISTORICO):
            with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as f:
                try:
                    historico = json.load(f)
                    if not isinstance(historico, list):
                        historico = []
                except json.JSONDecodeError:
                    historico = []
        
        # 2. Adiciona a nova tarefa
        [cite_start]historico.append(tarefa) [cite: 111]

        # 3. Escreve o histórico atualizado de volta
        with open(ARQUIVO_HISTORICO, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=4, ensure_ascii=False)
        print(f"Tarefa ID {tarefa.get('id')} registrada no histórico.")

    except IOError as e:
        print(f"Erro de E/S ao atualizar histórico: {e}")
    except Exception as e:
        print(f"Erro inesperado ao arquivar no histórico: {e}")


# Funções de Validação e Auxiliares

def validar_input(mensagem_prompt, tipo='str', opcoes_validas=None):
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Função robusta para capturar e validar a entrada do usuário. [cite: 74]
              Lida com validação de tipo, opções de lista e entradas obrigatórias.
    Parâmetros: 
        mensagem_prompt (str): A mensagem a ser exibida ao usuário.
        [cite_start]tipo (str): 'str' ou 'int' (para tratamento de exceção). [cite: 77]
        opcoes_validas (list, opcional): Uma lista de valores válidos (ex: PRIORIDADES_VALIDAS).
    Retorno: O valor validado (str ou int).
    """
    [cite_start]print("Executando a função validar_input") [cite: 80]
    while True:
        # [cite_start]Exibe as opções se fornecidas [cite: 23]
        if opcoes_validas:
            print(f"Opções válidas: {', '.join(opcoes_validas)}")
        
        entrada = input(mensagem_prompt)

        if tipo == 'int':
            try:
                valor_int = int(entrada)
                [cite_start]return valor_int [cite: 77]
            except ValueError:
                [cite_start]print("Erro: Por favor, digite um número inteiro válido.") [cite: 77]
                continue # Volta ao início do loop

        elif tipo == 'str':
            if not entrada.strip(): # Verifica se está vazio ou só com espaços
                print("Erro: Esta informação é obrigatória e não pode ficar em branco.")
                continue
            
            if opcoes_validas:
                # Padroniza a entrada e as opções para comparação (ex: 'Baixa' == 'baixa')
                entrada_padronizada = entrada.strip().capitalize()
                opcoes_padronizadas = [op.capitalize() for op in opcoes_validas]
                
                if entrada_padronizada in opcoes_padronizadas:
                    return entrada_padronizada # Retorna o valor padronizado
                else:
                    print(f"Erro: Opção '{entrada}' inválida. Tente novamente.")
            else:
                return entrada.strip() # Retorna a string limpa

def buscar_tarefa_por_id(id_tarefa):
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Encontra e retorna um dicionário de tarefa da 'lista_tarefas' global pelo ID. [cite: 83]
    Parâmetros: id_tarefa (int) - O ID da tarefa a ser buscada.
    Retorno: dict (a tarefa) ou None se não encontrada.
    """
    [cite_start]print(f"Executando a função buscar_tarefa_por_id para ID {id_tarefa}") [cite: 80]
    for tarefa in lista_tarefas:
        if tarefa['id'] == id_tarefa:
            return tarefa
    return None

def formatar_tarefa_para_exibicao(tarefa):
    """
    [cite_start][cite: 87]
    Propósito: Formata os dados de uma tarefa para uma exibição legível.
    Parâmetros: tarefa (dict) - A tarefa a ser formatada.
    Retorno: str - A string formatada.
    """
    [cite_start]print(f"Executando a função formatar_tarefa_para_exibicao para ID {tarefa.get('id')}") [cite: 80]
    
    # Processamento de datas
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
            
            # [cite_start]Cálculo do tempo de execução [cite: 35]
            data_criacao_obj = datetime.fromisoformat(tarefa['data_criacao'])
            delta = data_concl_obj - data_criacao_obj
            tempo_execucao = str(delta)
        except (ValueError, TypeError):
            pass # Mantém "N/A"

    # Monta a string de saída
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
        [cite_start]info += f"  Tempo de Execução: {tempo_execucao}\n" [cite: 35]
        
    return info


# [cite_start]--- Funções Principais (Ciclo de Vida da Tarefa) [cite: 20]

def criar_tarefa():
    """
    [cite_start][cite: 87, 93]
    Propósito: Cria uma nova tarefa solicitando informações ao usuário,
               [cite_start]valida os dados e adiciona a tarefa à lista global de tarefas. [cite: 22, 53, 94, 95]
    [cite_start]Parâmetros: Nenhum [cite: 96]
    [cite_start]Retorno: Nenhum [cite: 97]
    """
    [cite_start]print("Executando a função criar_tarefa") [cite: 80, 98]
    [cite_start]global lista_tarefas, proximo_id [cite: 64, 65]

    # [cite_start]Variáveis locais para a nova tarefa [cite: 61]
    [cite_start]titulo = validar_input("Digite o Título (obrigatório): ", 'str') [cite: 15]
    [cite_start]descricao = input("Digite a Descrição (opcional): ") [cite: 15]
    [cite_start]prioridade = validar_input("Digite a Prioridade (obrigatório): ", 'str', PRIORIDADES_VALIDAS) [cite: 16]
    [cite_start]origem = validar_input("Digite a Origem (obrigatório): ", 'str', ORIGENS_VALIDAS) [cite: 17]

    # Cria o dicionário da tarefa
    nova_tarefa = {
        [cite_start]"id": proximo_id, [cite: 84]
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        [cite_start]"status": "Pendente", # Status inicial obrigatório [cite: 16]
        "origem": origem,
        [cite_start]"data_criacao": datetime.now().isoformat(), [cite: 18]
        [cite_start]"data_conclusao": None [cite: 30]
    }

    # Adiciona à lista global
    [cite_start]lista_tarefas.append(nova_tarefa) [cite: 22]
    [cite_start]proximo_id += 1 [cite: 85]

    print(f"\nSucesso! Tarefa ID {nova_tarefa['id']} ('{titulo}') criada.")

def pegar_proxima_tarefa():
    """
    [cite_start][cite: 87]
    Propósito: Verifica se há tarefas urgentes/prioritárias e atualiza a primeira encontrada
               para 'Fazendo'. [cite_start]Limita a apenas uma tarefa 'Fazendo' por vez. [cite: 24, 12]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função pegar_proxima_tarefa") [cite: 80]
    
    # [cite_start]Verifica se já existe uma tarefa em execução [cite: 12]
    em_execucao = [t for t in lista_tarefas if t['status'] == "Fazendo"]
    if em_execucao:
        print("\nErro: Já existe uma tarefa em execução.")
        print(formatar_tarefa_para_exibicao(em_execucao[0]))
        return

    # [cite_start]Ordem de busca: Urgente -> Alta -> Média -> Baixa [cite: 26]
    for prioridade in PRIORIDADES_VALIDAS:
        for tarefa in lista_tarefas:
            if tarefa['status'] == "Pendente" and tarefa['prioridade'] == prioridade:
                # [cite_start]Encontrou a próxima tarefa [cite: 25]
                [cite_start]tarefa['status'] = "Fazendo" [cite: 27]
                print(f"\nPróxima tarefa (ID {tarefa['id']}) definida como 'Fazendo':")
                print(formatar_tarefa_para_exibicao(tarefa))
                return # Encerra a função após encontrar a primeira
    
    # Se o loop terminar sem retorno, não há tarefas pendentes
    print("\nNão há tarefas pendentes para serem executadas.")

def atualizar_prioridade():
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Permite ao usuário alterar a prioridade de uma tarefa existente. [cite: 28]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função atualizar_prioridade") [cite: 80]
    
    try:
        id_busca = validar_input("Digite o ID da tarefa para atualizar a prioridade: ", 'int')
        tarefa = buscar_tarefa_por_id(id_busca)

        if tarefa:
            print(f"Tarefa encontrada. Prioridade atual: {tarefa['prioridade']}")
            [cite_start]nova_prioridade = validar_input("Digite a nova Prioridade: ", 'str', PRIORIDADES_VALIDAS) [cite: 28]
            
            tarefa['prioridade'] = nova_prioridade
            print(f"Sucesso! Prioridade da Tarefa ID {id_busca} atualizada para '{nova_prioridade}'.")
        else:
            print(f"Erro: Tarefa com ID {id_busca} não encontrada.")
            
    except Exception as e:
        print(f"Erro ao processar a atualização: {e}")

def concluir_tarefa():
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Marca uma tarefa como 'Concluída' e registra a data/hora da conclusão. [cite: 29]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função concluir_tarefa") [cite: 80]

    try:
        id_busca = validar_input("Digite o ID da tarefa a ser concluída: ", 'int')
        tarefa = buscar_tarefa_por_id(id_busca)

        if tarefa:
            if tarefa['status'] == "Concluída":
                print(f"Aviso: Tarefa ID {id_busca} já está 'Concluída'.")
                return

            [cite_start]tarefa['status'] = "Concluída" [cite: 31]
            [cite_start]tarefa['data_conclusao'] = datetime.now().isoformat() [cite: 29, 30]
            print(f"Sucesso! Tarefa ID {id_busca} marcada como 'Concluída'.")
            print(formatar_tarefa_para_exibicao(tarefa))
        else:
            print(f"Erro: Tarefa com ID {id_busca} não encontrada.")
            
    except Exception as e:
        print(f"Erro ao processar a conclusão: {e}")

def arquivar_concluidas_antigas():
    """
    [cite_start][cite: 87]
    Propósito: Verifica tarefas 'Concluídas' há mais de uma semana e atualiza
               [cite_start]seu status para 'Arquivado', registrando-as no histórico. [cite: 32, 112]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função arquivar_concluidas_antigas") [cite: 80]
    
    uma_semana_atras = datetime.now() - timedelta(weeks=1)
    tarefas_arquivadas_count = 0
    
    # Usar [:] cria uma cópia para iterar, permitindo modificar a original
    for tarefa in lista_tarefas:
        if tarefa['status'] == "Concluída":
            try:
                data_conclusao_obj = datetime.fromisoformat(tarefa['data_conclusao'])
                
                [cite_start]if data_conclusao_obj < uma_semana_atras: [cite: 32]
                    # [cite_start]1. Registrar no histórico [cite: 110, 112]
                    arquivar_no_historico(tarefa)
                    # 2. Atualizar status na lista ativa
                    [cite_start]tarefa['status'] = "Arquivado" [cite: 32]
                    tarefas_arquivadas_count += 1
            except (TypeError, ValueError):
                # Ignora tarefas com data_conclusao inválida ou None
                continue
                
    if tarefas_arquivadas_count > 0:
        print(f"\nSucesso! {tarefas_arquivadas_count} tarefas antigas foram arquivadas.")
    else:
        print("\nNenhuma tarefa antiga para arquivar.")

def excluir_tarefa_logica():
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Realiza a exclusão lógica de uma tarefa, mudando seu status para 'Excluída' [cite: 33]
               [cite_start]e registrando-a no histórico. [cite: 110]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função excluir_tarefa_logica") [cite: 80]

    try:
        id_busca = validar_input("Digite o ID da tarefa a ser excluída: ", 'int')
        tarefa = buscar_tarefa_por_id(id_busca)

        if tarefa:
            if tarefa['status'] == "Excluída":
                print(f"Aviso: Tarefa ID {id_busca} já está 'Excluída'.")
                return

            # [cite_start]1. Registrar no histórico ANTES de alterar o status [cite: 110, 112]
            arquivar_no_historico(tarefa)
            
            # [cite_start]2. Atualizar status para "Excluída" (não remover da lista) [cite: 33]
            tarefa['status'] = "Excluída"
            print(f"Sucesso! Tarefa ID {id_busca} marcada como 'Excluída' e registrada no histórico.")
        else:
            print(f"Erro: Tarefa com ID {id_busca} não encontrada.")
            
    except Exception as e:
        print(f"Erro ao processar a exclusão: {e}")


# Funções de Relatório

def relatorio_todas_tarefas():
    """
    [cite_start][cite: 87]
    Propósito: Exibe todas as informações de todas as tarefas na lista principal.
               [cite_start]Calcula o tempo de execução para tarefas concluídas. [cite: 34, 35]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função relatorio_todas_tarefas") [cite: 80]
    
    if not lista_tarefas:
        print("\nNão há nenhuma tarefa cadastrada.")
        return
        
    print("\n--- RELATÓRIO COMPLETO DE TAREFAS ---")
    
    # Ordena para melhor visualização (Opcional, mas bom)
    lista_ordenada = sorted(lista_tarefas, key=lambda t: t['id'])
    
    for tarefa in lista_ordenada:
        print(formatar_tarefa_para_exibicao(tarefa))
        
    print("--- FIM DO RELATÓRIO ---")

def relatorio_arquivadas():
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Exibe a lista de tarefas com status 'Arquivado'. [cite: 36]
               [cite_start]Tarefas 'Excluídas' não são mostradas aqui. [cite: 37]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    [cite_start]print("Executando a função relatorio_arquivadas") [cite: 80]

    # Filtra apenas as tarefas com status "Arquivado" da lista principal
    [cite_start]tarefas_filtradas = [t for t in lista_tarefas if t['status'] == "Arquivado"] [cite: 36]
    
    if not tarefas_filtradas:
        print("\nNão há nenhuma tarefa arquivada para exibir.")
        return
        
    print("\n--- RELATÓRIO DE TAREFAS ARQUIVADAS ---")
    
    for tarefa in tarefas_filtradas:
        print(formatar_tarefa_para_exibicao(tarefa))
        
    print("--- FIM DO RELATÓRIO ---")
    print(f"(Nota: O arquivo {ARQUIVO_HISTORICO} contém o histórico completo, incluindo excluídas.)")

def exibir_menu():
    """
    [cite_start][cite: 87]
    [cite_start]Propósito: Imprime o menu principal de opções para o usuário. [cite: 43, 45]
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
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


# [cite_start]--- 3. Corpo Principal do Programa [cite: 71] ---

def main():
    """
    [cite_start][cite: 87]
    Propósito: Função principal que executa o fluxo do programa.
               Carrega dados, exibe o menu e gerencia o loop de execução.
    Parâmetros: Nenhum
    Retorno: Nenhum
    """
    print("Iniciando o sistema...")
    
    # Inicialização
    [cite_start]verificar_criar_arquivos() [cite: 119]
    [cite_start]carregar_dados() [cite: 104]
    
    # [cite_start]Loop principal do menu [cite: 43]
    while True:
        exibir_menu()
        
        # [cite_start]Validação da opção do menu [cite: 46, 77]
        try:
            opcao = validar_input("Escolha uma opção (1-9): ", 'int')
        except KeyboardInterrupt:
            print("\nOperação interrompida. Use a opção '9' para sair com segurança.")
            continue
        
        if opcao == 1:
            [cite_start]criar_tarefa() [cite: 48]
        
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
            [cite_start]salvar_dados() [cite: 105]
            print("Programa finalizado. Até logo!")
            [cite_start]sys.exit(0) [cite: 106]
            
        else:
            [cite_start]print("Opção inválida. Por favor, escolha um número entre 1 e 9.") [cite: 46]
        
        # Pausa para o usuário ler a saída antes de limpar (opcional)
        input("\nPressione Enter para continuar...")

# Ponto de entrada do script
if __name__ == "__main__":
    main()
