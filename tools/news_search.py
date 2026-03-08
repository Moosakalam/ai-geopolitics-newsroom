"""
NewsData.io Search Tool for Geopolitical News
Searches for Iran-Israel-America related news
"""

import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class NewsDataSearcher:
    """Search news using NewsData.io API"""
    
    def __init__(self):
        self.api_key = os.getenv("NEWSDATA_API_KEY")
        self.base_url = "https://newsdata.io/api/1/news"
        
        if not self.api_key:
            print("⚠️  WARNING: NEWSDATA_API_KEY not found in .env")
    
    def search_iran_israel_news(self, days_back: int = 7) -> str:
        """
        Search for Iran-Israel-America news
        
        Args:
            days_back: Number of days to search back
            
        Returns:
            Formatted string of news articles
        """
        
        if not self.api_key:
            return "Error: NewsData.io API key not configured. Please add NEWSDATA_API_KEY to .env file"
        
        # Multiple targeted queries
        queries = [
            "Iran Israel",
            "Iran nuclear",
            "Middle East tensions",
            "Hezbollah",
            "JCPOA"
        ]
        
        all_articles = []
        
        for query in queries:
            articles = self._search_api(query, max_results=5)
            all_articles.extend(articles)
        
        # Remove duplicates
        unique_articles = self._deduplicate(all_articles)
        
        # Sort by date (newest first)
        unique_articles.sort(
            key=lambda x: x.get("published_date", ""),
            reverse=True
        )
        
        # Format for agent consumption
        return self._format_for_agent(unique_articles[:15])
    
    def _search_api(self, query: str, max_results: int = 5) -> List[Dict]:
        """Execute API search"""
        
        params = {
            "apikey": self.api_key,
            "q": query,
            "language": "en",
            "country": "us,il,gb,qa",
            "size": max_results
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                return self._format_articles(data.get("results", []))
            else:
                return []
                
        except Exception as e:
            print(f"NewsData.io API error: {e}")
            return []
    
    def _format_articles(self, articles: List[Dict]) -> List[Dict]:
        """Format raw API response"""
        
        formatted = []
        for article in articles:
            formatted.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("link", ""),
                "source": article.get("source_id", "Unknown"),
                "published_date": article.get("pubDate", ""),
                "country": article.get("country", ["Unknown"])[0] if article.get("country") else "Unknown"
            })
        return formatted
    
    def _deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles"""
        seen_urls = set()
        unique = []
        
        for article in articles:
            url = article.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique.append(article)
        
        return unique
    
    def _format_for_agent(self, articles: List[Dict]) -> str:
        """Format articles as readable text for LLM agents"""
        
        if not articles:
            return "No recent news articles found."
        
        output = f"Found {len(articles)} recent news articles:\n\n"
        
        for i, article in enumerate(articles, 1):
            output += f"{i}. {article['title']}\n"
            output += f"   Source: {article['source']} | Date: {article['published_date']}\n"
            output += f"   URL: {article['url']}\n"
            if article.get('description'):
                output += f"   Summary: {article['description'][:200]}...\n"
            output += "\n"
        
        return output


# ============================================
# THIS IS THE MISSING FUNCTION - ADD IT HERE
# ============================================
def search_geopolitical_news(days_back: str = "7") -> str:
    """
    Wrapper function for LangChain tool integration
    This is what the agent actually calls
    
    Args:
        days_back: Number of days to search (as string)
    
    Returns:
        Formatted news articles as text
    """
    searcher = NewsDataSearcher()
    try:
        days = int(days_back)
    except:
        days = 7
    
    return searcher.search_iran_israel_news(days)


# Test the tool when run directly
if __name__ == "__main__":
    print("Testing NewsData.io tool...\n")
    result = search_geopolitical_news("7")
    print(result)