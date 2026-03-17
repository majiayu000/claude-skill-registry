---
# VERSION: 2.88.0
name: gemini-cli
description: "Google Gemini CLI orchestration (v0.22.0+) for AI-assisted development. Capabilities: second opinion/cross-validation, real-time Google Search grounding, codebase architecture analysis with codebase_investigator, Gemini 3 model access, extensions support (Conductor, Endor Labs), parallel code generation, code review from different perspective. INTEGRATED WITH TASK PRIMITIVE - creates traceable tasks in claude-task-viewer. Actions: query, search, analyze, generate, review with Gemini. Keywords: Gemini CLI, Gemini 3, google_web_search, codebase_investigator, second opinion, cross-validation, web research, current information, parallel AI, code review, architecture analysis, gemini prompt, AI comparison, real-time search, alternative perspective, extensions, Conductor. Use when: needing second AI opinion, searching current web information, analyzing codebase architecture, generating code in parallel, getting alternative code review, researching current events/docs, using Gemini extensions."
---

# Gemini CLI Integration Skill

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

This skill enables Claude Code to orchestrate Google Gemini CLI (v0.22.0+) with **Gemini 3 Pro** for code generation, review, analysis, and specialized tasks including real-time web search.

## What's New in v0.22.0 (December 2025)

- **Gemini 3**: Free tier users now have access to Gemini 3 via Preview Features toggle
- **Colab Integration**: Pre-installed in Google Colab, usable headlessly in notebook cells
- **Extensions Support**:
  - **Conductor**: Planning++ with context-driven development
  - **Endor Labs**: Code analysis, vulnerability scanning, dependency checks
- **Comprehensive Quota Visibility**: `/stats` shows all model usage
- **Multi-file Drag & Drop**: Proper `@` prefix handling for multiple files

## When to Use This Skill

### Ideal Use Cases

1. **Second Opinion / Cross-Validation**
   - Review code after Claude writes it (different AI perspective)
   - Security audit with alternative analysis
   - Find bugs Claude might have missed

2. **Google Search Grounding**
   - Questions requiring current internet information
   - Latest library versions, API changes, documentation
   - Current events, recent releases

3. **Codebase Architecture Analysis**
   - Use `codebase_investigator` tool
   - Understanding unfamiliar codebases
   - Mapping cross-file dependencies

4. **Parallel Processing**
   - Offload tasks while continuing other work
   - Multiple code generations simultaneously
   - Background documentation generation

5. **Extensions Workflows**
   - Conductor for detailed planning before implementation
   - Endor Labs for security/vulnerability scanning

### When NOT to Use

- Simple, quick tasks (overhead not worth it)
- Tasks requiring immediate response (rate limits cause delays)
- When context is already loaded in Claude
- Interactive refinement requiring conversation

## Quick Start

### Prerequisites

```bash
# Verify installation
command -v gemini || which gemini

# Check version
gemini --version  # Should show v0.22.0+
```

### Authentication

```bash
# Option 1: API Key
export GEMINI_API_KEY=your_key

# Option 2: OAuth (interactive, first run)
gemini  # Prompts for auth
```

### Enable Gemini 3 (Free Tier)

In interactive mode:
```
/settings
# Toggle "Preview Features" to true
```

## Core Commands

### Basic Execution

```bash
# Human-readable output
gemini "your prompt" --yolo -o text 2>&1

# JSON structured output
gemini "your prompt" --yolo -o json 2>&1

# Faster model for simple tasks
gemini "your prompt" -m gemini-2.5-flash -o text 2>&1
```

### Key Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--yolo` | `-y` | Auto-approve all tool calls |
| `--output-format` | `-o` | Output: `text`, `json`, `stream-json` |
| `--model` | `-m` | Model selection |
| `--resume` | `-r` | Resume session by index |
| `--sandbox` | `-s` | Run in isolated sandbox |
| `--debug` | `-d` | Enable debug output |

### Important Behavior Notes

**YOLO Mode**: Auto-approves tool calls but does NOT prevent planning prompts. Gemini may still ask "Does this plan look good?" Use forceful language:
- "Apply now"
- "Start immediately"
- "Do this without asking for confirmation"

**Rate Limits**: Free tier has 60 requests/min, 1000/day. CLI auto-retries with backoff.

## Model Selection

| Model | Use Case | Context |
|-------|----------|---------|
| `gemini-3-pro` | Complex tasks (default) | 1M tokens |
| `gemini-2.5-flash` | Quick tasks, lower latency | Large |
| `gemini-2.5-flash-lite` | Fastest, simplest tasks | Medium |

```bash
# Default (Gemini 3 Pro)
gemini "complex analysis" -o text

# Flash for speed
gemini "simple task" -m gemini-2.5-flash -o text
```

