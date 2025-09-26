import { useState, useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { MessageInput } from './MessageInput';
import { LoadingIndicator } from './LoadingIndicator';
import { apiService } from '../services/api';

interface Message {
  id: string;
  content: string;
  type: 'user' | 'ai';
  timestamp: Date;
  isError?: boolean;
  sources?: string[];
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [config, setConfig] = useState({ title: 'Chatbot', description: 'AI Assistant' });
  const [sessionId, setSessionId] = useState<string>('default');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    // Fetch config on component mount
    const fetchConfig = async () => {
      try {
        const configData = await apiService.getConfig();
        setConfig(configData);
        // Update document title
        document.title = configData.title;
      } catch (error) {
        console.error('Failed to fetch config:', error);
      }
    };
    
    fetchConfig();
  }, []);

  // Get AI response from backend
  const getAIResponse = async (userMessage: string) => {
    setIsLoading(true);
    
    try {
      const response = await apiService.sendMessage(userMessage, sessionId);
      
      const aiMessage: Message = {
        id: Date.now().toString() + '-ai',
        content: response.response,
        type: 'ai',
        timestamp: new Date(),
        sources: response.sources,
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Failed to get AI response:', error);
      
      const errorMessage: Message = {
        id: Date.now().toString() + '-ai',
        content: 'Sorry, I encountered an error while processing your request. Please make sure the backend server is running and try again.',
        type: 'ai',
        timestamp: new Date(),
        isError: true,
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      type: 'user',
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // Get AI response from backend
    await getAIResponse(content);
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white border-b px-4 py-3 md:px-6 md:py-4 shadow-sm">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-lg md:text-xl text-gray-900">{config.title}</h1>
            <p className="text-xs md:text-sm text-gray-600 mt-1">{config.description}</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-3 md:px-6 md:py-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full px-4">
            <div className="text-center text-gray-500">
              <div className="w-12 h-12 md:w-16 md:h-16 mx-auto mb-3 md:mb-4 bg-gray-200 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 md:w-8 md:h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="text-base md:text-lg mb-2">Welcome to {config.title}</h3>
              <p className="text-xs md:text-sm">Start a conversation by sending a message below.</p>
            </div>
          </div>
        ) : (
          <div className="space-y-1">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isLoading && <LoadingIndicator />}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}