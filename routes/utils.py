from flask import Blueprint, render_template, redirect, request, Response, current_app
import requests



utils_bp = Blueprint("utils", __name__)




# Rota Proxy Universal (Gere todos os pedidos HLS, como ficheiros .m3u8 e .ts)
@utils_bp.route("/Videos/<path:subpath>")
def jellyfin_proxy(subpath):
    api_key = current_app.config["API_KEY"]
    jelly_url = current_app.config["JELLYFIN_URL"]
    target_url = f"{jelly_url}/Videos/{subpath}"
    headers = {"X-Emby-Token": api_key}
    
    if "Range" in request.headers:
        headers["Range"] = request.headers["Range"]

    req = requests.get(target_url, headers=headers, params=request.args, stream=True)

    def generate():
        for chunk in req.iter_content(chunk_size=65536):
            if chunk:
                yield chunk

    response_headers = { 'Content-Type': req.headers.get('Content-Type')}
    if 'Content-Length' in req.headers:
        response_headers['Content-Length'] = req.headers['Content-Length']
    if 'Content-Range' in req.headers:
        response_headers['Content-Range'] = req.headers['Content-Range']

    return Response(generate(), status=req.status_code, headers=response_headers)
