import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Read Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_response(prompt: str) -> str:
    """
    Generate an AI response using Groq.
    """

    # Check whether API key exists
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from .env file")

    # Create Groq client
    client = Groq(api_key=GROQ_API_KEY)

    # Send request to Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_completion_tokens=1024
    )

    # Extract generated answer
    answer = response.choices[0].message.content

    return answer.strip()