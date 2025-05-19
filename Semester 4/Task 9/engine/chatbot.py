from transformers import pipeline

from engine.speech import speak
from dotenv import load_dotenv
import os

# Load Hugging Face token from .env
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

# Load the LLaMA 3.1 8B model pipeline with the token
chat_pipeline = pipeline(
    "text-generation",
    model="meta-llama/Llama-3.1-8B",
    token=hf_token,
    model_kwargs={"torch_dtype": "auto", "device_map": "auto"}  # Optional: faster on GPU
)

# Formal assistant system prompt
SYSTEM_PROMPT = (
    "You are a helpful, polite, and professional virtual assistant. "
    "Answer all user queries in a clear, relevant, and concise manner. "
    "If you don’t know something, say so honestly. Do not make up facts."
)

def chatBot(user_query):
    try:
        full_prompt = f"{SYSTEM_PROMPT}\nUser: {user_query}\nAssistant:"
        
        response = chat_pipeline(
            full_prompt,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            return_full_text=False
        )

        reply = response[0]["generated_text"].strip()
        #speak(reply)
        return reply

    except Exception as e:
        print("[chatBot ERROR]:", str(e))
        #speak("Sorry! Something went wrong connecting to the AI brain.")
        return "Sorry! Something went wrong connecting to the AI brain."
