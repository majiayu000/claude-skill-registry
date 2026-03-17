---
name: error-pattern-learner
description: |
  Remembers errors you have hit and how you fixed them. When the same or similar error
  appears again, it suggests the fix before you have to re-discover it. Like habit-formation
  but specifically for error/fix pairs. State persists between sessions.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
---

# Error Pattern Learner

Stop solving the same error twice.

---

## Why This Exists

You hit a cryptic error. You spend ten minutes figuring out the fix. Three weeks later, the same error appears in a different file, and you spend ten minutes again because the context from last time is gone. This happens constantly with environment issues, library quirks, and framework gotchas.

This skill watches for errors during your session, records how they were resolved, and matches against that history the next time something similar shows up.

---

## State File

All error/fix pairs persist in:

```
~/.claude/skills/error-pattern-learner/state/errors.json
```

The skill creates this file on first save. If the file is missing or corrupted, start fresh without complaining.

---

## Commands

### `/error-pattern-learner`

Show all known error patterns from the state file. Group by category (build, runtime, type, test, environment). Show the most recently matched patterns first.

### `/error-pattern-learner save`

Review the current session for error/fix pairs and save them to the state file. Merge with existing entries. If a matching error already exists, update its `last_seen` date and increment `occurrence_count`.

### `/error-pattern-learner search [error message]`

Search the state file for patterns matching the given error text. Uses fuzzy matching: strip line numbers, file paths, and timestamps from both the query and stored patterns before comparing. Show the top 3 matches with their fixes.

---

## Passive Detection

During any session where this skill is active, watch for error/fix sequences without interrupting the user.

### What counts as an error

A Bash tool call that returns a non-zero exit code. Specifically:

- Build failures (`npm run build`, `cargo build`, `go build`, `tsc`)
- Test failures (`npm test`, `pytest`, `go test`)
- Lint errors (`eslint`, `ruff`, `clippy`)
- Runtime errors (stack traces in stdout/stderr)
- Command-not-found or permission errors

Also watch for error text pasted directly by the user ("I'm getting this error: ...").

### What counts as a fix

After an error is detected, track the sequence of actions until the same command succeeds. The fix is the set of Edit/Write tool calls between the failed Bash call and the next successful Bash call of the same (or equivalent) command.

Example sequence:
```
1. Bash: npm run build  -> exit code 1, error: "Cannot find module './utils'"
2. Read: src/index.ts
3. Edit: src/index.ts (change import path from './utils' to './lib/utils')
4. Bash: npm run build  -> exit code 0
```

The error is "Cannot find module './utils'". The fix is "Change import path from `./utils` to `./lib/utils`."

### What to ignore

- Intentional errors (user running a command they know will fail to check output)
- The same error repeating because the fix hasn't been applied yet (only record once per fix cycle)
- Errors that were resolved by the user typing something, not by an Edit/Write action (we cannot reliably capture those)

---

## Pattern Extraction

When saving an error/fix pair, extract:

1. The error message (stripped of file-specific paths and line numbers)
2. The error category
3. The file type where the error occurred
4. A one-sentence description of the fix
5. The actual code change (abbreviated if large)
6. The command that triggered the error
7. The project context (language, framework if detectable)

### Error Message Normalization

To match errors across different files and projects, normalize the message:

```
Original:  "src/components/Header.tsx(42,15): error TS2304: Cannot find name 'UserContext'."
Normalized: "error TS2304: Cannot find name '[identifier]'."

Original:  "Module not found: Error: Can't resolve './components/Footer' in '/Users/jae/project/src'"
Normalized: "Module not found: Error: Can't resolve '[path]' in '[directory]'"
```

Replace:
- File paths with `[path]`
- Line/column numbers with `[line]`
- Specific identifiers with `[identifier]` (only when the fix is about the pattern, not the specific name)
- Absolute directory paths with `[directory]`

Keep the error code (TS2304, E0432, etc.) intact. Those are the most reliable matching signal.

---

## State File Format

### errors.json

