---
name: delegate-to-agent
description: "Intelligently delegate to native sub-agents for isolated context work. Use when user says 'background', 'parallel', 'deep dive', 'isolated', or when task would pollute main context."
allowed-tools: Task
---

# Delegate to Agent

You are an intelligent router that decides when to delegate tasks to native sub-agents vs handling them in the main conversation.

## When To Use

- User explicitly requests "background", "parallel", or "isolated" execution
- Task involves reading 10+ files (would pollute context)
- Security audit requiring isolation
- Long-running operations (tests, builds)
- Complex multi-area exploration
- User says "deep dive" or "thorough exploration"

---

## Very Aggressive Auto-Triggers (NO user request needed)

**CRITICAL**: These triggers fire AUTOMATICALLY based on context signals. Do NOT wait for user to say "background" or "parallel".

### Exploration Triggers (→ Explore or deep-research agent)
| Signal | Action |
|--------|--------|
| Glob/Grep will return >5 files | Spawn Explore agent instead of running directly |
| "Find all", "where is", "how does X work" | Delegate immediately to deep-research |
| Codebase question without specific file path | Delegate to Explore |
| Need to understand unfamiliar code area | Delegate to deep-research |

### Duration Triggers (→ background-worker with run_in_background: true)
| Command Pattern | Action |
|-----------------|--------|
| `npm install/build/test` | Always run in background |
| `pytest/jest/go test/cargo test` | Always run in background |
| `docker build/compose` | Always run in background |
| Any `--watch` flag | Always run in background |
| Estimated >15 seconds | Run in background |

### Security Triggers (→ security-auditor in background)
| Signal | Action |
|--------|--------|
| About to edit auth/login/password/token files | Spawn security-auditor |
| Touching .env, secrets, credentials, API keys | Spawn security-auditor |
| Before any PR creation | Spawn security-auditor |
| Modifying auth middleware or CORS config | Spawn security-auditor |

### Context Triggers (→ delegate + checkpoint)
| Context Level | Action |
|---------------|--------|
| >30% AND complex task ahead | Delegate exploration to subagent |
| >40% | Delegate ALL remaining discovery work |
| >50% | Create handoff, delegate remaining implementation |
| >60% | Stop, create handoff, instruct /compact |

### Parallel Triggers (→ multi-agent-coordinator)
| Signal | Action |
|--------|--------|
| Multiple independent file groups identified | Spawn parallel agents |
| "Review all X" across codebase | Batch into parallel agents |
| 3+ validators apply (tests, lint, security) | Run all in parallel |

## When NOT to Use

- Simple, quick tasks
- Tasks requiring immediate feedback
- Tasks needing main conversation context
- Single file operations
- User wants to see progress in real-time

## Decision Matrix (Aggressive Thresholds)

| Condition | Agent | Threshold | Reason |
|-----------|-------|-----------|--------|
| File search/exploration | Explore | >5 files | Context savings 87% |
| Security review | security-auditor | Any auth file | Isolated, thorough |
| Find all X across codebase | deep-research | Always | Context-heavy |
| Run tests/build | background-worker | >15 seconds | Non-blocking |
| Multiple exploration areas | multi-agent-coordinator | 3+ areas | Parallel efficiency |
| Codebase understanding | Explore | Any "how does" | Fast haiku agent |
| Quick single-file lookup | None (direct) | 1-2 files | Overhead not worth it |
| Need real-time feedback | None (direct) | User watching | Agents return on completion |

**Key Change from v7.3:** Threshold reduced from 10 files to 5 files. Bias toward delegation.

## Agent Routing

### security-auditor
**Trigger phrases**: "security audit", "OWASP", "vulnerabilities", "secrets scan", "penetration test"
**Model**: sonnet (complex reasoning)
**Tools**: Read, Grep, Glob, Bash (read-only)

```
Delegate to security-auditor when:
- Pre-deployment security check needed
- Reviewing auth/data handling code
- Looking for hardcoded secrets
- OWASP compliance check
```

### deep-research
**Trigger phrases**: "explore", "find all", "how does X work", "trace", "understand codebase"
**Model**: haiku (fast, low-cost)
**Tools**: Read, Grep, Glob, WebFetch, WebSearch

```
Delegate to deep-research when:
- Understanding unfamiliar code
- Finding all usages of function/pattern
- Mapping dependencies
- Reading documentation
- Would read 10+ files
```

### background-worker
**Trigger phrases**: "run tests", "build", "background", "parallel", "don't wait"
**Model**: haiku (fast)
**Tools**: Bash, Read, Write
**Permission**: acceptEdits (auto-approve)

```
Delegate to background-worker when:
- Test suite takes >30 seconds
- Build processes
- Database migrations
- Any long-running script
```

### multi-agent-coordinator
**Trigger phrases**: "coordinate", "multiple agents", "parallel exploration", "divide and conquer"
**Model**: sonnet (orchestration logic)
**Tools**: Read, Grep, Glob, Bash

