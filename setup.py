# setup.py

from core.config import ConfigurationManager, Estilos
from core.browser import BrowserManager
import sys

def open_browser_for_setup():
    """Abre o navegador no perfil da automação para configuração manual."""
    config = ConfigurationManager()
    
    if config.is_first_run():
        print(f"{Estilos.WARNING}Parece que esta é a primeira execução.")
        print("Por favor, execute 'python main.py' primeiro para criar os arquivos de configuração.{Estilos.ENDC}")
        sys.exit()

    print(f"{Estilos.INFO_ICON}Abrindo o navegador com o perfil '{config.profile_name}'.")
    print("Você pode usar esta janela para fazer login ou verificar suas configurações.")
    
    try:
        browser_manager = BrowserManager(config)
        driver = browser_manager.get_desktop_driver()
        driver.get("https://rewards.bing.com/")
        input(f"\n{Estilos.GREEN}O navegador está aberto. Pressione Enter aqui quando terminar para fechá-lo...{Estilos.ENDC}")
        driver.quit()
        print(f"{Estilos.SUCCESS_ICON} Navegador fechado.")
    except Exception as e:
        print(f"{Estilos.ERROR_ICON} Erro ao abrir o navegador: {e}")

if __name__ == "__main__":
    open_browser_for_setup()