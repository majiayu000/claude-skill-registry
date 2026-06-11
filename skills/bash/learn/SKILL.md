---
name: learn
description: "Manually teach error pattern and solution to learning database."
user-invocable: false
argument-hint: '"error" -> "solution"'
allowed-tools:
  - Read
  - Bash
routing:
  triggers:
    - "teach pattern"
    - "record learning"
    - "manual learning entry"
    - "teach error pattern"
    - "save learning"
  category: meta-tooling
  pairs_with:
    - retro
    - auto-dream
---

# Learn Error Pattern Skill

Parse a user-provided "error -> solution" pair, classify it, store it in the cross-session learning database at high confidence, and confirm back. One pattern per invocation. All database operations go through the `learning-db.py` CLI.

## Instructions

### Step 1: Parse Input

Extract two fields from the user's input:

- `error_pattern`: The error message or symptom text
- `solution`: The fix or resolution text

Accepted input formats:
- `/learn "error pattern" -> "solution"`
- `/learn "error pattern" => "solution"`
- Freeform: "teach that X means Y" or "remember: when X, do Y"

Both fields must be non-empty. If either is missing, ask the user for the missing part before proceeding. If the error pattern is vague (e.g., "it broke") or the solution is non-actionable (e.g., "fix it"), ask the user to provide the specific error message and concrete fix steps — vague patterns fail to match future errors and waste database space.

### Step 2: Classify Fix Type

Determine `fix_type` and `fix_action` from the solution text by applying these rules in order:

1. Solution contains an install command (`pip install`, `npm install`, `apt install`) -> `fix_type=auto`, `fix_action=install_dependency`
2. Solution contains `replace_all` -> `fix_type=auto`, `fix_action=use_replace_all`
3. Solution references a skill name -> `fix_type=skill`, `fix_action=<skill-name>`
4. Solution references an agent name -> `fix_type=agent`, `fix_action=<agent-name>`
5. Otherwise -> `fix_type=manual`, `fix_action=apply_suggestion`

### Step 3: Store Pattern

Execute the `learning-db.py` CLI to persist the pattern. Always pass user-provided strings as CLI arguments exactly as shown — never inline them into Python code via f-strings or string concatenation, because quotes or special characters in error text will break the script and create injection risk.

```bash
python3 ~/.claude/scripts/learning-db.py record \
  "<error_type>" \
  "<error_signature>" \
  "<error_pattern> → <solution>" \
  --category error \
  --confidence 0.9
```

- `<error_type>`: The classified type (e.g., "missing_file", "multiple_matches")
- `<error_signature>`: A kebab-case key derived from the error pattern
- Confidence is always 0.9 for manually taught patterns. If the pattern already exists, this updates its confidence to 0.9.

Example:
```bash
python3 ~/.claude/scripts/learning-db.py record \
  "multiple_matches" \
  "edit-tool-multiple-matches" \
  "Edit tool fails with 'found N matches' → Use replace_all=True parameter" \
  --category error \
  --confidence 0.9
```

The script must exit 0 and print confirmation. If it fails, see Error Handling below.

### Step 4: Confirm to User

Always display what was stored so the user can verify correctness — silently storing without confirmation hides typos and misclassifications:

```
Learned pattern:
  Error: "<error_pattern>"
  Solution: "<solution>"
  Type: <fix_type> (<fix_action>)
  Confidence: 0.9
```

## Error Handling

### Error: "Script fails with ImportError or FileNotFoundError"
Cause: scripts/learning-db.py not found or not synced to ~/.claude/scripts/
Solution: Verify working directory is the repo root, or use `~/.claude/scripts/learning-db.py` for cross-repo access.

### Error: "Database locked"
Cause: Another process holds the SQLite lock
Solution: Retry after 2 seconds. If persistent, check for hung processes with `lsof ~/.claude/learning/learning.db`.

### Error: "User provides only error, no solution"
Cause: Incomplete input
Solution: Ask the user explicitly for the solution text. Do not guess or fabricate solutions.

## References

- `hooks/lib/learning_db_v2.py`: Unified learning database module
- `scripts/learning-db.py`: CLI for recording, querying, and managing learnings
- `hooks/error-learner.py`: Automatic error learning hook (complementary system)
