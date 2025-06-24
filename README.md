# Robô de Automação para Microsoft Rewards

Este projeto contém um script em Python para automatizar a coleta de pontos no programa **Microsoft Rewards**. O robô utiliza a biblioteca Selenium para controlar uma instância do Google Chrome, realizando pesquisas diárias no Bing e completando as tarefas disponíveis no painel de recompensas.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4-green.svg)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ⚠️ Aviso Importante

O uso de bots e scripts de automação pode violar os Termos de Serviço da Microsoft. Utilize este projeto por sua conta e risco. Os desenvolvedores não se responsabilizam por qualquer penalidade, como a suspensão da sua conta.

## ✨ Funcionalidades

-   **Pesquisas Automatizadas**: Realiza pesquisas aleatórias no Bing para acumular pontos diários.
-   **Conclusão de Tarefas**: Navega pelo painel do Rewards e clica nos cartões de tarefas para ganhar pontos extras.
-   **Uso de Perfil Específico**: Opera em um perfil do Google Chrome já logado na sua conta Microsoft, evitando a necessidade de fazer login a cada execução.
-   **Gerenciamento Automático do Driver**: Utiliza o `webdriver-manager` para baixar e gerenciar automaticamente a versão correta do ChromeDriver.
-   **Interface Amigável no Terminal**: Exibe o progresso da automação com cores, ícones e mensagens claras.
-   **Configuração Flexível**: Carrega configurações sensíveis (como caminhos de diretório) a partir de um arquivo `.env` para maior segurança e portabilidade.
-   **Simulação Humana**: Inclui pausas aleatórias entre as ações para tornar a automação menos detectável.

## 📂 Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
AutoRewards/
├── main.py
├── config.json
├── requirements.txt
├── .gitignore
├── README.md
├── auto/
│   ├── altomacao.py
│   └── __init__.py
└── config/
    ├── config.py
    ├── ler_env.py
    ├── primeiro_login.py
    └── __init__.py
```

-   `main.py`: O script principal que orquestra a execução do robô, gerencia a configuração inicial e chama as funções de automação.
-   `auto/`: Contém os scripts de automação.
    -   `altomacao.py`: Contém a lógica principal para a automação das tarefas do Microsoft Rewards e pesquisas no Bing.
-   `config/`: Contém os arquivos de configuração do projeto.
    -   `config.py`: Define configurações do navegador e a lista de termos de pesquisa.
    -   `ler_env.py`: Responsável por carregar as variáveis de ambiente do arquivo `.env`.
    -   `primeiro_login.py`: Gerencia a verificação e marcação da configuração inicial do robô.
-   `config.json`: Arquivo utilizado para marcar se a configuração inicial do robô já foi realizada.
-   `.env.example`: Exemplo de arquivo de variáveis de ambiente (você deve criar um `.env` a partir dele).
-   `requirements.txt`: Lista as dependências Python necessárias para o projeto.
-   `.gitignore`: Define arquivos e diretórios que devem ser ignorados pelo Git, como arquivos de ambiente e caches.
-   `README.md`: Este arquivo de documentação.

## 📋 Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

1.  **[Python 3.7+](https://www.python.org/downloads/)**
2.  **[Google Chrome](https://www.google.com/chrome/)**

## 🚀 Instalação e Configuração

Siga os passos abaixo para preparar o ambiente.


### 2. Obtenha os Arquivos do Projeto

Você pode baixar os arquivos manualmente como um arquivo ZIP clicando em 'Code' e depois em 'Download ZIP' na página do GitHub do projeto, ou clonar o repositório usando o comando abaixo:

```bash
git clone https://github.com/yanmayck/AutoRewards.git
```

Depois, acesse a pasta do projeto:

```bash
cd AutoRewards
```

### 3. Crie um Ambiente Virtual (Recomendado)
Dentro da pasta do projeto, crie e ative um ambiente virtual.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
### 4. Instale as Dependências
Crie um arquivo chamado `requirements.txt` na pasta do projeto com o seguinte conteúdo:

```
# Requisitos do projeto para automação Microsoft Rewards
selenium
webdriver-manager
python-dotenv
```
Agora, instale as dependências usando o pip:

```bash
pip install -r requirements.txt
# Se tiver problemas de permissão no Windows, tente:
# pip install -r requirements.txt --user
```
### 5. Configure as Variáveis de Ambiente

O script precisa de um arquivo `.env` na pasta do projeto com as seguintes variáveis:

```ini
# Caminho onde será salvo o perfil do Chrome usado pela automação (recomendado deixar em C:/Perfis_Chrome_Selenium)
CHROME_DATA_PATH="C:/Perfis_Chrome_Selenium"

# Seu nível no Microsoft Rewards (1 para 10 pesquisas, 2 para 30 pesquisas)
NIVEL=1

