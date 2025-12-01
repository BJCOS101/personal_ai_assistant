export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SourceDocument[];
  timestamp: string | Date;
}

export interface SourceDocument {
  content: string;
  filename: string;
  page?: number;
  relevance_score: number;
}

export interface DocumentMetadata {
  filename: string;
  file_path: string;
  file_type: string;
  file_size: number;
  upload_date: string;
  num_chunks: number;
}

export interface ChatResponse {
  answer: string;
  sources: SourceDocument[];
  conversation_id?: string;
}

export interface QueryRequest {
  query: string;
  conversation_history?: Array<{ role: string; content: string }>;
  max_sources?: number;
}