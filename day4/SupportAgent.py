from typing import List, Optional, Literal
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

# 1. Invoking LLM 
llm = ChatOllama(model="qwen3:30b", temperature=0, num_gpu=999, keep_alive=0)

# 2. Define the State
class SupportState(TypedDict):
    email_content: str
    urgency: str # Low, Medium, High
    topic: str # Account, Billing, Bug, Feature Request, Technical Issue
    knowledge_base_info: str
    draft_response: str
    action: str # auto_reply, escalate

# 3. Define Nodes ( The "Brain" steps)

def classify_email(state: SupportState):
    """Classifies urgency and topic."""
    prompt = f"""
    Analyze this customer email: {state['email_content']}

    Classify into:
    - Urgency: Low, Medium, High
    - Topic: Account, Billing, Bug, Feature Request, Technical Issue

    Return ONLY JSON: {{"urgency": "...", "topic":"..."}}
    """
    #Using Structured output or parsing the result
    res = llm.invoke(prompt)
    import json
    # parsing
    data = json.loads(res.content)
    return {"urgency": data['urgency'], "topic": data['topic']}

def research_kb(state: SupportState):
    """Mock Knowledge base search"""
    # in real world we can use RAG here, this is for assignment and conditional logic i have put
    kb_data = {
        "Account": "To reset password, go to Settings > Security > Reset.",
        "Billing": "Subscription double charges are refunded within 3-5 days.",
        "Technical Issue": "API 504 Errors usually indicate timeout; check server status page."
    }
    info = kb_data.get(state['topic'], "No specific documentation found.")
    return {"knowledge_base_info": info}

def draft_response(state: SupportState):
    """Drafts the customer reply."""
    prompt = f"""
    Topic: {state['topic']}
    Knowledge: {state['knowledge_base_info']}
    Email: {state['email_content']}

    Draft a professional response to the customer.
    """
    res = llm.invoke(prompt)
    return {"draft_response": res.content}

def router_logic(state: SupportState) -> Literal["auto_reply", "escalate"]:
    """Determines if the case is too complex for AI."""
    # Escalation Logic: High urgency OR Complex topics like Bugs/API errors go to humans
    if state['urgency'] == "High" or state['topic'] in ["Bug", "Technical Issue"]:
        #state['action'] = "escalate"
        return "escalate"
    #state['action'] = "auto_reply"
    return "auto_reply"

def apply_action(state: SupportState):
    #this logic matches the router to ensure the state is updated
    decision = "escalate" if state['urgency'] == "High" or state['topic'] in ["Bug", "Technical Issue"] else "auto_reply"
    return {"action": decision}

# 4. Build the Graph
workflow = StateGraph(SupportState)

workflow.add_node("classify", classify_email)
workflow.add_node("research", research_kb)
workflow.add_node("draft", draft_response)
workflow.add_node("apply_action", apply_action)

workflow.add_edge(START, "classify")
workflow.add_edge("classify","research")
workflow.add_edge("research", "draft")

#Draft Flows into the Action node first
workflow.add_edge("draft", "apply_action")

# Decision Point : Auto-reply vs Escalation
workflow.add_conditional_edges(
    "apply_action",
    router_logic,
    {
        "auto_reply" : END,
        "escalate": END # in larger system you can connect to 'human_node'
    }
)

app = workflow.compile()

# 5. Execution and Testing
if __name__ == "__main__":
    test_email = "I was charged twice for my subscription! This is urgent."

    print(f"------Processing Email: {test_email}-----")
    final_state = app.invoke({"email_content": test_email})

    print(f"\n[1] Urgency: {final_state['urgency']}")
    print(f"[2] Topic: {final_state['topic']}")
    print(f"[3] Decision: {final_state['action']}")
    print(f"\n[4] Draft Response:\n {final_state['draft_response']}")






