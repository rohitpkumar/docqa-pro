'use client';

import { useState } from 'react';

export default function Chat() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    setAnswer('');
    
    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: question }),
      });
      const data = await response.json();
      setAnswer(data.text);
    } catch (error) {
      setAnswer('Error: Could not connect to backend. Make sure the API is running.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-2">
          DocQA Pro
        </h1>
        <p className="text-center text-gray-600 mb-8">
          Ask questions about GPT-4, Claude 3, Gemini, Llama 4, and Mistral Large
        </p>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="mb-4">
            <textarea
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              rows={3}
              placeholder="Ask a question, e.g., What is Claude 3's context window?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
          </div>
          
          <button
            onClick={askQuestion}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-blue-300 transition"
          >
            {loading ? 'Thinking...' : 'Ask Question'}
          </button>
          
          {answer && (
            <div className="mt-6 p-4 bg-gray-100 rounded-lg">
              <h3 className="font-semibold text-gray-700 mb-2">Answer:</h3>
              <p className="text-black whitespace-pre-wrap">{answer}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}