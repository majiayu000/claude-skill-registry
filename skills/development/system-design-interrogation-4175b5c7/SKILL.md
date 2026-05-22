---
name: system-design-interrogation
description: Use when planning system architecture to ensure nothing is missed. Provides structured questions covering scalability, security, data, and operational dimensions before implementation.
version: 1.0.0
---

# System Design Interrogation

## The Problem

Rushing to implementation without systematic design thinking leads to:
- Scalability issues discovered too late
- Security holes from missing tenant isolation
- Data model mismatches
- Frontend/backend contract conflicts
- Poor user experience

## The Solution: Question Before Implementing

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    SYSTEM DESIGN INTERROGATION                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│                        ┌─────────────┐                                     │
│                        │   FEATURE   │                                     │
│                        │   REQUEST   │                                     │
│                        └──────┬──────┘                                     │
│                               │                                            │
│    ┌──────────────────────────┼──────────────────────────┐                │
│    │                          │                          │                │
│    ▼                          ▼                          ▼                │
│  ┌────────┐             ┌────────┐              ┌────────┐               │
│  │ SCALE  │             │  DATA  │              │SECURITY│               │
│  └───┬────┘             └───┬────┘              └───┬────┘               │
│      │                      │                       │                     │
│  • Users?               • Where?               • Who access?              │
│  • Volume?              • Pattern?             • Isolation?               │
│  • Growth?              • Search?              • Attacks?                 │
│      │                      │                       │                     │
│      └──────────────────────┼───────────────────────┘                     │
│                             │                                             │
│    ┌────────────────────────┼────────────────────────┐                   │
│    │                        │                        │                   │
│    ▼                        ▼                        ▼                   │
│  ┌────────┐           ┌──────────┐            ┌────────┐                │
│  │   UX   │           │COHERENCE │            │ TRADE- │                │
│  └───┬────┘           └────┬─────┘            │  OFFS  │                │
│      │                     │                  └───┬────┘                │
│  • Latency?           • Contracts?           • Speed?                    │
│  • Feedback?          • Types?               • Quality?                  │
│  • Errors?            • API?                 • Cost?                     │
│      │                     │                      │                      │
│      └─────────────────────┴──────────────────────┘                      │
│                             │                                             │
│                             ▼                                             │
│                     ┌───────────────┐                                    │
│                     │ IMPLEMENTATION│                                    │
│                     │    READY      │                                    │
│                     └───────────────┘                                    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

## The Five Dimensions

### 1. Scale

**Key Questions:**
- How many users/tenants will use this?
- What's the expected data volume (now and in 1 year)?
- What's the request rate? Read-heavy or write-heavy?
- Does complexity grow linearly or exponentially with data?
- What happens at 10x current load? 100x?

**SkillForge Example:**
```
Feature: "Add document tagging"
- Users: 1000 active users
- Documents per user: ~50 average
- Tags per document: 3-5
- Total tags: 50,000 → 500,000
- Access: Read-heavy (10:1 read:write)
- Search: Need tag autocomplete (prefix search)
```

### 2. Data

**Key Questions:**
- Where does this data naturally belong?
- What's the primary access pattern?
- Is it master data or transactional?
- What's the retention policy?
- Does it need to be searchable? How?

**SkillForge Example:**
```
Feature: "Add document tagging"
- Data: Tags belong WITH documents (denormalized) or separate table?
- Pattern: Get tags for document (by doc_id), get documents by tag
- Storage: PostgreSQL (relational) or add to document JSON?
- Search: Full-text for tag names, filter by tag for documents
- Decision: Separate `tags` table with many-to-many join
```

### 3. Security

**Key Questions:**
- Who can access this data/feature?
- How is tenant isolation enforced?
- What happens if authorization fails?
- What attack vectors does this introduce?
- Is there PII involved?

**SkillForge Example:**
```
Feature: "Add document tagging"
- Access: User can only see/manage their own tags
- Isolation: All tag queries MUST include tenant_id filter
- AuthZ: Check user owns document before tagging
- Attacks: Tag injection? Limit tag length, sanitize input
- PII: Tags might contain PII → treat as sensitive
```

### 4. UX Impact

**Key Questions:**
- What's the expected latency for this operation?
- What feedback does the user get during the operation?
- What happens on failure? Can they retry?
- Is there optimistic UI possible?
- How does this affect the overall workflow?

**SkillForge Example:**
```
Feature: "Add document tagging"
- Latency: < 100ms for add/remove tag
- Feedback: Optimistic update, show tag immediately
- Failure: Rollback tag, show error toast
- Optimistic: Yes - add tag to UI before server confirms
- Workflow: Tags should be inline editable, no modal
```

### 5. Coherence

**Key Questions:**
- Which layers does this touch?
- What contracts/interfaces change?
- Are types consistent frontend ↔ backend?
- Does this break existing clients?
- How does this affect the API?

**SkillForge Example:**
```
Feature: "Add document tagging"
- Layers: DB → Backend API → Frontend UI → State
- Contracts: Document type needs `tags: Tag[]` field
- Types: Tag = { id: UUID, name: string, color?: string }
- Breaking: No - additive change to Document response
- API: POST /documents/{id}/tags, DELETE /documents/{id}/tags/{tag_id}
```

## The Process

### Before Writing Any Code

1. **State the Feature** - One sentence description
2. **Run Through 5 Dimensions** - Answer key questions for each
3. **Identify Trade-offs** - Speed vs quality, complexity vs flexibility
4. **Document Decisions** - Record answers in design doc or issue
5. **Review with Team** - Get alignment before implementing

### Quick Assessment Template

```markdown
## Feature: [Name]

### Scale
- Users:
- Data volume:
- Access pattern:
- Growth projection:

### Data
- Storage location:
- Schema changes:
- Search requirements:
- Retention:

### Security
- Authorization:
- Tenant isolation:
- Attack surface:
- PII handling:

### UX
- Target latency:
- Feedback mechanism:
- Error handling:
- Optimistic updates:

### Coherence
- Affected layers:
- Type changes:
- API changes:
- Breaking changes:

### Decision
[Final approach with rationale]
```

## Integration with SkillForge Workflow

### In Brainstorming Phase

Before implementation, run system design interrogation:

```
/brainstorm → System Design Questions → Implementation Plan
```

### In Code Review

Reviewer should verify:
- Scale considerations documented
- Security layer covered
- Types consistent across stack
- UX states handled

### In Testing

Tests should cover:
- Scale: Load tests for expected volume
- Security: Tenant isolation tests
- Coherence: Integration tests across layers
- UX: Error state tests

## Anti-Patterns

```
❌ "I'll add an index later if it's slow"
   → Ask: What's the expected query pattern NOW?

❌ "We can add tenant filtering in a future PR"
   → Ask: How is isolation enforced from DAY ONE?

❌ "The frontend can handle any response shape"
   → Ask: What's the TypeScript type for this?

❌ "Users won't do that"
   → Ask: What's the attack vector? What if they DO?

❌ "It's just a small feature"
   → Ask: How does this grow with 100x users?
```

## Quick Reference Card

| Dimension | Key Question | Red Flag |
|-----------|--------------|----------|
| Scale | How many? | "All users" |
| Data | Where stored? | "I'll figure it out" |
| Security | Who can access? | "Everyone" |
| UX | What's the latency? | "It'll be fast" |
| Coherence | What types change? | "No changes needed" |

---

**Version:** 1.0.0 (December 2025)
