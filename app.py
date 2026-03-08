import streamlit as st
import json
import os
import subprocess
import sys

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Geopolitics Desk | Portfolio Project",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SIDEBAR: MISSION CONTROL
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1903/1903162.png", width=80)
    st.title("The AI Newsroom")
    st.markdown("An autonomous Multi-Agent AI system built with **CrewAI** and **Google Gemini**.")
    
    st.divider()
    st.markdown("### ⚙️ Mission Control")
    st.write("Trigger the multi-agent system to research and write a new report based on the latest data.")
    
    if st.button("🚀 Run AI Analysis Now", use_container_width=True, type="primary"):
        with st.spinner("🤖 Agents are researching, writing, and editing... Please wait 3-5 minutes."):
            try:
                subprocess.run([sys.executable, "main.py"], check=True)
                st.success("✅ Analysis generated successfully!")
                st.rerun() 
            except Exception as e:
                st.error(f"❌ An error occurred while running the crew: {e}")
                
    st.divider()
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Shaik Moosa Kalam**")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/shaik-moosa-kalam-174251366/) | [GitHub](https://github.com/Moosakalam)")

# ==========================================
# 3. MAIN DASHBOARD & TABS
# ==========================================
st.title("🌍 Global Strategic Affairs Desk")
st.markdown("An autonomous AI pipeline that researches, synthesizes, and fact-checks complex geopolitical events.")

# Create tabs for the UI
tab1, tab2 = st.tabs(["📰 Latest Report", "🧠 Project Architecture (How It Works)"])

# ------------------------------------------
# TAB 1: THE ACTUAL REPORT (Your existing code)
# ------------------------------------------
with tab1:
    file_path = "outputs/research/latest_analysis.json"

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            col_article, col_editor = st.columns([2.5, 1.5], gap="large")
            
            with col_article:
                st.markdown("##### Published Analysis")
                article_text = data.get("final_article_markdown", "No article found.")
                st.markdown(article_text)
                
            with col_editor:
                st.markdown("##### 🕵️‍♂️ Editor's Fact-Check Report")
                
                status = data.get("publication_recommendation", "N/A")
                if "Approve" in status or "APPROVED" in status:
                    st.success(f"**Status:** {status}")
                else:
                    st.error(f"**Status:** {status}")
                    
                report = data.get("fact_check_report", {})
                m1, m2, m3 = st.columns(3)
                m1.metric("Claims Verified", report.get("claims_verified", 0))
                m2.metric("Corrections", report.get("claims_corrected", 0))
                m3.metric("Sources Added", report.get("sources_added", 0))
                
                st.divider()
                
                with st.expander("📝 Senior Editor's Notes", expanded=True):
                    st.write(data.get("editors_notes", "No notes provided."))
                    
                flags = report.get("credibility_flags", [])
                with st.expander(f"🚩 Credibility Flags ({len(flags)})", expanded=True):
                    if flags:
                        for flag in flags:
                            st.warning(flag)
                    else:
                        st.write("No flags raised.")
                        
                changes = data.get("editorial_changes_made", [])
                with st.expander(f"✂️ Editorial Changes ({len(changes)})"):
                    if changes:
                        for change in changes:
                            st.markdown(f"- {change}")
                    else:
                        st.write("No changes made.")
                        
        except Exception as e:
            st.error(f"Error parsing the JSON report: {e}")
    else:
        st.info("⚠️ No report found. Click 'Run AI Analysis Now' in the sidebar to generate the first report.")

# ------------------------------------------
# TAB 2: PROJECT ARCHITECTURE (For your Resume/Portfolio)
# ------------------------------------------
with tab2:
    st.header("System Architecture & Engineering")
    st.write("This project solves the problem of hallucination and bias in LLM-generated analysis by using a specialized **Multi-Agent System**. Instead of asking one model to write an article, the task is divided among 5 distinct AI personas with strict roles, tools, and validation layers.")
    
    st.markdown("### 🛠️ Tech Stack")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.button("🧠 CrewAI", use_container_width=True)
    col_t2.button("✨ Google Gemini 2.5 Flash", use_container_width=True)
    col_t3.button("🛡️ Pydantic", use_container_width=True)
    col_t4.button("📊 Streamlit", use_container_width=True)
    
    st.divider()
    
    st.markdown("### 🤖 The Agent Pipeline (Sequential Process)")
    
    st.info("**1. The News Researcher (Data Gathering)**\n\nEquipped with Web Search tools, this agent queries the internet for the latest geopolitical developments within a specific timeframe. It must gather a minimum of 15 credible sources, noting their biases (Western vs. Middle Eastern media).")
    
    st.info("**2. The Historian (Contextualization)**\n\nThis agent takes the current news and searches historical databases to establish context. It maps current events to historical treaties (e.g., JCPOA, Abraham Accords) and past conflicts to prevent recency bias. *Outputs strict JSON validated via Pydantic.*")
    
    st.info("**3. The Perspective Analyst (Bias Mitigation)**\n\nA highly specialized agent instructed to look at the collected data through three distinct lenses: Iranian, Israeli, and American. It maps out the 'red lines', security concerns, and strategic goals of each actor independently.")
    
    st.success("**4. The Writer (Synthesis)**\n\nTakes the raw JSON and text outputs from the first three agents and drafts a comprehensive, journalistic-style blog article. It is explicitly prompted to avoid sensationalism and 'both-sides' false equivalencies.")
    
    st.warning("**5. The Senior Editor (Quality Assurance)**\n\nThe final gatekeeper. This agent reviews the drafted article against the original raw research. It conducts a 4-level fact-check (Verifiable facts, Source Quality, Balance/Fairness, and Analytical Accuracy). It has the authority to flag credibility issues and make editorial changes. *Outputs strict JSON validated via Pydantic.*")
    
    st.divider()
    
    st.markdown("### 💡 Key Engineering Features")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("**Strict Output Validation**")
        st.write("Agents pass data to each other not as raw text, but as strict JSON structures enforced by `Pydantic` BaseModels. If an LLM hallucinates a bad JSON format, the framework automatically catches it and forces the LLM to self-correct before proceeding.")
    with col_f2:
        st.markdown("**Tool Caching**")
        st.write("To optimize API costs and execution speed, the system caches web search results. If the Historian searches for '1979 Iran Revolution' multiple times during development, the system intercepts the call and serves the cached data.")