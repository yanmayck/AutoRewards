import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Início do Script ---

print("🤖 Iniciando o processo para abrir o navegador...")

try:
    # 1. Configura o serviço do Chrome usando o ChromeDriverManager.
    #    O .install() verifica a sua versão do Chrome e baixa o driver correto.
    servico = Service(ChromeDriverManager().install())

    # 2. Inicializa o navegador Chrome com o serviço configurado.
    #    É neste momento que a janela do navegador realmente abre.
    navegador = webdriver.Chrome(service=servico)
    
    # 3. (Opcional) Navega para um site específico.

    print("✅ Navegador aberto com sucesso!")
    print("⏳ A janela ficará aberta por 20 segundos.")
    input("digite enter: ")

    # 4. Mantém o navegador aberto por 20 segundos para que você possa vê-lo.
    time.sleep(20)

except Exception as e:
    print(f"❌ Ocorreu um erro: {e}")

finally:
    # 5. Garante que o navegador seja fechado ao final do script.
    if 'navegador' in locals() and navegador:
        navegador.quit()
        print("🛑 Navegador fechado.")