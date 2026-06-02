# api.py - Simple FastAPI backend for DocQA Pro

import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# Initialize FastAPI
app = FastAPI(title="DocQA Pro API", description="RAG system for LLM documentation")

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the existing ChromaDB index
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

print("Loading index from chroma_storage...")
db = chromadb.PersistentClient(path="./chroma_storage")
chroma_collection = db.get_or_create_collection("docqa")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine()
print("Index loaded. API ready.")

# Request/Response models
class Question(BaseModel):
    text: str

class Answer(BaseModel):
    text: str

# API endpoint
@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    response = query_engine.query(question.text)
    return Answer(text=response.response)

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)