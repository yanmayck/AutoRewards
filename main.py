# main.py

import sys
import time
from core.config import ConfigurationManager, Estilos, total_pesquisas
from core.browser import BrowserManager
from core.bot import RewardsBot

def handle_first_run(config: ConfigurationManager):
    """Guia o usuário através do processo de configuração inicial."""
    config.perform_initial_setup()

    print(f"\n{Estilos.BOLD}{Estilos.WARNING}[ AÇÃO NECESSÁRIA ]{Estilos.ENDC}")
    print("O navegador será aberto para que você possa fazer o login pela primeira vez.")
    print("1. Entre com sua conta Microsoft no site do Rewards.")
    print("2. IMPORTANTE: Marque a opção 'Manter conectado'.")
    print("3. Feche o navegador quando terminar.")
    input(f"{Estilos.CYAN}Pressione Enter para abrir o navegador...{Estilos.ENDC}")

    try:
        browser_manager = BrowserManager(config)
        driver = browser_manager.get_desktop_driver()
        driver.get("https://rewards.bing.com/")
        input(f"{Estilos.GREEN}Após o login, pressione Enter aqui para finalizar a configuração...{Estilos.ENDC}")
        driver.quit()
        config.mark_setup_as_complete()
        print(f"\n{Estilos.SUCCESS_ICON} Configuração concluída! Execute o programa novamente para iniciar a automação.")
    except Exception as e:
        print(f"{Estilos.ERROR_ICON} Ocorreu um erro durante a configuração: {e}")
    
    sys.exit()

def run_automation():
    """Executa o fluxo principal de automação para desktop e mobile."""
    config = ConfigurationManager()
    browser_manager = BrowserManager(config)
    desktop_driver = None
    mobile_driver = None

    try:
        # --- Automação Desktop ---
        desktop_driver = browser_manager.get_desktop_driver()
        bot = RewardsBot(desktop_driver, config)
        bot.complete_dashboard_tasks()
        bot.perform_searches(total_pesquisas, search_type="Desktop")
        desktop_driver.quit()
        print(f"{Estilos.SUCCESS_ICON} Automação Desktop finalizada.")
        time.sleep(3)

        # --- Automação Mobile ---
        mobile_driver = browser_manager.get_mobile_driver()
        bot = RewardsBot(mobile_driver, config)
        bot.perform_searches(total_pesquisas, search_type="Mobile")
        mobile_driver.quit()
        print(f"{Estilos.SUCCESS_ICON} Automação Mobile finalizada.")

    finally:
        if desktop_driver:
            desktop_driver.quit()
        if mobile_driver:
            mobile_driver.quit()
        print(f"\n{Estilos.ROBOT_ICON} Sessão encerrada.")

if __name__ == "__main__":
    try:
        config_manager = ConfigurationManager()
        if config_manager.is_first_run():
            handle_first_run(config_manager)
        else:
            print(f"{Estilos.SUCCESS_ICON} Configuração encontrada. Iniciando autodmação...")
            run_automation()
    except KeyboardInterrupt:
        print(f"\n{Estilos.WARNING}Programa interrompido pelo usuário.{Estilos.ENDC}")
    except Exception as e:
        print(f"\n{Estilos.ERROR_ICON}{Estilos.FAIL} Um erro inesperado ocorreu: {e}{Estilos.ENDC}")