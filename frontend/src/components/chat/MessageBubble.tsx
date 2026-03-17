'use client';

import { useChatStore, Message } from '../../store/chatStore';
import { cn } from '../../utils/cn';
import { Bot, Copy, RefreshCw, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { formatDistanceToNow } from 'date-fns';
import { useState } from 'react';

interface MessageBubbleProps {
  message: Message;
  isLast: boolean;
}

export function MessageBubble({ message, isLast }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={cn("group w-full border-b border-gray-100 dark:border-gray-800/50 flex transition-colors", 
      isUser ? "bg-white dark:bg-gray-900" : "bg-gray-50 dark:bg-gray-800"
    )}>
      <div className="flex w-full max-w-4xl mx-auto gap-4 md:gap-6 p-4 md:py-6">
        <div className="flex flex-col items-center">
          <div className={cn("flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border text-white shadow-sm",
            isUser ? "bg-blue-600 border-blue-700" : "bg-emerald-600 border-emerald-700"
          )}>
            {isUser ? <User size={18} /> : <Bot size={18} />}
          </div>
        </div>

        <div className="relative flex w-full min-w-0 flex-col">
          <div className="font-semibold text-gray-800 dark:text-gray-200">
            {isUser ? 'You' : 'AI Assistant'}
          </div>

          <div className="prose prose-sm md:prose-base prose-slate dark:prose-invert max-w-none break-words my-2">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>

          <div className="flex items-center justify-between mt-1">
            <div className="text-xs text-gray-400">
              {formatDistanceToNow(new Date(message.timestamp), { addSuffix: true })}
            </div>

            {!isUser && (
              <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={handleCopy}
                  className="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition"
                  title="Copy message"
                >
                  <Copy size={14} className={copied ? "text-green-500" : ""} />
                </button>
                {isLast && (
                  <button
                    className="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition"
                    title="Regenerate response"
                  >
                    <RefreshCw size={14} />
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}