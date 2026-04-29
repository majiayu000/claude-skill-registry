---
name: audit-context
user-invocable: true
description: |
  Evaluates ambient context artifacts (CLAUDE.md, memory, local skills, settings hooks) for compatibility with swarm governance. Returns a classified report so users can address interference before launching a team.
keywords: audit, context, interference, CLAUDE.md, memory, skills, hooks, compatibility
---

# Audit Context

Evaluate the user's ambient context artifacts for compatibility with swarm's governance rules. You are a read-only diagnostic — never modify any files.

## What to scan

1. **CLAUDE.md files.** Read the project's `CLAUDE.md` (working directory root). If `.claude/CLAUDE.md` exists, read that too. Also check `~/.claude/CLAUDE.md` (global config) — it loads into every session.
2. **Memory files.** Find the project memory path by checking `~/.claude/projects/` for a directory matching the current working directory. Claude Code dash-encodes the project path (e.g., `/Users/foo/my-project` becomes `-Users-foo-my-project`). If a `memory/MEMORY.md` index exists, read it and follow links to individual memory files.
3. **Local skills and commands.** List `.claude/skills/` and `.claude/commands/` in the project directory. Flag any skill whose name matches a swarm built-in: `suggest-members`, `refine-outcomes`, `define-rubric`, `resolve-dispute`, `writing-style`, `code-mode`, `writing-mode`, `general-mode`, `workflow-rules`, `audit-context`.
4. **Settings hooks.** Check both `.claude/settings.json` (project) and `~/.claude/settings.json` (global) for a `hooks` section. Flag any hook that intercepts tools used by swarm (TeamCreate, Agent, SendMessage, CronCreate).
5. **Auto mode environment.** Check `~/.claude/settings.json` for `autoMode.environment`. If it is absent or contains no string mentioning a source-control hostname (`github.com`, `gitlab.com`, `bitbucket.org`, or any host matching the working directory's `git remote get-url origin`), flag this — the team's ship phase (commit/push/PR) will stall on classifier prompts in auto mode without it.

## How to classify

For each artifact, classify as one of three categories:

- **Complementary** — Does not conflict with any swarm rule. Style preferences (brevity, tone, formatting), domain conventions, and tool permissions are complementary by default. No action needed.
- **Potentially Interfering** — Could conflict with a swarm rule depending on context. The artifact's intent is benign but its phrasing is broad enough to suppress or alter expected swarm behavior. Worth reviewing.
- **Conflicting** — Directly contradicts a named swarm governance rule. Will likely cause unexpected behavior during a team run. Should be addressed before launching.

## Swarm governance rules to evaluate against

These are the rules that matter for interference detection:

### Workflow control
- After greenlight, execution is autonomous — no mid-phase confirmations unless escalating per hard rules.
- The user's request wording is not a greenlight — members wait for the lead to assign work.
- Phase transitions require facilitator signals (RESEARCH COMPLETE, CONVERGED, CONFIDENCE REACHED).
- Final delivery requires explicit user sign-off.

### Communication
- facilitator signal obligations are protocol mechanics — they must be sent regardless of communication preferences.
- Favor brevity during roundtables. No idle chatter.
- SendMessage is the only channel between teammates — plain text output dies with the turn.

### Execution
- All members except the lead are read-only.
- The lead is the sole executor — only the lead writes, edits, or runs commands.
- No code changes during review rounds.
- Wait for ALL reviews before making changes.

### Team structure
- Briefing templates are fixed — no added sections, task framing, or acknowledgment rituals.
- Hard rules are non-negotiable and take precedence over ambient preferences.

## Common interference patterns

Flag these specific patterns when you encounter them:

| Pattern | Example | Classification | Conflicting rule |
|---|---|---|---|
| Confirmation injection | "Always confirm before editing" | Conflicting | Autonomous post-greenlight execution |
| Auto-commit/push | "Commit after completing work" | Conflicting | Final delivery requires user approval |
| Silence preferences | "Don't repeat yourself", "Stay silent while waiting" | Potentially Interfering | facilitator signal obligations |
| Verbosity injection | "Explain your reasoning step by step" | Potentially Interfering | Favor brevity during roundtables |
| Methodology injection | "Always use TDD", "Write tests first" | Potentially Interfering | Phase arc is defined by mode skill |
| Tool restrictions | "Never use TeamCreate", "Don't spawn agents" | Conflicting | Always use TeamCreate |
| Briefing expansion | "Add detailed context to all briefs" | Conflicting | Briefing templates are fixed |
| Skill name collision | Local `suggest-members` skill | Conflicting | Shadows swarm built-in |
| Hook tool interception | Hook that blocks TeamCreate or SendMessage | Conflicting | Team creation and communication require these tools |
| Auto mode setup gap | `~/.claude/settings.json` missing `autoMode.environment` source-control trust | Potentially Interfering | Ship phase requires source-control trust in user-scope settings (run `/swarm:launch` for the host-specific block) |

## Output format

Present findings as a structured report grouped by source:

```
## Audit Results

### CLAUDE.md — [path]
- [excerpt] — **[Classification]** — conflicts with: [rule name]. [One-line recommendation.]

### Memory — [path]
- [excerpt] — **[Classification]** — conflicts with: [rule name]. [One-line recommendation.]

### Local Skills / Commands
- [name] — **[Classification]** — [reason]. [One-line recommendation.]

### Settings Hooks — .claude/settings.json
- [hook name / tool target] — **[Classification]** — [reason]. [One-line recommendation.]

### Summary
- Complementary: [count]
- Potentially Interfering: [count]
- Conflicting: [count]
```

If no artifacts are found, say so. If all artifacts are complementary, say "No interference detected — your environment is clean for swarm runs."
