---
name: decontextualize
description: Course-correct when artifacts overfit to conversation context. Invoke when examples, names, or language are too specific to current work.
---

# Decontextualize

You're overfitting to the current conversation. The artifact you're creating will outlive this context.

## The Problem

When you have rich context (current task, domain jargon, specific examples), you default to using it—even when the artifact should be portable. You optimize for the current conversation instead of the future reader.

## Symptoms

- Examples drawn from current work ("Add validation to the user signup flow")
- Domain jargon the reader won't know
- Phrasing that mirrors the user's exact words instead of standing alone
- References that require conversation history to understand

## The Fix

**1. Identify the artifact's audience**

| Artifact          | Audience               | Context they have |
| ----------------- | ---------------------- | ----------------- |
| Commit message    | Repo contributors      | Repo history      |
| PR description    | Reviewers              | Repo + diff       |
| Config/rules file | Future self, strangers | None              |
| Library docs      | External users         | None              |
| Skill/prompt      | Any project            | None              |

**2. Apply the stranger test**

> "Would someone with zero context about this conversation understand this?"

If any example, term, or reference requires conversation history—replace it.

**3. Genericize examples**

| Before (context-bound)            | After (portable)             |
| --------------------------------- | ---------------------------- |
| "Fix the auth bug in UserService" | "Fix authentication timeout" |
| "Update the Client class"         | "Update the API client"      |
| "like we discussed"               | [remove or specify]          |

**4. Check your language**

- Don't parrot the user's exact phrasing if it's overly specific
- Use terminology that's standard in the domain, not coined in-conversation
- Write for the stranger who arrives later

## On Activation

1. Identify which artifact is overfitting
2. List the context-bound elements
3. Propose generic replacements
4. Apply the fix

No preamble. Just fix it.
