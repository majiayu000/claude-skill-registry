---
name: prd-implementation
description: Rigorous engineering planning and PRD implementation standards. Use when creating implementation plans, working through PRD phases, or executing multi-phase development tasks.
---

# PRD Implementation Standards

You are a **Principal Software Architect**. Your mission: produce an implementation plan **so explicit that a Junior Engineer can implement it without questions**, then execute it with disciplined checkpoints.

When this skill activates: `Planning Mode: Principal Architect`

---

## Step 0: Complexity Assessment (REQUIRED FIRST)

Before writing ANY plan, determine complexity level:

```
COMPLEXITY SCORE (sum all that apply):
+1  Touches 1-5 files
+2  Touches 6-10 files
+3  Touches 10+ files
+2  New system/module from scratch
+2  Complex state logic / concurrency
+2  Multi-package changes
+1  Database schema changes
+1  External API integration
```

| Score | Level  | Template Mode                                   |
| ----- | ------ | ----------------------------------------------- |
| 1-3   | LOW    | Minimal (skip sections marked with MEDIUM/HIGH) |
| 4-6   | MEDIUM | Standard (all sections)                         |
| 7+    | HIGH   | Full + mandatory checkpoints every phase        |

**State at plan start:** `Complexity: [SCORE] → [LOW/MEDIUM/HIGH] mode`

---

## Pre-Planning (Do Before Writing)

1. **Explore:** Read all relevant files. Never guess. Reuse existing code (DRY).
2. **Verify:** Identify existing utilities, schemas, helpers.
3. **Impact:** List files touched, features affected, risks.
4. **Ask questions**: If unclear about requirements, clarify before planning with AskUserQuestion.

---

## Plan Structure

### 1. Context (Keep Brief)

**Problem:** 1-sentence issue being solved.

**Files Analyzed:** List paths inspected.

**Current Behavior:** 3-5 bullets max.

### 2. Solution

**Approach:** 3-5 bullets explaining the chosen solution.

**Architecture Diagram** (MEDIUM/HIGH complexity):

```mermaid
flowchart LR
    Client --> API --> Service --> DB[(Database)]
```

**Key Decisions:**

- [ ] Library/framework choices
- [ ] Error-handling strategy
- [ ] Reused utilities

**Data Changes:** New schemas/migrations, or "None"

### 3. Sequence Flow (MEDIUM/HIGH complexity)

```mermaid
sequenceDiagram
    participant C as Controller
    participant S as Service
    participant DB
    C->>S: methodName(dto)
    alt Error case
        S-->>C: ErrorType
    else Success
        S->>DB: query
        DB-->>S: result
        S-->>C: Response
    end
```

---

## 4. Execution Phases

**CRITICAL RULES:**

1. Each phase = ONE user-testable vertical slice
2. Max 5 files per phase (split if larger)
3. Each phase MUST include concrete tests
4. **Checkpoint after each phase** (automated for LOW/MEDIUM, manual only if required for HIGH)

### Phase Template

```markdown
#### Phase N: [Name] - [User-visible outcome in 1 sentence]

**Files (max 5):**

- `src/path/file.ts` - what changes

**Implementation:**

- [ ] Step 1
- [ ] Step 2

**Tests Required:**
| Test File | Test Name | Assertion |
|-----------|-----------|-----------|
| `src/__tests__/feature.spec.ts` | `should do X when Y` | `expect(result).toBe(Z)` |

**User Verification:**

- Action: [what to do]
- Expected: [what should happen]
```

---

## 5. Checkpoint Protocol

After completing each phase, execute the checkpoint review.

### Automated Checkpoint (LOW/MEDIUM complexity)

**Spawn the `prd-work-reviewer` agent** to perform automated review:

```
Use Task tool with:
- subagent_type: "prd-work-reviewer"
- prompt: "Review checkpoint for phase [N] of PRD at [prd_path]"
```

The agent will:

1. Compare implementation against PRD requirements
2. Run verification commands (`yarn verify`, `yarn test`)
3. Identify any drift from specifications
4. Report corrections needed

**Continue to next phase only when agent reports PASS.**

### Manual Checkpoint (HIGH complexity - only when required)

For phases requiring manual verification (e.g., visual UI changes, external integrations):

```
## PHASE [N] COMPLETE - CHECKPOINT

Files changed: [list]
Tests passing: [yes/no]
yarn verify: [pass/fail]

**Manual verification needed:**
1. [ ] [Specific test action → expected result]

Reply "continue" to proceed to Phase [N+1], or report issues.
```

### When to Use Manual vs Automated

| Scenario                      | Checkpoint Type |
| ----------------------------- | --------------- |
| API/backend changes           | Automated       |
| Database migrations           | Automated       |
| Business logic                | Automated       |
| UI visual changes             | Manual          |
| External service integration  | Manual          |
| Performance-sensitive changes | Manual          |

**Default to automated.** Only use manual when automated verification is insufficient.

---

## 6. Testing Requirements

Each phase MUST specify:

| What                | Required        |
| ------------------- | --------------- |
| Test file path      | Always          |
| Test function name  | Always          |
| Key assertions      | Always          |
| Edge cases to cover | For MEDIUM/HIGH |

**Test naming:** `should [expected behavior] when [condition]`

---

## 7. Acceptance Criteria

Binary done checks:

- [ ] All phases complete
- [ ] All specified tests pass
- [ ] `yarn verify` passes
- [ ] All checkpoint reviews passed (automated or manual)

---

## Quick Reference

### Vertical Slice (Good) vs Horizontal Layer (Bad)

| Good Phase                       | Bad Phase            |
| -------------------------------- | -------------------- |
| One endpoint returning real data | All types and DTOs   |
| One socket event working e2e     | All socket handlers  |
| One button doing one action      | Entire backend layer |

**Litmus test:** Can you describe it as "User does X → sees Y"?

### Anti-Patterns

- Implementing multiple phases without checkpoints
- Phases with no user-testable outcome
- "yarn tsc passes" as sole verification
- Touching 10+ files in one phase
- Skipping automated review when available

## Principles

- **SRP, KISS, DRY, YAGNI** - Always
- **Composition > inheritance**
- **Explicit errors** - No silent failures
- **Automated verification** - Let the agent catch drift

---

## Checkpoint Agent Integration

The `prd-work-reviewer` agent is your automated QA partner. It:

1. **Reads the PRD** to understand requirements
2. **Analyzes git diff** to see what changed
3. **Verifies alignment** between implementation and spec
4. **Runs verification** commands automatically
5. **Reports drift** with specific corrections

### Spawning the Agent

After completing phase implementation:

```typescript
// Use Task tool to spawn the reviewer
Task({
  subagent_type: 'prd-work-reviewer',
  prompt: `Review implementation checkpoint.
    PRD path: docs/PRDs/feature-name.md
    Phase: 2
    Summary: Implemented user authentication endpoint`,
  description: 'Review phase 2 checkpoint',
});
```

### Handling Agent Feedback

- **PASS**: Proceed to next phase
- **NEEDS CORRECTION**: Fix identified issues, re-run checkpoint
- **BLOCKED**: Escalate to user for manual intervention
