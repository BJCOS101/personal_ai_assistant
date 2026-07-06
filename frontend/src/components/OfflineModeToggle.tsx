import React, { useState, useEffect } from 'react';
import { Cloud, WifiOff, Loader2 } from 'lucide-react';
import { api } from '../services/api';

export const OfflineModeToggle: React.FC = () => {
  const [offline, setOffline] = useState(false);
  const [loading, setLoading] = useState(true);
  const [switching, setSwitching] = useState(false);

  const loadStatus = async () => {
    try {
      const status = await api.getLLMProvider();
      setOffline(status.offline_mode);
    } catch (err) {
      console.error('Error loading LLM provider status:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const handleToggle = async () => {
    const wantsOffline = !offline;
    setSwitching(true);
    try {
      const status = await api.setLLMProvider(wantsOffline);
      setOffline(status.offline_mode);
    } catch (err: any) {
      alert(
        `Couldn't switch to ${wantsOffline ? 'offline' : 'online'} mode: ` +
        (err.response?.data?.detail || err.message)
      );
    } finally {
      setSwitching(false);
    }
  };

  if (loading) {
    return <Loader2 className="w-4 h-4 text-gray-400 animate-spin" />;
  }

  return (
    <button
      onClick={handleToggle}
      disabled={switching}
      title={offline ? 'Offline mode: nothing leaves your machine' : 'Online mode: using cloud AI (Groq)'}
      className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium border transition-colors ${
        offline
          ? 'bg-green-50 border-green-300 text-green-700 hover:bg-green-100'
          : 'bg-blue-50 border-blue-300 text-blue-700 hover:bg-blue-100'
      } ${switching ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      {switching ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : offline ? (
        <WifiOff className="w-4 h-4" />
      ) : (
        <Cloud className="w-4 h-4" />
      )}
      {offline ? 'Offline Mode: On' : 'Offline Mode: Off'}
    </button>
  );
};
