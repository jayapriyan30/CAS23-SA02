from flask import Flask, jsonify, request
from flask_cors import CORS
from email_handler import fetch_primary_emails, send_email
from ai_response import generate_ai_response

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

@app.route("/api/emails", methods=["GET"])
def get_emails():
    """Fetch primary emails from Gmail."""
    return jsonify(fetch_primary_emails())

@app.route("/api/ai-response", methods=["POST"])
def ai_response():
    """Generate an AI-powered email response."""
    data = request.json
    response = generate_ai_response(data["email_text"])
    return jsonify({"response": response})

@app.route("/api/send-email", methods=["POST"])
def send_email_api():
    """Send an email response using Gmail SMTP."""
    data = request.json
    send_email(data["recipient"], data["subject"], data["body"])
    return jsonify({"message": "Email sent successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
