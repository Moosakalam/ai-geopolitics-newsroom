"""
Quick script to view the latest analysis
"""

import json
import os
from pathlib import Path

def find_latest_analysis():
    """Find the most recent analysis file"""
    
    # Check multiple locations
    possible_paths = [
        "outputs/research/latest_analysis.json",
        "final_geopolitics_report.json",
        "outputs/research/*.json"
    ]
    
    for path_pattern in possible_paths:
        if "*" in path_pattern:
            # Find all matching files
            import glob
            files = glob.glob(path_pattern)
            if files:
                # Return most recent
                return max(files, key=os.path.getctime)
        else:
            if os.path.exists(path_pattern):
                return path_pattern
    
    return None

def display_analysis(json_path: str):
    """Display the analysis in a readable format"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data_str = f.read()
    
    try:
        data = json.loads(data_str)
    except json.JSONDecodeError:
        # Plain text, not JSON
        print(data_str)
        return
    
    print("="*80)
    print(" GEOPOLITICAL ANALYSIS RESULTS")
    print("="*80)
    
    # Display article
    if 'final_article' in data:
        print("\n📄 ARTICLE:\n")
        print(data['final_article'][:2000])  # First 2000 chars
        print("\n... (truncated)")
    
    # Display fact-check
    if 'fact_check_report' in data:
        print("\n\n✅ FACT-CHECK REPORT:\n")
        report = data['fact_check_report']
        print(f"  Claims Verified: {report.get('claims_verified', 'N/A')}")
        print(f"  Claims Corrected: {report.get('claims_corrected', 'N/A')}")
        print(f"  Sources Added: {report.get('sources_added', 'N/A')}")
    
    # Display editor notes
    if 'editors_notes' in data:
        print("\n\n📝 EDITOR'S NOTES:\n")
        print(data['editors_notes'])
    
    print("\n" + "="*80)

if __name__ == "__main__":
    latest = find_latest_analysis()
    
    if latest:
        print(f"Found: {latest}\n")
        display_analysis(latest)
    else:
        print("❌ No analysis files found!")
        print("\nSearched in:")
        print("  - outputs/research/latest_analysis.json")
        print("  - final_geopolitics_report.json")
        print("  - outputs/research/*.json")