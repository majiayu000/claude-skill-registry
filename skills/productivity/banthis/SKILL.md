---
name: banthis
description: Banthis extends project memory with hard user prohibitions by writing a managed AGENTS.md/CLAUDE.md section and preserving all surrounding content. Use when the user says "stop doing X", "never do that again", "ban this", "remember not to", or "add a project rule".
metadata:
  short-description: Persist behavioral bans
---

# Banthis — durable behavioral bans

Extend the local instruction surface with a named prohibition. The op-cell is **extend**: add one hard rule, keep existing project memory intact, and make the rule visible to future sessions.

Banthis is for user frustration or correction that should persist. It is not a notes system, preference logger, or policy engine.

---

## When to Apply

Apply immediately when the user signals a behavior should never recur:

- “stop doing X”
- “never do that again”
- “ban this”
- “remember not to …”
- “add a project rule …”
- repeated frustration with a specific agent behavior

Certainty:

- **HIGH** — explicit ban language or direct instruction to remember a prohibition.
- **MEDIUM** — frustration plus a concrete repeated behavior. Ask only if the rule boundary is ambiguous.
- **LOW** — stylistic preference, local task constraint, or one-off correction. Do not persist unless the user asks.

---

## When NOT

Do not write a ban when:

- the constraint applies only to the current command or current file;
- the request is a normal implementation requirement;
- the rule would be vague (“be better”, “stop being annoying”);
- the rule duplicates an existing ban with no stronger wording;
- the rule is unsafe, impossible, or conflicts with a higher-priority instruction.

If a requested ban conflicts with an existing ban, surface the conflict instead of rewriting history.

---

## Workflow

1. **Extract the invariant.** Identify the forbidden behavior and the reason. No moralizing.
2. **Craft the title.** `<60` characters, noun phrase or imperative fragment, no markdown markers.
   - Good: `No silent scope shrink`
   - Bad: `User got mad because we keep doing dumb partial work`
3. **Craft the rule.** One line, direct prohibition, reason included:
   - `Do not X — reason.`
4. **Choose scope.**
   - Project-specific behavior: omit `--global`.
   - Agent-wide verbal tic or repeated generic habit: add `--global`.
5. **Write through the managed command.** From the skill directory, run:

   ```sh
   node scripts/banthis.mjs add "<title>" "Do not X — reason."
   ```

   For user-wide bans:

   ```sh
   node scripts/banthis.mjs --global add "<title>" "Do not X — reason."
   ```

6. **Report minimally.** Say which target file received the ban and whether it was added, updated, or unchanged.

---

## Target resolution

The script resolves the write target deterministically:

1. `--global` always writes `~/.claude/CLAUDE.md`.
2. Otherwise, use the current working directory.
3. In the current directory, `AGENTS.md` takes precedence over `CLAUDE.md`.
4. If neither exists, create `CLAUDE.md`.

No repository scan. No editor adapter. No external binary.

---

## Managed-section invariant

The script owns only this range:

```md
<!-- banthis:start -->
...
<!-- banthis:end -->
```

Guardrails:

- Never hand-edit inside the markers when the command can do it.
- Never place user-supplied text containing banthis markers into a title or rule.
- If the managed section exists, replace only that byte range.
- If absent, insert after the first top-level `# H1`; if no H1 exists, prepend the section.
- Preserve every byte outside the managed range except the minimal insertion boundary.

The managed section contains a preamble asserting that bans win over the current request. Future sessions must surface conflicts instead of quietly violating bans.

---

## Command contract

```sh
node scripts/banthis.mjs add <title> <rule>
node scripts/banthis.mjs list
node scripts/banthis.mjs remove <title>
node scripts/banthis.mjs init
```

Shortcut:

```sh
node scripts/banthis.mjs <title> <rule>
```

Flags:

```sh
-g, --global   target ~/.claude/CLAUDE.md
-h, --help     print usage
```

Results:

- `added` — no case-insensitive title match existed.
- `updated` — title matched case-insensitively and title or rule changed.
- `unchanged` — exact title and rule already present.

---

## Anti-patterns

- **Excess** — storing every preference as a hard ban. Bans are scarce and sharp.
- **Graft** — adding a second memory mechanism, JSON cache, slash-command shim, or editor adapter.
- **Sprawl** — scanning parent directories or rewriting unrelated docs.
- **Soft ban** — phrasing as “try not to” or “prefer not to”. Use `Do not … — reason.`
- **Hidden conflict** — obeying the current request while violating a persisted prohibition.

---

## Validation Gates

Before yielding after a ban operation:

1. The target file contains exactly one `<!-- banthis:start -->` and one `<!-- banthis:end -->` pair.
2. The new or updated title appears once, case-insensitive.
3. The rule is one line and starts with `Do not` unless the user supplied a stronger exact wording.
4. Content outside the managed markers is unchanged except for first insertion.
5. `list` reports the expected title and rule preview.
