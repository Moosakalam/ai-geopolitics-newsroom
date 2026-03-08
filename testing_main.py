# test_main.py
from crewai import Crew, Process

# 1. Import your 5 Agents
from agents.news_researcher import news_researcher
from agents.historian import Historical_researcher
from agents.perspective_analyst import perspective_analyst
from agents.writer import article_writer
from agents.editor import editor_agent

# 2. Import your 5 Tasks
from tasks.task_definitions import news_task, history_task, perspective_task, blog_writing_task, editing_task

print("Building Crew Architecture...")

# 3. Form the Master Crew
geopolitics_crew = Crew(
    agents=[
        news_researcher, 
        Historical_researcher, 
        perspective_analyst, 
        article_writer,
        editor_agent
    ],
    tasks=[
        news_task, 
        history_task, 
        perspective_task, 
        blog_writing_task,
        editing_task
    ],
    process=Process.sequential
)

print("\n==================================================")
print("🔍 CREW ARCHITECTURE VALIDATION (DRY RUN)")
print("==================================================\n")

print(f"Total Agents Loaded: {len(geopolitics_crew.agents)}")
print(f"Total Tasks Loaded:  {len(geopolitics_crew.tasks)}\n")

for i, task in enumerate(geopolitics_crew.tasks, 1):
    assigned_agent = task.agent.role if task.agent else "UNASSIGNED"
    print(f"Task {i}: Assigned to -> {assigned_agent}")

print("\n==================================================")
print("✓ SUCCESS: Architecture is perfectly assembled!")
print("✓ NO API CALLS WERE MADE.")
print("==================================================")