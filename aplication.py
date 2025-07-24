from flask import Flask, request
from flask import render_template
import os,json,subprocess
from services.bitoService import BitoService
from flask_cors import CORS,cross_origin
from dotenv import load_dotenv
load_dotenv()
from services.scraperService import ScraperService
import concurrent.futures
from routes.prompt_routes import register_prompt_routes
from routes.email_routes import register_email_routes


class Aplication:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        CORS(self.app, origins="*")
        self._port = os.environ.get('PORT', 8000)

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