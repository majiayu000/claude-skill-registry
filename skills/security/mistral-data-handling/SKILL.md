---
name: mistral-data-handling
description: |
  Implement Mistral AI PII handling, data retention, and GDPR/CCPA compliance patterns.
  Use when handling sensitive data, implementing data redaction, configuring retention policies,
  or ensuring compliance with privacy regulations for Mistral AI integrations.
  Trigger with phrases like "mistral data", "mistral PII",
  "mistral GDPR", "mistral data retention", "mistral privacy", "mistral CCPA".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Mistral AI Data Handling

## Overview
Handle sensitive data correctly when integrating with Mistral AI, ensuring privacy compliance.

## Prerequisites
- Understanding of GDPR/CCPA requirements
- Mistral AI SDK installed
- Database for audit logging
- Understanding of Mistral's data handling policies

## Mistral AI Data Policies

**Key Points:**
- Mistral AI does NOT use customer data for training (by default)
- API data is retained for 30 days for abuse monitoring
- Enterprise plans offer data processing agreements (DPAs)
- Check current policies at docs.mistral.ai

## Instructions

### Step 1: Data Classification

| Category | Examples | Handling |
|----------|----------|----------|
| PII | Email, name, phone, SSN | Redact before sending |
| Sensitive | Medical, financial | Anonymize or don't send |
| Credentials | API keys, passwords | NEVER send |
| Business | Internal data | Consider anonymization |
| Public | Product names, general info | Safe to send |

### Step 2: PII Detection

```typescript
interface PIIMatch {
  type: string;
  match: string;
  start: number;
  end: number;
}

const PII_PATTERNS: Array<{ type: string; regex: RegExp }> = [
  { type: 'email', regex: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g },
  { type: 'phone', regex: /\b(\+?1[-.]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/g },
  { type: 'ssn', regex: /\b\d{3}-\d{2}-\d{4}\b/g },
  { type: 'credit_card', regex: /\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g },
  { type: 'ip_address', regex: /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g },
  { type: 'date_of_birth', regex: /\b(0[1-9]|1[0-2])[\/\-](0[1-9]|[12]\d|3[01])[\/\-](19|20)\d{2}\b/g },
];

function detectPII(text: string): PIIMatch[] {
  const findings: PIIMatch[] = [];

  for (const { type, regex } of PII_PATTERNS) {
    // Reset regex state
    regex.lastIndex = 0;
    let match;
    while ((match = regex.exec(text)) !== null) {
      findings.push({
        type,
        match: match[0],
        start: match.index,
        end: match.index + match[0].length,
      });
    }
  }

  return findings;
}

// Usage
const text = 'Contact John at john@example.com or 555-123-4567';
const pii = detectPII(text);
console.log(pii);
// [{ type: 'email', match: 'john@example.com', ... }, { type: 'phone', match: '555-123-4567', ... }]
```

### Step 3: Data Redaction

```typescript
function redactPII(text: string, replacement = '[REDACTED]'): string {
  let redacted = text;

  for (const { regex } of PII_PATTERNS) {
    regex.lastIndex = 0;
    redacted = redacted.replace(regex, replacement);
  }

  return redacted;
}

function redactWithPlaceholders(text: string): { redacted: string; mapping: Map<string, string> } {
  const mapping = new Map<string, string>();
  let redacted = text;
  let counter = 0;

  for (const { type, regex } of PII_PATTERNS) {
    regex.lastIndex = 0;
    redacted = redacted.replace(regex, (match) => {
      const placeholder = `[${type.toUpperCase()}_${++counter}]`;
      mapping.set(placeholder, match);
      return placeholder;
    });
  }

  return { redacted, mapping };
}

// Usage
const input = 'Send report to john@example.com and jane@company.org';
const { redacted, mapping } = redactWithPlaceholders(input);
console.log(redacted);
// 'Send report to [EMAIL_1] and [EMAIL_2]'
```

### Step 4: Pre-Request Validation

```typescript
interface ValidationResult {
  safe: boolean;
  warnings: string[];
  piiFound: PIIMatch[];
}

function validateBeforeSending(messages: Array<{ role: string; content: string }>): ValidationResult {
  const warnings: string[] = [];
  const allPII: PIIMatch[] = [];

  for (const message of messages) {
    const pii = detectPII(message.content);
    allPII.push(...pii);
  }

  // Group by type
  const piiByType = allPII.reduce((acc, p) => {
    acc[p.type] = (acc[p.type] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  if (allPII.length > 0) {
    const typeList = Object.entries(piiByType)
      .map(([type, count]) => `${count} ${type}(s)`)
      .join(', ');
    warnings.push(`PII detected: ${typeList}`);
  }

  return {
    safe: allPII.length === 0,
    warnings,
    piiFound: allPII,
  };
}

// Middleware
async function safeChat(
  client: Mistral,
  messages: Array<{ role: string; content: string }>,
  options?: { allowPII?: boolean; autoRedact?: boolean }
): Promise<string> {
  const validation = validateBeforeSending(messages);

  if (!validation.safe) {
    if (options?.autoRedact) {
      // Auto-redact PII
      messages = messages.map(m => ({
        ...m,
        content: redactPII(m.content),
      }));
    } else if (!options?.allowPII) {
      throw new Error(`PII detected in request: ${validation.warnings.join(', ')}`);
    }
  }

  const response = await client.chat.complete({
    model: 'mistral-small-latest',
    messages,
  });

  return response.choices?.[0]?.message?.content ?? '';
}
```

