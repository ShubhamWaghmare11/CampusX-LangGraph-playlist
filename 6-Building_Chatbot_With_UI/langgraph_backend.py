from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama3-70b-8192")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]


def chat_node(state: ChatState):
    response = llm.invoke(state['messages']).content
    return {"messages": response}

graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)
checkpointer = InMemorySaver()

chatbot = graph.compile(checkpointer=checkpointer)
