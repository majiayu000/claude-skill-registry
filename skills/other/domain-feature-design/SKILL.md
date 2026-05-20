---
name: domain-feature-design
description: Guides agents through proper domain/feature design following Organon methodology. Ensures RFCs contain both organon mutation plan (ETHOS.md, PHILOSOPHY.md content) AND technical implementation plan (architecture, API, phases). Prevents common mistake of writing only technical plan or only organon plan. Use when designing new domains, features, or significant capabilities that require organon evolution.
protocol_id: PROTO-ORG-1
protocol_file: organon/protocols/PROTOCOLS.md
tools: [organon-validate, organon-verify]
loads:
  - book-llms/patterns.md
  - book-llms/templates.md
  - book-llms/scopes.md
  - book-llms/frontmatter-system.md
  - CLAUDE.md
context: fork
agent: general-purpose
---

# Domain/Feature Design Skill

> A Claude skill for properly designing new domains and features using RFC-Driven Evolution — ensures organon defines "should be" before code implements "what is."

---

## When to Use This Skill

Use this skill when:
- **Adding a new domain** to a product (bounded context with its own organon)
- **Adding a new feature** (cross-cutting capability)
- **Proposing significant changes** that require organon evolution
- **Reviewing domain/feature RFCs** to ensure they follow methodology

**Purpose:** Ensure domains/features are defined by their organon constraints first, with implementation following those constraints.

---

