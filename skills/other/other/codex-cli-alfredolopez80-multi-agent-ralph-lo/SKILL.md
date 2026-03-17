---
# VERSION: 2.89.0
name: codex-cli
description: "OpenAI Codex CLI orchestration for AI-assisted development using gpt-5.3-codex model family. Model variants: gpt-5.3-codex (medium), gpt-5.3-codex-high, gpt-5.3-codex-xhigh. Capabilities: code generation, refactoring, automated editing, parallel task execution, session management, code review, architecture analysis, and MCP integration. Actions: analyze, implement, review, fix, refactor with Codex. Keywords: Codex CLI, gpt-5.3-codex, codex exec, code generation, refactoring, parallel execution, session resume, code review, second opinion, independent review, architecture validation, Context7 MCP. Use when: delegating complex code tasks to Codex, running multi-agent workflows, executing automated reviews, implementing features with AI assistance, resuming previous sessions, querying OpenAI documentation. Triggers: 'use codex', 'codex exec', 'run with codex', 'codex resume', 'implement with codex', 'review with codex', 'codex docs'."
---

# Codex CLI Integration Skill (v2.37)

## v2.89 Key Changes (GPT-5.3-CODEX FAMILY)

- **Model family**: `gpt-5.3-codex` with three reasoning tiers
- **Reasoning tiers**: medium (default), high, xhigh (maximum)
- **Profiles**: Pre-configured profiles for each reasoning level
- **Backward compatible**: Still supports model override via `-m` flag

**Reasoning Tier Selection**:

| Tier | Model | Use Case | Command |
|------|-------|----------|---------|
| `medium` | `gpt-5.3-codex` | Default, fast code tasks | `codex exec "prompt"` |
| `high` | `gpt-5.3-codex-high` | Complex analysis, security | `codex exec --profile high "prompt"` |
| `xhigh` | `gpt-5.3-codex-xhigh` | Architecture, critical review | `codex exec --profile xhigh "prompt"` |

**ultrathink** - Take a deep breath. We're not here to write code. We're here to make a dent in the universe.

## The Vision
Codex orchestration should feel inevitable: minimal risk, maximum clarity.

## Your Work, Step by Step
1. **Select strategy**: Model, sandbox, and reasoning effort.
2. **Prepare context**: Inject the smallest, sharpest prompt.
3. **Execute**: Run Codex with clear constraints.
4. **Validate output**: Check for correctness and scope compliance.
5. **Summarize**: Report findings and next steps.

## Ultrathink Principles in Practice
- **Think Different**: Choose the safest path to insight.
- **Obsess Over Details**: Respect sandbox boundaries.
- **Plan Like Da Vinci**: Shape the prompt before execution.
- **Craft, Don't Code**: Keep commands precise.
- **Iterate Relentlessly**: Re-run with refined prompts.
- **Simplify Ruthlessly**: Reduce noise and scope.

# Codex CLI Integration Skill (v2.37)

This skill enables Claude to orchestrate OpenAI's Codex CLI (v0.79+) with the **gpt-5.3-codex** model for code generation, review, analysis, and automated editing. Includes Context7 MCP integration for documentation access.

## When to Use This Skill

**Ideal Use Cases:**
- Complex code analysis requiring deep understanding
- Large-scale refactoring across multiple files
- Automated code generation with safety controls
- Second opinion / cross-validation on code implementations
- Parallel processing of independent code tasks
- Session-based iterative development workflows

## Quick Start

### Prerequisites

Verify Codex CLI installation:
```bash
codex --version  # Should show v0.50.0+
```

Authentication (first time):
```bash
codex  # Interactive login via ChatGPT account
# Or: export CODEX_API_KEY=sk-...
```

### Model Selection (v2.89)

**Model family**: `gpt-5.3-codex` with reasoning tiers

| Model | Reasoning | Use Case |
|-------|-----------|----------|
| `gpt-5.3-codex` | medium | Default, fast code tasks (recommended) |
| `gpt-5.3-codex-high` | high | Complex analysis, security review |
| `gpt-5.3-codex-xhigh` | xhigh | Architecture design, critical decisions |
| `o3` | - | Highest reasoning capability |
| `o4-mini` | - | Fast, simple tasks |

