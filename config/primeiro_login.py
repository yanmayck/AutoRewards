from pathlib import Path
import json

def caminho_pasta(nomepasta: str = "Perfis_Chrome_Selenium") -> Path:
    usuario = Path.home()
    caminho_completo = usuario/nomepasta
    caminho_completo.mkdir(exist_ok=True)
    return caminho_completo

def precisa_configurar(nome_arquivo: str = "config.json", chave: str = "configuracao_feita") -> bool:
    """
    Verifica se a configuração precisa ser feita.
    """
    caminho_arquivo = Path(nome_arquivo)

    # Se o arquivo não existe, a configuração é necessária.
    if not caminho_arquivo.exists():
        return True

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if not isinstance(config, dict):
            return True # Se não for um dicionário, precisa reconfigurar.

        # A configuração NÃO é necessária APENAS se a chave existir e for True.
        # Em todos os outros casos, ela é necessária.
        if config.get(chave) is True:
            return False  # Já está configurado corretamente.
        else:
            return True   # Precisa configurar (chave não existe, valor é false, etc).

    except (json.JSONDecodeError, UnicodeDecodeError):
        # Se o arquivo for inválido, a configuração é necessária.
        return True
    except Exception:
        # Para qualquer outro erro, assumimos que a configuração é necessária.
        return True
    

def garantir_configuracao_feita(nome_arquivo: str = "config.json"):
    """
    Cria ou sobrescreve o arquivo de configuração para garantir que ele
    contenha {"configuracao_feita": true}.
    """
    print(f"--- Garantindo a configuração no arquivo '{nome_arquivo}' ---")
    caminho_arquivo = Path(nome_arquivo)
    
    # Define a estrutura final que queremos no arquivo
    config_correta = {
        "configuracao_feita": True
        # Você pode adicionar outras chaves padrão aqui se quiser
    }

    try:
        # Converte o dicionário para uma string JSON formatada
        conteudo_json = json.dumps(config_correta, indent=4, ensure_ascii=False)
        
        # Escreve/sobrescreve o arquivo com o conteúdo correto
        caminho_arquivo.write_text(conteudo_json, encoding='utf-8')
        
        print(f"✔️ Arquivo '{nome_arquivo}' criado/atualizado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: Não foi possível salvar o arquivo '{nome_arquivo}'.")
        print(f"Detalhe do erro: {e}")
        return False