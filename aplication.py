from flask import Flask, request
from flask import render_template
import os,json,subprocess
from services.bitoService import BitoService
from flask_cors import CORS,cross_origin
from dotenv import load_dotenv
load_dotenv()
import concurrent.futures
from routes.prompt_routes import register_prompt_routes
from routes.email_routes import register_email_routes
from routes.blog_routes import blog_bp
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class Aplication:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        CORS(self.app, origins="*")
        self._port = os.environ.get('PORT', 8080)

    def run(self):
        self.routes()
        self.app.run(host='0.0.0.0', port=self._port)

    def getResponse(self,data,error=False):
        statusCode=200
        if error:
            statusCode=500
        response = self.app.response_class(
                response=json.dumps(data),
                status=statusCode,
                mimetype='application/json'
            )
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
        return response

    def routes(self):
        @self.app.route('/')
        def index():
            data = {"a":"1234567897865476"}
            return self.getResponse(data)

        register_prompt_routes(self.app, self.getResponse)
        register_email_routes(self.app, self.getResponse)
        self.app.register_blueprint(blog_bp, url_prefix='/blog')

        # Ruta catch-all para SPA (sirve index.html para rutas no-API)
        from flask import send_from_directory
        @self.app.route('/<path:path>')
        def serve_vue_app(path):
            # Si la ruta es de API, deja que Flask la maneje
            if path.startswith('api') or path.startswith('blog'):
                return "Not found", 404
            static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../portafolio3d/dist'))
            # Sirve archivos estáticos si existen
            if os.path.exists(os.path.join(static_folder, path)):
                return send_from_directory(static_folder, path)
            # Si no, sirve index.html para rutas SPA
            return send_from_directory(static_folder, 'index.html')