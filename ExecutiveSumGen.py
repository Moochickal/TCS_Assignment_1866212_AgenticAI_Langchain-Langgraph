from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

#Initialize the model
llm = ChatOllama(model="gemma2:2b")

#Task 1 : Executive Summary Generator Prompt
# Role-based prompt with specific formatting and guardrail instructions
system_message = """
You are a Senior Strategy Analyst. Your goal is to summarize a quarterly performance report.

Rules:
- Create a concise summary of approximately 150 words.
- You must include a metrics table.
- You must include a dedicated section for Risks and Opportunities.
- Stick strictly to the facts from the provided text; do NOT hallucinate or invent data
- If specific data points are used, cite the source within the text as [Source].

Response format:
1. Executive Summary (Prose)
2. Key Metrics Table
3. Risks and Opportunities Section

User Data : {report_text}"""

#Creating the template stucture
template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    HumanMessagePromptTemplate.from_template("{report_text}")
])

print("-----Executive Summary Generator Initialized-----")
report_input = input("Please paste the content of the quarterly performance report here: \n")

#invoke the model
# We use the report_text as the variable name to match the template placeholders
response = llm.invoke(template.format(report_text = report_input))

#Output the result
print("\nAssistant Analysis:\n")
print(response.content)
