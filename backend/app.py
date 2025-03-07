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
    send_email(data["recipient"], data["subject"], data["body"])
    return jsonify({"message": "Email sent successfully"})
@app.route("/api/ai-response", methods=["POST"])
def ai_response():
    data = request.json
    response = generate_ai_response(data["email_text"])
    return jsonify({"response": response})
if __name__ == "__main__":
    app.run(debug=True, port=5000)
