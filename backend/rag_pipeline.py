# rag_pipeline.py - OPTIMIZED with persistent storage

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found")
    exit(1)
print(f"✅ API key loaded")

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings,
    StorageContext
)
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import load_index_from_storage

# Configure OpenAI
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

# Where to save the index
PERSIST_DIR = "./storage"

# Check if index already exists
if os.path.exists(PERSIST_DIR):
    print("\n📂 Loading existing index from disk...")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    print("✅ Index loaded (no API calls made)")
else:
    print("\n📁 First time setup: Loading PDFs and creating index...")
    reader = SimpleDirectoryReader("documents")
    documents = reader.load_data()
    print(f"✅ Loaded {len(documents)} pages")
    
    print("\n✂️  Splitting into optimized chunks...")
    parser = SimpleNodeParser.from_defaults(
        chunk_size=1500,
        chunk_overlap=200
    )
    nodes = parser.get_nodes_from_documents(documents)
    print(f"✅ Created {len(nodes)} chunks")
    
    print("\n🔢 Creating embeddings (one-time cost)...")
    index = VectorStoreIndex.from_documents(documents)
    
    # SAVE TO DISK - THIS IS THE OPTIMIZATION
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print(f"✅ Index saved to {PERSIST_DIR}")

query_engine = index.as_query_engine()

print("\n" + "="*50)
print("DocQA Pro Ready! Ask about GPT-4, Claude, Gemini, Llama, Mistral")
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