---
name: faion-project-naming
description: "Generate and validate project/product names. Brainstorm names, check domain availability, validate memorability, check trademarks, verify social handles. Use for naming projects, startups, products."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task
---

# Project Naming Skill

**Communication: User's language. Docs: English.**

## Agents

| Agent | Purpose |
|-------|---------|
| faion-name-generator-agent | Creative brainstorming (opus) |
| faion-domain-checker-agent | Domain verification (sonnet) |

## Workflow

```
GATHER CONCEPT → GENERATE NAMES → USER SELECTS → CHECK DOMAINS → PRESENT RESULTS → WRITE TO CONSTITUTION
     ↑                                                               ↓
     └───────────────── Loop if user wants more ─────────────────────┘
```

## Phase 1: Gather Concept

AskUserQuestion: description, tone (Professional/Playful/Technical/Premium)

Extract: product type, benefits, audience, constraints

## Phase 2: Generate Names (15-20 candidates)

**Strategies:**
- Descriptive (DropBox)
- Invented (Spotify)
- Compound (Facebook)
- Metaphor (Amazon)
- Portmanteau (Pinterest)
- Alliteration (PayPal)

Call `faion-name-generator-agent` agent with context + rejected names.

## Phase 3: User Selection

AskUserQuestion (multiSelect): show names, allow "generate more"

If "generate more" → add to rejected, loop to Phase 2.

## Phase 4: Check Selected

Call `faion-domain-checker-agent` for: .com, .io, .co, GitHub, Twitter

## Phase 5: Present Results

AskUserQuestion: "✅ {name} - select as final" or "🔄 generate more"

If final selected → Phase 6. Else → loop to Phase 2.

## Phase 6: Write to Constitution

Update `aidocs/sdd/{project}/constitution.md`:
```markdown
## Project Identity
- **Name:** {name}
- **Domain:** {name}.com
```

Confirm with next steps: register domain, create GitHub, claim Twitter.

## Scoring

| Factor | Points |
|--------|--------|
| .com available | 10 |
| .io available | 5 |
| No trademark | 5 |
| GitHub available | 3 |
| Twitter available | 3 |
| Easy to spell | 2 |

## Error Handling

- All .com taken → suggest .io, check premium
- Trademark conflict → remove, note reason
- User rejects all → different strategy
