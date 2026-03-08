from crewai import Agent
from crewai_tools import TavilySearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.1
)

# 1. Standard Web Search Tool (for general research)
web_search_tool = TavilySearchTool()

# 2. Custom Think Tank Searcher (Using Tavily's domain filtering)
think_tank_searcher = TavilySearchTool(
    name="think_tank_search_tool",
    description="Searches exclusively across major geopolitical think tanks for policy papers and strategic analysis.",
    # We restrict the search to these specific, highly credible domains
    include_domains=[
        "csis.org",          # Center for Strategic and International Studies
        "brookings.edu",     # Brookings Institution
        "rand.org",          # RAND Corporation
        "cfr.org",           # Council on Foreign Relations
        "crisisgroup.org",   # International Crisis Group
        "chathamhouse.org"   # Chatham House
    ]
)

# 3. Define the Agent
perspective_analyst = Agent(
    role='Strategic Affairs & Multi-Perspective Geopolitical Analyst',
    goal="Analyze the current Iran-Israel-America situation from each party's strategic perspective, identifying motivations, red lines, fears, and potential decision-making factors.",
    backstory="""You are a strategic analyst who has worked for international think tanks, 
    advised governments, and published policy papers on Middle Eastern security. 
    You have the unique ability to think from multiple viewpoints simultaneously - 
    understanding Iranian security concerns, Israeli threat perception, and American 
    strategic interests without bias. You avoid Western-centric analysis and genuinely 
    represent each perspective based on their stated goals, historical actions, and strategic culture.""",
    tools=[web_search_tool, think_tank_searcher],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=7,
    memory=True
)

print("✓ Perspective Analyst agent created successfully")