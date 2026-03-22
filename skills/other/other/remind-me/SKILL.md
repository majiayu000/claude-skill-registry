---
name: remind-me
description: Summarize recent activity in this repo to help you pick up where you left off
user-invokable: true
disable-model-invocation: true
---

# reminder

Generate a concise summary of recent activity in this repository so the user can quickly pick up where they left off.

## Discovery steps

### 1. Recent commits

Run:

```bash
git log --oneline --no-merges -15
```

Summarize the recent commit history as a narrative — what features were added, what was fixed, what was refactored. Group related commits together rather than listing them individually.

### 2. Current branch state

Run:

```bash
git branch --show-current
git status --short
```

Report the current branch and whether there are uncommitted changes (staged, unstaged, or untracked files). If there are changes, briefly describe what files are affected.

### 3. Work in progress

Run:

```bash
git stash list
```

If there are stashed changes, mention them.

### 4. Recent branches

Run:

```bash
git branch --sort=-committerdate --format='%(refname:short) %(committerdate:relative)' | head -5
```

List recently active branches — these may indicate parallel workstreams.

### 5. Open TODOs in code

Run a search for TODO and FIXME comments in the source:

```bash
grep -rn --include='*.ts' --include='*.tsx' 'TODO\|FIXME' src/ || true
```

If any are found, list them as potential next actions.

## Output format

Present the summary as a brief narrative, not raw command output. Structure it as:

```
## Where you left off

[1-2 sentence summary of the most recent work based on commits and branch state]

## Uncommitted changes

[Description of any in-progress work, or "Clean working tree" if none]

## Recent activity

[Narrative summary of the last ~15 commits, grouped by theme]

## Active branches

[List of recently active branches with relative dates]

## Open TODOs

[List of TODO/FIXME items found in source, or "None found" if clean]
```

Keep the tone concise and actionable — this is a quick "morning standup" to get reoriented.
