from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# 1. Initialize the local model via Ollama
# Updated initialization for your ScoringAgent.py
llm = ChatOllama(
    model="qwen3:30b", # Use a smaller quantization to fit 32GB
    temperature=0,
    num_gpu=999,  # Force offloading of all layers to GPU
    keep_alive=0  # Clear VRAM/RAM immediately after use
)

# 2. Define the mathematical tool for score calculation
@tool
def calculate_final_score(clarity: float, specificity: float, context: float, format_score: float, persona: float):
    """
    Calculates the final score as the mathematical average of the five quality criteria.
    This tool ensures accuracy that the LLM might miss on its own.
    """
    scores = [clarity, specificity, context, format_score, persona]
    final_score = sum(scores) / len(scores)
    return f"Final Score: {final_score:.1f}/10"

# List of tools available to the agent
tools = [calculate_final_score]

# 3. Define the System Persona and Evaulation Rules
system_prompt = """
You are a Senior Prompt Engineer. Your goal is to evaluate user prompts based on five pillars of quality.

Evaluation Criteria:
1. Clarity: Is the goal easy to understand and unambiguous?
2. Specificity: Are sufficient details and requirements provided?
3. Context: Is background info, audience, or a specific use case mentioned?
4. Output Format: Are constraints like tone, length, or structure specified?
5. Persona: Is a specific expert role or character assigned to the AI?

For every user input:
- Assign a numerical score (0-10) for each of the five criteria
- Use the 'calculate_final_score' tool to compute the average of the five numbers.
- Provide a brief, professional explanation for why you gave those scores.
- Offer 2-3 actionable suggestions for the user to improve their prompt.

Output your final response as a clean, structured Markdown report.
"""

# 4. Create the Chat Template
#  The agent_scratchpad is where the agent 'thinks' and processes tool results
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

#5. Bind tools and build the Agentic Workflow
llm_with_tools = llm.bind_tools(tools)
agent = create_tool_calling_agent(
    llm = llm_with_tools,
    tools = tools,
    prompt = prompt_template

)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 6. Execution Loop
print("---Prompt Quality Scoring Agent!(Ready)---")
print("Type your prompt to evaluate, or 'exit' to quit.")

while True:
    user_input  = input("\nPlease enter your prompt for evaluation: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Exiting the Prompt Quality Scoring Agent. Goodbye!")
        break

    try:
        # The AgentExecutor runs the ReAct loop ( Reason, Act , Think)
        result = agent_executor.invoke({"input": user_input})
        print("\n--- Evaluation Report ---\n")
        print(result["output"])
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")

    