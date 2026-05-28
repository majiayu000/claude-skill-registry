---
name: mistral-enterprise-rbac
description: |
  Configure Mistral AI enterprise access control and organization management.
  Use when implementing role-based permissions, managing team access,
  or setting up organization-level controls for Mistral AI.
  Trigger with phrases like "mistral access control", "mistral RBAC",
  "mistral enterprise", "mistral roles", "mistral permissions", "mistral team".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Mistral AI Enterprise RBAC

## Overview
Configure enterprise-grade access control for Mistral AI integrations within your organization.

## Prerequisites
- Mistral AI API access
- Understanding of role-based access patterns
- User management system in place
- Audit logging infrastructure

## Role Definitions

| Role | Permissions | Use Case |
|------|-------------|----------|
| Admin | Full access, manage keys | Platform administrators |
| Developer | All models, full features | Active development |
| Analyst | Read-only, limited models | Data analysis, reports |
| Service | API access, specific model | Automated systems |
| Viewer | Read logs only | Auditors, stakeholders |

## Instructions

### Step 1: Define Permission Schema

```typescript
// permissions.ts
export type MistralPermission =
  | 'chat:complete'
  | 'chat:stream'
  | 'embeddings:create'
  | 'models:list'
  | 'models:use:small'
  | 'models:use:large'
  | 'keys:manage'
  | 'usage:view'
  | 'audit:view';

export type MistralRole = 'admin' | 'developer' | 'analyst' | 'service' | 'viewer';

export const ROLE_PERMISSIONS: Record<MistralRole, MistralPermission[]> = {
  admin: [
    'chat:complete', 'chat:stream', 'embeddings:create',
    'models:list', 'models:use:small', 'models:use:large',
    'keys:manage', 'usage:view', 'audit:view',
  ],
  developer: [
    'chat:complete', 'chat:stream', 'embeddings:create',
    'models:list', 'models:use:small', 'models:use:large',
    'usage:view',
  ],
  analyst: [
    'chat:complete', 'embeddings:create',
    'models:list', 'models:use:small',
    'usage:view',
  ],
  service: [
    'chat:complete', 'chat:stream', 'embeddings:create',
    'models:use:small',
  ],
  viewer: [
    'models:list', 'usage:view', 'audit:view',
  ],
};

export function hasPermission(role: MistralRole, permission: MistralPermission): boolean {
  return ROLE_PERMISSIONS[role].includes(permission);
}
```

### Step 2: User and Organization Management

```typescript
interface MistralUser {
  id: string;
  email: string;
  role: MistralRole;
  organizationId: string;
  apiKeyId?: string;
  createdAt: Date;
  lastActiveAt?: Date;
}

interface MistralOrganization {
  id: string;
  name: string;
  plan: 'free' | 'pro' | 'enterprise';
  settings: {
    allowedModels: string[];
    maxRequestsPerDay: number;
    requireApproval: boolean;
  };
  createdAt: Date;
}

class OrganizationManager {
  async createOrganization(name: string, plan: MistralOrganization['plan']): Promise<MistralOrganization> {
    const org: MistralOrganization = {
      id: crypto.randomUUID(),
      name,
      plan,
      settings: this.getDefaultSettings(plan),
      createdAt: new Date(),
    };

    await db.organizations.insert(org);
    return org;
  }

  private getDefaultSettings(plan: MistralOrganization['plan']) {
    const settings = {
      free: {
        allowedModels: ['mistral-small-latest'],
        maxRequestsPerDay: 100,
        requireApproval: false,
      },
      pro: {
        allowedModels: ['mistral-small-latest', 'mistral-large-latest'],
        maxRequestsPerDay: 10000,
        requireApproval: false,
      },
      enterprise: {
        allowedModels: ['mistral-small-latest', 'mistral-large-latest', 'mistral-embed'],
        maxRequestsPerDay: 1000000,
        requireApproval: true,
      },
    };
    return settings[plan];
  }

  async addUser(orgId: string, email: string, role: MistralRole): Promise<MistralUser> {
    const user: MistralUser = {
      id: crypto.randomUUID(),
      email,
      role,
      organizationId: orgId,
      createdAt: new Date(),
    };

    await db.users.insert(user);
    return user;
  }

  async updateUserRole(userId: string, newRole: MistralRole): Promise<void> {
    await db.users.update({ id: userId }, { $set: { role: newRole } });

    // Audit log
    await auditLogger.log({
      action: 'user.role.updated',
      userId,
      newRole,
      performedBy: getCurrentUser().id,
    });
  }
}
```

### Step 3: Permission Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

interface AuthenticatedRequest extends Request {
  user?: MistralUser;
  organization?: MistralOrganization;
}

function requirePermission(permission: MistralPermission) {
  return async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const user = req.user;

    if (!user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!hasPermission(user.role, permission)) {
      // Audit failed access attempt
      await auditLogger.log({
        action: 'permission.denied',
        userId: user.id,
        permission,
        resource: req.path,
      });

      return res.status(403).json({
        error: 'Forbidden',
        message: `Missing permission: ${permission}`,
      });
    }

    next();
  };
}

// Usage
app.post('/api/chat',
  requirePermission('chat:complete'),
  async (req: AuthenticatedRequest, res) => {
    // Handle chat request
  }
);

