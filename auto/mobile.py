from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def iniciar_chrome_mobile(caminho_perfil_chrome: str, nome_do_perfil: str, nome_do_dispositivo: str, user_agent: str) -> webdriver.Chrome | None:
    try:
        print(f"Iniciando Chrome com perfil '{nome_do_perfil}'...")
        print(f"Emulando tela de: '{nome_do_dispositivo}'")
        
        chrome_options = Options()
        
        # 1. Carrega seu perfil de usuário (cookies, logins, etc.)
        chrome_options.add_argument(f"--user-data-dir={caminho_perfil_chrome}")
        chrome_options.add_argument(f"--profile-directory={nome_do_perfil}")
        
        # 2. Comando de SPOOFING: Define a identidade falsa (User-Agent)
        print(f"Fazendo spoofing com User-Agent: '{user_agent[:70]}...'")
        chrome_options.add_argument(f"user-agent={user_agent}")
        
        # 3. Emula o tamanho da tela do dispositivo
        mobile_emulation = {"deviceName": nome_do_dispositivo}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Inicializa o driver com todas as opções configuradas
        driver_mobile = webdriver.Chrome(options=chrome_options)
        
        print("\nDriver iniciado com sucesso em modo de emulação completa!")
        return driver_mobile

    except Exception as e:
        print(f"ERRO ao iniciar o driver: {e}")
        print("Verifique se o caminho do perfil está correto e se o Chrome não está aberto com esse perfil.")
        return None