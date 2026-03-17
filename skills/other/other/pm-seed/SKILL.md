---
name: pm-seed
description: Populate the PM knowledge system from existing project documentation — STATUS.md, KNOWN_ISSUES.md, PROJECT_STATE_REVIEW, security audit reports. The first-sprint bootstrap. Use once when the vault is new and existing project knowledge needs to be captured. Triggers on "/pm-seed", "seed from docs", "bootstrap vault", "import existing knowledge".
user-invocable: true
allowed-tools: Read, Write, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary.
Read `ops/config.yaml` for processing depth.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: seed from all known project documentation sources
- If path provided: seed from that specific file
- If "issues": seed from KNOWN_ISSUES.md only
- If "review": seed from the PROJECT_STATE_REVIEW report only
- If "security": seed from security audit reports only

**START NOW.**

---

## Philosophy

**The vault is only useful if it contains knowledge. /pm-seed closes the gap between "vault exists" and "vault is valuable."**

When the PM knowledge system is first created, it is structurally complete but epistemically empty. The project has history — decisions were made, issues were discovered, sprints were run, architectural choices were documented — but none of it is in the vault yet. Every session without seeding is a session where the PM agent operates without institutional memory.

/pm-seed is the bootstrap operation. It reads existing project documentation and runs the same extraction logic as /pm-document, but with awareness that it is creating the initial corpus rather than enriching an existing one. The seeding process should be comprehensive — it is acceptable to err toward over-extraction here, since the /pm-retrospect loop will trim what doesn't prove useful.

/pm-seed is not a one-time operation. Run it whenever a major new source of project knowledge is added (a new audit report, a milestone post-mortem, a major architecture documentation).

---

## Known Seed Sources

For this project, the following sources contain extractable decisions:

| Source | Location | Expected Decisions |
|--------|----------|-------------------|
| Project state review | `docs/Reports/PROJECT_STATE_REVIEW_2026-02-19.md` | Sprint records, issue states, health metrics, architectural decisions |
| Security audit | `docs/Reports/SECURITY_AUDIT_2026-02-19.md` | Enforcement lessons, architectural decisions, issue states |
| Status document | `docs/STATUS.md` | Feature status, tech facts, architectural decisions |
| Known issues | `docs/KNOWN_ISSUES.md` | Issue states, tech facts |
| Main context | `.claude/CLAUDE.md` | Tech facts, architectural decisions, enforcement lessons |

---

## Workflow

### 1. Inventory Existing Decisions

Before seeding, understand what already exists to avoid duplicates:

```bash
for f in decisions/*.md; do
  [[ -f "$f" ]] && rg "^description:" "$f" | head -1
done
```

### 2. Read Each Source Fully

For each source file, read the entire content. Do not skim.

### 3. Extract with PM Categories

Apply the same extraction logic as /pm-document:
- Architectural decisions → decisions/ (type: architectural)
- Technology facts → decisions/ (type: tech-fact)
- Enforcement lessons → decisions/ (type: enforcement)
- Issue states → decisions/ (type: issue)
- Sprint records → decisions/ (type: sprint-record)
- Team patterns → ops/observations/
- Tensions → ops/tensions/

### 4. Batch Present for Approval

Since seeding can produce 20-50 decisions from a single source, group them by type and present in batches. Do not auto-create.

### 5. Create Approved Decisions

Use templates/decision-note.md for all decision types.
Use templates/sprint-record.md for sprint records.
Use templates/observation-note.md for observations.

### 6. Seed the Health Log

After seeding sprint records, populate ops/health/health-log.md with the health trajectory:

```markdown
## Health Log

| Sprint | Health Before | Health After | Delta | Key Change |
|--------|--------------|-------------|-------|------------|
| 1 | 31 | 45 | +14 | Security remediation |
```

---

## Output Format

```
## Seed Extraction Complete — [source file]

### Found
- Architectural decisions: N
- Technology facts: N
- Enforcement lessons: N
- Issue states: N (open: N, resolved: N)
- Sprint records: N
- Team patterns: N
- Tensions: N

[Grouped presentation by type — same format as /pm-document]

---
APPROVE batch? (yes/select/reject)
```

---

## Seed Quality Standards

The same quality gates as /pm-document apply:
- Skip rate < 10% for project state reviews
- Every issue in KNOWN_ISSUES.md becomes an issue decision
- Every sprint mentioned in any document becomes a sprint-record decision
- Tech facts (QFTest casing, class names, Docker patterns) become tech-fact decisions

The vault after seeding should be immediately useful — a new session should be able to read decisions/ and understand the full project history without reading the raw source documents.
