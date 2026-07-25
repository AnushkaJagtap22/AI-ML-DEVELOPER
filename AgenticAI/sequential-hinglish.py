import os
from typing import TypedDict

#lets create state
class pipelinestate(TypedDict):
    raw_input : str 
    edited_text : str
    script_text : str
    final_output : str

from langchain_groq import  ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model = 'llama-3.3-70b-versatile', temperature=0.7)

# create nodes

def editor_node(state : pipelinestate) -> dict :
    """Stage 1 : Cleans up grammar , removes typos and refines the tone."""

    prompt = (
        "You are an expert copyeditor. Clean up the following raw text ." \
        "Fix any grammatical errors , spelling mistakes and smooth out the transition flow" \
        "while keeping the core message intact . Return only the edited text. \n\n " 
        f"Text : \n {state['raw_input']}"
    )
    response = llm.invoke(prompt)

    return {"edited_text" : response.content.strip()}

def scriptwriter_node(state : pipelinestate) -> dict :
    """Stage 2 : Formats the clean text into an engaging video script style."""
    print("\n --- [Stage 2] Executing ScriptWriter Node ---")

    prompt = (
        "You are a charismatic Youtube content creator . Take this edited text and tranform it " \
        "into a highly engaging , punchy , conversational video script hook . Make it sound like" \
        "a real person speaking passionately . Return only the sript content. \n\n"
        f"Edited Text : \n{state['edited_text']}"
    )

    response = llm.invoke(prompt)
    return {"script_text" : response.content.strip()}

def translate_node(state : pipelinestate) -> dict:
    """Stage 3 : Translate the script into natural flowing Hinglish"""
    print("\n --- [Stage 3] Executing Hinglish Translator Node ---")

    prompt = (
        "You are an expert content localizer  for the Indian market .Take the following script." \
        "and convert it into natural , flowing 'Hinglish'. Do not simply translate it sentence by sentencce " \
        "or repeat information. ALternating comfortably  between Hindi and English just like an intellectual tech " \
        "educator  would speak naturally on a live stream . Keep the energy high" \
        "Return only the final Hinglish text \n\n"
        f"Script:\n{state['script_text']}"
    )

    response = llm.invoke(prompt)
    return {"final_output" : response.content.strip()}

# now your state and nodes are ready 
# now it is time ti create a graph
# for creating graph you have to connect these nodes and for that use edges
# edges are very important to create the workflow

from langgraph.graph import StateGraph , START , END

# create the graph
graph = StateGraph(pipelinestate)

# add nodes to graph
graph.add_node("Editor",editor_node)
graph.add_node("ScriptWriter", scriptwriter_node)
graph.add_node("Translator", translate_node)

# add edges
# sequential
graph.add_edge(START,"Editor")
graph.add_edge('Editor','ScriptWriter')
graph.add_edge('ScriptWriter','Translator')
graph.add_edge('Translator',END)

#compile the graph 
app = graph.compile()

result = app.invoke({
    "raw_input" : "AI agents are the future of tech. They can think, plan, and act on their own. LangGraph helps you build these agents with proper control and memory."
})

#output 
print("your result are : - \n\n")
print(result['final_output'])