### Step 5: Audit Logging

```typescript
interface AuditLog {
  timestamp: Date;
  requestId: string;
  userId?: string;
  operation: string;
  model: string;
  inputTokens: number;
  outputTokens: number;
  piiDetected: boolean;
  piiTypes: string[];
  redacted: boolean;
}

class MistralAuditLogger {
  private logs: AuditLog[] = [];

  async log(entry: Omit<AuditLog, 'timestamp'>): Promise<void> {
    const log: AuditLog = {
      ...entry,
      timestamp: new Date(),
    };

    // Store in database
    await db.auditLogs.insert(log);

    // Console log for immediate visibility
    console.log('[AUDIT]', JSON.stringify(log));
  }

  async getLogsForUser(userId: string, days = 30): Promise<AuditLog[]> {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - days);

    return db.auditLogs.find({
      userId,
      timestamp: { $gte: cutoff },
    });
  }
}
```

### Step 6: GDPR Data Subject Requests

```typescript
// Right to Access (DSAR)
async function exportUserData(userId: string): Promise<{
  auditLogs: AuditLog[];
  exportedAt: string;
}> {
  const auditLogs = await auditLogger.getLogsForUser(userId);

  return {
    auditLogs: auditLogs.map(log => ({
      ...log,
      // Don't include actual content, just metadata
    })),
    exportedAt: new Date().toISOString(),
  };
}

// Right to Erasure
async function deleteUserData(userId: string): Promise<{
  success: boolean;
  deletedCount: number;
}> {
  // 1. Delete audit logs older than legal retention period
  const result = await db.auditLogs.deleteMany({
    userId,
    timestamp: { $lt: new Date(Date.now() - 7 * 365 * 24 * 60 * 60 * 1000) }, // Keep 7 years for compliance
  });

  // 2. Anonymize remaining logs
  await db.auditLogs.updateMany(
    { userId },
    { $set: { userId: '[DELETED]' } }
  );

  // 3. Record deletion for compliance
  await db.deletionLog.insert({
    userId,
    deletedAt: new Date(),
    recordsAffected: result.deletedCount,
  });

  return {
    success: true,
    deletedCount: result.deletedCount,
  };
}
```

### Step 7: Data Retention Policy

```typescript
interface RetentionPolicy {
  dataType: string;
  retentionDays: number;
  reason: string;
}

const RETENTION_POLICIES: RetentionPolicy[] = [
  { dataType: 'audit_logs', retentionDays: 90, reason: 'Operational debugging' },
  { dataType: 'error_logs', retentionDays: 30, reason: 'Error tracking' },
  { dataType: 'compliance_logs', retentionDays: 2555, reason: 'Legal requirement (7 years)' },
];

async function enforceRetention(): Promise<void> {
  for (const policy of RETENTION_POLICIES) {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - policy.retentionDays);

    const result = await db.collection(policy.dataType).deleteMany({
      createdAt: { $lt: cutoff },
    });

    console.log(`Cleaned ${result.deletedCount} records from ${policy.dataType}`);
  }
}

// Run daily
// cron.schedule('0 3 * * *', enforceRetention);
```

## Output
- PII detection implemented
- Data redaction active
- Audit logging enabled
- GDPR compliance procedures in place

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| PII in logs | Missing redaction | Apply logging middleware |
| Deletion failed | Locked records | Check foreign key constraints |
| False positives | Overly broad regex | Tune PII patterns |
| Audit gaps | Async failures | Add retry logic |

## Examples

### Safe Chat Wrapper
```typescript
const response = await safeChat(client, messages, { autoRedact: true });
```

### Quick PII Check
```typescript
const hasPII = detectPII(userInput).length > 0;
if (hasPII) {
  console.warn('PII detected in user input');
}
```

## Resources
- [GDPR Developer Guide](https://gdpr.eu/developers/)
- [CCPA Compliance Guide](https://oag.ca.gov/privacy/ccpa)
- [Mistral AI Privacy Policy](https://mistral.ai/privacy/)

## Next Steps
For enterprise access control, see `mistral-enterprise-rbac`.
