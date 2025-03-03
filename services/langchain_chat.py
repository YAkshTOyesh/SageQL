from typing import Optional  # Optional allows variables to be None
import streamlit as st
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from langchain_openai import ChatOpenAI  # Base class for OpenAI-compatible chat models

class ChatOpenRouter(ChatOpenAI):
    """
    Custom class that extends LangChain's ChatOpenAI to work with OpenRouter.
    It securely fetches the API key and sets OpenRouter's API endpoint.
    """

    def __init__(self,
                 openai_api_key: Optional[str] = None,  # Allows passing API key manually
                 **kwargs):  # Accepts additional keyword arguments
        """
        Initializes the ChatOpenRouter instance.
        If the API key is not provided explicitly, it is fetched from the environment.
        """
        openai_api_key = st.secrets["OPEN_ROUTER_API_KEY"]

        # Call the parent constructor with OpenRouter's API endpoint and the resolved API key
        super().__init__(
            base_url="https://openrouter.ai/api/v1",  # OpenRouter's API endpoint
            openai_api_key=openai_api_key,  # Pass the API key
            **kwargs  # Pass any additional arguments
        )
    
    def _chat_memory_workflow(self):
        # Define a new graph
        workflow = StateGraph(state_schema=MessagesState)

        # Define the function that calls the model
        def call_model(state: MessagesState):
            response = self.invoke(state["messages"])
            return {"messages": response}


        # Define the (single) node in the graph
        workflow.add_edge(START, "model")
        workflow.add_node("model", call_model)

        # Add memory
        memory = MemorySaver()
        app = workflow.compile(checkpointer=memory)
        return app

    def _normal_chat_(self, workflow, query, config):
        input_messages = [HumanMessage(query)]
        output = workflow.invoke({"messages": input_messages}, config)
        return output

# Create an instance of ChatOpenRouter with a specific model
openrouter_model = ChatOpenRouter(
    model_name="meta-llama/llama-3-8b-instruct:free"  # Using Claude 3.7 Sonnet model via OpenRouter
)

chat_history_thread = {"configurable": {"thread_id": "abc123"}}
chat_workflow = openrouter_model._chat_memory_workflow()

query_1 = "Hi! I'm Bob."

output_1 = openrouter_model._normal_chat_(chat_workflow, query_1, chat_history_thread)
output_1["messages"][-1].pretty_print()  # output contains all messages in state

query_2 = "What's my name?"
output_2 = openrouter_model._normal_chat_(chat_workflow, query_2, chat_history_thread)

output_2["messages"][-1].pretty_print()



