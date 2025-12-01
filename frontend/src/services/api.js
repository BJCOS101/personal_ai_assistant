import axios from 'axios';
const API_BASE_URL = '/api';
export const api = {
    // Document management
    uploadDocument: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },
    listDocuments: async () => {
        const response = await axios.get(`${API_BASE_URL}/documents`);
        return response.data;
    },
    deleteDocument: async (filename) => {
        const response = await axios.delete(`${API_BASE_URL}/documents/${filename}`);
        return response.data;
    },
    clearKnowledgeBase: async () => {
        const response = await axios.post(`${API_BASE_URL}/clear`);
        return response.data;
    },
    // Query
    query: async (request) => {
        const response = await axios.post(`${API_BASE_URL}/query`, request);
        return response.data;
    },
    // Health check
    healthCheck: async () => {
        const response = await axios.get(`${API_BASE_URL}/health`);
        return response.data;
    },
};
// WebSocket connection
export const createWebSocketConnection = (clientId, onMessage, onError) => {
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
