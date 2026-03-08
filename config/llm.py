"""
LLM initialization using Google Gemini
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GOOGLE_API_KEY, GEMINI_MODEL

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True  # Important for Gemini
)

# For faster/cheaper tasks, use Flash model
llm_fast = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True
)

print(f"✓ Gemini LLM initialized: {GEMINI_MODEL}")