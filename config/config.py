from dotenv import load_dotenv
import os
    
    
    
    
    
total_pesquisas = [
    # Perguntas Gerais e Curiosidades
    "o que é a teoria da relatividade",
    "quem foi Santos Dumont",
    "fases da lua em 2025",
    "maiores desertos do mundo",
    "história da invenção do telefone",
    "quantos países existem no mundo",
    "o que significa a sigla UNESCO",
    "como fazer um nó de gravata",
    
    # Tecnologia e Internet
    "o que é blockchain",
    "melhores celulares custo-benefício 2025",
    "Python vs JavaScript qual usar",
    "como funciona a internet 5G",
    "lançamentos de placas de vídeo",
    "o que é um ataque de phishing",
    "história da Microsoft",
    
    # Cultura Pop e Entretenimento
    "próximos lançamentos da Netflix",
    "filmes em cartaz nos cinemas",
    "músicas mais tocadas no Spotify Brasil",
    "vencedores do Oscar de melhor filme",
    "biografia da Anitta",
    "jogos mais esperados do ano",
    "o que é um dorama",
    
    # Viagens e Geografia (com toque local)
    "pontos turísticos de Caldas Novas, GO",
    "melhores praias do Nordeste brasileiro",
    "o que fazer em Pirenópolis",
    "qual a capital da Nova Zelândia",
    "clima em Gramado, RS",
    "sete maravilhas do mundo moderno",
    "Parque Nacional da Chapada dos Veadeiros",
    "Rio Araguaia",
    
    # Culinária e Receitas (com toque local)
    "receita de pamonha goiana",
    "como fazer feijoada completa",
    "benefícios do pequi para a saúde",
    "melhores vinhos para iniciantes",
    "receita de bolo de fubá cremoso",
    "como temperar frango para assar",
    "comidas típicas do Centro-Oeste",
    
    # Ciência e Natureza
    "animais em extinção no Cerrado",
    "planetas do sistema solar em ordem",
    "como as abelhas produzem mel",
    "o que são buracos negros",
    "curiosidades sobre o corpo humano",
    "tipos de rochas",
    
    # Saúde e Bem-estar
    "exercícios para fazer em casa",
    "benefícios da meditação guiada",
    "receitas de lanches saudáveis",
    "como melhorar a qualidade do sono",
    "dicas para beber mais água",
    
    # Notícias e Assuntos Gerais
    "cotação do dólar hoje",
    "resultados do campeonato brasileiro",
    "previsão do tempo para amanhã",
    "notícias de economia no Brasil",
    "principais índices da bolsa de valores",
]

class Estilos:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INFO_ICON = "ℹ️ "
    SUCCESS_ICON = "✅"
    WAIT_ICON = "⏳"
    CARD_ICON = "🃏"
    TAB_ICON = "📑"
    ERROR_ICON = "❌"
    STOP_ICON = "🛑"
    ROBOT_ICON = "🤖"


load_dotenv()
caminho_user_data = os.getenv("CHROME_DATA_PATH")
nome_do_perfil = os.getenv("CHROME_BOT_PROFILE")
nivel = os.getenv("NIVEL")