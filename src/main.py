from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

def classify_ticket(ticket_text: str) -> dict:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": """Classify support tickets into categories.
                Return JSON with: category, priority,summary
                Categories: billing, technical, account, general
                Prorities: low, medium, high, urgent"""
            },
            {
                "role": "user",
                "content": ticket_text
            }
    ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)

ticket = "I have been charged twice for my subscription this month!"
result = classify_ticket(ticket)
print(result)