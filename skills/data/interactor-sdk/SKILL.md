---
name: interactor-sdk
description: Complete SDK implementations for Interactor platform integration. Use when building TypeScript/Node.js or Python applications that need full Interactor client libraries. Includes complete client classes, webhook handlers, SSE streaming, and production-ready patterns.
author: Interactor Integration Guide
---

# Interactor SDK Examples Skill

Production-ready SDK implementations for TypeScript/Node.js and Python with complete client classes, webhook handlers, and real-time streaming components.

## When to Use

- **New Integration**: Building a new application that needs Interactor integration
- **Client Library**: Need a complete, reusable client class for Interactor APIs
- **Webhook Handling**: Implementing secure webhook receivers with signature verification
- **Real-time Streaming**: Building SSE-based real-time features for AI agents or workflows
- **Reference Implementation**: Need production patterns for error handling, retries, and token management

## Prerequisites

- Completed setup from `interactor-auth` skill (OAuth client credentials)
- Understanding of the Interactor platform architecture
- For TypeScript: Node.js 18+ with TypeScript configured
  - Dependencies: `axios`, `@types/node`
- For Python: Python 3.9+
  - Dependencies: `httpx` (for async client), `requests` (for sync client)

### Environment Variables

```bash
# Required - from interactor-auth setup
INTERACTOR_CLIENT_ID=client_xxx
INTERACTOR_CLIENT_SECRET=secret_xxx

# Optional - webhook secret for signature verification
INTERACTOR_WEBHOOK_SECRET=whsec_xxx
```

## Platform Architecture Reference

```
┌─────────────────────────────────────────────────────────────────────┐
│  YOUR APPLICATION                                                    │
│                                                                      │
│  Your Users ──────> Your Backend ──────> INTERACTOR                 │
│  (you manage auth)  (client_credentials)  (platform APIs)           │
│                     (namespaces per user)                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Base URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Account Server** | `https://auth.interactor.com/api/v1` | Authentication, OAuth clients |
| **Core API** | `https://core.interactor.com/api/v1` | Credentials, Agents, Workflows |

---

## Namespace Handling

Namespaces provide multi-tenant isolation. Each namespace represents a distinct user or tenant in your application.

### Namespace Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| User-based | `user_12345` | Per-user credential storage |
| Organization-based | `org_acme_corp` | Team/company isolation |
| Composite | `org_acme_user_123` | User within organization |

### Passing Namespaces

Namespaces can be passed in two ways (both are supported):

```typescript
// Method 1: X-Namespace header (recommended for all endpoints)
headers: { 'X-Namespace': 'user_123' }

// Method 2: Query parameter (supported on list endpoints)
GET /credentials?namespace=user_123
```

**Best Practice**: Use the `X-Namespace` header consistently for clarity and to avoid URL encoding issues.

---

## TypeScript/Node.js SDK

### Complete InteractorClient Class

```typescript
// src/interactor/client.ts
import axios, { AxiosInstance, AxiosError } from 'axios';

// ============================================================================
// Types
// ============================================================================

export interface InteractorConfig {
  clientId: string;
  clientSecret: string;
  accountServerUrl?: string;
  coreApiUrl?: string;
  tokenRefreshBuffer?: number; // seconds before expiry to refresh
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface ApiResponse<T> {
  data: T;
  meta?: Record<string, any>;
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    current_page: number;
    total_pages: number;
    total_count: number;
    per_page: number;
  };
}

// Credential Types
export interface Credential {
  id: string;
  provider: string;
  status: 'active' | 'expired' | 'revoked';
  scopes: string[];
  created_at: string;
  updated_at: string;
  expires_at: string | null;
}

export interface CredentialToken {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
  scope?: string;
}

// AI Agent Types
export interface Assistant {
  id: string;
  name: string;
  model: string;
  system_prompt: string;
  tools: Tool[];
  data_sources: DataSource[];
  created_at: string;
  updated_at: string;
}

export interface Room {
  id: string;
  assistant_id: string;
  namespace: string;
  metadata: Record<string, any>;
  created_at: string;
}

export interface Message {
  id: string;
  room_id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  tool_calls?: ToolCall[];
  created_at: string;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  parameters: Record<string, any>;
  callback_url?: string;
}

export interface ToolCall {
  id: string;
  tool_id: string;
  arguments: Record<string, any>;
  status: 'pending' | 'completed' | 'failed';
  result?: any;
}

export interface DataSource {
  id: string;
  name: string;
  type: 'file' | 'url' | 'database';
  config: Record<string, any>;
  semantic_mappings: SemanticMapping[];
}

export interface SemanticMapping {
  field: string;
  description: string;
  type: string;
}

// Workflow Types
export interface Workflow {
  id: string;
  name: string;
  description: string;
  states: WorkflowState[];
  initial_state: string;
  created_at: string;
  updated_at: string;
}

export interface WorkflowState {
  name: string;
  type: 'action' | 'halting' | 'terminal';
  actions?: WorkflowAction[];
  transitions?: WorkflowTransition[];
  presentation?: HaltingPresentation;
}

export interface WorkflowAction {
  type: 'http' | 'email' | 'transform' | 'ai_process';
  config: Record<string, any>;
}

export interface WorkflowTransition {
  to: string;
  condition?: string;
  event?: string;
}

export interface HaltingPresentation {
  type: 'form' | 'approval' | 'selection';
  config: Record<string, any>;
}

export interface WorkflowInstance {
  id: string;
  workflow_id: string;
  namespace: string;
  current_state: string;
  context: Record<string, any>;
  status: 'running' | 'halted' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
}

export interface WorkflowThread {
  id: string;
  instance_id: string;
  messages: ThreadMessage[];
  created_at: string;
}

export interface ThreadMessage {
  id: string;
  role: 'user' | 'system' | 'workflow';
  content: string;
  created_at: string;
}

// Webhook Types
export interface Webhook {
  id: string;
  url: string;
  events: string[];
  secret: string;
  active: boolean;
  created_at: string;
}

// ============================================================================
// Interactor Client
// ============================================================================

export class InteractorClient {
  private config: Required<InteractorConfig>;
  private accountClient: AxiosInstance;
  private coreClient: AxiosInstance;
  private accessToken: string | null = null;
  private tokenExpiresAt: number = 0;

  constructor(config: InteractorConfig) {
    this.config = {
      accountServerUrl: 'https://auth.interactor.com/api/v1',
      coreApiUrl: 'https://core.interactor.com/api/v1',
      tokenRefreshBuffer: 60, // refresh 60s before expiry
      ...config,
    };

    // Account server client (for authentication)
    this.accountClient = axios.create({
      baseURL: this.config.accountServerUrl,
      headers: { 'Content-Type': 'application/json' },
    });

    // Core API client (for all other operations)
    this.coreClient = axios.create({
      baseURL: this.config.coreApiUrl,
      headers: { 'Content-Type': 'application/json' },
    });

    // Add auth interceptor to core client
    this.coreClient.interceptors.request.use(async (config) => {
      const token = await this.getAccessToken();
      config.headers.Authorization = `Bearer ${token}`;
      return config;
    });

    // Add error interceptor
    this.coreClient.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => this.handleError(error)
    );
  }

  // ============================================================================
  // Lifecycle Management
  // ============================================================================

  /**
   * Clear cached tokens and reset client state.
   * Call this when done using the client to free resources.
   */
  close(): void {
    this.accessToken = null;
    this.tokenExpiresAt = 0;
  }

  /**
   * Check if client has a valid (non-expired) token cached.
   */
  isAuthenticated(): boolean {
    const now = Date.now() / 1000;
    return this.accessToken !== null && now < this.tokenExpiresAt;
  }

  // ============================================================================
  // Authentication
  // ============================================================================

  async getAccessToken(): Promise<string> {
    const now = Date.now() / 1000;

    // Return cached token if still valid
    if (this.accessToken && now < this.tokenExpiresAt - this.config.tokenRefreshBuffer) {
      return this.accessToken;
    }

    // Request new token
    const response = await this.accountClient.post<ApiResponse<TokenResponse>>(
      '/oauth/token',
      {
        grant_type: 'client_credentials',
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret,
      }
    );

    const { access_token, expires_in } = response.data.data;
    this.accessToken = access_token;
    this.tokenExpiresAt = now + expires_in;

    return this.accessToken;
  }

  // ============================================================================
  // Credential Management
  // ============================================================================

  async initiateOAuth(
    namespace: string,
    provider: string,
    scopes: string[],
    redirectUri: string
  ): Promise<{ authorization_url: string; state: string }> {
    const response = await this.coreClient.post<ApiResponse<{ authorization_url: string; state: string }>>(
      '/oauth/initiate',
      { provider, scopes, redirect_uri: redirectUri },
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async completeOAuth(
    namespace: string,
    provider: string,
    code: string,
    state: string
  ): Promise<Credential> {
    const response = await this.coreClient.post<ApiResponse<Credential>>(
      '/oauth/callback',
      { provider, code, state },
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async getCredentialToken(
    namespace: string,
    credentialId: string
  ): Promise<CredentialToken> {
    const response = await this.coreClient.get<ApiResponse<CredentialToken>>(
      `/credentials/${credentialId}/token`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listCredentials(
    namespace: string,
    options?: { provider?: string; status?: string; page?: number; per_page?: number }
  ): Promise<PaginatedResponse<Credential>> {
    const response = await this.coreClient.get<PaginatedResponse<Credential>>(
      '/credentials',
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  async revokeCredential(namespace: string, credentialId: string): Promise<void> {
    await this.coreClient.delete(`/credentials/${credentialId}`, {
      headers: { 'X-Namespace': namespace },
    });
  }

  async refreshCredential(namespace: string, credentialId: string): Promise<Credential> {
    const response = await this.coreClient.post<ApiResponse<Credential>>(
      `/credentials/${credentialId}/refresh`,
      {},
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  // ============================================================================
  // AI Agents - Assistants
  // ============================================================================

  async createAssistant(
    namespace: string,
    data: {
      name: string;
      model: string;
      system_prompt: string;
      tools?: string[];
      data_sources?: string[];
      temperature?: number;
      max_tokens?: number;
    }
  ): Promise<Assistant> {
    const response = await this.coreClient.post<ApiResponse<Assistant>>(
      '/assistants',
      data,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async getAssistant(namespace: string, assistantId: string): Promise<Assistant> {
    const response = await this.coreClient.get<ApiResponse<Assistant>>(
      `/assistants/${assistantId}`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async updateAssistant(
    namespace: string,
    assistantId: string,
    data: Partial<{
      name: string;
      system_prompt: string;
      tools: string[];
      data_sources: string[];
      temperature: number;
      max_tokens: number;
    }>
  ): Promise<Assistant> {
    const response = await this.coreClient.patch<ApiResponse<Assistant>>(
      `/assistants/${assistantId}`,
      data,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listAssistants(
    namespace: string,
    options?: { page?: number; per_page?: number }
  ): Promise<PaginatedResponse<Assistant>> {
    const response = await this.coreClient.get<PaginatedResponse<Assistant>>(
      '/assistants',
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  async deleteAssistant(namespace: string, assistantId: string): Promise<void> {
    await this.coreClient.delete(`/assistants/${assistantId}`, {
      headers: { 'X-Namespace': namespace },
    });
  }

  // ============================================================================
  // AI Agents - Rooms (Conversations)
  // ============================================================================

  async createRoom(
    namespace: string,
    assistantId: string,
    metadata?: Record<string, any>
  ): Promise<Room> {
    const response = await this.coreClient.post<ApiResponse<Room>>(
      '/rooms',
      { assistant_id: assistantId, metadata },
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async getRoom(namespace: string, roomId: string): Promise<Room> {
    const response = await this.coreClient.get<ApiResponse<Room>>(
      `/rooms/${roomId}`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listRooms(
    namespace: string,
    options?: { assistant_id?: string; page?: number; per_page?: number }
  ): Promise<PaginatedResponse<Room>> {
    const response = await this.coreClient.get<PaginatedResponse<Room>>(
      '/rooms',
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  async deleteRoom(namespace: string, roomId: string): Promise<void> {
    await this.coreClient.delete(`/rooms/${roomId}`, {
      headers: { 'X-Namespace': namespace },
    });
  }

  // ============================================================================
  // AI Agents - Messages
  // ============================================================================

  async sendMessage(
    namespace: string,
    roomId: string,
    content: string,
    options?: { stream?: boolean }
  ): Promise<Message> {
    const response = await this.coreClient.post<ApiResponse<Message>>(
      `/rooms/${roomId}/messages`,
      { content, stream: options?.stream ?? false },
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listMessages(
    namespace: string,
    roomId: string,
    options?: { page?: number; per_page?: number; order?: 'asc' | 'desc' }
  ): Promise<PaginatedResponse<Message>> {
    const response = await this.coreClient.get<PaginatedResponse<Message>>(
      `/rooms/${roomId}/messages`,
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  // ============================================================================
  // AI Agents - Tools
  // ============================================================================

  async createTool(
    namespace: string,
    data: {
      name: string;
      description: string;
      parameters: Record<string, any>;
      callback_url?: string;
    }
  ): Promise<Tool> {
    const response = await this.coreClient.post<ApiResponse<Tool>>(
      '/tools',
      data,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async getTool(namespace: string, toolId: string): Promise<Tool> {
    const response = await this.coreClient.get<ApiResponse<Tool>>(
      `/tools/${toolId}`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listTools(
    namespace: string,
    options?: { page?: number; per_page?: number }
  ): Promise<PaginatedResponse<Tool>> {
    const response = await this.coreClient.get<PaginatedResponse<Tool>>(
      '/tools',
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  async deleteTool(namespace: string, toolId: string): Promise<void> {
    await this.coreClient.delete(`/tools/${toolId}`, {
      headers: { 'X-Namespace': namespace },
    });
  }

  async submitToolResult(
    namespace: string,
    roomId: string,
    toolCallId: string,
    result: any
  ): Promise<Message> {
    const response = await this.coreClient.post<ApiResponse<Message>>(
      `/rooms/${roomId}/tool-results`,
      { tool_call_id: toolCallId, result },
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  // ============================================================================
  // AI Agents - Data Sources
  // ============================================================================

  async createDataSource(
    namespace: string,
    data: {
      name: string;
      type: 'file' | 'url' | 'database';
      config: Record<string, any>;
      semantic_mappings?: SemanticMapping[];
    }
  ): Promise<DataSource> {
    const response = await this.coreClient.post<ApiResponse<DataSource>>(
      '/data-sources',
      data,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async getDataSource(namespace: string, dataSourceId: string): Promise<DataSource> {
    const response = await this.coreClient.get<ApiResponse<DataSource>>(
      `/data-sources/${dataSourceId}`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listDataSources(
    namespace: string,
    options?: { type?: string; page?: number; per_page?: number }
  ): Promise<PaginatedResponse<DataSource>> {
    const response = await this.coreClient.get<PaginatedResponse<DataSource>>(
      '/data-sources',
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  async syncDataSource(namespace: string, dataSourceId: string): Promise<void> {
    await this.coreClient.post(
      `/data-sources/${dataSourceId}/sync`,
      {},
      { headers: { 'X-Namespace': namespace } }
    );
  }

  async deleteDataSource(namespace: string, dataSourceId: string): Promise<void> {
    await this.coreClient.delete(`/data-sources/${dataSourceId}`, {
      headers: { 'X-Namespace': namespace },
    });
  }

  // ============================================================================
  // Workflows
  // ============================================================================

  async createWorkflow(
    namespace: string,
    data: {
      name: string;
      description?: string;
      states: WorkflowState[];
      initial_state: string;
    }
  ): Promise<Workflow> {
    const response = await this.coreClient.post<ApiResponse<Workflow>>(
      '/workflows',
      data,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async getWorkflow(namespace: string, workflowId: string): Promise<Workflow> {
    const response = await this.coreClient.get<ApiResponse<Workflow>>(
      `/workflows/${workflowId}`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listWorkflows(
    namespace: string,
    options?: { page?: number; per_page?: number }
  ): Promise<PaginatedResponse<Workflow>> {
    const response = await this.coreClient.get<PaginatedResponse<Workflow>>(
      '/workflows',
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  async deleteWorkflow(namespace: string, workflowId: string): Promise<void> {
    await this.coreClient.delete(`/workflows/${workflowId}`, {
      headers: { 'X-Namespace': namespace },
    });
  }

  // ============================================================================
  // Workflow Instances
  // ============================================================================

  async startWorkflowInstance(
    namespace: string,
    workflowId: string,
    initialContext?: Record<string, any>
  ): Promise<WorkflowInstance> {
    const response = await this.coreClient.post<ApiResponse<WorkflowInstance>>(
      '/workflow-instances',
      { workflow_id: workflowId, context: initialContext },
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async getWorkflowInstance(namespace: string, instanceId: string): Promise<WorkflowInstance> {
    const response = await this.coreClient.get<ApiResponse<WorkflowInstance>>(
      `/workflow-instances/${instanceId}`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listWorkflowInstances(
    namespace: string,
    options?: { workflow_id?: string; status?: string; page?: number; per_page?: number }
  ): Promise<PaginatedResponse<WorkflowInstance>> {
    const response = await this.coreClient.get<PaginatedResponse<WorkflowInstance>>(
      '/workflow-instances',
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  async submitWorkflowInput(
    namespace: string,
    instanceId: string,
    input: Record<string, any>
  ): Promise<WorkflowInstance> {
    const response = await this.coreClient.post<ApiResponse<WorkflowInstance>>(
      `/workflow-instances/${instanceId}/input`,
      input,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async triggerWorkflowEvent(
    namespace: string,
    instanceId: string,
    event: string,
    payload?: Record<string, any>
  ): Promise<WorkflowInstance> {
    const response = await this.coreClient.post<ApiResponse<WorkflowInstance>>(
      `/workflow-instances/${instanceId}/events`,
      { event, payload },
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async cancelWorkflowInstance(namespace: string, instanceId: string): Promise<void> {
    await this.coreClient.post(
      `/workflow-instances/${instanceId}/cancel`,
      {},
      { headers: { 'X-Namespace': namespace } }
    );
  }

  // ============================================================================
  // Workflow Threads
  // ============================================================================

  async getWorkflowThread(namespace: string, instanceId: string): Promise<WorkflowThread> {
    const response = await this.coreClient.get<ApiResponse<WorkflowThread>>(
      `/workflow-instances/${instanceId}/thread`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async sendWorkflowThreadMessage(
    namespace: string,
    instanceId: string,
    content: string
  ): Promise<ThreadMessage> {
    const response = await this.coreClient.post<ApiResponse<ThreadMessage>>(
      `/workflow-instances/${instanceId}/thread/messages`,
      { content },
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  // ============================================================================
  // Webhooks
  // ============================================================================

  async createWebhook(
    namespace: string,
    data: {
      url: string;
      events: string[];
      secret?: string;
    }
  ): Promise<Webhook> {
    const response = await this.coreClient.post<ApiResponse<Webhook>>(
      '/webhooks',
      data,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async getWebhook(namespace: string, webhookId: string): Promise<Webhook> {
    const response = await this.coreClient.get<ApiResponse<Webhook>>(
      `/webhooks/${webhookId}`,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async listWebhooks(
    namespace: string,
    options?: { page?: number; per_page?: number }
  ): Promise<PaginatedResponse<Webhook>> {
    const response = await this.coreClient.get<PaginatedResponse<Webhook>>(
      '/webhooks',
      {
        params: options,
        headers: { 'X-Namespace': namespace },
      }
    );
    return response.data;
  }

  async updateWebhook(
    namespace: string,
    webhookId: string,
    data: Partial<{ url: string; events: string[]; active: boolean }>
  ): Promise<Webhook> {
    const response = await this.coreClient.patch<ApiResponse<Webhook>>(
      `/webhooks/${webhookId}`,
      data,
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  async deleteWebhook(namespace: string, webhookId: string): Promise<void> {
    await this.coreClient.delete(`/webhooks/${webhookId}`, {
      headers: { 'X-Namespace': namespace },
    });
  }

  async rotateWebhookSecret(namespace: string, webhookId: string): Promise<Webhook> {
    const response = await this.coreClient.post<ApiResponse<Webhook>>(
      `/webhooks/${webhookId}/rotate-secret`,
      {},
      { headers: { 'X-Namespace': namespace } }
    );
    return response.data.data;
  }

  // ============================================================================
  // SSE Streaming URLs
  // ============================================================================

  async getRoomStreamUrl(namespace: string, roomId: string): Promise<string> {
    const token = await this.getAccessToken();
    return `${this.config.coreApiUrl}/rooms/${roomId}/stream?token=${token}&namespace=${namespace}`;
  }

  async getWorkflowStreamUrl(namespace: string, instanceId: string): Promise<string> {
    const token = await this.getAccessToken();
    return `${this.config.coreApiUrl}/workflow-instances/${instanceId}/stream?token=${token}&namespace=${namespace}`;
  }

  // ============================================================================
  // Error Handling
  // ============================================================================

  private handleError(error: AxiosError): Promise<never> {
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data as any;

      switch (status) {
        case 401:
          // Clear cached token on auth error
          this.accessToken = null;
          this.tokenExpiresAt = 0;
          throw new InteractorError('Authentication failed', 'AUTH_ERROR', status, data);
        case 403:
          throw new InteractorError('Permission denied', 'FORBIDDEN', status, data);
        case 404:
          throw new InteractorError('Resource not found', 'NOT_FOUND', status, data);
        case 422:
          throw new InteractorError('Validation error', 'VALIDATION_ERROR', status, data);
        case 429:
          throw new InteractorError('Rate limit exceeded', 'RATE_LIMITED', status, data);
        default:
          throw new InteractorError(
            data?.error || 'API request failed',
            'API_ERROR',
            status,
            data
          );
      }
    }

    if (error.request) {
      throw new InteractorError('Network error - no response received', 'NETWORK_ERROR');
    }

    throw new InteractorError(error.message, 'UNKNOWN_ERROR');
  }
}

// ============================================================================
// Custom Error Class
// ============================================================================

export class InteractorError extends Error {
  constructor(
    message: string,
    public code: string,
    public status?: number,
    public details?: any
  ) {
    super(message);
    this.name = 'InteractorError';
  }
}

// ============================================================================
// Retry Utility with Exponential Backoff
// ============================================================================

export interface RetryOptions {
  maxRetries?: number;
  baseDelayMs?: number;
  maxDelayMs?: number;
  retryOn?: (error: any) => boolean;
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxRetries = 3,
    baseDelayMs = 1000,
    maxDelayMs = 30000,
    retryOn = (error) => {
      // Retry on rate limits and transient errors
      const status = error?.status || error?.response?.status;
      return status === 429 || status === 503 || status === 502;
    },
  } = options;

  let lastError: any;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      lastError = error;

      if (attempt === maxRetries || !retryOn(error)) {
        throw error;
      }

      // Calculate delay with exponential backoff and jitter
      const exponentialDelay = baseDelayMs * Math.pow(2, attempt);
      const jitter = Math.random() * 1000;
      const delay = Math.min(exponentialDelay + jitter, maxDelayMs);

      // Check for Retry-After header
      const retryAfter = error?.response?.headers?.['retry-after'];
      const waitMs = retryAfter ? parseInt(retryAfter) * 1000 : delay;

      console.warn(
        `Request failed (attempt ${attempt + 1}/${maxRetries + 1}), ` +
        `retrying in ${Math.round(waitMs / 1000)}s: ${error.message}`
      );

      await new Promise((resolve) => setTimeout(resolve, waitMs));
    }
  }

  throw lastError;
}

// ============================================================================
// Singleton Factory (Connection Pooling)
// ============================================================================

let _clientInstance: InteractorClient | null = null;

export function getInteractorClient(config?: InteractorConfig): InteractorClient {
  if (!_clientInstance) {
    if (!config) {
      // Use environment variables if no config provided
      config = {
        clientId: process.env.INTERACTOR_CLIENT_ID!,
        clientSecret: process.env.INTERACTOR_CLIENT_SECRET!,
      };
    }
    _clientInstance = new InteractorClient(config);
  }
  return _clientInstance;
}

export function resetInteractorClient(): void {
  _clientInstance = null;
}
```

