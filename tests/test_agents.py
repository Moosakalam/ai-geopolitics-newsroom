"""Test individual agent"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now imports will work
from agents.news_researcher import news_researcher
from crewai import Task , Crew

# Create a simple test task
test_task = Task(
    description="""
    Search for news about Iran-Israel tensions from the last 3 days.
    Provide a brief summary of the top 5 most important developments.
    """,
    agent=news_researcher,
    expected_output="Summary of top 5 news items with sources"
)

# Execute the task
print("Testing News Researcher agent...\n")
test_crew = Crew(
    agents=[news_researcher],
    tasks=[test_task],
    verbose=True
)

# 2. Execute using kickoff() instead of execute()
print("Testing News Researcher agent...\n")
result = test_crew.kickoff()
print("\n" + "="*50)
print("RESULT:")
print("="*50)
print(result)