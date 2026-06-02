# rag_chroma.py - CORRECTED (uses optimized chunk size)

import os
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found")
    exit(1)
print(f"✅ API key loaded")

from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    VectorStoreIndex,
    StorageContext
)
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

PERSIST_DIR = "./chroma_storage"

if os.path.exists(PERSIST_DIR):
    print("\n📂 Loading fast index from ChromaDB...")
    start = time.time()
    db = chromadb.PersistentClient(path=PERSIST_DIR)
    chroma_collection = db.get_or_create_collection("docqa")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)
    print(f"✅ Loaded in {time.time() - start:.1f} seconds")
else:
    print("\n📁 First time setup: Loading PDFs...")
    reader = SimpleDirectoryReader("documents")
    documents = reader.load_data()
    print(f"✅ Loaded {len(documents)} pages")
    
    print("\n✂️  Splitting into chunks with chunk_size=1500...")
    parser = SimpleNodeParser.from_defaults(chunk_size=1500, chunk_overlap=200)
    nodes = parser.get_nodes_from_documents(documents)
    print(f"✅ Created {len(nodes)} chunks")
    
    print("\n🔢 Creating embeddings (one-time cost ~$3.48)...")
    
    db = chromadb.PersistentClient(path=PERSIST_DIR)
    chroma_collection = db.create_collection("docqa")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # FIX: Use the pre-processed nodes, NOT the raw documents
    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context
    )
    
    print(f"✅ Fast index saved to {PERSIST_DIR} with {len(nodes)} chunks")

query_engine = index.as_query_engine()

print("\n" + "="*50)
print("DocQA Pro Ready (Fast ChromaDB version)")
print("Type 'quit' to exit")
print("="*50)

while True:
    question = input("\n❓ Question: ").strip()
    if question.lower() in ['quit', 'exit', 'q']:
        break
    if not question:
        continue
    print("🤔 Searching...")
    try:
        response = query_engine.query(question)
        print(f"\n📖 Answer: {response}\n")
    except Exception as e:
        print(f"❌ Error: {e}")