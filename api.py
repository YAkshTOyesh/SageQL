from fastapi import FastAPI
from pydantic import BaseModel
from services.open_router import query_openrouter

# Create a Pydantic model for request body validation
class QueryRequest(BaseModel):
    query: str

api = FastAPI()

# Endpoint for streaming SQL generation

async def generate_sql_response(prompt:str):
    # Fetch the response from OpenRouter
    response = await query_openrouter(prompt)
    whole_message = response.choices[0].message.content
    
    # Return the result as a JSON response
    return {"sql_part": whole_message}

@api.post("/generate_sql")
async def generate_sql(request: QueryRequest):
    # Return the generated SQL part as JSON
    json_ans = await generate_sql_response(request.query)
    return json_ans