### Usage Example

```typescript
// src/example.ts
import {
  InteractorClient,
  InteractorError,
  getInteractorClient,
  withRetry
} from './interactor/client';

// Option 1: Create client directly
const client = new InteractorClient({
  clientId: process.env.INTERACTOR_CLIENT_ID!,
  clientSecret: process.env.INTERACTOR_CLIENT_SECRET!,
});

// Option 2: Use singleton (recommended for production)
// const client = getInteractorClient();

async function main() {
  const namespace = 'user_123'; // Your user's namespace

  try {
    // Create an AI assistant with retry logic
    const assistant = await withRetry(() =>
      client.createAssistant(namespace, {
        name: 'Customer Support Bot',
        model: 'gpt-4',
        system_prompt: 'You are a helpful customer support assistant.',
      })
    );
    console.log('Created assistant:', assistant.id);

    // Create a conversation room
    const room = await client.createRoom(namespace, assistant.id, {
      user_name: 'John Doe',
      topic: 'Order inquiry',
    });
    console.log('Created room:', room.id);

    // Send a message with custom retry options
    const response = await withRetry(
      () => client.sendMessage(namespace, room.id, 'Hello! I need help with my order.'),
      { maxRetries: 5, baseDelayMs: 2000 }
    );
    console.log('Assistant response:', response.content);

  } catch (error) {
    if (error instanceof InteractorError) {
      console.error(`Interactor Error [${error.code}]:`, error.message);
      if (error.details) console.error('Details:', error.details);
    } else {
      throw error;
    }
  }
}

main();
```

### Environment Validation

```typescript
// src/interactor/validate-env.ts
export function validateInteractorEnv(): void {
  const required = ['INTERACTOR_CLIENT_ID', 'INTERACTOR_CLIENT_SECRET'];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(
      `Missing required Interactor environment variables: ${missing.join(', ')}\n` +
      `Please configure these in your .env file or environment.`
    );
  }
}

// Call at application startup
// validateInteractorEnv();
```

---

## Python SDK

### Complete InteractorClient Class

