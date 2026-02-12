from langchain_huggingface import HuggingFaceEmbeddings


# Load model ONCE
embedding_model = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1",
    model_kwargs={"trust_remote_code": True}
)

def get_embedding(text: str) -> list[float]:
    return embedding_model.embed_query(text)


if __name__ == "__main__":
    text = "How is the weather today?"  
    embedding = get_embedding(text)

    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
