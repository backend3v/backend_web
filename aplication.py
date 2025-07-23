from flask import Flask, request
from flask import render_template
import os,json,subprocess
from services.bitoService import BitoService
from flask_cors import CORS,cross_origin
from dotenv import load_dotenv
load_dotenv()


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

        @self.app.route('/send-email', methods=['POST'])
        def send_email():
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            data = request.json
            to_email = data.get('to')
            subject = data.get('subject')
            message = data.get('message')

            if not to_email or not subject or not message:
                return self.getResponse({"error": "Missing 'to', 'subject' or 'message' in request."}, error=True)

            # Configuración del servidor SMTP (modifica según tu proveedor)
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', 587))
            smtp_user = os.environ.get('SMTP_USER')
            smtp_password = os.environ.get('SMTP_PASSWORD')

            if not smtp_user or not smtp_password:
                return self.getResponse({"error": "SMTP credentials not set in environment variables."}, error=True)

            try:
                msg = MIMEMultipart()
                msg['From'] = smtp_user
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, to_email, msg.as_string())
                server.quit()
                return self.getResponse({"success": True, "message": "Email sent successfully."})
            except Exception as e:
                return self.getResponse({"error": str(e)}, error=True)