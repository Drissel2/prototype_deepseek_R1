import { useState } from 'react';
import axios from 'axios';

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const res = await axios.post('/api/generate', { prompt });
      setResponse(res.data.generated_text);
    } catch (err) {
      setResponse('Error generating text.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-50">
      <h1 className="text-3xl font-extrabold mb-6 text-blue-700">DeepSeek AI Playground</h1>
      <textarea
        className="w-full max-w-2xl p-4 border-2 border-blue-300 rounded-lg shadow-md mb-4"
        rows={6}
        placeholder="Enter your prompt here..."
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
      />
      <button
        disabled={loading}
        className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-700 disabled:opacity-50"
        onClick={handleSubmit}
      >
        {loading ? 'Generating...' : 'Generate'}
      </button>
      <div className="w-full max-w-2xl mt-6 p-4 bg-white rounded-lg shadow-inner">
        <pre className="whitespace-pre-wrap">{response}</pre>
      </div>
    </div>
  );
}

export default App;