## Core Principle

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   ORGANON   │         │     RFC     │         │    CODE     │
│ "should be" │ ◄─────► │ "will be"   │ ────────► │  "what is"  │
│             │  cites  │             │ implements│             │
│ Constraints │         │ Proposals   │           │ Reality     │
└─────────────┘         └─────────────┘           └─────────────┘
```

**RFCs have dual nature:**
1. **Organon mutation plan** - What constraints the domain will define
2. **Technical implementation plan** - How code will implement those constraints

**BOTH are required.** Writing only one is incomplete.

---

## Identity Check (Always Start Here)

Before designing a domain/feature, load and internalize:

1. **Read `book-llms/patterns.md`** - RFC-Driven Evolution Pattern section
2. **Read `book-llms/templates.md`** - RFC Template section
3. **Read `book-llms/scopes.md`** - Domain vs Feature vs Component
4. **Read product ETHOS.md** - Parent constraints the domain inherits
5. **Read `book-llms/frontmatter-system.md`** - Organon file structure

**Critical question:** Is this a domain (bounded context), feature (cross-cutting capability), or component (code module)?

---

## Pre-Design Phase: Scope Classification

### Domain vs Feature vs Component

| Type | Question Answered | Use When | Example |
|------|-------------------|----------|---------|
| **Domain** | "What business concepts exist?" | Rich bounded context with own concepts, events, lifecycle | Testing framework (assertions, coverage, discovery) |
| **Feature** | "What can users do?" | Cross-cutting capability used by multiple domains | Caching, auth, logging |
| **Component** | "Where is the code?" | Code modules with dependency relationships | Parser, runtime, compiler |

**Decision heuristic:**
- Has ≥3 unique concepts + lifecycle → **Domain**
- Crosses multiple domains → **Feature**
- Users think in code terms → **Component**

**For this skill, focus on Domains and Features** (Components rarely need full RFC).

---

## The RFC-Driven Design Workflow

### Phase 1: Problem Definition (5-10 minutes)

**Before writing any RFC, answer these questions:**

1. **Why does the organon need to evolve?**
   - What gap exists in current constraints?
   - What problem are we solving?

2. **What scope is this?**
   - Domain (bounded context) or Feature (cross-cutting)?
   - Parent scope (product, domain)?

3. **What will the organon define?**
   - Identity (IS/IS NOT statements)
   - ≥3 Invariants (constraints with enforcement mechanisms)
   - ≥3 Principles (design priorities, prioritized)
   - Decision heuristics (situation → action)

4. **How will code implement it?**
   - High-level architecture (packages, modules)
   - Core abstractions (types, interfaces)
   - Implementation phases (what ships when)

**If you can't answer these, you're not ready to write an RFC.**

---

### Phase 2: Create RFC Structure (10-15 minutes)

**Step 1: Create RFC file**

```bash
# Determine next RFC number
ls rfcs/*.md | sort | tail -1  # Get latest number
# Create new RFC (e.g., RFC 002)
touch rfcs/002-<feature-name>.md
```

**Step 2: Copy RFC template**

Load `book-llms/templates.md` → RFC Template section → copy entire template to new RFC file.

**Step 3: Fill in frontmatter**

```yaml
---
type: rationale
scope: product
name: [feature-name]
version: "1.0"
summary: [One-sentence description]
token_estimate: [estimate ~5000-8000 for domain RFCs]
status: draft
created: [YYYY-MM-DD]
author: [your-agent-name]
related_files:
  - ../organon/domains/tools/ETHOS.md  # or appropriate product ETHOS
  - ../book-llms/[relevant].md
load_priority: high
audience: [llm, human]
---
```

---

### Phase 3: Write Organon Mutation Plan (30-45 minutes)

**This is the critical section that defines WHAT the organon will say.**

#### 3.1: Create Section - Domain ETHOS.md Content

Write out the **exact content** that will go in the domain/feature ETHOS.md:

```markdown
## Organon Impact

### Create

**`organon/domains/<name>/ETHOS.md`** ← Core domain definition

This file defines the <name> domain's identity and constraints:

\```markdown
## Identity

### What This Domain IS
- [Specific identity statement 1]
- [Specific identity statement 2]
- [Specific identity statement 3]
- [What it provides / what problem it solves]
- [What it integrates with]

### What This Domain IS NOT
- [Clear boundary 1 - what it explicitly does NOT do]
- [Clear boundary 2]
- [Clear boundary 3]
- [What it is not responsible for]

## Invariants

1. **INV-<SCOPE>-1: <kebab-case-name>**
   - [Exact invariant text - what constraint must hold]
   - Enforced by: [Specific enforcement mechanism - tests, gates, reviews]

2. **INV-<SCOPE>-2: <kebab-case-name>**
   - [Exact invariant text]
   - Enforced by: [Specific enforcement mechanism]

3. **INV-<SCOPE>-3: <kebab-case-name>**
   - [Exact invariant text]
   - Enforced by: [Specific enforcement mechanism]

[Minimum 3 invariants, typically 5-7 for a domain]

## Principles (Prioritized)

1. **[Principle 1] over [alternative 1]** - [One-line explanation]
2. **[Principle 2] over [alternative 2]** - [One-line explanation]
3. **[Principle 3] over [alternative 3]** - [One-line explanation]
4. **[Principle 4] over [alternative 4]** - [One-line explanation]
5. **[Principle 5] over [alternative 5]** - [One-line explanation]

[Prioritized list - 1 is most important]

## Decision Heuristics

| Situation | Action |
|-----------|--------|
| [Specific scenario 1] | [Clear action / decision] |
| [Specific scenario 2] | [Clear action / decision] |
| [Specific scenario 3] | [Clear action / decision]|
| [Specific scenario 4] | [Clear action / decision] |
| [Specific scenario 5] | [Clear action / decision] |

[Minimum 5 heuristics covering common decision points]
\```
```

**Quality checklist for ETHOS.md content:**
- [ ] Identity IS statements are specific (not generic platitudes)
- [ ] Identity IS NOT statements define clear boundaries
- [ ] Each invariant has concrete enforcement mechanism
- [ ] Invariants are testable/verifiable (not vague aspirations)
- [ ] Principles are prioritized (not equal weight)
- [ ] Heuristics cover real decisions (not obvious situations)

#### 3.2: Create Section - Domain PHILOSOPHY.md Content

Write out the **exact content** that will go in the domain/feature PHILOSOPHY.md:

```markdown
**`organon/domains/<name>/PHILOSOPHY.md`** ← Design rationale

This file explains WHY the <name> domain is designed this way:

\```markdown
## The Problem

[Detailed problem description - 2-3 paragraphs]

**Why does this problem exist?**
1. [Root cause 1]
2. [Root cause 2]
3. [Root cause 3]

**Why haven't we solved it yet?**
- [Historical reason or blocker]

**Result:** [Negative outcome of unsolved problem]

## The Bet

**Bet:** [One-sentence statement of what assumption we're making]

**Why this works:**
- [Evidence point 1]
- [Evidence point 2]
- [Evidence point 3]

**What must be true:**
- [Prerequisite 1 for bet to succeed]
- [Prerequisite 2]
- [Prerequisite 3]

## Trade-offs

### 1. [Trade-off Name] ([Choice A] > [Choice B])
**Choice:** [What we decided]

**Benefit:** [What we gain]

**Cost:** [What we give up]

**Why we chose [X]:** [2-3 sentence rationale]

### 2. [Trade-off Name]
[Same structure]

### 3. [Trade-off Name]
[Same structure]

### 4. [Trade-off Name]
[Same structure]

### 5. [Trade-off Name]
[Same structure]

[Minimum 5 trade-offs - major design decisions]

## Alternatives Considered

### Alt 1: [Alternative Approach Name]
**Rejected because:** [Clear reason why this won't work]

### Alt 2: [Alternative Approach Name]
**Rejected because:** [Clear reason]

### Alt 3: [Alternative Approach Name]
**Rejected because:** [Clear reason]

## Success Criteria

This bet succeeds if:
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]
- [ ] [Measurable outcome 4]
\```
```

**Quality checklist for PHILOSOPHY.md content:**
- [ ] Problem section explains WHY (not just WHAT)
- [ ] The Bet is a falsifiable hypothesis
- [ ] Trade-offs show both sides (benefit AND cost)
- [ ] Rationale explains decision-making reasoning
- [ ] Alternatives considered show exploration (not just one path)
- [ ] Success criteria are measurable (not vague)

#### 3.3: Update Section

List **specific** organon files that will be updated:

```markdown
### Update

**`<product-path>/ETHOS.md`** (product-level organon)
- Add reference: "<name> domain inherits product invariants"
- Add decision heuristic: "Working on <name>? Read organon/domains/<name>/ETHOS.md"

**`<product-path>/README.md`**
- Add link to <name> domain in "Domains" section

**`book-llms/[relevant-file].md`** (if applicable)
- Add <name> as reference implementation example
- Update relevant patterns/specifications
```

---

### Phase 4: Write Technical Implementation Plan (30-45 minutes)

**This section defines HOW code will implement the organon constraints.**

#### 4.1: Architecture

```markdown
## Technical Implementation

### Architecture

**Package Structure:**
\```
<product>/
├── organon/
│   └── domains/
│       └── <name>/
│           ├── ETHOS.md      ← Domain constraints
│           ├── PHILOSOPHY.md ← Design rationale
│           └── README.md     ← Navigation
└── src/
    └── [implementation-path]/
        ├── core/              ← Pure functions
        ├── [subdirs]          ← Domain-specific modules
        └── index.ts           ← Public API
\```

**Core Abstractions:**
\```typescript
// Show key types/interfaces that implement domain concepts
interface [CoreConcept1] {
  // ...
}

interface [CoreConcept2] {
  // ...
}

type [CoreAbstraction] = ...
\```

**Implements domain invariants:**
- **INV-<SCOPE>-1** ([name]): [How code enforces this constraint]
- **INV-<SCOPE>-2** ([name]): [How code enforces this constraint]
- **INV-<SCOPE>-3** ([name]): [How code enforces this constraint]
[Map each invariant to implementation strategy]
```

#### 4.2: API Design

```markdown
### API Design

**Core API** (implements domain principles):

\```typescript
// Show actual function signatures, interfaces, types

// Main entry point
export function [primaryFunction](options: [Options]): Promise<[Result]> {
  // ...
}

// Options interface
export interface [Options] {
  [field1]: [type];
  [field2]: [type];
  // ...
}

// Result interface
export interface [Result] {
  success: boolean;
  [data]: [type];
  [errors]?: Error[];
}

// Supporting functions
export function [helperFunction1](...): Promise<...>
export function [helperFunction2](...): Promise<...>
\```

**API Design Principles:**
- [How API reflects domain principles]
- [Why options object vs positional args]
- [Why async vs sync]
```

#### 4.3: Implementation Plan

```markdown
### Implementation Plan

**Phase 1: [Name] (Weeks X-Y)**

**Week X: [Milestone Name]**
- [ ] [Specific task 1]
- [ ] [Specific task 2]
- [ ] [Specific task 3]
- [ ] [Specific task 4]

**Week Y: [Milestone Name]**
- [ ] [Specific task 5]
- [ ] [Specific task 6]
- [ ] [Specific task 7]

**Deliverable:** [What ships in Phase 1 - specific, testable]

---

**Phase 2: [Name] (Weeks A-B)**
- [ ] [Task 8]
- [ ] [Task 9]
- [ ] [Task 10]

**Deliverable:** [What ships in Phase 2]

---

**Phase 3: [Name] (Weeks C-D)**
- [ ] [Task 11]
- [ ] [Task 12]

**Deliverable:** [What ships in Phase 3]
```

**Quality checklist for implementation plan:**
- [ ] Tasks are specific (not vague "implement X")
- [ ] Phases have clear deliverables (what ships when)
- [ ] Week-by-week breakdown for Phase 1
- [ ] Each phase maps to domain invariants being implemented
- [ ] Time estimates are realistic (2-6 weeks per phase)

#### 4.4: Design Decisions (Technical)

```markdown
### Design Decisions (Technical)

These decisions implement the domain principles defined in <name>/PHILOSOPHY.md:

**Decision 1: [Technical Choice Name]**
- **Implements:** [Which domain principle or invariant]
- **Technical benefit:** [What this enables technically]
- **Trade-off:** [What we're giving up]
- **Why we chose [X]:** [2-3 sentence rationale]

**Decision 2: [Technical Choice Name]**
[Same structure - minimum 5 decisions]
```

---

### Phase 5: Complete Supporting Sections (15-20 minutes)

Fill in remaining RFC sections:

```markdown
## Success Metrics
- [ ] **[Metric 1]** - [Measurable, specific]
- [ ] **[Metric 2]** - [Measurable, specific]
- [ ] **[Metric 3]** - [Measurable, specific]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Med/Low] | [Specific mitigation strategy] |

## Open Questions
1. **[Question 1]** - [What's uncertain?]
   - **Recommendation:** [Suggested resolution]

## Dependencies
**Blocks:** [What can't happen until this is done]
**Blocked by:** [What must happen first]
```

---

## RFC Quality Checklist

Before submitting RFC for review, verify:

### Organon Mutation Plan (Required)
- [ ] **ETHOS.md content is detailed** (not just "will add invariants")
  - [ ] ≥3 identity IS statements
  - [ ] ≥3 identity IS NOT statements
  - [ ] ≥3 invariants with enforcement mechanisms
  - [ ] ≥3 principles (prioritized)
  - [ ] ≥5 decision heuristics
- [ ] **PHILOSOPHY.md content is detailed** (not just "will add philosophy")
  - [ ] Problem section explains WHY
  - [ ] The Bet is a falsifiable hypothesis
  - [ ] ≥5 trade-offs with rationale
  - [ ] ≥3 alternatives considered
  - [ ] Measurable success criteria

### Technical Implementation Plan (Required)
- [ ] **Architecture is detailed**
  - [ ] Package structure shown
  - [ ] Core abstractions defined (TypeScript interfaces/types)
  - [ ] Each invariant mapped to enforcement strategy
- [ ] **API Design is concrete**
  - [ ] Function signatures shown
  - [ ] Interfaces defined
  - [ ] Design rationale provided
- [ ] **Implementation Plan is specific**
  - [ ] Week-by-week for Phase 1
  - [ ] Clear deliverables per phase
  - [ ] Tasks are actionable (not vague)
- [ ] **Design Decisions explain technical choices**
  - [ ] ≥5 decisions documented
  - [ ] Each links to domain principle
  - [ ] Trade-offs acknowledged

### Both Plans Present (Critical)
- [ ] RFC is NOT just organon plan (has technical details)
- [ ] RFC is NOT just technical plan (has organon content)
- [ ] Both plans are detailed enough to begin work
- [ ] Organon defines "should be", code implements "what is"

---

## Common Mistakes (Don't Do This)

### ❌ Mistake 1: Only Technical Plan

**Bad RFC structure:**
```markdown
## Organon Impact
- Create testing/ETHOS.md (will add invariants)
- Create testing/PHILOSOPHY.md (will explain design)

## Technical Implementation
[5000 words of architecture, API, phases]
```

**Problem:** Doesn't show WHAT the organon will say. Just states it will exist.

**Fix:** Write out the actual invariants, principles, identity statements.

---

### ❌ Mistake 2: Only Organon Plan

**Bad RFC structure:**
```markdown
## Organon Impact
[Detailed ETHOS.md and PHILOSOPHY.md content]

## Technical Implementation
We will implement the constraints defined above.
```

**Problem:** No technical details. How will code be structured? What's the API? What are the phases?

**Fix:** Add Architecture, API Design, Implementation Plan sections.

---

### ❌ Mistake 3: Vague Invariants

**Bad invariant:**
```markdown
1. **INV-TEST-1: quality**
   - Code should be high quality
   - Enforced by: reviews
```

**Problem:** "High quality" is not testable. "Reviews" is not automated.

**Good invariant:**
```markdown
1. **INV-TEST-1: 100-percent-coverage**
   - Testing domain itself has 100% test coverage
   - Enforced by: Vitest coverage gate in CI (fails build < 100%)
```

---

### ❌ Mistake 4: Generic Identity Statements

**Bad identity:**
```markdown
### What This Domain IS
- A good testing framework
- Well-designed and useful
- Follows best practices
```

**Problem:** Could describe ANY testing framework. Not specific.

**Good identity:**
```markdown
### What This Domain IS
- A semantic testing framework for tier-4 invariant verification
- TypeScript-native library published as @organon-methodology/testing
- Bridge between "declare invariant in ETHOS.md" and "verify in code"
- Integration layer connecting invariants to test frameworks (not a test runner)
- Coverage tracker that maps invariant IDs to test implementations
```

---

### ❌ Mistake 5: Unprioritized Principles

**Bad principles:**
```markdown
## Principles
- Clarity
- Speed
- Simplicity
- Testability
- Flexibility
```

**Problem:** No prioritization. All seem equal. No trade-offs shown.

**Good principles:**
```markdown
## Principles (Prioritized)
1. **Testability over speed** - Pure functions, deterministic
2. **Clarity over brevity** - Verbose errors, explicit API
3. **Reusability over flexibility** - Pre-built assertions for 80% cases
4. **Fail-fast over forgiving** - Errors surface immediately
5. **Integration over replacement** - Works with existing test frameworks
```

---

## Review Process

Once RFC is complete:

1. **Self-review** using quality checklist above
2. **Submit for review** (create PR with RFC file)
3. **Address feedback** (iterate on RFC, don't start coding yet)
4. **Get approval** (reviewers sign off)
5. **Begin implementation** following Same-PR principle:
   - Implement Phase 1
   - Create organon files (ETHOS.md, PHILOSOPHY.md)
   - Run `organon validate` on new organon files to verify structure
   - Run `organon verify` to check cross-file integrity
   - **Same PR:** Organon files + implementation code
   - Update RFC status: Draft → Implementing → Implemented

---

## Meta-Principle

> The organon defines "should be" before code implements "what is."

If you write code before defining the organon, you're doing it backwards. The organon is the source of truth that defines the product. Code follows.

**RFCs are the bridge:** They propose what the organon will say AND how code will implement it. Both are required.

---

## When in Doubt

1. **Check RFC template** (`book-llms/templates.md`) - Am I following the structure?
2. **Check RFC pattern** (`book-llms/patterns.md`) - Do I have both organon + technical?
3. **Check existing RFC** (`rfcs/001-testing-framework.md`) - Does mine have similar detail level?
4. **Ask:** Can someone start implementing from this RFC without additional design work?

**If any answer is NO, the RFC is incomplete.**

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| Can't classify scope (domain vs feature vs component) | Re-read `book-llms/scopes.md`. Apply: ≥3 unique concepts + lifecycle → domain; crosses multiple domains → feature; code terms → component. |
| Invariants are too vague to test | Apply "testable?" filter — if you can't write a verification gate for it, rewrite to be more specific or move to principles. |
| Missing organon mutation plan | Stop and write exact ETHOS.md and PHILOSOPHY.md content before proceeding to technical plan. |
| Missing technical implementation plan | Stop and add architecture, API design, and phased implementation plan. Both plans are required. |
| RFC too large (>10000 tokens) | Split into multiple RFCs with explicit dependency chain. Each RFC must be self-contained. |
| Principles not truly prioritized | Reorder with explicit trade-off reasoning. Test: if principle 3 conflicts with principle 1, does 1 genuinely win? |
| Parent scope constraints contradicted | Remove or weaken the contradicting constraint in the child RFC. Child scopes can add constraints, never relax them. |
