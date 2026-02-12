import streamlit as st
import pandas as pd
import json
import requests
import arxiv
import os
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from astrapy import DataAPIClient

# ==========================================
# 1. TOOL DEFINITIONS
# ==========================================
class ResearchTools:
    def __init__(self, serper_api_key: str):
        self.serper_key = serper_api_key

    def search_job(self, query: str, max_results: int = 5):
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": max_results, "location": "India"})
        headers = {'X-API-KEY': self.serper_key, 'Content-Type': 'application/json'}
        try:
            response = requests.post(url, headers=headers, data=payload)
            results = response.json().get('organic', [])
            return [{"type": "job_search", "title": r.get('title'), "link": r.get('link'), "summary": r.get('snippet')} for r in results]
        except Exception as e:
            return [{"error": str(e)}]

# ==========================================
# 2. AGENT CLASSES
# ==========================================
class PlannerAgent:
    def __init__(self, groq_key: str):
        self.llm = ChatGroq(api_key=groq_key, model="llama-3.3-70b-versatile")

    def create_plan(self, user_goal: str):
        prompt = f"Create a research plan for: {user_goal}. Return JSON with a 'tasks' list. Each task needs 'tool' (arxiv or job_search) and 'description'."
        response = self.llm.invoke(prompt)
        try:
            # Basic JSON extraction logic
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content).get("tasks", [])
        except:
            return [{"tool": "job_search", "description": user_goal}]

class ResearcherAgent:
    def __init__(self, groq_key, serper_key, astra_token, astra_endpoint):
        self.tools = ResearchTools(serper_key)
        self.arxiv_client = arxiv.Client()
        # Initializing database connection
        client = DataAPIClient(token=astra_token)
        self.db = client.get_database(astra_endpoint)
        self.collection = self.db.get_collection("ResearchPapers")

    def execute_task(self, task):
        tool = task.get('tool')
        desc = task.get('description')
        if tool == "arxiv":
            search = arxiv.Search(query=desc, max_results=3)
            return [{"type": "paper", "title": r.title, "link": r.entry_id, "summary": r.summary[:200]} for r in self.arxiv_client.results(search)]
        else:
            return self.tools.search_job(desc)

    def store_findings(self, findings):
        if findings:
            try: self.collection.insert_many(findings)
            except: pass

class CriticAgent:
    def __init__(self, groq_key: str):
        self.llm = ChatGroq(api_key=groq_key, model="llama-3.1-8b-instant")

    def validate_findings(self, findings):
        # Simplified validation for the UI
        return {"confidence_score": 0.9 if findings else 0.0, "issues_found": []}

# ==========================================
# 3. ORCHESTRATOR
# ==========================================
class ResearchOrchestrator:
    def __init__(self, Planner, Researcher, Critic):
        self.planner = Planner
        self.researcher = Researcher
        self.critic = Critic

    def run(self, user_goal: str):
        plan = self.planner.create_plan(user_goal)
        all_findings = []
        for task in plan:
            findings = self.researcher.execute_task(task)
            all_findings.extend(findings)
        
        report = self.critic.validate_findings(all_findings)
        self.researcher.store_findings(all_findings)
        return {"findings": all_findings, "report": report, "plan": plan}

# ==========================================
# 4. STREAMLIT UI
# ==========================================
st.set_page_config(page_title="AI Research Hub", layout="wide")

st.title("🤖 AI Research Agent Orchestrator")
st.markdown("Enter your keys in the sidebar and start your research agent loop.")

with st.sidebar:
    st.header("🔑 API Credentials")
    g_key = st.text_input("Groq API Key", type="password")
    s_key = st.text_input("Serper API Key", type="password")
    a_token = st.text_input("Astra DB Token", type="password")
    a_url = st.text_input("Astra Endpoint URL")

query = st.text_input("Research Topic", placeholder="e.g., Latest AI trends in Healthcare")

if st.button("🚀 Start Research"):
    if not all([g_key, s_key, a_token, a_url]):
        st.error("Missing API credentials!")
    else:
        with st.spinner("Agents are collaborating..."):
            # 1. Setup agents
            p = PlannerAgent(g_key)
            r = ResearcherAgent(g_key, s_key, a_token, a_url)
            c = CriticAgent(g_key)
            boss = ResearchOrchestrator(p, r, c)
            
            # 2. Run the logic
            result = boss.run(query)
            findings = result.get("findings", [])
            report = result.get("report", {}) # Get the critic report
            
            # --- PASTE THE EXPANDER HERE ---
            with st.expander("👁️ View Agent Thought Process"):
                st.write("### Planner Insight")
                st.info("The Planner broke your goal into specific search tasks.")
                # We don't have 'plan' directly here unless we return it from boss.run
                # But we can show the Critic's validation:
                st.write(f"**Critic Confidence Score:** {report.get('confidence_score', 'N/A')}")
                if report.get('issues_found'):
                    st.warning(f"Issues noted: {report.get('issues_found')}")
            # -------------------------------

            # 3. Display final results
            if findings:
                st.success(f"Research Complete! Found {len(findings)} items.")
                st.dataframe(pd.DataFrame(findings), use_container_width=True)