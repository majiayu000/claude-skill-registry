---
name: twinmind-data-handling
description: |
  Handle data privacy, GDPR compliance, and data retention for TwinMind.
  Use when implementing data protection, handling user data requests,
  or ensuring compliance with privacy regulations.
  Trigger with phrases like "twinmind GDPR", "twinmind data privacy",
  "twinmind data retention", "twinmind user data", "twinmind compliance".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# TwinMind Data Handling

## Overview
Data privacy, retention, and compliance procedures for TwinMind meeting transcriptions.

## Prerequisites
- Understanding of GDPR/CCPA requirements
- TwinMind account with admin access
- Database access for data management
- Legal/compliance team consultation

## Data Classification

| Data Type | Classification | Retention | Notes |
|-----------|---------------|-----------|-------|
| Audio recordings | Not stored | 0 | TwinMind deletes immediately |
| Transcripts | Sensitive | Configurable | Contains meeting content |
| Summaries | Sensitive | Same as transcript | Derived from transcript |
| Action items | Business | Configurable | May contain PII |
| Speaker data | PII | Same as transcript | Names, voice profiles |
| Usage logs | Internal | 90 days | For debugging |
| Billing data | Business | 7 years | Legal requirement |

## Instructions

### Step 1: Configure Data Retention Policies

```typescript
// src/twinmind/compliance/retention.ts
export interface RetentionPolicy {
  transcripts: {
    defaultDays: number;
    maxDays: number;
    autoDelete: boolean;
  };
  summaries: {
    defaultDays: number;
    linkedToTranscript: boolean;  // Delete when transcript deleted
  };
  actionItems: {
    defaultDays: number;
    deleteOnComplete: boolean;
  };
  userProfiles: {
    retainAfterDeletion: number;  // Days to retain after user deletion
  };
}

const defaultRetentionPolicy: RetentionPolicy = {
  transcripts: {
    defaultDays: 90,
    maxDays: 365,
    autoDelete: true,
  },
  summaries: {
    defaultDays: 90,
    linkedToTranscript: true,
  },
  actionItems: {
    defaultDays: 180,
    deleteOnComplete: false,
  },
  userProfiles: {
    retainAfterDeletion: 30,
  },
};

export async function applyRetentionPolicy(policy: RetentionPolicy): Promise<void> {
  const client = getTwinMindClient();

  await client.patch('/settings/retention', {
    transcript_retention_days: policy.transcripts.defaultDays,
    auto_delete_enabled: policy.transcripts.autoDelete,
    cascade_delete_summaries: policy.summaries.linkedToTranscript,
  });

  console.log('Retention policy applied successfully');
}

// Cleanup job for expired data
export async function cleanupExpiredData(): Promise<{
  transcriptsDeleted: number;
  summariesDeleted: number;
  actionItemsDeleted: number;
}> {
  const client = getTwinMindClient();
  const policy = await getRetentionPolicy();

  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - policy.transcripts.defaultDays);

  // Find and delete expired transcripts
  const expiredTranscripts = await client.get('/transcripts', {
    params: {
      created_before: cutoffDate.toISOString(),
      limit: 1000,
    },
  });

  let transcriptsDeleted = 0;
  for (const transcript of expiredTranscripts.data) {
    await client.delete(`/transcripts/${transcript.id}`);
    transcriptsDeleted++;
  }

  return {
    transcriptsDeleted,
    summariesDeleted: transcriptsDeleted,  // Cascaded
    actionItemsDeleted: 0,  // Handled separately
  };
}
```

### Step 2: Implement PII Redaction

```typescript
// src/twinmind/compliance/pii.ts
export interface PIIPattern {
  name: string;
  pattern: RegExp;
  replacement: string;
}

const defaultPIIPatterns: PIIPattern[] = [
  {
    name: 'SSN',
    pattern: /\b\d{3}-\d{2}-\d{4}\b/g,
    replacement: '[SSN REDACTED]',
  },
  {
    name: 'Credit Card',
    pattern: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g,
    replacement: '[CARD REDACTED]',
  },
  {
    name: 'Email',
    pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
    replacement: '[EMAIL REDACTED]',
  },
  {
    name: 'Phone',
    pattern: /\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b/g,
    replacement: '[PHONE REDACTED]',
  },
  {
    name: 'IP Address',
    pattern: /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g,
    replacement: '[IP REDACTED]',
  },
];

export function redactPII(
  text: string,
  patterns: PIIPattern[] = defaultPIIPatterns
): {
  redactedText: string;
  redactions: Array<{ type: string; count: number }>;
} {
  let redactedText = text;
  const redactions: Array<{ type: string; count: number }> = [];

  for (const pattern of patterns) {
    const matches = text.match(pattern.pattern);
    if (matches && matches.length > 0) {
      redactedText = redactedText.replace(pattern.pattern, pattern.replacement);
      redactions.push({ type: pattern.name, count: matches.length });
    }
  }

  return { redactedText, redactions };
}

// Configure automatic PII redaction
export async function enablePIIRedaction(): Promise<void> {
  const client = getTwinMindClient();

  await client.patch('/settings/privacy', {
    redact_pii: true,
    pii_patterns: defaultPIIPatterns.map(p => ({
      name: p.name,
      pattern: p.pattern.source,
      flags: p.pattern.flags,
    })),
  });
}
```

