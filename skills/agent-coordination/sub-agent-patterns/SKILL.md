---
name: sub-agent-patterns
description: |
  Comprehensive guide to sub-agents in Claude Code: built-in agents (Explore, Plan, general-purpose), custom agent creation, configuration, and delegation patterns.

  Use when: creating custom sub-agents, delegating bulk operations, parallel research, understanding built-in agents, or configuring agent tools/models.
user-invocable: true
---

# Sub-Agents in Claude Code

**Status**: Production Ready ✅
**Last Updated**: 2026-01-14
**Source**: https://code.claude.com/docs/en/sub-agents

Sub-agents are specialized AI assistants that Claude Code can delegate tasks to. Each sub-agent has its own context window, configurable tools, and custom system prompt.

---

## Why Use Sub-Agents: Context Hygiene

The primary value of sub-agents isn't specialization—it's **keeping your main context clean**.

**Without agent** (context bloat):
```
Main context accumulates:
├─ git status output (50 lines)
├─ npm run build output (200 lines)
├─ tsc --noEmit output (100 lines)
├─ wrangler deploy output (100 lines)
├─ curl health check responses
├─ All reasoning about what to do next
└─ Context: 📈 500+ lines consumed
```

**With agent** (context hygiene):
```
Main context:
├─ "Deploy to cloudflare"
├─ [agent summary - 30 lines]
└─ Context: 📊 ~50 lines consumed

Agent context (isolated):
├─ All verbose tool outputs
├─ All intermediate reasoning
└─ Discarded after returning summary
```

**The math**: A deploy workflow runs ~10 tool calls. That's 500+ lines in main context vs 30-line summary with an agent. Over a session, this compounds dramatically.

**When this matters most**:
- Repeatable workflows (deploy, migrate, audit, review)
- Verbose tool outputs (build logs, test results, API responses)
- Multi-step operations where only the final result matters
- Long sessions where context pressure builds up

**Key insight**: Use agents for **workflows you repeat**, not just for specialization. The context savings compound over time.

---

## Built-in Sub-Agents

Claude Code includes three built-in sub-agents available out of the box:

### Explore Agent

Fast, lightweight agent optimized for **read-only** codebase exploration.

| Property | Value |
|----------|-------|
| **Model** | Haiku (fast, low-latency) |
| **Mode** | Strictly read-only |
| **Tools** | Glob, Grep, Read, Bash (read-only: ls, git status, git log, git diff, find, cat, head, tail) |

**Thoroughness levels** (specify when invoking):
- `quick` - Fast searches, targeted lookups
- `medium` - Balanced speed and thoroughness
- `very thorough` - Comprehensive analysis across multiple locations

**When Claude uses it**: Searching/understanding codebase without making changes. Findings don't bloat the main conversation.

```
User: Where are errors from the client handled?
Claude: [Invokes Explore with "medium" thoroughness]
       → Returns: src/services/process.ts:712
```

### Plan Agent

Specialized for **plan mode** research and information gathering.

| Property | Value |
|----------|-------|
| **Model** | Sonnet |
| **Mode** | Read-only research |
| **Tools** | Read, Glob, Grep, Bash |
| **Invocation** | Automatic in plan mode |

**When Claude uses it**: In plan mode when researching codebase to create a plan. Prevents infinite nesting (sub-agents cannot spawn sub-agents).

### General-Purpose Agent

Capable agent for complex, multi-step tasks requiring both exploration AND action.

| Property | Value |
|----------|-------|
| **Model** | Sonnet |
| **Mode** | Read AND write |
| **Tools** | All tools |
| **Purpose** | Complex research, multi-step operations, code modifications |

**When Claude uses it**:
- Task requires both exploration and modification
- Complex reasoning needed to interpret search results
- Multiple strategies may be needed
- Task has multiple dependent steps

---

## Creating Custom Sub-Agents

### File Locations

| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| Project | `.claude/agents/` | Current project only | Highest |
| User | `~/.claude/agents/` | All projects | Lower |
| CLI | `--agents '{...}'` | Current session | Middle |

When names conflict, project-level takes precedence.

**⚠️ CRITICAL: Session Restart Required**

