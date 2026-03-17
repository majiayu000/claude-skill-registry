---
name: improve-skill
description: "Analyze coding agent session transcripts to improve existing skills or create new ones. Use when asked to improve a skill based on a session, or extract a new skill from session history."
---

# Improve Skill

This skill helps analyze coding agent sessions to improve or create skills. It works with Claude Code, Pi, and Codex session files.

## Quick Start

Extract the current session and generate an improvement prompt:

```bash
# Auto-detect agent and extract current session
./scripts/extract-session.js
```

## Session Extraction

The `extract-session.js` script finds and parses session files from any of the three agents:

```bash
# Auto-detect (uses most recent session for current working directory)
./scripts/extract-session.js

# Specify agent type
./scripts/extract-session.js --agent claude
./scripts/extract-session.js --agent pi
./scripts/extract-session.js --agent codex

# Specify a different working directory
./scripts/extract-session.js --cwd /path/to/project

# Use a specific session file
./scripts/extract-session.js /path/to/session.jsonl
```

**Session file locations:**
- **Claude Code**: `~/.claude/projects/<encoded-cwd>/*.jsonl`
- **Pi**: `~/.pi/agent/sessions/<encoded-cwd>/*.jsonl`
- **Codex**: `~/.codex/sessions/YYYY/MM/DD/*.jsonl`

## Workflow: Improve an Existing Skill

When asked to improve a skill based on a session:

1. **Extract the session transcript:**
   ```bash
   ./scripts/extract-session.js > /tmp/session-transcript.txt
   ```

2. **Find the existing skill** in one of these locations:
   - `~/.codex/skills/<skill-name>/SKILL.md`
   - `~/.claude/skills/<skill-name>/SKILL.md`
   - `~/.pi/agent/skills/<skill-name>/SKILL.md`

3. **Generate an improvement prompt** for a new session:

```
═══════════════════════════════════════════════════════════════════════════════
COPY THE FOLLOWING PROMPT INTO A NEW AGENT SESSION:
═══════════════════════════════════════════════════════════════════════════════

I need to improve the "<skill-name>" skill based on a session where I used it.

First, read the current skill at: <path-to-skill>

Then analyze this session transcript to understand:
- Where I struggled to use the skill correctly
- What information was missing from the skill
- What examples would have helped
- What I had to figure out on my own

<session_transcript>
<paste transcript here>
</session_transcript>

Based on this analysis, improve the skill by:
1. Adding missing instructions or clarifications
2. Adding examples for common use cases discovered
3. Fixing any incorrect guidance
4. Making the skill more concise where possible

Write the improved skill back to the same location.

═══════════════════════════════════════════════════════════════════════════════
```

## Workflow: Create a New Skill

When asked to create a new skill from a session:

1. **Extract the session transcript:**
   ```bash
   ./scripts/extract-session.js > /tmp/session-transcript.txt
   ```

2. **Generate a creation prompt** for a new session:

```
═══════════════════════════════════════════════════════════════════════════════
COPY THE FOLLOWING PROMPT INTO A NEW AGENT SESSION:
═══════════════════════════════════════════════════════════════════════════════

Analyze this session transcript to extract a reusable skill called "<skill-name>":

<session_transcript>
<paste transcript here>
</session_transcript>

Create a new skill that captures:
1. The core capability or workflow demonstrated
2. Key commands, APIs, or patterns used
3. Common pitfalls and how to avoid them
4. Example usage for typical scenarios

Write the skill to: ~/.codex/skills/<skill-name>/SKILL.md

Use this format:
---
name: <skill-name>
description: "<one-line description>"
---

# <Skill Name> Skill

<overview and quick reference>

## <Section for each major capability>

<instructions and examples>

═══════════════════════════════════════════════════════════════════════════════
```

## Why a Separate Session?

The improvement prompt is meant to be copied into a **fresh agent session** because:

1. **Token efficiency** - The current session already has a lot of context; starting fresh means only the transcript and skill are loaded
2. **Clean analysis** - The new session can focus purely on improvement without being influenced by the current task
3. **Reproducibility** - The prompt is self-contained and can be shared or reused

## Tips for Good Skill Improvements

When analyzing a transcript, look for:

- **Confusion patterns** - Where did the agent retry or change approach?
- **Missing examples** - What specific commands or code patterns were discovered?
- **Workarounds** - What did the agent have to figure out that wasn't documented?
- **Errors** - What failed and how was it resolved?
- **Successful patterns** - What worked well and should be highlighted?

Keep skills concise - focus on the most important information and examples.
