# evaluate.py - Simple quality evaluation for DocQA Pro

import time
import os
from dotenv import load_dotenv

load_dotenv()

# Check API key
if not os.getenv("OPENAI_API_KEY"):
    print("❌ ERROR: OPENAI_API_KEY not found in .env file")
    exit(1)

print("✅ API key loaded")

from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

print("\n📂 Loading index from chroma_storage...")
db = chromadb.PersistentClient(path="./chroma_storage")
chroma_collection = db.get_or_create_collection("docqa")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine()
print("✅ Index loaded\n")

# Test questions with expected keywords
test_cases = [
    {
        "question": "What is Claude 3's context window?",
        "expected_keyword": "200k",
        "reason": "Claude 3 has 200k token context window in production"
    },
    {
        "question": "Which company created Claude 3?",
        "expected_keyword": "Anthropic",
        "reason": "Anthropic created Claude 3"
    },
    {
        "question": "Does GPT-4 support vision?",
        "expected_keyword": "vision",
        "reason": "GPT-4 is multimodal"
    },
    {
        "question": "What is Gemini?",
        "expected_keyword": "Google",
        "reason": "Gemini is Google's model"
    },
    {
        "question": "Compare Claude 3 and GPT-4",
        "expected_keyword": "Claude",
        "reason": "Comparison should mention at least Claude"
    }
]

# FIX 1 & 2: Initialize results list and total_time
results = []
total_time = 0

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. Question: {test['question']}")
    print(f"   Expected keyword: '{test['expected_keyword']}'")
    
    start_time = time.time()
    response = query_engine.query(test['question'])
    end_time = time.time()
    
    response_time = end_time - start_time
    answer = response.response
    answer_lower = answer.lower()
    
    # Check if expected keyword is in answer
    keyword_found = test['expected_keyword'].lower() in answer_lower
    
    # Calculate answer length (as proxy for completeness)
    answer_length = len(answer.split())
    
    results.append({
        "question": test['question'],
        "keyword_found": keyword_found,
        "response_time": round(response_time, 2),
        "answer_length": answer_length
    })
    
    total_time += response_time
    
    # Show result
    status = "✅ PASS" if keyword_found else "❌ FAIL"
    print(f"   Status: {status}")
    print(f"   Response time: {response_time:.2f} seconds")
    print(f"   Answer preview: {answer[:150]}...")

# Calculate overall metrics
total_questions = len(test_cases)
passed = sum(1 for r in results if r["keyword_found"])
accuracy = (passed / total_questions) * 100
avg_response_time = total_time / total_questions

print("\n" + "=" * 60)
print("Evaluation Summary")
print("=" * 60)
print(f"Total questions: {total_questions}")
print(f"Passed (keyword found): {passed}")
print(f"Failed: {total_questions - passed}")
print(f"Accuracy: {accuracy:.1f}%")
print(f"Average response time: {avg_response_time:.2f} seconds")

print("\n" + "=" * 60)
print("Detailed Results")
print("=" * 60)
print(f"{'#':<3} {'Status':<8} {'Time(s)':<8} {'Length':<8} Question")
print("-" * 60)
for i, r in enumerate(results, 1):
    status = "✅" if r["keyword_found"] else "❌"
    print(f"{i:<3} {status:<8} {r['response_time']:<8} {r['answer_length']:<8} {r['question'][:40]}...")

print("\n✅ Evaluation complete.")