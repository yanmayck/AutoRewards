# Imports necessários para a solução
import time
import random
import config
from dotenv import load_dotenv
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import config.config as config
# --- Constantes de Cores e Ícones para o Terminal ---

def configurar_navegador(caminho_user_data, nome_do_perfil):
    """
    Configura e inicializa o navegador Chrome com as opções especificadas.

    Args:
        caminho_user_data (str): Caminho para o diretório de dados do usuário do Chrome.
        nome_do_perfil (str): Nome do perfil do Chrome a ser usado.

    Returns:
        webdriver.Chrome: Instância do driver do Chrome configurada.
    """
    print(f"{config.Estilos.HEADER}{config.Estilos.ROBOT_ICON} Iniciando o Robô de Automação Rewards...{config.Estilos.ENDC}")
    
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
    print(f"{config.Estilos.WAIT_ICON} {config.Estilos.CYAN}   Aguardando a nova aba abrir...{config.Estilos.ENDC}")
    wait.until(EC.number_of_windows_to_be(2))

    # Muda o foco para a nova aba
    for handle in driver.window_handles:
        if handle != aba_original:
            driver.switch_to.window(handle)
            break
            
    print(f"{config.Estilos.TAB_ICON} {config.Estilos.GREEN}   Foco na nova aba: '{driver.title[:40]}...'{config.Estilos.ENDC}")
    time.sleep(5)  # Mantém a espera para a tarefa ser processada

    print(f"{config.Estilos.TAB_ICON} {config.Estilos.BLUE}   Fechando a aba da tarefa...{config.Estilos.ENDC}")
    driver.close()

    print(f"{config.Estilos.TAB_ICON} {config.Estilos.BLUE}   Retornando foco para a aba principal...{config.Estilos.ENDC}")
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

    print(f"\n{config.Estilos.WAIT_ICON} {config.Estilos.CYAN}Aguardando os cartões aparecerem na página principal...{config.Estilos.ENDC}")
    cartoes = wait.until(EC.presence_of_all_elements_located(localizador_dos_cartoes))
    numero_de_cartoes = len(cartoes)
    print(f"{config.Estilos.SUCCESS_ICON} {config.Estilos.GREEN}Sucesso! {numero_de_cartoes} cartões encontrados.{config.Estilos.ENDC}")

    aba_original = driver.current_window_handle
    print(f"{config.Estilos.INFO_ICON} {config.Estilos.BLUE}Aba principal identificada: {aba_original}{config.Estilos.ENDC}")
    print(f"{config.Estilos.BOLD}{'='*60}{config.Estilos.ENDC}")
    
    listaNumerosNaoAceitos = [3, 4, 5, 6]

    for i in range(numero_de_cartoes):
        if i  in listaNumerosNaoAceitos:
            print(f"\n{config.Estilos.INFO_ICON} {config.Estilos.BLUE}Pulando cartão #{i+1} conforme lista de exclusão.{config.Estilos.ENDC}")
            continue

        print(f"\n{config.Estilos.CARD_ICON} {config.Estilos.BOLD}Processando Cartão #{i+1} de {numero_de_cartoes}{config.Estilos.ENDC}")
        
        try:
            # Re-localiza os cartões a cada iteração para evitar 'StaleElementReferenceException'
            cartoes = wait.until(EC.presence_of_all_elements_located(localizador_dos_cartoes))
            cartao_atual = cartoes[i]

            if "disabled" in cartao_atual.get_attribute("class"):
                print(f"{config.Estilos.WARNING}   -> Cartão #{i+1} está desabilitado. Pulando.{config.Estilos.ENDC}")
                continue

            # Tenta clicar no cartão
            cartao_atual.click()
            
            # Processa a nova aba que foi aberta
            processar_aba_tarefa(driver, wait, aba_original)
            
            print(f"{config.Estilos.SUCCESS_ICON} {config.Estilos.GREEN}   Cartão #{i+1} processado com sucesso!{config.Estilos.ENDC}")
            # Aguarda a página principal estar pronta novamente
            wait.until(EC.visibility_of_element_located(localizador_dos_cartoes))
            
        except StaleElementReferenceException:
            print(f"{config.Estilos.WARNING}   -> Ocorreu um StaleElementReferenceException. Tentando novamente a iteração...{config.Estilos.ENDC}")
            continue # Pula para a próxima iteração, o elemento será re-localizado
        except Exception as e:
            print(f"{config.Estilos.ERROR_ICON} {config.Estilos.FAIL}   Ocorreu um erro ao processar o cartão #{i+1}: {e}{config.Estilos.ENDC}")
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
   

    if not config.caminho_user_data or not config.nome_do_perfil:
        print(f"{config.Estilos.FAIL}{config.Estilos.ERROR_ICON} Variáveis de ambiente CHROME_DATA_PATH ou CHROME_BOT_PROFILE não definidas.{config.Estilos.ENDC}")
        return

    driver = None  # Inicializa driver como None
    try:
        driver = configurar_navegador(config.caminho_user_data, config.nome_do_perfil)
        executar_automacao_rewards(driver)
        realizar_pesquisas_aleatorias(driver, config.total_pesquisas,config.nivel)
        print(f"\n{config.Estilos.BOLD}{'='*60}{config.Estilos.ENDC}")
        print(f"{config.Estilos.SUCCESS_ICON} {config.Estilos.HEADER}{config.Estilos.BOLD} TODOS OS CARTÕES FORAM PROCESSADOS! {config.Estilos.SUCCESS_ICON}{config.Estilos.ENDC}")

    except TimeoutException:
        print(f"\n{config.Estilos.ERROR_ICON} {config.Estilos.FAIL}{config.Estilos.BOLD}ERRO: O tempo de espera acabou. Os cartões não foram encontrados ou a página não carregou.{config.Estilos.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{config.Estilos.STOP_ICON} {config.Estilos.WARNING}{config.Estilos.BOLD} Programa finalizado pelo usuário.{config.Estilos.ENDC}")
    except Exception as e:
        print(f"\n{config.Estilos.ERROR_ICON} {config.Estilos.FAIL}{config.Estilos.BOLD}Ocorreu um erro inesperado na execução principal: {e}{config.Estilos.ENDC}")
    
    finally:
        if driver:
            print(f"\n{config.Estilos.INFO_ICON} {config.Estilos.CYAN}O navegador permanecerá aberto por 10 segundos antes de fechar.{config.Estilos.ENDC}")
            time.sleep(10)
            driver.quit()
            print(f"{config.Estilos.ROBOT_ICON} {config.Estilos.BLUE}Navegador fechado. Sessão encerrada.{config.Estilos.ENDC}")

if __name__ == "__main__":
    main()