### Step 3: Implement GDPR Data Subject Requests

```typescript
// src/twinmind/compliance/gdpr.ts
export interface DataSubjectRequest {
  type: 'access' | 'rectification' | 'erasure' | 'portability';
  subjectEmail: string;
  requestedAt: Date;
  deadline: Date;  // 30 days from request
  status: 'pending' | 'in_progress' | 'completed' | 'rejected';
}

export class GDPRHandler {
  private client = getTwinMindClient();

  // Right to Access (Article 15)
  async handleAccessRequest(email: string): Promise<{
    transcripts: any[];
    summaries: any[];
    actionItems: any[];
    profile: any;
  }> {
    // Find all data associated with email
    const [transcripts, profile] = await Promise.all([
      this.client.get('/transcripts', {
        params: { participant_email: email, limit: 1000 },
      }),
      this.client.get('/users', { params: { email } }),
    ]);

    // Get related summaries and action items
    const summaries = [];
    const actionItems = [];

    for (const transcript of transcripts.data) {
      const [summary, actions] = await Promise.all([
        this.client.get(`/transcripts/${transcript.id}/summary`).catch(() => null),
        this.client.get(`/transcripts/${transcript.id}/action-items`).catch(() => []),
      ]);
      if (summary) summaries.push(summary.data);
      actionItems.push(...(actions.data || []));
    }

    return {
      transcripts: transcripts.data,
      summaries,
      actionItems,
      profile: profile.data,
    };
  }

  // Right to Erasure (Article 17)
  async handleErasureRequest(email: string): Promise<{
    transcriptsDeleted: number;
    profileDeleted: boolean;
  }> {
    // Find all data
    const data = await this.handleAccessRequest(email);

    // Delete transcripts (cascades to summaries)
    let transcriptsDeleted = 0;
    for (const transcript of data.transcripts) {
      await this.client.delete(`/transcripts/${transcript.id}`);
      transcriptsDeleted++;
    }

    // Delete user profile
    if (data.profile?.id) {
      await this.client.delete(`/users/${data.profile.id}`);
    }

    return {
      transcriptsDeleted,
      profileDeleted: !!data.profile?.id,
    };
  }

  // Right to Data Portability (Article 20)
  async handlePortabilityRequest(email: string): Promise<Buffer> {
    const data = await this.handleAccessRequest(email);

    // Export in machine-readable format (JSON)
    const exportData = {
      exportedAt: new Date().toISOString(),
      subject: email,
      data: {
        profile: data.profile,
        transcripts: data.transcripts.map(t => ({
          id: t.id,
          title: t.title,
          text: t.text,
          duration_seconds: t.duration_seconds,
          language: t.language,
          created_at: t.created_at,
        })),
        summaries: data.summaries,
        actionItems: data.actionItems,
      },
    };

    return Buffer.from(JSON.stringify(exportData, null, 2));
  }

  // Log and track DSR
  async createDSR(request: Omit<DataSubjectRequest, 'deadline' | 'status'>): Promise<string> {
    const dsr: DataSubjectRequest = {
      ...request,
      deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),  // 30 days
      status: 'pending',
    };

    // Store in database
    const result = await db.dataSubjectRequests.create(dsr);

    // Notify compliance team
    await notifyComplianceTeam({
      type: 'NEW_DSR',
      request: dsr,
    });

    return result.id;
  }
}
```

### Step 4: Implement Consent Management

```typescript
// src/twinmind/compliance/consent.ts
export interface ConsentRecord {
  userId: string;
  purposes: {
    transcription: boolean;
    aiProcessing: boolean;
    storage: boolean;
    sharing: boolean;
    marketing: boolean;
  };
  consentedAt: Date;
  method: 'explicit' | 'implied';
  ipAddress?: string;
  version: string;  // Consent policy version
}

export class ConsentManager {
  async recordConsent(
    userId: string,
    purposes: ConsentRecord['purposes'],
    method: 'explicit' | 'implied',
    ipAddress?: string
  ): Promise<void> {
    const record: ConsentRecord = {
      userId,
      purposes,
      consentedAt: new Date(),
      method,
      ipAddress,
      version: process.env.CONSENT_POLICY_VERSION || '1.0',
    };

    await db.consents.create(record);

    // Sync to TwinMind
    const client = getTwinMindClient();
    await client.patch(`/users/${userId}/consent`, {
      transcription: purposes.transcription,
      ai_processing: purposes.aiProcessing,
      storage: purposes.storage,
    });
  }

  async getConsent(userId: string): Promise<ConsentRecord | null> {
    return db.consents.findLatest({ userId });
  }

  async revokeConsent(userId: string, purposes: string[]): Promise<void> {
    const current = await this.getConsent(userId);

    if (!current) {
      throw new Error('No consent record found');
    }

    const updated = { ...current.purposes };
    for (const purpose of purposes) {
      updated[purpose as keyof typeof updated] = false;
    }

    await this.recordConsent(userId, updated, 'explicit');

    // If all consents revoked, trigger data deletion
    if (Object.values(updated).every(v => !v)) {
      const gdpr = new GDPRHandler();
      await gdpr.handleErasureRequest(userId);
    }
  }

  async checkConsent(userId: string, purpose: keyof ConsentRecord['purposes']): Promise<boolean> {
    const consent = await this.getConsent(userId);
    return consent?.purposes[purpose] ?? false;
  }
}

// Middleware to check consent before processing
export function requireConsent(purpose: keyof ConsentRecord['purposes']) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const userId = req.user?.id;

    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const consentManager = new ConsentManager();
    const hasConsent = await consentManager.checkConsent(userId, purpose);

    if (!hasConsent) {
      return res.status(403).json({
        error: 'Consent required',
        required_purpose: purpose,
        consent_url: '/settings/privacy',
      });
    }

    next();
  };
}
```

