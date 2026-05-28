---
name: reverse-engineer
description: |
  Reverse engineer existing code into SDD specification documents.
  Use when: analyzing legacy code, documenting undocumented systems, creating specs from existing implementations.
  Keywords: reverse engineering, legacy code, documentation, spec extraction, code archaeology, 反向工程, 舊有程式碼, 規格提取.
---

# Reverse Engineering to SDD Specification Guide

> **Language**: English | [繁體中文](../../../locales/zh-TW/skills/claude-code/reverse-engineer/SKILL.md)

**Version**: 1.1.0
**Last Updated**: 2026-01-19
**Applicability**: Claude Code Skills

> **Core Standard**: This skill implements [Reverse Engineering Standards](../../../core/reverse-engineering-standards.md). For comprehensive methodology documentation accessible by any AI tool, refer to the core standard.

---

## Purpose

This skill guides you through reverse engineering existing code into SDD (Spec-Driven Development) specification documents, with strict adherence to Anti-Hallucination standards.

## Quick Reference

### Reverse Engineering Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│              Reverse Engineering Workflow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  Code Analysis (AI Automated)                              │
│      ├─ Scan code structure, APIs, data models                 │
│      ├─ Parse existing tests for acceptance criteria           │
│      └─ Generate draft spec (with uncertainty labels)          │
│                                                                 │
│  2️⃣  Human Input (Required)                                    │
│      ├─ Write Motivation (why this feature exists)             │
│      ├─ Add Risk Assessment                                    │
│      └─ Verify dependencies and business context               │
│                                                                 │
│  3️⃣  Review & Confirm                                          │
│      ├─ Discuss with stakeholders                              │
│      └─ Confirm [Confirmed] / [Inferred] / [Unknown] labels    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### What Can vs Cannot Be Extracted

| Aspect | Extractable | Certainty | Notes |
|--------|-------------|-----------|-------|
| **API Endpoints** | ✅ Yes | [Confirmed] | Route definitions, HTTP methods |
| **Data Models** | ✅ Yes | [Confirmed] | Types, interfaces, schemas |
| **Function Signatures** | ✅ Yes | [Confirmed] | Parameters, return types |
| **Test Cases** | ✅ Yes | [Confirmed] | → Acceptance Criteria |
| **Dependencies** | ✅ Yes | [Confirmed] | Package references |
| **Behavior Patterns** | ⚠️ Partial | [Inferred] | From code analysis |
| **Motivation/Why** | ❌ No | [Unknown] | Needs human input |
| **Business Context** | ❌ No | [Unknown] | Needs human input |
| **Risk Assessment** | ❌ No | [Unknown] | Needs domain expertise |
| **Trade-off Decisions** | ❌ No | [Unknown] | Historical context missing |

## Core Principles

### 1. Anti-Hallucination Compliance

**CRITICAL**: This skill MUST strictly follow [Anti-Hallucination Standards](../../../core/anti-hallucination.md).

#### Certainty Labels

| Tag | Use When | Example |
|-----|----------|---------|
| `[Confirmed]` | Direct evidence from code/tests | API endpoint at `src/api/users.ts:15` |
| `[Inferred]` | Logical deduction from patterns | "Likely uses dependency injection based on constructor pattern" |
| `[Unknown]` | Cannot determine from code | Motivation, business requirements |
| `[Need Confirmation]` | Requires human verification | Design intent, edge case handling |

#### Source Attribution

Every extracted item MUST include source attribution:

```markdown
## API Design

### User Authentication
[Confirmed] POST /api/auth/login endpoint accepts email and password
- [Source: Code] src/controllers/AuthController.ts:25-45
- [Source: Code] src/routes/auth.ts:8

### Session Management
[Inferred] Sessions expire after 24 hours based on JWT expiry configuration
- [Source: Code] src/config/auth.ts:12 - TOKEN_EXPIRY=86400
- [Source: Knowledge] Standard JWT expiry interpretation (⚠️ Verify intent)
```

### 2. Progressive Disclosure

Start with high-level architecture, then drill down:

1. **System Overview**: Entry points, main components
2. **Component Details**: Individual modules, their responsibilities
3. **Implementation Specifics**: Algorithms, data flows

