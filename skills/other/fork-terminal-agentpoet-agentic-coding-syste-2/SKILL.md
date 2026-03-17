---
name: Fork Terminal
description: Spawn parallel AI agents in new terminal windows for true concurrency
triggers:
  - "fork terminal"
  - "spawn agent"
  - "parallel execution"
  - "fork"
  - "run in parallel"
---

# Fork Terminal Skill

Execute multiple AI agents concurrently in separate terminal windows, each with full context and task isolation.

## Core Concept

**Compute Advantage Equation**:
```
Engineering Output = (# of Parallel Agents) × (Quality of Specs) × (Agent Autonomy)
```

Forking terminals allows you to multiply your development capacity by running agents in parallel.

## Supported Agents

| Agent | Command Prefix | Best For |
|-------|---------------|----------|
| Claude Code | `claude code` | Backend, architecture, TypeScript, Python, full-stack |
| Gemini CLI | `gemini` | Frontend, UI/UX, design, animations, creative work |
| GPT-4 CLI | `gpt4` | Documentation, content, general tasks |

## Usage Patterns

### Single Fork
```bash
"fork terminal use claude code to implement backend API from specs/api-spec.md"
```

### Multiple Parallel Forks
```bash
"fork 3 terminals:
 1. Claude Code: Implement database migrations
 2. Gemini: Design and build UI components
 3. Claude Code: Write integration tests"
```

### With Model Override
```bash
"fork terminal use claude code with opus model to refactor entire codebase architecture"
```

## Context Handoff

When forking, automatically pass:
- Current project specification (SPEC_TEMPLATE.md)
- Recent conversation (last 5-10 messages)
- Relevant file paths and contents
- Active task from TodoWrite
- Project context from CLAUDE.md

## Implementation

Uses `fork_terminal.py` (if available) or manual terminal spawning:

1. Detect OS (macOS: `open`, Linux: `gnome-terminal` or `xterm`, Windows: `cmd`)
2. Spawn new terminal window
3. Navigate to project directory
4. Start agent with context file
5. Monitor via logs in `temp/logs/fork-{timestamp}.log`

## Git Worktree Integration

For complete isolation:

```bash
# Create isolated environment
git worktree add ../project-feature-x -b feature/x

# Fork into worktree
"fork terminal in worktree ../project-feature-x use claude code to implement feature X"
```

Each agent works in separate git worktree = zero conflicts.

## Monitoring

All forked agents log to:
- `temp/logs/fork-{agent}-{timestamp}.log`
- Monitored via hooks system (if enabled)
- Aggregated in main session

## Best Practices

**When to Fork**:
- Independent features that can be built in parallel
- Frontend + Backend simultaneous development
- Research while implementation continues
- Testing while new features are being developed

**When NOT to Fork**:
- Tasks depend on each other sequentially
- Single file needs editing by multiple agents (conflicts)
- Simple tasks that take <5 minutes

## Example Workflows

### Full-Stack Parallel Development
```bash
"I'm building a SaaS dashboard.

Fork 3 terminals:
1. Claude Code: Create Next.js API routes for user management
   - Read: SPEC_TEMPLATE.md section on backend
   - Create: src/app/api/users/route.ts
   - Implement: CRUD operations with Supabase

2. Gemini: Design dashboard UI components
   - Read: SPEC_TEMPLATE.md section on UI requirements
   - Reference: .ai/design.json for design system
   - Create: src/components/Dashboard.tsx

3. Claude Code: Set up database schema and RLS
   - Read: SPEC_TEMPLATE.md database requirements
   - Create: database/migrations/001_initial_schema.sql
   - Enable: RLS on all tables"
```

### Research + Implementation
```bash
"fork 2 terminals:
1. Claude Code (research): Research best practices for WebSocket implementation in Next.js 14
   - Use Deep Research skill
   - Save findings to: temp/research/websocket-patterns.md

2. Claude Code (implementation): Continue building REST API
   - Complete all CRUD endpoints
   - Add error handling
   - Write tests"
```

### Experimental Approaches
```bash
"fork 2 terminals to try different approaches:
1. Claude Code: Implement feature using LangGraph multi-agent pattern
2. Claude Code: Implement same feature using simple sequential processing

Test both, keep the better one."
```

## Integration with Main Session

Forked agents report back by:
1. Updating shared `PROGRESS.md`
2. Committing code to feature branches
3. Adding entries to `directives/learning.json`
4. Logging to `temp/logs/`

Main session monitors forks and can:
- Check progress via log files
- Review commits via `git log`
- Aggregate results when forks complete

---

**Remember**: Forking is about multiplying your capacity. Use it liberally for parallel work!
