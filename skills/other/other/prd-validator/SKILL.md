---
name: prd-validator
description: Phase 1.5 — Automatic PRD validation after generation. Verifies references exist in codebase, evaluates scope realism, classifies ACs as measurable or vague, and blocks on missing Non-Goals. Generates prd-validation.md in the state directory.
---

# PRD Validator

Runs **automatically as Phase 1.5**, between PRD generation and TechSpec generation.
Purpose: catch problems in the PRD before they propagate into the TechSpec and Tasks.

## Position in flow

```
[Prompt Enrichment]
      ↓
PRD generation
      ↓
[PRD Validation]  ← THIS SKILL
      ↓
TechSpec generation
```

## Entry conditions

- `prd.md` must exist in `tasks/prd-{slug}/` (run PRD generation first)
- Generates `prd-validation.md` and saves to `.claude/feature-state/{slug}/`
- Load if already exists (resume flow)
- Can be forced with `--revalidate`

---

## Validation 1: Reference Existence

Grep the codebase for every entity, service, path, endpoint, and component mentioned in the PRD.

### What to check
- **Services/classes**: e.g., "uses the existing UserService" → grep for `UserService`
- **API endpoints**: e.g., "/api/users/connect" → grep for `users/connect` or `usersConnect`
- **Database collections/tables**: e.g., "connections collection" → grep for `connections`
- **UI components**: e.g., "TrainerCard component" → grep for `TrainerCard`
- **File paths**: explicit paths mentioned → check they exist with Glob

### Classification
- **Found in codebase** → ✅ Pass
- **Not found, but PRD says "will be created"** → ⚠️ Warning (document as new entity)
- **Not found, PRD implies it exists** → ❌ Blocker (misleading reference)

### Search commands

```bash
# For each entity/service name extracted from PRD:
grep -r "{term}" . \
  --include="*.ts" --include="*.tsx" --include="*.swift" \
  --include="*.rs" --include="*.py" --include="*.go" \
  -l 2>/dev/null | head -10
```

---

## Validation 2: Scope Realism

### Requirement count
- Count bullet points or numbered items in functional requirements sections
- **≤8 requirements** → ✅ Manageable
- **9–15 requirements** → ⚠️ Warning: "This is a larger scope. Consider splitting into phases."
- **>15 requirements** → ❌ Blocker: "Scope too large. Break into sub-features."

### Scope creep word detection
Scan for phrases that inflate scope without commitment:

| Pattern | Example | Action |
|---------|---------|--------|
| `also`, `besides`, `additionally` | "It should also support dark mode" | ⚠️ Warning |
| `in the future`, `eventually`, `later` | "In the future, add analytics" | ⚠️ Warning — move to Deferred |
| `it would be nice`, `ideally`, `if possible` | "Ideally the UX is seamless" | ⚠️ Warning — remove or commit |
| `real-time`, `live`, `instant` | "Real-time dashboard" | ⚠️ Warning — clarify complexity |
| `all`, `every`, `any`, `unlimited` | "Works for any file type" | ⚠️ Warning — narrow the scope |

### Comparison with existing features
If `context.md` exists, compare requirement count with similar implemented features.
If similar feature had 6 tasks and this PRD has 18 requirements → flag the discrepancy.

---

## Validation 3: Acceptance Criteria Quality

For each AC in the PRD, classify as **measurable** or **vague**:

### Vague AC patterns (flag these)
| Pattern | Example |
|---------|---------|
| Subjective quality | "should feel fast", "good UX", "intuitive interface" |
| Unquantified performance | "loads quickly", "responds fast" |
| Vague compliance | "should be secure", "must be reliable" |
| Undefined success | "users should be happy", "works correctly" |

### Measurable AC patterns (accept these)
| Pattern | Example |
|---------|---------|
| Specific metric | "responds in <500ms for 95% of requests" |
| Boolean condition | "returns 404 when user not found" |
| Explicit state change | "status changes to 'active' after approval" |
| Countable outcome | "displays all 10 items on first load" |

### Auto-fix suggestions for vague ACs
When a vague AC is detected, propose a measurable version:

| Vague | Suggested replacement |
|-------|-----------------------|
| "should be fast" | "page loads within 2 seconds on a 3G connection" |
| "good UX" | "task can be completed in ≤3 steps by a new user" |
| "must be secure" | "all endpoints validate auth token before processing" |
| "responsive design" | "layout is usable on screens ≥320px wide" |

