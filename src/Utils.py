import json
import os
from dotenv import load_dotenv


def carregar_videos():
    try:
        with open("videos.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}
    



def CarregarEnv():
    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    JELLYFIN_URL = os.getenv("JELLYFIN_URL")

    if not API_KEY or not JELLYFIN_URL:
        raise Exception("Variaveis de ambiente nao carregadas")

    return API_KEY, JELLYFIN_URL