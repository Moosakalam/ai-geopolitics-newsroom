import os
import requests
from typing import List, Dict
from dotenv import load_dotenv
# To install: pip install tavily-python
from tavily import TavilyClient


load_dotenv()

class FactChecker:
     def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
       
        
        if not self.api_key:
            print("⚠️  WARNING: NEWSDATA_API_KEY not found in .env")