Agents are loaded at session startup only. If you create new agent files during a session:
1. They won't appear in `/agents`
2. Claude won't be able to invoke them
3. **Solution**: Restart Claude Code session to discover new agents

This is the most common reason custom agents "don't work" - they were created after the session started.

### File Format

Markdown files with YAML frontmatter:

```yaml
---
name: code-reviewer
description: Expert code reviewer. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: inherit
permissionMode: default
skills: project-workflow
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---

Your sub-agent's system prompt goes here.

Include specific instructions, best practices, and constraints.
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens) |
| `description` | Yes | When Claude should use this agent |
| `tools` | No | Comma-separated list. Omit = inherit all tools |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit`. Default: sonnet |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Comma-separated skills to auto-load (sub-agents don't inherit parent skills) |
| `hooks` | No | `PreToolUse`, `PostToolUse`, `Stop` event handlers |

### Available Tools Reference

Complete list of tools that can be assigned to sub-agents:

| Tool | Purpose | Type |
|------|---------|------|
| **Read** | Read files (text, images, PDFs, notebooks) | Read-only |
| **Write** | Create or overwrite files | Write |
| **Edit** | Exact string replacements in files | Write |
| **MultiEdit** | Batch edits to single file | Write |
| **Glob** | File pattern matching (`**/*.ts`) | Read-only |
| **Grep** | Content search with regex (ripgrep) | Read-only |
| **LS** | List directory contents | Read-only |
| **Bash** | Execute shell commands | Execute |
| **BashOutput** | Get output from background shells | Execute |
| **KillShell** | Terminate background shell | Execute |
| **Task** | Spawn sub-agents | Orchestration |
| **WebFetch** | Fetch and analyze web content | Web |
| **WebSearch** | Search the web | Web |
| **TodoWrite** | Create/manage task lists | Organization |
| **TodoRead** | Read current task list | Organization |
| **NotebookRead** | Read Jupyter notebooks | Notebook |
| **NotebookEdit** | Edit Jupyter notebook cells | Notebook |
| **AskUserQuestion** | Interactive user questions | UI |
| **EnterPlanMode** | Enter planning mode | Planning |
| **ExitPlanMode** | Exit planning mode with plan | Planning |
| **Skill** | Execute skills in conversation | Skills |
| **LSP** | Language Server Protocol integration | Advanced |
| **MCPSearch** | MCP tool discovery | Advanced |

**Tool Access Patterns by Agent Type:**

| Agent Type | Recommended Tools | Notes |
|------------|-------------------|-------|
| Read-only reviewers | `Read, Grep, Glob, LS` | No write capability |
| File creators | `Read, Write, Edit, Glob, Grep` | ⚠️ **No Bash** - avoids approval spam |
| Script runners | `Read, Write, Edit, Glob, Grep, Bash` | Use when CLI execution needed |
| Research agents | `Read, Grep, Glob, WebFetch, WebSearch` | Read-only external access |
| Documentation | `Read, Write, Edit, Glob, Grep, WebFetch` | No Bash for cleaner workflow |
| Orchestrators | `Read, Grep, Glob, Task` | Minimal tools, delegates to specialists |
| Full access | Omit `tools` field (inherits all) | Use sparingly |

**⚠️ Tool Access Principle**: If an agent doesn't need Bash, don't give it Bash. Each bash command requires approval, causing workflow interruptions. See "Avoiding Bash Approval Spam" below.

### Avoiding Bash Approval Spam (CRITICAL)

When sub-agents have Bash in their tools list, they often default to using `cat > file << 'EOF'` heredocs for file creation instead of the Write tool. Each unique bash command requires user approval, causing:

- Dozens of approval prompts per agent run
- Slow, frustrating workflow
- Hard to review (heredocs are walls of minified content)

**Root Causes**:
1. **Models default to bash for file ops** - Training data bias toward shell commands
2. **Bash in tools list = Bash gets used** - Even if Write tool is available
3. **Instructions get buried** - A "don't use bash" rule at line 300 of a 450-line prompt gets ignored

**Solutions** (in order of preference):

1. **Remove Bash from tools list** (if not needed):
   ```yaml
   # Before - causes approval spam
   tools: Read, Write, Edit, Glob, Grep, Bash

   # After - clean file operations
   tools: Read, Write, Edit, Glob, Grep
   ```
   If the agent only creates files, it doesn't need Bash. The orchestrator can run necessary scripts after.

2. **Put critical instructions FIRST** (immediately after frontmatter):
   ```markdown
   ---
   name: site-builder
   tools: Read, Write, Edit, Glob, Grep
   model: sonnet
   ---

   ## ⛔ CRITICAL: USE WRITE TOOL FOR ALL FILES

   **You do NOT have Bash access.** Create ALL files using the **Write tool**.

   ---

   [rest of prompt...]
   ```
   Instructions at the top get followed. Instructions buried 300 lines deep get ignored.

3. **Remove contradictory instructions**:
   ```markdown
   # BAD - contradictory
   Line 75: "Copy images with `cp -r intake/images/* build/images/`"
   Line 300: "NEVER use cp, mkdir, cat, or echo"

   # GOOD - consistent
   Only mention the pattern you want used. Remove all bash examples if you want Write tool.
   ```

**When to keep Bash:**
- Agent needs to run external CLIs (wrangler, npm, git)
- Agent needs to execute scripts
- Agent needs to check command outputs

**Testing**: Before vs after removing Bash:
- **Before** (with Bash): 11+ heredoc approval prompts, wrong patterns applied
- **After** (no Bash): Mostly Write tool usage, correct patterns, minimal prompts

### Using /agents Command (Recommended)

```
/agents
```

Interactive menu to:
- View all sub-agents (built-in, user, project)
- Create new sub-agents with guided setup
- Edit existing sub-agents and tool access
- Delete custom sub-agents
- See which sub-agents are active

### CLI Configuration

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

---

## Using Sub-Agents

### Automatic Delegation

Claude proactively delegates based on:
- Task description in your request
- `description` field in sub-agent config
- Current context and available tools

**Tip**: Include "use PROACTIVELY" or "MUST BE USED" in description for more automatic invocation.

### Explicit Invocation

```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

### Resumable Sub-Agents

Sub-agents can be resumed to continue previous conversations:

```
# Initial invocation
> Use the code-analyzer agent to review the auth module
[Agent completes, returns agentId: "abc123"]

# Resume with full context
> Resume agent abc123 and now analyze the authorization logic
```

**Use cases**:
- Long-running research across multiple sessions
- Iterative refinement without losing context
- Multi-step workflows with maintained context

### Disabling Sub-Agents

Add to settings.json permissions:

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(Plan)"]
  }
}
```

Or via CLI:
```bash
claude --disallowedTools "Task(Explore)"
```

---

## Agent Orchestration

Sub-agents can invoke other sub-agents, enabling sophisticated orchestration patterns. This is accomplished by including the `Task` tool in an agent's tool list.

### How It Works

When a sub-agent has access to the `Task` tool, it can:
- Spawn other sub-agents (built-in or custom)
- Coordinate parallel work across specialists
- Chain agents for multi-phase workflows

```yaml
---
name: orchestrator
description: Orchestrator agent that coordinates other specialized agents. Use for complex multi-phase tasks.
tools: Read, Grep, Glob, Task  # ← Task tool enables agent spawning
model: sonnet
---
```

### Orchestrator Pattern

```yaml
---
name: release-orchestrator
description: Coordinates release preparation by delegating to specialized agents. Use before releases.
tools: Read, Grep, Glob, Bash, Task
---

You are a release orchestrator. When invoked:

1. Use Task tool to spawn code-reviewer agent
   → Review all uncommitted changes

2. Use Task tool to spawn test-runner agent
   → Run full test suite

3. Use Task tool to spawn doc-validator agent
   → Check documentation is current

4. Collect all reports and synthesize:
   - Blockers (must fix before release)
   - Warnings (should address)
   - Ready to release: YES/NO

Spawn agents in parallel when tasks are independent.
Wait for all agents before synthesizing final report.
```

### Practical Examples

**Multi-Specialist Workflow:**
```
User: "Prepare this codebase for production"

orchestrator agent:
  ├─ Task(code-reviewer) → Reviews code quality
  ├─ Task(security-auditor) → Checks for vulnerabilities
  ├─ Task(performance-analyzer) → Identifies bottlenecks
  └─ Synthesizes findings into actionable report
```

**Parallel Research:**
```
User: "Compare these 5 frameworks for our use case"

research-orchestrator:
  ├─ Task(general-purpose) → Research framework A
  ├─ Task(general-purpose) → Research framework B
  ├─ Task(general-purpose) → Research framework C
  ├─ Task(general-purpose) → Research framework D
  ├─ Task(general-purpose) → Research framework E
  └─ Synthesizes comparison matrix with recommendation
```

### Nesting Depth

| Level | Example | Status |
|-------|---------|--------|
| 1 | Claude → orchestrator | ✅ Works |
| 2 | orchestrator → code-reviewer | ✅ Works |
| 3 | code-reviewer → sub-task | ⚠️ Works but context gets thin |
| 4+ | Deeper nesting | ❌ Not recommended |

**Best practice**: Keep orchestration to 2 levels deep. Beyond that, context windows shrink and coordination becomes fragile.

### When to Use Orchestration

| Use Orchestration | Use Direct Delegation |
|-------------------|----------------------|
| Complex multi-phase workflows | Single specialist task |
| Need to synthesize from multiple sources | Simple audit or review |
| Parallel execution important | Sequential is fine |
| Different specialists required | Same agent type |

### Orchestrator vs Direct Delegation

**Direct (simpler, often sufficient):**
```
User: "Review my code changes"
Claude: [Invokes code-reviewer agent directly]
```

**Orchestrated (when coordination needed):**
```
User: "Prepare release"
Claude: [Invokes release-orchestrator]
        orchestrator: [Spawns code-reviewer, test-runner, doc-validator]
        orchestrator: [Synthesizes all reports]
        [Returns comprehensive release readiness report]
```

### Configuration Notes

1. **Tool access propagates**: An orchestrator with `Task` can spawn any agent the session has access to
2. **Model inheritance**: Spawned agents use their configured model (or inherit if set to `inherit`)
3. **Context isolation**: Each spawned agent has its own context window
4. **Results bubble up**: Orchestrator receives agent results and can synthesize them

---

## Advanced Patterns

### Background Agents (Async Delegation)

Send agents to the background while continuing work in your main session:

**Ctrl+B** during agent execution moves it to background.

```
> Use the research-agent to analyze these 10 frameworks
[Agent starts working...]
[Press Ctrl+B]
→ Agent continues in background
→ Main session free for other work
→ Check results later with: "What did the research agent find?"
```

**Use cases**:
- Long-running research tasks
- Parallel documentation fetching
- Non-blocking code reviews

### Model Selection Strategy

**Quality-First Approach**: Default to Sonnet for most agents. The cost savings from Haiku rarely outweigh the quality loss.

| Model | Best For | Speed | Cost | Quality |
|-------|----------|-------|------|---------|
| `sonnet` | **Default for most agents** - content generation, reasoning, file creation | Balanced | Standard | ✅ High |
| `opus` | Creative work, complex reasoning, quality-critical outputs | Slower | Premium | ✅ Highest |
| `haiku` | **Only for simple script execution** where quality doesn't matter | 2x faster | 3x cheaper | ⚠️ Variable |
| `inherit` | Match main conversation | Varies | Varies | Matches parent |

**Why Sonnet Default?**

Testing showed significant quality differences:
- **Haiku**: Wrong stylesheet links, missing CSS, wrong values, incorrect patterns
- **Sonnet**: Correct patterns, proper validation, fewer errors

| Task Type | Recommended Model | Why |
|-----------|-------------------|-----|
| Content generation | Sonnet | Quality matters |
| File creation | Sonnet | Patterns must be correct |
| Code writing | Sonnet | Bugs are expensive |
| Audits/reviews | Sonnet | Judgment required |
| Creative work | Opus | Maximum quality |
| Deploy scripts | Haiku (OK) | Just running commands |
| Simple format checks | Haiku (OK) | Pass/fail only |

**Pattern**: Default Sonnet, use Opus for creative, Haiku only when quality truly doesn't matter:

```yaml
---
name: site-builder
model: sonnet  # Content quality matters - NOT haiku
tools: Read, Write, Edit, Glob, Grep
---

---
name: creative-director
model: opus  # Creative work needs maximum quality
tools: Read, Write, Edit, Glob, Grep
---

---
name: deploy-runner
model: haiku  # Just running wrangler commands - quality irrelevant
tools: Read, Bash
---
```

### Agent Context Considerations

Agent context usage depends heavily on the task:

| Scenario | Context | Tool Calls | Works? |
|----------|---------|------------|--------|
| Deep research agent | 130k | 90+ | ✅ Yes |
| Multi-file audit | 80k+ | 50+ | ✅ Yes |
| Simple format check | 3k | 5-10 | ✅ Yes |
| Chained orchestration | Varies | Varies | ✅ Depends on task |

**Reality**: Agents with 90+ tool calls and 130k context work fine when doing meaningful work. The limiting factor is task complexity, not arbitrary token limits.

**What actually matters**:
- Is the agent making progress on each tool call?
- Is context being used for real work vs redundant instructions?
- Are results coherent at the end?

**When context becomes a problem**:
- Agent starts repeating itself or losing track
- Results become incoherent or contradictory
- Agent "forgets" earlier findings in long sessions

### Persona-Based Routing

Prevent agents from drifting into adjacent domains with explicit constraints:

```yaml
---
name: frontend-specialist
description: Frontend code expert. NEVER writes backend logic.
tools: Read, Write, Edit, Glob, Grep
---

You are a frontend specialist.

BOUNDARIES:
- NEVER write backend logic, API routes, or database queries
- ALWAYS use React patterns consistent with the codebase
- If task requires backend work, STOP and report "Requires backend specialist"

FOCUS:
- React components, hooks, state management
- CSS/Tailwind styling
- Client-side routing
- Browser APIs
```

This prevents hallucination when agents encounter unfamiliar domains.

### Hooks Patterns

Hooks enable automated validation and feedback:

**Block-at-commit** (enforce quality gates):
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            if [[ "$BASH_COMMAND" == *"git commit"* ]]; then
              npm test || exit 1
            fi
```

**Hint hooks** (non-blocking feedback):
```yaml
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/lint-check.sh"
          # Exits 0 to continue, non-zero to warn
```

**Best practice**: Validate at commit stage, not mid-plan. Let agents work freely, catch issues before permanent changes.

### Nested CLAUDE.md Context

Claude automatically loads `CLAUDE.md` files from subdirectories when accessing those paths:

```
project/
├── CLAUDE.md              # Root context (always loaded)
├── src/
│   └── CLAUDE.md          # Loaded when editing src/**
├── tests/
│   └── CLAUDE.md          # Loaded when editing tests/**
└── docs/
    └── CLAUDE.md          # Loaded when editing docs/**
```

**Use for**: Directory-specific coding standards, local patterns, module documentation.

This is lazy-loaded context - sub-agents get relevant context without bloating main prompt.

### Master-Clone vs Custom Subagent

Two philosophies for delegation:

**Custom Subagents** (explicit specialists):
```
Main Claude → task-runner agent → result
```
- Pros: Isolated context, specialized prompts, reusable
- Cons: Gatekeeper effect (main agent loses visibility)

**Master-Clone** (dynamic delegation):
```
Main Claude → Task(general-purpose) → result
```
- Pros: Main agent stays informed, flexible routing
- Cons: Less specialized, may need more guidance

**Recommendation**: Use custom agents for well-defined, repeated tasks. Use Task(general-purpose) for ad-hoc delegation where main context matters.

---

## Delegation Patterns

### The Sweet Spot

**Best use case**: Tasks that are **repetitive but require judgment**.

```
✅ Good fit:
   - Audit 70 skills (repetitive) checking versions against docs (judgment)
   - Update 50 files (repetitive) deciding what needs changing (judgment)
   - Research 10 frameworks (repetitive) evaluating trade-offs (judgment)

❌ Poor fit:
   - Simple find-replace (no judgment needed, use sed/grep)
   - Single complex task (not repetitive, do it yourself)
   - Tasks with cross-item dependencies (agents work independently)
```

### Core Prompt Template

This 5-step structure works consistently:

```markdown
For each [item]:
1. Read [source file/data]
2. Verify with [external check - npm view, API, docs]
3. Check [authoritative source]
4. Evaluate/score
5. FIX issues found ← Critical: gives agent authority to act
```

**Key elements:**
- **"FIX issues found"** - Without this, agents only report. With it, they take action.
- **Exact file paths** - Prevents ambiguity and wrong-file edits
- **Output format template** - Ensures consistent, parseable reports
- **Item list** - Explicit list of what to process

### Batch Sizing

| Batch Size | Use When |
|------------|----------|
| 3-5 items | Complex tasks (deep research, multi-step fixes) |
| 5-8 items | Standard tasks (audits, updates, validations) |
| 8-12 items | Simple tasks (version checks, format fixes) |

**Why not more?**
- Agent context fills up
- One failure doesn't ruin entire batch
- Easier to review smaller changesets

**Parallel agents**: Launch 2-4 agents simultaneously, each with their own batch.

### Workflow Pattern

```
┌─────────────────────────────────────────────────────────────┐
│  1. PLAN: Identify items, divide into batches               │
│     └─ "58 skills ÷ 10 per batch = 6 agents"                │
├─────────────────────────────────────────────────────────────┤
│  2. LAUNCH: Parallel Task tool calls with identical prompts │
│     └─ Same template, different item lists                  │
├─────────────────────────────────────────────────────────────┤
│  3. WAIT: Agents work in parallel                           │
│     └─ Read → Verify → Check → Edit → Report                │
├─────────────────────────────────────────────────────────────┤
│  4. REVIEW: Check agent reports and file changes            │
│     └─ git status, spot-check diffs                         │
├─────────────────────────────────────────────────────────────┤
│  5. COMMIT: Batch changes with meaningful changelog         │
│     └─ One commit per tier/category, not per agent          │
└─────────────────────────────────────────────────────────────┘
```

---

## Prompt Templates

### Audit/Validation Pattern

```markdown
Deep audit these [N] [items]. For each:

1. Read the [source file] from [path]
2. Verify [versions/data] with [command or API]
3. Check official [docs/source] for accuracy
4. Score 1-10 and note any issues
5. FIX issues found directly in the file

Items to audit:
- [item-1]
- [item-2]
- [item-3]

For each item, create a summary with:
- Score and status (PASS/NEEDS_UPDATE)
- Issues found
- Fixes applied
- Files modified

Working directory: [absolute path]
```

### Bulk Update Pattern

```markdown
Update these [N] [items] to [new standard/format]. For each:

1. Read the current file at [path pattern]
2. Identify what needs changing
3. Apply the update following this pattern:
   [show example of correct format]
4. Verify the change is valid
5. Report what was changed

Items to update:
- [item-1]
- [item-2]
- [item-3]

Output format:
| Item | Status | Changes Made |
|------|--------|--------------|

Working directory: [absolute path]
```

### Research/Comparison Pattern

```markdown
Research these [N] [options/frameworks/tools]. For each:

1. Check official documentation at [URL pattern or search]
2. Find current version and recent changes
3. Identify key features relevant to [use case]
4. Note any gotchas, limitations, or known issues
5. Rate suitability for [specific need] (1-10)

Options to research:
- [option-1]
- [option-2]
- [option-3]

Output format:
## [Option Name]
- **Version**: X.Y.Z
- **Key Features**: ...
- **Limitations**: ...
- **Suitability Score**: X/10
- **Recommendation**: ...
```

---

## Example Custom Sub-Agents

### Code Reviewer

```yaml
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

```yaml
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data Scientist

```yaml
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

Always ensure queries are efficient and cost-effective.
```

---

## Commit Strategy

**Agents don't commit** - they only edit files. This is by design:

| Agent Does | Human Does |
|------------|------------|
| Research & verify | Review changes |
| Edit files | Spot-check diffs |
| Score & report | git add/commit |
| Create summaries | Write changelog |

**Why?**
- Review before commit catches agent errors
- Batch multiple agents into meaningful commits
- Clean commit history (not 50 tiny commits)
- Human decides commit message/grouping

**Commit pattern:**
```bash
git add [files] && git commit -m "$(cat <<'EOF'
[type]([scope]): [summary]

[Batch 1 changes]
[Batch 2 changes]
[Batch 3 changes]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Error Handling

### When One Agent Fails

1. Check the error message
2. Decide: retry that batch OR skip and continue
3. Don't let one failure block the whole operation

### When Agent Makes Wrong Change

1. `git diff [file]` to see what changed
2. `git checkout -- [file]` to revert
3. Re-run with more specific instructions

### When Agents Conflict

Rare (agents work on different items), but if it happens:
1. Check which agent's change is correct
2. Manually resolve or re-run one agent

---

## Best Practices

1. **Start with Claude-generated agents**: Use `/agents` to generate initial config, then customize
2. **Design focused sub-agents**: Single, clear responsibility per agent
3. **Write detailed prompts**: Specific instructions, examples, constraints
4. **Don't give Bash unless needed**: Prevents approval spam (see "Avoiding Bash Approval Spam")
5. **Put critical instructions FIRST**: Instructions at top of prompt get followed, buried ones get ignored
6. **Remove contradictory instructions**: If you want Write tool, remove all bash examples
7. **Default to Sonnet model**: Quality matters more than cost savings (see Model Selection)
8. **Version control**: Check `.claude/agents/` into git for team sharing
9. **Use inherit for model sparingly**: Better to explicitly set model for predictable behavior

---

## Performance Considerations

| Consideration | Impact |
|---------------|--------|
| **Context efficiency** | Agents preserve main context, enabling longer sessions |
| **Latency** | Sub-agents start fresh, may add latency gathering context |
| **Thoroughness** | Explore agent's thoroughness levels trade speed for completeness |

---

## Quick Reference

```
Built-in agents:
  Explore  → Haiku, read-only, quick/medium/thorough
  Plan     → Sonnet, plan mode research
  General  → Sonnet, all tools, read/write

Custom agents:
  Project  → .claude/agents/*.md (highest priority)
  User     → ~/.claude/agents/*.md
  CLI      → --agents '{...}'

Config fields:
  name, description (required)
  tools, model, permissionMode, skills, hooks (optional)

Tool access principle:
  ⚠️ Don't give Bash unless agent needs CLI execution
  File creators: Read, Write, Edit, Glob, Grep (no Bash!)
  Script runners: Read, Write, Edit, Glob, Grep, Bash (only if needed)
  Research: Read, Grep, Glob, WebFetch, WebSearch

Model selection (quality-first):
  Default: sonnet (most agents - quality matters)
  Creative: opus (maximum quality)
  Scripts only: haiku (just running commands)
  ⚠️ Avoid Haiku for content generation - quality drops significantly

Instruction placement:
  ⛔ Critical instructions go FIRST (right after frontmatter)
  ⚠️ Instructions buried 300+ lines deep get ignored
  ✅ Remove contradictory instructions (pick one pattern)

Delegation:
  Batch size: 5-8 items per agent
  Parallel: 2-4 agents simultaneously
  Prompt: 5-step (read → verify → check → evaluate → FIX)

Orchestration:
  Enable: Add "Task" to agent's tools list
  Depth: Keep to 2 levels max
  Use: Multi-phase workflows, parallel specialists

Advanced:
  Background: Ctrl+B during agent execution
  Context: 130k+ and 90+ tool calls work fine for real work
  Hooks: PreToolUse, PostToolUse, Stop events

Resume agents:
  > Resume agent [agentId] and continue...
```

---

## References

### Official Documentation
- [Sub-Agents Documentation](https://code.claude.com/docs/en/sub-agents)
- [Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [Tools Documentation](https://code.claude.com/docs/en/tools)
- [Hooks Documentation](https://code.claude.com/docs/en/hooks)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)

### Community Resources
- [Awesome Claude Code Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - 100+ specialized agents
- [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts) - Internal prompt analysis
- [Claude Code Built-in Tools Reference](https://www.vtrivedy.com/posts/claudecode-tools-reference/) - Comprehensive tool guide
- [Claude Code Frameworks Guide (Dec 2025)](https://www.medianeth.dev/blog/claude-code-frameworks-subagents-2025) - Advanced patterns

---

**Last Updated**: 2026-01-14
