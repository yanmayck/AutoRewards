# main.py

from auto.altomacao import main
from config.primeiro_login import caminho_pasta, precisa_configurar, garantir_configuracao_feita
from config.ler_env import autocaminho, caminho_user_data, nome_do_perfil # <<<---- IMPORTADO AQUI
from config.config import configurar_navegador

if __name__ == "__main__":
    if precisa_configurar():
        try:
            # Passa o retorno de caminho_pasta() para a função autocaminho
            autocaminho(caminho_pasta())
            
            # Chama a configuração do navegador, que abre e fecha o browser para criar o perfil
            # É importante ter os valores de .env já carregados
            print("Configurando o navegador pela primeira vez...")
            driver_config = configurar_navegador(caminho_user_data, nome_do_perfil) # <<<---- CORRIGIDO AQUI
            input("Precione Enter: ")
            driver_config.quit() # Fecha o navegador após a configuração inicial
            
            # Marca que a configuração foi feita
            garantir_configuracao_feita()
            print("Configuração inicial finalizada. O robô começará na próxima execução.")

        except Exception as e:
            print(f"❌ Ocorreu um erro durante a configuração inicial: {e}")
            print("Por favor, tente rodar o programa novamente.")
    
        # Se a configuração não for necessária, executa o robô principal
    try:       
        main()
    except KeyboardInterrupt:
        print("\nPrograma finalizado pelo usuário.")
    except Exception as e:
        print(f"Ocorreu um erro durante a execução do programa: {e}")