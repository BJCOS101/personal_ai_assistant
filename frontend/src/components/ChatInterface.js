import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Message } from './Message';
import { api } from '../services/api';
export const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };
    useEffect(() => {
        scrollToBottom();
    }, [messages]);
    const handleSend = async () => {
        if (!input.trim() || isLoading)
            return;
        const userMessage = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date(),
        };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);
        try {
            // Convert messages to conversation history format
            const conversationHistory = [...messages, userMessage].map((msg) => ({
                role: msg.role,
                content: msg.content,
            }));
            const response = await api.query({
                query: input,
                conversation_history: conversationHistory,
                max_sources: 3,
            });
            const assistantMessage = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: response.answer,
                sources: response.sources,
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, assistantMessage]);
        }
        catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: 'Sorry, I encountered an error processing your question. Please try again.',
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        }
        finally {
            setIsLoading(false);
        }
    };
    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };
    return (<div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (<div className="flex items-center justify-center h-full text-gray-500">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Welcome to your AI Knowledge Assistant</h2>
              <p>Upload documents and start asking questions!</p>
            </div>
          </div>) : (messages.map((message) => <Message key={message.id} message={message}/>))}
        {isLoading && (<div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
              <Loader2 className="w-5 h-5 text-white animate-spin"/>
            </div>
            <div className="bg-gray-100 rounded-lg px-4 py-3">
              <p className="text-gray-600">Thinking...</p>
            </div>
          </div>)}
        <div ref={messagesEndRef}/>
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex gap-2">
          <textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyDown} placeholder="Ask a question about your documents..." className="flex-1 resize-none rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500" rows={3} disabled={isLoading}/>
          <button onClick={handleSend} disabled={!input.trim() || isLoading} className="bg-blue-500 text-white rounded-lg px-6 py-3 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors">
            <Send className="w-5 h-5"/>
          </button>
        </div>
      </div>
    </div>);
};
