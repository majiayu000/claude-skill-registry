---
title: "Claude Code Continuous Learning Skill"
type: github
url: "https://github.com/blader/claude-code-continuous-learning-skill"
stars: 359
language: "Shell"
tags:
  - claude-code
  - ai-agents
  - developer-experience
  - ai-tools
authors:
  - blader
summary: "A meta-skill that extracts reusable knowledge from debugging sessions and saves it as new skills, giving Claude Code persistent memory across sessions."
date: 2026-01-18
---

## Overview

Every Claude Code session starts fresh—no memory of past discoveries. The Continuous Learning Skill solves this by extracting non-obvious knowledge (debugging techniques, workarounds, project patterns) and saving it as new skills that load automatically in future sessions.

The architecture exploits Claude Code's native skill retrieval system. At startup, Claude loads skill names and descriptions (~100 tokens each). When your current context semantically matches a description, the full skill loads. This skill *writes* to that retrieval system, not just reads from it.

## Key Features

- **Automatic extraction**: Evaluates each session for knowledge worth preserving
- **Quality gates**: Only extracts reusable, non-trivial, verified solutions
- **Searchable descriptions**: Generated descriptions optimized for future semantic matching
- **Retrospective mode**: Run `/retrospective` at session end to catch missed learnings

## Architecture

::mermaid
<pre>
flowchart LR
    Problem[Problem] --> Investigate[Investigation]
    Investigate --> Solution[Solution]
    Solution --> Eval{Worth<br/>preserving?}
    Eval -->|Yes| Extract[Extract Skill]
    Eval -->|No| Done[End]
    Extract --> Library[(Skills Library)]
    Library -->|Future sessions| Match[Semantic Matching]
    Match --> Load[Auto-load Skill]
</pre>
::

## Code Snippets

### Installation

```bash
git clone https://github.com/blader/claude-code-continuous-learning-skill.git \
  ~/.claude/skills/continuous-learning
```

### Hook Setup

Create an activation hook that injects evaluation reminders:

```bash
mkdir -p ~/.claude/hooks
cp ~/.claude/skills/continuous-learning/scripts/continuous-learning-activator.sh \
   ~/.claude/hooks/
chmod +x ~/.claude/hooks/continuous-learning-activator.sh
```

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/continuous-learning-activator.sh"
          }
        ]
      }
    ]
  }
}
```

## Quality Gates

The system applies strict criteria before extraction:

| Gate | Question |
|------|----------|
| **Reusable** | Will this help with future tasks? |
| **Non-trivial** | Did this require discovery, not docs lookup? |
| **Specific** | Can you describe exact triggers and solutions? |
| **Verified** | Has the solution been tested and confirmed? |

## Extraction Triggers

- Non-obvious debugging requiring >10 minutes investigation
- Error resolution where root cause wasn't apparent
- Workaround discovery through experimentation
- Configuration insights differing from standard patterns

## Academic Foundations

The approach draws from AI agent research:

- **Voyager** (Wang et al., 2023): Game-playing agents building skill libraries
- **CASCADE** (2024): Meta-skills—skills for acquiring skills
- **SEAgent** (2025): Agents learning software environments through trial and error
- **Reflexion** (Shinn et al., 2023): Self-reflection improving agent performance

## Connections

- [[claude-code-skills]] - Official Skills documentation that this tool extends with automatic generation
- [[introducing-agent-skills-in-vs-code]] - Same portable skill concept applied to VS Code's agent ecosystem
