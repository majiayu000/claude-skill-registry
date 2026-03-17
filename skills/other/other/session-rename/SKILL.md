---
name: session-rename
description: Rename the current chat tab or any saved session with a descriptive name
argument-hint: "<new-name> [--session N]"
tags: [session, management, productivity]
user-invocable: true
---

# Session Rename

Rename the **current chat tab** (VSCode extension) or any saved session file.

## Usage

```
/session-rename EAGLES Framework    # Rename CURRENT chat tab
/session-rename list                # List all past conversations with indices
/session-rename --session 3 My Name # Rename conversation #3
```

## How It Works

### Renaming the current chat tab

1. Detect the current session ID from the conversation context or by finding the most recently modified `.jsonl` file in `~/.claude/projects/{project-slug}/`
2. Open `~/.claude/projects/{project-slug}/sessions-index.json`
3. Find or insert the entry matching the current session ID
4. Set the `firstPrompt` field to the user's chosen name (this controls the tab title)
5. Write the updated index back to disk

### Implementation

Run this Python script via Bash to rename the current tab:

```python
import os, json, glob

# Config
project_slug = 'c--rh-optimerp-sourcing-candidate-attraction'  # Auto-detect from cwd
new_name = 'USER_PROVIDED_NAME'

# Find project dir
project_dir = os.path.expanduser(f'~/.claude/projects/{project_slug}')
index_path = os.path.join(project_dir, 'sessions-index.json')

# Find current session (most recently modified .jsonl)
jsonl_files = sorted(
    glob.glob(os.path.join(project_dir, '*.jsonl')),
    key=os.path.getmtime, reverse=True
)
current_id = os.path.basename(jsonl_files[0]).replace('.jsonl', '')

# Load or create index
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
else:
    index = {'version': 1, 'entries': [], 'originalPath': os.getcwd()}

# Find or create entry
entry = next((e for e in index['entries'] if e.get('sessionId') == current_id), None)
if entry:
    old_name = entry.get('firstPrompt', '(unnamed)')
    entry['firstPrompt'] = new_name
else:
    stat = os.stat(jsonl_files[0])
    index['entries'].append({
        'sessionId': current_id,
        'fullPath': jsonl_files[0],
        'fileMtime': int(stat.st_mtime * 1000),
        'firstPrompt': new_name,
        'messageCount': 100,
        'gitBranch': 'hatim',
        'projectPath': os.getcwd(),
        'isSidechain': False
    })
    old_name = '(not in index)'

# Save
with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=2)

print(f'Renamed: {old_name} -> {new_name}')
```

### Listing past conversations

When invoked with `list`, read `sessions-index.json` and display all entries sorted by modification time:

```
[1] EAGLES Claude Framework v3.0 (78MB, Feb 17)     <-- current
[2] Calculator with Ant Design (379MB, Feb 02)
[3] QCO Enhancement (95MB, Jan 30)
...
```

## Rules

- When no `--session` flag is given, always rename the CURRENT conversation
- The `firstPrompt` field in `sessions-index.json` is what controls the tab title in VSCode
- Auto-detect the project slug from the current working directory path
- If sessions-index.json doesn't exist, create it with version 1
- The rename takes effect when the user switches tabs or reopens the chat panel
- Also rename the custom `.md` session file in `~/.claude/sessions/` if one exists for this session
