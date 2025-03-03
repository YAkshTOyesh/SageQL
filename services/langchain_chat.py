from typing import Optional  # Optional allows variables to be None
import streamlit as st
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_openai import ChatOpenAI  # Base class for OpenAI-compatible chat models
from settings import SETTINGS

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
    
    def _set_system_prompt(self):
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SETTINGS["system_prompt"],
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        return prompt_template
    
    def _chat_memory_workflow(self, has_system_prompt = False):
        # Define a new graph
        workflow = StateGraph(state_schema=MessagesState)

        # Define the function that calls the model
        def call_model(state: MessagesState):
            if has_system_prompt:
                prompt_template = self._set_system_prompt()
                prompt = prompt_template.invoke(state)
                response = self.invoke(prompt)
            else:
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
chat_history_thread_pirate = {"configurable": {"thread_id": "abc234"}}
chat_workflow_pirate = openrouter_model._chat_memory_workflow(has_system_prompt=True)

query_1 = "Hi! I'm Bob."

output_1 = openrouter_model._normal_chat_(chat_workflow, query_1, chat_history_thread)
output_1["messages"][-1].pretty_print()  # output contains all messages in state

# Change expert to pirate
query_3 = "Hi I'm Jim?"
output_3 = openrouter_model._normal_chat_(chat_workflow_pirate, query_3, chat_history_thread_pirate)

output_3["messages"][-1].pretty_print()

# See memory revert back
query_2 = "What's my name?"
output_2 = openrouter_model._normal_chat_(chat_workflow, query_2, chat_history_thread)

output_2["messages"][-1].pretty_print()