```python
# interactor/client.py
import asyncio
import time
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass
from enum import Enum

import httpx

# ============================================================================
# Types
# ============================================================================

T = TypeVar('T')

@dataclass
class InteractorConfig:
    client_id: str
    client_secret: str
    account_server_url: str = "https://auth.interactor.com/api/v1"
    core_api_url: str = "https://core.interactor.com/api/v1"
    token_refresh_buffer: int = 60  # seconds before expiry to refresh

@dataclass
class TokenInfo:
    access_token: str
    expires_at: float

@dataclass
class PaginationMeta:
    current_page: int
    total_pages: int
    total_count: int
    per_page: int

@dataclass
class PaginatedResponse:
    data: List[Dict[str, Any]]
    meta: PaginationMeta

class CredentialStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"

class WorkflowStatus(Enum):
    RUNNING = "running"
    HALTED = "halted"
    COMPLETED = "completed"
    FAILED = "failed"

# ============================================================================
# Custom Exceptions
# ============================================================================

class InteractorError(Exception):
    def __init__(
        self,
        message: str,
        code: str,
        status: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.code = code
        self.status = status
        self.details = details

class AuthenticationError(InteractorError):
    pass

class NotFoundError(InteractorError):
    pass

class ValidationError(InteractorError):
    pass

class RateLimitError(InteractorError):
    pass

# ============================================================================
# Interactor Client
# ============================================================================

class InteractorClient:
    def __init__(self, config: InteractorConfig):
        self.config = config
        self._token_info: Optional[TokenInfo] = None
        self._lock = asyncio.Lock()

    # ============================================================================
    # Authentication
    # ============================================================================

    async def _get_access_token(self) -> str:
        """Get valid access token, refreshing if necessary."""
        async with self._lock:
            now = time.time()

            # Return cached token if still valid
            if (
                self._token_info
                and now < self._token_info.expires_at - self.config.token_refresh_buffer
            ):
                return self._token_info.access_token

            # Request new token
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.config.account_server_url}/oauth/token",
                    json={
                        "grant_type": "client_credentials",
                        "client_id": self.config.client_id,
                        "client_secret": self.config.client_secret,
                    },
                )
                response.raise_for_status()
                data = response.json()["data"]

                self._token_info = TokenInfo(
                    access_token=data["access_token"],
                    expires_at=now + data["expires_in"],
                )

                return self._token_info.access_token

    async def _request(
        self,
        method: str,
        path: str,
        namespace: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make authenticated request to Core API."""
        token = await self._get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            **(kwargs.pop("headers", {})),
        }

        if namespace:
            headers["X-Namespace"] = namespace

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.config.core_api_url}{path}",
                headers=headers,
                **kwargs
            )

            if response.status_code == 204:
                return {}

            self._handle_error(response)
            return response.json()

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle API errors."""
        if response.is_success:
            return

        try:
            data = response.json()
        except Exception:
            data = {}

        error_message = data.get("error", "API request failed")

        error_classes = {
            401: (AuthenticationError, "AUTH_ERROR"),
            403: (InteractorError, "FORBIDDEN"),
            404: (NotFoundError, "NOT_FOUND"),
            422: (ValidationError, "VALIDATION_ERROR"),
            429: (RateLimitError, "RATE_LIMITED"),
        }

        error_class, code = error_classes.get(
            response.status_code,
            (InteractorError, "API_ERROR")
        )

        if response.status_code == 401:
            self._token_info = None  # Clear cached token

        raise error_class(error_message, code, response.status_code, data)

    # ============================================================================
    # Credential Management
    # ============================================================================

    async def initiate_oauth(
        self,
        namespace: str,
        provider: str,
        scopes: List[str],
        redirect_uri: str
    ) -> Dict[str, str]:
        """Initiate OAuth flow for a provider."""
        response = await self._request(
            "POST",
            "/oauth/initiate",
            namespace=namespace,
            json={
                "provider": provider,
                "scopes": scopes,
                "redirect_uri": redirect_uri,
            },
        )
        return response["data"]

    async def complete_oauth(
        self,
        namespace: str,
        provider: str,
        code: str,
        state: str
    ) -> Dict[str, Any]:
        """Complete OAuth flow with authorization code."""
        response = await self._request(
            "POST",
            "/oauth/callback",
            namespace=namespace,
            json={
                "provider": provider,
                "code": code,
                "state": state,
            },
        )
        return response["data"]

    async def get_credential_token(
        self,
        namespace: str,
        credential_id: str
    ) -> Dict[str, Any]:
        """Get access token for a stored credential."""
        response = await self._request(
            "GET",
            f"/credentials/{credential_id}/token",
            namespace=namespace,
        )
        return response["data"]

    async def list_credentials(
        self,
        namespace: str,
        provider: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> PaginatedResponse:
        """List credentials for a namespace."""
        params = {"page": page, "per_page": per_page}
        if provider:
            params["provider"] = provider
        if status:
            params["status"] = status

        response = await self._request(
            "GET",
            "/credentials",
            namespace=namespace,
            params=params,
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    async def revoke_credential(self, namespace: str, credential_id: str) -> None:
        """Revoke a credential."""
        await self._request(
            "DELETE",
            f"/credentials/{credential_id}",
            namespace=namespace,
        )

    async def refresh_credential(
        self,
        namespace: str,
        credential_id: str
    ) -> Dict[str, Any]:
        """Manually refresh a credential."""
        response = await self._request(
            "POST",
            f"/credentials/{credential_id}/refresh",
            namespace=namespace,
        )
        return response["data"]

    # ============================================================================
    # AI Agents - Assistants
    # ============================================================================

    async def create_assistant(
        self,
        namespace: str,
        name: str,
        model: str,
        system_prompt: str,
        tools: Optional[List[str]] = None,
        data_sources: Optional[List[str]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """Create a new AI assistant."""
        response = await self._request(
            "POST",
            "/assistants",
            namespace=namespace,
            json={
                "name": name,
                "model": model,
                "system_prompt": system_prompt,
                "tools": tools or [],
                "data_sources": data_sources or [],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        return response["data"]

    async def get_assistant(self, namespace: str, assistant_id: str) -> Dict[str, Any]:
        """Get assistant by ID."""
        response = await self._request(
            "GET",
            f"/assistants/{assistant_id}",
            namespace=namespace,
        )
        return response["data"]

    async def update_assistant(
        self,
        namespace: str,
        assistant_id: str,
        **updates
    ) -> Dict[str, Any]:
        """Update an assistant."""
        response = await self._request(
            "PATCH",
            f"/assistants/{assistant_id}",
            namespace=namespace,
            json=updates,
        )
        return response["data"]

    async def list_assistants(
        self,
        namespace: str,
        page: int = 1,
        per_page: int = 20
    ) -> PaginatedResponse:
        """List assistants."""
        response = await self._request(
            "GET",
            "/assistants",
            namespace=namespace,
            params={"page": page, "per_page": per_page},
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    async def delete_assistant(self, namespace: str, assistant_id: str) -> None:
        """Delete an assistant."""
        await self._request(
            "DELETE",
            f"/assistants/{assistant_id}",
            namespace=namespace,
        )

    # ============================================================================
    # AI Agents - Rooms
    # ============================================================================

    async def create_room(
        self,
        namespace: str,
        assistant_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a conversation room."""
        response = await self._request(
            "POST",
            "/rooms",
            namespace=namespace,
            json={
                "assistant_id": assistant_id,
                "metadata": metadata or {},
            },
        )
        return response["data"]

    async def get_room(self, namespace: str, room_id: str) -> Dict[str, Any]:
        """Get room by ID."""
        response = await self._request(
            "GET",
            f"/rooms/{room_id}",
            namespace=namespace,
        )
        return response["data"]

    async def list_rooms(
        self,
        namespace: str,
        assistant_id: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> PaginatedResponse:
        """List rooms."""
        params = {"page": page, "per_page": per_page}
        if assistant_id:
            params["assistant_id"] = assistant_id

        response = await self._request(
            "GET",
            "/rooms",
            namespace=namespace,
            params=params,
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    async def delete_room(self, namespace: str, room_id: str) -> None:
        """Delete a room."""
        await self._request(
            "DELETE",
            f"/rooms/{room_id}",
            namespace=namespace,
        )

    async def update_room(
        self,
        namespace: str,
        room_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update room metadata."""
        response = await self._request(
            "PATCH",
            f"/rooms/{room_id}",
            namespace=namespace,
            json={"metadata": metadata or {}},
        )
        return response["data"]

    # ============================================================================
    # AI Agents - Messages
    # ============================================================================

    async def send_message(
        self,
        namespace: str,
        room_id: str,
        content: str,
        stream: bool = False,
        role: str = "user"
    ) -> Dict[str, Any]:
        """Send a message to a room."""
        response = await self._request(
            "POST",
            f"/rooms/{room_id}/messages",
            namespace=namespace,
            json={"content": content, "stream": stream, "role": role},
        )
        return response["data"]

    async def list_messages(
        self,
        namespace: str,
        room_id: str,
        page: int = 1,
        per_page: int = 50,
        order: str = "asc"
    ) -> PaginatedResponse:
        """List messages in a room."""
        response = await self._request(
            "GET",
            f"/rooms/{room_id}/messages",
            namespace=namespace,
            params={"page": page, "per_page": per_page, "order": order},
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    # ============================================================================
    # AI Agents - Tools
    # ============================================================================

    async def create_tool(
        self,
        namespace: str,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        callback_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a tool for assistants."""
        response = await self._request(
            "POST",
            "/tools",
            namespace=namespace,
            json={
                "name": name,
                "description": description,
                "parameters": parameters,
                "callback_url": callback_url,
            },
        )
        return response["data"]

    async def get_tool(self, namespace: str, tool_id: str) -> Dict[str, Any]:
        """Get tool by ID."""
        response = await self._request(
            "GET",
            f"/tools/{tool_id}",
            namespace=namespace,
        )
        return response["data"]

    async def list_tools(
        self,
        namespace: str,
        page: int = 1,
        per_page: int = 20
    ) -> PaginatedResponse:
        """List tools."""
        response = await self._request(
            "GET",
            "/tools",
            namespace=namespace,
            params={"page": page, "per_page": per_page},
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    async def delete_tool(self, namespace: str, tool_id: str) -> None:
        """Delete a tool."""
        await self._request(
            "DELETE",
            f"/tools/{tool_id}",
            namespace=namespace,
        )

    async def submit_tool_result(
        self,
        namespace: str,
        room_id: str,
        tool_call_id: str,
        result: Any
    ) -> Dict[str, Any]:
        """Submit result for a tool call."""
        response = await self._request(
            "POST",
            f"/rooms/{room_id}/tool-results",
            namespace=namespace,
            json={"tool_call_id": tool_call_id, "result": result},
        )
        return response["data"]

    # ============================================================================
    # AI Agents - Data Sources
    # ============================================================================

    async def create_data_source(
        self,
        namespace: str,
        name: str,
        source_type: str,
        config: Dict[str, Any],
        semantic_mappings: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Create a data source."""
        response = await self._request(
            "POST",
            "/data-sources",
            namespace=namespace,
            json={
                "name": name,
                "type": source_type,
                "config": config,
                "semantic_mappings": semantic_mappings or [],
            },
        )
        return response["data"]

    async def get_data_source(self, namespace: str, data_source_id: str) -> Dict[str, Any]:
        """Get data source by ID."""
        response = await self._request(
            "GET",
            f"/data-sources/{data_source_id}",
            namespace=namespace,
        )
        return response["data"]

    async def list_data_sources(
        self,
        namespace: str,
        source_type: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> PaginatedResponse:
        """List data sources."""
        params = {"page": page, "per_page": per_page}
        if source_type:
            params["type"] = source_type

        response = await self._request(
            "GET",
            "/data-sources",
            namespace=namespace,
            params=params,
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    async def sync_data_source(self, namespace: str, data_source_id: str) -> None:
        """Trigger data source sync."""
        await self._request(
            "POST",
            f"/data-sources/{data_source_id}/sync",
            namespace=namespace,
        )

    async def delete_data_source(self, namespace: str, data_source_id: str) -> None:
        """Delete a data source."""
        await self._request(
            "DELETE",
            f"/data-sources/{data_source_id}",
            namespace=namespace,
        )

    # ============================================================================
    # Workflows
    # ============================================================================

    async def create_workflow(
        self,
        namespace: str,
        name: str,
        states: List[Dict[str, Any]],
        initial_state: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a workflow."""
        response = await self._request(
            "POST",
            "/workflows",
            namespace=namespace,
            json={
                "name": name,
                "description": description,
                "states": states,
                "initial_state": initial_state,
            },
        )
        return response["data"]

    async def get_workflow(self, namespace: str, workflow_id: str) -> Dict[str, Any]:
        """Get workflow by ID."""
        response = await self._request(
            "GET",
            f"/workflows/{workflow_id}",
            namespace=namespace,
        )
        return response["data"]

    async def list_workflows(
        self,
        namespace: str,
        page: int = 1,
        per_page: int = 20
    ) -> PaginatedResponse:
        """List workflows."""
        response = await self._request(
            "GET",
            "/workflows",
            namespace=namespace,
            params={"page": page, "per_page": per_page},
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    async def delete_workflow(self, namespace: str, workflow_id: str) -> None:
        """Delete a workflow."""
        await self._request(
            "DELETE",
            f"/workflows/{workflow_id}",
            namespace=namespace,
        )

    # ============================================================================
    # Workflow Instances
    # ============================================================================

    async def start_workflow_instance(
        self,
        namespace: str,
        workflow_id: str,
        initial_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Start a workflow instance."""
        response = await self._request(
            "POST",
            "/workflow-instances",
            namespace=namespace,
            json={
                "workflow_id": workflow_id,
                "context": initial_context or {},
            },
        )
        return response["data"]

    async def get_workflow_instance(
        self,
        namespace: str,
        instance_id: str
    ) -> Dict[str, Any]:
        """Get workflow instance by ID."""
        response = await self._request(
            "GET",
            f"/workflow-instances/{instance_id}",
            namespace=namespace,
        )
        return response["data"]

    async def list_workflow_instances(
        self,
        namespace: str,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> PaginatedResponse:
        """List workflow instances."""
        params = {"page": page, "per_page": per_page}
        if workflow_id:
            params["workflow_id"] = workflow_id
        if status:
            params["status"] = status

        response = await self._request(
            "GET",
            "/workflow-instances",
            namespace=namespace,
            params=params,
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    async def submit_workflow_input(
        self,
        namespace: str,
        instance_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Submit input to a halted workflow instance."""
        response = await self._request(
            "POST",
            f"/workflow-instances/{instance_id}/input",
            namespace=namespace,
            json=input_data,
        )
        return response["data"]

    async def trigger_workflow_event(
        self,
        namespace: str,
        instance_id: str,
        event: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Trigger an event on a workflow instance."""
        response = await self._request(
            "POST",
            f"/workflow-instances/{instance_id}/events",
            namespace=namespace,
            json={"event": event, "payload": payload or {}},
        )
        return response["data"]

    async def cancel_workflow_instance(self, namespace: str, instance_id: str) -> None:
        """Cancel a workflow instance."""
        await self._request(
            "POST",
            f"/workflow-instances/{instance_id}/cancel",
            namespace=namespace,
        )

    # ============================================================================
    # Workflow Threads
    # ============================================================================

    async def get_workflow_thread(
        self,
        namespace: str,
        instance_id: str
    ) -> Dict[str, Any]:
        """Get workflow instance thread."""
        response = await self._request(
            "GET",
            f"/workflow-instances/{instance_id}/thread",
            namespace=namespace,
        )
        return response["data"]

    async def send_workflow_thread_message(
        self,
        namespace: str,
        instance_id: str,
        content: str
    ) -> Dict[str, Any]:
        """Send message to workflow thread."""
        response = await self._request(
            "POST",
            f"/workflow-instances/{instance_id}/thread/messages",
            namespace=namespace,
            json={"content": content},
        )
        return response["data"]

    # ============================================================================
    # Webhooks
    # ============================================================================

    async def create_webhook(
        self,
        namespace: str,
        url: str,
        events: List[str],
        secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a webhook."""
        response = await self._request(
            "POST",
            "/webhooks",
            namespace=namespace,
            json={
                "url": url,
                "events": events,
                "secret": secret,
            },
        )
        return response["data"]

    async def get_webhook(self, namespace: str, webhook_id: str) -> Dict[str, Any]:
        """Get webhook by ID."""
        response = await self._request(
            "GET",
            f"/webhooks/{webhook_id}",
            namespace=namespace,
        )
        return response["data"]

    async def list_webhooks(
        self,
        namespace: str,
        page: int = 1,
        per_page: int = 20
    ) -> PaginatedResponse:
        """List webhooks."""
        response = await self._request(
            "GET",
            "/webhooks",
            namespace=namespace,
            params={"page": page, "per_page": per_page},
        )
        return PaginatedResponse(
            data=response["data"],
            meta=PaginationMeta(**response["meta"]),
        )

    async def update_webhook(
        self,
        namespace: str,
        webhook_id: str,
        **updates
    ) -> Dict[str, Any]:
        """Update a webhook."""
        response = await self._request(
            "PATCH",
            f"/webhooks/{webhook_id}",
            namespace=namespace,
            json=updates,
        )
        return response["data"]

    async def delete_webhook(self, namespace: str, webhook_id: str) -> None:
        """Delete a webhook."""
        await self._request(
            "DELETE",
            f"/webhooks/{webhook_id}",
            namespace=namespace,
        )

    async def rotate_webhook_secret(
        self,
        namespace: str,
        webhook_id: str
    ) -> Dict[str, Any]:
        """Rotate webhook secret."""
        response = await self._request(
            "POST",
            f"/webhooks/{webhook_id}/rotate-secret",
            namespace=namespace,
        )
        return response["data"]

    # ============================================================================
    # SSE Streaming URLs
    # ============================================================================

    async def get_room_stream_url(self, namespace: str, room_id: str) -> str:
        """Get SSE stream URL for a room."""
        token = await self._get_access_token()
        return f"{self.config.core_api_url}/rooms/{room_id}/stream?token={token}&namespace={namespace}"

    async def get_workflow_stream_url(self, namespace: str, instance_id: str) -> str:
        """Get SSE stream URL for a workflow instance."""
        token = await self._get_access_token()
        return f"{self.config.core_api_url}/workflow-instances/{instance_id}/stream?token={token}&namespace={namespace}"
```

