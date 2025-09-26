// API service for communicating with FastAPI backend

// Use environment variable for API URL, with fallbacks
const API_BASE_URL = import.meta.env.VITE_API_URL || 
                     (import.meta.env.DEV ? '/api' : 'http://localhost:8000');

export interface ChatRequest {
    message: string;
    session_id?: string;
}

export interface ChatResponse {
    response: string;
    sources?: string[];
    session_id: string;
}

export interface KnowledgeEntry {
    id: string;
    key: string;
    value: string;
    tags: string[];
    createdAt: string;
    updatedAt: string;
}

export interface AppConfig {
    title: string;
    description: string;
}

class ApiService {
    private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
        const url = `${API_BASE_URL}${endpoint}`;

        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options?.headers,
                },
                ...options,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    async sendMessage(message: string, sessionId?: string): Promise<ChatResponse> {
        return this.request<ChatResponse>('/chat', {
            method: 'POST',
            body: JSON.stringify({ 
                message, 
                session_id: sessionId || 'default' 
            }),
        });
    }

    async getKnowledgeBase(): Promise<KnowledgeEntry[]> {
        return this.request<KnowledgeEntry[]>('/knowledge');
    }

    async getConfig(): Promise<AppConfig> {
        return this.request<AppConfig>('/config');
    }

    async healthCheck(): Promise<{ status: string }> {
        return this.request<{ status: string }>('/health');
    }

    async listSessions(): Promise<{ sessions: string[] }> {
        return this.request<{ sessions: string[] }>('/sessions');
    }

    async getSessionHistory(sessionId: string): Promise<{ session_id: string; history: any[] }> {
        return this.request<{ session_id: string; history: any[] }>(`/sessions/${sessionId}/history`);
    }

    async clearSession(sessionId: string): Promise<{ message: string }> {
        return this.request<{ message: string }>(`/sessions/${sessionId}`, {
            method: 'DELETE',
        });
    }
}

export const apiService = new ApiService();