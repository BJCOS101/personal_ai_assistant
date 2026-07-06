import axios from 'axios';
import { DocumentMetadata, QueryRequest, ChatResponse, LLMProviderStatus } from '../types';

const API_BASE_URL = '/api';

export const api = {
  // Document management
  uploadDocument: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  listDocuments: async (): Promise<{ documents: DocumentMetadata[]; total_count: number }> => {
    const response = await axios.get(`${API_BASE_URL}/documents`);
    return response.data;
  },

  deleteDocument: async (filename: string): Promise<any> => {
    const response = await axios.delete(`${API_BASE_URL}/documents/${filename}`);
    return response.data;
  },

  clearKnowledgeBase: async (): Promise<any> => {
    const response = await axios.post(`${API_BASE_URL}/clear`);
    return response.data;
  },

  // Query
  query: async (request: QueryRequest): Promise<ChatResponse> => {
    const response = await axios.post(`${API_BASE_URL}/query`, request);
    return response.data;
  },

  // Health check
  healthCheck: async (): Promise<any> => {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  },

  // LLM provider (online/offline toggle)
  getLLMProvider: async (): Promise<LLMProviderStatus> => {
    const response = await axios.get(`${API_BASE_URL}/llm-provider`);
    return response.data;
  },

  setLLMProvider: async (offlineMode: boolean): Promise<LLMProviderStatus> => {
    const response = await axios.post(`${API_BASE_URL}/llm-provider`, {
      offline_mode: offlineMode,
    });
    return response.data;
  },
};

// WebSocket connection
export const createWebSocketConnection = (
  clientId: string,
  onMessage: (data: any) => void,
  onError: (error: Event) => void
): WebSocket => {
  const wsUrl = `ws://localhost:8000/api/ws/chat/${clientId}`;
  const ws = new WebSocket(wsUrl);

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    onError(error);
  };

  return ws;
};