# core/browser.py (Versão Corrigida e Melhorada)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from .config import Estilos

class BrowserManager:
    """Gerencia a criação de drivers do Selenium para diferentes plataformas."""

    def __init__(self, config_manager):
        self.config = config_manager
        if not self.config.user_data_path or not self.config.profile_name:
            raise ValueError("Caminho do perfil ou nome do perfil não definidos na configuração.")

    def _get_common_options(self) -> Options:
        """Cria e retorna as opções base do Chrome com o perfil do usuário."""
        options = Options()
        options.add_argument(f"--user-data-dir={self.config.user_data_path}")
        options.add_argument(f"--profile-directory={self.config.profile_name}")
        
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        return options

    def get_desktop_driver(self, is_headless: bool = False) -> webdriver.Chrome:
        """
        Retorna um driver do Chrome configurado para desktop.
        Aceita um parâmetro para rodar em modo headless.
        """
        print(f"{Estilos.ROBOT_ICON}{Estilos.BLUE} Iniciando navegador Desktop...{Estilos.ENDC}")
        options = self._get_common_options()
        options.add_argument("--start-maximized")
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        if is_headless:
            print(f"{Estilos.INFO_ICON} Modo Headless ATIVADO para Desktop.\n")
            options.add_argument("--headless=new")
        
        service = ChromeService(executable_path=ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def get_mobile_driver(self, device_name: str = "Pixel 5", is_headless: bool = False) -> webdriver.Chrome:
        """
        Retorna um driver do Chrome com emulação de dispositivo móvel.
        Também aceita o parâmetro is_headless.
        """
        print(f"{Estilos.ROBOT_ICON}{Estilos.CYAN} Iniciando navegador Mobile emulando '{device_name}'...{Estilos.ENDC}")
        options = self._get_common_options()
        
        mobile_emulation = { "deviceName": device_name }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        if is_headless:
            print(f"{Estilos.INFO_ICON} Modo Headless ATIVADO para Mobile.\n")
            options.add_argument("--headless=new")
        
        service = ChromeService(executable_path=ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)