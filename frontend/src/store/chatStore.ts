import { create } from 'zustand';
import axios from 'axios';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  updatedAt: Date;
}

interface ChatState {
  chats: Chat[];
  activeChatId: string | null;
  isLoading: boolean;
  error: string | null;
  addMessage: (chatId: string, role: 'user' | 'assistant', content: string) => void;
  sendMessage: (content: string) => Promise<void>;
  createNewChat: () => void;
  setActiveChat: (id: string) => void;
  deleteChat: (id: string) => void;
}

const generateId = () => Math.random().toString(36).substring(2, 15);

export const useChatStore = create<ChatState>((set, get) => ({
  chats: [{ id: 'default', title: 'New Conversation', messages: [], updatedAt: new Date() }],
  activeChatId: 'default',
  isLoading: false,
  error: null,

  addMessage: (chatId, role, content) => {
    set((state) => {
      const updatedChats = state.chats.map((chat) => {
        if (chat.id === chatId) {
          return {
            ...chat,
            messages: [...chat.messages, { id: generateId(), role, content, timestamp: new Date() }],
            updatedAt: new Date(),
          };
        }
        return chat;
      });
      return { chats: updatedChats, error: null };
    });
  },

  setActiveChat: (id) => set({ activeChatId: id }),

  createNewChat: () => {
    const newChat = {
      id: generateId(),
      title: 'New Conversation',
      messages: [],
      updatedAt: new Date(),
    };
    set((state) => ({
      chats: [newChat, ...state.chats],
      activeChatId: newChat.id,
      error: null,
    }));
  },

  deleteChat: (id) => {
    set((state) => {
      const filtered = state.chats.filter(c => c.id !== id);
      return {
        chats: filtered,
        activeChatId: state.activeChatId === id ? (filtered[0]?.id || null) : state.activeChatId,
      };
    });
  },

  sendMessage: async (content) => {
    const { activeChatId, addMessage, chats } = get();
    let currentId = activeChatId;

    if (!currentId) {
      currentId = generateId();
      set((state) => ({
        chats: [{ id: currentId as string, title: content.substring(0, 30) + '...', messages: [], updatedAt: new Date() }, ...state.chats],
        activeChatId: currentId,
      }));
    } else {
      // update title if it's the first message
      const chat = chats.find(c => c.id === currentId);
      if (chat && chat.messages.length === 0) {
        set((state) => ({
          chats: state.chats.map(c => c.id === currentId ? { ...c, title: content.substring(0, 30) + '...' } : c)
        }));
      }
    }

    // Add user message immediately
    addMessage(currentId, 'user', content);
    
    set({ isLoading: true, error: null });

    try {
      const currentChat = get().chats.find(c => c.id === currentId);
      const chat_history = currentChat ? currentChat.messages.map(m => ({
        role: m.role,
        content: m.content
      })) : [];

      const response = await axios.post('http://localhost:8000/ask', { 
        question: content,
        chat_history: chat_history
      });
      
      addMessage(currentId, 'assistant', response.data.answer);
      
    } catch (error: any) {
      console.error(error);
      set({ error: error.message || 'Failed to fetch response. Please try again later.' });
    } finally {
      set({ isLoading: false });
    }
  },
}));