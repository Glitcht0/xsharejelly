from flask import Blueprint, render_template, redirect, request
import json
import re
from src.Utils import carregar_videos


admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/add", methods=["GET", "POST"])
def add_video():
    mensagem = None
    erro = False

    if request.method == "POST":
        nome = request.form.get("nome")
        link_ou_id = request.form.get("link_ou_id")
        senha = request.form.get("senha")

        if senha == "adicionar62254":
            if nome and link_ou_id:
                match = re.search(r'([a-fA-F0-9]{32})', link_ou_id)
                if match:
                    video_id = match.group(1)
                    videos_db = carregar_videos()
                    
                    if nome in videos_db:
                        return render_template("add_video.html", mensagem=f"Erro: Já existe um vídeo com o nome '{nome}'.", erro=True)
                    
                    videos_db[nome] = video_id
                    with open("videos.json", "w", encoding="utf-8") as arquivo:
                        json.dump(videos_db, arquivo, indent=4)

                    linkVideo = f"https://play.glitcht.org/play/{nome}"
                    mensagem = f"Sucesso! ID extraído: {video_id} | Link: {linkVideo}"
                else:
                    mensagem = "Erro: Não encontrei um ID válido de 32 caracteres."
                    erro = True
            else:
                mensagem = "Preencha todos os campos."
                erro = True
        else:
            mensagem = "Senha incorreta!"
            erro = True

    return render_template("add_video.html", mensagem=mensagem, erro=erro)



