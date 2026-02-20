from flask import Blueprint, render_template, redirect, request, current_app

from src.Utils import carregar_videos
from src.Audio import obter_audio_pt




video_bp = Blueprint("video", __name__)



@video_bp.route("/play")
def play_redirect():
    nome = request.args.get("nome_video")
    return redirect(f"/play/{nome}")



@video_bp.route("/play/<video_nome>")
def play_video(video_nome):
    api_key = current_app.config["API_KEY"]
    jelly_url = current_app.config["JELLYFIN_URL"]

    videos_db = carregar_videos()
    if video_nome not in videos_db:
        return render_template("home.html", mensagem=f"Erro: O vídeo '{video_nome}' não foi encontrado.", erro=True)
    
    item_id = videos_db[video_nome]
    indice_audio_pt = obter_audio_pt(item_id, api_key, jelly_url)
    
    # URL da Playlist HLS com parâmetros de compatibilidade máxima para AVI/MKV antigos
    # URL da Playlist HLS com parâmetros de compatibilidade máxima para AVI/MKV antigos
    # URL da Playlist HLS com parâmetros de compatibilidade máxima para AVI/MKV antigos
    hls_url = (
        f"/Videos/{item_id}/master.m3u8"
        f"?MediaSourceId={item_id}"
        f"&VideoCodec=av1,h264"           # Devolvemos o AV1! O Jellyfin não vai mais estragar a qualidade.
        f"&AudioCodec=aac,mp3"
        f"&SegmentContainer=mp4"          # OBRIGATÓRIO: A única forma do player web aceitar AV1 sem dar tela preta.
        f"&TranscodingMaxAudioChannels=2" # Mantém o áudio estéreo seguro para o navegador.
    )
    
    if indice_audio_pt is not None:
        hls_url += f"&AudioStreamIndex={indice_audio_pt}"
        
    return render_template("player.html", nome=video_nome, hls_url=hls_url)