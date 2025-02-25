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
 # Send POST request
    response = requests.post(API_URL, json={"query": query})

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the 'sql_part' field from the response
        message = data.get("sql_part", "")

        # Yield each character in the message
        for char in message:
            yield char
            time.sleep(0.01)
    else:
        # Handle the case where the request failed
        raise Exception(f"Request failed with status code {response.status_code}")

st.title("💬 Sage QL Chat Interface")
st.write("🚀 This is where you'll interact with Sage QL. (Coming Soon!)")
st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            # st.code(message["content"], language="sql", wrap_lines=True)
            st.markdown(message["content"])
        else:
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
        output = st.write_stream(fetch_sql_stream(prompt))

    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": output})
