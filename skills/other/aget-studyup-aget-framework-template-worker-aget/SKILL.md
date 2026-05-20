---
name: aget-studyup
description: Research a topic across the knowledge base before implementation. Searches L-docs, patterns, PROJECT_PLANs, SOPs, and governance for relevant context.
version: 1.0.0
---

# /aget-studyup

Focused KB research on a specific topic before proposing changes or starting implementation.

## Purpose

Per L335 (Memory Architecture) and PATTERN_step_back_review_kb, this skill enables targeted research across the knowledge base. Use it to gather context and precedents before implementing changes.

## Input

$ARGUMENTS - The topic to research (required)

Examples:
- `/aget-studyup release` — Research release-related artifacts
- `/aget-studyup skills` — Research skill-related context
- `/aget-studyup L477` — Find references to specific L-doc

## Execution

### Step 1: Validate Input

If no topic provided, prompt user:

> **Topic required**
>
> Usage: `/aget-studyup <topic>`
>
> Example: `/aget-studyup release`

### Step 2: Run Study Up Script

```bash
python3 scripts/study_up.py --topic "$ARGUMENTS"
```

The script searches 5 KB areas:
- L-docs (`.aget/evolution/L*.md`)
- Patterns (`docs/patterns/PATTERN_*.md`)
- PROJECT_PLANs (`planning/PROJECT_PLAN*.md`)
- SOPs (`sops/SOP_*.md`)
- Governance (`governance/*.md`)

### Step 3: Present Findings

Display results in this format:

```
=== /aget-studyup: {topic} ===

L-docs Found: [count]
  - L###: {title} ({match_count} matches)
  - ...

Patterns Found: [count]
  - PATTERN_{name}: {matches}

PROJECT_PLANs Found: [count]
  - {plan_name}: {status}

SOPs Found: [count]
  - SOP_{name}: {matches}

Governance: [count]
  - {file}: {matches}

Recommendation:
  [coverage assessment based on findings]
```

### Step 4: Suggest Next Steps

Based on findings, suggest:
- Specific L-docs to read in detail
- Active PROJECT_PLANs to be aware of
- Governance constraints that apply

## Output Modes

### Human-Readable (default)
```bash
python3 scripts/study_up.py --topic "$ARGUMENTS"
```

### JSON (programmatic)
```bash
python3 scripts/study_up.py --topic "$ARGUMENTS" --json
```

### Quiet (minimal)
```bash
python3 scripts/study_up.py --topic "$ARGUMENTS" --quiet
```

## Constraints

- **C1**: Topic argument is REQUIRED. Do not run without a topic.
- **C2**: Read-only operation. Never modify KB files.
- **C3**: Present findings objectively. Let user decide relevance.
- **C4**: If topic returns 0 results, report "No matches found" and suggest alternative search terms.

## When to Use

| Scenario | Use /aget-studyup |
|----------|-------------------|
| Before implementing a feature | Yes — check for related patterns |
| Before creating L-doc | Yes — avoid duplicating existing learnings |
| User asks about existing work | Yes — surface relevant artifacts |
| Quick file lookup | No — use grep/glob directly |

## Related Skills

- `/aget-wake-up` — Session initialization (broader context load)
- `/aget-check-health` — Health verification
- `/aget-check-evolution` — Evolution directory health
- `/aget-record-lesson` — Capture new learnings

## Traceability

| Link | Reference |
|------|-----------|
| Script | `scripts/study_up.py` |
| Spec | AGET_SESSION_SPEC.md (CAP-SESSION-007) |
| Pattern | PATTERN_step_back_review_kb.md |
| L-docs | L335 (Memory Architecture), L187 (Silent Execution) |
| Tests | tests/test_session_protocol.py::TestStudyUpProtocol (6 tests) |

---

*aget-studyup v1.0.0*
*Category: Research*
*Based on CAP-SESSION-007 (Study Up Protocol)*
