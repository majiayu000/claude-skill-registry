---
name: rp-cli-investigate
description: "Deep investigation workflow using rp-cli and RepoPrompt's context builder. Use when investigating bugs, understanding codebases, or tracing issues through complex systems. CRITICAL: Do not timeout rp-cli commands."
---

# Deep Investigation Mode (rp-cli)

Systematic investigation workflow using RepoPrompt's context building capabilities.

## ⚠️ CRITICAL: NO TIMEOUTS

**Do NOT add timeouts to `rp-cli` commands.**

The `builder` command invokes AI-powered context analysis that takes 60-90+ seconds. This is normal. Let it complete.

**Wrong:**
```bash
# ❌ Timeout → "didn't work" → skip to manual file reading
timeout 30 rp-cli -e 'builder "..."'
```

**Right:**
```bash
# ✅ Wait for actual completion
rp-cli -e 'builder "Investigate the auth flow"'
```

**If you bail on `builder` because it "took too long", you are doing it wrong.**

---

## Quick Reference

```bash
# Core exploration
rp-cli -e 'tree'                              # File tree
rp-cli -e 'search "pattern"'                  # Search code
rp-cli -e 'read path/file.swift'              # Read file
rp-cli -e 'structure path/'                   # Code structure

# Context building (THE MAIN TOOL - wait for it!)
rp-cli -e 'builder "instructions" --response-type plan'

# Follow-up in same tab
rp-cli -t '<tab_id>' -e 'chat "follow-up question" --mode plan'
```

---

## Investigation Protocol

### Phase 1: Initial Assessment (BRIEF)

1. Read any provided files/reports (traces, logs, error reports)
2. Summarize symptoms and constraints
3. Form initial hypotheses

**Do NOT do extensive file reading here.** Save deep exploration for `builder`.

### Phase 2: Systematic Exploration via `builder` (REQUIRED)

⚠️ **You MUST call `builder`.** Do not skip this step.

```bash
rp-cli -e 'builder "Investigate: <specific area>

Symptoms observed:
- <symptom 1>
- <symptom 2>

Hypotheses to test:
- <theory 1>
- <theory 2>

Areas to explore:
- <files/patterns/subsystems>
" --response-type plan'
```

**Wait for this to complete.** It will take 60-90+ seconds. That's normal.

### Phase 3: Follow-up Deep Dives

After `builder` returns, continue with targeted questions:

```bash
rp-cli -t '<tab_id>' -e 'chat "<specific follow-up>" --mode plan'
```

### Phase 4: Evidence Gathering

- Check git history for recent relevant changes
- Look for patterns across similar files
- Trace data/control flow through the codebase

### Phase 5: Conclusions

Document:
- Root cause identification (with evidence)
- Eliminated hypotheses (and why)
- Recommended fixes

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| Adding timeouts to `rp-cli` | Commands legitimately take time; timeout ≠ failure |
| Skipping `builder` | You'll miss critical context the AI analysis provides |
| 5+ manual file reads before `builder` | Save deep reading for after context is built |
| Declaring "builder didn't work" after timeout | It was working; you killed it |
| Falling back to manual investigation | The whole point is to use `builder` for context |

---

## Report Template

```markdown
# Investigation: [Title]

## Summary
[1-2 sentence summary]

## Symptoms
- [Observed symptom 1]
- [Observed symptom 2]

## Investigation Log

### Phase - [Area Investigated]
**Hypothesis:** [What you were testing]
**Findings:** [What you found]
**Evidence:** [File:line references]
**Conclusion:** [Confirmed/Eliminated/Needs more investigation]

## Root Cause
[Detailed explanation with evidence]

## Recommendations
1. [Fix 1]
2. [Fix 2]
```
