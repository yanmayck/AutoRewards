from dotenv import load_dotenv,set_key, unset_key, find_dotenv
import os


load_dotenv()
caminho_user_data = os.getenv("CHROME_DATA_PATH")
nome_do_perfil = os.getenv("CHROME_BOT_PROFILE")
nivel = os.getenv("NIVEL")

def autocaminho(CHROME_DATA_PATH):
    dotenv_path = find_dotenv()
    if not dotenv_path:
        with open(".env","w"):
            pass
        dotenv_path = find_dotenv()
    set_key(dotenv_path,"CHROME_DATA_PATH",CHROME_DATA_PATH)
    set_key(dotenv_path,"CHROME_BOT_PROFILE","MeuPerfilPrincipal")
    set_key(dotenv_path,"NIVEL",1)