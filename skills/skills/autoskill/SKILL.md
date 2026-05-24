---
name: autoskill
description: Analyze coding sessions to detect corrections and preferences, then propose targeted improvements to Skills used in the session. Use this skill when the user asks to "learn from this session", "update skills", or "remember this pattern". Extracts durable preferences and codifies them into the appropriate skill files.
license: Complete terms in LICENSE.txt
---

This skill analyzes coding sessions to extract durable preferences from corrections and approvals, then proposes targeted updates to Skills that were active during the session. It acts as a learning mechanism across sessions, ensuring Claude improves based on feedback.

The user triggers autoskill after a session where Skills were used. The skill detects signals, filters for quality, maps them to the relevant Skill files, and proposes minimal, reversible edits for review.

## When to activate

Trigger on explicit requests:

- "autoskill", "learn from this session", "update skills from these corrections"
- "remember this pattern", "make sure you do X next time"

Do NOT activate for one-off corrections or when the user declines skill modifications.

## Signal detection

Scan the session for:

**Corrections** (highest value)

- "No, use X instead of Y"
- "We always do it this way"
- "Don't do X in this codebase"

**Repeated patterns** (high value)

- Same feedback given 2+ times
- Consistent naming/structure choices across multiple files

**Approvals** (supporting evidence)

- "Yes, that's right"
- "Perfect, keep doing it this way"

**Ignore:**

- Context-specific one-offs ("use X here" without "always")
- Ambiguous feedback
- Contradictory signals (ask for clarification instead)

## Signal quality filter

Before proposing any change, ask:

1. Was this correction repeated, or stated as a general rule?
2. Would this apply to future sessions, or just this task?
3. Is it specific enough to be actionable?
4. Is this **new information** I wouldn't already know?

Only propose changes that pass all four.

### What counts as "new information"

**Worth capturing:**

- Project-specific conventions ("we use `cn()` not `clsx()` here")
- Custom component/utility locations ("buttons are in `@/components/ui`")
- Team preferences that differ from defaults ("we prefer explicit returns")
- Domain-specific terminology or patterns
- Non-obvious architectural decisions ("auth logic lives in middleware, not components")
- Integrations and API quirks specific to this stack

**NOT worth capturing (I already know this):**

- General best practices (DRY, separation of concerns)
- Language/framework conventions (React hooks rules, TypeScript basics)
- Common library usage (standard Tailwind classes, typical Next.js patterns)
- Universal security practices (input validation, SQL injection prevention)
- Standard accessibility guidelines

If I'd give the same advice to any project, it doesn't belong in a skill.

## Mapping signals to Skills

Match each signal to the Skill that was active and relevant during the session:

- If the signal relates to a Skill that was used, update that Skill's `SKILL.md`
- If 3+ related signals don't fit any active Skill, propose a new Skill
- Ignore signals that don't map to any Skill used in the session

## Proposing changes

For each proposed edit, provide:

```
File: path/to/SKILL.md
Section: [existing section or "new section: X"]
Confidence: HIGH | MEDIUM

Signal: "[exact user quote or paraphrase]"

Current text (if modifying):
> existing content

Proposed text:
> updated content

Rationale: [one sentence]
```

Group proposals by file. Present HIGH confidence changes first.

## Review flow

Always present changes for review before applying. Format:

```
## autoskill summary

Detected [N] durable preferences from this session.

### HIGH confidence (recommended to apply)
- [change 1]
- [change 2]

### MEDIUM confidence (review carefully)
- [change 3]

Apply high confidence changes? [y/n/selective]
```

Wait for explicit approval before editing any file.

## Applying changes

When approved:

1. Edit the target file with minimal, focused changes
2. If git is available, commit with message: `chore(autoskill): [brief description]`
3. Report what was changed

## Constraints

- Never delete existing rules without explicit instruction
- Prefer additive changes over rewrites
- One concept per change (easy to revert)
- Preserve existing file structure and tone
- When uncertain, downgrade to MEDIUM confidence and ask