### Step 5: Data Anonymization

```typescript
// src/twinmind/compliance/anonymization.ts
import crypto from 'crypto';

export interface AnonymizationConfig {
  hashSalt: string;
  preserveStructure: boolean;
  preserveTimestamps: boolean;
}

export function anonymizeTranscript(
  transcript: Transcript,
  config: AnonymizationConfig
): Transcript {
  return {
    ...transcript,
    id: hashId(transcript.id, config.hashSalt),
    text: redactPII(transcript.text).redactedText,
    speakers: transcript.speakers?.map((speaker, index) => ({
      ...speaker,
      id: hashId(speaker.id, config.hashSalt),
      name: `Speaker ${index + 1}`,
    })),
    segments: transcript.segments?.map(segment => ({
      ...segment,
      speaker_id: hashId(segment.speaker_id || '', config.hashSalt),
      text: redactPII(segment.text).redactedText,
    })),
  };
}

function hashId(id: string, salt: string): string {
  return crypto.createHmac('sha256', salt).update(id).digest('hex').substring(0, 16);
}

// Export anonymized data for analytics
export async function exportAnonymizedData(
  dateRange: { from: Date; to: Date }
): Promise<any[]> {
  const client = getTwinMindClient();
  const config: AnonymizationConfig = {
    hashSalt: process.env.ANONYMIZATION_SALT!,
    preserveStructure: true,
    preserveTimestamps: true,
  };

  const transcripts = await client.get('/transcripts', {
    params: {
      created_after: dateRange.from.toISOString(),
      created_before: dateRange.to.toISOString(),
    },
  });

  return transcripts.data.map((t: Transcript) => anonymizeTranscript(t, config));
}
```

## Output
- Data retention policy configuration
- PII redaction implementation
- GDPR request handlers
- Consent management system
- Data anonymization utilities

## Compliance Checklist

```markdown
## GDPR Compliance Checklist

### Data Processing
- [ ] Lawful basis documented for all processing
- [ ] Data minimization principle applied
- [ ] Purpose limitation enforced
- [ ] Accuracy mechanisms in place

### Data Subject Rights
- [ ] Right to access implemented
- [ ] Right to rectification implemented
- [ ] Right to erasure implemented
- [ ] Right to data portability implemented
- [ ] Right to object implemented

### Security
- [ ] Encryption at rest enabled
- [ ] Encryption in transit (TLS 1.3)
- [ ] Access controls implemented
- [ ] Audit logging enabled

### Documentation
- [ ] Privacy policy updated
- [ ] Data processing records maintained
- [ ] DPA signed with TwinMind
- [ ] DPIA conducted if required

### Breach Response
- [ ] Breach notification procedure documented
- [ ] 72-hour notification capability
- [ ] Incident response team identified
```

## TwinMind Privacy Features

TwinMind provides these built-in privacy protections:
- **No audio storage**: Audio processed in real-time and immediately deleted
- **On-device processing**: Option for local transcription (no data sent to cloud)
- **Encrypted storage**: All transcripts encrypted with user-controlled keys
- **Data residency**: Choose data storage region (EU, US, APAC)
- **Automatic deletion**: Configurable retention periods

## Error Handling

| Issue | Cause | Solution |
|-------|-------|----------|
| DSR deadline missed | Processing delay | Automate DSR handling |
| PII not redacted | Pattern not matched | Update patterns |
| Consent invalid | Version mismatch | Re-request consent |
| Data not deleted | Cascade failure | Verify deletion |

## Resources
- [GDPR Official Text](https://gdpr.eu/)
- [TwinMind Privacy Policy](https://twinmind.com/privacy)
- [TwinMind DPA Template](https://twinmind.com/legal/dpa)

## Next Steps
For enterprise access control, see `twinmind-enterprise-rbac`.