---

## Validation 4: Non-Goals Section

- PRD contains a `Non-Goals`, `Out of Scope`, or `YAGNI` section → ✅ Pass
- PRD missing any such section → ❌ **Blocker**

When blocking on missing Non-Goals, suggest a starter list based on common exclusions
for the detected feature type (from prompt-enricher keywords):

```markdown
**Suggested Non-Goals for [feature type]:**
- [Context-appropriate exclusion 1]
- [Context-appropriate exclusion 2]
- [Context-appropriate exclusion 3]
```

---

## Validation 5: Conflict with Existing PRDs

Scan `tasks/prd-*/prd.md` for other PRDs that cover the same domain:

1. Extract the top 5 keywords from the current PRD's title and goals
2. Check if any existing PRD contains ≥3 of those keywords
3. If overlap found:
   - ⚠️ Warning: "PRD `prd-{other-slug}` covers similar domain. Review for conflicts."
   - List the overlapping keywords

---

## Behavior

| Finding type | Effect |
|--------------|--------|
| ✅ Pass | Continue silently |
| ⚠️ Warning | Present to user, ask if they want to fix before proceeding. Can be dismissed. |
| ❌ Blocker | **Stop the flow**. User must correct before TechSpec generation. Auto-fix suggested when possible. |

### User interaction for blockers

```
❌ PRD Validation Failed — cannot proceed to TechSpec

Blocker 1: AC #3 is not measurable
  Current: "the system should feel responsive"
  Suggested fix: "page loads within 2 seconds on 3G connection"

Blocker 2: No Non-Goals section found
  Suggested Non-Goals:
  - Email notifications (requires separate notification service)
  - Mobile app changes (this feature is web-only)
  - Bulk operations (out of scope for v1)

Would you like me to apply these fixes to the PRD? [Yes / Let me fix manually / Show full report]
```

### User interaction for warnings only

```
⚠️ PRD Validation — warnings found (non-blocking)

• Scope may be large (13 functional requirements)
• "UserService" referenced but not found in codebase — confirm it will be created
• "In the future, add analytics" → move this to Deferred section

Continue to TechSpec generation? [Yes, continue / Let me address these first]
```

---

## Output: prd-validation.md

Save to `.claude/feature-state/{slug}/prd-validation.md`:

```markdown
## PRD Validation Report

Generated: {timestamp}
PRD: tasks/prd-{slug}/prd.md

### ✅ Passed
- Acceptance criteria are measurable
- Non-goals section present
- Scope is within reasonable bounds (7 requirements)

### ⚠️ Warnings (non-blocking)
- Scope may be large (12 functional requirements)
- "UserService" referenced but not found in codebase (will be created as new entity)
- Scope creep phrase detected: "In the future, add analytics" → move to Deferred

### ❌ Blockers (must fix before proceeding)
- AC #3 is not measurable: "system should feel responsive"
  → Suggested: "page loads within 2 seconds on 3G connection"
- No Non-Goals section found
  → Suggested Non-Goals: [list]

### Reference Check
| Entity | Found in codebase? | Notes |
|--------|--------------------|-------|
| UserService | ❌ Not found | Marked as new creation in PRD |
| /api/users | ✅ Found | src/api/users.ts |
| TrainerCard | ✅ Found | Presentation/Features/Trainer/ |

### Scope Analysis
- Functional requirements: 12
- Scope creep phrases: 1 ("in the future")
- Similar feature: prd-student-enrollment had 6 requirements → this is ~2x larger

### AC Quality
| AC | Classification | Issue |
|----|----------------|-------|
| AC-1: returns 404 when not found | ✅ Measurable | — |
| AC-2: fast response | ❌ Vague | "fast" is not quantified |
| AC-3: users can connect | ⚠️ Borderline | Add: "within 2 clicks from the dashboard" |

### Verdict
BLOCKED — fix 2 blocker(s) before proceeding to TechSpec generation.
```

---

## Integration with spec-writer

When `prd-validation.md` exists and has no blockers, spec-writer reads it for context:
- Use the Reference Check table to know which entities are NEW vs EXISTING
- Use Scope Analysis to calibrate TechSpec complexity
- Reference the passed ACs as the baseline for implementation criteria
