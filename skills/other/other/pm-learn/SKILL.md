---
name: pm-learn
description: Capture a specific insight, tech fact, or enforcement lesson in-flight during a session — without going through the full /pm-document pipeline. Quick capture for things discovered during team coordination that shouldn't wait for the end-of-session wrap-up. Triggers on "/pm-learn", "remember this", "capture this fact", "note this lesson", "quick capture".
user-invocable: true
allowed-tools: Read, Write, Grep, Glob
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary and decision types.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- The ARGUMENTS are the thing to capture. Parse what type of knowledge this is:
  - Tech fact: specific behavior of Ignition, QFTest, Docker, Dulwich, etc.
  - Enforcement lesson: process failure or correction learned
  - Architectural decision: design choice with rationale
  - Observation: team pattern or PM system friction
- Create the appropriate decision note immediately.

**Example invocations:**
- `/pm-learn QFTest's Groovy interpreter field is case-sensitive: must be "Groovy" not "groovy"`
- `/pm-learn deploy-arch-team consistently omits alternatives_considered in deliverables`
- `/pm-learn validation block must be embedded at Step 1, not Step 3`

**START NOW.**

---

## Philosophy

**Insights that aren't captured within the session are often lost. /pm-learn makes capture instant.**

During active coordination work, the PM agent discovers things — team corrections, technology behavior, enforcement gaps — that should be documented. But invoking the full /pm-document pipeline in the middle of active work is disruptive. The pipeline is designed for batch processing of source documents, not for real-time insight capture.

/pm-learn is the interrupt handler. It receives the insight as ARGUMENTS, creates the appropriate decision note immediately using the right template, assigns it to the correct decision register, and returns to the active session. The note will be linked and updated in the next /pm-pipeline pass.

Speed matters here. The note does not need to be perfect — it needs to be captured. It can be enriched later with /pm-review.

---

## Workflow

### 1. Parse the Insight Type

From the ARGUMENTS text, determine:
- **Tech-fact**: mentions a specific technology, class name, behavior, version difference
- **Enforcement**: mentions a process failure, a correction, "must", "required", "always", "never"
- **Architectural**: mentions a design choice, "we decided", "architecture requires"
- **Observation**: mentions a team pattern, agent behavior, PM system friction

### 2. Check for Near-Duplicates

```bash
# Quick check — is this already documented?
rg -i "[key term from insight]" decisions/ --include="*.md" -l | head -5
```

If near-duplicate found: update existing note instead of creating new one.

### 3. Create the Note

Use templates/decision-note.md. Fill in:
- Title: prose claim version of the insight (claim test: "this decision argues that [title]")
- description: one sentence adding mechanism or scope
- type: tech-fact | enforcement | architectural | observation
- status: active (for facts and architectural), speculative (if uncertain)
- meta_state: current
- last_reviewed: today
- topics: best-guess register (will be verified in /pm-link)

Body: 100-200 words minimum. Show the reasoning, not just the assertion.

### 4. Queue for Linking

Add a note to ops/tasks.md: "pm-link [new decision name]"

### 5. Confirm Capture

```
## Captured

[[decision-title]]
Type: tech-fact | enforcement | architectural | observation
File: decisions/[filename].md
Status: active

Queued for linking: yes
Register tentatively assigned: [[register-name]]

Full pipeline (link + update) should run within 2 sessions.
```

---

## Quality Minimum for Quick Capture

Even in quick capture mode, the note must meet:
- Title passes claim test
- Body has at least one connective word (because, therefore, which means)
- Type and status are set
- At least one register tentatively linked in topics

Notes that fail this minimum should be written to ops/observations/ instead as pending observations for later triage.

---

## What /pm-learn is NOT

- NOT a replacement for /pm-document when processing full source documents
- NOT for capturing things that are uncertain (use `status: speculative` and note uncertainty)
- NOT for capturing team deliverables (those go through /pm-document)
- NOT for meta-commentary about the PM system (those go to ops/observations/ via the normal path)
