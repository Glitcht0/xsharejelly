
import requests


def obter_audio_pt(item_id, API_KEY, JELLYFIN_URL):
    """
    Pergunta ao Jellyfin os detalhes do vídeo e procura a trilha de áudio em PT/POR.
    Retorna o 'Index' (número da trilha) ou None se não achar.
    """
    url_info = f"{JELLYFIN_URL}/Items?Ids={item_id}&Fields=MediaSources"
    headers = {"X-Emby-Token": API_KEY}
    
    try:
        resposta = requests.get(url_info, headers=headers).json()
        # Navega no JSON de resposta do Jellyfin para achar os streams do vídeo
        streams = resposta["Items"][0]["MediaSources"][0]["MediaStreams"]
        
        for stream in streams:
            if stream.get("Type") == "Audio":
                # Pega a linguagem do áudio (ex: 'eng', 'por', 'pt')
                lingua = stream.get("Language", "").lower()
                
                # Se for português, retorna o número dessa trilha
                if lingua in ["por", "pt", "pt-br", "pb"]:
                    return stream.get("Index")
    except Exception as e:
        print(f"Erro ao buscar áudio: {e}")
        
    return None # Se não achar português ou der erro, devolve None