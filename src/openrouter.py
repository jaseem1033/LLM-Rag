from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(
  base_url = "https://openrouter.ai/api/v1",
  api_key = api_key,
)

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