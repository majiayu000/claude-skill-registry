---
name: opencode-clarify
description: "This skill should be used when the user asks to 'clarify requirements', 'resolve uncertainties', 'answer spec questions', or when auto-triggered by /opencode-specify with >3 NEEDS CLARIFICATION markers. Systematically surfaces and resolves ambiguities in specifications."
---

# Clarify - Systematic Uncertainty Resolution

Scan specifications for ambiguities and resolve them through structured questioning. Produces cleaner specs that feed into architecture and planning.

**Triggers:**
- Auto-triggered by `/opencode-specify` when >3 `[NEEDS CLARIFICATION]` markers
- Manual: `/opencode-clarify` to review current spec
- Manual: `/opencode-clarify path/to/spec.md` for specific spec

---

## Process

### 1. Load Specification

Find active spec:
```bash
# Most recent spec
ls -t .opencode/specs/*/spec.md | head -1
```

Or use provided path.

### 2. Extract Markers

```bash
grep -n "NEEDS CLARIFICATION" .opencode/specs/*/spec.md
```

Parse each marker:
- Line number
- Requirement ID (FR-xxx, SC-xxx, etc.)
- Context (what section)
- Question text

### 3. Scan for Implicit Ambiguities

Beyond explicit markers, scan for:

| Pattern | Example | Issue |
|---------|---------|-------|
| Vague adjectives | "fast", "reliable", "user-friendly" | Not measurable |
| Undefined terms | "admin user", "valid input" | Domain-specific |
| Missing edge cases | Only happy path defined | Incomplete |
| Passive voice | "data is validated" | Who validates? When? |
| Unbounded lists | "users can upload files" | What types? Size limits? |

Add discovered ambiguities to question queue.

### 4. Categorize Uncertainties

Group by taxonomy:

| Category | Examples |
|----------|----------|
| **Functional scope** | What features? What's excluded? |
| **Data model** | What entities? Relationships? |
| **UX flows** | User journey? Error states? |
| **Performance** | Latency? Throughput? Scale? |
| **Integration** | External systems? APIs? |
| **Edge cases** | Limits? Errors? Recovery? |
| **Constraints** | Budget? Timeline? Tech restrictions? |
| **Terminology** | Domain-specific definitions? |
| **Completion** | Definition of done? |

### 5. Prioritize Questions

Score each: `Impact × Uncertainty`

- **Impact:** How much does this affect architecture, data model, task breakdown, or testing?
- **Uncertainty:** How unclear is this currently?

Take top 5 questions maximum per clarify session.

### 6. Generate Questions

**Format rules:**
- Multiple choice (2-5 options) preferred
- If open-ended: constrain to ≤5 word answer
- One question at a time
- Include context from spec

**Question template:**
```markdown
## Question 1 of 5

**Context:** FR-003 states "System MUST validate user input"

**Question:** What validation rules apply to email addresses?

**Options:**
A) RFC 5322 strict validation
B) Simple format check (contains @ and .)
C) Format check + DNS MX record verification
D) Custom business rules (please specify)

**Impact:** Affects error messages, test cases, and integration complexity.
```

### 7. Apply Answers Immediately

After each answer:

1. Update spec.md - replace marker with resolved requirement
2. Log to `.opencode/specs/{slug}/clarifications/log.md`

**Before:**
```markdown
- FR-003: System MUST validate email [NEEDS CLARIFICATION: validation rules]
```

**After:**
```markdown
- FR-003: System MUST validate email format (RFC 5322) and verify domain has MX record
```

**Clarification log entry:**
```markdown
## 2025-01-29: Email Validation Rules

**Question:** What validation rules apply to email addresses?
**Answer:** RFC 5322 + MX verification (Option C)
**Updated:** FR-003
**Rationale:** Balance strictness with user experience, catch typos in domain
```

### 8. Track Coverage

After all questions answered, report coverage:

```markdown
## Clarification Summary

| Category | Status |
|----------|--------|
| Functional scope | Resolved |
| Data model | Resolved |
| UX flows | Outstanding (1 marker) |
| Performance | Clear |
| Integration | Deferred |
| Edge cases | Resolved |
| Constraints | Clear |
| Terminology | Resolved |
| Completion | Clear |

**Remaining markers:** 1
**Ready for architecture:** Yes (≤3 markers)
```

---

## Question Patterns

### Multiple Choice (Preferred)

```markdown
**Question:** How should the system handle failed payment attempts?

A) Retry automatically up to 3 times
B) Notify user immediately, no retry
C) Queue for manual review
D) Combination (specify)
```

### Constrained Open-Ended

```markdown
**Question:** Maximum file upload size? (≤5 words)

Example answers: "10MB", "50MB per file", "No limit"
```

### Binary with Justification

```markdown
**Question:** Should inactive users be auto-deleted?

A) Yes - after [specify duration]
B) No - keep indefinitely

If yes, what defines "inactive"?
```

---

## Handling Technical Uncertainties

Some markers are technical (HOW, not WHAT). Don't resolve these in clarify.

**Technical markers → arch-lead:**
```
[NEEDS CLARIFICATION: which database?]
[NEEDS CLARIFICATION: sync or async processing?]
[NEEDS CLARIFICATION: API design]
```

**Flag for arch-lead:**
```markdown
## Technical Uncertainties (for Architecture)

These require technical research, not stakeholder input:

1. FR-015: Processing approach (sync/async) - arch-lead to evaluate
2. NFR-003: Database selection based on scale requirements
```

---

## Deferral

Some questions can't be answered yet. Mark as deferred:

```markdown
- FR-020: System MUST integrate with payment provider [DEFERRED: vendor selection pending]
```

Deferred items:
- Don't block spec completion
- Must have clear unblock condition
- Tracked in clarification log

---

## Completion Criteria

Clarify session complete when:

1. All explicit markers addressed (resolved or deferred)
2. No implicit ambiguities in P1 scenarios
3. Coverage summary shows no Outstanding in critical categories
4. Remaining markers ≤ 3 (threshold for arch-lead handoff)

---

## Output

Updates to:
- `.opencode/specs/{slug}/spec.md` - markers replaced with answers
- `.opencode/specs/{slug}/clarifications/log.md` - decision history

Commit changes:
```bash
git add .opencode/specs/{slug}/
git commit -m "clarify: resolve {N} uncertainties in {slug}"
```

---

## Constraints

- Maximum 5 questions per session (avoid fatigue)
- Multiple choice whenever possible
- Open-ended answers ≤5 words
- Update spec immediately after each answer
- Never resolve technical uncertainties (arch-lead's job)
- Always log decisions with rationale
