---
name: mistral-security-basics
description: |
  Apply Mistral AI security best practices for secrets and access control.
  Use when securing API keys, implementing least privilege access,
  or auditing Mistral AI security configuration.
  Trigger with phrases like "mistral security", "mistral secrets",
  "secure mistral", "mistral API key security".
allowed-tools: Read, Write, Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Mistral AI Security Basics

## Overview
Security best practices for Mistral AI API keys and access control.

## Prerequisites
- Mistral AI SDK installed
- Understanding of environment variables
- Access to Mistral AI console

## Instructions

### Step 1: Configure Environment Variables

```bash
# .env (NEVER commit to git)
MISTRAL_API_KEY=your-api-key-here

# .gitignore - Add these lines
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
```

**Validate .gitignore:**
```bash
# Check if .env would be committed
git check-ignore .env || echo "WARNING: .env is not ignored!"

# Check for exposed secrets in history
git log -p --all -S 'MISTRAL_API_KEY' -- '*.ts' '*.js' '*.py' '*.env'
```

### Step 2: Secure Key Loading

```typescript
// src/config/mistral.ts
import { z } from 'zod';

const envSchema = z.object({
  MISTRAL_API_KEY: z.string().min(20, 'Invalid API key format'),
  NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),
});

export function loadMistralConfig() {
  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    console.error('Environment validation failed:', result.error.format());
    throw new Error('Missing or invalid MISTRAL_API_KEY');
  }

  return result.data;
}

// Usage
const config = loadMistralConfig();
const client = new Mistral({ apiKey: config.MISTRAL_API_KEY });
```

### Step 3: Key Rotation Procedure

```bash
# 1. Generate new key in Mistral console
#    https://console.mistral.ai/api-keys/

# 2. Test new key before rotation
MISTRAL_API_KEY_NEW="new-key-here"
curl -H "Authorization: Bearer ${MISTRAL_API_KEY_NEW}" \
  https://api.mistral.ai/v1/models

# 3. Update environment variable / secrets manager
export MISTRAL_API_KEY="${MISTRAL_API_KEY_NEW}"

# 4. Deploy with new key

# 5. Revoke old key in Mistral console
```

### Step 4: Environment-Specific Keys

| Environment | Key Type | Permissions |
|-------------|----------|-------------|
| Development | Dev key | All models, low limits |
| Staging | Staging key | All models, medium limits |
| Production | Production key | Required models only |

```typescript
// src/config/environments.ts
interface MistralEnvConfig {
  apiKey: string;
  allowedModels: string[];
  maxTokensPerRequest: number;
}

const configs: Record<string, MistralEnvConfig> = {
  development: {
    apiKey: process.env.MISTRAL_API_KEY_DEV!,
    allowedModels: ['mistral-small-latest', 'mistral-large-latest'],
    maxTokensPerRequest: 1000,
  },
  production: {
    apiKey: process.env.MISTRAL_API_KEY_PROD!,
    allowedModels: ['mistral-small-latest'],
    maxTokensPerRequest: 4000,
  },
};

export function getEnvConfig(): MistralEnvConfig {
  const env = process.env.NODE_ENV || 'development';
  return configs[env] || configs.development;
}
```

### Step 5: Request Validation & Sanitization

```typescript
import { z } from 'zod';

const messageSchema = z.object({
  role: z.enum(['system', 'user', 'assistant']),
  content: z.string().max(100000), // Prevent huge payloads
});

const chatRequestSchema = z.object({
  model: z.enum(['mistral-small-latest', 'mistral-large-latest']),
  messages: z.array(messageSchema).min(1).max(100),
  temperature: z.number().min(0).max(1).optional(),
  maxTokens: z.number().min(1).max(4000).optional(),
});

function validateChatRequest(input: unknown) {
  return chatRequestSchema.parse(input);
}

// Usage in API endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const validated = validateChatRequest(req.body);
    const response = await client.chat.complete(validated);
    res.json(response);
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ error: 'Invalid request', details: error.errors });
    } else {
      res.status(500).json({ error: 'Internal error' });
    }
  }
});
```

