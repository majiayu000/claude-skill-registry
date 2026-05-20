---
name: guide-loader
description: Use when needing specialized guide content - delegates to dev-guides-navigator plugin for online guide discovery with caching and disambiguation
version: 3.0.0
user-invocable: false
---

# Guide Loader

Load development guides into context when needed. Delegates to the `dev-guides-navigator` plugin for online guide discovery.

## Activation

Activate when:
- Designing or implementing features that match guide topics
- User requests a specific guide
- Invoked by other skills (guide-integrator, task-context-loader)
- "Load the ECA guide" or "What does my guide say about..."

## Workflow

### 1. Check for Local Guides Path (Legacy)

Read `{project_path}/project_state.md` and look for `**Guides Path:** {path}`.

If found and specific guide requested by filename, read it directly. Otherwise, proceed to step 2.

### 2. Delegate to Navigator

Invoke the `dev-guides-navigator` skill with the task keywords. The navigator handles:
- Hash-based caching of `llms.txt` (no redundant fetches)
- Topic matching with KG metadata disambiguation
- Routing to the correct guide via topic `index.md`
- Fetching the specific guide content

### 3. Integrate with Current Work

Based on guide content returned by the navigator, suggest:
```
Apply to current task:
- {Specific recommendation from guide}
- {Pattern to follow}
- {Thing to avoid}

Add these to architecture/implementation? (yes/no)
```

## Stop Points

STOP and wait for user:
- If requested guide not found locally or via navigator
- After presenting guide content (ask if need more)
