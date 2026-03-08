from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Using a very low temperature (0.1) for maximum factual adherence and strictness
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.1 
)

editor_agent = Agent(
    role='Senior Geopolitical Editor & Fact-Checker',
    goal='Review, fact-check, and edit the blog article to ensure it meets the highest standards of accuracy, balance, and quality.',
    backstory="""You are a veteran Senior Editor at a top-tier geopolitical publication. 
    You have a legendary reputation for meticulous fact-checking, demanding absolute neutrality, 
    and ensuring every claim is backed by high-credibility sources. You do not tolerate 
    lazy writing, biased terminology, or logical leaps. You have the authority to make minor 
    edits yourself, but you will aggressively delegate major structural issues back to the Writer.""",
    tools=[], # The editor relies on the context provided by the research agents
    llm=llm,
    verbose=True,
    allow_delegation=True, # Changed to True so it can communicate with the Writer
    max_iter=5,
    memory=True
)

print("✓ Editor agent created successfully")