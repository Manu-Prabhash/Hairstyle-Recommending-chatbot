import requests
import os
from dotenv import load_dotenv

load_dotenv()

# TO USE: Create a .env file in the same directory and add: GROQ_API_KEY=your_actual_key_here
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def hair_chatbot_response(user_input):
    def is_hair_related(text):
        keywords = [
            "hair", "scalp", "dandruff", "hair fall", "hair loss", "dry scalp",
            "oily hair", "itchy scalp", "split ends", "hair growth", "bald",
            "alopecia", "hair thinning", "scalp infection", "hair care", "frizz",
            "shampoo", "conditioner", "hair treatment", "hair mask", "style"
        ]
        return any(keyword in text.lower() for keyword in keywords)

    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found. Please set it in your environment variables."

    if not is_hair_related(user_input):
        return "I specialize in hair and scalp care. Please ask a related question."

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a dermatology assistant specializing in hair and scalp care."
                    },
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.3
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"Request failed with status: {response.status_code}"
    except Exception as e:
        return "The service is currently unavailable. Please try again later."