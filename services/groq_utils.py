import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq_model(prompt: str):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",  # Valid model name from Groq
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("❌ Groq SDK Error:", e)
        return "Error: Unable to generate response."
