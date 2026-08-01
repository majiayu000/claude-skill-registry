---
name: threat-modeling
description: 'Use when implementing auth, file uploads, payments, or external APIs.
  Applies STRIDE framework systematically. Triggers: "authentication", "file upload",
  "payment", "multi-tenant", "external API". If'
---

---
name: threat-modeling
description: Use when implementing auth, file uploads, payments, or external APIs. Applies STRIDE framework systematically. Triggers: "authentication", "file upload", "payment", "multi-tenant", "external API". If thinking "I know security" - use this anyway.
---

# Threat Modeling

## MANDATORY FIRST STEP

**TodoWrite:** Create 18+ items (6 STRIDE categories × 3 items each)
- Define assets/entry points
- Enumerate threats per STRIDE category
- Risk scoring
- Identify controls
- Document threat model
- Verification checkpoint

---

## Quick-Start Templates

### Authentication Feature

**Assets:** User credentials, session tokens, reset tokens
**Entry points:** Login, signup, password reset endpoints

**STRIDE Focus:**
| Threat | Check |
|--------|-------|
| Spoofing | Credential stuffing protection? Rate limiting? |
| Tampering | Token manipulation? Secure cookies? |
| Repudiation | Login attempt logging? |
| Info Disclosure | Token leakage? Error messages reveal info? |
| DoS | Rate limiting? Account lockout? |
| EoP | Session hijacking? Privilege escalation? |

### File Upload Feature

**Assets:** Stored files, file metadata, server filesystem
**Entry points:** Upload endpoint, file retrieval

**STRIDE Focus:**
| Threat | Check |
|--------|-------|
| Spoofing | Impersonate uploader? |
| Tampering | Malicious files? Path traversal? |
| Repudiation | Upload logging? |
| Info Disclosure | Access others' files? |
| DoS | Large file attacks? |
| EoP | Execute uploaded code? |

### Multi-Tenant API

**Assets:** Tenant data, API endpoints, configurations
**Entry points:** All endpoints with tenant context

**STRIDE Focus:**
| Threat | Check |
|--------|-------|
| Info Disclosure | Cross-tenant data leakage? |
| EoP | Access other tenant's data? |
| Tampering | Modify tenant_id in requests? |
| Spoofing | Impersonate other tenant? |

---

## STRIDE Process

Apply each category systematically (S→T→R→I→D→E):
1. **S**poofing: Can attacker impersonate?
2. **T**ampering: Can attacker modify data/code?
3. **R**epudiation: Can attacker deny actions?
4. **I**nformation Disclosure: Can attacker access secrets?
5. **D**enial of Service: Can attacker disrupt?
6. **E**levation of Privilege: Can attacker gain unauthorized access?

**Risk Scoring:** Likelihood (1-5) × Impact (1-5)
- 15-25: Critical (address immediately)
- 6-14: High (before release)
- 1-5: Low (track)

---

## Verification Checkpoint

Before marking complete, verify 3 specifics:
1. ✅ Each STRIDE category has ≥2 concrete threats identified
2. ✅ All high-risk (score ≥6) threats have controls documented
3. ✅ Threat model includes data flow diagram with trust boundaries

---

## Response Templates

**"This is over-engineering for a simple feature"**
> Security bugs cost 30x more post-release than during design. STRIDE takes 15-30 minutes and prevents deployment blockers. Which STRIDE categories don't apply to this feature?

---

## Red Flags

| Thought | Reality |
|---------|---------|
| "Ad-hoc brainstorming is faster" | Misses 60% of threats |
| "Everything is critical" | No risk prioritization = wrong fixes |
| "We'll security review later" | 30x more expensive post-implementation |
