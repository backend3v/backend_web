from flask import Flask, request
from flask import render_template
import os,json,subprocess
from services.bitoService import BitoService
from flask_cors import CORS,cross_origin



class Aplication:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self._port = os.environ.get('PORT', 8000)

    def run(self):
        self.routes()
        self.app.run(host='0.0.0.0', port=self._port)

    def getResponse(self,data,error=False):
        statusCode=200
        if error:
            statusCode=500
        response = self.app.response_class(
                response=data,
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

        @self.app.route('/prompt', methods=['POST'])
        def prompt():
            data = request.json
            prompt_text = data.get('prompt')
            lang = data.get('lang')
            #prompt_text = "Quien es el presidente de Argentina?"
            if not prompt_text:
                return json.dumps({"error": "Missing prompt text"}), 400
            try:
                BS = BitoService(lang)
                result = BS.setConsult(prompt_text)
                #print(result)
                #result = result.replace('```json','').replace('```','')
                #result = BS.test()

                return self.getResponse(result)
            except subprocess.CalledProcessError as e:
                return self.getResponse(data={"error": str(e), "output": e.output},error=True)