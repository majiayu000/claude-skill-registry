---
name: gemini-cli-integration
description: Comprehensive guide for integrating Gemini CLI as research assistant. Use when you need to delegate research to Gemini, understand its capabilities vs Claude's, or determine the right tool for a task.
---

# Gemini CLI Integration

**Position Gemini CLI as Claude's research assistant** - delegate when you need web-grounded information, codebase investigation, or sophisticated reasoning that benefits from Google Search backing.

## Core Principle: Division of Labor

```
┌─────────────────────┐         ┌──────────────────────┐
│   GEMINI CLI        │         │   CLAUDE CODE        │
│   Research Wing     │────────>│   Implementation     │
└─────────────────────┘         └──────────────────────┘

Gemini: Investigate               Claude: Execute
- Web-grounded research          - File operations
- Codebase analysis              - Code edits
- Current docs lookup            - Following patterns
- Sophisticated reasoning        - Agent orchestration
- Multimodal analysis            - Workflow automation
```

## Gemini CLI Capabilities

### 1. Google Search Grounding ⭐ **KEY DIFFERENTIATOR**
**What:** Real-time access to Google Search results within responses
**When to use:**
- Need current framework documentation (post-Jan 2025)
- Looking up error messages and solutions
- Researching best practices and emerging patterns
- Finding library comparisons and benchmarks
- Understanding breaking changes in new releases

**Example:**
```bash
gemini "What are the breaking changes in Next.js 15?"
gemini "Best practices for React Server Components in 2025"
gemini "How to fix ECONNRESET errors in Node.js"
```

### 2. Codebase Investigator Agent ⭐ **KEY DIFFERENTIATOR**
**What:** Autonomous agent that maps entire codebase architecture
**When to use:**
- Investigating unfamiliar codebases
- Understanding system-wide dependencies
- Identifying technical debt patterns
- Root-cause analysis across multiple modules

**Example:**
```bash
gemini "Analyze this codebase and map out:
1. Core architectural patterns
2. Module dependencies
3. Data flow
4. Testing strategy
5. Technical debt areas"
```

