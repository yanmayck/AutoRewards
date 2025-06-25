# gui/main_window.py

import sys
import subprocess
import threading
import customtkinter as ctk
from dotenv import set_key

# Importa as classes dos outros arquivos da GUI
from gui.utils import QueueHandler
from gui.ui_components import UIComponents
from gui.automation_handler import AutomationHandler

# Importa as classes do Core
from core.config import ConfigurationManager, Estilos

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Auto Rewards Bot")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configurações e Lógica
        self.config = ConfigurationManager()
        self.log_queue = QueueHandler()
        sys.stdout = self.log_queue
        
        # --- Layout Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        # Cria os componentes da UI
        self.ui = UIComponents(controls_frame)
        self._create_log_widgets(log_frame)

        # Conecta os botões às suas funções
        self.ui.start_button.configure(command=self._start_automation)
        self.ui.setup_button.configure(command=self._run_setup)

        # Carrega e inicia processos
        self._load_initial_config()
        self._start_log_polling()

    def _create_log_widgets(self, master_frame):
        log_label = ctk.CTkLabel(master_frame, text="Log de Atividades", font=ctk.CTkFont(size=16, weight="bold"))
        log_label.pack(pady=10, padx=10, anchor="w")
        
        self.log_textbox = ctk.CTkTextbox(master_frame, state="disabled", wrap="word")
        self.log_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _load_initial_config(self):
        """Carrega as configs do .env e preenche a UI."""
        self.ui.profile_entry.insert(0, self.config.profile_name or "MeuPerfilPrincipal")
        self.ui.level_combo.set(self.config.level or "1")
        self.ui.mobile_device_combo.set("Pixel 5")

    def _save_current_config(self):
        """Salva as configurações da UI no arquivo .env."""
        settings = self.ui.get_settings()
        set_key(self.config.env_path, "CHROME_BOT_PROFILE", settings["profile"])
        set_key(self.config.env_path, "NIVEL", settings["level"])
        
        self.config._load_env_vars()
        print(f"{Estilos.INFO_ICON} Configurações salvas no arquivo .env\n")

    def _start_automation(self):
        """Prepara e inicia a thread de automação."""
        self._save_current_config()
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        self.log_textbox.configure(state="disabled")

        settings = self.ui.get_settings()
        handler = AutomationHandler(settings, self.config)
        
        automation_thread = threading.Thread(target=handler.run)
        automation_thread.start()
        
        self._toggle_controls(False)
        self._check_thread(automation_thread)
    
    def _check_thread(self, thread):
        """Verifica se a thread ainda está rodando e reabilita os controles quando ela termina."""
        if thread.is_alive():
            self.after(100, lambda: self._check_thread(thread))
        else:
            self._toggle_controls(True)

    def _toggle_controls(self, is_enabled):
        """Habilita ou desabilita os controles durante a execução."""
        state = "normal" if is_enabled else "disabled"
        for widget in [self.ui.profile_entry, self.ui.level_combo, self.ui.mobile_device_combo,
                       self.ui.headless_check, self.ui.dashboard_check, self.ui.desktop_search_check,
                       self.ui.mobile_search_check, self.ui.setup_button]:
            widget.configure(state=state)
        
        if is_enabled:
            self.ui.start_button.configure(text="Iniciar Automação", state="normal")
        else:
            self.ui.start_button.configure(text="Executando...", state="disabled")

    def _start_log_polling(self):
        """Verifica a fila de logs e atualiza a UI."""
        try:
            while not self.log_queue.empty():
                message = self.log_queue.get()
                self.log_textbox.configure(state="normal")
                self.log_textbox.insert("end", message)
                self.log_textbox.configure(state="disabled")
                self.log_textbox.see("end")
            self.after(100, self._start_log_polling)
        except Exception:
            pass
            
    def _run_setup(self):
        """Abre o navegador para configuração manual."""
        print("Abrindo navegador para configuração manual...")
        subprocess.Popen([sys.executable, 'setup.py'])