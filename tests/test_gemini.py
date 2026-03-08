
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment
load_dotenv()

# Test 1: Check API key
print("Test 1: Checking API key...")
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"✓ API key found: {api_key[:20]}...")
else:
    print("✗ API key not found in .env")
    exit(1)

# Test 2: Initialize LLM
print("\nTest 2: Initializing Gemini...")
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",  # Use fast model for testing
        google_api_key=api_key,
        temperature=0.7
    )
    print("✓ Gemini initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize: {e}")
    exit(1)

# Test 3: Simple query
print("\nTest 3: Testing simple query...")
try:
    response = llm.invoke("Say 'Hello, I am Gemini and I'm working!'")
    print(f"✓ Response: {response.content}")
except Exception as e:
    print(f"✗ Query failed: {e}")
    exit(1)

# Test 4: Geopolitical query
print("\nTest 4: Testing geopolitical knowledge...")
try:
    response = llm.invoke("""
    In one sentence, what is the main tension between Iran and Israel?
    """)
    print(f"✓ Response: {response.content}")
except Exception as e:
    print(f"✗ Query failed: {e}")
    exit(1)

print("\n✅ All tests passed! Gemini is ready to use.")