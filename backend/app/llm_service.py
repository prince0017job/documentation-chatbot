from google import genai
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question, context):

    prompt = f"""
You are a documentation assistant.

Answer the user's question using ONLY the information provided
in the context below.

If the answer cannot be found in the context, say:
"I couldn't find this information in the provided documents."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    models = [
        "gemini-2.5-flash",
        "gemini-3-flash-preview"
    ]

    for model_name in models:

        for attempt in range(2):

            try:

                print(
                    f"Trying Gemini model: {model_name}, "
                    f"attempt: {attempt + 1}"
                )

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                print(
                    f"GEMINI ERROR ({model_name}):",
                    e
                )

                time.sleep(3)

    return (
        "The AI service is temporarily unavailable. "
        "Please try again in a few minutes."
    )