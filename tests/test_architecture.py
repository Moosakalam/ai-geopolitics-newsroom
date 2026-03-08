import sys
import os

# 1. Add project root to Python path so it can find main.py and the agents folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Now the import will work perfectly
from testing_main import geopolitics_crew

print("==================================================")
print("🔍 CREW ARCHITECTURE VALIDATION (DRY RUN)")
print("==================================================\n")

# Check Agents
print(f"Total Agents Loaded: {len(geopolitics_crew.agents)}")
print("-" * 30)
for i, agent in enumerate(geopolitics_crew.agents, 1):
    tool_names = [tool.name for tool in agent.tools] if agent.tools else ["None"]
    print(f"Agent {i}: {agent.role}")
    print(f"  └─ Tools Attached: {', '.join(tool_names)}")
print("\n")

# Check Tasks
print(f"Total Tasks Loaded: {len(geopolitics_crew.tasks)}")
print("-" * 30)
for i, task in enumerate(geopolitics_crew.tasks, 1):
    assigned_agent = task.agent.role if task.agent else "UNASSIGNED"
    desc_preview = task.description[:60].replace('\n', ' ').strip() + "..."
    
    print(f"Task {i}: {desc_preview}")
    print(f"  └─ Assigned to:  {assigned_agent}")
    print(f"  └─ Expects JSON: {'Yes' if task.output_json else 'No'}")
print("\n")

print("==================================================")
print("✓ SUCCESS: All modules imported and validated!")
print("✓ NO API CALLS WERE MADE.")
print("==================================================")