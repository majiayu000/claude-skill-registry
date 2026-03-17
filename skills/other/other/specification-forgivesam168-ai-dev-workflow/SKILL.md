---
name: specification
description: 'Generate comprehensive specification documents (PRD/Spec). Use when asked to "write spec", "create PRD", "document requirements", "user stories", "acceptance criteria", "產生規格", "寫需求文件", "specifications", or transforming brainstorm results into formal structured requirements for features.'
license: See LICENSE.txt in repository root
---

# Specification (PRD/Spec Generator)

> 💡 **Recommended Agent**: `spec-agent` (Specification Specialist)
> - **CLI**: Input `/agent` and select `spec-agent`
> - **VS Code**: Use `@workspace #spec-agent` in Chat

## When to Use This Skill

Use this skill when:
- After brainstorming session is complete
- Transforming clarified requirements into formal specification
- Need structured, testable requirements documentation
- Before creating implementation plan
- 完成 brainstorm 後要產生正式規格文件
- 需要將想法轉換為可測試的需求

## Prerequisites

**Required**: `01-brainstorm.md` should exist with:
- Clear problem statement
- Chosen solution approach
- Key decisions documented

**Optional**: Can generate spec without brainstorm, but will need to ask more clarifying questions

## Step-by-Step Workflow

### Step 1: Clarifying Questions

If not already covered in brainstorm, ask about:

**Problem & Users**:
- What specific problem are we solving?
- Who are the target users?
- What are their pain points?

**Scope & Boundaries**:
- What are the **goals** (must-have features)?
- What are the **non-goals** (explicitly excluded)?
- What is the MVP scope vs future enhancements?

**Technical Constraints**:
- Security requirements (auth, data protection)
- Performance requirements (latency, throughput)
- Schema/API contract requirements
- Integration points with existing systems

**Financial Systems Specific**:
- Money handling: precision requirements (decimal places)
- Storage format: integer minor units or decimal string?
- Idempotency: which operations must be idempotent?
- Audit trail: what needs to be logged?
- Timezone: how to handle date/time?

### Step 2: Generate Structured Spec

Create `changes/<YYYY-MM-DD>-<slug>/03-spec.md` with the following structure:

---

**Template**:

```markdown
# Specification: {Feature Name}

## Overview
{Brief 2-3 sentence description of what this feature does and why it matters}

## Context
{Background information, related systems, and why this is needed now}

## Goals
Primary objectives and business value:
1. {Goal 1: e.g., "Enable users to export transaction history"}
2. {Goal 2: e.g., "Improve reporting speed by 50%"}
3. {Goal 3}

## Non-Goals
Explicitly excluded from this implementation:
- {Non-goal 1: e.g., "Real-time streaming (future enhancement)"}
- {Non-goal 2: e.g., "Support for legacy file formats"}

## User Stories

### Story 1: {Actor} wants to {Action}
**As a** {user role}
**I want** {capability}
**So that** {benefit}

**Acceptance Criteria**:
- [ ] {Testable criterion 1}
- [ ] {Testable criterion 2}
- [ ] {Testable criterion 3}

**Edge Cases**:
- {Edge case 1 and how to handle it}
- {Edge case 2}

---

### Story 2: {Title}
{Repeat structure}

---

## Functional Requirements

### FR-1: {Requirement Title}
**Description**: {Detailed description}
**Priority**: Must-Have / Should-Have / Nice-to-Have
**Dependencies**: {Other FRs or systems this depends on}

### FR-2: {Title}
{Repeat structure}

---

## Technical Considerations

### Security
- **Authentication**: {How users are authenticated}
- **Authorization**: {Who can access what}
- **Data Protection**: {Encryption, PII handling}
- **Input Validation**: {What inputs are validated and how}

### Performance
- **Latency**: {Expected response times}
- **Throughput**: {Requests per second}
- **Scalability**: {How this scales with load}

### API/Schema Contracts
- **Endpoints**: {List of API endpoints or contract references}
- **Data Models**: {Key entities and their relationships}
- **Versioning**: {How breaking changes are handled}

### Financial Systems Requirements (if applicable)
- **Money Precision**: Use `decimal` with {X} decimal places OR store as integer minor units (e.g., cents)
- **Currency**: Explicitly store currency code (ISO 4217)
- **Idempotency**: {Which operations support Idempotency-Key header}
- **Audit Trail**: {What events are logged and where}
- **Timezone**: Store timestamps in UTC, display in user timezone

---

## Data Model (if applicable)

### Entity: {EntityName}
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Unique identifier |
| `amount` | Decimal(19,4) | Yes | Transaction amount |
| `currency` | String(3) | Yes | ISO 4217 currency code |
| `createdAt` | DateTime (UTC) | Yes | Creation timestamp |

{Additional entities}

---

## API Contracts (if applicable)

### POST /api/v1/{resource}
**Request**:
```json
{
  "field1": "value",
  "field2": 123
}
```

**Response (200 OK)**:
```json
{
  "id": "uuid",
  "status": "created"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input
- `409 Conflict`: Duplicate idempotency key
- `422 Unprocessable Entity`: Business rule violation

---

## Success Metrics
How we measure if this feature is successful:
1. {Metric 1: e.g., "Export usage increases by 30%"}
2. {Metric 2: e.g., "Support tickets for reporting decrease by 50%"}
3. {Metric 3}

## Open Questions
Items requiring further clarification before implementation:
1. {Question 1}
2. {Question 2}

## References
- Brainstorm: `01-brainstorm.md`
- Decision Log: `02-decision-log.md`
- Related ADRs: {Links if applicable}
```

---

### Step 3: Validation

Ensure the spec meets quality criteria:

**Completeness Checklist**:
- [ ] All user stories have acceptance criteria
- [ ] Edge cases and error scenarios are covered
- [ ] Security requirements are explicit
- [ ] Performance requirements are defined
- [ ] API/schema contracts are documented (if applicable)
- [ ] Financial requirements specify precision (if applicable)
- [ ] Success metrics are measurable

**Testability Check**:
- Can a junior developer implement this without asking clarifying questions?
- Are acceptance criteria explicit and testable?
- Are error conditions and edge cases documented?

**Financial Systems Check** (if applicable):
- ✅ Money uses `decimal` or integer minor units (NO float/double)
- ✅ Currency is explicitly stored
- ✅ Idempotency requirements documented
- ✅ Audit trail requirements defined
- ✅ Timezone handling specified

## Output Template

The generated `03-spec.md` should be:
- **Readable**: A junior developer can understand it
- **Testable**: Every requirement has acceptance criteria
- **Complete**: Covers happy path, edge cases, and errors
- **Traceable**: Links back to brainstorm and decision log

## Quality Criteria

**Must Have**:
- ✅ User stories with acceptance criteria
- ✅ Functional requirements prioritized
- ✅ Security and performance considerations
- ✅ Error handling and edge cases documented

**Financial Systems Must Have**:
- ✅ Money precision specified (NO floats)
- ✅ Idempotency documented for transactions
- ✅ Audit trail requirements defined

**Nice to Have**:
- API contracts with request/response examples
- Data model diagrams
- Sequence diagrams for complex flows

## Next Step

After spec completion:

**CLI**:
```
Input: "幫我規劃實作計畫"
[System loads implementation-planning skill]
→ /agent → Select plan-agent
→ Generate 04-plan.md
```

**VS Code**:
```
Input: /create-plan
Or use: "create implementation plan"
```

Or use workflow orchestrator:
```
Input: "what's next?"
[System detects spec complete, recommends plan stage]
```

## Troubleshooting

### "I don't have brainstorm.md yet"
**Solution**: Either:
1. Run brainstorming first (recommended): "開始 brainstorming"
2. Proceed without it (agent will ask more questions)

### "The spec is too vague"
**Solution**: Add more acceptance criteria to user stories. Each criterion should be testable (pass/fail).

### "How detailed should the spec be?"
**Solution**: Detailed enough that:
- A junior developer can implement without confusion
- Acceptance criteria are testable
- But not so detailed that it prescribes implementation (that's for plan stage)

### "Should I include diagrams?"
**Solution**: 
- **Yes**: For complex data flows, state machines, or multi-system integrations
- **No**: For simple CRUD operations or straightforward features
- Use tools like Excalidraw or Mermaid for quick diagrams

## Financial Systems Best Practices

### Money Handling
**DON'T**:
```csharp
double price = 19.99; // ❌ Floating point = rounding errors
```

**DO**:
```csharp
// Option 1: Decimal
decimal price = 19.99M;

// Option 2: Integer minor units
int priceInCents = 1999; // Store cents, display as $19.99
string currency = "USD";
```

### Idempotency
For transactional endpoints, specify:
```
POST /api/v1/transactions
Header: Idempotency-Key: {unique-uuid}

Behavior:
- First request: Process transaction
- Repeat request (same key): Return original result (no duplicate)
- Different key: Process as new transaction
```

### Audit Trail
Document what events to log:
- Transaction created/updated/deleted
- User: who performed action
- Timestamp: when (UTC)
- IP/correlation-id: traceability

## Related Documentation

- [Brainstorming Skill](../brainstorming/SKILL.md) - Previous stage
- [Implementation Planning Skill](../implementation-planning/SKILL.md) - Next stage
- [WORKFLOW.md](../../WORKFLOW.md) - Overall workflow
- [API Design Instructions](../../instructions/api-design.instructions.md) - Financial API standards

---

💡 **Tip**: A good spec is complete when you can hand it to a developer and they don't need to ask clarifying questions.
