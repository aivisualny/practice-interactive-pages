import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeSentiment = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>감정 분석 데모</h1>
        <div className="input-container">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="분석할 텍스트를 입력하세요..."
            rows="4"
          />
          <button onClick={analyzeSentiment} disabled={loading}>
            {loading ? '분석 중...' : '분석하기'}
          </button>
        </div>
        {result && (
          <div className="result-container">
            <h2>분석 결과</h2>
            <p>감정: {result.sentiment}</p>
            <p>신뢰도: {(result.confidence * 100).toFixed(2)}%</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App; 