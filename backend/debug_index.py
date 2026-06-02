import os
from dotenv import load_dotenv
load_dotenv()

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser

print("Step 1: Checking documents folder...")
documents_folder = "documents"
pdf_files = [f for f in os.listdir(documents_folder) if f.endswith('.pdf')]
print(f"Found {len(pdf_files)} PDFs:")
for f in pdf_files:
    print(f"  - {f}")

print("\nStep 2: Loading PDFs...")
reader = SimpleDirectoryReader(documents_folder)
documents = reader.load_data()
print(f"Loaded {len(documents)} pages")

print("\nStep 3: Creating chunks...")
parser = SimpleNodeParser.from_defaults(chunk_size=1500, chunk_overlap=200)
nodes = parser.get_nodes_from_documents(documents)
print(f"Created {len(nodes)} chunks")

print("\nStep 4: Checking chunk content...")
if nodes:
    sample_text = nodes[0].text[:200]
    print(f"First chunk preview: {sample_text}...")
else:
    print("No nodes created!")

print("\nStep 5: Checking for 'Claude' in chunks...")
claude_count = sum(1 for node in nodes if 'claude' in node.text.lower())
print(f"Chunks containing 'Claude': {claude_count} out of {len(nodes)}")
