---
name: lokalise-data-handling
description: |
  Implement Lokalise translation data handling, PII management, and compliance patterns.
  Use when handling sensitive translation data, implementing data redaction,
  or ensuring compliance with privacy regulations for Lokalise integrations.
  Trigger with phrases like "lokalise data", "lokalise PII",
  "lokalise GDPR", "lokalise data retention", "lokalise privacy", "lokalise compliance".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Lokalise Data Handling

## Overview
Handle translation data correctly with privacy, compliance, and data governance best practices.

## Prerequisites
- Understanding of GDPR/CCPA requirements
- Lokalise SDK installed
- Database for audit logging
- Data classification policies

## Data Classification

| Category | Examples | Handling |
|----------|----------|----------|
| Translation Keys | `welcome.message`, `error.network` | Standard |
| UI Text | "Welcome!", "Submit" | Standard |
| Dynamic Content | `Hello, {name}` | Review for PII |
| User-Generated | Comments, descriptions | May contain PII |
| API Tokens | `abc123...` | Never log |
| Screenshots | Context images | May contain PII |

## Instructions

### Step 1: Translation Content Scanning
```typescript
// Scan translations for potential PII before upload
const PII_PATTERNS = [
  { type: "email", regex: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g },
  { type: "phone", regex: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g },
  { type: "ssn", regex: /\b\d{3}-\d{2}-\d{4}\b/g },
  { type: "credit_card", regex: /\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g },
  { type: "ip_address", regex: /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g },
];

interface PIIFinding {
  type: string;
  match: string;
  key: string;
  language: string;
}

function scanTranslationsForPII(
  translations: Record<string, string>,
  language: string
): PIIFinding[] {
  const findings: PIIFinding[] = [];

  for (const [key, value] of Object.entries(translations)) {
    for (const pattern of PII_PATTERNS) {
      const matches = value.matchAll(pattern.regex);
      for (const match of matches) {
        findings.push({
          type: pattern.type,
          match: match[0],
          key,
          language,
        });
      }
    }
  }

  return findings;
}

// Pre-upload validation
async function validateBeforeUpload(filePath: string): Promise<{
  valid: boolean;
  findings: PIIFinding[];
}> {
  const content = JSON.parse(fs.readFileSync(filePath, "utf8"));
  const locale = path.basename(filePath, ".json");
  const findings = scanTranslationsForPII(content, locale);

  if (findings.length > 0) {
    console.warn("PII detected in translations:");
    findings.forEach(f => {
      console.warn(`  ${f.type} in ${f.key} (${f.language}): ${f.match}`);
    });
  }

  return {
    valid: findings.length === 0,
    findings,
  };
}
```

### Step 2: Safe Logging Practices
```typescript
// Never log API tokens or sensitive translation content
function safeLokaliseLog(
  operation: string,
  data: Record<string, any>
): void {
  const sanitized = { ...data };

  // Remove sensitive fields
  delete sanitized.apiToken;
  delete sanitized.apiKey;
  delete sanitized.webhookSecret;

  // Truncate large translation content
  if (sanitized.translation && typeof sanitized.translation === "string") {
    sanitized.translation = sanitized.translation.length > 100
      ? `${sanitized.translation.slice(0, 100)}...`
      : sanitized.translation;
  }

  // Mask key IDs in production
  if (process.env.NODE_ENV === "production" && sanitized.keyId) {
    sanitized.keyId = "***";
  }

  console.log(`[Lokalise] ${operation}:`, sanitized);
}

// Usage
safeLokaliseLog("translation.update", {
  projectId: "123456.abc",
  keyId: 789,
  language: "es",
  translation: "Updated translation text here...",
});
```

### Step 3: Data Retention Management
```typescript
interface RetentionPolicy {
  dataType: string;
  retentionDays: number;
  reason: string;
}

const RETENTION_POLICIES: RetentionPolicy[] = [
  { dataType: "api_logs", retentionDays: 30, reason: "Debugging" },
  { dataType: "error_logs", retentionDays: 90, reason: "Root cause analysis" },
  { dataType: "audit_logs", retentionDays: 2555, reason: "Compliance (7 years)" },
  { dataType: "webhook_payloads", retentionDays: 7, reason: "Retry/debugging" },
  { dataType: "translation_cache", retentionDays: 1, reason: "Performance" },
];

async function enforceRetention(dataType: string): Promise<number> {
  const policy = RETENTION_POLICIES.find(p => p.dataType === dataType);
  if (!policy) {
    throw new Error(`No retention policy for ${dataType}`);
  }

  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - policy.retentionDays);

  const deleted = await db.lokaliseData.deleteMany({
    dataType,
    createdAt: { $lt: cutoff },
  });

  console.log(`Retention: Deleted ${deleted.count} ${dataType} records older than ${policy.retentionDays} days`);
  return deleted.count;
}

// Schedule daily cleanup
// cron.schedule('0 3 * * *', () => {
//   RETENTION_POLICIES.forEach(p => enforceRetention(p.dataType));
// });
```

