"""app.py"""
import streamlit as st
import random
import time
import requests
import json

# API endpoint for generating SQL
API_URL = "http://127.0.0.1:8000/generate_sql"

# Function to stream SQL response
# Function to fetch and stream SQL response word by word
def fetch_sql_stream(query):
    with requests.post(API_URL, json={"query": query}, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))  # Convert JSON response to dict
                yield data["sql_part"] + " "  # Extract the value of "sql_part"

st.title("💬 Sage QL Chat Interface")
st.write("🚀 This is where you'll interact with Sage QL. (Coming Soon!)")
st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write("Generating SQL query...")
        output = st.write_stream(fetch_sql_stream(prompt))  # ✅ Correct way to stream response

    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": output})
