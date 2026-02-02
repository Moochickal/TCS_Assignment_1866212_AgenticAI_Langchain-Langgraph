from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Initialize the model
llm = ChatOllama(model="gemma2:2b")

# Task 5 : Market Analysis Brief System Message
system_message = """
You are a Market Research Analyst. Your goal is to generate a strategic market brief based on provided reports and articles.

Rules:
- Perform a SWOT Analysis ( Strengths, Weaknesses, Opportunities, Threats).
- Highlight the Top 3 Market Trends.
- Provide a citation for every trend and SWOT point identified ( e.g., [Source Name]).
- Output MUST be a combination of a narrative summary and a structured JSON object.

Expected Output Format:
1. Narrative Summary: A high-level overview of the market landscape.
2. Structured Data (JSON):
{{
  "swot": {{
    "strengths": [],
    "weaknesses": [],
    "opportunities": [],
    "threats": []
  }},
  "top_trends": [
    {{"trend": "Name", "description": "Details", "citation": "Source"}}
  ]
}}

Guardrails:
- Avoid fabricated data.
- Ensure every point is supported by the provided source text.
"""

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    HumanMessagePromptTemplate.from_template("{source_content}")
])

print("----- Market Analysis Brief Generator Initialized------")
sources = input("Please paste the combined news articles and internal reports: ") 

# Invoke the model using the template.format() method
response = llm.invoke(template.format(
    source_content = sources
))

# Output the narrative summary and structured JSON result
print("----- Final Market Analysis Brief ------\n")
print(response.content) 