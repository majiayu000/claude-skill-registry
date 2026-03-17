---
name: pm-document
description: Extract structured decisions from source material — sprint outputs, team reports, issue investigations, security audits. Comprehensive extraction is the default. Every architectural decision, tech fact, enforcement lesson, and sprint outcome that serves PM coordination gets documented. Triggers on "/pm-document", "/pm-document [file]", "extract decisions", "document this sprint", "process this report".
version: "1.0"
generated_from: "arscontexta-v1.6"
user-invocable: true
allowed-tools: Read, Write, Grep, Glob
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary mapping. Key terms:
- `vocabulary.notes` = "decisions" (folder)
- `vocabulary.note` = "decision"
- `vocabulary.reduce` = "document"
- `vocabulary.cmd_reflect` = "/pm-link"
- `vocabulary.extraction_categories` = PM-specific categories

Read `ops/config.yaml` for processing depth and chaining mode.

---

## THE MISSION

You are the PM documentation engine. Sprint outputs, security audit findings, team reports, and issue investigations enter. Structured, atomic decision notes exit. Your judgment must err toward documentation, not omission.

**What to extract for PM coordination:**

| Category | What to Find | Output Type |
|----------|--------------|-------------|
| Architectural decisions | Major design choices with rationale and trade-offs | decision (type: architectural) |
| Technology facts | Ignition class names, QFTest casing, Docker patterns, Dulwich behavior | decision (type: tech-fact) |
| Enforcement lessons | Process patterns learned from sprint failures or agent corrections | decision (type: enforcement) |
| Issue states | Known issues with lifecycle status | decision (type: issue) |
| Sprint records | Sprint outcomes: teams deployed, health metrics, what was accepted/rejected | decision (type: sprint-record) |
| Team patterns | Observations about agent team performance | observation (ops/observations/) |
| Tensions | Contradictions between decisions or approaches | tension (ops/tensions/) |

**Invalid skip reasons:**
- "we already know this" — DOING is not DOCUMENTING. The articulated decision needs externalization.
- "it's in the code" — code is implementation, not the reasoning WHY
- "obvious" — obvious to whom? Future sessions need explicit decisions.
- "covered in STATUS.md" — STATUS.md is status, not decision rationale

**For PM-relevant sources: skip rate < 10%. Zero extraction from a sprint output = BUG.**

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If target contains a file path: extract decisions from that file
- If target is empty: scan inbox/ for unprocessed items, pick one
- If target is "inbox" or "all": process all inbox items sequentially

**Execute these steps:**

1. Read the source file fully
2. Identify what type of source this is: sprint output, team report, security audit, issue investigation, project review
3. For each candidate decision:
   - Determine its type (architectural, tech-fact, enforcement, issue, sprint-record)
   - Check if a decision note already exists for this topic (grep decisions/ by title keywords)
   - If near-duplicate: create enrichment task (update existing note's status or rationale)
   - If new: classify and prepare for creation
4. Present extraction report with titles, types, rationale — grouped by decision type
5. Wait for user approval before creating files
6. Create approved decision notes using template from templates/decision-note.md
7. Suggest /pm-link as next step

**START NOW.**

---

## Workflow

### 1. Orient

Before reading source, understand what already exists:

```bash
for f in decisions/*.md; do
  [[ -f "$f" ]] && echo "=== $(basename "$f" .md) ===" && rg "^description:" "$f" -A 0
done
```

Scan descriptions to prevent duplicate extraction.

### 2. Read Source Fully

Read the ENTIRE source. What sprint is this from? What teams were deployed? What issues were identified or resolved? What architectural choices were made?

### 3. Categorize First, Then Route

STOP. Before filtering, determine the category of each candidate:

| Category | Route |
|----------|-------|
| Architectural decision | -> decision note (skip selectivity gate) |
| Technology fact | -> decision note (skip selectivity gate) |
| Enforcement lesson | -> decision note (skip selectivity gate) |
| Issue state | -> decision note (skip selectivity gate) |
| Sprint record | -> decision note (skip selectivity gate) |
| Team pattern observation | -> ops/observations/ note |
| Tension/contradiction | -> ops/tensions/ note |

### 4. Check for Existing Decisions

```bash
rg "QFTest" decisions/ --include="*.md" -l
rg "issue_id:" decisions/ --include="*.md" -A 1
```

Near-duplicate? Update the existing note's status or add context rather than creating a duplicate.

### 5. Present Findings

```
Documentation scan complete.

SUMMARY:
- Architectural decisions: N
- Technology facts: N
- Enforcement lessons: N
- Issue states: N
- Sprint records: N
- Team patterns (ops/observations/): N
- Tensions (ops/tensions/): N
- Enrichment tasks (update existing): N
- Skipped: N

---

ARCHITECTURAL DECISIONS:
1. [decision as claim] — sprint N, connects to [[existing decision]]

TECHNOLOGY FACTS:
1. [fact as claim] — technology: Ignition/QFTest/Docker, validated against: [source]

ENFORCEMENT LESSONS:
1. [lesson as claim] — learned sprint N, pattern: [brief]

ISSUE STATES:
1. [issue ID] [issue title] — status: open/resolved, discovered: YYYY-MM-DD

SPRINT RECORDS:
1. Sprint N — teams: [list], health: before/after

ENRICHMENT TASKS:
1. [[existing decision]] — source adds [what is missing]

SKIPPED (truly nothing to add):
- [description] — why
```

Wait for user approval before creating files.

### 6. Create Decision Notes

Use templates/decision-note.md structure. Every note must have:
- Title: prose claim ("this decision argues that [title]" must work)
- description: adds information beyond title
- type, status, meta_state, last_reviewed
- topics: links to relevant decision registers
- Body: reasoning, not just assertion (150-400 words)
- Source footer linking back to the source

### 7. Quality Gates

Before writing each note:
- Title passes the claim test ("this decision argues that [title]")
- description adds information beyond the title
- Body shows reasoning with connective words (because, but, therefore)
- At least one decision register linked in topics
- Source attribution present
- meta_state and last_reviewed set

---

## Pipeline Chaining

After documentation completes:
- **manual:** Output "Next: /pm-link [created decisions]"
- **suggested:** Output next step AND add to ops/queue/queue.json
- **automatic:** Queue entries created and processing continues

---

## Critical

Never auto-document. Always present findings and wait for user approval.

For PM-relevant sources, every sprint outcome, architectural discussion, and team deliverable contains documentable decisions. Skip rate < 10% for sprint outputs.
