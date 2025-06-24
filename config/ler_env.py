# config/ler_env.py

from dotenv import load_dotenv, set_key, find_dotenv
import os
from pathlib import Path # Importar Path para o type hint

load_dotenv()
caminho_user_data = os.getenv("CHROME_DATA_PATH")
nome_do_perfil = os.getenv("CHROME_BOT_PROFILE")
nivel = os.getenv("NIVEL")

def autocaminho(CHROME_DATA_PATH: Path): # O parâmetro recebido é um objeto Path
    dotenv_path = find_dotenv()
    if not dotenv_path:
        with open(".env", "w"):
            pass
        dotenv_path = find_dotenv()
    
    # CORREÇÃO: Converta os valores para string antes de salvar
    set_key(dotenv_path, "CHROME_DATA_PATH", str(CHROME_DATA_PATH)) # <<<---- CORRIGIDO AQUI
    set_key(dotenv_path, "CHROME_BOT_PROFILE", "MeuPerfilPrincipal")
    set_key(dotenv_path, "NIVEL", "1") # <<<---- CORRIGIDO AQUI (passar como string)