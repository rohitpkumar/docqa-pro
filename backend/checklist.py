# checklist.py - Run this BEFORE any RAG script

import sys
import os
from dotenv import load_dotenv

print("=" * 50)
print("PRE-RUN CHECKLIST")
print("=" * 50)

# Check 1: Python version
print("\n1. Python version:")
print(f"   {sys.version}")

# Check 2: Virtual environment
print("\n2. Virtual environment:")
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("   ✅ Virtual environment is active")
else:
    print("   ❌ WARNING: No virtual environment active")

# Check 3: Required packages
print("\n3. Required packages:")
packages = [
    "llama_index.core",
    "llama_index.llms.openai", 
    "dotenv",
    "pypdf"
]
for pkg in packages:
    try:
        __import__(pkg.replace(".", "."))
        print(f"   ✅ {pkg}")
    except ImportError:
        print(f"   ❌ MISSING: {pkg}")

# Check 4: OpenAI API key
print("\n4. OpenAI API key:")
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key and api_key.startswith("sk-"):
    print(f"   ✅ API key loaded (starts with: {api_key[:15]}...)")
else:
    print("   ❌ API key missing or invalid")

# Check 5: Documents folder
print("\n5. Documents folder:")
if os.path.exists("documents"):
    pdf_count = len([f for f in os.listdir("documents") if f.endswith('.pdf')])
    print(f"   ✅ Found {pdf_count} PDF files")
else:
    print("   ❌ 'documents' folder not found")

# Check 6: Storage folder (if exists)
print("\n6. Existing storage:")
if os.path.exists("storage"):
    print("   ✅ Storage folder exists (will load from disk, $0 cost)")
else:
    print("   ℹ️  No storage folder found (will create fresh, one-time cost)")

print("\n" + "=" * 50)
print("If all checks passed, run: python rag_pipeline.py")
print("=" * 50)