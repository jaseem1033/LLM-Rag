'use client';

import { useChatStore } from '../../store/chatStore';
import { cn } from '../../utils/cn';
import { MessageSquare, Plus, Search, Trash2, Settings, User } from 'lucide-react';
import { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';

export function Sidebar() {
  const { chats, activeChatId, setActiveChat, createNewChat, deleteChat } = useChatStore();
  const [searchTerm, setSearchTerm] = useState('');

  const filteredChats = chats.filter((c) => 
    c.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex h-full w-[260px] flex-col bg-gray-950 p-3 text-white">
      <div className="mb-4 flex items-center gap-2">
        <button
          onClick={createNewChat}
          className="flex flex-1 items-center gap-2 rounded-md border border-white/20 p-3 text-sm font-medium transition-colors hover:bg-gray-800"
        >
          <Plus size={16} /> New Chat
        </button>
      </div>

      <div className="relative mb-4">
        <Search className="absolute left-3 top-2.5 text-gray-400" size={16} />
        <input
          type="text"
          placeholder="Search chats..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full rounded-md border border-gray-800 bg-gray-900 py-2 pl-9 pr-3 text-sm text-gray-200 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        />
      </div>

      <div className="flex-1 overflow-y-auto overflow-x-hidden space-y-1">
        {filteredChats.length === 0 ? (
          <div className="p-3 text-center text-sm text-gray-500">
            No chats found
          </div>
        ) : (
          filteredChats.map((chat) => (
            <div
              key={chat.id}
              onClick={() => setActiveChat(chat.id)}
              className={cn(
                "group relative flex cursor-pointer items-center gap-3 rounded-md p-3 text-sm transition-colors hover:bg-gray-800",
                activeChatId === chat.id ? "bg-gray-800 text-white" : "text-gray-300"
              )}
            >
              <MessageSquare size={16} className="text-gray-400 shrink-0" />
              <div className="flex-1 overflow-hidden">
                <div className="truncate">{chat.title || 'New Chat'}</div>
                <div className="truncate text-xs text-gray-500 mt-1">
                  {formatDistanceToNow(new Date(chat.updatedAt), { addSuffix: true })}
                </div>
              </div>
              <button
                className="absolute right-2 hidden text-gray-400 hover:text-red-400 group-hover:block"
                onClick={(e) => {
                  e.stopPropagation();
                  deleteChat(chat.id);
                }}
              >
                <Trash2 size={16} />
              </button>
            </div>
          ))
        )}
      </div>

      <div className="mt-4 border-t border-gray-800 pt-4">
        <div className="flex cursor-pointer items-center gap-3 rounded-md p-3 text-sm text-gray-300 transition-colors hover:bg-gray-800 hover:text-white">
          <Settings size={16} /> Settings
        </div>
        <div className="flex cursor-pointer items-center gap-3 rounded-md p-3 text-sm text-gray-300 transition-colors hover:bg-gray-800 hover:text-white">
          <User size={16} /> Profile
        </div>
      </div>
    </div>
  );
}