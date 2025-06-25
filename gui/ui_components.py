# gui/ui_components.py

import customtkinter as ctk

class UIComponents:
    """Cria e gerencia todos os widgets da interface."""

    def __init__(self, master_frame: ctk.CTkFrame):
        # --- Seção de Configuração ---
        settings_label = ctk.CTkLabel(master_frame, text="Configurações", font=ctk.CTkFont(size=16, weight="bold"))
        settings_label.pack(pady=10, padx=20, anchor="w")

        ctk.CTkLabel(master_frame, text="Nome do Perfil Chrome:").pack(anchor="w", padx=20)
        self.profile_entry = ctk.CTkEntry(master_frame, placeholder_text="Ex: MeuPerfil")
        self.profile_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(master_frame, text="Nível do Rewards:").pack(anchor="w", padx=20)
        self.level_combo = ctk.CTkComboBox(master_frame, values=["1", "2"])
        self.level_combo.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(master_frame, text="Dispositivo Móvel Emulado:").pack(anchor="w", padx=20)
        mobile_devices = ["Pixel 5", "iPhone 12 Pro", "Samsung Galaxy S20 Ultra", "iPad Pro"]
        self.mobile_device_combo = ctk.CTkComboBox(master_frame, values=mobile_devices)
        self.mobile_device_combo.pack(fill="x", padx=20, pady=(0, 20))

        # --- Seção de Opções de Execução ---
        options_label = ctk.CTkLabel(master_frame, text="Opções de Execução", font=ctk.CTkFont(size=16, weight="bold"))
        options_label.pack(pady=10, padx=20, anchor="w")
        
        self.headless_check = ctk.CTkCheckBox(master_frame, text="Rodar em modo oculto (headless)")
        self.headless_check.pack(anchor="w", padx=20, pady=5)
        
        self.dashboard_check = ctk.CTkCheckBox(master_frame, text="Concluir tarefas do painel")
        self.dashboard_check.pack(anchor="w", padx=20, pady=5)
        
        self.desktop_search_check = ctk.CTkCheckBox(master_frame, text="Fazer pesquisas Desktop")
        self.desktop_search_check.pack(anchor="w", padx=20, pady=5)
        
        self.mobile_search_check = ctk.CTkCheckBox(master_frame, text="Fazer pesquisas Mobile")
        self.mobile_search_check.pack(anchor="w", padx=20, pady=(5, 20))
        
        self.dashboard_check.select()
        self.desktop_search_check.select()
        self.mobile_search_check.select()
        
        # --- Botões de Ação ---
        self.start_button = ctk.CTkButton(master_frame, text="Iniciar Automação")
        self.start_button.pack(fill="x", padx=20, pady=10)

        self.setup_button = ctk.CTkButton(master_frame, text="Abrir para Login Manual", fg_color="transparent", border_width=2)
        self.setup_button.pack(fill="x", padx=20, pady=5)

    def get_settings(self) -> dict:
        """Retorna um dicionário com todas as configurações atuais da UI."""
        return {
            "profile": self.profile_entry.get(),
            "level": self.level_combo.get(),
            "run_dashboard": self.dashboard_check.get(),
            "run_desktop_search": self.desktop_search_check.get(),
            "run_mobile_search": self.mobile_search_check.get(),
            "is_headless": self.headless_check.get(),
            "mobile_device": self.mobile_device_combo.get(),
        }