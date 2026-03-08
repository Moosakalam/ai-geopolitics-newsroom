"""
Format JSON output into beautiful markdown articles
"""

import json
import os
from datetime import datetime
from pathlib import Path


def format_and_save_article(json_path: str, timestamp: str = None) -> str:
    """
    Convert JSON analysis to formatted markdown article
    
    Args:
        json_path: Path to the JSON file
        timestamp: Optional timestamp for filename
        
    Returns:
        Path to the saved markdown file
    """
    
    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        data_str = f.read()
    
    # Parse JSON (handle if it's nested or plain text)
    try:
        data = json.loads(data_str)
    except json.JSONDecodeError:
        # If it's not JSON, treat as plain text
        data = {"final_article": data_str}
    
    # Extract components
    article = data.get('final_article', data_str)
    fact_check = data.get('fact_check_report', {})
    editor_notes = data.get('editors_notes', '')
    editorial_changes = data.get('editorial_changes_made', [])
    
    # Build the formatted article
    formatted = build_formatted_article(
        article=article,
        fact_check=fact_check,
        editor_notes=editor_notes,
        editorial_changes=editorial_changes
    )
    
    # Save to markdown file
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_dir = Path("outputs/articles")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    md_filename = output_dir / f"geopolitical_analysis_{timestamp}.md"
    latest_filename = output_dir / "latest_analysis.md"
    
    # Save timestamped version
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(formatted)
    
    # Save as latest
    with open(latest_filename, 'w', encoding='utf-8') as f:
        f.write(formatted)
    
    return str(md_filename)


def build_formatted_article(article: str, fact_check: dict, 
                            editor_notes: str, editorial_changes: list) -> str:
    """Build the formatted markdown article"""
    
    now = datetime.now()
    
    output = f"""# Understanding Iran-Israel-America Tensions: A Geopolitical Analysis

**Published:** {now.strftime('%B %d, %Y at %I:%M %p')}  
**Analysis Period:** Last 7 days  
**Analysis Type:** Multi-agent AI-assisted geopolitical assessment  

---

{article}

---

## 📊 Analysis Metadata

### Editorial Assessment

{editor_notes if editor_notes else "No editorial notes provided."}

### Fact-Check Summary

- **Claims Verified:** {fact_check.get('claims_verified', 'N/A')}
- **Claims Corrected:** {fact_check.get('claims_corrected', 'N/A')}
- **Sources Added:** {fact_check.get('sources_added', 'N/A')}
- **Credibility Flags:** {len(fact_check.get('credibility_flags', []))}

"""

    # Add credibility flags if they exist
    if fact_check.get('credibility_flags'):
        output += "\n#### Source Credibility Notes\n\n"
        for flag in fact_check.get('credibility_flags', []):
            output += f"- {flag}\n"
    
    # Add editorial changes if they exist
    if editorial_changes:
        output += "\n### Editorial Changes Made\n\n"
        for change in editorial_changes:
            output += f"- {change}\n"
    
    output += f"""

---

## 🤖 About This Analysis

This report was generated using a multi-agent AI system that:

1. **Researched** current news from multiple international sources
2. **Analyzed** historical context and patterns
3. **Evaluated** perspectives from Iran, Israel, and the United States
4. **Synthesized** findings into a coherent analysis
5. **Fact-checked** and verified all claims

**Methodology:** Sequential multi-agent workflow with autonomous research, analysis, writing, and editorial review stages.

**Data Sources:** NewsData.io, international news agencies, government statements, and think tank publications.

**Disclaimer:** This analysis is for informational purposes only. All claims are sourced and fact-checked, but readers should verify information independently and consult multiple sources.

---

*Generated on {now.strftime('%Y-%m-%d')} using CrewAI multi-agent system with Google Gemini Pro*
"""
    
    return output


def create_summary_report(json_path: str) -> dict:
    """
    Create a summary report of the analysis
    
    Args:
        json_path: Path to the JSON file
        
    Returns:
        Dictionary with summary statistics
    """
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data_str = f.read()
    
    try:
        data = json.loads(data_str)
    except json.JSONDecodeError:
        data = {"final_article": data_str}
    
    article = data.get('final_article', data_str)
    fact_check = data.get('fact_check_report', {})
    
    summary = {
        'timestamp': datetime.now().isoformat(),
        'word_count': len(article.split()),
        'character_count': len(article),
        'claims_verified': fact_check.get('claims_verified', 0),
        'claims_corrected': fact_check.get('claims_corrected', 0),
        'credibility_flags': len(fact_check.get('credibility_flags', [])),
        'publication_status': data.get('publication_recommendation', 'Unknown')
    }
    
    return summary


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "outputs/research/latest_analysis.json"
    
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found!")
        print(f"Current directory: {os.getcwd()}")
        print(f"Looking for: {os.path.abspath(json_file)}")
        sys.exit(1)
    
    print(f"📄 Processing: {json_file}")
    
    # Format and save
    article_path = format_and_save_article(json_file)
    print(f"✅ Formatted article saved to: {article_path}")
    
    # Create summary
    summary = create_summary_report(json_file)
    print(f"\n📊 Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")