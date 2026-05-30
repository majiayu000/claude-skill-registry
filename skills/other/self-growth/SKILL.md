---
name: self-growth
description: "Continuous learning framework — learn from work, organize knowledge, build feedback loops. Use when: recording lessons, organizing knowledge, or setting up learning systems that persist across sessions."
---

# Self-Growth Framework

You're an agent that improves over time. Knowledge gained during work shouldn't vanish when a session ends — it should accumulate into reusable assets. But be selective: only accumulate what's within your scope and genuinely reusable.

## References

Load on demand — not every invocation requires all of these:

- [behavior.md](references/behavior.md) — behavioral guidelines (safety, response standards, output format)
- [memory-system.md](references/memory-system.md) — memory write rules
- [memory-advanced.md](references/memory-advanced.md) — group memory, shared knowledge, and advanced features
- [proficiency.md](references/proficiency.md) — skill proficiency tracking

---

## Five-Step Flow

```
Task or knowledge comes in
    ↓
① Scope check: Is this my responsibility?
   ├── No → Hand off (explain why + suggest who + share what you know)
   └── Yes ↓
② Learning filter: Is this worth recording? Will it come up again?
   ├── No → Don't record (or just note in daily log)
   └── Yes ↓
③ Knowledge routing: Where does it go?
   ├── Operational rules (tool quirks, paths, gotchas) → Lessons Learned in CLAUDE.md + memory_store dual-layer
   ├── Reusable knowledge (methods, domain expertise) → knowledge/ (staging) → playbooks/ (validated) → skills/ (formal)
   └── Update existing skill → Direct update
④ Feedback loop: Am I improving?
   ├── Read growth-profile.md "growth signals" and compare against today's work
   ├── Detect: user corrections, task success rate, rework frequency (role-specific signals)
   ├── Recognize: cross-task patterns ("user keeps fixing my X" = persistent weakness)
   └── Calibrate: is this learning aligned with growth direction (Phase 1→2→3)?
⑤ Reflection cadence: When do I do all this?
   └── During daily reflection — execute ①-④ together
```

---

## ① Scope Check

Before acting on a task or recording knowledge, ask:

```
1. Is this within my defined responsibilities?
   └── Clear yes → proceed
   └── Clear no  → hand off
   └── Unclear   → keep checking

2. Does it require my specific expertise?
   └── Yes → likely mine
   └── No  → likely someone else's

3. Will doing this pull me away from core duties?
   └── Yes → hand off
   └── No  → proceed

4. Still unsure?
   └── Ask manager or user
```

**How to hand off well:**
1. **Explain why:** "This involves [X], which is outside my scope"
2. **Suggest who:** "This should go to [person], because they own [Y]"
3. **Share context:** Hand over any relevant information you already have

**Don't:** refuse without giving direction, push through poorly, or quietly log it into your own knowledge base (that pollutes your domain).

### Edge Cases

- **Cross-domain support:** You can read knowledge from other domains to complete your own work — but you don't maintain their knowledge bases.
- **No clear owner:** Judge who it's closest to; if unsure, ask manager.
- **Urgent but out of scope:** Hand off. You can help organize information, but the core work should go to the right person.

---

## ② Learning Filter

Trigger this when you:
- Solve a tricky problem (will this recur?)
- Discover a better approach (method or one-off trick?)
- Complete a complex task (any reusable knowledge in the process?)
- Are about to write a Lessons Learned (is this an operational rule, or should it be a standalone methodology?)
- End a session (anything worth preserving?)

### Routing Decision

```
What I learned
    │
    ├── Operational rule (how tools work, paths, gotchas)
    │   → CLAUDE.md Lessons Learned + memory_store dual-layer (fact + decision)
    │
    ├── Reusable knowledge (methodology, domain expertise)
    │   → knowledge/ → playbooks/ → skills/
    │
    └── One-off, won't repeat
        → Don't record (or just daily log)
```

### Lessons Learned Format

```markdown
### YYYY-MM-DD: One-line description

Content description...
```

When writing to Lessons Learned, **simultaneously** `memory_store` with dual-layer storage (fact + decision).

### Lessons Learned vs. Independent Skill

**CLAUDE.md Lessons Learned holds operational rules only:** how tools work, where paths are, what to do first.

**Methodology/domain knowledge gets its own Skill:** reusable ways of doing things, domain expertise.

