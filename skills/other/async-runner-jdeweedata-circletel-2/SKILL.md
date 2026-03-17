---
name: async-runner
description: Run background agents and bash commands asynchronously for CircleTel development. Use when running dev servers, parallel tests, long builds, or multi-agent research tasks without blocking the main workflow.
---

# Async Task Runner

Skill for managing asynchronous background tasks and agents in CircleTel development.

## When to Use

This skill activates when you:
- Need to run dev server while coding
- Want parallel test execution
- Run long builds in background
- Spawn research agents for codebase exploration
- Monitor logs while implementing fixes

**Keywords**: background, parallel, async, spawn, concurrent, dev server, watch, monitor, simultaneously

## Quick Reference

| Action | Command/Method |
|--------|----------------|
| Background bash | `Ctrl+B` or append `&` |
| Check running tasks | `/tasks` |
| Kill background task | Use task ID from `/tasks` |
| Spawn background agent | Task tool with `run_in_background: true` |

## Background Bash Commands

### Development Server (Always Background)
```bash
# Start dev server - never blocks
npm run dev:memory &
```

### Parallel Test Execution
Ask Claude:
```
"Run these tests in parallel:
1. Type check
2. Unit tests
3. E2E tests

Continue working on the auth fix while they run."
```

Claude will spawn:
```bash
npm run type-check:memory &
npm run test &
npm run test:e2e &
```

### Long-Running Builds
```
"Start the production build in background while I review code"
```

Claude runs:
```bash
npm run build:memory &
```
Then continues with your code review.

### Log Monitoring
```
"Tail the Supabase logs in background while I debug"
```

## Background Agents

### Parallel Research
```
"Spawn 3 Explore agents in parallel:
1. Investigate how auth works in /app/dashboard
2. Map the payment flow in /app/checkout
3. Document the coverage API integration"
```

Claude spawns specialized Explore agents that run concurrently. Results come back asynchronously.

### Multi-File Analysis
```
"Analyze these files in parallel:
1. app/api/payment/route.ts - check error handling
2. lib/payment/netcash.ts - review integration
3. components/checkout/PaymentForm.tsx - check validation"
```

### Codebase Exploration
```
"Use Explore agents to find:
1. All files that import CustomerAuthProvider
2. All API routes that use service role
3. All components with loading states"
```

## CircleTel-Specific Patterns

### Full Development Setup
```
"Start my development environment:
1. Dev server (background)
2. Supabase logs (background)
3. Then start working on the billing feature"
```

Spawns:
```bash
npm run dev:memory &
npx supabase functions serve &
```
Then begins coding.

### Pre-Commit Workflow
```
"Run all checks in parallel before I commit:
- Type check
- Lint
- Build
- Tests"
```

### Deployment Verification
```
"Run pre-deploy checks in background while I write the PR description:
1. Full type check
2. Production build
3. E2E tests"
```

## Task Management

### Check Running Tasks
```
/tasks
```
Shows all background bash processes and agents.

### Monitor Task Output
```
"Show me the output from the background build"
```

Claude retrieves output via TaskOutputTool.

### Cancel Task
```
"Kill the dev server"
```

Or use task ID:
```
"Kill task abc123"
```

## When to Use Background

### Always Background
- `npm run dev` / `npm run dev:memory`
- `npm run watch`
- Log tailing (`tail -f`, `supabase logs`)
- Long builds (`npm run build:memory`)

### Run in Parallel
- Independent test suites
- Multiple lint checks
- Codebase exploration
- File analysis tasks

### Run Sequentially
- Dependent operations (build → deploy)
- Database migrations
- Git operations
- File modifications to same files

## Resource Considerations

### Memory Usage (Approximate)
| Process | Memory |
|---------|--------|
| Dev server | ~500MB |
| Build | ~2GB |
| Type check | ~1GB |
| Tests | ~1GB |

**Recommendation**: Limit to 2-3 heavy tasks simultaneously.

### When NOT to Background
- Interactive commands (`npm init`)
- Commands requiring user input
- Quick one-time commands (`git status`)
- Commands that need immediate results

## Integration with Other Skills

### With Session Manager
```
# Name session for async work
/rename dashboard-tests

# Start background tasks
"Run all dashboard E2E tests in background"

# Can resume later
claude --resume dashboard-tests
# Background results available
```

### With Context Manager
```
# Background tasks don't consume context
# Use for verbose operations
"Run verbose build in background"
# Build output doesn't fill context window
```

### With Stats Tracker
```
# Background agents still count toward usage
# But more efficient than sequential
/stats  # Check usage after parallel work
```

## Examples

### Example 1: Feature Development
```
You: "Start dev server and begin working on the payment form"

Claude:
- Starts: npm run dev:memory & (background)
- Immediately begins: Reading PaymentForm.tsx
- Dev server running while coding
```

### Example 2: Bug Investigation
```
You: "Investigate this timeout error from multiple angles in parallel"

Claude spawns 3 Explore agents:
- Agent 1: Checks API route error handling
- Agent 2: Reviews database query performance
- Agent 3: Analyzes frontend retry logic

All run concurrently, results aggregated.
```

### Example 3: Release Preparation
```
You: "Run full test suite in background while I update the changelog"

Claude:
- Background: npm run type-check:memory &
- Background: npm run build:memory &
- Background: npm run test:e2e &
- Foreground: Opens CHANGELOG.md for editing

Reports results as each completes.
```

## Best Practices

1. **Always background dev servers** - Never block with `npm run dev`
2. **Parallel for independent tasks** - Tests, lints, builds together
3. **Sequential for dependencies** - Build before deploy
4. **Use Explore agents** - Faster, uses efficient Haiku model
5. **Monitor resource usage** - Don't overload system
6. **Check task status** - Use `/tasks` to track
7. **Clean up finished tasks** - Kill completed background processes

## Troubleshooting

### Background task not starting
```
# Check if command is valid
npm run dev:memory  # Test without &

# Then add background
npm run dev:memory &
```

### Can't see background output
```
"Show output from background task [name/id]"
```

### Too many background tasks
```
# List all
/tasks

# Kill unnecessary ones
"Kill the old dev server"
```

---

**Version**: 1.0.0
**Last Updated**: 2025-12-10
**For**: Claude Code v2.0.64+
