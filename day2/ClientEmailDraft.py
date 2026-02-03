from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

#Initialize the model
llm = ChatOllama(model="gemma2:2b")

#Task 2 : Client Email Draft System Message
system_message = """
You are a Professional Project Manager. Your goal is to draft a formal progress update email for a client.

Rules: 
- Maintain a strictly professional and formal tone.
- Use Placeholders for [Client Name], [Project Name], and [Deadline].
- Summarize project progress and milestones clearly.
- Request feedback from the client at the end.
- Use bullet points for Action Items.

Expected Output Format:
- Subject Line
- Professional Greeting
- Professional Progress Summary
- Bullet list of Action Items
- Formal Closing 

Guardrails: 
- Avoid including any sensitive or confidential data.
- Do not invent project details; only use the information provided by the user.
"""

#Creating the template structure
template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    HumanMessagePromptTemplate.from_template("{project_details}")
])

print("-----Client Email Draft Generator Initialized-----")
details_input = input("Enter the project milestones and upcoming deadlines: \n")

#Invoke the model
response = llm.invoke(template.format(
    project_details = details_input
))

#Output the result
print("\nGenerated Email Draft:\n")
print(response.content)
