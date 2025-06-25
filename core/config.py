# core/config.py

import os
import json
from pathlib import Path
from dotenv import load_dotenv, set_key, find_dotenv

class ConfigurationManager:
    """Gerencia as configurações do projeto, lendo e escrevendo nos arquivos .env e config.json."""
    
    def __init__(self, env_file_name=".env", config_file_name="config.json"):
        self.env_path = find_dotenv(env_file_name)
        if not self.env_path:
            # Cria o arquivo .env se ele não existir no projeto
            env_path_obj = Path(env_file_name)
            env_path_obj.touch()
            self.env_path = str(env_path_obj.resolve())

        self.config_file_path = Path(config_file_name)
        self._load_env_vars()

    def _load_env_vars(self):
        """Carrega as variáveis de ambiente do arquivo .env para os atributos da classe."""
        load_dotenv(dotenv_path=self.env_path)
        self.user_data_path = os.getenv("CHROME_DATA_PATH")
        self.profile_name = os.getenv("CHROME_BOT_PROFILE")
        self.level = os.getenv("NIVEL")

    def is_first_run(self) -> bool:
        """Verifica se é a primeira execução com base na existência e conteúdo do config.json."""
        if not self.config_file_path.exists():
            return True
        try:
            with self.config_file_path.open('r', encoding='utf-8') as f:
                config_data = json.load(f)
            return config_data.get("configuracao_feita") is not True
        except (json.JSONDecodeError, TypeError):
            return True

    def perform_initial_setup(self, base_dir_name: str = "Perfis_Chrome_Selenium", profile_name: str = "MeuPerfilPrincipal", level: str = "1"):
        """Executa os passos de configuração inicial: cria a pasta do perfil e o arquivo .env."""
        print("--- Realizando configuração inicial ---")
        user_home = Path.home()
        chrome_data_path = user_home / base_dir_name
        chrome_data_path.mkdir(exist_ok=True)

        set_key(self.env_path, "CHROME_DATA_PATH", str(chrome_data_path))
        set_key(self.env_path, "CHROME_BOT_PROFILE", profile_name)
        set_key(self.env_path, "NIVEL", level)
        print(f"{Estilos.SUCCESS_ICON} Arquivo .env configurado com sucesso em: '{self.env_path}'")
        
        # Recarrega as variáveis para a instância atual
        self._load_env_vars()

    def mark_setup_as_complete(self):
        """Cria/sobrescreve o config.json para marcar a configuração como concluída."""
        config_data = {"configuracao_feita": True}
        try:
            with self.config_file_path.open('w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
            print(f"{Estilos.SUCCESS_ICON} Arquivo '{self.config_file_path.name}' salvo com sucesso!")
        except IOError as e:
            print(f"{Estilos.ERROR_ICON} ERRO: Não foi possível salvar o arquivo de configuração. Detalhe: {e}")

class Estilos:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    INFO_ICON = "ℹ️ "
    SUCCESS_ICON = "✅"
    WAIT_ICON = "⏳"
    CARD_ICON = "🃏"
    TAB_ICON = "📑"
    ERROR_ICON = "❌"
    ROBOT_ICON = "🤖"

# Mantido do arquivo original config/config.py
total_pesquisas = [
    "o que é a teoria da relatividade", "quem foi Santos Dumont", "fases da lua em 2025",
    "maiores desertos do mundo", "história da invenção do telefone", "o que é blockchain",
    "melhores celulares custo-benefício 2025", "como funciona a internet 5G", "próximos lançamentos da Netflix",
    "filmes em cartaz nos cinemas", "vencedores do Oscar de melhor filme", "pontos turísticos de Caldas Novas, GO",
    "melhores praias do Nordeste brasileiro", "o que fazer em Pirenópolis", "receita de pamonha goiana",
    "como fazer feijoada completa", "benefícios do pequi para a saúde", "animais em extinção no Cerrado",
    "planetas do sistema solar em ordem", "exercícios para fazer em casa", "benefícios da meditação guiada",
    "cotação do dólar hoje", "resultados do campeonato brasileiro", "previsão do tempo para amanhã"
]