```json
{
  "version": 1,
  "updated_at": "2026-02-10T14:30:00Z",
  "patterns": [
    {
      "id": "err-001",
      "category": "type",
      "error_normalized": "error TS2304: Cannot find name '[identifier]'.",
      "error_raw_example": "error TS2304: Cannot find name 'UserContext'.",
      "fix_summary": "Import the missing type/value. Check if it was renamed or moved.",
      "fix_example": "Added `import { UserContext } from '@/contexts/user'` to the file.",
      "command": "tsc --noEmit",
      "file_types": [".tsx", ".ts"],
      "framework": "next.js",
      "occurrence_count": 4,
      "first_seen": "2026-01-20",
      "last_seen": "2026-02-10",
      "tags": ["typescript", "import"]
    },
    {
      "id": "err-002",
      "category": "build",
      "error_normalized": "Module not found: Error: Can't resolve '[path]'",
      "error_raw_example": "Module not found: Error: Can't resolve './components/Footer'",
      "fix_summary": "File was moved or renamed. Update the import path to the new location.",
      "fix_example": "Changed import from './components/Footer' to './components/layout/Footer'",
      "command": "npm run build",
      "file_types": [".tsx"],
      "framework": "next.js",
      "occurrence_count": 2,
      "first_seen": "2026-02-05",
      "last_seen": "2026-02-09",
      "tags": ["import", "module-resolution"]
    },
    {
      "id": "err-003",
      "category": "environment",
      "error_normalized": "EACCES: permission denied, mkdir '[path]'",
      "error_raw_example": "EACCES: permission denied, mkdir '/usr/local/lib/node_modules'",
      "fix_summary": "Don't use sudo with npm. Fix directory ownership or use nvm.",
      "fix_example": "Ran: sudo chown -R $(whoami) /usr/local/lib/node_modules",
      "command": "npm install -g [package]",
      "file_types": [],
      "framework": null,
      "occurrence_count": 1,
      "first_seen": "2026-02-10",
      "last_seen": "2026-02-10",
      "tags": ["npm", "permissions"]
    }
  ]
}
```

---

## Matching Algorithm

When a new error appears, find matches in this order:

1. Exact error code match (TS2304, E0432, EACCES). Highest confidence.
2. Normalized message match (after stripping paths/lines). High confidence.
3. Keyword overlap with existing `error_normalized` fields. Medium confidence.
4. Same category + same `command` + same `file_types`. Low confidence.

For each match, show:

```
Known error pattern found (err-001, seen 4 times):
  Error: TS2304 - Cannot find name '[identifier]'
  Usual fix: Import the missing type/value. Check if it was renamed or moved.
  Last fix applied: Added `import { UserContext } from '@/contexts/user'`
```

If multiple patterns match, show the highest-confidence one first. Cap at 3 suggestions.

---

## Session Start Behavior

At the beginning of a session:

1. Check if `~/.claude/skills/error-pattern-learner/state/errors.json` exists
2. If it exists, load it silently
3. Do not announce anything. Just have it ready for matching.

---

## Categories

| Category | Covers |
|---|---|
| `build` | Compilation failures, bundler errors, missing modules |
| `runtime` | Uncaught exceptions, segfaults, process crashes |
| `type` | TypeScript errors, type mismatches, missing declarations |
| `test` | Test assertion failures, test runner config issues |
| `lint` | ESLint, Prettier, Ruff, Clippy violations |
| `environment` | Permission errors, missing binaries, wrong Node/Python version |
| `git` | Merge conflicts, rebase failures, hook errors |
| `network` | API timeouts, DNS failures, certificate errors |

---

## Important Constraints

- Never interrupt the user to say "I detected an error pattern." Only surface matches when they are relevant to the current error being worked on.
- When suggesting a fix, be clear it is a suggestion from a previous session, not a guaranteed answer. The context might be different this time.
- Merge, do not overwrite. When saving, read the existing file first and increment counts for known patterns.
- Keep `fix_example` under 200 characters. The point is to jog memory, not replay the entire change.
- If `errors.json` grows beyond 200 entries, drop the oldest entries with `occurrence_count` of 1 that have not been seen in 30+ days.
- The state file is the user's data. They can edit or delete it at any time.
