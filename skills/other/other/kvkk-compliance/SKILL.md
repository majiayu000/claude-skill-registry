---
name: kvkk-compliance
description: KVKK and GDPR compliance patterns - consent management, right to erasure, breach notification, audit logging, cookie consent, and data classification.
---

# KVKK & GDPR Compliance Patterns

Practical patterns for Turkish KVKK (Law No. 6698) and EU GDPR data protection compliance.

## KVKK vs GDPR Comparison

| Aspect | KVKK (Turkey) | GDPR (EU) |
|--------|---------------|-----------|
| Authority | KVKK Board (Kisisel Verileri Koruma Kurumu) | National DPAs + EDPB |
| Consent | Explicit, no pre-ticked boxes | Freely given, specific, informed |
| Breach notification | "As soon as possible" to Board | 72 hours to DPA |
| DPO requirement | VERBiS registration | Mandatory for public bodies + large-scale |
| Right to erasure | Article 7 - withdrawal + deletion | Article 17 - "Right to be forgotten" |
| Data transfer abroad | Board approval or adequate country | Adequacy decision, SCCs, or BCRs |
| Fines | Up to ~2M TL per violation | Up to 20M EUR or 4% global turnover |
| Legal bases | 5 in Article 5 + explicit consent | 6 in Article 6 + explicit consent |

## Data Classification

```typescript
enum DataCategory {
  PERSONAL = 'personal',           // name, email, phone
  SPECIAL = 'special_category',    // health, biometrics, religion
  ANONYMOUS = 'anonymous',         // cannot identify anyone
  PSEUDONYMOUS = 'pseudonymous',   // identifiable only with additional data
}

interface DataField {
  name: string
  category: DataCategory
  retentionDays: number
  requiresExplicitConsent: boolean
  encryptAtRest: boolean
}

const USER_DATA_FIELDS: DataField[] = [
  { name: 'email', category: DataCategory.PERSONAL, retentionDays: 730, requiresExplicitConsent: false, encryptAtRest: false },
  { name: 'healthRecords', category: DataCategory.SPECIAL, retentionDays: 365, requiresExplicitConsent: true, encryptAtRest: true },
  { name: 'analyticsId', category: DataCategory.PSEUDONYMOUS, retentionDays: 365, requiresExplicitConsent: false, encryptAtRest: false },
]
```

## Consent Management

```typescript
// BAD: single "accept all" checkbox - violates both KVKK and GDPR
// <input type="checkbox" /> I accept everything

// GOOD: granular, purpose-specific consent
interface ConsentRecord {
  userId: string; purpose: string; granted: boolean
  timestamp: Date; ipAddress: string; version: string
}

const CONSENT_PURPOSES = [
  { id: 'essential', label: 'Service operation', required: true },
  { id: 'analytics', label: 'Usage analytics', required: false },
  { id: 'marketing', label: 'Marketing emails', required: false },
  { id: 'third_party', label: 'Third-party sharing', required: false },
] as const

async function recordConsent(userId: string, purposeId: string, granted: boolean, meta: { ip: string; userAgent: string }): Promise<ConsentRecord> {
  // Always INSERT, never UPDATE - full audit trail
  return db.consentRecords.create({
    data: { userId, purpose: purposeId, granted, timestamp: new Date(), ipAddress: meta.ip, version: CURRENT_CONSENT_VERSION },
  })
}

async function hasActiveConsent(userId: string, purposeId: string): Promise<boolean> {
  const latest = await db.consentRecords.findFirst({
    where: { userId, purpose: purposeId },
    orderBy: { timestamp: 'desc' },
  })
  return latest?.granted === true
}
```

## Right to Erasure (Soft Delete + Anonymization)

```typescript
const GRACE_PERIOD_DAYS = 30

async function requestAccountDeletion(userId: string): Promise<void> {
  await db.users.update({ where: { id: userId }, data: { status: 'deletion_pending', deactivatedAt: new Date() } })
  await db.deletionRequests.create({
    data: { userId, requestedAt: new Date(), gracePeriodEndsAt: new Date(Date.now() + GRACE_PERIOD_DAYS * 86400000), status: 'pending' },
  })
}

// Scheduled job: purge after grace period
async function purgeExpiredAccounts(): Promise<void> {
  const expired = await db.deletionRequests.findMany({
    where: { status: 'pending', gracePeriodEndsAt: { lte: new Date() } },
  })
  for (const req of expired) {
    await db.$transaction(async (tx) => {
      await tx.users.update({
        where: { id: req.userId },
        data: { email: `deleted-${req.userId}@anon.local`, fullName: 'Deleted User', phone: null, address: null, status: 'deleted' },
      })
      // Anonymize consent records (retain for legal proof, not delete)
      await tx.consentRecords.updateMany({
        where: { userId: req.userId },
        data: { userId: `deleted-${req.userId}`, ipAddress: 'REDACTED' }
      })
      await tx.orders.updateMany({ where: { userId: req.userId }, data: { userEmail: null, userName: 'Deleted User' } })
      await tx.deletionRequests.update({ where: { id: req.id }, data: { status: 'completed', completedAt: new Date() } })
    })
  }
}
```

## Cookie Consent Flow