### 3. Test-to-Requirement Mapping

Extract acceptance criteria from tests:

```javascript
// Test file: src/tests/auth.test.ts
describe('Authentication', () => {
  it('should return 401 for invalid credentials', () => {...});
  it('should issue JWT token on successful login', () => {...});
  it('should refresh token before expiry', () => {...});
});
```

Becomes:

```markdown
## Acceptance Criteria
[Inferred] From test analysis (src/tests/auth.test.ts):
- [ ] Return 401 status code for invalid credentials
- [ ] Issue JWT token on successful login
- [ ] Support token refresh before expiry
```

## Workflow Stages

### Stage 1: Code Scanning

**Input**: File path or directory
**Output**: Code structure analysis

**Actions**:
1. Identify entry points (main functions, API routes, event handlers)
2. Map module dependencies
3. Extract type definitions and interfaces
4. List configuration sources

### Stage 2: Test Analysis

**Input**: Test files
**Output**: Acceptance criteria candidates

**Actions**:
1. Parse test case names
2. Extract Given-When-Then patterns (if BDD-style)
3. Identify boundary conditions
4. Note coverage gaps

### Stage 3: Gap Identification

**Input**: Code + test analysis
**Output**: List of unknowns requiring human input

**Required Human Input**:
- [ ] Motivation: Why was this feature built?
- [ ] User Story: Who uses this and for what purpose?
- [ ] Risks: What could go wrong?
- [ ] Trade-offs: Why this approach over alternatives?
- [ ] Out of Scope: What was explicitly excluded?

### Stage 4: Spec Generation

**Input**: All analysis results
**Output**: Draft specification document

**Template**: Use [reverse-spec-template.md](../../../templates/reverse-spec-template.md)

### Stage 5: Human Review

**Input**: Draft specification
**Output**: Validated specification

**Review Checklist**:
- [ ] All `[Confirmed]` items verified accurate
- [ ] All `[Inferred]` items validated or corrected
- [ ] All `[Unknown]` items filled in by human
- [ ] Source citations checked
- [ ] Business context added

## Examples

### Example 1: API Endpoint Extraction

**Input Code** (`src/controllers/UserController.ts`):
```typescript
export class UserController {
  @Get('/users/:id')
  @Authorize('admin', 'user')
  async getUser(@Param('id') id: string): Promise<User> {
    return this.userService.findById(id);
  }
}
```

**Extracted Specification**:
```markdown
## API Endpoints

### GET /users/:id
[Confirmed] Retrieves a user by ID
- [Source: Code] src/controllers/UserController.ts:3-7

**Authorization**: [Confirmed] Requires 'admin' or 'user' role
- [Source: Code] @Authorize decorator at line 4

**Parameters**:
- `id` (path, required): User identifier [Confirmed]

**Response**: [Confirmed] Returns User object
- [Source: Code] Return type at line 5

**Error Handling**: [Unknown] Error responses not evident from code
```

### Example 2: Test-to-Criteria Extraction

**Input Test** (`src/tests/cart.test.ts`):
```typescript
describe('Shopping Cart', () => {
  it('should add item to empty cart', () => {...});
  it('should increment quantity for duplicate items', () => {...});
  it('should not exceed maximum quantity of 99', () => {...});
  it('should calculate total with tax', () => {...});
});
```

**Extracted Acceptance Criteria**:
```markdown
## Acceptance Criteria

[Inferred] From test analysis (src/tests/cart.test.ts):
- [ ] Can add item to empty cart (line 2)
- [ ] Increments quantity for duplicate items (line 3)
- [ ] Maximum quantity limit: 99 items (line 4)
- [ ] Total calculation includes tax (line 5)

[Unknown] Tax calculation rules not specified in tests
[Need Confirmation] What happens when cart exceeds 99 items? (reject or cap?)
```

## Integration with Other Skills

### With /spec (Spec-Driven Development)

1. Generate reverse-engineered spec using `/reverse-spec`
2. Review and fill in `[Unknown]` sections
3. Use `/spec review` to validate completeness
4. Proceed with normal SDD workflow for enhancements

### With /tdd (Test-Driven Development)

