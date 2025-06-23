# Imports necessários para a solução
import time
import os
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# --- Constantes de Cores e Ícones para o Terminal ---
class Estilos:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INFO_ICON = "ℹ️ "
    SUCCESS_ICON = "✅"
    WAIT_ICON = "⏳"
    CARD_ICON = "🃏"
    TAB_ICON = "📑"
    ERROR_ICON = "❌"
    STOP_ICON = "🛑"
    ROBOT_ICON = "🤖"


total_pesquisas = [
    # Perguntas Gerais e Curiosidades
    "o que é a teoria da relatividade",
    "quem foi Santos Dumont",
    "fases da lua em 2025",
    "maiores desertos do mundo",
    "história da invenção do telefone",
    "quantos países existem no mundo",
    "o que significa a sigla UNESCO",
    "como fazer um nó de gravata",
    
    # Tecnologia e Internet
    "o que é blockchain",
    "melhores celulares custo-benefício 2025",
    "Python vs JavaScript qual usar",
    "como funciona a internet 5G",
    "lançamentos de placas de vídeo",
    "o que é um ataque de phishing",
    "história da Microsoft",
    
    # Cultura Pop e Entretenimento
    "próximos lançamentos da Netflix",
    "filmes em cartaz nos cinemas",
    "músicas mais tocadas no Spotify Brasil",
    "vencedores do Oscar de melhor filme",
    "biografia da Anitta",
    "jogos mais esperados do ano",
    "o que é um dorama",
    
    # Viagens e Geografia (com toque local)
    "pontos turísticos de Caldas Novas, GO",
    "melhores praias do Nordeste brasileiro",
    "o que fazer em Pirenópolis",
    "qual a capital da Nova Zelândia",
    "clima em Gramado, RS",
    "sete maravilhas do mundo moderno",
    "Parque Nacional da Chapada dos Veadeiros",
    "Rio Araguaia",
    
    # Culinária e Receitas (com toque local)
    "receita de pamonha goiana",
    "como fazer feijoada completa",
    "benefícios do pequi para a saúde",
    "melhores vinhos para iniciantes",
    "receita de bolo de fubá cremoso",
    "como temperar frango para assar",
    "comidas típicas do Centro-Oeste",
    
    # Ciência e Natureza
    "animais em extinção no Cerrado",
    "planetas do sistema solar em ordem",
    "como as abelhas produzem mel",
    "o que são buracos negros",
    "curiosidades sobre o corpo humano",
    "tipos de rochas",
    
    # Saúde e Bem-estar
    "exercícios para fazer em casa",
    "benefícios da meditação guiada",
    "receitas de lanches saudáveis",
    "como melhorar a qualidade do sono",
    "dicas para beber mais água",
    
    # Notícias e Assuntos Gerais
    "cotação do dólar hoje",
    "resultados do campeonato brasileiro",
    "previsão do tempo para amanhã",
    "notícias de economia no Brasil",
    "principais índices da bolsa de valores",
]



