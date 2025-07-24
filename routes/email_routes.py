import os
from flask import request

def register_email_routes(app, getResponse):
    @app.route('/send-email', methods=['POST'])
    def send_email():
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        data = request.json
        to_email = data.get('to')
        subject = data.get('subject')
        message = data.get('message')

        if not to_email or not subject or not message:
            return getResponse({"error": "Missing 'to', 'subject' or 'message' in request."}, error=True)

        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_user = os.environ.get('SMTP_USER')
        smtp_password = os.environ.get('SMTP_PASSWORD')

        if not smtp_user or not smtp_password:
            return getResponse({"error": "SMTP credentials not set in environment variables."}, error=True)

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
            return getResponse({"success": True, "message": "Email sent successfully."})
        except Exception as e:
            return getResponse({"error": str(e)}, error=True) 