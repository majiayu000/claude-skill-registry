---
name: pm-link
description: Find connections between decisions and update decision registers. Requires semantic judgment to identify genuine relationships — which decisions supersede others, which sprint records validate architectural choices, which issues surfaced tech facts. Use after /pm-document creates decisions. Triggers on "/pm-link", "/pm-link [decision]", "find connections", "update registers".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary mapping. Key terms:
- decisions folder, decision registers, /pm-update as next phase

Read `ops/config.yaml` for processing depth.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If target contains decision name: find connections for that decision
- If target is empty: find connections for recently created decisions
- If target is "recent": find connections for all decisions created today

**Execute these steps:**

1. Read the target decision fully
2. Run discovery: search decision registers + keyword grep for related decisions
3. Evaluate each candidate: does a genuine PM relationship exist?
4. Add inline wiki-links where connections pass the articulation test
5. Update relevant decision registers
6. Report what was connected and why
7. Suggest /pm-update as next step

**START NOW.**

---

## Philosophy

**The decision graph IS the institutional memory.**

Individual decisions are less valuable than their relationships. A decision about QFTest class casing is more valuable when linked to the sprint that discovered it, the issue it resolved, and the enforcement lesson it generated. Connections create compound value as sprints accumulate.

This is not keyword matching. This is PM judgment — understanding what decisions MEAN and how they relate. A decision about "Dulwich for Git repos" deeply connects to "sandbox isolation architecture" even though they share no words.

## PM Connection Types

| Relationship | When to Use |
|-------------|-------------|
| `supersedes` | New architectural decision replaces previous approach |
| `validates` | Sprint outcome confirms a decision was correct |
| `invalidates` | Evidence or sprint result shows previous decision was wrong |
| `implements` | A sprint implemented an architectural decision |
| `surfaces` | An issue surfaced the need for a decision |
| `enforces` | A lesson enforces a process decision |
| `extends` | New decision adds dimension to existing one |
| `contradicts` | Two decisions conflict — creates tension |

**The articulation test:** Complete "[[decision A]] connects to [[decision B]] because [specific reason]". If you cannot fill in a specific reason, the connection fails.

## Workflow

### 1. Understand the Decision

Read the full decision note. What is it deciding? What sprint? What technology? What issue?

### 2. Discovery

**Keyword search by topic:**
```bash
rg "QFTest|Groovy|FPMIApp|Dulwich|Docker" decisions/ --include="*.md" -l
rg "issue_id:" decisions/ --include="*.md" -B 1 -A 3
rg "sprint_number:" decisions/ --include="*.md" -B 1 -A 1
```

**Search by type:**
```bash
rg "^type: tech-fact" decisions/ --include="*.md" -l
rg "^type: enforcement" decisions/ --include="*.md" -l
```

**Read relevant registers:** If the decision is about QFTest, read decisions/qftest-register.md. If it's about an issue, read decisions/issue-register.md.

### 3. Evaluate Connections

For each candidate, can you complete:
> [[decision A]] connects to [[decision B]] because [specific PM reason]

**Valid PM relationship examples:**
- "[[QFTest Groovy casing decision]] connects to [[QF-1A issue]] because the wrong casing WAS the root cause of QF-1A"
- "[[Sprint 5 docker fix]] connects to [[sandbox isolation architecture decision]] because it validates the sidecar approach works"
- "[[validation block enforcement lesson]] supersedes [[informal review approach]] because formal CLAIM/SOURCE/VALIDATION proved necessary after QF-8 Phase 3 failure"

### 4. Add Inline Connections

Connections live in prose, not just footers:

Good: "Since [[QFTest requires Groovy not groovy casing]], all test scripts must use capital-G Groovy in the interpreter field."
Bad: "This relates to [[QFTest casing]]."

### 5. Update Decision Registers

Add decision to appropriate register(s) under Core Decisions. Include context phrase explaining contribution.

Check register size — if approaching 35 decisions, flag for split.

### 6. Output Report

```
## Linking Complete

### Connections Added
[[source decision]]
- -> [[target]] — [relationship type]: [why]
- <- [[incoming]] — [relationship type]: [why]

### Register Updates
[[register name]]
- Added [[decision]] to Core Decisions — [contribution]
- Added to History: Sprint N section

### Synthesis Opportunities
[Decisions that together imply a higher-order architectural insight not yet captured]

### Flagged for Attention
- [[orphan decision]] — could not find connections, needs register assignment
- Tension between [[A]] and [[B]] needs resolution
```

## Quality Gates

- Every connection passes the articulation test
- Inline links read as natural prose
- Decision registers gain synthesis, not just entries
- No links to non-existent files

## Pipeline Chaining

After linking completes:
- **manual:** Output "Next: /pm-update [decisions that affected older decisions' status]"
- **suggested:** Output next step AND advance queue entry phase
