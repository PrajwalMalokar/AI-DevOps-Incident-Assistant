from fastapi import FastAPI
from pydantic import BaseModel
import requests
app = FastAPI()

class Query(BaseModel):
    issue: str


@app.get("/")
def read_root():
    return{"message": "AI DevOps Assistant is running"}

@app.post("/analyze")
def analyze_issue(query:Query):
    user_input = query.issue
    
    prompt = f"""
    You are a senior DevOps engineer,
    Analyze the following issue:
    {user_input}
    Give response in this format:
    1. Root Cause
    2. Solution
    3. Prevention
    """

    response = requests.post(
       "http://localhost:11434/api/generate",
       json = {
           "model": "phi3",
           "prompt": prompt,
           "stream": False
       }
    )

    result = response.json()
    return {

        "analysis": result["response"]
    }