### Python Usage Example (Async)

```python
# example_async.py
import asyncio
import os
from interactor.client import InteractorClient, InteractorConfig, InteractorError

async def main():
    config = InteractorConfig(
        client_id=os.environ["INTERACTOR_CLIENT_ID"],
        client_secret=os.environ["INTERACTOR_CLIENT_SECRET"],
    )
    client = InteractorClient(config)
    namespace = "user_123"

    try:
        # Create assistant
        assistant = await client.create_assistant(
            namespace=namespace,
            name="Support Bot",
            model="gpt-4",
            system_prompt="You are a helpful assistant.",
        )
        print(f"Created assistant: {assistant['id']}")

        # Create room
        room = await client.create_room(
            namespace=namespace,
            assistant_id=assistant["id"],
            metadata={"user": "john@example.com"},
        )
        print(f"Created room: {room['id']}")

        # Send message
        response = await client.send_message(
            namespace=namespace,
            room_id=room["id"],
            content="Hello! How can you help me?",
        )
        print(f"Response: {response['content']}")

    except InteractorError as e:
        print(f"Error [{e.code}]: {e}")
        if e.details:
            print(f"Details: {e.details}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Python SDK (Sync Version)

For simpler use cases or synchronous codebases, use this synchronous client.

> **Note**: The sync client provides core functionality for credentials, assistants, rooms, messages,
> workflows, and webhooks. For advanced features like Tools, Data Sources, and Workflow Threads,
> use the async client. The sync client is designed for simpler integrations where async is not needed.

```python
# interactor/client_sync.py
import os
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================================================================
# Configuration
# ============================================================================

@dataclass
class InteractorConfig:
    client_id: str
    client_secret: str
    account_server_url: str = "https://auth.interactor.com/api/v1"
    core_api_url: str = "https://core.interactor.com/api/v1"
    token_refresh_buffer: int = 60
    timeout: int = 30

# ============================================================================
# Exceptions
# ============================================================================

class InteractorError(Exception):
    def __init__(self, message: str, code: str, status: Optional[int] = None, details: Optional[Dict] = None):
        super().__init__(message)
        self.code = code
        self.status = status
        self.details = details

class AuthenticationError(InteractorError):
    pass

class NotFoundError(InteractorError):
    pass

class RateLimitError(InteractorError):
    pass

# ============================================================================
# Sync Interactor Client
# ============================================================================

