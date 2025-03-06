import openai

openai.api_key = "your_openai_api_key"

def generate_ai_response(email_text):
    """Generate AI-powered response based on email text."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": email_text}]
    )
    return response["choices"][0]["message"]["content"]