### Step 4: Audit Logging
```typescript
interface AuditEntry {
  timestamp: Date;
  userId: string;
  action: string;
  resource: string;
  projectId: string;
  details?: Record<string, any>;
  ipAddress?: string;
}

async function auditLokaliseAction(entry: Omit<AuditEntry, "timestamp">): Promise<void> {
  const audit: AuditEntry = {
    ...entry,
    timestamp: new Date(),
  };

  // Store in audit log (separate from regular logs)
  await db.auditLog.insert(audit);

  // Log for real-time monitoring
  console.log("[AUDIT]", JSON.stringify(audit));
}

// Usage
await auditLokaliseAction({
  userId: currentUser.id,
  action: "translation.update",
  resource: `key:${keyId}`,
  projectId: "123456.abc",
  details: {
    language: "es",
    previousValue: "[REDACTED]",
    newValue: "[REDACTED]",
  },
  ipAddress: request.ip,
});
```

### Step 5: Data Export for Compliance
```typescript
// GDPR Data Subject Access Request (DSAR)
async function exportUserTranslationActivity(userId: string): Promise<{
  user: { id: string; email: string };
  activity: AuditEntry[];
  exportedAt: string;
}> {
  // Get all Lokalise-related activity for user
  const activity = await db.auditLog.find({
    userId,
    resource: { $regex: /^lokalise/ },
  });

  return {
    user: { id: userId, email: "[from user database]" },
    activity: activity.map(a => ({
      ...a,
      // Redact sensitive details
      details: { action: a.details?.action, timestamp: a.timestamp },
    })),
    exportedAt: new Date().toISOString(),
  };
}

// Right to deletion
async function deleteUserTranslationData(userId: string): Promise<{
  deletedRecords: number;
  auditLogRetained: boolean;
}> {
  // Delete user's cached data
  const deleted = await db.translationCache.deleteMany({ userId });

  // Note: Audit logs may need to be retained for compliance
  // Instead of deleting, anonymize
  await db.auditLog.updateMany(
    { userId },
    { $set: { userId: "DELETED_USER", userEmail: "REDACTED" } }
  );

  // Log the deletion itself
  await auditLokaliseAction({
    userId: "system",
    action: "gdpr.deletion",
    resource: `user:${userId}`,
    projectId: "all",
    details: { reason: "GDPR right to deletion" },
  });

  return {
    deletedRecords: deleted.count,
    auditLogRetained: true,
  };
}
```

## Output
- PII scanning for translations
- Safe logging practices
- Data retention enforcement
- Audit trail for compliance

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| PII in translations | User-submitted content | Scan before upload |
| Token in logs | Improper logging | Use safe log wrapper |
| Audit gaps | Missing logging | Add audit calls |
| Retention violation | No cleanup | Schedule retention jobs |

## Examples

### Pre-commit PII Check
```bash
#!/bin/bash
# .husky/pre-commit

# Check for PII in translation files
node scripts/scan-translations-pii.js

if [ $? -ne 0 ]; then
  echo "PII detected in translations. Please review and remove."
  exit 1
fi
```

### Compliance Checklist
```markdown
## Translation Data Compliance Checklist

### Data Collection
- [ ] Only necessary data collected
- [ ] User consent for personalized content
- [ ] Purpose documented

### Storage
- [ ] Translations stored securely
- [ ] API tokens in secret manager
- [ ] Cache encrypted at rest

### Retention
- [ ] Retention policies defined
- [ ] Automatic cleanup scheduled
- [ ] Audit logs retained per regulations

### Access
- [ ] Role-based access to projects
- [ ] Access logged and auditable
- [ ] Regular access reviews

### User Rights
- [ ] Data export capability
- [ ] Deletion process documented
- [ ] Anonymization procedures
```

### Quick PII Scan
```typescript
const result = await validateBeforeUpload("./locales/en.json");
if (!result.valid) {
  console.error("Cannot upload: PII detected");
  result.findings.forEach(f => console.error(`  ${f.type}: ${f.key}`));
  process.exit(1);
}
```

## Resources
- [GDPR Developer Guide](https://gdpr.eu/developers/)
- [CCPA Compliance](https://oag.ca.gov/privacy/ccpa)
- [Lokalise Privacy](https://lokalise.com/privacy-policy)

## Next Steps
For enterprise access control, see `lokalise-enterprise-rbac`.
