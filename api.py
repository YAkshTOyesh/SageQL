from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

# Create a Pydantic model for request body validation
class QueryRequest(BaseModel):
    query: str

api = FastAPI()

# Endpoint for streaming SQL generation
# Async generator to stream SQL query parts
async def generate_sql_response(query: str):
    sql_query = f"SELECT * FROM users WHERE name LIKE '%{query}%';"  # Full SQL query
    words = sql_query.split()  # Split query into words

    for word in words:
        yield json.dumps({"sql_part": word}) + "\n"  # Send each word as JSON
        await asyncio.sleep(0.1)  # Simulate streaming delay

@api.post("/generate_sql")
async def generate_sql(request: QueryRequest):
    return StreamingResponse(generate_sql_response(request.query), media_type="application/json")
    # return StreamingResponse(generate_sql_response(query["query"]), media_type="application/json")
