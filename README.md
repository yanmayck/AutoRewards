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

O projeto é composto pelos seguintes arquivos principais:

```
robux/
├── altomacao.py
├── .env.example (você deve criar um .env a partir dele)
├── requirements.txt
└── README.md
```

-   `altomacao.py`: O script principal que contém a lógica de automação.
-   `.env`: Arquivo de configuração de variáveis de ambiente (deve ser criado).
-   `requirements.txt`: Lista as dependências Python necessárias.
-   `README.md`: Este arquivo de documentação.

## 📋 Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

1.  **[Python 3.7+](https://www.python.org/downloads/)**
2.  **[Google Chrome](https://www.google.com/chrome/)**

## 🚀 Instalação e Configuração

Siga os passos abaixo para preparar o ambiente.


### 2. Obtenha os Arquivos do Projeto

Você pode baixar os arquivos manualmente ou clonar o repositório usando o comando abaixo:

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

## ⚙️ Como Funciona o Script (`altomacao.py`)

O script `altomacao.py` orquestra as ações de automação usando a biblioteca Selenium. Abaixo estão os principais passos:

1.  **Carregamento de Variáveis de Ambiente**: Utiliza `python-dotenv` para carregar as configurações (`CHROME_DATA_PATH`, `CHROME_BOT_PROFILE`, `NIVEL`) do arquivo `.env`.
2.  **Configuração do Navegador**:
    *   Usa `webdriver-manager` para baixar e gerenciar automaticamente o ChromeDriver compatível com sua versão do Chrome.
    *   Configura o Chrome para usar um perfil específico (`--user-data-dir` e `--profile-directory`), garantindo que a sessão logada do Microsoft Rewards seja reutilizada.
    *   O navegador é iniciado maximizado.
3.  **Execução da Automação de Tarefas (`executar_automacao_rewards`)**:
    *   Navega para `https://rewards.bing.com/`.
    *   Aguarda e localiza os "cartões" de tarefas disponíveis na página.
    *   Itera sobre os cartões, clicando em cada um para ativá-los.
    *   Para cada clique, uma nova aba é aberta. O script alterna para essa nova aba, aguarda um tempo para que a tarefa seja registrada, fecha a aba e retorna para a aba principal do Rewards. Isso evita a `StaleElementReferenceException` ao re-localizar os elementos após o retorno.
    *   Cartões desabilitados são automaticamente pulados.
4.  **Realização de Pesquisas (`realizar_pesquisas_aleatorias`)**:
    *   Baseado na variável `NIVEL` do `.env`:
        *   `NIVEL="1"`: Realiza 10 pesquisas aleatórias.
        *   `NIVEL="2"`: Realiza 30 pesquisas aleatórias.
    *   Um termo de pesquisa é sorteado de uma lista pré-definida de termos (para simular comportamento humano e obter variedade).
    *   Navega para `https://www.bing.com/`, encontra o campo de busca, digita o termo sorteado e submete a pesquisa.
    *   Após cada pesquisa, uma pequena pausa aleatória é inserida.
5.  **Tratamento de Erros e Logs**: O script inclui tratamento básico de exceções e imprime mensagens coloridas no terminal para indicar o progresso e quaisquer problemas encontrados.

## ▶️ Como Executar

Com tudo configurado, abra o terminal na pasta do seu projeto (`C:/suaPasta`) e execute o script:

```bash
python altomacao.py
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