class InteractorClientSync:
    """Synchronous Interactor client using requests library."""

    def __init__(self, config: Optional[InteractorConfig] = None):
        if config is None:
            config = InteractorConfig(
                client_id=os.environ.get("INTERACTOR_CLIENT_ID", ""),
                client_secret=os.environ.get("INTERACTOR_CLIENT_SECRET", ""),
            )

        if not config.client_id or not config.client_secret:
            raise ValueError(
                "INTERACTOR_CLIENT_ID and INTERACTOR_CLIENT_SECRET are required. "
                "Set them as environment variables or pass a config object."
            )

        self.config = config
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0

        # Setup session with retry logic
        self._session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "PATCH", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("https://", adapter)

    def _get_access_token(self) -> str:
        """Get valid access token, refreshing if necessary."""
        now = time.time()

        if self._access_token and now < self._token_expires_at - self.config.token_refresh_buffer:
            return self._access_token

        response = self._session.post(
            f"{self.config.account_server_url}/oauth/token",
            json={
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            },
            timeout=self.config.timeout,
        )
        self._handle_error(response)

        data = response.json()["data"]
        self._access_token = data["access_token"]
        self._token_expires_at = now + data["expires_in"]

        return self._access_token

    def _request(
        self,
        method: str,
        path: str,
        namespace: Optional[str] = None,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to Core API."""
        token = self._get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        if namespace:
            headers["X-Namespace"] = namespace

        response = self._session.request(
            method,
            f"{self.config.core_api_url}{path}",
            headers=headers,
            params=params,
            json=json,
            timeout=self.config.timeout,
        )

        if response.status_code == 204:
            return {}

        self._handle_error(response)
        return response.json()

    def _handle_error(self, response: requests.Response) -> None:
        """Handle API errors."""
        if response.ok:
            return

        try:
            data = response.json()
        except Exception:
            data = {}

        error_message = data.get("error", {}).get("message", "API request failed")

        error_map = {
            401: (AuthenticationError, "AUTH_ERROR"),
            403: (InteractorError, "FORBIDDEN"),
            404: (NotFoundError, "NOT_FOUND"),
            422: (InteractorError, "VALIDATION_ERROR"),
            429: (RateLimitError, "RATE_LIMITED"),
        }

        error_class, code = error_map.get(response.status_code, (InteractorError, "API_ERROR"))

        if response.status_code == 401:
            self._access_token = None
            self._token_expires_at = 0

        raise error_class(error_message, code, response.status_code, data)

    # ========== Credentials ==========

    def list_credentials(self, namespace: str, **filters) -> Dict[str, Any]:
        return self._request("GET", "/credentials", namespace=namespace, params=filters)

    def get_credential(self, namespace: str, credential_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/credentials/{credential_id}", namespace=namespace)["data"]

    def get_credential_token(self, namespace: str, credential_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/credentials/{credential_id}/token", namespace=namespace)["data"]

    def initiate_oauth(
        self,
        namespace: str,
        service_id: str,
        redirect_uri: str,
        scopes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/oauth/initiate",
            namespace=namespace,
            json={"service_id": service_id, "redirect_uri": redirect_uri, "scopes": scopes},
        )["data"]

    def get_oauth_status(self, flow_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/oauth/status/{flow_id}")["data"]

    def delete_credential(self, namespace: str, credential_id: str) -> None:
        self._request("DELETE", f"/credentials/{credential_id}", namespace=namespace)

    # ========== Assistants ==========

    def create_assistant(self, namespace: str, **data) -> Dict[str, Any]:
        return self._request("POST", "/assistants", namespace=namespace, json=data)["data"]

    def get_assistant(self, namespace: str, assistant_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/assistants/{assistant_id}", namespace=namespace)["data"]

    def list_assistants(self, namespace: str, **params) -> Dict[str, Any]:
        return self._request("GET", "/assistants", namespace=namespace, params=params)

    def delete_assistant(self, namespace: str, assistant_id: str) -> None:
        self._request("DELETE", f"/assistants/{assistant_id}", namespace=namespace)

    # ========== Rooms ==========

    def create_room(
        self,
        namespace: str,
        assistant_id: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/rooms",
            namespace=namespace,
            json={"assistant_id": assistant_id, "metadata": metadata or {}},
        )["data"]

    def get_room(self, namespace: str, room_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/rooms/{room_id}", namespace=namespace)["data"]

    def list_rooms(self, namespace: str, **params) -> Dict[str, Any]:
        return self._request("GET", "/rooms", namespace=namespace, params=params)

    def delete_room(self, namespace: str, room_id: str) -> None:
        self._request("DELETE", f"/rooms/{room_id}", namespace=namespace)

    # ========== Messages ==========

    def send_message(self, namespace: str, room_id: str, content: str) -> Dict[str, Any]:
        return self._request(
            "POST",
            f"/rooms/{room_id}/messages",
            namespace=namespace,
            json={"content": content, "role": "user"},
        )["data"]

    def list_messages(self, namespace: str, room_id: str, **params) -> Dict[str, Any]:
        return self._request("GET", f"/rooms/{room_id}/messages", namespace=namespace, params=params)

    # ========== Workflows ==========

    def create_workflow(self, namespace: str, **data) -> Dict[str, Any]:
        return self._request("POST", "/workflows", namespace=namespace, json=data)["data"]

    def get_workflow(self, namespace: str, workflow_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/workflows/{workflow_id}", namespace=namespace)["data"]

    def list_workflows(self, namespace: str, **params) -> Dict[str, Any]:
        return self._request("GET", "/workflows", namespace=namespace, params=params)

    def start_workflow_instance(
        self,
        namespace: str,
        workflow_id: str,
        initial_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Start a workflow instance."""
        return self._request(
            "POST",
            "/workflow-instances",
            namespace=namespace,
            json={"workflow_id": workflow_id, "context": initial_context or {}},
        )["data"]

    def get_workflow_instance(self, namespace: str, instance_id: str) -> Dict[str, Any]:
        """Get workflow instance by ID."""
        return self._request("GET", f"/workflow-instances/{instance_id}", namespace=namespace)["data"]

    def list_workflow_instances(
        self,
        namespace: str,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
        **params
    ) -> Dict[str, Any]:
        """List workflow instances."""
        if workflow_id:
            params["workflow_id"] = workflow_id
        if status:
            params["status"] = status
        return self._request("GET", "/workflow-instances", namespace=namespace, params=params)

    def submit_workflow_input(
        self,
        namespace: str,
        instance_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Submit input to a halted workflow instance."""
        return self._request(
            "POST",
            f"/workflow-instances/{instance_id}/input",
            namespace=namespace,
            json=input_data,
        )["data"]

    def trigger_workflow_event(
        self,
        namespace: str,
        instance_id: str,
        event: str,
        payload: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Trigger an event on a workflow instance."""
        return self._request(
            "POST",
            f"/workflow-instances/{instance_id}/events",
            namespace=namespace,
            json={"event": event, "payload": payload or {}},
        )["data"]

    def cancel_workflow_instance(self, namespace: str, instance_id: str) -> None:
        """Cancel a workflow instance."""
        self._request("POST", f"/workflow-instances/{instance_id}/cancel", namespace=namespace)

    # ========== Webhooks ==========

    def create_webhook(self, namespace: str, url: str, events: List[str]) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/webhooks",
            namespace=namespace,
            json={"url": url, "events": events, "enabled": True},
        )["data"]

    def list_webhooks(self, namespace: str) -> Dict[str, Any]:
        return self._request("GET", "/webhooks", namespace=namespace)

    def delete_webhook(self, namespace: str, webhook_id: str) -> None:
        self._request("DELETE", f"/webhooks/{webhook_id}", namespace=namespace)

    def get_webhook(self, namespace: str, webhook_id: str) -> Dict[str, Any]:
        """Get webhook by ID."""
        return self._request("GET", f"/webhooks/{webhook_id}", namespace=namespace)["data"]

    def update_webhook(
        self,
        namespace: str,
        webhook_id: str,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        enabled: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update a webhook."""
        updates = {}
        if url is not None:
            updates["url"] = url
        if events is not None:
            updates["events"] = events
        if enabled is not None:
            updates["enabled"] = enabled
        return self._request(
            "PATCH",
            f"/webhooks/{webhook_id}",
            namespace=namespace,
            json=updates,
        )["data"]

    # ========== Update Methods ==========

    def update_assistant(
        self,
        namespace: str,
        assistant_id: str,
        **updates
    ) -> Dict[str, Any]:
        """Update an assistant."""
        return self._request(
            "PATCH",
            f"/assistants/{assistant_id}",
            namespace=namespace,
            json=updates,
        )["data"]

    def update_room(
        self,
        namespace: str,
        room_id: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Update room metadata."""
        return self._request(
            "PATCH",
            f"/rooms/{room_id}",
            namespace=namespace,
            json={"metadata": metadata or {}},
        )["data"]


# ============================================================================
# Singleton Factory
# ============================================================================

_sync_client_instance: Optional[InteractorClientSync] = None

def get_sync_client(config: Optional[InteractorConfig] = None) -> InteractorClientSync:
    """Get singleton sync client instance."""
    global _sync_client_instance
    if _sync_client_instance is None:
        _sync_client_instance = InteractorClientSync(config)
    return _sync_client_instance


# ============================================================================
# Environment Validation
# ============================================================================

def validate_env() -> None:
    """Validate required environment variables at startup."""
    required = ["INTERACTOR_CLIENT_ID", "INTERACTOR_CLIENT_SECRET"]
    missing = [key for key in required if not os.environ.get(key)]

    if missing:
        raise EnvironmentError(
            f"Missing required Interactor environment variables: {', '.join(missing)}"
        )
```

### Python Usage Example (Sync)

```python
# example_sync.py
import os
from interactor.client_sync import InteractorClientSync, InteractorError, get_sync_client, validate_env

# Validate environment at startup
validate_env()

# Option 1: Create client directly
client = InteractorClientSync()

# Option 2: Use singleton (recommended)
# client = get_sync_client()

def main():
    namespace = "user_123"

    try:
        # Create assistant
        assistant = client.create_assistant(
            namespace=namespace,
            name="Support Bot",
            model="gpt-4",
            system_prompt="You are a helpful assistant.",
        )
        print(f"Created assistant: {assistant['id']}")

        # Create room
        room = client.create_room(
            namespace=namespace,
            assistant_id=assistant["id"],
            metadata={"user": "john@example.com"},
        )
        print(f"Created room: {room['id']}")

        # Send message
        response = client.send_message(
            namespace=namespace,
            room_id=room["id"],
            content="Hello! How can you help me?",
        )
        print(f"Response: {response['content']}")

    except InteractorError as e:
        print(f"Error [{e.code}]: {e}")

if __name__ == "__main__":
    main()
```

---

## Webhook Handler Examples

### Express.js Webhook Handler

```typescript
// src/webhooks/express-handler.ts
import express from 'express';
import crypto from 'crypto';

const app = express();

// IMPORTANT: Use raw body for signature verification
app.use('/webhooks/interactor', express.raw({ type: 'application/json' }));

interface WebhookPayload {
  event: string;
  timestamp: string;
  data: Record<string, any>;
}

function verifySignature(
  payload: Buffer,
  signature: string,
  secret: string
): boolean {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}

app.post('/webhooks/interactor', async (req, res) => {
  const signature = req.headers['x-interactor-signature'] as string;
  const webhookSecret = process.env.INTERACTOR_WEBHOOK_SECRET!;

  // Verify signature
  if (!signature || !verifySignature(req.body, signature, webhookSecret)) {
    console.error('Invalid webhook signature');
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Parse payload
  const payload: WebhookPayload = JSON.parse(req.body.toString());

  // Handle events
  try {
    switch (payload.event) {
      case 'credential.connected':
        await handleCredentialConnected(payload.data);
        break;
      case 'credential.expired':
        await handleCredentialExpired(payload.data);
        break;
      case 'credential.revoked':
        await handleCredentialRevoked(payload.data);
        break;
      case 'room.message.created':
        await handleNewMessage(payload.data);
        break;
      case 'room.tool_call.pending':
        await handleToolCall(payload.data);
        break;
      case 'workflow.instance.halted':
        await handleWorkflowHalted(payload.data);
        break;
      case 'workflow.instance.completed':
        await handleWorkflowCompleted(payload.data);
        break;
      default:
        console.log(`Unhandled event: ${payload.event}`);
    }

    res.json({ received: true });
  } catch (error) {
    console.error('Webhook processing error:', error);
    res.status(500).json({ error: 'Processing failed' });
  }
});

// Event handlers
async function handleCredentialConnected(data: any) {
  console.log(`Credential connected: ${data.credential_id} for ${data.provider}`);
  // Update your database, notify user, etc.
}

async function handleCredentialExpired(data: any) {
  console.log(`Credential expired: ${data.credential_id}`);
  // Notify user to reconnect
}

async function handleCredentialRevoked(data: any) {
  console.log(`Credential revoked: ${data.credential_id}`);
  // Clean up dependent resources
}

async function handleNewMessage(data: any) {
  console.log(`New message in room ${data.room_id}: ${data.content}`);
  // Real-time notification to your frontend
}

async function handleToolCall(data: any) {
  console.log(`Tool call pending: ${data.tool_call_id} for ${data.tool_name}`);
  // Execute tool and submit result
}

async function handleWorkflowHalted(data: any) {
  console.log(`Workflow halted: ${data.instance_id} at ${data.current_state}`);
  // Notify user about required action
}

async function handleWorkflowCompleted(data: any) {
  console.log(`Workflow completed: ${data.instance_id}`);
  // Process final results
}

app.listen(3000, () => {
  console.log('Webhook server listening on port 3000');
});
```

### Flask Webhook Handler

```python
# webhooks/flask_handler.py
import hmac
import hashlib
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

WEBHOOK_SECRET = os.environ["INTERACTOR_WEBHOOK_SECRET"]

def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify webhook signature using HMAC SHA256."""
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)

@app.route("/webhooks/interactor", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("X-Interactor-Signature", "")

    # Verify signature
    if not verify_signature(request.data, signature):
        return jsonify({"error": "Invalid signature"}), 401

    payload = request.json
    event = payload["event"]
    data = payload["data"]

    # Route to handlers
    handlers = {
        "credential.connected": handle_credential_connected,
        "credential.expired": handle_credential_expired,
        "credential.revoked": handle_credential_revoked,
        "room.message.created": handle_new_message,
        "room.tool_call.pending": handle_tool_call,
        "workflow.instance.halted": handle_workflow_halted,
        "workflow.instance.completed": handle_workflow_completed,
    }

    handler = handlers.get(event)
    if handler:
        try:
            handler(data)
        except Exception as e:
            app.logger.error(f"Webhook handler error: {e}")
            return jsonify({"error": "Processing failed"}), 500
    else:
        app.logger.info(f"Unhandled event: {event}")

    return jsonify({"received": True})

# Event handlers
def handle_credential_connected(data):
    print(f"Credential connected: {data['credential_id']}")

def handle_credential_expired(data):
    print(f"Credential expired: {data['credential_id']}")

def handle_credential_revoked(data):
    print(f"Credential revoked: {data['credential_id']}")

def handle_new_message(data):
    print(f"New message in room {data['room_id']}")

def handle_tool_call(data):
    print(f"Tool call: {data['tool_call_id']}")

def handle_workflow_halted(data):
    print(f"Workflow halted: {data['instance_id']}")

def handle_workflow_completed(data):
    print(f"Workflow completed: {data['instance_id']}")

if __name__ == "__main__":
    app.run(port=3000, debug=True)
```

---

## SSE Streaming Examples

### React SSE Hook

```typescript
// src/hooks/useInteractorStream.ts
import { useState, useEffect, useCallback, useRef } from 'react';

export type StreamEvent =
  | { type: 'message.delta'; content: string }
  | { type: 'message.complete'; message: Message }
  | { type: 'tool_call.start'; tool_call: ToolCall }
  | { type: 'tool_call.complete'; tool_call: ToolCall }
  | { type: 'workflow.state_changed'; state: string; context: Record<string, any> }
  | { type: 'workflow.halted'; presentation: any }
  | { type: 'error'; error: string };

interface Message {
  id: string;
  role: string;
  content: string;
}

interface ToolCall {
  id: string;
  tool_id: string;
  arguments: Record<string, any>;
  status: string;
}

interface UseInteractorStreamOptions {
  onEvent?: (event: StreamEvent) => void;
  onError?: (error: Error) => void;
  autoReconnect?: boolean;
  reconnectInterval?: number;
}

interface UseInteractorStreamResult {
  isConnected: boolean;
  events: StreamEvent[];
  streamingContent: string;
  connect: (url: string) => void;
  disconnect: () => void;
}

export function useInteractorStream(
  options: UseInteractorStreamOptions = {}
): UseInteractorStreamResult {
  const {
    onEvent,
    onError,
    autoReconnect = true,
    reconnectInterval = 5000,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [streamingContent, setStreamingContent] = useState('');

  const eventSourceRef = useRef<EventSource | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const currentUrlRef = useRef<string | null>(null);

  const clearReconnectTimeout = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
  }, []);

  const disconnect = useCallback(() => {
    clearReconnectTimeout();
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setIsConnected(false);
    currentUrlRef.current = null;
  }, [clearReconnectTimeout]);

  const connect = useCallback((url: string) => {
    // Clean up existing connection
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }
    clearReconnectTimeout();

    currentUrlRef.current = url;
    const eventSource = new EventSource(url);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      setIsConnected(true);
      setStreamingContent('');
    };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as StreamEvent;

        // Handle streaming content
        if (data.type === 'message.delta') {
          setStreamingContent((prev) => prev + data.content);
        } else if (data.type === 'message.complete') {
          setStreamingContent('');
        }

        setEvents((prev) => [...prev, data]);
        onEvent?.(data);
      } catch (error) {
        console.error('Failed to parse SSE event:', error);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE connection error:', error);
      setIsConnected(false);
      eventSource.close();
      eventSourceRef.current = null;

      const err = new Error('SSE connection failed');
      onError?.(err);

      // Auto-reconnect
      if (autoReconnect && currentUrlRef.current) {
        reconnectTimeoutRef.current = setTimeout(() => {
          if (currentUrlRef.current) {
            connect(currentUrlRef.current);
          }
        }, reconnectInterval);
      }
    };
  }, [autoReconnect, reconnectInterval, onEvent, onError, clearReconnectTimeout]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    isConnected,
    events,
    streamingContent,
    connect,
    disconnect,
  };
}
```

### React Chat Component with Streaming

```tsx
// src/components/InteractorChat.tsx
import React, { useState, useEffect } from 'react';
import { InteractorClient } from '../interactor/client';
import { useInteractorStream, StreamEvent } from '../hooks/useInteractorStream';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  isStreaming?: boolean;
}

interface InteractorChatProps {
  client: InteractorClient;
  namespace: string;
  roomId: string;
}

export function InteractorChat({ client, namespace, roomId }: InteractorChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleStreamEvent = (event: StreamEvent) => {
    switch (event.type) {
      case 'message.delta':
        setMessages((prev) => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage?.isStreaming) {
            return [
              ...prev.slice(0, -1),
              { ...lastMessage, content: lastMessage.content + event.content },
            ];
          }
          return prev;
        });
        break;

      case 'message.complete':
        setMessages((prev) => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage?.isStreaming) {
            return [
              ...prev.slice(0, -1),
              { ...lastMessage, isStreaming: false },
            ];
          }
          return prev;
        });
        setIsLoading(false);
        break;

      case 'tool_call.start':
        console.log('Tool call started:', event.tool_call);
        break;

      case 'error':
        console.error('Stream error:', event.error);
        setIsLoading(false);
        break;
    }
  };

  const { isConnected, connect, disconnect, streamingContent } = useInteractorStream({
    onEvent: handleStreamEvent,
  });

  // Connect to SSE stream
  useEffect(() => {
    async function connectToStream() {
      const url = await client.getRoomStreamUrl(namespace, roomId);
      connect(url);
    }
    connectToStream();
    return () => disconnect();
  }, [client, namespace, roomId, connect, disconnect]);

  // Load existing messages
  useEffect(() => {
    async function loadMessages() {
      const response = await client.listMessages(namespace, roomId, {
        order: 'asc',
        per_page: 100,
      });
      setMessages(
        response.data.map((m) => ({
          id: m.id,
          role: m.role as 'user' | 'assistant',
          content: m.content,
        }))
      );
    }
    loadMessages();
  }, [client, namespace, roomId]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Add placeholder for streaming response
    const streamingMessage: Message = {
      id: `streaming-${Date.now()}`,
      role: 'assistant',
      content: '',
      isStreaming: true,
    };
    setMessages((prev) => [...prev, streamingMessage]);

    try {
      await client.sendMessage(namespace, roomId, input, true); // stream=true
    } catch (error) {
      console.error('Failed to send message:', error);
      setIsLoading(false);
      // Remove streaming placeholder on error
      setMessages((prev) => prev.filter((m) => !m.isStreaming));
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Connection status */}
      <div className={`text-sm px-4 py-1 ${isConnected ? 'bg-green-100' : 'bg-red-100'}`}>
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`p-3 rounded-lg ${
              message.role === 'user'
                ? 'bg-blue-100 ml-auto max-w-[80%]'
                : 'bg-gray-100 mr-auto max-w-[80%]'
            }`}
          >
            <div className="text-sm font-medium mb-1">
              {message.role === 'user' ? 'You' : 'Assistant'}
            </div>
            <div className="whitespace-pre-wrap">
              {message.content}
              {message.isStreaming && (
                <span className="animate-pulse">▊</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type a message..."
            disabled={isLoading}
            className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## Testing & Mocking

### TypeScript Mock Client

```typescript
// src/interactor/__mocks__/client.ts
import { InteractorClient, InteractorConfig } from '../client';

export class MockInteractorClient extends InteractorClient {
  private mockResponses: Map<string, any> = new Map();

  constructor() {
    // Bypass real initialization
    super({
      clientId: 'mock_client_id',
      clientSecret: 'mock_client_secret',
    } as InteractorConfig);
  }

  // Override token management
  async getAccessToken(): Promise<string> {
    return 'mock_access_token';
  }

  // Mock any method response
  mockResponse(method: string, response: any): void {
    this.mockResponses.set(method, response);
  }

  // Override methods for testing
  async createAssistant(namespace: string, data: any): Promise<any> {
    return this.mockResponses.get('createAssistant') || {
      id: 'asst_mock_123',
      name: data.name,
      model: data.model,
      system_prompt: data.system_prompt,
    };
  }

  async createRoom(namespace: string, assistantId: string, metadata?: any): Promise<any> {
    return this.mockResponses.get('createRoom') || {
      id: 'room_mock_456',
      assistant_id: assistantId,
      namespace,
      metadata,
    };
  }

  async sendMessage(namespace: string, roomId: string, content: string): Promise<any> {
    return this.mockResponses.get('sendMessage') || {
      id: 'msg_mock_789',
      room_id: roomId,
      role: 'assistant',
      content: 'Mock response to: ' + content,
    };
  }
}

// Usage in tests
// jest.mock('./interactor/client', () => ({
//   InteractorClient: MockInteractorClient,
// }));
```

### Jest Test Example

```typescript
// src/__tests__/interactor.test.ts
import { MockInteractorClient } from '../interactor/__mocks__/client';

describe('Interactor Integration', () => {
  let client: MockInteractorClient;

  beforeEach(() => {
    client = new MockInteractorClient();
  });

  it('should create an assistant', async () => {
    const assistant = await client.createAssistant('user_123', {
      name: 'Test Bot',
      model: 'gpt-4',
      system_prompt: 'You are helpful.',
    });

    expect(assistant.id).toBe('asst_mock_123');
    expect(assistant.name).toBe('Test Bot');
  });

  it('should handle custom mock responses', async () => {
    client.mockResponse('createAssistant', {
      id: 'asst_custom',
      name: 'Custom Bot',
    });

    const assistant = await client.createAssistant('user_123', {
      name: 'Any Name',
      model: 'gpt-4',
      system_prompt: 'Test',
    });

    expect(assistant.id).toBe('asst_custom');
  });
});
```

### Python Mock Client (pytest)

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_interactor_client():
    """Create a mock Interactor client for testing."""
    client = MagicMock()

    # Mock async methods
    client.create_assistant = AsyncMock(return_value={
        "id": "asst_mock_123",
        "name": "Test Bot",
        "model": "gpt-4",
    })

    client.create_room = AsyncMock(return_value={
        "id": "room_mock_456",
        "assistant_id": "asst_mock_123",
        "namespace": "user_123",
    })

    client.send_message = AsyncMock(return_value={
        "id": "msg_mock_789",
        "role": "assistant",
        "content": "Mock response",
    })

    return client


@pytest.fixture
def mock_sync_client():
    """Create a mock sync Interactor client for testing."""
    client = MagicMock()

    client.create_assistant.return_value = {
        "id": "asst_mock_123",
        "name": "Test Bot",
    }

    client.create_room.return_value = {
        "id": "room_mock_456",
    }

    return client
```

### Python Test Example

```python
# tests/test_interactor.py
import pytest

@pytest.mark.asyncio
async def test_create_assistant(mock_interactor_client):
    """Test assistant creation with mock client."""
    result = await mock_interactor_client.create_assistant(
        namespace="user_123",
        name="Test Bot",
        model="gpt-4",
        system_prompt="You are helpful.",
    )

    assert result["id"] == "asst_mock_123"
    mock_interactor_client.create_assistant.assert_called_once()


def test_sync_create_room(mock_sync_client):
    """Test room creation with sync mock client."""
    result = mock_sync_client.create_room(
        namespace="user_123",
        assistant_id="asst_123",
    )

    assert result["id"] == "room_mock_456"
```

### Integration Test with Real API (Sandbox)

```typescript
// src/__tests__/integration.test.ts
import { InteractorClient } from '../interactor/client';

// Only run in CI with sandbox credentials
const runIntegrationTests = process.env.INTERACTOR_SANDBOX_CLIENT_ID;

(runIntegrationTests ? describe : describe.skip)('Interactor Integration (Sandbox)', () => {
  let client: InteractorClient;
  const namespace = `test_${Date.now()}`;

  beforeAll(() => {
    client = new InteractorClient({
      clientId: process.env.INTERACTOR_SANDBOX_CLIENT_ID!,
      clientSecret: process.env.INTERACTOR_SANDBOX_CLIENT_SECRET!,
    });
  });

  it('should authenticate and get token', async () => {
    const token = await client.getAccessToken();
    expect(token).toBeDefined();
    expect(token.length).toBeGreaterThan(10);
  });

  it('should create and delete assistant', async () => {
    const assistant = await client.createAssistant(namespace, {
      name: 'Integration Test Bot',
      model: 'gpt-4',
      system_prompt: 'Test assistant',
    });

    expect(assistant.id).toMatch(/^asst_/);

    // Cleanup
    await client.deleteAssistant(namespace, assistant.id);
  });
});
```

---

## Best Practices

### Token Management
- Always cache tokens with expiration tracking
- Refresh tokens 60 seconds before expiry to avoid edge cases
- Clear cached tokens on authentication errors (401)
- Use thread-safe token refresh (mutex/lock in async contexts)
- Use singleton pattern to avoid multiple token refreshes

### Error Handling
- Implement specific error types for different scenarios
- Always log errors with context (namespace, resource ID, request ID)
- Provide meaningful error messages to end users
- Handle rate limits with exponential backoff and jitter
- Implement circuit breakers for repeated failures

### Retry Strategy

```typescript
// Recommended retry configuration
const retryConfig = {
  maxRetries: 3,
  baseDelayMs: 1000,
  maxDelayMs: 30000,
  retryOn: [429, 502, 503, 504],  // Rate limits and transient errors
};
```

### Namespace Isolation
- Always include namespace in requests (prefer X-Namespace header)
- Use consistent namespace format: `user_{id}` or `org_{id}_user_{id}`
- Never share data across namespaces
- Validate namespace ownership in your application before making API calls
- Document namespace strategy for your team

### Connection Pooling
- Use singleton pattern for client instances
- Reuse HTTP connections via session/client objects
- Configure appropriate timeouts (30s default)
- Monitor connection pool health in production

### Webhook Security
- Always verify webhook signatures using HMAC SHA-256
- Use timing-safe comparison for signatures
- Implement idempotency keys for webhook processing
- Log all webhook events for debugging
- Return 200 quickly, process asynchronously for long operations

### SSE Streaming
- Implement reconnection with exponential backoff
- Handle connection drops gracefully
- Clean up resources on component unmount
- Provide visual feedback for connection status
- Consider heartbeat/keepalive for long connections

### Production Checklist

```markdown
- [ ] Environment variables configured and validated at startup
- [ ] Token caching implemented with proper expiry handling
- [ ] Retry logic with exponential backoff
- [ ] Error types properly handled and logged
- [ ] Webhook signature verification enabled
- [ ] Rate limit handling implemented
- [ ] Namespace strategy documented
- [ ] Singleton client pattern used
- [ ] Health monitoring configured
- [ ] Integration tests against sandbox environment
```

---

## API Reference

### Base URLs

| Environment | Account Server | Core API |
|-------------|----------------|----------|
| Production | `https://auth.interactor.com/api/v1` | `https://core.interactor.com/api/v1` |
| Sandbox | `https://sandbox-auth.interactor.com/api/v1` | `https://sandbox-core.interactor.com/api/v1` |

### API Response Envelope

All API responses follow a consistent envelope structure:

```typescript
// Success Response
interface ApiResponse<T> {
  data: T;
  meta?: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
    has_more: boolean;
  };
}

// Error Response
interface ErrorResponse {
  error: {
    code: string;           // Machine-readable error code
    message: string;        // Human-readable message
    details?: {             // Validation errors (optional)
      field: string;
      message: string;
    }[];
    request_id: string;     // For support debugging
  };
}
```

**Example Success Response:**
```json
{
  "data": {
    "id": "asst_abc123",
    "name": "Support Bot",
    "model": "gpt-4"
  }
}
```

**Example Paginated Response:**
```json
{
  "data": [
    { "id": "asst_abc123", "name": "Bot 1" },
    { "id": "asst_def456", "name": "Bot 2" }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 45,
    "total_pages": 3,
    "has_more": true
  }
}
```

**Example Error Response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ],
    "request_id": "req_xyz789"
  }
}
```

### Endpoint Reference

> **OpenAPI Specification**: The complete machine-readable API spec is available at:
> - Production: `https://core.interactor.com/api/v1/openapi.yaml`
> - Documentation: `https://docs.interactor.com/api`

#### Authentication Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/oauth/token` | Get access token (client_credentials) |
| `POST` | `/oauth/revoke` | Revoke access token |
| `GET` | `/oauth/jwks` | Get JWKS public keys |

#### Credentials Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/credentials` | List credentials |
| `GET` | `/credentials/{id}` | Get credential by ID |
| `GET` | `/credentials/{id}/token` | Get credential access token |
| `DELETE` | `/credentials/{id}` | Delete credential |
| `POST` | `/credentials/{id}/refresh` | Force refresh credential |
| `POST` | `/oauth/initiate` | Initiate OAuth flow |
| `GET` | `/oauth/status/{flow_id}` | Get OAuth flow status |

#### Assistants Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/assistants` | Create assistant |
| `GET` | `/assistants` | List assistants |
| `GET` | `/assistants/{id}` | Get assistant by ID |
| `PATCH` | `/assistants/{id}` | Update assistant |
| `DELETE` | `/assistants/{id}` | Delete assistant |

#### Rooms Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/rooms` | Create room |
| `GET` | `/rooms` | List rooms |
| `GET` | `/rooms/{id}` | Get room by ID |
| `PATCH` | `/rooms/{id}` | Update room metadata |
| `DELETE` | `/rooms/{id}` | Delete room |
| `GET` | `/rooms/{id}/stream` | SSE stream (with token query param) |

#### Messages Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/rooms/{room_id}/messages` | Send message |
| `GET` | `/rooms/{room_id}/messages` | List messages |

#### Tools Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/tools` | Create tool |
| `GET` | `/tools` | List tools |
| `GET` | `/tools/{id}` | Get tool by ID |
| `PATCH` | `/tools/{id}` | Update tool |
| `DELETE` | `/tools/{id}` | Delete tool |
| `POST` | `/rooms/{room_id}/tool-results` | Submit tool result |

#### Data Sources Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/data-sources` | Create data source |
| `GET` | `/data-sources` | List data sources |
| `GET` | `/data-sources/{id}` | Get data source by ID |
| `PATCH` | `/data-sources/{id}` | Update data source |
| `DELETE` | `/data-sources/{id}` | Delete data source |
| `POST` | `/data-sources/{id}/sync` | Trigger sync |

#### Workflow Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/workflows` | Create workflow |
| `GET` | `/workflows` | List workflows |
| `GET` | `/workflows/{id}` | Get workflow by ID |
| `DELETE` | `/workflows/{id}` | Delete workflow |

#### Workflow Instance Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/workflow-instances` | Start workflow instance |
| `GET` | `/workflow-instances` | List instances |
| `GET` | `/workflow-instances/{id}` | Get instance by ID |
| `POST` | `/workflow-instances/{id}/input` | Submit input to halted instance |
| `POST` | `/workflow-instances/{id}/events` | Trigger event |
| `POST` | `/workflow-instances/{id}/cancel` | Cancel instance |
| `GET` | `/workflow-instances/{id}/thread` | Get instance thread |
| `POST` | `/workflow-instances/{id}/thread/messages` | Send thread message |
| `GET` | `/workflow-instances/{id}/stream` | SSE stream |

#### Webhook Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/webhooks` | Create webhook |
| `GET` | `/webhooks` | List webhooks |
| `GET` | `/webhooks/{id}` | Get webhook by ID |
| `PATCH` | `/webhooks/{id}` | Update webhook |
| `DELETE` | `/webhooks/{id}` | Delete webhook |
| `POST` | `/webhooks/{id}/rotate-secret` | Rotate webhook secret |

---

## Webhook Event Catalog

### Event Types and Schemas

| Event | Description | Trigger |
|-------|-------------|---------|
| `credential.connected` | OAuth credential successfully connected | OAuth flow completion |
| `credential.refreshed` | Credential token refreshed | Auto or manual refresh |
| `credential.expired` | Credential expired and needs reconnection | Token expiry without refresh |
| `credential.revoked` | Credential was revoked | User or provider revocation |
| `credential.error` | Credential error occurred | Refresh failure, API error |
| `room.message.created` | New message in room | User or assistant message |
| `room.message.updated` | Message was updated | Edit or completion |
| `room.tool_call.pending` | Tool call awaiting result | Assistant requests tool |
| `room.tool_call.completed` | Tool call completed | Result submitted |
| `workflow.instance.started` | Workflow instance started | Instance creation |
| `workflow.instance.state_changed` | Workflow state transition | State machine advancement |
| `workflow.instance.halted` | Workflow waiting for input | Requires user interaction |
| `workflow.instance.completed` | Workflow finished | Terminal state reached |
| `workflow.instance.failed` | Workflow error | Unhandled exception |
| `workflow.instance.cancelled` | Workflow cancelled | Manual cancellation |

### Event Payload Schema

```typescript
interface WebhookEvent {
  id: string;                    // Unique event ID (evt_xxx)
  event: string;                 // Event type
  timestamp: string;             // ISO 8601 timestamp
  idempotency_key: string;       // For deduplication
  namespace: string;             // Affected namespace
  data: Record<string, any>;     // Event-specific payload
}
```

### Example Event Payloads

**credential.connected:**
```json
{
  "id": "evt_abc123",
  "event": "credential.connected",
  "timestamp": "2024-01-15T10:30:00Z",
  "idempotency_key": "idem_xyz789",
  "namespace": "user_123",
  "data": {
    "credential_id": "cred_def456",
    "provider": "google",
    "service_id": "svc_google_calendar",
    "scopes": ["calendar.read", "calendar.write"],
    "metadata": {}
  }
}
```

**room.message.created:**
```json
{
  "id": "evt_def456",
  "event": "room.message.created",
  "timestamp": "2024-01-15T10:31:00Z",
  "idempotency_key": "idem_abc123",
  "namespace": "user_123",
  "data": {
    "message_id": "msg_ghi789",
    "room_id": "room_abc123",
    "role": "assistant",
    "content": "Hello! How can I help you?",
    "tool_calls": null
  }
}
```

**room.tool_call.pending:**
```json
{
  "id": "evt_ghi789",
  "event": "room.tool_call.pending",
  "timestamp": "2024-01-15T10:32:00Z",
  "idempotency_key": "idem_def456",
  "namespace": "user_123",
  "data": {
    "tool_call_id": "tc_jkl012",
    "room_id": "room_abc123",
    "tool_id": "tool_mno345",
    "tool_name": "get_calendar_events",
    "arguments": {
      "start_date": "2024-01-15",
      "end_date": "2024-01-22"
    }
  }
}
```

**workflow.instance.halted:**
```json
{
  "id": "evt_jkl012",
  "event": "workflow.instance.halted",
  "timestamp": "2024-01-15T10:33:00Z",
  "idempotency_key": "idem_ghi789",
  "namespace": "user_123",
  "data": {
    "instance_id": "wfi_mno345",
    "workflow_id": "wf_pqr678",
    "current_state": "awaiting_approval",
    "context": {
      "order_id": "ord_123",
      "total": 599.99
    },
    "presentation": {
      "type": "form",
      "title": "Approval Required",
      "description": "Please approve this order",
      "fields": [
        {
          "name": "approved",
          "type": "boolean",
          "label": "Approve Order?",
          "required": true
        },
        {
          "name": "notes",
          "type": "text",
          "label": "Notes (optional)",
          "required": false
        }
      ]
    }
  }
}
```

### Webhook Delivery Semantics

**Delivery Guarantees:**
- **At-least-once delivery**: Events may be delivered more than once
- **Ordering**: Not guaranteed; use timestamps for ordering
- **Timeout**: Your endpoint must respond within 30 seconds
- **Expected response**: HTTP 2xx status code

**Retry Policy:**

| Attempt | Delay | Total Time |
|---------|-------|------------|
| 1 | Immediate | 0s |
| 2 | 30 seconds | 30s |
| 3 | 2 minutes | 2m 30s |
| 4 | 10 minutes | 12m 30s |
| 5 | 30 minutes | 42m 30s |
| 6 (final) | 2 hours | 2h 42m 30s |

**Headers Sent:**
```
X-Interactor-Signature: sha256=<hex_signature>
X-Interactor-Timestamp: <unix_timestamp>
X-Interactor-Event: <event_type>
X-Request-Id: <request_id>
Content-Type: application/json
```

### Idempotency Processing

Always use the `idempotency_key` to prevent duplicate processing:

```typescript
// TypeScript idempotent handler
const processedEvents = new Set<string>(); // Use Redis in production

async function handleWebhook(event: WebhookEvent): Promise<void> {
  // Check if already processed
  if (processedEvents.has(event.idempotency_key)) {
    console.log(`Event ${event.idempotency_key} already processed, skipping`);
    return;
  }

  try {
    // Process the event
    await processEvent(event);

    // Mark as processed (with TTL in production)
    processedEvents.add(event.idempotency_key);
  } catch (error) {
    // Don't mark as processed on error - allow retry
    throw error;
  }
}
```

```python
# Python with Redis
import redis
from typing import Callable

redis_client = redis.Redis()
IDEMPOTENCY_TTL = 86400 * 7  # 7 days

def idempotent_handler(handler: Callable):
    """Decorator for idempotent webhook handling."""
    def wrapper(event: dict):
        key = f"webhook:processed:{event['idempotency_key']}"

        # Check if already processed
        if redis_client.exists(key):
            return {"status": "already_processed"}

        # Process event
        result = handler(event)

        # Mark as processed with TTL
        redis_client.setex(key, IDEMPOTENCY_TTL, "1")

        return result
    return wrapper

@idempotent_handler
def handle_credential_connected(event: dict):
    # Process credential connection
    pass
```

---

## Authentication Scopes & RBAC

### OAuth Scopes

| Scope | Description | Endpoints Granted |
|-------|-------------|-------------------|
| `credentials:read` | Read credential metadata | `GET /credentials`, `GET /credentials/{id}` |
| `credentials:write` | Create/delete credentials | `POST /oauth/initiate`, `DELETE /credentials/{id}` |
| `credentials:token` | Access credential tokens | `GET /credentials/{id}/token` |
| `assistants:read` | Read assistants | `GET /assistants`, `GET /assistants/{id}` |
| `assistants:write` | Manage assistants | `POST/PATCH/DELETE /assistants` |
| `rooms:read` | Read rooms and messages | `GET /rooms`, `GET /rooms/{id}/messages` |
| `rooms:write` | Send messages, manage rooms | `POST /rooms`, `POST /rooms/{id}/messages` |
| `tools:read` | Read tools | `GET /tools` |
| `tools:write` | Manage tools | `POST/PATCH/DELETE /tools` |
| `workflows:read` | Read workflows and instances | `GET /workflows`, `GET /workflow-instances` |
| `workflows:write` | Manage workflows | `POST/DELETE /workflows` |
| `workflows:execute` | Start/control instances | `POST /workflow-instances`, `POST .../input` |
| `webhooks:read` | Read webhooks | `GET /webhooks` |
| `webhooks:write` | Manage webhooks | `POST/PATCH/DELETE /webhooks` |
| `admin` | Full access to namespace | All endpoints |

### Requesting Specific Scopes

```typescript
// Request limited scopes for least-privilege
const response = await axios.post(`${accountServerUrl}/oauth/token`, {
  grant_type: 'client_credentials',
  client_id: process.env.INTERACTOR_CLIENT_ID,
  client_secret: process.env.INTERACTOR_CLIENT_SECRET,
  scope: 'credentials:read credentials:token assistants:read rooms:read rooms:write',
});
```

### Role-Based Access Patterns

**Pattern 1: Background Worker (minimal access)**
```bash
# .env for background job processor
INTERACTOR_SCOPES=credentials:token workflows:execute
```

**Pattern 2: User-Facing API Server**
```bash
# .env for API server
INTERACTOR_SCOPES=credentials:read assistants:read rooms:read rooms:write
```

**Pattern 3: Admin Dashboard**
```bash
# .env for admin service
INTERACTOR_SCOPES=admin
```

### Namespace-Level Permissions

- Each namespace is isolated; tokens only access their granted namespaces
- Cross-namespace access requires explicit multi-namespace token grants
- Validate namespace ownership in your application before API calls

```typescript
// Validate user owns namespace before API call
async function validateNamespaceAccess(userId: string, namespace: string): Promise<boolean> {
  // Your application's namespace ownership check
  const expectedNamespace = `user_${userId}`;
  return namespace === expectedNamespace;
}

// Usage
app.get('/api/credentials', async (req, res) => {
  const namespace = `user_${req.user.id}`;

  // This prevents users from accessing other namespaces
  const credentials = await client.listCredentials(namespace);
  res.json(credentials);
});
```

---

## Security & Compliance

### Data Security

**Encryption:**
- All API traffic uses TLS 1.2+ (TLS 1.3 recommended)
- OAuth tokens encrypted at rest using AES-256-GCM
- Credential secrets stored using envelope encryption with KMS
- Database encryption at rest enabled

**Data Residency:**
- Production data stored in specified region (default: US)
- Contact support for EU or other region requirements

### Secrets Management

**Environment Variables (Required):**
```bash
# Never commit these to version control
INTERACTOR_CLIENT_ID=client_xxx      # OAuth client ID
INTERACTOR_CLIENT_SECRET=secret_xxx  # OAuth client secret (rotate quarterly)
INTERACTOR_WEBHOOK_SECRET=whsec_xxx  # Webhook verification secret
```

**Storage Recommendations:**
- Use secrets manager (AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager)
- Never log secrets or include in error messages
- Rotate secrets quarterly or after any suspected compromise

### Secret Rotation

**Rotate Client Secret:**
```bash
# 1. Generate new secret in Interactor dashboard
# 2. Update your secrets manager with new value
# 3. Deploy application with new secret
# 4. Verify authentication works
# 5. Revoke old secret in dashboard
```

**Rotate Webhook Secret:**
```typescript
// API supports webhook secret rotation
const result = await client.rotateWebhookSecret(namespace, webhookId);
const newSecret = result.secret; // Store securely, update verification code
```

### Compliance

**Standards:**
- SOC 2 Type II certified
- GDPR compliant (EU data processing agreements available)
- CCPA compliant

**Audit Logging:**
- All API requests logged with request_id
- Webhook deliveries logged with retry attempts
- Access logs retained for 90 days

**Data Retention:**
- Credential metadata: Until deletion
- Conversation history: Configurable per assistant (default: 90 days)
- Workflow instances: 30 days after completion
- Audit logs: 90 days

### Security Checklist

```markdown
- [ ] TLS 1.2+ enforced for all connections
- [ ] Client secrets stored in secrets manager
- [ ] Webhook signature verification enabled
- [ ] Scopes limited to minimum required
- [ ] Namespace validation in application layer
- [ ] Secrets rotation schedule established
- [ ] Error messages don't expose internal details
- [ ] Rate limiting configured
- [ ] Monitoring for authentication failures
```

---

## API Versioning & Deprecation

### Current Version

- **API Version**: v1
- **SDK Version**: 2.0.0
- **Base Path**: `/api/v1`

### Versioning Strategy

- API versions are indicated in the URL path (`/api/v1`, `/api/v2`)
- Minor/patch updates within a version are backward-compatible
- Breaking changes require a new major version

### Deprecation Policy

| Timeline | Action |
|----------|--------|
| Announcement | New version released, deprecation notice published |
| +6 months | Deprecation warnings in API responses |
| +12 months | Old version enters maintenance mode (security fixes only) |
| +18 months | Old version sunset (returns 410 Gone) |

### Deprecation Headers

When using deprecated endpoints or parameters:

```
Deprecation: true
Sunset: Sat, 01 Jul 2025 00:00:00 GMT
Link: <https://docs.interactor.com/migration/v1-to-v2>; rel="deprecation"
```

### Migration Guide

Check the documentation for migration guides between versions:
- `https://docs.interactor.com/migration/v1-to-v2`

### Changelog

See the full changelog at: `https://docs.interactor.com/changelog`

**Recent Changes (v2.0.0):**
- Added workflow thread messaging endpoints
- Added data source sync endpoint
- Standardized error response format
- Added idempotency_key to all webhook events

---

## Rate Limiting

### Rate Limit Tiers

| Tier | Requests/minute | Burst | Applied To |
|------|-----------------|-------|------------|
| Standard | 600 | 100 | Per client_id |
| Per-Namespace | 300 | 50 | Per namespace |
| Streaming | 60 | 10 | SSE connections |
| OAuth | 20 | 5 | Token requests |

### Rate Limit Headers

All responses include rate limit information:

```
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 542
X-RateLimit-Reset: 1705312800
X-RateLimit-Scope: client
```

### Handling Rate Limits

```typescript
// Enhanced retry with rate limit awareness
async function requestWithRateLimit<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error instanceof InteractorError && error.status === 429) {
        // Parse Retry-After header
        const retryAfter = error.headers?.['retry-after'];
        const waitMs = retryAfter
          ? parseInt(retryAfter, 10) * 1000
          : Math.pow(2, attempt) * 1000;

        console.log(`Rate limited, waiting ${waitMs}ms before retry`);
        await sleep(waitMs);
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

```python
# Python rate limit handler
import time
from typing import TypeVar, Callable

T = TypeVar('T')

def with_rate_limit_retry(fn: Callable[[], T], max_retries: int = 3) -> T:
    """Execute function with rate limit retry handling."""
    for attempt in range(max_retries):
        try:
            return fn()
        except InteractorError as e:
            if e.status == 429:
                # Get retry delay from header or calculate
                retry_after = e.headers.get('Retry-After', str(2 ** attempt))
                wait_seconds = int(retry_after)

                print(f"Rate limited, waiting {wait_seconds}s before retry")
                time.sleep(wait_seconds)
                continue
            raise
    raise Exception("Max retries exceeded")
```

### Best Practices

- Implement exponential backoff with jitter
- Monitor `X-RateLimit-Remaining` and preemptively slow down
- Use webhooks instead of polling for real-time updates
- Batch operations where possible
- Cache responses that don't change frequently

---

## Observability & Monitoring

### Recommended Metrics

```typescript
// Prometheus-style metrics to emit
const metrics = {
  // Request metrics
  'interactor_requests_total': {
    type: 'counter',
    labels: ['endpoint', 'method', 'status', 'namespace'],
    description: 'Total API requests',
  },
  'interactor_request_duration_ms': {
    type: 'histogram',
    labels: ['endpoint', 'method'],
    buckets: [10, 50, 100, 250, 500, 1000, 2500, 5000],
    description: 'Request latency in milliseconds',
  },

  // Token metrics
  'interactor_token_refresh_total': {
    type: 'counter',
    labels: ['status'], // success, failure
    description: 'Token refresh attempts',
  },
  'interactor_token_expiry_seconds': {
    type: 'gauge',
    description: 'Seconds until current token expires',
  },

  // Webhook metrics
  'interactor_webhook_received_total': {
    type: 'counter',
    labels: ['event', 'status'], // status: processed, duplicate, failed
    description: 'Webhooks received',
  },
  'interactor_webhook_processing_duration_ms': {
    type: 'histogram',
    labels: ['event'],
    description: 'Webhook processing time',
  },

  // Streaming metrics
  'interactor_sse_connections_active': {
    type: 'gauge',
    labels: ['type'], // room, workflow
    description: 'Active SSE connections',
  },
  'interactor_sse_disconnects_total': {
    type: 'counter',
    labels: ['type', 'reason'], // timeout, error, client_close
    description: 'SSE disconnection events',
  },

  // Error metrics
  'interactor_errors_total': {
    type: 'counter',
    labels: ['type', 'code'], // type: auth, rate_limit, validation, server
    description: 'API errors by type',
  },
};
```

### Recommended Log Fields

```typescript
interface InteractorLogContext {
  // Always include
  request_id: string;       // From X-Request-Id header
  namespace: string;        // Current namespace
  endpoint: string;         // API endpoint called
  method: string;           // HTTP method
  status_code: number;      // Response status
  duration_ms: number;      // Request duration

  // Include when relevant
  user_id?: string;         // Your application's user ID
  resource_id?: string;     // ID of resource being accessed
  error_code?: string;      // Interactor error code
  retry_count?: number;     // Retry attempt number
}

// Example structured log
logger.info('Interactor API call', {
  request_id: 'req_xyz789',
  namespace: 'user_123',
  endpoint: '/assistants',
  method: 'POST',
  status_code: 201,
  duration_ms: 145,
  resource_id: 'asst_abc123',
});
```

### Health Check Endpoint

```typescript
// Implement a health check that validates Interactor connectivity
app.get('/health/interactor', async (req, res) => {
  const startTime = Date.now();

  try {
    // Validate we can get a token
    await client.getAccessToken();

    const latency = Date.now() - startTime;

    res.json({
      status: 'healthy',
      latency_ms: latency,
      token_valid: client.isAuthenticated(),
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message,
    });
  }
});
```

### Alerting Recommendations

| Metric | Threshold | Severity |
|--------|-----------|----------|
| Error rate | > 5% over 5 min | Warning |
| Error rate | > 10% over 5 min | Critical |
| P99 latency | > 5000ms | Warning |
| Token refresh failures | > 3 consecutive | Critical |
| Webhook processing failures | > 10% | Warning |
| SSE disconnects | > 10/min | Warning |
| Rate limit hits | > 50% of limit | Warning |

---

## Pagination Patterns

### Page-Based Pagination

All list endpoints support page-based pagination:

```typescript
// Basic pagination
const response = await client.listAssistants(namespace, { page: 1, per_page: 20 });

console.log(response.data);      // Array of items
console.log(response.meta.page); // Current page (1)
console.log(response.meta.total); // Total items (45)
console.log(response.meta.has_more); // true
```

### Iterate Through All Pages

```typescript
// TypeScript: Generator for iterating all items
async function* iterateAll<T>(
  fetchPage: (page: number) => Promise<PaginatedResponse<T>>,
  perPage: number = 100
): AsyncGenerator<T> {
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const response = await fetchPage(page);

    for (const item of response.data) {
      yield item;
    }

    hasMore = response.meta.has_more;
    page++;
  }
}

// Usage
const allAssistants: Assistant[] = [];
for await (const assistant of iterateAll(
  (page) => client.listAssistants(namespace, { page, per_page: 100 })
)) {
  allAssistants.push(assistant);
}
```

```python
# Python: Generator for all pages
from typing import AsyncGenerator, TypeVar, Callable, Any

T = TypeVar('T')

async def iterate_all_pages(
    fetch_page: Callable[[int], Any],
    per_page: int = 100
) -> AsyncGenerator[T, None]:
    """Iterate through all pages of a paginated endpoint."""
    page = 1
    has_more = True

    while has_more:
        response = await fetch_page(page)

        for item in response.data:
            yield item

        has_more = response.meta.has_more
        page += 1

# Usage
async def get_all_assistants(client, namespace: str) -> list:
    assistants = []
    async for assistant in iterate_all_pages(
        lambda page: client.list_assistants(namespace, page=page, per_page=100)
    ):
        assistants.append(assistant)
    return assistants
```

### Pagination Best Practices

- Use `per_page=100` for bulk operations (maximum allowed)
- Use `per_page=20` for UI pagination
- Cache page results when data doesn't change frequently
- Implement infinite scroll with `has_more` flag
- Handle items being added/removed between page fetches

---

## Idempotency

### Idempotency for Write Operations

Critical write operations support idempotency keys to prevent duplicate processing:

```typescript
// TypeScript: Idempotent request
async function createAssistantIdempotent(
  client: InteractorClient,
  namespace: string,
  data: CreateAssistantData,
  idempotencyKey: string
): Promise<Assistant> {
  // Include idempotency key in headers
  const response = await axios.post(
    `${client.config.coreApiUrl}/assistants`,
    data,
    {
      headers: {
        'Authorization': `Bearer ${await client.getAccessToken()}`,
        'X-Namespace': namespace,
        'Idempotency-Key': idempotencyKey,
      },
    }
  );
  return response.data.data;
}

// Usage with UUID
import { v4 as uuidv4 } from 'uuid';

const idempotencyKey = uuidv4(); // or derive from request content
const assistant = await createAssistantIdempotent(
  client,
  namespace,
  { name: 'My Bot', model: 'gpt-4' },
  idempotencyKey
);
```

### Idempotency Key Guidelines

| Endpoint | Recommended Key Strategy |
|----------|-------------------------|
| Create Assistant | UUID or hash of (namespace + name + model) |
| Create Room | UUID or hash of (namespace + assistant_id + user_session) |
| Send Message | UUID or hash of (room_id + content + timestamp) |
| Start Workflow | UUID or hash of (workflow_id + input_data) |
| Create Webhook | UUID or hash of (namespace + url + events) |

### Server Behavior

- Keys are scoped to client_id + namespace
- Keys are valid for 24 hours
- Duplicate requests return the original response
- Different request body with same key returns 409 Conflict

---

## Secrets Lifecycle Management

### Credential Token Refresh

```typescript
// Force refresh a credential token
async function refreshCredentialToken(
  client: InteractorClient,
  namespace: string,
  credentialId: string
): Promise<void> {
  try {
    await client.refreshCredential(namespace, credentialId);
    console.log(`Credential ${credentialId} refreshed successfully`);
  } catch (error) {
    if (error instanceof InteractorError && error.code === 'REFRESH_FAILED') {
      // Token cannot be refreshed - notify user to reconnect
      await notifyUserToReconnect(namespace, credentialId);
    }
    throw error;
  }
}
```

### Handling Expired Credentials

```typescript
// Webhook handler for credential expiry
async function handleCredentialExpired(data: CredentialExpiredEvent): Promise<void> {
  const { credential_id, namespace, provider } = data;

  // 1. Mark credential as expired in your database
  await db.credentials.update({
    where: { externalId: credential_id },
    data: { status: 'expired' },
  });

  // 2. Notify user
  await sendNotification({
    userId: extractUserFromNamespace(namespace),
    type: 'credential_expired',
    title: `Your ${provider} connection expired`,
    message: 'Please reconnect to continue using this service.',
    action: {
      label: 'Reconnect',
      url: `/settings/connections/${credential_id}/reconnect`,
    },
  });

  // 3. Pause dependent workflows
  await pauseWorkflowsUsingCredential(credential_id);
}
```

### Credential Revocation

```typescript
// Properly revoke a credential
async function revokeCredential(
  client: InteractorClient,
  namespace: string,
  credentialId: string
): Promise<void> {
  // 1. Delete from Interactor (revokes OAuth token with provider)
  await client.deleteCredential(namespace, credentialId);

  // 2. Clean up local references
  await db.credentials.delete({
    where: { externalId: credentialId },
  });

  // 3. Clean up dependent resources
  await cleanupDependentResources(credentialId);

  console.log(`Credential ${credentialId} fully revoked`);
}
```

### Webhook Secret Rotation

```typescript
// Rotate webhook secret with zero downtime
async function rotateWebhookSecret(
  client: InteractorClient,
  namespace: string,
  webhookId: string
): Promise<void> {
  // 1. Get current secret (for grace period)
  const oldSecret = process.env.INTERACTOR_WEBHOOK_SECRET;

  // 2. Rotate secret via API
  const result = await client.rotateWebhookSecret(namespace, webhookId);
  const newSecret = result.secret;

  // 3. Update secrets manager (both secrets valid during transition)
  await secretsManager.put('INTERACTOR_WEBHOOK_SECRET', newSecret);
  await secretsManager.put('INTERACTOR_WEBHOOK_SECRET_OLD', oldSecret);

  // 4. Deploy application with dual-secret verification
  // (verify with new secret first, fall back to old)

  // 5. After deployment confirmed, remove old secret
  setTimeout(async () => {
    await secretsManager.delete('INTERACTOR_WEBHOOK_SECRET_OLD');
  }, 3600000); // 1 hour grace period
}

// Dual-secret verification during rotation
function verifySignatureDuringRotation(
  payload: Buffer,
  signature: string
): boolean {
  const secrets = [
    process.env.INTERACTOR_WEBHOOK_SECRET,
    process.env.INTERACTOR_WEBHOOK_SECRET_OLD,
  ].filter(Boolean);

  for (const secret of secrets) {
    if (verifySignature(payload, signature, secret)) {
      return true;
    }
  }
  return false;
}
```

---

## Quickstart & Onboarding

### Sandbox Environment

For testing and development, use the sandbox environment:

```bash
# Sandbox credentials (request from dashboard or support)
INTERACTOR_ACCOUNT_SERVER_URL=https://sandbox-auth.interactor.com/api/v1
INTERACTOR_CORE_API_URL=https://sandbox-core.interactor.com/api/v1
INTERACTOR_CLIENT_ID=sandbox_client_xxx
INTERACTOR_CLIENT_SECRET=sandbox_secret_xxx
```

### Quickstart Checklist

```markdown
## Getting Started (30 minutes)

### 1. Get Credentials (5 min)
- [ ] Create account at https://dashboard.interactor.com
- [ ] Create a new application
- [ ] Copy client_id and client_secret

### 2. Setup Environment (5 min)
- [ ] Install SDK: `npm install @interactor/sdk` or `pip install interactor`
- [ ] Set environment variables
- [ ] Validate environment: run `validateInteractorEnv()`

### 3. Test Authentication (5 min)
- [ ] Get access token
- [ ] Verify token works with simple API call

### 4. Create First Assistant (10 min)
- [ ] Create assistant with system prompt
- [ ] Create room
- [ ] Send test message
- [ ] Verify response

### 5. Setup Webhook (5 min)
- [ ] Expose endpoint (use ngrok for local dev)
- [ ] Register webhook
- [ ] Verify signature verification works
- [ ] Test with credential.connected event
```

### Support & Resources

| Resource | URL |
|----------|-----|
| Documentation | https://docs.interactor.com |
| API Reference | https://docs.interactor.com/api |
| Status Page | https://status.interactor.com |
| Support Email | support@interactor.com |
| GitHub Issues | https://github.com/interactor/sdk/issues |
| Community Discord | https://discord.gg/interactor |

---

## Related Skills

- **interactor-auth**: Setup and authentication prerequisites
- **interactor-credentials**: OAuth credential management
- **interactor-agents**: AI assistants, rooms, and messages
- **interactor-workflows**: State machine automation
- **interactor-webhooks**: Webhook and SSE event handling

---

## Output Format

When using this skill, provide implementation code that:
1. Uses the appropriate SDK class for your language
2. Includes proper error handling
3. Follows namespace isolation patterns
4. Implements secure webhook verification
5. Handles SSE streaming with reconnection logic
