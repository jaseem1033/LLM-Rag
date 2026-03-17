'use client';

import { useChatStore } from '../../store/chatStore';
import { MessageBubble } from './MessageBubble';
import { InputBar } from './InputBar';
import { useEffect, useRef } from 'react';
import { Bot, Lightbulb, MessageSquare } from 'lucide-react';

export function ChatWindow() {
  const { chats, activeChatId } = useChatStore();
  const activeChat = chats.find(c => c.id === activeChatId);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [activeChat?.messages]);

  if (!activeChat) {
    return <div className="flex-1 flex items-center justify-center text-gray-400">Loading chat...</div>;
  }

  const { messages } = activeChat;

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900 overflow-hidden relative w-full border-l border-gray-100 dark:border-gray-800">
      
      {/* Header */}
      <div className="h-14 border-b border-gray-100 dark:border-gray-800 flex items-center px-4 justify-between bg-white dark:bg-gray-900 z-10 sticky top-0">
        <div className="font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
          {activeChat.title || 'New Conversation'}
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <span className="flex h-2 w-2 rounded-full bg-green-500"></span> Online
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto w-full pb-32 pt-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-8 mt-20 text-center space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-500 flex-1">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-2xl flex items-center justify-center text-blue-600 dark:text-blue-400">
              <Bot size={32} />
            </div>
            <div className="space-y-2 max-w-xl">
              <h2 className="text-2xl font-bold tracking-tight text-gray-800 dark:text-gray-100">
                How can I help you today?
              </h2>
              <p className="text-gray-500 dark:text-gray-400">
                I'm your AI Assistant. You can ask me questions, have me explain concepts, or query your documents.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl text-left">
              {[
                { title: "Summarize text", icon: <MessageSquare size={18} />, color: "text-purple-500", desc: "Paste a long document to get a concise summary." },
                { title: "Explain a concept", icon: <Lightbulb size={18} />, color: "text-yellow-500", desc: "Ask about something complex to get it simplified." }
              ].map((card, i) => (
                <button 
                  key={i}
                  className="p-4 border border-gray-200 dark:border-gray-800 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-left flex flex-col gap-2"
                >
                  <div className={`flex items-center gap-2 font-medium text-gray-800 dark:text-gray-200 ${card.color}`}>
                    {card.icon} <span className="text-gray-800 dark:text-gray-200">{card.title}</span>
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400">{card.desc}</div>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex flex-col flex-1 pb-4">
            {messages.map((message, idx) => (
              <MessageBubble 
                key={message.id} 
                message={message} 
                isLast={idx === messages.length - 1} 
              />
            ))}
            <div ref={messagesEndRef} className="h-4" />
          </div>
        )}
      </div>

      {/* Input UI */}
      <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-white via-white to-transparent dark:from-gray-900 dark:via-gray-900 pt-6">
        <InputBar />
      </div>
    </div>
  );
}