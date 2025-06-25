# gui/automation_handler.py

import traceback
from core.bot import RewardsBot
from core.config import ConfigurationManager, Estilos, total_pesquisas
from core.browser import BrowserManager

class AutomationHandler:
    """Lida com a execução da lógica de automação do Selenium."""
    
    def __init__(self, settings: dict, config_manager: ConfigurationManager):
        self.settings = settings
        self.config = config_manager
        
    def run(self):
        """Executa o fluxo de automação com base nas configurações fornecidas."""
        try:
            print(f"{Estilos.ROBOT_ICON} Iniciando o processo de automação...")
            browser_manager = BrowserManager(self.config)

            # --- Automação Desktop ---
            if self.settings["run_dashboard"] or self.settings["run_desktop_search"]:
                print("\n--- Iniciando etapa Desktop ---")
                desktop_driver = browser_manager.get_desktop_driver(is_headless=self.settings["is_headless"])
                bot = RewardsBot(desktop_driver, self.config)
                if self.settings["run_dashboard"]:
                    bot.complete_dashboard_tasks()
                if self.settings["run_desktop_search"]:
                    bot.perform_searches(total_pesquisas, search_type="Desktop")
                desktop_driver.quit()
                print("--- Etapa Desktop finalizada com sucesso ---\n")

            # --- Automação Mobile ---
            if self.settings["run_mobile_search"]:
                print("\n--- Iniciando etapa Mobile ---")
                mobile_driver = browser_manager.get_mobile_driver(
                    device_name=self.settings["mobile_device"], 
                    is_headless=self.settings["is_headless"]
                )
                bot = RewardsBot(mobile_driver, self.config)
                bot.perform_searches(total_pesquisas, search_type="Mobile")
                mobile_driver.quit()
                print("--- Etapa Mobile finalizada com sucesso ---\n")
            
            print(f"{Estilos.SUCCESS_ICON} Automação concluída!")

        except Exception as e:
            print(f"{Estilos.ERROR_ICON} Um erro crítico ocorreu: {e}\n{traceback.format_exc()}")