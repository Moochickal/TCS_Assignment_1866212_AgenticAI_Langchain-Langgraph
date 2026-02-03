from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

#Initialize the model
llm = ChatOllama(model="gemma2:2b")

# Task 3 : Policy Complaince Checker System Message
# The prompt is designed to enforce a strict JSON structrue and role based behavior.

system_message = """
You are an HR Compliance Auditor. Your goal is to review the HR policy for clarity and compliance.

Rules:
- Identify missing compliance clauses or ambiguous language.
- Suggest improvements based on standard HR best practices.
- Do not invent compliance rules; base suggestions only on the provided context.
- Your response must be ONLY a valid JSON object. No conversational filler before or after.

Expected JSON Format:

{{
      "issues": ["List of identified problems"],
      "severity": ["High", "Medium" or "Low" for each coresponding issue],
      "recommendations": ["Specific suggested improvements for each issue"]
}}
  
Policy Content: {policy_text}
"""

# Creating the template using the format from your reference file
template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    HumanMessagePromptTemplate.from_template("{policy_text}")
])

print("----- HR Policy Compliance Checker Initialized------")
policy_input = input("Please paste the HR policy draft you wish to audit: ")

# Invoke the model using the template.format() method
response = llm.invoke(template.format(
    policy_text = policy_input
))

# Output the raw JSON result
print("----- Compliance Audit Result (JSON) ------\n")
print(response.content)