### Step 6: Audit Logging

```typescript
interface AuditEntry {
  timestamp: Date;
  action: string;
  userId?: string;
  model: string;
  tokensUsed?: number;
  success: boolean;
  errorCode?: string;
  ipAddress?: string;
}

async function auditLog(entry: Omit<AuditEntry, 'timestamp'>): Promise<void> {
  const log: AuditEntry = { ...entry, timestamp: new Date() };

  // Log to your audit system
  console.log('[AUDIT]', JSON.stringify(log));

  // Optional: send to logging service
  // await loggingService.record(log);
}

// Usage
async function chatWithAudit(
  userId: string,
  messages: Message[],
  ipAddress?: string
): Promise<string> {
  const start = Date.now();
  try {
    const response = await client.chat.complete({
      model: 'mistral-small-latest',
      messages,
    });

    await auditLog({
      action: 'chat.complete',
      userId,
      model: 'mistral-small-latest',
      tokensUsed: response.usage?.totalTokens,
      success: true,
      ipAddress,
    });

    return response.choices?.[0]?.message?.content ?? '';
  } catch (error: any) {
    await auditLog({
      action: 'chat.complete',
      userId,
      model: 'mistral-small-latest',
      success: false,
      errorCode: error.status?.toString(),
      ipAddress,
    });
    throw error;
  }
}
```

## Security Checklist

- [ ] API key stored in environment variable (not code)
- [ ] `.env` files in `.gitignore`
- [ ] Different keys for dev/staging/prod
- [ ] Input validation on all requests
- [ ] Output sanitization before display
- [ ] Audit logging enabled
- [ ] Rate limiting implemented
- [ ] Error messages don't expose internals
- [ ] HTTPS enforced for all endpoints
- [ ] Regular key rotation scheduled

## Output
- Secure API key storage
- Environment-specific access controls
- Input validation
- Audit logging enabled

## Error Handling
| Security Issue | Detection | Mitigation |
|----------------|-----------|------------|
| Exposed API key | Git scanning, log review | Rotate immediately, revoke old key |
| Injection attacks | Input validation | Zod schemas, sanitization |
| Missing audit trail | Log review | Implement comprehensive logging |
| Excessive permissions | Access review | Limit models per environment |

## Examples

### Secrets Manager Integration (AWS)
```typescript
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

const sm = new SecretsManager({ region: 'us-east-1' });

async function getMistralApiKey(): Promise<string> {
  const secret = await sm.getSecretValue({
    SecretId: 'mistral/api-key',
  });
  return secret.SecretString!;
}
```

### Secrets Manager Integration (GCP)
```typescript
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

const client = new SecretManagerServiceClient();

async function getMistralApiKey(): Promise<string> {
  const [version] = await client.accessSecretVersion({
    name: 'projects/my-project/secrets/mistral-api-key/versions/latest',
  });
  return version.payload?.data?.toString()!;
}
```

### Content Filtering
```typescript
const BLOCKED_PATTERNS = [
  /\b(password|secret|key)\s*[:=]/i,
  /\b\d{16}\b/, // Credit card numbers
  /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b/i, // Emails
];

function containsSensitiveData(text: string): boolean {
  return BLOCKED_PATTERNS.some(pattern => pattern.test(text));
}

async function safeChatComplete(messages: Message[]): Promise<string> {
  // Check input for sensitive data
  for (const msg of messages) {
    if (containsSensitiveData(msg.content)) {
      throw new Error('Message contains potentially sensitive data');
    }
  }

  return client.chat.complete({ model: 'mistral-small-latest', messages });
}
```

## Resources
- [Mistral AI Console](https://console.mistral.ai/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [Zod Documentation](https://zod.dev/)

## Next Steps
For production deployment, see `mistral-prod-checklist`.
