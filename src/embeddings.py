from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

#Generate the embeddings
embedding = get_embedding("How is the weather today?")
print(f"Dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")