**Usage by tier**:
```bash
# Medium (default) - fast iteration
codex exec "refactor authentication module"

# High - complex analysis
codex exec -m gpt-5.3-codex-high "security audit of payment flow"

# XHigh - architectural decisions
codex exec -m gpt-5.3-codex-xhigh "design microservices architecture"
```

### Sandbox Modes

| Mode | Permission | Use Case |
|------|------------|----------|
| `read-only` | Read files only (default) | Analysis, review |
| `workspace-write` | Read/write workspace | Code editing, refactoring |
| `danger-full-access` | Full system access | Install deps, network |

## Core Commands

### Basic Execution

```bash
# Read-only analysis (default)
codex exec -m gpt-5.3-codex "analyze src/auth for security issues"

# Code editing (workspace-write)
codex exec -m gpt-5.3-codex --full-auto "fix bug in login.py"

# With reasoning effort
codex exec -m gpt-5.3-codex --config model_reasoning_effort=high "complex analysis"

# Skip git check (non-git directories)
codex exec --skip-git-repo-check "analyze code"
```

### Suppress Thinking Tokens

Add `2>/dev/null` to suppress stderr (thinking tokens):
```bash
codex exec -m gpt-5.3-codex "review code" 2>/dev/null
```

### Session Resume

```bash
# Resume last session (stdin for prompt - required due to CLI bug)
echo "continue with fixes" | codex exec resume --last 2>/dev/null

# Resume with full-auto
echo "apply fixes" | codex exec resume --last --full-auto 2>/dev/null

# Resume specific session
echo "follow-up" | codex exec resume SESSION_ID
```

**Important**: Resume inherits model, reasoning, and sandbox from original session.

### JSON Output

```bash
# JSON Lines output
codex exec --json -m gpt-5.3-codex "analyze code" > output.jsonl

# Extract session ID
SID=$(grep -o '"thread_id":"[^"]*"' output.jsonl | head -1 | cut -d'"' -f4)

# Extract agent message
grep '"type":"agent_message"' output.jsonl | jq -r '.item.text'
```

## Orchestration Patterns

### Pattern 1: Context Pre-injection

Claude collects information first, injects into prompt for faster execution:

```bash
# Collect errors
ERRORS=$(npm run lint 2>&1 | grep error)

# Inject context
codex exec -m gpt-5.3-codex --full-auto "Fix these errors:
$ERRORS

Files: src/auth/login.ts, src/utils/token.ts
Constraint: Only modify listed files."
```

### Pattern 2: Session Reuse

Related tasks reuse sessions for context preservation:

```bash
# First: analyze
codex exec -m gpt-5.3-codex "analyze src/auth for issues"

# Continue: fix (reuses context)
echo "fix the issues you found" | codex exec resume --last --full-auto
```

**When to reuse:**
- Analyze → Fix (knows findings)
- Implement → Test (knows implementation)
- Test → Fix (knows failures)

### Pattern 3: Parallel Execution

Independent tasks run simultaneously:

```bash
# Parallel analysis
codex exec --json -m gpt-5.3-codex "analyze auth" > auth.jsonl 2>&1 &
codex exec --json -m gpt-5.3-codex "analyze api" > api.jsonl 2>&1 &
wait

# Parallel fixes with resume
AUTH_SID=$(grep -o '"thread_id":"[^"]*"' auth.jsonl | head -1 | cut -d'"' -f4)
echo "fix issues" | codex exec resume $AUTH_SID --full-auto &
# ...
wait
```

**Parallelizable:**
- Different directories/modules
- Different analysis dimensions (security/performance/quality)
- Read-only operations

**Must serialize:**
- Writing same files
- Dependent on prior results

## Interactive Workflow

Before running Codex tasks, confirm with user:

1. **Model selection**: `gpt-5.3-codex` or `gpt-5.2`?
2. **Reasoning effort**: `low`, `medium`, or `high`?
3. **Sandbox mode**: Based on task requirements

