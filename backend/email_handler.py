import base64
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the required Gmail API scope
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """
    Authenticate the user with Gmail API using OAuth 2.0.
    Returns an authenticated service object.
    """
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def fetch_primary_emails():
    """
    Fetch primary category emails from Gmail inbox.
    Returns a list of email dictionaries (id, sender, subject, body).
    """
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    # Fetch only primary emails
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="category:primary").execute()
    messages = results.get("messages", [])

    email_list = []
    for msg in messages[:5]:  # Limit to 5 emails
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        payload = msg_data["payload"]
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")

        # Extract email body (handle different formats)
        body = "No content"
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain" and "data" in part["body"]:
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                    break
        elif "body" in payload and "data" in payload["body"]:
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

        email_list.append({
            "email_id": msg["id"],
            "sender": sender,
            "subject": subject,
            "body": body,
        })

    return email_list


def send_email(recipient, subject, body):
    """
    Send an email using SMTP (Gmail).
    """
    sender_email = "your-email@gmail.com"
    sender_password = "your-app-password"  # Generate App Password from Google

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")
