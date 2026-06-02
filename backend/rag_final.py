import os
from dotenv import load_dotenv
load_dotenv()

from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

print("Loading PDFs...")
reader = PDFReader()
documents = []
pdf_files = [f for f in os.listdir("documents") if f.endswith('.pdf')]

for pdf in pdf_files:
    print(f"  Reading: {pdf}")
    docs = reader.load_data(file=os.path.join("documents", pdf))
    documents.extend(docs)
    print(f"    → {len(docs)} pages")

print(f"Total pages: {len(documents)}")

# Verify text extraction
print(f"Sample text: {documents[0].text[:200]}")
print("If you see readable English, PDF loading works.")

print("\nCreating index...")
db = chromadb.PersistentClient(path="./chroma_storage")
try:
    db.delete_collection("docqa")
except:
    pass
collection = db.create_collection("docqa")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
print("Index ready!\n")

query_engine = index.as_query_engine()

while True:
    q = input("Question (or quit): ").strip()
    if q.lower() == 'quit':
        break
    if q:
        r = query_engine.query(q)
        print(f"\nAnswer: {r.response}\n")