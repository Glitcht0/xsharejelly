from flask import Flask
from src.Utils import CarregarEnv

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def create_app():
    app = Flask(__name__)

    # Secret key
    app.config["SECRET_KEY"] = "vsrw2342342343234234wfsdsdcvs"

    # Carrega variáveis
    API_KEY, JELLYFIN_URL = CarregarEnv()

    app.config["API_KEY"] = API_KEY
    app.config["JELLYFIN_URL"] = JELLYFIN_URL

    # Importa blueprints
    from routes.video import video_bp
    from routes.adm import admin_bp
    from routes.utils import utils_bp
    from routes.home import home_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(utils_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=9875, host="0.0.0.0")