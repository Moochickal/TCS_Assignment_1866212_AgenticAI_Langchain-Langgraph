# 🤖 Prompt Quality Scoring Agent
> **A Senior Prompt Engineer in your Terminal.**

[![LangChain](https://img.shields.io/badge/Powered%20by-LangChain-blue)](https://python.langchain.com/)
[![Ollama](https://img.shields.io/badge/Model-Gemma2--2b-orange)](https://ollama.com/)

This agent evaluates, scores, and provides actionable feedback on LLM prompts. Developed as part of a **LangChain Agentic Workflows** assignment, it bridges the gap between vague inputs and high-quality AI responses.

---

## 📖 Project Overview
The agent utilizes the **Reason-Think-Act (ReAct)** pattern to analyze prompts against five industry-standard pillars. By integrating a custom Python mathematical tool, it ensures that final scores are precise and grounded in objective analysis.


## 📊 Evaluation Pillars
Each prompt is audited on a scale of **0–10** using the following criteria:

* **Clarity 🎯**: Is the goal unambiguous and easy to follow?
* **Specificity 🔎**: Are there sufficient technical or creative details?
* **Context 🌐**: Is there background information or a defined audience?
* **Output Format 📋**: Are length, tone, and structure (e.g., JSON, Bullets) defined?
* **Persona 🎭**: Is a specific expert role assigned to the AI?

---

## 🚀 Getting Started

### Prerequisites
* **Python**: 3.9+
* **LLM Server**: [Ollama](https://ollama.com/) installed and running.
* **Model**: `gemma2:2b` (or higher).  I used qwen3:30b

### Installation & Execution
1. **Prepare Environment**:
   ```bash

   pip install langchain langchain-ollama