## Unique Gemini Capabilities

### 1. google_web_search

Real-time internet search via Google:

```bash
gemini "What are the latest React 19 features? Use Google Search." -o text

gemini "What's new in TypeScript 5.5? Use Google Search." -o text

gemini "Best practices for Next.js 15 as of December 2025." -o text
```

**Best for:**
- Current events and news
- Latest library versions
- Recent documentation updates
- Community opinions and benchmarks

### 2. codebase_investigator

Deep codebase analysis:

```bash
gemini "Use the codebase_investigator tool to analyze this project" -o text

gemini "Use codebase_investigator to map the authentication flow" -o text
```

**Output includes:**
- Overall architecture description
- Key file purposes
- Component relationships
- Dependency chains
- Potential issues

### 3. save_memory

Cross-session persistence:

```bash
gemini "Remember that this project uses Zustand. Save to memory." -o text
```

## Extensions (v0.22.0+)

### Conductor Extension

Planning++ with context-driven development:

```bash
# Install
gemini extensions install https://github.com/gemini-cli-extensions/conductor

# Use for detailed planning
gemini "Use Conductor to plan the implementation of user authentication" -o text
```

**Conductor workflow**: Plan → Pull details → Create guardrails → Implement

### Endor Labs Extension

Security analysis and dependency checks:

```bash
# Install
gemini extensions install https://github.com/endorlabs/gemini-extension

# Use for security scanning
gemini "Use Endor Labs to check for vulnerabilities in this project" -o text
```

### List Extensions

```bash
gemini --list-extensions
# or
gemini -l
```

## Integration Patterns

### Pattern 1: Generate-Review-Fix Cycle

```bash
# 1. Generate
gemini "Create a user auth module with bcrypt and JWT" --yolo -o text

# 2. Review (Gemini reviews its own work)
gemini "Review auth.js for security vulnerabilities" -o text

# 3. Fix identified issues
gemini "Fix in auth.js: XSS risk, add input validation. Apply now." --yolo -o text
```

### Pattern 2: Background Execution

For long tasks, run in background:

```bash
gemini "Generate comprehensive tests" --yolo -o text 2>&1 &
echo $!  # Get PID

# Multiple parallel tasks
gemini "Create frontend" --yolo -o text 2>&1 &
gemini "Create backend" --yolo -o text 2>&1 &
gemini "Create tests" --yolo -o text 2>&1 &
wait
```

### Pattern 3: Cross-Validation with Claude

```bash
# Claude generates → Gemini reviews
# (After Claude writes code)
gemini "Review this code for bugs and security issues: [paste code]" -o text

# Gemini generates → Claude reviews
gemini "Create [code]" --yolo -o text
# Then Claude reviews the output
```

### Pattern 4: Session Continuity

```bash
# Initial task
gemini "Analyze this codebase architecture" -o text

# List sessions
gemini --list-sessions

# Resume for follow-up
echo "What patterns did you find?" | gemini -r 1 -o text

# Further refinement
echo "Focus on authentication flow" | gemini -r 1 -o text
```

## JSON Output Processing

```bash
gemini "your prompt" -o json 2>&1
```

Response structure:
```json
{
  "response": "The actual response content",
  "stats": {
    "models": {
      "gemini-3-pro": {
        "tokens": {
          "prompt": 1500,
          "candidates": 500,
          "total": 2000,
          "cached": 800
        }
      }
    },
    "tools": {
      "totalCalls": 2,
      "byName": {
        "google_web_search": {"count": 1, "success": 1}
      }
    }
  }
}
```

## Configuration

### Settings Location

Priority order:
1. `/etc/gemini-cli/settings.json` (system)
2. `~/.gemini/settings.json` (user)
3. `.gemini/settings.json` (project)

### Project Context (GEMINI.md)

Create `.gemini/GEMINI.md` in project root:

```markdown
# Project Context

This is a TypeScript React app.

## Coding Standards
- Use functional components
- Prefer hooks over classes
- All functions need JSDoc
```

### Ignore Files (.geminiignore)

```
node_modules/
dist/
*.log
.env
```

## Quick Reference Commands

| Task | Command |
|------|---------|
| Basic query | `gemini "prompt" --yolo -o text` |
| Web search | `gemini "prompt. Use Google Search." -o text` |
| Architecture | `gemini "Use codebase_investigator..." -o text` |
| Fast model | `gemini "prompt" -m gemini-2.5-flash -o text` |
| JSON output | `gemini "prompt" -o json` |
| Resume session | `echo "follow-up" \| gemini -r 1 -o text` |
| List sessions | `gemini --list-sessions` |
| List extensions | `gemini --list-extensions` |