### Decision Matrix

| Task Type | Sandbox | Flags |
|-----------|---------|-------|
| Review/analysis | `read-only` | `--sandbox read-only 2>/dev/null` |
| Apply local edits | `workspace-write` | `--full-auto 2>/dev/null` |
| Network/deps | `danger-full-access` | `--sandbox danger-full-access --full-auto` |
| Resume session | Inherited | `echo "prompt" \| codex exec resume --last` |

## Code Review Workflow

### Independent Review

Use Codex as second opinion on Claude's work:

```bash
codex exec -m gpt-5.3-codex --sandbox read-only "Review src/payment/processor.py for:
1. Race conditions in transaction processing
2. Proper error handling and rollback
3. Security issues with payment data
4. Edge cases that could cause data loss
Provide specific line numbers and severity ratings."
```

### Comprehensive Review

```bash
# Security audit
codex exec -m gpt-5.3-codex --sandbox read-only --config model_reasoning_effort=high \
  "Perform security audit of src/auth. Check for:
  - Authentication/authorization issues
  - Input validation vulnerabilities
  - Cryptographic weaknesses
  - Sensitive data exposure"

# Performance review
codex exec -m gpt-5.3-codex --sandbox read-only \
  "Analyze src/database for performance:
  - N+1 query problems
  - Missing indexes
  - Blocking operations"
```

### Pull Request Review

```bash
codex exec -m gpt-5.3-codex --sandbox read-only \
  "Run 'git diff main...HEAD' to see changes.
  Review for:
  1. Breaking changes
  2. Performance implications
  3. Test coverage
  4. Security concerns
  Provide feedback by file with severity levels."
```

## Prompt Design

### Structure Formula

```
[Verb] + [Scope] + [Requirements] + [Output Format] + [Constraints]
```

### Verb Selection

| Read-only | Write |
|-----------|-------|
| analyze, review, find, explain | fix, refactor, implement, add |

### Examples

**Bad vs Good:**
```bash
# Bad: vague
codex exec "review code"

# Good: specific
codex exec -m gpt-5.3-codex --sandbox read-only \
  "Review src/auth for SQL injection, XSS.
  Output: markdown with severity levels.
  Format: file:line, description, fix suggestion."
```

### Parallel Prompt Consistency

```bash
# Consistent structure for aggregation
FORMAT="Output JSON: {category, items: [{file, line, description}]}"

codex exec -m gpt-5.3-codex "review security. $FORMAT" &
codex exec -m gpt-5.3-codex "review performance. $FORMAT" &
codex exec -m gpt-5.3-codex "review quality. $FORMAT" &
wait
```

## Claude-Codex Engineering Loop

### Dual-AI Workflow

1. **Claude plans** → Architecture, requirements
2. **Codex validates plan** → Check logic, edge cases
3. **Claude implements** → Write code with tools
4. **Codex reviews** → Bug detection, security
5. **Claude fixes** → Apply corrections
6. **Codex re-validates** → Confirm quality
7. **Repeat** until standards met

### Implementation

```bash
# Phase 2: Codex validates Claude's plan
echo "Review this implementation plan for issues:
[Claude's plan here]

Check for:
- Logic errors
- Missing edge cases
- Architecture flaws
- Security concerns" | codex exec -m gpt-5.3-codex --sandbox read-only

# Phase 4: Codex reviews Claude's code
codex exec -m gpt-5.3-codex --sandbox read-only \
  "Review implementation in src/feature for:
  - Bugs
  - Performance issues
  - Best practices
  - Security vulnerabilities"
```

## Error Handling

1. **Non-zero exit**: Stop and report, ask for direction
2. **Warnings**: Summarize and ask how to proceed
3. **High-impact flags**: Ask permission before `--full-auto`, `--sandbox danger-full-access`

## Post-Task Follow-up

After every Codex command:
1. Summarize outcome
2. Confirm next steps with user
3. Offer: "Resume session with 'codex resume' for continued analysis"

