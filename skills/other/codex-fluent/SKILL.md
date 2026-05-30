---
name: codex-fluent
description: Use when Codex feels slow, bloated, or heavy after heavy use. Provides safe session hygiene, archive strategy, and handoff discipline to keep daily Codex usage responsive and low-friction. Always pairs with comprehensive handoffs before archiving active work.
---

# Codex Fluent

Keep Codex feeling fast, light, and pleasant to use over months of heavy daily work.

This skill is about **operational fluency** — the subjective experience of Codex staying responsive, starting quickly, and not forcing you to fight accumulated context and state.

## Core Philosophy

- Fresh small state = speed and low mental load.
- Old work must be preserved, but moved out of the active path.
- **Handoffs are non-negotiable** before archiving anything you might still need.
- Never delete. Archive with clear restore paths.

## When to Use This Skill

- Codex feels laggy on startup or when switching sessions.
- You have many long-running or old chats you rarely touch but don't want to lose.
- Before big maintenance or after noticing session directory growth.
- After a `codex-retrospective` session where Codex itself flagged repeated context bloat or "I keep having to re-explain the current state".

## Safety Rules (Hard)

1. **Inspect first, always.** The first invocation must be report-only.
2. **Handoff before archive.** For any active repo chat you might continue, a high-quality handoff document + reactivation prompt must exist before it is moved to archive.
3. **Backup before mutate.** All changes must be preceded by a timestamped backup.
4. **Archive, never delete.** Sessions, logs, and worktrees are moved to dedicated archive directories (`~/.codex/archived_sessions/`, `archived_worktrees/`, `archived_logs/`).
5. Codex must be closed (or you explicitly accept `--wait-for-codex-exit`) before any filesystem changes to active state.
6. Never touch credentials, global skills you still use, or memory files without explicit confirmation.

## Recommended Cadence

- Heavy daily multi-repo users: weekly report + maintenance when needed.
- Moderate users: every 10–14 days.
- The skill can generate a recurring **report-only reminder** prompt for you.

## Workflow

### 1. Diagnosis (Report Mode)

Ask:
```
Use codex-fluent to inspect my current Codex local state and give me a clear picture of what is causing drag.
```

The skill will report on:
- Active vs archived session sizes
- Largest active sessions and their ages
- Stale worktrees
- Large log files
- Potential thread metadata bloat (title/preview)
- Dead config entries
- Heavy background processes (reported only)

### 2. Handoff Creation (Mandatory for Valuable Work)

Before any archiving of chats you care about, create excellent handoffs.

Use the template in `references/handoff-template.md`.

The reactivation prompt must allow a completely fresh Codex thread (or even Claude via the codex skill) to pick up without the old giant context.

### 3. Apply Maintenance

Only after handoffs exist for everything important:

```
Use codex-fluent to perform safe maintenance now. I have created handoffs for the sessions I want to keep continuity on. Codex is closed.
```

What a normal apply does:
- Timestamped backup to `~/Documents/Codex/codex-backups/codex-fluent-YYYYMMDD-HHMM/`
- Move qualifying old sessions to `~/.codex/archived_sessions/`
- Move stale worktrees to `~/.codex/archived_worktrees/`
- Rotate oversized logs
- Clean dead project entries from config
- Normalize certain path issues where safe

### 4. Verification

Run diagnosis again and compare before/after sizes and feel.

### 5. (Optional) Recurring Reminder

Generate a safe, report-only weekly reminder prompt that never applies changes automatically.

## Integration with Other Arsenal Skills

- After running `codex-retrospective`, if Codex complains about "having to re-read huge context every time" or repeated state loss, this skill is the natural follow-up.
- Use `strategic-compact` thinking when designing handoff documents — they should be the ultimate compact representation of a thread.
- Handoff documents created here are excellent material to feed into future `codex-retrospective` runs.

## What This Skill Will Not Do

- Automatically delete anything.
- Kill processes.
- Touch credentials or irreplaceable memory.
- Archive pinned or explicitly marked "do not touch" sessions without confirmation.
- Promise universal speedups (results depend on your usage patterns).

## References

- `references/handoff-template.md` — High-quality handoff document template + reactivation prompt
- `references/maintenance-checklist.md` — Step-by-step safe maintenance checklist
- `references/examples/` — Real-world (anonymized) before/after reports and handoff examples

## Success Criteria

After using this skill properly you should experience:
- Noticeably faster Codex startup and session switching
- Lower anxiety about "losing history"
- Clear, searchable handoff documents in your important repos
- A repeatable, low-risk maintenance habit

Start with a diagnosis run. The rest follows naturally.