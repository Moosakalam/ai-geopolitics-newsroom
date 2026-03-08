"""
Configuration settings for the geopolitical agent system
Using Google Gemini API
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("gemini-2.5-flash-lite", "gemini-2.5-flash-lite")

# Alternative models available:
# - gemini-1.5-pro (best quality, more expensive)
# - gemini-1.5-flash (faster, cheaper)
# - gemini-pro (older, cheaper)

# Validate API key
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# News API Configuration
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

# Agent Settings
VERBOSE_MODE = True
MAX_ITERATIONS = 10
ALLOW_DELEGATION = True

# Search Settings
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", 20))
NEWS_SOURCES = [
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "aljazeera.com",
    "timesofisrael.com"
]

# Output Settings
OUTPUT_DIR = "outputs"
ARTICLE_LENGTH = int(os.getenv("ARTICLE_LENGTH", 1500))
OUTPUT_FORMAT = "markdown"
SAVE_RESEARCH_DATA = True

# Rate Limiting
MAX_RPM = 10  # Requests per minute
REQUEST_TIMEOUT = 30  # seconds

print(f"✓ Loaded configuration with Gemini model: {GEMINI_MODEL}")