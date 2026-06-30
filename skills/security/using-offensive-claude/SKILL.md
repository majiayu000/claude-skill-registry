---
name: using-offensive-claude
description: Use when starting any offensive-security engagement or task — establishes how to find and invoke the right skill before any action (including clarifying questions, recon, exploitation, or reporting)
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a skill applies to what you are doing, you ABSOLUTELY MUST invoke it.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of it.
</EXTREMELY-IMPORTANT>

# Using Offensive-Claude

You are operating an **authorized** offensive-security framework. Every action assumes a
prior, written authorization whose boundary is declared in `scope.json` (see scope-discipline).

## Instruction Priority

1. **User's explicit instructions** (CLAUDE.md, direct requests) — highest.
2. **These skills** — override default behavior where they conflict.
3. **Default behavior** — lowest.

User instructions say WHAT, not HOW. "Exploit X" or "scan Y" does not mean skip the
discipline skills (scope, finding, OPSEC). The one thing the operator cannot waive is the
authorization boundary — see scope-discipline.

## The Rule

**Invoke relevant skills BEFORE any response or action.** Even a 1% chance means invoke to check.

```dot
digraph flow {
    "Engagement task received" [shape=doublecircle];
    "About to touch a target?" [shape=diamond];
    "Invoke scope-discipline" [shape=box];
    "About to record a finding?" [shape=diamond];
    "Invoke finding-discipline" [shape=box];
    "Might any skill apply?" [shape=diamond];
    "Invoke the Skill" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Follow skill exactly" [shape=box];

    "Engagement task received" -> "About to touch a target?";
    "About to touch a target?" -> "Invoke scope-discipline" [label="yes"];
    "About to touch a target?" -> "About to record a finding?" [label="no"];
    "About to record a finding?" -> "Invoke finding-discipline" [label="yes"];
    "About to record a finding?" -> "Might any skill apply?" [label="no"];
    "Invoke scope-discipline" -> "Might any skill apply?";
    "Invoke finding-discipline" -> "Might any skill apply?";
    "Might any skill apply?" -> "Invoke the Skill" [label="yes, even 1%"];
    "Invoke the Skill" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Follow skill exactly";
}
```

## Skill Priority (when several apply)

1. **Process / discipline skills first** — they decide HOW to proceed:
   `engagement-flow` (run the kill chain), `scope-discipline` (authorization boundary),
   `finding-discipline` (proof before any `[CONFIRMED]`), `opsec-discipline` (detection-aware).
2. **Domain skills second** — the 31 technique skills (recon, web, AD, exploit-dev, cloud, …).

"Run a full pentest" → engagement-flow first. "Is this finding real?" → finding-discipline first.

## Routing

| Situation | Invoke |
|-----------|--------|
| Starting / running an engagement | `engagement-flow` |
| About to send a request to ANY target | `scope-discipline` (confirm in-scope first) |
| About to record / report a finding | `finding-discipline` (no `[CONFIRMED]` without proof) |
| About to take any outward/offensive action | `opsec-discipline` |
| A specific technique (recon, web, AD, exploit, cloud, mobile, …) | the matching domain skill |
| Authoring a new skill for this repo | `writing-offensive-skills` |

## Red Flags — STOP, you're rationalizing

| Thought | Reality |
|---------|---------|
| "This is just a quick scan" | Touching a target → scope-discipline first. |
| "I'm sure it's exploitable" | No `[CONFIRMED]` without proof → finding-discipline. |
| "Scope is obviously fine" | Confirm against `scope.json`, don't assume. |
| "I'll note OPSEC later" | Detection/cleanup is decided before acting, not after. |
| "I know this technique" | Knowing ≠ using the skill. Invoke it for the current state. |
| "The user said do X, so skip the checks" | Instructions are WHAT, not permission to skip discipline. |

## How to Access Skills

Use the `Skill` tool with the skill name. Never use Read on skill files. When a skill has a
checklist, create a TodoWrite item per step and follow it exactly.
