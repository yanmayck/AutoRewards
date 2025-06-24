from config.config import configurar_navegador,Estilos
from config.ler_env import nome_do_perfil, caminho_user_data
from selenium.webdriver.support.ui import WebDriverWait


try:
    driver = configurar_navegador(caminho_user_data,nome_do_perfil)
    input("digite enter para fechar")
    wait = WebDriverWait(driver, 20)


except:
    print(f"{Estilos.ERROR_ICON}{Estilos.WARNING}algo deu errado {Estilos.ERROR_ICON}")

finally:
    driver.quit()
    print(f"{Estilos.GREEN}{Estilos.SUCCESS_ICON}comfiguração completa!!{Estilos.SUCCESS_ICON}")