app.post('/api/chat/stream',
  requirePermission('chat:stream'),
  async (req: AuthenticatedRequest, res) => {
    // Handle streaming
  }
);
```

### Step 4: Model Access Control

```typescript
function requireModelAccess(model: string) {
  return async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const user = req.user!;
    const org = req.organization!;

    // Check organization allows this model
    if (!org.settings.allowedModels.includes(model)) {
      return res.status(403).json({
        error: 'Model not allowed',
        message: `Your organization does not have access to ${model}`,
      });
    }

    // Check user role allows this model
    const modelPermission = model.includes('large')
      ? 'models:use:large'
      : 'models:use:small';

    if (!hasPermission(user.role, modelPermission as MistralPermission)) {
      return res.status(403).json({
        error: 'Model access denied',
        message: `Your role does not allow access to ${model}`,
      });
    }

    next();
  };
}
```

### Step 5: API Key Scoping

```typescript
interface ScopedApiKey {
  id: string;
  key: string; // Hashed
  userId: string;
  organizationId: string;
  name: string;
  permissions: MistralPermission[];
  allowedModels: string[];
  rateLimit: {
    requestsPerMinute: number;
    tokensPerDay: number;
  };
  expiresAt?: Date;
  createdAt: Date;
}

class ApiKeyManager {
  async createScopedKey(
    userId: string,
    name: string,
    permissions: MistralPermission[],
    options?: {
      allowedModels?: string[];
      rateLimit?: Partial<ScopedApiKey['rateLimit']>;
      expiresInDays?: number;
    }
  ): Promise<{ id: string; key: string }> {
    const user = await db.users.findOne({ id: userId });
    if (!user) throw new Error('User not found');

    // Validate permissions don't exceed user's role
    for (const perm of permissions) {
      if (!hasPermission(user.role, perm)) {
        throw new Error(`Cannot grant permission ${perm} - exceeds user role`);
      }
    }

    const rawKey = `msk_${crypto.randomBytes(32).toString('hex')}`;
    const hashedKey = crypto.createHash('sha256').update(rawKey).digest('hex');

    const scopedKey: ScopedApiKey = {
      id: crypto.randomUUID(),
      key: hashedKey,
      userId,
      organizationId: user.organizationId,
      name,
      permissions,
      allowedModels: options?.allowedModels || ['mistral-small-latest'],
      rateLimit: {
        requestsPerMinute: options?.rateLimit?.requestsPerMinute || 60,
        tokensPerDay: options?.rateLimit?.tokensPerDay || 100000,
      },
      expiresAt: options?.expiresInDays
        ? new Date(Date.now() + options.expiresInDays * 24 * 60 * 60 * 1000)
        : undefined,
      createdAt: new Date(),
    };

    await db.apiKeys.insert(scopedKey);

    return { id: scopedKey.id, key: rawKey };
  }

  async validateKey(rawKey: string): Promise<ScopedApiKey | null> {
    const hashedKey = crypto.createHash('sha256').update(rawKey).digest('hex');
    const key = await db.apiKeys.findOne({ key: hashedKey });

    if (!key) return null;
    if (key.expiresAt && key.expiresAt < new Date()) return null;

    return key;
  }
}
```

### Step 6: Usage Quotas

```typescript
class UsageQuotaManager {
  async checkQuota(userId: string, orgId: string): Promise<{
    allowed: boolean;
    remaining: { requests: number; tokens: number };
    resetAt: Date;
  }> {
    const org = await db.organizations.findOne({ id: orgId });
    const today = new Date().toISOString().split('T')[0];

    const usage = await db.usage.findOne({
      organizationId: orgId,
      date: today,
    }) || { requests: 0, tokens: 0 };

    const maxRequests = org!.settings.maxRequestsPerDay;
    const remaining = {
      requests: Math.max(0, maxRequests - usage.requests),
      tokens: Math.max(0, 1000000 - usage.tokens), // Example limit
    };

    return {
      allowed: remaining.requests > 0 && remaining.tokens > 0,
      remaining,
      resetAt: new Date(new Date().setHours(24, 0, 0, 0)),
    };
  }

  async recordUsage(orgId: string, requests: number, tokens: number): Promise<void> {
    const today = new Date().toISOString().split('T')[0];

    await db.usage.updateOne(
      { organizationId: orgId, date: today },
      {
        $inc: { requests, tokens },
        $setOnInsert: { organizationId: orgId, date: today },
      },
      { upsert: true }
    );
  }
}
```

## Output
- Role definitions implemented
- Permission middleware active
- Model access control configured
- API key scoping enabled

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Permission denied | Wrong role | Update user role or permissions |
| Key expired | TTL passed | Generate new key |
| Quota exceeded | Heavy usage | Upgrade plan or wait for reset |
| Model not allowed | Organization restriction | Contact admin |

## Examples

### Quick Permission Check
```typescript
if (!hasPermission(user.role, 'chat:stream')) {
  throw new ForbiddenError('Streaming not allowed for your role');
}
```

### Create Limited Service Key
```typescript
const { key } = await keyManager.createScopedKey(
  serviceUserId,
  'background-processor',
  ['chat:complete'],
  {
    allowedModels: ['mistral-small-latest'],
    rateLimit: { requestsPerMinute: 10 },
    expiresInDays: 30,
  }
);
```

## Resources
- [RBAC Best Practices](https://csrc.nist.gov/projects/role-based-access-control)
- [Mistral AI Documentation](https://docs.mistral.ai/)

## Next Steps
For major migrations, see `mistral-migration-deep-dive`.
