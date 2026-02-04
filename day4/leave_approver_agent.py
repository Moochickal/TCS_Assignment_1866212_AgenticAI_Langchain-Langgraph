from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from datetime import datetime

#Define the Typed State
class State(TypedDict):
    user_name: str
    user_email: str
    leave_approved_status: str
    response_email: str
    date: str

#Initialize the LLM
llm = ChatOllama(model="qwen3:30b", temperature=0, num_gpu=999, keep_alive=0)

#Node - Check if leave is approved
def check_email_node(state: State) -> State:
    """Node to determine leave approval status based on the user email.
    Example rule : if 'sick' is mentioned, approve leave automatically.
    """
    if "sick" in state["user_email"].lower():
        state["leave_approved_status"] = "Approved"
    else:
        state["leave_approved_status"] = "Rejected"
    return state

#Node - Generate Response Email
def generate_response_email_node(state: State) -> State:
    """Based on the leave approval status, write a response email back to the user on behalf of ther supervisor stating decision"""
    prompt = f"Write a short, polite an empathatic email to the user informing about the status of the leave.\
    Employee name is : {state['user_name']} and date is{state['date']}, leaves are {state['leave_approved_status']}"

    # if state["leave_approved_status"]:
    #     prompt = f"Write a short, polite email on behalf of the supervisor approving leave in response to : '{state['user_email']}'"
    # else:
    #     prompt = f"Write a short, polite email on behalf of the supervisor rejecting leave in response to : '{state['user_email']}'"

    response = llm.invoke(prompt)
    state["response_email"] = response.content
    return state


#Build the LangGraph

graph = StateGraph(State)

#Register nodes
graph.add_node("check_email", check_email_node)
graph.add_node("generate_response_email", generate_response_email_node)

#Define the execution flow
graph.add_edge(START, "check_email")
graph.add_edge("check_email","generate_response_email")
graph.add_edge("generate_response_email", END)


#Compile the graph
graph = graph.compile()

#Run the demo

initial_state ={
    "user_name": "Vishnu",
    #"user_email": "Hi, I am feeling sick and would like to take leave tomorrow.",
    "user_email": "Hi, I have a party to attend today and would like to avail a leave today.",
    "leave_approved_status": False,
    "response_email": "",
    "date": str(datetime.now().strftime("%Y-%m-%d"))
}

result = graph.invoke(initial_state)
print(result)
print("User Email:\n", result["user_email"])
print("Leave Approved?:", result["leave_approved_status"])
print("Response Email:\n", result["response_email"])

#Visualize the graph
#Get the graph in mermaid png format and save it

graph_image = graph.get_graph(xray=True).draw_mermaid_png()

with open("leave-approver.png","wb") as f:
    f.write(graph_image)

print("Graph Saved")





        



