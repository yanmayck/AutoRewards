# robux/auto/altomacao.py

# Imports necessários para a solução
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# Importa a FUNÇÃO de configurar o navegador do módulo 'config'
import config.config as config 

# Importa as VARIÁVEIS lidas do .env do módulo 'ler_env'
from config.ler_env import caminho_user_data, nome_do_perfil, nivel


def processar_aba_tarefa(driver, wait, aba_original):
    """
    Gerencia a troca de abas para processar uma tarefa do Rewards.
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


def realizar_pesquisas_aleatorias(driver, lista_termos, nivel):
    """
    Realiza um número definido de pesquisas aleatórias no Bing.
    """
    if nivel == "1":
        numero_de_pesquisas = 10
    else:
        numero_de_pesquisas = 30
    print(f"Iniciando {numero_de_pesquisas} pesquisas aleatórias...")
    localizador_campo_busca = (By.ID, "sb_form_q")
    wait = WebDriverWait(driver, 10)

    for i in range(numero_de_pesquisas):
        try:
            print(f"\n--- Pesquisa #{i+1}/{numero_de_pesquisas} ---")
            
            termo_aleatorio = random.choice(lista_termos)
            print(f"Termo sorteado: '{termo_aleatorio}'")
            
            driver.get("https://www.bing.com/")

            campo_busca = wait.until(EC.visibility_of_element_located(localizador_campo_busca))
            
            campo_busca.clear()
            campo_busca.send_keys(termo_aleatorio)
            campo_busca.submit()
            
            print("Pesquisa realizada com sucesso.")
            
            time.sleep(random.uniform(3, 6))

        except Exception as e:
            print(f"Ocorreu um erro na pesquisa #{i+1}: {e}")
            continue
            

def main():
    """
    Função principal que orquestra a execução do robô.
    """
    if not caminho_user_data or not nome_do_perfil:
        print(f"{config.Estilos.FAIL}{config.Estilos.ERROR_ICON} Variáveis de ambiente CHROME_DATA_PATH ou CHROME_BOT_PROFILE não definidas.{config.Estilos.ENDC}")
        return

    driver = None  # Inicializa driver como None
    try:
        # ==================================================================
        # A CORREÇÃO ESTÁ AQUI:
        # As variáveis 'caminho_user_data' e 'nome_do_perfil' são usadas
        # diretamente, sem o prefixo 'config.', pois vêm de 'ler_env'.
        driver = config.configurar_navegador(caminho_user_data, nome_do_perfil)
        # ==================================================================

        executar_automacao_rewards(driver)
        realizar_pesquisas_aleatorias(driver, config.total_pesquisas, nivel)
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

# Esta parte não é necessária quando 'altomacao.py' é chamado por 'main.py',
# mas não causa mal em mantê-la.
if __name__ == "__main__":
    main()