```
Delegate to multi-agent-coordinator when:
- Complex task benefits from parallelization
- Need to explore multiple areas simultaneously
- Task has independent subtasks
- Need specialized agents working together
```

## Workflow

### 0. Auto-Delegation Check (BEFORE any action)

**Run this check BEFORE every tool use in any skill:**

```
1. FILE COUNT CHECK
   Question: Will this search/read >5 files?
   If YES → Spawn Explore agent, return summary only

2. DURATION CHECK
   Question: Is this npm/pytest/docker/build command?
   If YES → Use run_in_background: true, store task_id

3. CONTEXT CHECK
   Question: Is context >30%?
   If YES + complex task → Delegate exploration
   If >50% → Create handoff, delegate remaining

4. SECURITY CHECK
   Question: Touching auth/secrets/credentials?
   If YES → Spawn security-auditor in background
```

**Example: Before running a Grep**
```
About to: Grep for "handleAuth" across codebase
Check 1: Will return >5 files? → Likely yes
Action: Spawn Explore agent instead
        Prompt: "Find all handleAuth usages, return file:line summary"
        Agent returns: 8 files listed with context
        Main context: receives 500 tokens, not 8000
```

### 1. Analyze Request

Determine if delegation is appropriate:
```
Questions:
- Will this read many files? → deep-research
- Is this security-sensitive? → security-auditor
- Will this take >30 seconds? → background-worker
- Can this be parallelized? → multi-agent-coordinator
- Is this quick/simple? → Don't delegate
```

### 2. Select Agent

Match request to most appropriate agent based on:
- Task type
- Expected duration
- Context sensitivity
- Parallelization potential

### 3. Formulate Prompt

Create clear, actionable prompt for the agent:
```markdown
## Task
[Clear description of what to do]

## Scope
[Files/directories to focus on]

## Expected Output
[What format to return results in]

## Constraints
[Any limitations or focuses]
```

### 4. Invoke Agent

Use Task tool to spawn agent:
```
Task:
  subagent_type: [agent-name]
  description: [short description]
  prompt: [detailed prompt]
  run_in_background: [true/false]
```

### 5. Handle Results

- Summarize agent findings for user
- Highlight key discoveries
- Recommend next steps

## Prompt Templates

### For deep-research
```
Explore the codebase to understand [topic].

Focus areas:
- [Area 1]
- [Area 2]

Return:
- Key findings with file paths
- Code patterns discovered
- Dependency relationships
- Recommendations
```

### For security-auditor
```
Perform security audit on [scope].

Check for:
- OWASP Top 10 vulnerabilities
- Hardcoded secrets
- Auth/authz issues
- Input validation

Return:
- Findings by severity
- Specific file:line locations
- Remediation recommendations
```

### For background-worker
```
Run [command/process].

Expected duration: [estimate]
Success criteria: [what indicates success]

Return:
- Exit status
- Key output (summarized)
- Any failures with details
```

### For multi-agent-coordinator
```
Coordinate exploration of [complex task].

Subtasks:
1. [Subtask 1] - can parallelize
2. [Subtask 2] - depends on 1
3. [Subtask 3] - can parallelize

Synthesize findings into unified report.
```

## Background Task Patterns

### Using run_in_background: true

For long-running commands (>15 seconds), use background execution:

```
Task:
  subagent_type: background-worker
  description: "Run test suite"
  prompt: "Run pytest, report pass/fail summary"
  run_in_background: true
```

This returns immediately with a `task_id`. Continue working on other tasks.

### Polling with TaskOutput

Check background task status when needed:

```
TaskOutput:
  task_id: "abc123"
  block: false  # Non-blocking check
```

Returns:
- `status`: running | completed | failed
- `result`: Output when completed

### Parallel Background Pattern

Spawn multiple background tasks simultaneously:

```
# In single message, spawn 3 agents:
Task: { subagent_type: "background-worker", prompt: "npm test", run_in_background: true }
Task: { subagent_type: "background-worker", prompt: "npm lint", run_in_background: true }
Task: { subagent_type: "security-auditor", prompt: "Security scan", run_in_background: true }

# Continue with implementation work...

# Before commit, poll all:
TaskOutput: { task_id: "test_id" }
TaskOutput: { task_id: "lint_id" }
TaskOutput: { task_id: "security_id" }

# Aggregate: "Tests: PASS, Lint: 2 warnings, Security: No issues"
```

## Anti-Patterns

- Delegating trivial tasks (overhead exceeds benefit)
- Not providing enough context to agent
- Running agents when real-time feedback needed
- Over-parallelizing simple sequential tasks
- Not summarizing agent results for user
- **NEW:** Waiting for background tasks when you could continue working
- **NEW:** Running tests/builds synchronously when they could be background

## Integration with Skills

Some tasks are better handled by skills:
- Quick code review → code-reviewer skill
- Simple debugging → debugger skill
- Single file edit → refactorer skill

**Rule of thumb**: If task can be done in <30 seconds with minimal file reads, use a skill instead.

## Keywords

delegate, background, parallel, isolated, sub-agent, spawn, coordinate, async, long-running
