---
name: cortex
description: Automatic session tracking and memory system for Claude Code. Activates when working in git repositories to track file changes, commits, and session context. Creates .cortex_log.md (session history), .cortex_status.json (current state), and .cortex_handoff.md (next steps) for session continuity across conversations. Use when needing persistent memory, session handoffs, or work history tracking.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Cortex - Session Orchestration & Universal Logging

Cortex is an automatic memory system that traces all work across sessions and enables skills to communicate with each other.

## What Cortex Provides

1. **Automatic session tracing** - Tracks all file changes, git operations, and major events
2. **Agent handoffs** - Seamless context transfer between sessions
3. **Inter-skill communication** - Python API for skills to share data and patterns
4. **Pattern detection** - Analyzes work patterns to recommend new skills (via Synapse)

## Core Files Generated

Cortex automatically maintains three files in your project root:

- **`.cortex_log.md`** - Human-readable session history with detailed narrative
- **`.cortex_status.json`** - Machine-readable current state and metrics
- **`.cortex_handoff.md`** - Quick start guide for next session

These files are automatically updated throughout your work session.

## How It Works

### Automatic Tracing

Cortex runs automatically via git hooks. Every time you:
- Make file changes
- Commit code
- Complete a task

Cortex updates the memory files with context about what happened and why.

### Agent Handoffs

When starting a new session, Claude reads `.cortex_handoff.md` to understand:
- What was done in the last session
- Current repository state
- Priority next steps
- Recent work context

### Inter-Skill Communication

Skills can use Cortex's Python API to communicate:

```python
from cortex_api import add_cortex_event, get_cortex_memory, get_pattern_analysis

# Record an event
add_cortex_event("api_call", "Called GitHub API", {
    "endpoint": "/repos/user/repo",
    "status": 200
})

# Query memory
recent_events = get_cortex_memory(filter_type="api_call", limit=10)

# Analyze patterns (used by Synapse)
patterns = get_pattern_analysis(days=7, threshold=5)
```

See [API_REFERENCE.md](references/API_REFERENCE.md) for complete documentation.

## Installation

Run the installation script to set up git hooks:

```bash
cd .claude/skills/cortex/scripts
./install.sh
```

This configures Cortex to automatically track your work.

## Usage

### Manual Session Tracing

To manually update Cortex files:

```bash
python3 .claude/skills/cortex/scripts/trace_session.py
```

### Manual Handoff Generation

To generate a handoff document:

```bash
python3 .claude/skills/cortex/scripts/handoff_generator.py
```

### Using Cortex API in Your Skills

1. Import the API:
   ```python
   from cortex_api import add_cortex_event, get_cortex_memory
   ```

2. Record events during your skill's operation
3. Query patterns to inform decisions
4. Cortex handles all file locking and persistence

## Integration with Synapse

Cortex's pattern analysis powers Synapse automatic skill generation:

1. Cortex tracks recurring patterns (API calls, data processing, etc.)
2. Synapse queries Cortex for patterns above a threshold
3. Synapse automatically generates skills when patterns reach critical frequency
4. New skills use Cortex API to record their own events

This creates a self-improving system where skills emerge from actual usage patterns.

## Files and Scripts

### Scripts

- **`trace_session.py`** - Updates `.cortex_log.md` and `.cortex_status.json`
- **`handoff_generator.py`** - Creates `.cortex_handoff.md`
- **`cortex_api.py`** - Python API for inter-skill communication
- **`install.sh`** - Sets up git hooks

### References

- **[API_REFERENCE.md](references/API_REFERENCE.md)** - Complete Cortex API documentation
- **[WORKFLOWS.md](references/WORKFLOWS.md)** - Common Cortex usage patterns
- **[MULTI_LLM.md](references/MULTI_LLM.md)** - Using Cortex with GPT, Gemini, etc.

## Best Practices

1. **Let it run automatically** - Don't manually trace unless needed
2. **Check `.cortex_handoff.md` at session start** - Quick context refresh
3. **Use Cortex API in custom skills** - Enables automatic pattern detection
4. **Commit Cortex files with your work** - Preserves memory across machines

## Multi-LLM Support

Cortex works with Claude Code, GPT, Gemini, and other CLI-based LLMs. The memory files use universal markdown and JSON formats.

See [MULTI_LLM.md](references/MULTI_LLM.md) for LLM-specific integration guides.

---

*Cortex is the foundation of DeepSynth's self-improving skills system.*
