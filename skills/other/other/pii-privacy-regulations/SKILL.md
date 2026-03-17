---
name: "PII & Privacy Regulations Skill"
description: "Handling personally identifiable information under European and Australian privacy regulations."
applyTo: "**/*privacy*,**/*PII*,**/*personal*,**/*GDPR*,**/*data-protection*,**/*consent*,**/*user-data*"
---

# PII & Privacy Regulations Skill

> Handling personally identifiable information under European and Australian privacy regulations.

## ⚠️ Staleness Warning

Privacy regulations are actively evolving. Major changes expected.

**Refresh triggers:**

- GDPR enforcement updates or new guidelines
- Australian Privacy Act reform (ongoing review)
- New adequacy decisions for data transfers
- Significant enforcement actions or fines
- EU AI Act privacy provisions (2025-2026)

**Last validated:** February 2026

**Check current state:**
- EU: [GDPR.eu](https://gdpr.eu/), [EU Commission](https://commission.europa.eu/law/law-topic/data-protection_en)
- Australia: [OAIC](https://www.oaic.gov.au/privacy/australian-privacy-principles)

---

## What is PII?

Personally Identifiable Information (PII) is any data that can identify an individual directly or indirectly.

### Direct Identifiers

| Category | Examples |
| -------- | -------- |
| **Name** | Full name, maiden name, alias |
| **Government IDs** | SSN, passport, driver's license, TFN (AU) |
| **Financial** | Bank account, credit card numbers |
| **Contact** | Email, phone, physical address |
| **Biometric** | Fingerprints, facial recognition, voice |

### Indirect Identifiers (Quasi-identifiers)

| Category | Examples |
| -------- | -------- |
| **Location** | IP address, GPS coordinates, ZIP/postcode |
| **Device** | Device ID, MAC address, browser fingerprint |
| **Demographic** | Age, gender, ethnicity, occupation |
| **Behavioral** | Purchase history, browsing patterns |

> **Key insight:** Combining quasi-identifiers can uniquely identify individuals even without direct identifiers.

---

## 🇪🇺 GDPR (European Union)

**Applies to:** Any organization processing EU residents' data, regardless of location.

### Core Principles (Article 5)

| Principle | Requirement |
| --------- | ----------- |
| **Lawfulness, Fairness, Transparency** | Process data legally with clear communication |
| **Purpose Limitation** | Collect only for specified, legitimate purposes |
| **Data Minimization** | Collect only what's necessary |
| **Accuracy** | Keep data accurate and up to date |
| **Storage Limitation** | Retain only as long as necessary |
| **Integrity & Confidentiality** | Ensure appropriate security |
| **Accountability** | Demonstrate compliance |

### Lawful Bases for Processing

| Basis | When to Use |
| ----- | ----------- |
| **Consent** | Freely given, specific, informed, unambiguous |
| **Contract** | Necessary for contract performance |
| **Legal Obligation** | Required by law |
| **Vital Interests** | Protect someone's life |
| **Public Task** | Official authority or public interest |
| **Legitimate Interests** | Business need balanced against rights |

### Individual Rights (Data Subject Rights)

| Right | Description | Response Time |
| ----- | ----------- | ------------- |
| **Access** | Obtain copy of their data | 1 month |
| **Rectification** | Correct inaccurate data | 1 month |
| **Erasure** ("Right to be Forgotten") | Delete their data | 1 month |
| **Restrict Processing** | Limit how data is used | 1 month |
| **Data Portability** | Receive data in machine-readable format | 1 month |
| **Object** | Stop certain processing | Without delay |
| **Automated Decision-Making** | Human review of automated decisions | 1 month |

### GDPR Compliance Checklist

```markdown
## Lawful Basis & Transparency
- [ ] Document lawful basis for each processing activity
- [ ] Maintain records of processing activities (Article 30)
- [ ] Privacy policy is clear, accessible, updated

## Data Security
- [ ] Encryption at rest and in transit
- [ ] Pseudonymization where possible
- [ ] Data Protection Impact Assessment (DPIA) for high-risk processing
- [ ] Breach notification process (72 hours to authority)

## Governance
- [ ] Data Protection Officer (DPO) appointed if required
- [ ] Data Processing Agreements with third parties
- [ ] EU representative appointed (if outside EU)

## Individual Rights
- [ ] Process to handle access requests
- [ ] Process to handle deletion requests
- [ ] Process to handle data portability requests
- [ ] Consent mechanism (opt-in, not opt-out)
```

### 2025-2026 Updates

| Update | Impact |
| ------ | ------ |
| **Simplified Record-Keeping** (May 2025) | Organizations <750 employees only need records for high-risk processing |
| **Enhanced Enforcement Procedures** (June 2025) | Additional procedural rules for cross-border cases |
| **AI Act Integration** | Additional requirements for AI systems processing personal data |

---

## 🇦🇺 Australian Privacy Principles (APPs)

**Applies to:** Organizations with annual turnover >$3M AUD, government agencies, health service providers, and some others.

### The 13 APPs

| APP | Title | Key Requirement |
| --- | ----- | --------------- |
| **APP 1** | Open & Transparent Management | Have a clear, up-to-date privacy policy |
| **APP 2** | Anonymity & Pseudonymity | Allow anonymous/pseudonymous dealings where practical |
| **APP 3** | Collection of Solicited Information | Only collect necessary info; higher bar for sensitive info |
| **APP 4** | Unsolicited Personal Information | Assess and destroy if wouldn't have been collected |
| **APP 5** | Notification of Collection | Tell individuals what you're collecting and why |
| **APP 6** | Use or Disclosure | Only for primary purpose or permitted secondary purposes |
| **APP 7** | Direct Marketing | Opt-out required; sensitive info needs consent |
| **APP 8** | Cross-Border Disclosure | Ensure overseas recipients comply with APPs |
| **APP 9** | Government Identifiers | Don't adopt government IDs as your own identifier |
| **APP 10** | Quality of Information | Keep data accurate, complete, up to date |
| **APP 11** | Security of Information | Protect from misuse, loss, unauthorized access |
| **APP 12** | Access to Information | Provide access when requested |
| **APP 13** | Correction of Information | Correct inaccurate information |

### Sensitive Information (Higher Protection)

Under Australian law, sensitive information includes:

- Health information
- Genetic information
- Biometric data
- Racial or ethnic origin
- Political opinions
- Religious beliefs
- Sexual orientation
- Criminal record
- Trade union membership

> **Rule:** Sensitive information generally requires **consent** to collect.

### Notifiable Data Breaches (NDB) Scheme

**When to notify:**
- Unauthorized access, disclosure, or loss of personal information
- Likely to result in serious harm to individuals
- Remedial action hasn't prevented serious harm

**Timeline:**
- Notify OAIC and affected individuals **as soon as practicable**
- Assessment must be completed within **30 days**

### Australian Privacy Act Reform (Ongoing)

The Privacy Act is under review. Expected changes:

| Proposed Change | Status |
| --------------- | ------ |
| Expanded definition of personal information | Under review |
| New individual rights (erasure, explanation of AI decisions) | Proposed |
| Higher penalties | Enacted (up to $50M AUD) |
| Direct right of action for individuals | Under review |
| Removal of small business exemption | Under consideration |

---

## Cross-Jurisdictional Comparison

| Aspect | GDPR (EU) | APP (Australia) |
| ------ | --------- | --------------- |
| **Scope** | All organizations processing EU data | >$3M turnover + exceptions |
| **Consent** | Must be explicit opt-in | Can be implied in some cases |
| **Right to Erasure** | Explicit right | Not explicit (under review) |
| **Breach Notification** | 72 hours to authority | "As soon as practicable" |
| **Penalties** | Up to €20M or 4% global revenue | Up to $50M AUD |
| **Cross-Border Transfer** | Adequacy decisions, SCCs, BCRs | Must ensure APP compliance |
| **DPO Required** | Yes, in certain cases | No requirement |

---

## Code Implementation Patterns

### Never Log PII

```typescript
// ❌ BAD
logger.info(`User ${user.email} logged in from ${user.ipAddress}`);

// ✅ GOOD
logger.info(`User ${hashUserId(user.id)} logged in`);
```

### Encrypt PII at Rest

```typescript
// Encrypt before storing
const encryptedEmail = encrypt(user.email, encryptionKey);
await db.users.update({ id: user.id, email: encryptedEmail });

// Decrypt only when needed
const email = decrypt(storedUser.email, encryptionKey);
```

### Implement Data Minimization

```typescript
// ❌ BAD - Fetching everything
const user = await db.users.findById(id);
return user; // Contains PII you don't need

// ✅ GOOD - Select only needed fields
const user = await db.users.findById(id, {
  select: ['id', 'displayName', 'preferences']
});
return user;
```

### Consent Management

```typescript
interface ConsentRecord {
  userId: string;
  purpose: 'marketing' | 'analytics' | 'personalization';
  granted: boolean;
  timestamp: Date;
  source: 'web' | 'mobile' | 'api';
  version: string; // Privacy policy version
}

// Always check consent before processing
async function canProcess(userId: string, purpose: string): Promise<boolean> {
  const consent = await getLatestConsent(userId, purpose);
  return consent?.granted === true;
}
```

### Data Subject Request Handler

```typescript
interface DataSubjectRequest {
  type: 'access' | 'rectification' | 'erasure' | 'portability' | 'objection';
  userId: string;
  requestedAt: Date;
  deadline: Date; // 30 days for GDPR
  status: 'pending' | 'processing' | 'completed' | 'denied';
}

// Implement audit trail for all requests
async function handleDSR(request: DataSubjectRequest) {
  await auditLog.record({
    action: 'dsr_received',
    requestType: request.type,
    userId: request.userId,
    timestamp: new Date()
  });

  // Process based on type...
}
```

### Pseudonymization Pattern

```typescript
// Replace direct identifiers with tokens
function pseudonymize(record: UserRecord): PseudonymizedRecord {
  return {
    pseudoId: generateToken(record.id), // Reversible with key
    ageGroup: getAgeGroup(record.birthDate), // 18-25, 26-35, etc.
    region: record.country, // Keep general location
    // Omit: name, email, exact address, etc.
  };
}
```

---

## Compliance Checklist

### For New Projects

```markdown
## Privacy Impact Assessment
- [ ] What PII will be collected?
- [ ] What is the lawful basis (GDPR) / primary purpose (APP)?
- [ ] Is all collected data necessary? (data minimization)
- [ ] How long will data be retained?
- [ ] Who will have access?
- [ ] Will data cross borders?
- [ ] What security measures are in place?

## Technical Implementation
- [ ] PII encrypted at rest
- [ ] PII encrypted in transit (TLS 1.2+)
- [ ] Logging excludes PII
- [ ] Consent captured before processing
- [ ] Data subject request endpoints implemented
- [ ] Retention/deletion automation in place
- [ ] Audit logging for PII access
```

---

## Quick Reference: When Processing is Prohibited

| Scenario | GDPR | APP |
| -------- | ---- | --- |
| No lawful basis identified | ❌ | ❌ |
| Sensitive data without explicit consent | ❌ | ❌ |
| Marketing without opt-out option | ❌ | ❌ |
| Cross-border transfer without safeguards | ❌ | ❌ |
| Retention beyond stated period | ❌ | ❌ |
| Collection beyond stated purpose | ❌ | ❌ |

---

## Resources

### Official
- [GDPR Full Text](https://gdpr.eu/tag/gdpr/)
- [EU Commission Data Protection](https://commission.europa.eu/law/law-topic/data-protection_en)
- [OAIC Australian Privacy Principles](https://www.oaic.gov.au/privacy/australian-privacy-principles)
- [OAIC Privacy Act](https://www.oaic.gov.au/privacy/privacy-legislation/the-privacy-act)

### Tools
- Data Protection Impact Assessment templates
- Consent management platforms
- Data discovery and classification tools

---

## Synapses

See [synapses.json](synapses.json) for connections.
