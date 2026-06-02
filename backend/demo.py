# demo.py - Fast loading demo (loads index once)

import os
import time
from dotenv import load_dotenv

load_dotenv()

from llama_index.core import (
    StorageContext,
    load_index_from_storage
)

print("🚀 Loading DocQA Pro...", end=" ", flush=True)
start = time.time()

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

print(f"Ready in {time.time() - start:.1f}s\n")

print("=" * 50)
print("Demo Questions (pre-loaded for speed):")
print("=" * 50)

demo_questions = [
    "What is Claude 3's context window?",
]

for q in demo_questions:
    print(f"\n❓ {q}")
    print("🤔 Answering...", end=" ", flush=True)
    response = query_engine.query(q)
    print(f"\n📖 {response.response[:200]}")
    print("-" * 40)

print("\n✅ Demo ready. Type your own question below.\n")

while True:
    q = input("❓ Your question (or 'quit'): ").strip()
    if q.lower() == 'quit':
        break
    if q:
        response = query_engine.query(q)
        print(f"\n📖 {response.response}\n")