## Configuration

### Profile Setup (~/.codex/config.toml)

```toml
model = "gpt-5.3-codex"
model_reasoning_effort = "medium"

# Reasoning tier profiles
[profiles.medium]
model = "gpt-5.3-codex"
model_reasoning_effort = "medium"

[profiles.high]
model = "gpt-5.3-codex-high"
model_reasoning_effort = "high"

[profiles.xhigh]
model = "gpt-5.3-codex-xhigh"
model_reasoning_effort = "high"

# Task-specific profiles
[profiles.review]
model = "gpt-5.3-codex-high"
model_reasoning_effort = "high"
sandbox_mode = "read-only"

[profiles.implement]
model = "gpt-5.3-codex"
model_reasoning_effort = "medium"
sandbox_mode = "workspace-write"

[profiles.architect]
model = "gpt-5.3-codex-xhigh"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
```

Usage:
```bash
# Use reasoning tier profiles
codex exec --profile medium "quick fix"
codex exec --profile high "security audit"
codex exec --profile xhigh "architecture review"

# Use task-specific profiles
codex exec --profile review "analyze code"
codex exec --profile implement "add feature"
codex exec --profile architect "design system"
```

## Quick Reference

| Use Case | Command |
|----------|---------|
| Medium (default) | `codex exec "prompt" 2>/dev/null` |
| High reasoning | `codex exec -m gpt-5.3-codex-high "prompt" 2>/dev/null` |
| XHigh reasoning | `codex exec -m gpt-5.3-codex-xhigh "prompt" 2>/dev/null` |
| Edit files | `codex exec --full-auto "prompt" 2>/dev/null` |
| High effort | `--config model_reasoning_effort=high` |
| Resume last | `echo "prompt" \| codex exec resume --last` |
| JSON output | `codex exec --json "prompt" > out.jsonl` |
| Specific dir | `codex exec -C /path "prompt"` |
| Non-git dir | `--skip-git-repo-check` |
| Profile: medium | `codex exec --profile medium "prompt"` |
| Profile: high | `codex exec --profile high "prompt"` |
| Profile: xhigh | `codex exec --profile xhigh "prompt"` |
| Profile: review | `codex exec --profile review "prompt"` |
| Profile: architect | `codex exec --profile architect "prompt"` |

## Documentation Access via Context7 MCP

Both Claude and Codex have Context7 MCP configured. Use it to access OpenAI documentation:

### Available Documentation Libraries

| Library ID | Content | Snippets |
|------------|---------|----------|
| `/websites/developers_openai_codex` | Codex CLI docs | 614 |
| `/websites/platform_openai` | OpenAI API docs | 9,418 |
| `/openai/openai-python` | Python SDK | 429 |
| `/openai/openai-node` | Node.js SDK | 437 |

### Query Documentation Before Execution

```yaml
# Before running complex Codex commands, verify syntax
mcp__context7__query-docs:
  libraryId: "/websites/developers_openai_codex"
  query: "exec sandbox modes full-auto workspace-write"

# On errors, look up solutions
mcp__context7__query-docs:
  libraryId: "/websites/developers_openai_codex"
  query: "error troubleshooting session resume"
```

### MCP Server Configuration Reference

```toml
# ~/.codex/config.toml - Codex MCP configuration

# STDIO server (local command)
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp@latest"]

# Remote HTTP server
[mcp_servers.remote]
url = "https://example.com/mcp"
bearer_token_env_var = "API_TOKEN"

# With environment variables
[mcp_servers.server.env]
API_KEY = "value"
```

### Verify MCP Servers

```bash
# List configured MCP servers
codex mcp list

# Add new MCP server
codex mcp add context7 -- npx -y @upstash/context7-mcp

# Test MCP server
npx @modelcontextprotocol/inspector codex mcp-server
```

## See Also

- `/openai-docs` - OpenAI documentation access skill
- `references/cli_reference.md` - Complete CLI arguments
- `references/prompt_patterns.md` - Advanced prompt design
- `references/parallel_execution.md` - Parallel orchestration details
