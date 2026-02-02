from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Initialize the model
llm = ChatOllama(model="gemma2:2b")

# Task 4  Meeting Minutes Summarizer System Message
system_message = """
You are a Meeting Assistant. Your goal is to convert raw transcripts into structured minutes.

Rules:
- Organize the content into two main sections: ## Decisions and ## Action Items.
- For each Action Item, you MUST identify an owner and a deadline.
- For every entry provide a 'Confidence Score' ( 0-100%) based on how clearly it was stated in the transcript.
- Use only information explicitely found in the transcript; do not add external items.
- Output the final result as a clean Markdown document.

Response Format:
##Decisions
- [Decision Name]: [Brief Description] (Confidence Score: X%)

##Action Item
| Action Item  | Owner | Deadline | Confidence Score |
| :---  | :--- | :--- | :--- |
| [Task]  | [Name] | [Date/Time] | [X%] |
"""

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_message),
    HumanMessagePromptTemplate.from_template("{transcript_text}")
])

print("----- Meeting Minutes Summarizer Initialized------")
transcript_input = input("Please paste the raw meeting transcript here: ")

# Invoke the model using the template.format() method
response = llm.invoke(template.format(
    transcript_text = transcript_input
))

# Output the formatted Markdown result
print("----- Structured Meeting Minutes ------\n")
print(response.content)

