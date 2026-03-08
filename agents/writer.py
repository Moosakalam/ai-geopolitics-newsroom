from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3 # Slightly higher temperature for better writing flow
)

article_writer = Agent(
    role='Senior Geopolitical Journalist & Editor',
    goal='Synthesize complex geopolitical research into an engaging, balanced, and accessible blog article.',
    backstory="""You are an award-winning geopolitical journalist. You specialize in 
    translating dense think-tank analysis, raw news, and historical data into 
    compelling, easy-to-understand articles for educated but non-expert readers. 
    You are renowned for your strict neutrality, engaging prose, and rigorous citation 
    of sources. You never take sides and avoid sensationalism.""",
    tools=[], # No tools needed; it uses the context from other agents
    llm=llm,
    verbose=True,
    allow_delegation=False
)

print("✓ Writer agent created successfully")