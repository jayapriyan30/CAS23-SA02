from flask import Flask, jsonify, request
from flask_cors import CORS
from email_handler import fetch_primary_emails, send_email

app = Flask(__name__)
CORS(app) 

@app.route("/api/emails", methods=["GET"])
def get_emails():
    return jsonify(fetch_primary_emails())

@app.route("/api/send-email", methods=["POST"])
def send_email_api():
    data = request.json
    recipient = data["recipient"]
    subject = data["subject"]
    body = data["body"]
    
    send_email(recipient, subject, body)
    return jsonify({"message": "Email sent successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

