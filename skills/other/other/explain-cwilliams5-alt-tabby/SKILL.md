---
name: explain
description: Explain a file, function, or system — architectural walkthrough using query tools
user-invocable: true
disable-model-invocation: false
argument-hint: "[file, function, or system]"
---
The user wants to understand how something works. Not a review, not an audit — just teach. Build a concise architectural explanation using the query tools. Minimize context cost — don't load entire files when a query tool can answer.

## How to Research

Use the query tools to build understanding efficiently:

- `query_interface.ps1 <filename>` — Start here. Shows a file's public functions and globals — the API surface without loading the implementation.
- `query_function.ps1 <funcName>` — Read a specific function body when you need implementation details.
- `query_function_visibility.ps1 <funcName>` — Who calls this function? Who does it call? Traces the call graph.
- `query_global_ownership.ps1 <globalName>` — Who reads/writes this global? Shows data flow across files.
- `query_config.ps1 <keyword>` — Find config settings related to the topic. `-Usage <key>` shows which files consume a setting.
- `query_ipc.ps1 <msgType>` — Trace IPC message flow between processes.
- `query_timers.ps1 <keyword>` — Find timers related to the topic.
- `query_state.ps1 <State> [Event]` — Trace state machine paths.

**Prefer interface queries over file reads.** `query_interface.ps1` gives you the shape of a file in a few lines. Only use `query_function.ps1` when you need to explain *how* something works, not just *what* it does.

## How to Explain

Structure the explanation as:

### 1. Overview (1-3 sentences)
What this system/feature does and why it exists.

### 2. Files involved
List the files with one-line descriptions of their role. Don't list every file in the project — only the ones directly involved.

### 3. Data flow
How data moves through the system. Use a simple diagram if it helps:
```
Event → Producer → Store → Display List → Paint
```

### 4. Key functions
The important functions and what they do — not an exhaustive list, just the ones needed to understand the system. Include `file:function` format so the user can navigate.

### 5. Key decisions
Non-obvious design choices that explain "why" not just "what." Reference comments in the code or rules files if they exist.

### 6. Config
Any user-configurable settings that affect this system.

## Tone

- Concise — tables and diagrams over prose
- No jargon without explanation — if a term is project-specific, define it
- Answer the user's actual question — if they asked about icon caching, don't explain the entire paint pipeline. Stay focused.
- If the user's question is vague, narrow it by explaining what sub-topics exist and asking which they want to dive into
