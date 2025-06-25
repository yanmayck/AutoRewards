# core/bot.py

import time
import random
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from .config import Estilos

class RewardsBot:
    """Encapsula toda a lógica de automação do Microsoft Rewards."""

    def __init__(self, driver: WebDriver, config_manager):
        self.driver = driver
        self.config = config_manager
        self.wait = WebDriverWait(self.driver, 20)
        self.rewards_url = "https://rewards.bing.com/"
        self.bing_url = "https://www.bing.com/"

    def _process_task_tab(self, original_tab_handle: str):
        """Muda para a nova aba da tarefa, aguarda, fecha e retorna à original."""
        self.wait.until(EC.number_of_windows_to_be(2))
        for handle in self.driver.window_handles:
            if handle != original_tab_handle:
                self.driver.switch_to.window(handle)
                break
        
        print(f"{Estilos.TAB_ICON}   Aba da tarefa em foco. Aguardando 5 segundos...")
        time.sleep(5)
        self.driver.close()
        self.driver.switch_to.window(original_tab_handle)
        print(f"{Estilos.TAB_ICON}   Aba da tarefa fechada, retornando ao painel.")

    def complete_dashboard_tasks(self):
        """Executa as tarefas do painel principal do Rewards."""
        print(f"\n{Estilos.BOLD}--- Iniciando conclusão de tarefas do painel ---{Estilos.ENDC}")
        self.driver.get(self.rewards_url)
        
        card_locator = (By.CSS_SELECTOR, ".ds-card-sec.ng-scope")
        print(f"{Estilos.WAIT_ICON} Aguardando cartões de tarefa...")
        try:
            cards = self.wait.until(EC.presence_of_all_elements_located(card_locator))
            print(f"{Estilos.SUCCESS_ICON} {len(cards)} cartões encontrados.")
        except TimeoutException:
            print(f"{Estilos.WARNING} Nenhum cartão de tarefa encontrado ou a página não carregou. Pulando esta etapa.")
            return

        original_tab = self.driver.current_window_handle
        
        for i in range(len(cards)):
            try:
                # Re-localiza os cartões para evitar StaleElementReferenceException
                current_card = self.wait.until(EC.presence_of_all_elements_located(card_locator))[i]
                
                if "disabled" in current_card.get_attribute("class"):
                    print(f"{Estilos.INFO_ICON} Cartão #{i+1} está desabilitado. Pulando.")
                    continue
                
                print(f"\n{Estilos.CARD_ICON} Processando Cartão #{i+1}...")
                current_card.click()
                self._process_task_tab(original_tab)
                print(f"{Estilos.SUCCESS_ICON} Cartão #{i+1} processado.")

            except StaleElementReferenceException:
                print(f"{Estilos.WARNING}   Ocorreu um erro de referência (Stale). Tentando novamente na próxima iteração.")
                continue
            except Exception as e:
                print(f"{Estilos.ERROR_ICON}   Erro ao processar o cartão #{i+1}: {e}")
                self.driver.switch_to.window(original_tab) # Garante o retorno à aba principal

    def perform_searches(self, search_terms: list, search_type: str = "Desktop"):
        """Realiza pesquisas aleatórias no Bing."""
        num_searches = 30 if self.config.level == "2" else 10 # Nível 1 faz 10, Nível 2 faz 30
        if search_type.lower() == 'mobile':
            num_searches = 20 # Exemplo: 20 pesquisas para mobile
        
        print(f"\n{Estilos.BOLD}--- Iniciando {num_searches} pesquisas ({search_type}) ---{Estilos.ENDC}")
        search_field_locator = (By.ID, "sb_form_q")

        for i in range(num_searches):
            term = random.choice(search_terms)
            print(f"  Pesquisa #{i+1}/{num_searches}: '{term}'")
            try:
                self.driver.get(self.bing_url)
                search_field = self.wait.until(EC.visibility_of_element_located(search_field_locator))
                search_field.clear()
                search_field.send_keys(term)
                search_field.submit()
                time.sleep(random.uniform(2, 4))
            except Exception as e:
                print(f"{Estilos.FAIL}    Erro na pesquisa #{i+1}: {e}{Estilos.ENDC}")
                continue