import React, { useEffect, useState } from 'react';
import './App.css';

interface Message {
  id: string;
  direction: 'SENT' | 'RECEIVED';
  content: string;
  timestamp: string;
}

interface Conversation {
  id: string;
  state: 'OPEN' | 'CLOSED';
  messages: Message[];
}

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const response = await fetch('http://localhost:8000/conversations/', {
        headers: {
          'Authorization': 'debug'
        }
      });
      if (!response.ok) {
        throw new Error('Falha ao carregar conversas');
      }
      const data = await response.json();
      setConversations(data);
    } catch (err) {
      setError('Erro ao carregar conversas');
      console.error('Erro:', err);
    }
  };

  const fetchConversationDetails = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:8000/conversations/${id}/`, {
        headers: {
          'Authorization': 'debug'
        }
      });
      if (!response.ok) {
        throw new Error('Falha ao carregar detalhes da conversa');
      }
      const data = await response.json();
      setSelectedConversation(data);
    } catch (err) {
      setError('Erro ao carregar detalhes da conversa');
      console.error('Erro:', err);
    }
  };

  const getMessageDirection = (direction: 'SENT' | 'RECEIVED') => {
    return direction === 'SENT' ? 'Enviada' : 'Recebida';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Conversas do WhatsApp</h1>
      </header>
      <div className="App-content">
        {error && <div className="error-message">{error}</div>}
        <div className="conversations-list">
          <h2>Conversas</h2>
          {conversations.map(conversation => (
            <div
              key={conversation.id}
              className={`conversation-item ${selectedConversation?.id === conversation.id ? 'selected' : ''}`}
              onClick={() => fetchConversationDetails(conversation.id)}
            >
              <span>ID: {conversation.id.substring(0, 8)}...</span>
              <span className={`status ${conversation.state.toLowerCase()}`}>
                {conversation.state === 'OPEN' ? 'ABERTA' : 'FECHADA'}
              </span>
            </div>
          ))}
        </div>
        {selectedConversation && (
          <div className="messages-panel">
            <h2>Mensagens</h2>
            <div className="messages-container">
              {selectedConversation.messages.map(message => (
                <div
                  key={message.id}
                  className={`message ${message.direction.toLowerCase()}`}
                >
                  <div className="message-direction">{getMessageDirection(message.direction)}</div>
                  <div className="message-content">{message.content}</div>
                  <div className="message-timestamp">
                    {new Date(message.timestamp).toLocaleString('pt-BR')}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
