---
name: pm-remember
description: Retrieve specific knowledge from the PM vault — find decisions about a technology, look up the state of an issue, recall what was decided in a sprint, search for enforcement lessons. The semantic recall interface. Triggers on "/pm-remember", "what do we know about", "look up", "recall", "find decisions about", "what's the status of".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- The ARGUMENTS are the query. Parse the intent:
  - Technology query: "what do we know about QFTest" → search by technology
  - Issue query: "status of SA-3" → find issue decision
  - Sprint query: "what happened in sprint 3" → find sprint record
  - Enforcement query: "validation requirements" → find enforcement decisions
  - General query: search broadly, report what's found

**START NOW.**

---

## Philosophy

**Recall is only valuable if it's accurate and complete. /pm-remember searches the actual vault.**

The PM agent has implicit knowledge from its training. But for this project specifically — which decisions were made, what was discovered in Sprint 3, what is the current status of issue SA-3 — the authoritative source is the vault. /pm-remember forces retrieval from the vault rather than relying on training-time knowledge or session context that may be incomplete.

This matters because the vault is updated over time. The training-time "knowledge" about a decision is the knowledge at training time — which for a fast-moving project means it may already be outdated. The vault's last_reviewed date and meta_state field tell you whether information is current.

/pm-remember reads first, then synthesizes. It does not answer from memory.

---

## Query Parsing

| Query pattern | Strategy |
|--------------|----------|
| "what do we know about [technology]" | Search by technology keyword in decisions/ |
| "status of [issue ID]" | Find issue decision by issue_id field |
| "sprint N" | Find sprint-record decision for that sprint |
| "what was decided about [topic]" | Keyword search + register navigation |
| "enforcement rules" | Read enforcement-register.md |
| "open issues" | Find all issue decisions with status: open |
| "team patterns" | Read ops/observations/ |

---

## Workflow

### 1. Parse Query Intent

From ARGUMENTS, determine: technology lookup, issue lookup, sprint lookup, topical search, or enforcement search.

### 2. Execute Targeted Search

```bash
# Technology search
rg -i "[technology keyword]" decisions/ --include="*.md" -l

# Issue ID search
rg "issue_id: [ID]" decisions/ --include="*.md" -l

# Sprint search
ls decisions/sprint-*.md | grep "[N]"

# Topical search — read the relevant register first
cat decisions/[topic]-register.md

# Enforcement search
cat decisions/enforcement-register.md

# Open issues
rg "^status: open" decisions/ --include="*.md" -l
rg "^type: issue" decisions/ --include="*.md" -l
```

### 3. Read Full Decisions

For each candidate found, read the full decision note. Do not summarize from just the YAML front matter — the body contains the reasoning.

### 4. Synthesize and Present

Present findings organized by relevance:
- Most relevant decision(s) first
- Current status clearly stated
- meta_state prominently noted (current vs outdated)
- Last reviewed date
- Any tensions or contradictions flagged

---

## Output Format

```
## Recall: "[query]"

### Found N relevant decisions

---

**[[decision-title]]**
Type: tech-fact | Status: active | meta_state: current | Last reviewed: YYYY-MM-DD

[Summary of body in 2-3 sentences]

Key claim: [the title stated as a fact]
[Any caveats or related tensions]

---

**[[decision-title-2]]** (less relevant)
...

---

### Not Found
[If nothing relevant found: honest statement + suggestion for where to look or what to document]

### Staleness Warning
[If relevant decisions have meta_state: outdated or last_reviewed > 14 days]

### Suggested Follow-Up
- /pm-learn [if the user is correcting outdated information]
- /pm-update [if status needs to change]
- /pm-document [if this knowledge isn't documented yet]
```

---

## Recall Quality Standards

- NEVER answer from training knowledge when the vault has a decision on this topic
- ALWAYS note meta_state and last_reviewed — staleness is part of the answer
- ALWAYS flag contradictions between what was found and what the user seems to expect
- If the vault has no decision on this topic, say so clearly — that's useful information about vault gaps
