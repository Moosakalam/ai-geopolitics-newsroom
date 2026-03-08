from crewai import Agent 
from langchain.tools import tool
from tools.news_search import search_geopolitical_news
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from config.settings import GOOGLE_API_KEY, GEMINI_MODEL
from crewai.tools import BaseTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from crewai_tools import TavilySearchTool , SerperDevTool
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.1, 
    google_api_key=GOOGLE_API_KEY
)
my_tavily_key = os.getenv("TAVILY_API_KEY")

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1500)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
my_serper_key = os.getenv("SERPER_API_KEY")
# 2. INSTANTIATE THE PRE-BUILT TOOLS (One line of code each!)
news_search_tool = SerperDevTool()      # Great for recent news
history_search_tool = TavilySearchTool(api_key=my_tavily_key) # Great for deep/academic research

Historical_researcher = Agent(
    role='Middle East Conflict Historian & Strategic Context Analyst',
    
    goal='Provide comprehensive historical background that connects current Iran-Israel-America tensions to past events, treaties, conflicts, and strategic shifts',
    
    backstory="""You hold a PhD in Middle Eastern History with 20 years of academic research. 
You've published extensively on the Iran-Israel conflict, the Islamic Revolution, 
US foreign policy in the Middle East, and regional proxy wars. You excel at 
identifying historical patterns and connecting past events to present situations. 
Your analysis helps readers understand 'how we got here' without oversimplifying 
complex historical dynamics.""",
    
    tools=[news_search_tool,history_search_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=5,
    memory = True
)

print("✓ News historian agent created successfully")
