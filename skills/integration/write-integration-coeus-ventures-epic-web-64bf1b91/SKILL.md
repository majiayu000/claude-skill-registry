---
name: write-integration
description: Write external integrations following the Epic architecture patterns. Use when creating services for third-party APIs, email, payments, or complex business logic. Triggers on "create an integration", "add a service", or "integrate with".
---

# Write Integration

## Overview

This skill creates external integrations that follow the Epic three-layer architecture. Integrations belong to the **Infrastructure layer** and handle external API calls, complex business logic, and reusable services.

## Architecture Context

```
Backend: Actions call integrations
            |
            v
Infrastructure: Integrations (external APIs, complex logic)
                     |
                     v
              External Services (Stripe, GitHub, OpenAI, etc.)
```

Integrations:
- Run on the server (Infrastructure layer)
- Handle external API integrations
- Implement complex reusable business logic
- May only be called by Backend layer (Actions, Routes)
- NEVER imported by Frontend
- NEVER call other routes or actions

## Integration Location

```
shared/integrations/
  integration-name/
    integration-name.ts       # Main integration
    types.ts                  # TypeScript types
    index.ts                  # Public exports
```

## Class Specification Format

Follow the Epic Class specification format from `docs/Epic.md`:

```markdown
# ServiceName

[Description of what external system this integrates with]

## Properties
- config: ServiceConfig
- client: ExternalClient

## Methods
- methodName(params): Promise<Result>

## Relationships
- Composes: ExternalSDK
```

## Implementation Pattern

```typescript
import 'server-only';

interface ServiceConfig {
  apiKey: string;
  baseUrl?: string;
}

interface MethodResult<T> {
  success: boolean;
  data?: T;
  error?: string;
}

const defaultConfig: Partial<ServiceConfig> = {
  baseUrl: 'https://api.example.com',
};

export class ServiceName {
  private config: ServiceConfig;

  constructor(config?: Partial<ServiceConfig>) {
    this.config = {
      ...defaultConfig,
      apiKey: config?.apiKey || process.env.SERVICE_API_KEY!,
      ...config,
    };

    if (!this.config.apiKey) {
      throw new Error('ServiceName: API key is required');
    }
  }

  async methodName(params: MethodParams): Promise<MethodResult<ReturnType>> {
    try {
      const response = await fetch(`${this.config.baseUrl}/endpoint`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      });

      if (!response.ok) {
        const error = await response.text();
        return { success: false, error };
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('ServiceName.methodName error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }
}

// Export singleton instance
export const serviceName = new ServiceName();
```

## Integration Categories

### 1. Communication Services
```typescript
// Email (Resend, SendGrid)
export class EmailService {
  async send(to: string, subject: string, html: string): Promise<Result> {
    // Implementation
  }
}

// SMS (Twilio)
export class SMSService {
  async send(to: string, message: string): Promise<Result> {
    // Implementation
  }
}
```

### 2. Payment Services
```typescript
// Stripe
export class StripeService {
  async createCheckoutSession(params: CheckoutParams): Promise<Result<Session>> {
    // Implementation
  }

  async handleWebhook(payload: string, signature: string): Promise<Event> {
    // Implementation
  }
}
```

### 3. AI/ML Services
```typescript
// OpenAI, Anthropic
export class AIService {
  async complete(prompt: string, options?: Options): Promise<Result<string>> {
    // Implementation
  }

  async embed(text: string): Promise<Result<number[]>> {
    // Implementation
  }
}
```

### 4. Storage Services
```typescript
// S3, Cloudinary
export class StorageService {
  async upload(file: Buffer, path: string): Promise<Result<string>> {
    // Implementation
  }

  async delete(path: string): Promise<Result<boolean>> {
    // Implementation
  }
}
```

### 5. External APIs
```typescript
// GitHub, Vercel, etc.
export class GitHubService {
  async createRepository(name: string): Promise<Result<Repository>> {
    // Implementation
  }

  async createIssue(repo: string, title: string): Promise<Result<Issue>> {
    // Implementation
  }
}
```

## Error Handling Pattern

```typescript
async methodName(params: Params): Promise<Result<T>> {
  try {
    // Validate configuration
    if (!this.config.apiKey) {
      return { success: false, error: 'API key not configured' };
    }

    // Make request with retry logic
    const response = await this.withRetry(() =>
      fetch(url, options)
    );

    // Handle rate limiting
    if (response.status === 429) {
      return { success: false, error: 'Rate limit exceeded' };
    }

    // Handle errors
    if (!response.ok) {
      const error = await response.json();
      return { success: false, error: error.message };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('Service error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

private async withRetry<T>(
  fn: () => Promise<T>,
  retries = 3
): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
  throw new Error('Max retries exceeded');
}
```

## Constraints

- MUST include `import 'server-only'` at top
- NEVER import React, Jotai, or frontend code
- NEVER call other routes or actions
- ALWAYS use environment variables for secrets
- ALWAYS return consistent `{ success, data?, error? }` format
- ALWAYS implement proper error handling
- ALWAYS log errors for debugging

## Checklist

Before finalizing an integration:
- [ ] `server-only` import present
- [ ] Environment variables documented
- [ ] Error handling with try/catch
- [ ] Consistent return format
- [ ] Retry logic for transient failures
- [ ] Rate limiting handling
- [ ] Logging for debugging
- [ ] TypeScript types exported

## Example Specification

```markdown
# StripeService

Handles Stripe payment processing and subscription management.

## Properties
- stripe: Stripe - SDK client instance

## Methods
- createCheckoutSession(params: CheckoutParams): Promise<Result<Session>>
- createCustomer(email: string): Promise<Result<Customer>>
- handleWebhook(payload: string, signature: string): Promise<Event>

## Relationships
- Composes: Stripe SDK
```