### 3. Massive Context Window
**What:** 1M tokens (vs Claude's 200k in standard mode)
**When to use:**
- Analyzing entire documentation sets
- Processing very large codebases
- Reviewing extensive conversation history

### 4. Multimodal Analysis
**What:** Process images, PDFs, diagrams alongside text
**When to use:**
- Analyzing architecture diagrams
- Reviewing UI mockups or screenshots
- Processing technical documentation PDFs
- Debugging from error screenshots

**Example:**
```bash
# Analyze diagram
gemini "Explain this architecture diagram and identify potential issues" < diagram.png

# Process PDF documentation
gemini "Summarize the key APIs from this documentation" < api-docs.pdf
```

### 5. Shell Interpolation
**What:** Inject live shell command output into prompts using `!{command}`
**When to use:** Dynamic context in GEMINI.md custom commands
**Example:**
```toml
prompt = """
Current git status:
!{git status --short}

Recent commits:
!{git log --oneline -5}

Analyze the current state and suggest next steps.
"""
```

### 6. Advanced Reasoning (Gemini 3 Pro)
**What:** State-of-the-art reasoning capabilities
**When to use:**
- Complex technical problem-solving
- Architectural decision analysis
- Tradeoff evaluation
- Debugging intricate issues

## Claude Code Capabilities (Stay in Claude for These)

### 1. Superior File Operations
- **Edit tool**: Precise string replacement in files
- **Write tool**: Create new files efficiently
- **Read tool**: Fast file reading with line ranges
- **MultiEdit**: Batch edits across files

### 2. Agent Orchestration
- **Task tool**: Launch specialized subagents in parallel
- Multiple specialized agents (architecture-strategist, code-simplicity-reviewer, etc.)
- Sophisticated workflow coordination

### 3. Project Pattern Recognition
- Understands established codebase patterns
- Maintains consistency with existing code
- Follows project-specific conventions
- Respects CLAUDE.md instructions

### 4. Skills System
- Modular skill invocation
- Context-aware best practices
- Domain-specific expertise (testing, documentation, etc.)

## Decision Matrix: Claude vs Gemini

| Task | Tool | Rationale |
|------|------|-----------|
| Research current framework best practices | **Gemini** | Web grounding gives latest info |
| Implement feature based on design | **Claude** | Superior file operations |
| Investigate unfamiliar codebase | **Gemini** | Codebase Investigator agent |
| Edit files in known codebase | **Claude** | Pattern recognition + Edit tool |
| Look up error solution | **Gemini** | Google Search grounding |
| Orchestrate multiple agents | **Claude** | Task tool + specialized agents |
| Analyze architecture diagram | **Gemini** | Multimodal analysis |
| Follow project conventions | **Claude** | Understands CLAUDE.md context |
| Debug with web research | **Gemini** | Real-time docs + Search |
| Refactor existing code | **Claude** | File operations + patterns |
| Understand new library API | **Gemini** | Latest docs via Search |
| Run slash commands | **Claude** | Designed for Claude's workflow |
| Design/UX research before frontend work | **Gemini** | Current trends, real examples, anti-convergence |

## Integration Patterns

### Pattern 1: Research → Implement
```
1. Use Gemini for research
   gemini "/research Best practices for WebSocket in Next.js"

2. Document findings in RESEARCH.md

3. Return to Claude for implementation
   /architect (design based on research)
   /plan (create tasks)
   /execute (implement with Claude)
```

### Pattern 2: Investigate → Fix
```
1. Gemini investigates error
   gemini "Analyze this error and suggest root cause"

2. Claude implements fix
   /execute (make the changes)
   /verify (run tests)
```

### Pattern 3: Parallel Research
```
# Launch multiple Gemini sessions in parallel for different research topics
Terminal 1: gemini "Research authentication patterns"
Terminal 2: gemini "Research state management options"
Terminal 3: gemini "Research API design best practices"

# Consolidate findings in Claude
```

### Pattern 4: Design Research → Implement
```
1. Gemini researches design direction
   gemini -p "Research distinctive approaches for [component type]"

2. Claude synthesizes and implements
   /skill frontend-design (apply research to implementation)
```

## When to Explicitly Suggest Gemini

Claude should proactively suggest delegating to Gemini when:

### Trigger Phrases from User:
- "What are current best practices for..."
- "How do people typically implement..."
- "I'm not familiar with this codebase..."
- "What's the latest on..."
- "Research whether..."
- "Investigate this error..."

### Contextual Signals:
- User is about to implement something unfamiliar
- Need information about tools/frameworks after Jan 2025
- Working with an unfamiliar codebase
- Facing an error that needs web research
- Evaluating multiple technical options

### Frontend/UX Work (ALWAYS):
- Building any new UI component
- Designing page layouts
- Choosing typography, colors, or visual direction
- Creating user flows or interactions

### Example Response:
```
I can help implement this, but first let's research current best practices
using Gemini CLI's web grounding:

    gemini "What are Next.js 15 best practices for data fetching?"

This will give us the latest recommendations, then I can implement
following those patterns.
```

## Gemini CLI Command Reference

### Basic Usage
```bash
# Interactive mode (default)
gemini
gemini "your prompt here"

# Non-interactive mode
gemini --prompt "your prompt here"
gemini --prompt "your prompt" > output.txt

# Continue in interactive after prompt
gemini --prompt-interactive "start with this"
```

### Modes
```bash
# YOLO mode (auto-approve all actions)
gemini --yolo "fix the failing tests"

# Sandbox mode (safer execution)
gemini --sandbox "install dependencies"

# Resume previous session
gemini --resume latest
gemini --resume 3  # Resume session #3
```

### Session Management
```bash
# List previous sessions
gemini --list-sessions

# Delete a session
gemini --delete-session 3
```

### Extensions & MCP
```bash
# List available extensions
gemini --list-extensions

# Use specific extensions
gemini -e extension1 -e extension2

# MCP server management
gemini mcp list
gemini mcp add server-name command [args...]
gemini mcp remove server-name
```

### Output Formats
```bash
# JSON output for scripting
gemini --output-format json "analyze code"

# Streaming JSON
gemini --output-format stream-json "long analysis"
```

## Best Practices

### DO:
✅ Use Gemini for web-grounded research before implementing unfamiliar features
✅ Delegate codebase investigation to Codebase Investigator agent
✅ Use multimodal capabilities for diagram/screenshot analysis
✅ Bring research findings back to Claude for implementation
✅ Use non-interactive mode in scripts and automation
✅ Leverage Google Search grounding for current best practices

### DON'T:
❌ Use Gemini for file edits in known codebases (Claude's Edit tool is better)
❌ Use Gemini when pattern matching matters (Claude knows project conventions)
❌ Use Gemini for agent orchestration (Claude's Task tool is superior)
❌ Duplicate work - if Gemini researched it, don't re-research in Claude
❌ Use Gemini for tasks that don't benefit from web grounding

## GEMINI.md Configuration

Gemini uses `~/.gemini/GEMINI.md` for project-specific context (like Claude's CLAUDE.md).

**Key differences from Claude:**
- Uses shell interpolation `!{command}` for dynamic context
- Custom commands are TOML format (not markdown)
- Emphasizes Google grounding capabilities

**Current state:** Well-configured GEMINI.md exists at `~/.gemini/GEMINI.md`

## Free Tier Limits

**With Personal Google Account:**
- 60 requests per minute
- 1,000 requests per day
- Access to Gemini 2.5 Pro (1M context)

**Cost-effective for:**
- Daily development research
- Periodic codebase investigations
- Error debugging sessions
- Best practice lookups

## Philosophy: Complementary Tools

```
Gemini CLI ≠ Replacement for Claude
Gemini CLI = Research Assistant for Claude

Claude remains the primary interface for:
- File operations
- Code implementation
- Workflow orchestration
- Project pattern adherence

Gemini serves as specialized tool for:
- Web-grounded research
- Codebase investigation
- Current information lookup
- Multimodal analysis
```

**The Goal:** Use the right tool for each task, creating a powerful workflow where research (Gemini) feeds implementation (Claude).

## Quick Decision Tree

```
Need to write/edit code?
├─ Yes → Use Claude
└─ No → Need current web info?
    ├─ Yes → Use Gemini
    └─ No → Analyzing unfamiliar code?
        ├─ Yes → Use Gemini (Codebase Investigator)
        └─ No → Following project patterns?
            ├─ Yes → Use Claude
            └─ No → Use Gemini for research, Claude for implementation
```

## Summary: When to Suggest Gemini

**Always suggest Gemini for:**
1. Research needing current information (2025 best practices)
2. Investigating unfamiliar codebases
3. Error debugging requiring web search
4. Library/framework comparisons
5. Analyzing visual artifacts (diagrams, screenshots)

**Never suggest Gemini for:**
1. File edits in known codebases
2. Tasks requiring project pattern recognition
3. Workflow orchestration with multiple agents
4. Tasks that don't benefit from web grounding

**The Integration Pattern:**
Research (Gemini) → Document (Claude) → Design (Claude) → Implement (Claude)
