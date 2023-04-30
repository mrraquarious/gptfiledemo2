import React, { useState } from 'react'
function Chatbox() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessages([...messages, { content: question, type: 'user' }]);
    const response = await fetch('http://localhost:5000/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });

    const eventSource = new EventSource(response.url);
    eventSource.onmessage = (event) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { content: event.data, type: 'bot' },
      ]);
    };
    setQuestion('');
  };

  return (
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index} style={{ textAlign: message.type === 'user' ? 'left' : 'right' }}>
            {message.content}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Chatbox;

