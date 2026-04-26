from fastapi import FastAPI
from pydantic import BaseModel
import requests
app = FastAPI()

class Query(BaseModel):
    issue: str

def retrieve_context(user_issue):
    with open("knowledge_base.txt", "r",encoding="utf-8") as file:
        knowledge = file.read()

    chunks = knowledge.split("\n\n")

    relevant_chunks = []
    for chunk in chunks:
        if any(word.lower() in chunk.lower() for word in user_issue.split()):
            relevant_chunks.append(chunk)

    return "\n".join(relevant_chunks[:2])
@app.get("/")
def read_root():
    return{"message": "AI DevOps Assistant is running"}

@app.post("/analyze")
def analyze_issue(query:Query):
    context=retrieve_context(query.issue)
    user_input = query.issue
    
    prompt = f"""
    You are a senior DevOps engineer.
    Use the following context:
    {context}
    Analyze the following issue:
    {user_input}
    Give response in this format:
    1. Root Cause
    2. Solution
    3. Prevention
    """

    response = requests.post(
       "http://ollama:11434/api/generate",
       json = {
           "model": "phi3",
           "prompt": prompt,
           "stream": False
       }
    )

    result = response.json()
    return {
        "retrieved_context": context,
        "analysis": result["response"]
    }