# Nome do perfil da sua automação (pode ser qualquer nome, ex: MeuPerfilPrincipal)
CHROME_BOT_PROFILE="MeuPerfilPrincipal"
```

> ⚠️ Antes de rodar o robô, crie a pasta `C:/Perfis_Chrome_Selenium` no seu computador. Ela será usada para armazenar o perfil do Chrome exclusivo da automação.

### 6. (IMPORTANTE) Prepare o Perfil do Chrome

1.  Se quiser, crie um novo perfil no Chrome (opcional, recomendado para separar do seu perfil principal). Para isso, clique no ícone do seu perfil no canto superior direito do Chrome e selecione **Adicionar**.
2.  Anote o nome do diretório desse novo perfil (ex: `Profile 2`) e atualize a variável `CHROME_BOT_PROFILE` no seu arquivo `.env`.
3.  Abra o Chrome com este novo perfil e faça login no site do Microsoft Rewards (`rewards.bing.com`).
4.  Marque a opção para **Manter conectado** ou **Salvar senha** quando o navegador perguntar.
5.  Feche o navegador.

O robô usará este perfil e, como o login já está salvo, não será necessário digitar usuário e senha a cada execução.

## ⚙️ Visão Geral do Funcionamento

O robô é orquestrado principalmente pelo script `main.py`, que gerencia o fluxo de execução e a configuração inicial. O script `altomacao.py` contém a lógica detalhada das ações de automação, como o processamento de tarefas e as pesquisas. Abaixo estão os principais passos do funcionamento:

1.  **Verificação e Configuração Inicial**: O `main.py` verifica se o robô já foi configurado. Se não, ele executa um processo de configuração inicial para criar o perfil do Chrome e carregar as variáveis de ambiente.
2.  **Carregamento de Variáveis de Ambiente**: Utiliza `python-dotenv` para carregar as configurações (`CHROME_DATA_PATH`, `CHROME_BOT_PROFILE`, `NIVEL`) do arquivo `.env`.
3.  **Configuração do Navegador**: O `config.py` configura o Chrome para usar um perfil específico (`--user-data-dir` e `--profile-directory`), garantindo que a sessão logada do Microsoft Rewards seja reutilizada. O navegador é iniciado maximizado.
4.  **Execução da Automação de Tarefas (`executar_automacao_rewards` em `altomacao.py`)**:
    *   Navega para `https://rewards.bing.com/`.
    *   Aguarda e localiza os "cartões" de tarefas disponíveis na página.
    *   Itera sobre os cartões, clicando em cada um para ativá-los.
    *   Para cada clique, uma nova aba é aberta. O script alterna para essa nova aba, aguarda um tempo para que a tarefa seja registrada, fecha a aba e retorna para a aba principal do Rewards. Isso evita a `StaleElementReferenceException` ao re-localizar os elementos após o retorno.
    *   Cartões desabilitados são automaticamente pulados.
5.  **Realização de Pesquisas (`realizar_pesquisas_aleatorias` em `altomacao.py`)**:
    *   Baseado na variável `NIVEL` do `.env`:
        *   `NIVEL="1"`: Realiza 10 pesquisas aleatórias.
        *   `NIVEL="2"`: Realiza 30 pesquisas aleatórias.
    *   Um termo de pesquisa é sorteado de uma lista pré-definida de termos (para simular comportamento humano e obter variedade).
    *   Navega para `https://www.bing.com/`, encontra o campo de busca, digita o termo sorteado e submete a pesquisa.
    *   Após cada pesquisa, uma pequena pausa aleatória é inserida.
6.  **Tratamento de Erros e Logs**: O robô inclui tratamento básico de exceções e imprime mensagens coloridas no terminal para indicar o progresso e quaisquer problemas encontrados.

## ▶️ Como Executar

Com tudo configurado, abra o terminal na pasta do seu projeto (`C:/suaPasta`) e execute o script principal:

```bash
python main.py
```
O robô iniciará, abrirá o navegador no perfil correto e começará a executar as tarefas. Sente-se, relaxe e acompanhe o progresso pelo terminal!

## ❓ Resolução de Problemas Comuns

Se você encontrar problemas, verifique as seguintes soluções:

1.  **WebDriver não encontrado ou incompatível**:
    *   O `webdriver-manager` deve lidar com isso automaticamente. Certifique-se de que sua conexão com a internet está funcionando para que ele possa baixar o driver.
    *   Se o Chrome for atualizado, o `webdriver-manager` deve baixar a nova versão do driver na próxima execução.
2.  **Perfil do Chrome não encontrado ou login expirado**:
    *   Verifique os valores de `CHROME_DATA_PATH` e `CHROME_BOT_PROFILE` no seu arquivo `.env` com cuidado. Um erro comum é digitar `User Profile` em vez de `User Data`.
    *   Abra manualmente o Chrome com o perfil que você configurou e verifique se você ainda está logado no Microsoft Rewards. Se não estiver, faça login novamente e marque a opção para manter-se conectado.
3.  **`StaleElementReferenceException`**:
    *   Este erro geralmente ocorre quando um elemento da página (como um cartão) é acessado depois que a página foi alterada. O script tenta re-localizar os elementos para mitigar isso. Se persistir, pode indicar uma mudança na estrutura do site do Rewards que exige uma atualização no script.
4.  **Permissões**:
    *   No Windows, se o `pip install` falhar por permissão, tente executar o comando com `--user` como sugerido na seção de instalação.
    *   Certifique-se de que o Python e o Chrome não estão sendo bloqueados por um firewall ou antivírus.
5.  **A automação não está clicando em todos os cartões**:
    *   O script possui uma `listaNumerosNaoAceitos` que pula alguns cartões por padrão. Verifique esta lista no código (`altomacao.py`) se você deseja que todos os cartões sejam processados.

Se o problema persistir, por favor, abra uma issue no repositório do projeto com o máximo de detalhes possível, incluindo mensagens de erro e passos para reproduzir o problema.