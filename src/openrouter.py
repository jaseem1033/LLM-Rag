from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
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