1. Extract existing test patterns
2. Identify test coverage gaps
3. Use `/tdd` to add missing tests
4. Update spec with new acceptance criteria

### With /bdd (Behavior-Driven Development)

1. Convert extracted acceptance criteria to Gherkin format
2. Use `/bdd` to formalize scenarios
3. Validate scenarios with stakeholders

## Complete Reverse Engineering Pipeline

The reverse engineering skill supports a complete SDD → BDD → TDD pipeline:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   Complete Reverse Engineering Pipeline                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Code + Tests                                                          │
│        │                                                                │
│        ▼                                                                │
│   /reverse-spec                                                         │
│        │                                                                │
│        └─→ Generate SPEC-XXX with Acceptance Criteria                   │
│                │                                                        │
│                ▼                                                        │
│   /reverse-bdd                                                          │
│        │                                                                │
│        ├─→ AC → Gherkin scenario conversion                             │
│        ├─→ Auto-transform bullet points to Given-When-Then              │
│        └─→ Generate .feature files                                      │
│                │                                                        │
│                ▼                                                        │
│   /reverse-tdd                                                          │
│        │                                                                │
│        ├─→ Analyze existing unit tests                                  │
│        └─→ Generate coverage report with gaps                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Pipeline Commands

| Command | Input | Output | Purpose |
|---------|-------|--------|---------|
| `/reverse-spec` | Code directory | SPEC-XXX.md | Extract requirements from code |
| `/reverse-bdd` | SPEC file | .feature files | Convert AC to Gherkin scenarios |
| `/reverse-tdd` | .feature files | Coverage report | Map scenarios to unit tests |

### Usage Example

```bash
# Step 1: Reverse engineer code to SDD specification
/reverse-spec src/auth/

# Step 2: Transform acceptance criteria to BDD scenarios
/reverse-bdd specs/SPEC-AUTH.md

# Step 3: Analyze test coverage against BDD scenarios
/reverse-tdd features/auth.feature
```

### Detailed Guides

- [BDD Extraction Workflow](./bdd-extraction.md) - Detailed guide for AC → Gherkin transformation
- [TDD Analysis Workflow](./tdd-analysis.md) - Detailed guide for BDD → TDD coverage analysis

## Anti-Patterns to Avoid

### ❌ Don't Do This

1. **Fabricating Motivation**
   - Wrong: "This feature was built to improve user experience"
   - Right: "[Unknown] Motivation requires human input"

2. **Assuming Requirements**
   - Wrong: "The system requires SSO support"
   - Right: "[Need Confirmation] SSO configuration found in code - is this a requirement?"

3. **Speculating About Unread Code**
   - Wrong: "The PaymentService handles Stripe integration"
   - Right: "[Unknown] PaymentService functionality - need to read src/services/PaymentService.ts"

4. **Presenting Options Without Uncertainty**
   - Wrong: "The code uses Redis for caching"
   - Right: "[Confirmed] Redis client configured in src/config/cache.ts:5"

## Best Practices

### Do's

- ✅ Read all relevant files before making claims
- ✅ Tag every statement with certainty level
- ✅ Include source citations with file:line
- ✅ Clearly list what needs human input
- ✅ Preserve original code comments as context

### Don'ts

- ❌ Assume motivation or business context
- ❌ Present inferences as confirmed facts
- ❌ Skip source attribution
- ❌ Generate specs for unread code
- ❌ Fill in `[Unknown]` sections without human input

---

## Configuration Detection

This skill auto-detects project configuration:

1. Check for existing `specs/` directory
2. Check for SDD tooling (OpenSpec, Spec Kit)
3. Detect test framework for acceptance criteria extraction
4. Identify code patterns (MVC, DDD, etc.)

---

## Related Standards

- [Reverse Engineering Standards](../../../core/reverse-engineering-standards.md) - **Core methodology standard (primary reference)**
- [Spec-Driven Development](../../../core/spec-driven-development.md) - Output format and review process
- [Anti-Hallucination Guidelines](../../../core/anti-hallucination.md) - Evidence-based analysis requirements
- [Code Review Checklist](../../../core/code-review-checklist.md) - Review guidelines

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-19 | Add BDD/TDD pipeline integration; Add core standard reference |
| 1.0.0 | 2026-01-19 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
