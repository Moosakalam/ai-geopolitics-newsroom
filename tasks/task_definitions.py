from crewai import Task
from pydantic import BaseModel
from typing import List

from agents.historian import Historical_researcher
from agents.perspective_analyst import perspective_analyst
from agents.writer import article_writer
from agents.news_researcher import news_researcher
from agents.editor import editor_agent

# ==========================================
# 1. DEFINE STRICT PYDANTIC MODELS
# ==========================================

# --- Models for History Task ---
class TimelineItem(BaseModel):
    year: str
    event: str
    significance: str

class Agreement(BaseModel):
    name: str
    year: str
    status: str

class HistoryOutput(BaseModel):
    timeline: List[TimelineItem]
    key_agreements: List[Agreement]
    historical_patterns: List[str]
    context_analysis: str


# --- Models for News Task ---
class NewsMetadata(BaseModel):
    search_period: str
    total_sources_found: int

class NewsItem(BaseModel):
    date: str
    category: str
    headline: str
    details: str
    source_name: str
    source_url: str
    source_perspective: str
    credibility_rating: str
    contradicts_other_reports: bool

class NewsOutput(BaseModel):
    metadata: NewsMetadata
    summary: str
    news_items: List[NewsItem]
    flagged_contradictions: List[str]


# --- Models for Editor Task ---
class FactCheckReport(BaseModel):
    claims_verified: int
    claims_corrected: int
    sources_added: int
    credibility_flags: List[str]

class EditorOutput(BaseModel):
    final_article_markdown: str
    fact_check_report: FactCheckReport
    editorial_changes_made: List[str]
    publication_recommendation: str
    editors_notes: str


# ==========================================
# 2. DEFINE THE TASKS
# ==========================================

perspective_task = Task(
    description="""
    Analyze the current geopolitical situation using the following strict framework:

    IRANIAN PERSPECTIVE:
    - Security Concerns: US sanctions, Israeli covert ops, existential threats.
    - Strategic Goals: Nuclear deterrence, "Axis of Resistance" leadership, regime survival.
    - Red Lines: Direct attacks on territory, regime change.

    ISRAELI PERSPECTIVE:
    - Security Concerns: Iranian nuclear weapons, Hezbollah proxy threats (150k missiles), existential threat doctrine.
    - Strategic Goals: Prevent Iranian nuclear capability, degrade proxies, expand Abraham Accords.
    - Red Lines: Iranian nuclear breakout, permanent Iranian presence in Syria.

    AMERICAN PERSPECTIVE:
    - Strategic Interests: Non-proliferation, Israeli alliance, regional stability.
    - Competing Pressures: Israel lobby vs war fatigue, domestic politics.
    - Policy Options: Diplomatic engagement vs containment, sanctions pressure.
    """,
    expected_output="""A deep analysis document containing:
    1. A 2-3 paragraph section for each perspective (Iran, Israel, America).
    2. Identified escalation and de-escalation factors.
    3. Areas of potential compromise.
    4. Likely scenarios analysis based on current data.
    """,
    agent=perspective_analyst
)

history_task = Task(
    description="""
    Research and analyze the historical context of Iran-Israel-America tensions.
    You must cover the following Key Historical Areas:
    1. 1979 Iranian Revolution and aftermath
    2. Iran-Iraq War (1980-1988)
    3. Iranian nuclear program development
    4. JCPOA nuclear deal (2015) and US withdrawal (2018)
    5. Abraham Accords (2020)
    6. Proxy conflicts (Hezbollah, Hamas, Houthis)
    7. Israeli strikes on Iranian assets
    8. US policy shifts across administrations
    """,
    expected_output="""A JSON object containing the timeline, key agreements, historical patterns, and long-form context analysis.""",
    agent=Historical_researcher,
    
    # Pass the Pydantic class here instead of a dictionary!
    output_json=HistoryOutput 
)

