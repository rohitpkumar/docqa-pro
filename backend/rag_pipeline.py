# rag_pipeline.py - Using LlamaIndex (stable)

import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file")
    print("Please create a .env file with: OPENAI_API_KEY=your-key-here")
    exit(1)
print(f"✅ API key loaded (starts with: {api_key[:15]}...)")

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings
)
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser

# Configure OpenAI
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

# Step 1: Load PDFs from documents folder
documents_folder = "documents"
print(f"\n📁 Loading PDFs from: {documents_folder}")

try:
    reader = SimpleDirectoryReader(documents_folder)
    documents = reader.load_data()
    print(f"✅ Loaded {len(documents)} document pages")
except Exception as e:
    print(f"❌ Error loading documents: {e}")
    print("Make sure your PDFs are in the 'documents' folder")
    exit(1)

# Step 2: Split into chunks
print("\n✂️  Splitting documents into chunks...")
parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=50)
nodes = parser.get_nodes_from_documents(documents)
print(f"✅ Created {len(nodes)} chunks")

# Step 3: Create vector index
print("\n🔢 Creating embeddings and index...")
index = VectorStoreIndex.from_documents(documents)
print("✅ Index created")

# Step 4: Create query engine
query_engine = index.as_query_engine()

print("\n" + "="*50)
print("DocQA Pro is ready! Ask questions about your LLM documents.")
print("Type 'quit' to exit.")
print("="*50)

# Step 5: Interactive Q&A loop
while True:
    question = input("\n❓ Your question: ").strip()
    if question.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        break
    
    if not question:
        continue
    
    print("\n🤔 Searching documents...")
    try:
        response = query_engine.query(question)
        print(f"\n📖 Answer: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")