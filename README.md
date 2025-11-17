# Gerenciador de Tarefas

Este é um projeto em Python para gerenciamento de tarefas pessoais, desenvolvido conforme as especificações da Atividade de Aplicação.

## 🚀 Como Executar

1.  **Pré-requisitos:** Você precisa ter o **Python 3.x** instalado em seu computador.
2.  **Localização:** Salve o arquivo `gerenciador_tarefas.py` em uma pasta de sua preferência.
3.  **Execução:**
    * Abra seu terminal (Prompt de Comando no Windows, Terminal no macOS/Linux).
    * Navegue até a pasta onde você salvou o arquivo.
        ```sh
        cd caminho/para/a/pasta
        ```
    * Execute o programa usando o Python:
        ```sh
        python gerenciador_tarefas.py
        ```

## ⚙️ Funcionalidades

O programa oferece um menu completo para gerenciar o ciclo de vida de suas tarefas, incluindo:

* Criação de tarefas com título, descrição, prioridade e origem.
* Um sistema para "puxar" a próxima tarefa pendente mais prioritária.
* Atualização de prioridade, conclusão e exclusão (lógica) de tarefas.
* Relatórios completos e filtrados (apenas tarefas arquivadas).
* Arquivamento automático de tarefas concluídas há mais de uma semana.

## 💾 Persistência de Dados

O programa gerencia os dados automaticamente:

* **`tarefas.json`**: Armazena a lista de tarefas ativas. É lido na inicialização e salvo ao sair.
* **`tarefas_arquivadas.json`**: Armazena um histórico (log) de todas as tarefas que foram marcadas como "Excluída" ou "Arquivado".

**Importante:** Na primeira vez que você executar o programa, ele criará automaticamente os arquivos `tarefas.json` e `tarefas_arquivadas.json` na mesma pasta, caso eles não existam.
