---
name: mob
description: Use when the user wants to set, change, or clear git commit co-authors for pair or mob programming.
argument-hint: <names...> | solo | just me
disable-model-invocation: true
allowed-tools:
  - Bash(git mob:*)
  - Bash(git solo:*)
  - Bash(git add-coauthor:*)
  - Bash(git mob-print:*)
  - Read
---

# Mob Programming Co-author Manager

## Arguments

```
$ARGUMENTS
```

## Workflow

### 1. Solo Mode
If arguments indicate solo work (e.g., "solo", "just me"): run `git solo`, report primary author, exit.

### 2. Load Co-authors
Use `git mob -p` to find coauthors file, read with Read tool, parse JSON for available co-authors and initials.

### 3. Match Names to Initials
Match each name: exact initials → name substring (case-insensitive) → email prefix. If ambiguous, ask user to clarify.

### 4. Handle Unknown Names
If no match:
1. Infer email from existing patterns (domain, naming convention)
2. Generate initials from name (avoid collisions)
3. Prompt for confirmation (show initials, name, inferred email)
4. Run `git add-coauthor <initials> "<name>" <email>`

### 5. Set Mob
Run `git mob <initials...>` with resolved initials.

### 6. Report
Show primary author and all co-authors with names.

## Example
```
/mob alice dana
→ alice → aw (Alice Wong)
→ dana not found → infer dana@acme.com → add as dw
→ git mob aw dw
```

## Edge Cases
Handle: missing coauthors file (create it), empty args (show status), ambiguous matches (prompt), mixed known/unknown (resolve known first).
