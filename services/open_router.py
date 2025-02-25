from openai import OpenAI
import streamlit as st


async def query_openrouter(prompt: str):
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= st.secrets["OPEN_ROUTER_API_KEY"],
  )

  completion = client.chat.completions.create(
    model="meta-llama/llama-3-8b-instruct:free",
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ],
  )
  return completion
  

