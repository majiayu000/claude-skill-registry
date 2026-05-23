---
name: recover-context
description: Recover from missing workspace context
---

# Recover Context

Uses **Orchestrator**. When the AI agent encounters insufficient context to proceed, this provides a structured protocol for acknowledging the gap, describing what's missing, and offering recovery paths.

**Prerequisites:** Agent has identified a context gap, work is blocked by missing information

---

## Protocol

When context is insufficient:

1. **Stop** — Do not proceed with incomplete information
2. **Describe** — State what was attempted and what's missing
3. **Offer options** — Provide structured recovery paths from below

**You MUST NOT:**

- Invent information
- Guess at conventions or patterns
- Proceed without acknowledging the gap
- Claim to have scanned when it hasn't

---

## Recovery Options

### Option 1: Point to Docs

If the information exists somewhere, the human points to it:

> "Look at docs/architecture/caching.md"

The agent reads it and integrates relevant context.

### Option 2: Direct Answer

The human provides the information directly:

> "We use Redis for caching with a 5-minute TTL by default"

The agent records it in workspace context for future reference.

### Option 3: Create Missing Doc

If the information should be documented but isn't, collaboratively create it.

### Option 4: Proceed with Assumptions

For low-risk situations, state assumptions explicitly:

> "I'll assume X. Please correct if wrong."

---

## Output

```markdown
## Context Anchors

- **Phase:** Context Recovery
- **Blocked on:** <what's missing>

## Context Gap

**What was attempted:** <action that revealed the gap>

**What's missing:** <specific information needed>

**Why it's needed:** <how it blocks progress>

## Recovery Options

1. Point me to the relevant documentation
2. Tell me directly
3. Let's create the missing documentation
4. I'll proceed with these assumptions: <list assumptions>

## Next Step

Awaiting guidance on which recovery option to use.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human provides context recovery guidance.

---

## Error Handling

| Error                        | Recovery                                  |
| ---------------------------- | ----------------------------------------- |
| Human doesn't know either    | Escalate or document as unknown           |
| Pointed doc doesn't exist    | Note the gap, offer to create it          |
| Multiple conflicting sources | Flag conflict, ask which is authoritative |
