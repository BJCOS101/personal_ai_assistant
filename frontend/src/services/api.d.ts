import { DocumentMetadata, QueryRequest, ChatResponse } from '../types';
export declare const api: {
    uploadDocument: (file: File) => Promise<any>;
    listDocuments: () => Promise<{
        documents: DocumentMetadata[];
        total_count: number;
    }>;
    deleteDocument: (filename: string) => Promise<any>;
    clearKnowledgeBase: () => Promise<any>;
    query: (request: QueryRequest) => Promise<ChatResponse>;
    healthCheck: () => Promise<any>;
};
export declare const createWebSocketConnection: (clientId: string, onMessage: (data: any) => void, onError: (error: Event) => void) => WebSocket;
