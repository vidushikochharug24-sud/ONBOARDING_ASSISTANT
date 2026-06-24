import React, { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { chatAPI } from '../utils/api';
import '../styles/codebase-chat.css';

export default function CodebaseChat({ guide }) {
  const guideId = guide?.id || guide?.guide_id;
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState('');
  const endRef = useRef(null);

  useEffect(() => {
    setMessages([]);
    setQuestion('');
    setError('');
    setIsTyping(false);
  }, [guideId]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || !guideId || isTyping) {
      return;
    }

    const nextUserMessage = { role: 'user', content: trimmedQuestion };
    const history = [...messages];

    setMessages((currentMessages) => [...currentMessages, nextUserMessage]);
    setQuestion('');
    setError('');
    setIsTyping(true);

    try {
      const response = await chatAPI.ask({
        guide_id: guideId,
        question: trimmedQuestion,
        conversation_history: history,
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.answer,
      };

      setMessages((currentMessages) => [...currentMessages, assistantMessage]);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get answer');
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <section className="codebase-chat">
      <div className="chat-header">
        <div>
          <h2>🤖 Ask about this codebase</h2>
          <p>Ask anything — how auth works, where to find X, what Y file does</p>
        </div>
      </div>

      <div className="chat-window">
        {messages.length === 0 ? (
          <div className="chat-empty-state">
            <p>Start a conversation about this guide and the underlying code.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={`${message.role}-${index}`}
              className={`chat-message ${message.role}`}
            >
              <div className="chat-bubble">
                {message.role === 'assistant' ? (
                  <div className="markdown-content">
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  </div>
                ) : (
                  <p>{message.content}</p>
                )}
              </div>
            </div>
          ))
        )}

        {isTyping && (
          <div className="chat-message assistant typing-message">
            <div className="chat-bubble typing-bubble">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
            </div>
          </div>
        )}

        <div ref={endRef} />
      </div>

      {error && <div className="chat-error">{error}</div>}

      <form className="chat-input-row" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about this codebase..."
          disabled={isTyping}
        />
        <button type="submit" className="chat-submit-button" disabled={isTyping || !question.trim()}>
          Ask
        </button>
      </form>
    </section>
  );
}