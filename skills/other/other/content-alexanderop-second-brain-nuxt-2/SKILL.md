---
title: "Building a Conversation Search Skill for Claude Code"
type: note
tags:
  - claude-code
  - ai-tools
  - productivity
  - python
  - skills
authors:
  - alex-colvin
summary: "How to build a skill that searches past Claude Code conversations to find solutions to previously solved problems, leveraging the JSONL conversation history stored locally."
notes: "Created from my own experience - I faced an issue but forgot the fix. The conversation history had the answer."
date: 2026-01-02
---

## Motivation

Yesterday I faced a bug but couldn't remember how I fixed it last time. Then I realized: Claude Code stores every conversation locally. Why not search through them?

## Where Claude Code Stores Conversations

All conversations are stored as JSONL files under:

```bash
~/.claude/projects/<encoded-project-path>/<session-id>.jsonl
```

The project path is encoded by replacing `/` with `-`. For example:

- `/Users/alex/Projects/nuxt/secondBrain`
- becomes `-Users-alex-Projects-nuxt-secondBrain`

Each conversation is a separate JSONL file named with a UUID like `fff8047b-ca56-4302-b746-a78eb86a13f4.jsonl`.

## JSONL Structure

Each line is a JSON object with a `type` field:

```json
{
  "type": "user",
  "message": { "role": "user", "content": "fix the ESLint config" },
  "uuid": "f9f49f7e-...",
  "timestamp": "2025-12-31T20:31:22.799Z",
  "gitBranch": "main",
  "sessionId": "fff8047b-..."
}
```

Types include `user`, `assistant`, `system`, and `summary`. Assistant messages contain tool uses (Bash commands, file edits) that show exactly how problems were solved.

## The Skill

I created a Python script that parses these JSONL files and scores them against a search query. The skill lives at `~/.claude/skills/conversation-search/`.

### SKILL.md

```markdown
---
name: conversation-search
description: Search past Claude Code conversation history to find solutions to previously solved problems.
---

# Conversation History Search

Use this skill when the user asks:
- "How did we fix X before?"
- "What was the solution for Y?"
- "Search history for Z"
```

### search_history.py

```python
#!/usr/bin/env python3
from pathlib import Path
import json
import re

def get_claude_projects_dir() -> Path:
    return Path.home() / '.claude' / 'projects'

def decode_project_path(encoded: str) -> str:
    if encoded.startswith('-'):
        return '/' + encoded[1:].replace('-', '/')
    return encoded.replace('-', '/')

def tokenize(text: str) -> set:
    return set(re.findall(r'\b\w+\b', text.lower()))

def calculate_relevance_score(query: str, messages: list) -> float:
    query_tokens = tokenize(query)
    total_score = 0.0

    for msg in messages:
        msg_tokens = tokenize(msg.get('content', ''))
        overlap = len(query_tokens & msg_tokens)
        if overlap > 0:
            score = overlap / len(query_tokens)
            # Boost user messages (problem descriptions)
            if msg.get('role') == 'user':
                score *= 1.5
            total_score += score

    return total_score

def search_conversations(query: str, limit: int = 5):
    results = []
    for project_dir in get_claude_projects_dir().iterdir():
        if not project_dir.is_dir():
            continue
        for jsonl_file in project_dir.glob('*.jsonl'):
            messages = []
            with open(jsonl_file) as f:
                for line in f:
                    entry = json.loads(line)
                    if entry.get('type') in ('user', 'assistant'):
                        messages.append(entry.get('message', {}))

            score = calculate_relevance_score(query, messages)
            if score > 0:
                results.append((score, jsonl_file, messages))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:limit]
```

## Usage

```bash
# Find how an error was fixed
python3 ~/.claude/skills/conversation-search/scripts/search_history.py "EMFILE error"

# Search within a specific project
python3 ~/.claude/skills/conversation-search/scripts/search_history.py "vitest" --project ~/Projects/myapp
```

Claude Code automatically invokes this skill when you ask things like "what did we work on yesterday?" or "how did we fix that SSR bug?"

## Output

Results include:
- **Score**: Relevance ranking
- **Problem**: The original issue
- **Solution**: How it was resolved
- **Commands Run**: Bash commands executed during the fix

## Key Insight

The conversation history is a goldmine. Every bug fix, every implementation decision, every command that worked—it's all there. This skill turns that history into searchable institutional memory.

## Related

See [[writing-a-good-claude-md]] for configuring Claude Code, and [[claude-code-skills]] for more on building skills.