news_task = Task(
    description="""
    Conduct comprehensive research on the current state of Iran-Israel-America tensions. 
    Your research should cover the period from {date_start} to {date_end}.

    FOCUS AREAS:
    1. Military Developments (Troop movements, exercises, weapons transfers, strikes)
    2. Diplomatic Activity (Official statements, UN meetings, mediation)
    3. Economic Measures (Sanctions, relief, trade restrictions)
    4. Nuclear Program (IAEA reports, enrichment levels, facilities)
    5. Proxy Activities (Hezbollah, Hamas, or Houthi actions, Israeli responses)

    REQUIREMENTS:
    - Minimum 15 credible sources.
    - Include sources from multiple perspectives: 
      * Western media (Reuters, AP, BBC)
      * Middle Eastern media (Al Jazeera, Times of Israel, Middle East Eye)
      * Official government statements
      * Think tank analyses
    - Verify dates and avoid outdated information.
    - Flag any contradictory reports.
    - Note source credibility for each item.
    - Organize chronologically.
    """,
    expected_output="Comprehensive research report with 15+ credible sources, organized by category and chronology, with source credibility ratings in JSON format.",
    agent=news_researcher,
    
    # Pass the Pydantic class here instead of a dictionary!
    output_json=NewsOutput 
)

blog_writing_task = Task(
    description="""
    Write a comprehensive, balanced, and engaging blog article analyzing the current Iran-Israel-America tensions. 
    Your article should inform educated readers who may not be Middle East experts.

    ARTICLE SPECIFICATIONS:
    Title Requirements: Informative, specific, not sensationalist.
    
    Structure:
    1. Introduction (150-200 words): Hook, thesis, why this matters now.
    2. Recent Developments (250-300 words): Key incidents chronologically with examples.
    3. Historical Context (200-250 words): Brief background, how we got here.
    4. Iranian Perspective (200-250 words): Security concerns, strategic goals, quotes.
    5. Israeli Perspective (200-250 words): Threat views, red lines, objectives, quotes.
    6. American Perspective (200-250 words): US interests, dilemmas, policy options, quotes.
    7. Analysis & Scenarios (250-300 words): Escalation vs de-escalation, wild cards.
    8. Conclusion (100-150 words): Synthesis, what to watch for.

    STYLE REQUIREMENTS:
    - Clear, direct prose, active voice.
    - Explain jargon on first use.
    - Tone: Serious, analytical, balanced, fair.
    - Attribution: Every factual claim needs a source [1], [2].

    WHAT TO AVOID:
    - "Both sides" false equivalence
    - Predictions presented as certainty
    - Sensationalism, fear-mongering, or clichés.

    REQUIRED ELEMENTS:
    - Target length: 1200-1500 words
    - Minimum 3 quoted sources
    - At least 8-10 citations
    - Markdown formatting
    """,
    expected_output="Publication-ready blog article (1200-1500 words) in Markdown format with proper structure, citations, and balanced analysis.",
    agent=article_writer,
    context=[news_task, history_task, perspective_task] 
)

editing_task = Task(
    description="""
    Review, fact-check, and edit the drafted blog article. 
    You have access to the original research from the News, History, and Perspective agents.

    FACT-CHECKING PROTOCOL:
    Level 1: Verifiable Facts (Dates, locations, casualties, quotes).
    Level 2: Source Quality (Check credibility, require mix of perspectives).
    Level 3: Balance & Fairness (Neutral language, no loaded terms, equal depth).
    Level 4: Accuracy of Analysis (Logical leaps, hedged predictions).

    EDITORIAL IMPROVEMENTS:
    - Strengthen weak arguments, remove redundancy, improve transitions.
    - Check word count (1200-1500 words).
    - Ensure markdown formatting and H1/H2/H3 hierarchy.
    
    DELEGATION TRIGGERS:
    If there are major structural problems, missing perspectives, or major factual errors, 
    you MUST use your delegation tool to send the article back to the Writer agent for a rewrite. 
    Handle minor edits yourself.
    """,
    expected_output="Final polished article with a comprehensive fact-check report and editorial notes.",
    agent=editor_agent,
    context=[blog_writing_task, news_task, history_task, perspective_task], 
    
    # Pass the Pydantic class here instead of a dictionary!
    output_json=EditorOutput 
)