def configurar_navegador(caminho_user_data, nome_do_perfil):
    """
    Configura e inicializa o navegador Chrome com as opções especificadas.

    Args:
        caminho_user_data (str): Caminho para o diretório de dados do usuário do Chrome.
        nome_do_perfil (str): Nome do perfil do Chrome a ser usado.

    Returns:
        webdriver.Chrome: Instância do driver do Chrome configurada.
    """
    print(f"{Estilos.HEADER}{Estilos.ROBOT_ICON} Iniciando o Robô de Automação Rewards...{Estilos.ENDC}")
    
    service = ChromeService(executable_path=ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={caminho_user_data}")
    chrome_options.add_argument(f"--profile-directory={nome_do_perfil}")
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def processar_aba_tarefa(driver, wait, aba_original):
    """
    Gerencia a troca de abas para processar uma tarefa do Rewards.

    Args:
        driver (webdriver.Chrome): A instância do driver do Selenium.
        wait (WebDriverWait): A instância do WebDriverWait.
        aba_original (str): O identificador da janela da aba principal.
    """
    print(f"{Estilos.WAIT_ICON} {Estilos.CYAN}   Aguardando a nova aba abrir...{Estilos.ENDC}")
    wait.until(EC.number_of_windows_to_be(2))

    # Muda o foco para a nova aba
    for handle in driver.window_handles:
        if handle != aba_original:
            driver.switch_to.window(handle)
            break
            
    print(f"{Estilos.TAB_ICON} {Estilos.GREEN}   Foco na nova aba: '{driver.title[:40]}...'{Estilos.ENDC}")
    time.sleep(5)  # Mantém a espera para a tarefa ser processada

    print(f"{Estilos.TAB_ICON} {Estilos.BLUE}   Fechando a aba da tarefa...{Estilos.ENDC}")
    driver.close()

    print(f"{Estilos.TAB_ICON} {Estilos.BLUE}   Retornando foco para a aba principal...{Estilos.ENDC}")
    driver.switch_to.window(aba_original)

def executar_automacao_rewards(driver):
    """
    Executa a automação principal na página do Bing Rewards.

    Args:
        driver (webdriver.Chrome): A instância do driver do Selenium.
    """
    driver.get("https://rewards.bing.com/")
    
    localizador_dos_cartoes = (By.CSS_SELECTOR, ".ds-card-sec.ng-scope")
    wait = WebDriverWait(driver, 20)

    print(f"\n{Estilos.WAIT_ICON} {Estilos.CYAN}Aguardando os cartões aparecerem na página principal...{Estilos.ENDC}")
    cartoes = wait.until(EC.presence_of_all_elements_located(localizador_dos_cartoes))
    numero_de_cartoes = len(cartoes)
    print(f"{Estilos.SUCCESS_ICON} {Estilos.GREEN}Sucesso! {numero_de_cartoes} cartões encontrados.{Estilos.ENDC}")

    aba_original = driver.current_window_handle
    print(f"{Estilos.INFO_ICON} {Estilos.BLUE}Aba principal identificada: {aba_original}{Estilos.ENDC}")
    print(f"{Estilos.BOLD}{'='*60}{Estilos.ENDC}")
    
    listaNumerosNaoAceitos = [3, 4, 5, 6]

    for i in range(numero_de_cartoes):
        if i  in listaNumerosNaoAceitos:
            print(f"\n{Estilos.INFO_ICON} {Estilos.BLUE}Pulando cartão #{i+1} conforme lista de exclusão.{Estilos.ENDC}")
            continue

        print(f"\n{Estilos.CARD_ICON} {Estilos.BOLD}Processando Cartão #{i+1} de {numero_de_cartoes}{Estilos.ENDC}")
        
        try:
            # Re-localiza os cartões a cada iteração para evitar 'StaleElementReferenceException'
            cartoes = wait.until(EC.presence_of_all_elements_located(localizador_dos_cartoes))
            cartao_atual = cartoes[i]

            if "disabled" in cartao_atual.get_attribute("class"):
                print(f"{Estilos.WARNING}   -> Cartão #{i+1} está desabilitado. Pulando.{Estilos.ENDC}")
                continue

            # Tenta clicar no cartão
            cartao_atual.click()
            
            # Processa a nova aba que foi aberta
            processar_aba_tarefa(driver, wait, aba_original)
            
            print(f"{Estilos.SUCCESS_ICON} {Estilos.GREEN}   Cartão #{i+1} processado com sucesso!{Estilos.ENDC}")
            # Aguarda a página principal estar pronta novamente
            wait.until(EC.visibility_of_element_located(localizador_dos_cartoes))
            
        except StaleElementReferenceException:
            print(f"{Estilos.WARNING}   -> Ocorreu um StaleElementReferenceException. Tentando novamente a iteração...{Estilos.ENDC}")
            continue # Pula para a próxima iteração, o elemento será re-localizado
        except Exception as e:
            print(f"{Estilos.ERROR_ICON} {Estilos.FAIL}   Ocorreu um erro ao processar o cartão #{i+1}: {e}{Estilos.ENDC}")
            # Se o erro foi crítico, pode ser melhor voltar para a aba principal e continuar
            driver.switch_to.window(aba_original)
def realizar_pesquisas_aleatorias(driver, lista_termos,nivel ):
    """
    Realiza um número definido de pesquisas aleatórias no Bing.

    :param driver: A instância do WebDriver.
    :param lista_termos: A lista de strings de onde os termos serão sorteados.
    :param numero_de_pesquisas: Quantas pesquisas devem ser feitas.
    """
    if nivel ==1:
        numero_de_pesquisas = 10
    else:
        numero_de_pesquisas = 30
    print(f"Iniciando {numero_de_pesquisas} pesquisas aleatórias...")
    localizador_campo_busca = (By.ID, "sb_form_q")
    wait = WebDriverWait(driver, 10)

    for i in range(numero_de_pesquisas):
        try:
            print(f"\n--- Pesquisa #{i+1}/{numero_de_pesquisas} ---")
            
            # a. Sorteia um termo da lista
            termo_aleatorio = random.choice(lista_termos)
            print(f"Termo sorteado: '{termo_aleatorio}'")
            
            # b. Garante que estamos na página de busca
            #    Se não for a primeira pesquisa, a página de resultados estará aberta.
            #    Navegar para o Bing.com reseta o estado.
            driver.get("https://www.bing.com/")

            # c. Encontra o campo de busca (ESSENCIAL fazer isso DENTRO do loop)
            campo_busca = wait.until(EC.visibility_of_element_located(localizador_campo_busca))
            
            # d. Limpa o campo, digita e envia
            campo_busca.clear() # Limpa o campo para garantir que está vazio
            campo_busca.send_keys(termo_aleatorio)
            campo_busca.submit()
            
            print("Pesquisa realizada com sucesso.")
            
            # g. Pausa "humana"
            time.sleep(random.uniform(3, 6))

        except Exception as e:
            print(f"Ocorreu um erro na pesquisa #{i+1}: {e}")
            # Se der um erro, podemos tentar ir para a próxima pesquisa
            continue
            

def main():
    """
    Função principal que orquestra a execução do robô.
    """
    load_dotenv()
    caminho_user_data = os.getenv("CHROME_DATA_PATH")
    nome_do_perfil = os.getenv("CHROME_BOT_PROFILE")
    nivel = os.getenv("NIVEL")

    if not caminho_user_data or not nome_do_perfil:
        print(f"{Estilos.FAIL}{Estilos.ERROR_ICON} Variáveis de ambiente CHROME_DATA_PATH ou CHROME_BOT_PROFILE não definidas.{Estilos.ENDC}")
        return

    driver = None  # Inicializa driver como None
    try:
        driver = configurar_navegador(caminho_user_data, nome_do_perfil)
        realizar_pesquisas_aleatorias(driver, total_pesquisas,nivel)
        executar_automacao_rewards(driver)
        print(f"\n{Estilos.BOLD}{'='*60}{Estilos.ENDC}")
        print(f"{Estilos.SUCCESS_ICON} {Estilos.HEADER}{Estilos.BOLD} TODOS OS CARTÕES FORAM PROCESSADOS! {Estilos.SUCCESS_ICON}{Estilos.ENDC}")

    except TimeoutException:
        print(f"\n{Estilos.ERROR_ICON} {Estilos.FAIL}{Estilos.BOLD}ERRO: O tempo de espera acabou. Os cartões não foram encontrados ou a página não carregou.{Estilos.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Estilos.STOP_ICON} {Estilos.WARNING}{Estilos.BOLD} Programa finalizado pelo usuário.{Estilos.ENDC}")
    except Exception as e:
        print(f"\n{Estilos.ERROR_ICON} {Estilos.FAIL}{Estilos.BOLD}Ocorreu um erro inesperado na execução principal: {e}{Estilos.ENDC}")
    
    finally:
        if driver:
            print(f"\n{Estilos.INFO_ICON} {Estilos.CYAN}O navegador permanecerá aberto por 10 segundos antes de fechar.{Estilos.ENDC}")
            time.sleep(10)
            driver.quit()
            print(f"{Estilos.ROBOT_ICON} {Estilos.BLUE}Navegador fechado. Sessão encerrada.{Estilos.ENDC}")

if __name__ == "__main__":
    main()