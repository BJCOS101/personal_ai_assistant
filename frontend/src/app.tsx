import React from 'react';
import { ChatInterface } from './components/ChatInterface';
import { DocumentUpload } from './components/DocumentUpload';
import { Sidebar } from './components/Sidebar';
import { Brain } from 'lucide-react';

function App() {
  const [refreshKey, setRefreshKey] = React.useState(0);

  const handleUploadComplete = () => {
    // Trigger sidebar refresh
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="bg-blue-500 rounded-lg p-2">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              Personal AI Knowledge Assistant
            </h1>
            <p className="text-sm text-gray-600">
              Ask questions about your documents
            </p>
          </div>
        </div>
      </header>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <aside className="w-80 bg-white border-r border-gray-200 flex flex-col overflow-hidden">
          <DocumentUpload onUploadComplete={handleUploadComplete} />
          <div className="flex-1 overflow-y-auto">
            <Sidebar key={refreshKey} />
          </div>
        </aside>

        {/* Chat */}
        <main className="flex-1 bg-white">
          <ChatInterface />
        </main>
      </div>
    </div>
  );
}

export default App;