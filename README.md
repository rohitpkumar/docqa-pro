# DocQA Pro – RAG System for LLM Documentation

**Ask questions across GPT-4, Claude 3, Gemini, Llama 4, and Mistral Large PDFs – with cited answers.**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org)

---

## 🎯 What It Does

Upload LLM documentation PDFs or use pre-loaded ones. Ask questions like:

- *"What is Claude 3's context window?"*
- *"Compare GPT-4 and Gemini"*
- *"Which models support vision?"*

The system retrieves relevant chunks and generates accurate answers.

---

## 🧠 How It Works

PDFs → Chunks (1500 chars) → Embeddings → ChromaDB → GPT-4 → Answer


| Component | Technology |
|-----------|------------|
| Backend | FastAPI + Python 3.12 |
| RAG | LlamaIndex |
| Vector DB | ChromaDB (0.3s load) |
| LLM | OpenAI GPT-3.5-Turbo |
| Frontend | Next.js + Tailwind |

---

## 📊 Evaluation Results

| Metric | Result |
|--------|--------|
| Accuracy (5 test Qs) | **100%** |
| Avg response time | 10.2 sec |
| Index load time | **0.3 sec** |

---

## 🏃 Quick Start

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key" > .env
python api.py

# Frontend (new terminal)
cd frontend
npm install && npm run dev

Open http://localhost:3000

🧪 Run Evaluation
cd backend && python evaluate.py

📁 Project Structure
backend/
├── api.py              # FastAPI server
├── evaluate.py         # Quality metrics
├── chroma_storage/     # Vector index
└── documents/          # LLM PDFs
frontend/
├── app/components/     # Chat UI
└── page.tsx

📝 Key RAG Decisions

Question	Answer
Chunk size?	1500 chars / 200 overlap
Why ChromaDB?	0.3s load vs 2+ min JSON
RAG vs fine-tune?	Add documents without retraining
