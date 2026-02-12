from groq import Groq, RateLimitError, APIError, APITimeoutError
import time
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

def call_llm_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            print("Inside try")
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "What is google?"
                    }
                ],
                timeout=30.0, # 30 second timeout
                max_tokens=200
            )
            return response.choices[0].message.content

        except RateLimitError:
            # Wait and retry
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)

        except APITimeoutError:
            print("Request timed out. Retrying...")
            continue

        except APIError as e:
            print(f"API error: {e}")
            raise

    raise Exception("Max retries exceeded")

print(call_llm_with_retry())