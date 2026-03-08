# main.py
from crewai import Crew, Process
from datetime import datetime, timedelta
import os
import json

# 1. Import your 5 Agents
from agents.news_researcher import news_researcher
from agents.historian import Historical_researcher
from agents.perspective_analyst import perspective_analyst
from agents.writer import article_writer
from agents.editor import editor_agent

# 2. Import your 5 Tasks
from tasks.task_definitions import news_task, history_task, perspective_task, blog_writing_task, editing_task

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
    process=Process.sequential,
    cache=True,
    verbose=True
)

# ==========================================
# 4. THE EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    # Calculate dynamic dates
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    print("="*60)
    print("🚀 Starting the Geopolitical Analysis Crew...")
    print(f"📅 Analyzing data from {start_date} to {end_date}")
    print("="*60 + "\n")

    # 5. Kick off execution
    final_output = geopolitics_crew.kickoff(
        inputs={
            "date_start": start_date,
            "date_end": end_date,
            "time_period": f"{start_date} to {end_date}"
        }
    )

    # 6. Create outputs directory if it doesn't exist
    os.makedirs("outputs/research", exist_ok=True)
    os.makedirs("outputs/articles", exist_ok=True)
    
    # 7. Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"outputs/research/analysis_{timestamp}.json"
    
    # 8. Save the JSON
    with open(json_filename, "w", encoding="utf-8") as file:
        file.write(final_output.raw)
    
    # Also save as "latest" for easy access
    latest_filename = "outputs/research/latest_analysis.json"
    with open(latest_filename, "w", encoding="utf-8") as file:
        file.write(final_output.raw)

    print(f"\n{'='*60}")
    print(f"✓ SUCCESS! Analysis saved to:")
    print(f"  📁 {json_filename}")
    print(f"  📁 {latest_filename}")
    print(f"{'='*60}\n")
    
    # 9. Auto-format to readable article
    try:
        from utils.format_output import format_and_save_article
        article_path = format_and_save_article(latest_filename, timestamp)
        print(f"✓ Formatted article saved to: {article_path}\n")
    except ImportError:
        print("⚠️  format_output.py not found. Skipping auto-formatting.\n")