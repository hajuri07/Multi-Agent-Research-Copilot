---
title: Multi-Agent Research Copilot
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🤖 Multi-Agent Research Copilot (LLM + Real Tools)

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME)
[![Live Demo](https://img.shields.io/badge/Demo-Live_on_HF-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://hajuri07-multiagent-research.hf.space)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=flat-square)](https://www.python.org/downloads/)

An autonomous, multi-agent orchestration framework designed to automate complex research workflows. This system utilizes an iterative **Planner-Researcher-Critic** loop to decompose high-level user goals into actionable sub-tasks, execute them using live web tools, and validate findings through a reflective critique layer.



## 🌟 Key Features
* **Autonomous Task Decomposition:** A dedicated **Planner Agent** (Llama 3.3) analyzes user intent and generates a structured execution roadmap.
* **Multi-Tool Integration:** The **Researcher Agent** interacts with live APIs, including **Arxiv** for academic papers and **Serper (Google Search)** for real-time market data.
* **Reflective Quality Control:** A **Critic Agent** performs self-reflection, evaluating gathered data for relevance and accuracy before final synthesis.
* **Agentic RAG & Persistence:** Integrated with **Astra DB** (Vector Database) to store findings and ground future generations in verifiable facts.
* **Dockerized Architecture:** Fully containerized deployment optimized for Hugging Face Spaces.

## 🏗️ System Architecture
The system operates on a **Reasoning + Acting (ReAct)** pattern to ensure that LLM outputs are grounded in real-world data rather than training-set hallucinations.

1. **Planner:** Orchestrates the workflow by breaking the "User Goal" into tool-specific tasks.
2. **Researcher:** Executes the tasks via API calls and synthesizes the raw data.
3. **Critic:** Scores the findings and identifies potential gaps or misinformation.
4. **Memory:** Validated insights are vectorized and stored in **Astra DB**.



## 🛠️ Tech Stack
* **LLM Orchestration:** LangChain / Custom Agentic Loops
* **Inference Engine:** Groq (Llama-3.3-70B-Versatile)
* **Vector Database:** DataStax Astra DB
* **Frontend:** Streamlit
* **Containerization:** Docker
* **APIs:** Arxiv, Serper.dev

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Multi-Agent-Research-Copilot.git](https://github.com/YOUR_USERNAME/Multi-Agent-Research-Copilot.git)
cd Multi-Agent-Research-Copilot
2. Set Up Environment Variables
Create a sidebar entry or a .env file with the following:

GROQ_API_KEY

SERPER_API_KEY

ASTRA_DB_TOKEN

ASTRA_DB_ENDPOINT

3. Run with Docker
Bash
docker build -t research-copilot .
docker run -p 7860:7860 research-copilot