```typescript
const COOKIE_CATEGORIES = {
  necessary: { name: 'Strictly Necessary', required: true },
  functional: { name: 'Functional', required: false },
  analytics: { name: 'Analytics', required: false },
  marketing: { name: 'Marketing', required: false },
} as const

type CookiePrefs = Record<keyof typeof COOKIE_CATEGORIES, boolean>

// BAD: set tracking cookies before consent
// document.cookie = '_ga=GA1.2.123; max-age=63072000'

// GOOD: only after explicit consent per category
function applyCookiePreferences(prefs: CookiePrefs): void {
  initSessionCookies() // always allowed
  prefs.analytics ? initGoogleAnalytics() : removeAnalyticsCookies()
  prefs.marketing ? initMarketingPixels() : removeMarketingCookies()
  document.cookie = `cookie_consent=${JSON.stringify(prefs)}; path=/; max-age=${365 * 86400}; SameSite=Lax; Secure`
}
```

## Data Breach Notification (72-Hour Rule)

```typescript
const NOTIFICATION_DEADLINE_HOURS = 72

async function reportBreach(breach: { detectedAt: Date; severity: string; affectedCount: number; dataTypes: string[]; description: string }): Promise<void> {
  const record = await db.dataBreaches.create({ data: { ...breach, notifiedAuthorityAt: null, notifiedUsersAt: null } })
  const deadline = new Date(breach.detectedAt.getTime() + NOTIFICATION_DEADLINE_HOURS * 3600000)

  // GDPR Art 33: notify authority within 72h | KVKK: "as soon as possible"
  await notifyDataProtectionAuthority({ breachId: record.id, deadline, ...breach })

  // GDPR Art 34: high-risk breaches require user notification
  if (breach.severity === 'high' || breach.severity === 'critical') {
    await notifyAffectedUsers(record.id)
  }
}
```

## Audit Logging (Who, What, When, Which Data)

```typescript
interface AuditLogEntry {
  actorId: string; actorRole: string
  action: 'read' | 'create' | 'update' | 'delete' | 'export'
  resourceType: string; resourceId: string
  fieldsAccessed: string[]; ipAddress: string
  justification?: string
}

async function logDataAccess(entry: AuditLogEntry): Promise<void> {
  // Append-only table - no UPDATE or DELETE allowed on audit_logs
  await db.$executeRaw`
    INSERT INTO audit_logs (actor_id, actor_role, action, resource_type, resource_id, fields_accessed, ip_address, justification, timestamp)
    VALUES (${entry.actorId}, ${entry.actorRole}, ${entry.action}, ${entry.resourceType}, ${entry.resourceId}, ${JSON.stringify(entry.fieldsAccessed)}, ${entry.ipAddress}, ${entry.justification || null}, NOW())
  `
}

// Express middleware: auto-log every personal data access
function auditMiddleware(resourceType: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const origJson = res.json.bind(res)
    res.json = (body: unknown) => {
      const actionMap: Record<string, string> = {
        GET: 'read', POST: 'create', PUT: 'update', PATCH: 'update', DELETE: 'delete'
      }
      logDataAccess({
        actorId: req.user?.id || 'anon',
        actorRole: req.user?.role || 'unknown',
        action: actionMap[req.method] || 'read',
        resourceType,
        resourceId: req.params.id || 'list',
        fieldsAccessed: Object.keys((body as Record<string, unknown>) || {}),
        ipAddress: req.ip || '',
      }).catch(console.error)
      return origJson(body)
    }
    next()
  }
}
```

## Privacy Policy Checklist

```
Controller identity    [ ] Company name, address, contact, VERBiS number
Data collected         [ ] Full list of categories with examples
Legal basis            [ ] Purpose + legal basis for each activity
Retention periods      [ ] How long each type is kept
Data subject rights    [ ] Access, rectification, erasure, portability, objection
Consent withdrawal     [ ] Clear opt-out instructions
Cookie policy          [ ] Categories, purposes, opt-out
International transfer [ ] Countries, safeguards (SCCs, adequacy)
Third parties          [ ] Processors and sub-processors
Automated decisions    [ ] Profiling details, right to object
Breach procedure       [ ] Notification timeline and method
DPO contact            [ ] Data Protection Officer details
```

## DPA Template Reference

Every third-party processor needs a Data Processing Agreement with these clauses:

```
Subject & duration      What data, how long, why
Processor obligations   Process only on documented instructions
Sub-processors          Prior written auth, flow-down obligations
Security measures       Encryption, access controls, incident response
Audit rights            Controller can inspect compliance
Data return/deletion    Return or destroy data at contract end
Breach notification     Notify controller without undue delay
International transfer  SCCs if data leaves TR/EU
```

## Contrast: GOOD vs BAD Consent

```typescript
// BAD: blanket consent - violates KVKK Art 3, GDPR Art 7
function BadForm() {
  return (
    <form>
      <label><input type="checkbox" /> I agree to privacy policy, marketing, tracking, and sharing.</label>
      <button>Sign Up</button>
    </form>
  )
}

// GOOD: granular opt-in per purpose
function GoodForm() {
  return (
    <form>
      <fieldset>
        <legend>Data Processing Consent</legend>
        <label><input type="checkbox" checked disabled /> Account operation (required)</label>
        <label><input type="checkbox" name="analytics" /> Usage analytics</label>
        <label><input type="checkbox" name="marketing" /> Marketing emails</label>
        <label><input type="checkbox" name="third_party" /> Partner sharing (<a href="/privacy">details</a>)</label>
      </fieldset>
      <p>Change preferences anytime in account settings.</p>
      <button>Sign Up</button>
    </form>
  )
}
```

**Core rule**: Compliance is not a one-time feature. Build data protection into every flow, log every access, and assume regulators will ask "show me the evidence."
