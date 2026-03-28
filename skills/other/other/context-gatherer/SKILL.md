---
name: context-gatherer
description: Phase 0.1 — Automatic codebase scan before PRD generation. Extracts key terms from the user prompt, searches the codebase for related files, identifies existing patterns, and generates context.md in the state directory.
---

# Context Gatherer

Runs **automatically as Phase 0.1**, before `idea-explorer` asks its first question.
Purpose: ground the entire spec in the actual codebase — not assumptions.

## When to run

- Always runs before the first `idea-explorer` question
- Skips if `.claude/feature-state/{slug}/context.md` already exists (resume)
- Can be forced with `--recontextualize`

## Step 1: Extract key terms from the user prompt

Parse the user's feature prompt for:
- **Entities**: nouns that likely map to data models (e.g., "student", "trainer", "subscription")
- **Actions**: verbs that describe behavior (e.g., "connect", "enroll", "notify", "list")
- **Domain words**: business-specific terms (e.g., "checkout", "onboarding", "dashboard")

Example:
```
Prompt: "Allow personal trainers to connect with students after checkout"
Key terms: ["trainer", "student", "connect", "checkout", "personal trainer"]
```

## Step 2: Search the codebase for related files

For each extracted key term, search across the codebase:

```bash
# Search in source files (code, types, schemas)
grep -r "{term}" . \
  --include="*.ts" --include="*.tsx" --include="*.js" \
  --include="*.swift" --include="*.rs" --include="*.py" --include="*.go" \
  -l 2>/dev/null | head -20

# Search in test files
grep -r "{term}" . --include="*test*" --include="*spec*" -l 2>/dev/null | head -10
```

Deduplicate results and score by frequency of term occurrence.
Select the **5–10 most relevant files** (highest term density + most central paths).

## Step 3: Read project context files

Always read these files if they exist:

| File | Purpose |
|------|---------|
| `./CLAUDE.md` | Project-level conventions |
| `./.claude/spec-workflow/PROJECT.md` | Project DNA (architecture rules, constraints) |
| `./README.md` | Project overview |
| `./AGENTS.md` | Agent-specific instructions |
| `./package.json` | Node.js dependencies and scripts |
| `./Cargo.toml` | Rust dependencies |
| `./Package.swift` | Swift dependencies |
| `./go.mod` | Go module info |

## Step 4: Extract existing patterns

From the files identified in Steps 2–3, extract:

### Architecture patterns
- What patterns are in use? (MVVM, Repository, Clean Architecture, MVC, etc.)
- Where are they located in the project?

### Naming conventions
- How are entities named? (camelCase, snake_case, PascalCase)
- How are files named? (feature-name.ts, FeatureName.swift, etc.)

### Similar features
- Is there already a feature similar to what's being requested?
- Which files implement it? What can be reused or extended?

### Existing entities related to the prompt
- Do any of the key terms already have implementations?
- What fields, methods, or relationships do they already have?

## Step 5: Generate context.md

Save to `.claude/feature-state/{slug}/context.md`:

```markdown
## Context Report

Generated: {timestamp}
Prompt: "{original prompt}"

### Related Files Found
- `path/to/file1` — [why it's relevant, e.g., "implements Student entity"]
- `path/to/file2` — [e.g., "Firestore queries for trainer data"]
- `path/to/file3` — [e.g., "authentication middleware used by all API routes"]

### Existing Patterns
- Architecture: MVVM + Repository + Use Cases
- Auth: Firebase Auth — ID token in Authorization header on all routes
- Data: Firestore with soft delete (status: 'archived')
- Naming: Firebase UIDs stored as 'uid' throughout

### Similar Features Already Implemented
- **Student enrollment** at `src/api/students/` — creates Firestore docs via Cloud Function
- **Trainer profile** at `Presentation/Features/Trainer/` — MVVM pattern, fetches from /api/trainers

### Entities Related to Prompt
- **Student** — exists at `src/types/student.ts`, fields: uid, name, email, trainerId?
- **Trainer** — exists at `src/types/trainer.ts`, fields: uid, name, specialization[]
- **checkout** — Cloud Function `handleCheckoutComplete` creates student records after Stripe payment

### Constraints Detected
- Stripe webhook creates student-trainer relationships — any new connection flow should integrate with this
- FCM token not guaranteed — push notifications are optional for all users
- Feature flags via Firebase Remote Config — new user-facing features need a flag

### What DOESN'T Exist (Relevant to Prompt)
- No direct trainer-student connection endpoint outside of checkout
- No student list view for trainers in CMS
- No real-time listener for connection status
```

## Step 6: Surface to user before first question

Before asking the first `idea-explorer` question, show a summary:

```
📂 Context gathered from codebase:

Related files found: 7
Existing patterns: MVVM + Repository (iOS) / Firebase Auth + Firestore
Similar feature: Student enrollment at src/api/students/

Already exists:
  ✅ Student entity (src/types/student.ts) — has trainerId? field
  ✅ Trainer entity (src/types/trainer.ts)
  ✅ handleCheckoutComplete — creates trainer-student link after Stripe

Gaps detected:
  ❌ No direct connect API outside checkout flow
  ❌ No trainer CMS view of students

Injecting this context into spec generation...
```

## Output location

```
.claude/feature-state/{slug}/context.md
```

This file is:
- **Injected into idea-explorer** as initial context (question framing)
- **Injected into spec-writer** as architectural context
- **Referenced during PRD Validation** to verify entity references