## Rate Limit Strategies

1. **Let auto-retry handle it**: Default behavior with backoff
2. **Use Flash for lower priority**: Different quota
3. **Batch operations**: Combine into single prompts
4. **Add delays**: `sleep 2` between calls in scripts

## Error Handling

### Common Issues

| Issue | Solution |
|-------|----------|
| "API key not found" | Set `GEMINI_API_KEY` env var |
| "Rate limit exceeded" | Wait for auto-retry or use Flash |
| "Context too large" | Use `.geminiignore` or be specific |
| "Tool call failed" | Check JSON stats for details |

### Debug Mode

```bash
gemini "prompt" --debug -o text
```

## Validation After Generation

Always verify Gemini's output:
- Check for security vulnerabilities (XSS, injection)
- Test functionality matches requirements
- Review code style consistency
- Verify dependencies are appropriate

## See Also

- `references/command_reference.md` - Complete CLI flags
- `references/tools.md` - Built-in tools documentation
- `references/patterns.md` - Advanced integration patterns
- `references/templates.md` - Reusable prompt templates

---

## Integration with Claude Code Task Primitive (v2.65.2)

### Overview

Gemini CLI is now **fully integrated with Claude Code Task Primitive**. Every Gemini execution creates a traceable task in `~/.claude/tasks/<session>/tasks.json`, making it visible in **claude-task-viewer**.

### How It Works

```
User: /gemini-cli "Analyze authentication flow"
    ↓
Claude: TaskCreate → Task (subagent: gemini-cli)
    ↓
Hook: task-project-tracker.sh (PostToolUse)
    ↓
Task gets: project metadata, tool="gemini", session_id
    ↓
Global Sync: global-task-sync.sh → ~/.claude/tasks/<session>/tasks.json
    ↓
claude-task-viewer: Shows task with project filter
```

### Automatic Task Creation

Tasks are created automatically via hooks when you invoke `/gemini-cli`:

| Component | Role |
|-----------|------|
| `task-project-tracker.sh` | Adds `project` and `tool` fields to tasks |
| `global-task-sync.sh` | Syncs tasks to global `~/.claude/tasks/` |
| `project-backup-metadata.sh` | Tracks session by project |

### Task Metadata Structure

```json
{
  "id": "1",
  "subject": "Gemini analysis: authentication flow",
  "description": "Use codebase_investigator to map auth dependencies",
  "activeForm": "Running Gemini analysis...",
  "status": "in_progress",
  "project": {
    "path": "/Users/.../my-repo",
    "repo": "owner/my-repo",
    "branch": "main"
  },
  "tool": "gemini",
  "metadata": {
    "model": "gemini-3-pro",
    "capabilities": ["google_web_search", "codebase_investigator"]
  }
}
```

### Viewing Gemini Tasks

```bash
# Open claude-task-viewer
npx claude-task-viewer --open

# Filter by project
# → Shows all gemini tasks with project metadata

# List tasks from CLI
ls -la ~/.claude/tasks/*/tasks.json
cat ~/.claude/tasks/ralph-*/tasks.json | jq '.tasks[] | select(.tool == "gemini")'
```

### Integration with Adversarial Council

Gemini works seamlessly with adversarial:

```bash
# 1. Create adversarial task
/adversarial --council "Design rate limiter"

# 2. Gemini runs as one of the council members
#    → Task shows: tool="adversarial", metadata.council_mode="council"

# 3. Both adversarial and gemini tasks are tracked
#    → Full visibility in claude-task-viewer
```

### Cross-Validation Pattern

Gemini provides excellent second opinion when combined with Claude:

```bash
# Claude writes code
# Then Gemini reviews
/gemini-cli "Review the auth module for security issues"

# Both executions tracked separately
# → Full audit trail in claude-task-viewer
```

### Session Continuity

Gemini sessions are preserved across Claude Code sessions:

```bash
# Session stored in: ~/.claude/tasks/<session>/tasks.json

# List previous sessions
gemini --list-sessions

# Resume with task update
echo "continue analysis" | gemini -r 1

# Task automatically updated with new session_id
```

### Web Search Grounding

Gemini's web search is also tracked:

```bash
/gemini-cli "What are the latest React 19 features? Use Google Search."

# Task includes:
#   metadata.capabilities: ["google_web_search"]
#   → Visible in task viewer
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Task not appearing in viewer | Check `task-project-tracker.sh` is registered in settings.json |
| Missing project metadata | Verify `project-backup-metadata.sh` ran on session start |
| Task sync failed | Check `~/.ralph/logs/global-task-sync.log` |
| Gemini session not tracked | Ensure `tool: "gemini"` is added by hook |
