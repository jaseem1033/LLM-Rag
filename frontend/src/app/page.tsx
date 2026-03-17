import { ChatWindow } from '@/components/chat/ChatWindow';
import { Sidebar } from '@/components/chat/Sidebar';

export default function Home() {
  return (
    <main className="flex h-screen bg-white dark:bg-gray-950 font-sans overflow-hidden">
      <Sidebar />
      <ChatWindow />
    </main>
  );
}
