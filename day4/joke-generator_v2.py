from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

llm = ChatOllama(model="qwen3:30b", temperature=0, num_gpu=999, keep_alive=0)

class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str

def generate_joke(state: State):
    """First call to llm to generate initial joke"""
    initial_joke = llm.invoke(f"Write a short joke on {state['topic']}")
    return {"joke": initial_joke.content}

def check_punchline(state: State):
    """Gate to check the punchline in the code"""
    if "?" in state["joke"] or "!" in state["joke"]:
        return "Pass"
    return "FAIL"

def improved_joke(state: State):
    """Second call to llm to improve the joke"""
    improved_joke =llm.invoke(f"Make this joke funnier by adding a punchline or wordplay: {state['joke']}")
    return {"improved_joke": improved_joke.content}

def final_joke(state: State):
    """Polish the final joke"""
    joke_to_polish = state.get('improved_joke') or state.get('joke')
    final_joke = llm.invoke(f"Add a surprising twist to the joke: {joke_to_polish}")
    return {"final_joke": final_joke.content}

joke_graph = StateGraph(State)

joke_graph.add_node("generate_joke", generate_joke)
joke_graph.add_node("improved_joke", improved_joke)
joke_graph.add_node("final_joke", final_joke)

joke_graph.add_edge(START,"generate_joke")
joke_graph.add_conditional_edges("generate_joke", check_punchline, {"FAIL": "improved_joke", "Pass": "final_joke"})
joke_graph.add_edge("improved_joke", "final_joke")
joke_graph.add_edge("final_joke", END)

final_graph = joke_graph.compile()

graph_image = final_graph.get_graph(xray=True).draw_mermaid_png()

with open("joke_generator-graph.png", "wb") as file:
    file.write(graph_image)
    
state = final_graph.invoke({"topic": "Rabbit and Tortoise"})

print("\n---Workflow Reuslts ---")
print(f"Initial Joke: {state.get('joke', 'N/A')}")

#Safely check if the 'improved_joke' step was actually run
if 'improved_joke' in state:
    print(f"Improved Joke: {state['improved_joke']}")
else:
    print("Improved Joke: [SKIPPED - Initial joke passed the punchline check]")

print(f"Final Polished Joke: {state.get('final_joke', 'N/A')}")

      





