'use client';

import { useChatStore } from '../../store/chatStore';
import { Send, Pickaxe, Loader2, Link, FileUp } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import TextareaAutosize from 'react-textarea-autosize';

export function InputBar() {
  const { sendMessage, isLoading } = useChatStore();
  const [content, setContent] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = async () => {
    if (!content.trim() || isLoading) return;
    
    const message = content;
    setContent('');
    await sendMessage(message);
    
    // Focus back on input after sending
    setTimeout(() => {
      inputRef.current?.focus();
    }, 10);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="mx-auto w-full max-w-3xl px-4 pb-6 pt-2">
      <div className="relative flex w-full flex-col rounded-xl border border-gray-200 bg-white p-3 shadow-sm dark:border-gray-700 dark:bg-gray-800 transition-colors focus-within:ring-2 focus-within:ring-blue-500/50 focus-within:border-blue-500">
        <TextareaAutosize
          ref={inputRef}
          tabIndex={0}
          rows={1}
          maxRows={6}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything..."
          className="m-0 w-full resize-none border-0 bg-transparent p-0 pr-10 focus:ring-0 focus-visible:ring-0 dark:text-white sm:text-sm leading-relaxed"
        />
        <div className="flex items-center justify-between mt-2 pt-2 border-t border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-2">
            <button className="flex h-8 w-8 items-center justify-center rounded-md text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <FileUp size={18} />
            </button>
            <button className="flex h-8 w-8 items-center justify-center rounded-md text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <Link size={18} />
            </button>
          </div>
          <button
            onClick={handleSend}
            disabled={!content.trim() || isLoading}
            className="flex h-8 w-8 items-center justify-center rounded-md bg-blue-600 p-1 text-white shadow-sm transition-colors hover:bg-blue-700 disabled:bg-blue-300 disabled:opacity-50 dark:disabled:bg-blue-800"
          >
            {isLoading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
          </button>
        </div>
      </div>
      <div className="mt-2 text-center text-xs text-gray-500 dark:text-gray-400">
        AI Assistant can make mistakes. Consider verifying important information.
      </div>
    </div>
  );
}