**Test:** "Would this knowledge be useful in a different project?" Yes → independent Skill. No → Lessons Learned.

---

## ③ Knowledge Routing

| Type | Where | Naming convention |
|------|-------|------------------|
| Research/reflection notes (staging) | `knowledge/` | `{domain}-{topic}-{aspect}.md` |
| Validated methodology | `playbooks/` | Proven through the full cycle, executable independently |
| Domain expertise | Knowledge Skill | `knowledge-{domain}` |
| Methodology | Method Skill | `method-{topic}` |
| Project decisions | Project Skill | `proj-{project}-{topic}` |
| Deliverables / analysis reports | `output/` | `output/{task-name}/` |
| Daily log | `memory/` | `memory/YYYY-MM-DD.md` |

### Knowledge Lifecycle

```
knowledge/ (staging: things learned, researched, still being digested)
    ↓ validated through real use
playbooks/ (finalized: handoff-ready, executable independently)
    ↓ when it needs to be embedded in the system, go through Layer 3 approval
.claude/skills/ (formal: capabilities bound to the system)
```

### Promotion Signals

Proactively evaluate whether knowledge in `knowledge/` is ready to be promoted:

- Same type of problem appears **3+ times**
- Appears across **2+ different tasks or projects**

Promotion path:
- Operational rule → CLAUDE.md Lessons Learned
- Reusable methodology → `knowledge/` → `playbooks/` → `skills/`

### When to Create a New Skill

1. **Enough content?** — At least 2–3 related knowledge points
2. **Clear boundary?** — Scope is defined; you know what doesn't belong
3. **Correct naming?** — Follows convention (`knowledge-`, `method-`, `proj-`)

---

## ④ Feedback Loop

**Run during daily reflection. Read your workspace's `growth-profile.md`.**

### Three Steps

1. **Signal detection:** Read the "growth signals" in `growth-profile.md`, compare against today's work — did any positive or warning signals appear?
2. **Pattern recognition:** Look for trends across multiple tasks — "user always revises my X" = persistent capability gap; "revision volume is clearly dropping" = improving
3. **Direction calibration:** Align with growth direction (Phase 1→2→3) — "Does this learning move me closer to the next phase?" If what you learned drifts from the direction, note it but don't force a correction (may be exploration)

### Without a growth-profile.md

If your workspace has no `growth-profile.md`, skip this step. The feedback loop requires a manager to define growth signals before it can operate.

If no explicit growth goals exist, focus on:
- Reducing rework (fewer corrections from user)
- Increasing first-attempt success rate
- Expanding the situations you can handle independently

---

## ⑤ Reflection Cadence

During the daily reflection schedule, execute ①–④ together:
- Review today's tasks and learnings
- Check Lessons Learned and `knowledge/` — are there recurring patterns ready to be promoted?
- Execute knowledge routing
- Execute feedback loop
- Log to `evolution/weekly/`

### Reflection Principles

- **Synthesize, don't collect** — Don't repeat what happened during today's work; extract what matters
- **Search when you find gaps** — When you discover a knowledge gap, actively search to fill it; don't just think about it
- **Check against user expectations** — Use the "user expectations" section of CLAUDE.md as the baseline
- **Record or it didn't happen** — Saying "I learned X" without writing it down = didn't learn
- **"Nothing to note" is usually wrong** — Look harder; don't dismiss reflection with a one-liner

---

## Red Lines

1. **Don't record everything** — One-off facts aren't worth the overhead. Be selective.
2. **Don't build catch-all containers** — Each skill/file should have clear scope. Don't dump everything in one place.
3. **Don't record outside your scope** — Valuable knowledge that's not your domain? Pass it to the right owner.
4. **Don't reinvent** — Check if an existing skill/file already covers this before creating new ones.
5. **Don't skip the filter** — Every piece of knowledge goes through ②. No exceptions.
6. **Don't modify Layer 3 files yourself** — Write a proposal to `evolution/proposals/` and wait for approval.

---

## Manager Collaboration

1. **When scope is unclear:** Proactively ask your manager to clarify the boundary.
2. **When you find a gray area:** Report it to the manager and let them decide ownership.
3. **When creating a new Skill:** Notify the manager so they know what you've accumulated.
4. **When growth direction is in question:** Report to the manager; let them update the `growth-profile`.
