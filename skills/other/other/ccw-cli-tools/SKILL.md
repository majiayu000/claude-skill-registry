---
name: ccw-cli-tools
description: CLI tools execution specification (gemini/claude/codex/qwen/opencode) with unified prompt template, mode options, and auto-invoke triggers for code analysis and implementation tasks. Supports configurable CLI endpoints for analysis, write, and review modes.
version: 1.0.0
---

# CLI Tools - Unified Execution Framework

**Purpose**: Structured CLI tool usage with configuration-driven tool selection, unified prompt templates, and quality-gated execution.

**Configuration**: `~/.claude/cli-tools.json` (Global, always read at initialization)

## Initialization (Required First Step)

**Before any tool selection or recommendation**:

1. Check if configuration exists in memory:
   - If configuration is already in conversation memory → Use it directly
   - If NOT in memory → Read the configuration file:
     ```bash
     Read(file_path="~/.claude/cli-tools.json")
     ```

2. Parse the JSON to understand:
   - Available tools and their `enabled` status
   - Each tool's `primaryModel` and `secondaryModel`
   - Tags defined for tag-based routing
   - Tool types (builtin, cli-wrapper, api-endpoint)

3. Use configuration throughout the selection process

**Why**: Tools, models, and tags may change. Configuration file is the single source of truth.
**Optimization**: Reuse in-memory configuration to avoid redundant file reads.

## Process Flow

```
┌─ USER REQUEST
│
├─ STEP 1: Load Configuration
│  ├─ Check if configuration exists in conversation memory
│  └─ If NOT in memory → Read(file_path="~/.claude/cli-tools.json")
│
├─ STEP 2: Understand User Intent
│  ├─ Parse task type (analysis, implementation, security, etc.)
│  ├─ Extract required capabilities (tags)
│  └─ Identify scope (files, modules)
│
├─ STEP 3: Select Tool (based on config)
│  ├─ Explicit --tool specified?
│  │  YES → Validate in config → Use it
│  │  NO  → Match tags with enabled tools → Select best match
│  │       → No match → Use first enabled tool (default)
│  └─ Get primaryModel from config
│
├─ STEP 4: Build Prompt
│  └─ Use 6-field template: PURPOSE, TASK, MODE, CONTEXT, EXPECTED, CONSTRAINTS
│
├─ STEP 5: Select Rule Template
│  ├─ Determine rule from task type
│  └─ Pass via --rule parameter
│
├─ STEP 6: Execute CLI Command
│  └─ ccw cli -p "<PROMPT>" --tool <tool> --mode <mode> --rule <rule>
│
└─ STEP 7: Handle Results
   ├─ On success → Deliver output to user
   └─ On failure → Check secondaryModel or fallback tool
```

## Configuration Reference

### Configuration File Location

**Path**: `~/.claude/cli-tools.json` (Global configuration)

**IMPORTANT**: Check conversation memory first. Only read file if configuration is not in memory.

### Reading Configuration

**Priority**: Check conversation memory first

**Loading Options**:
- **Option 1** (Preferred): Use in-memory configuration if already loaded in conversation
- **Option 2** (Fallback): Read from file when not in memory

```bash
# Read configuration file
cat ~/.claude/cli-tools.json
```

The configuration defines all available tools with their enabled status, models, and tags.

### Configuration Structure

The JSON file contains a `tools` object where each tool has these fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `enabled` | boolean | Tool availability status | `true` or `false` |
| `primaryModel` | string | Default model for execution | `"gemini-2.5-pro"` |
| `secondaryModel` | string | Fallback model on primary failure | `"gemini-2.5-flash"` |
| `tags` | array | Capability tags for routing | `["分析", "Debug"]` |
| `type` | string | Tool type | `"builtin"`, `"cli-wrapper"`, `"api-endpoint"` |

### Expected Tools (Reference Only)

Typical tools found in configuration (actual availability determined by reading the file):

| Tool | Typical Type | Common Use |
|------|--------------|------------|
| `gemini` | builtin | Analysis, Debug (分析, Debug tags) |
| `qwen` | builtin | General coding |
| `codex` | builtin | Code review, implementation |
| `claude` | builtin | General tasks |
| `opencode` | builtin | Open-source model fallback |

**Note**: Tool availability, models, and tags may differ. Use in-memory configuration or read `~/.claude/cli-tools.json` if not cached.

### Configuration Fields

- **`enabled`**: Tool availability (boolean)
- **`primaryModel`**: Default model for execution
- **`secondaryModel`**: Fallback model on primary failure
- **`tags`**: Capability tags for routing (分析, Debug, implementation, etc.)
- **`type`**: Tool type (builtin, cli-wrapper, api-endpoint)

## Universal Prompt Template

**Structure**: Every CLI command follows this 6-field template

```bash
ccw cli -p "PURPOSE: [goal] + [why] + [success criteria] + [scope]
TASK: • [step 1: specific action] • [step 2: specific action] • [step 3: specific action]
MODE: [analysis|write|review]
CONTEXT: @[file patterns] | Memory: [session/tech/module context]
EXPECTED: [deliverable format] + [quality criteria] + [structure requirements]
CONSTRAINTS: [domain constraints]" --tool <tool-id> --mode <mode> --rule <template>
```

### Field Specifications

#### PURPOSE (Goal Definition)

**What**: Clear objective + motivation + success criteria + scope boundary

**Components**:
- What: Specific task goal
- Why: Business/technical motivation
- Success: Measurable success criteria
- Scope: Bounded context/files

**Example - Good**:
```
PURPOSE: Identify OWASP Top 10 vulnerabilities in auth module to pass security audit;
success = all critical/high issues documented with remediation;
scope = src/auth/** only
```

**Example - Bad**:
```
PURPOSE: Analyze code
```

#### TASK (Action Steps)

**What**: Specific, actionable steps with clear verbs and targets

**Format**: Bullet list with concrete actions

**Example - Good**:
```
TASK:
• Scan for SQL injection in query builders
• Check XSS in template rendering
• Verify CSRF token validation
```

**Example - Bad**:
```
TASK: Review code and find issues
```

#### MODE (Permission Level)

**Options**:
- **`analysis`** - Read-only, safe for auto-execution
- **`write`** - Create/Modify/Delete files, full operations
- **`review`** - Git-aware code review (codex only)

**Rules**:
- Always specify explicitly
- Default to `analysis` for read-only tasks
- Require explicit `--mode write` for file modifications
- Use `--mode review` with `--tool codex` for git-aware review

#### CONTEXT (File Scope + Memory)

**Format**: `CONTEXT: @[file patterns] | Memory: [memory context]`

**File Patterns**:
- `@**/*` - All files (default)
- `@src/**/*.ts` - Specific pattern
- `@../shared/**/*` - Parent/sibling (requires `--includeDirs`)

**Memory Context** (when building on previous work):
```
Memory: Building on auth refactoring (commit abc123), using JWT for sessions
Memory: Integration with auth module, shared error patterns from @shared/utils/errors.ts
```

#### EXPECTED (Output Specification)

**What**: Output format + quality criteria + structure requirements

**Example - Good**:
```
EXPECTED: Markdown report with:
severity levels (Critical/High/Medium/Low),
file:line references,
remediation code snippets,
priority ranking
```

**Example - Bad**:
```
EXPECTED: Report
```

#### CONSTRAINTS (Domain Boundaries)

**What**: Scope limits, special requirements, focus areas

**Example - Good**:
```
CONSTRAINTS: Focus on authentication | Ignore test files | No breaking changes
```

**Example - Bad**:
```
CONSTRAINTS: (missing or too vague)
```

## CLI Execution Modes

### MODE: analysis
- **Permission**: Read-only
- **Use For**: Code review, architecture analysis, pattern discovery, exploration
- **Safe**: Yes - can auto-execute
- **Default**: When not specified

### MODE: write
- **Permission**: Create/Modify/Delete files
- **Use For**: Feature implementation, bug fixes, documentation, code creation
- **Safe**: No - requires explicit `--mode write`
- **Requirements**: Must be explicitly requested by user

### MODE: review
- **Permission**: Read-only (git-aware review output)
- **Use For**: Code review of uncommitted changes, branch diffs, specific commits
- **Tool Support**: `codex` only (others treat as analysis)
- **Constraint**: Target flags (`--uncommitted`, `--base`, `--commit`) and prompt are mutually exclusive

## Command Structure

### Basic Command

```bash
ccw cli -p "<PROMPT>" --tool <tool-id> --mode <analysis|write|review>
```

### Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `--tool <tool>` | Tool from config | `--tool gemini` |
| `--mode <mode>` | **REQUIRED**: analysis/write/review | `--mode analysis` |
| `--model <model>` | Model override | `--model gemini-2.5-flash` |
| `--cd <path>` | Working directory | `--cd src/auth` |
| `--includeDirs <dirs>` | Additional directories | `--includeDirs ../shared,../types` |
| `--rule <template>` | Auto-load template | `--rule analysis-review-architecture` |
| `--resume [id]` | Resume session | `--resume` or `--resume <id>` |

### Advanced Directory Configuration

#### Working Directory (`--cd`)

When using `--cd`:
- `@**/*` = Files within working directory tree only
- Cannot reference parent/sibling without `--includeDirs`
- Reduces token usage by scoping context

#### Include Directories (`--includeDirs`)

**Two-step requirement for external files**:

1. Add `--includeDirs` parameter
2. Reference in CONTEXT with @ patterns

```bash
# Single directory
ccw cli -p "CONTEXT: @**/* @../shared/**/*" \
  --tool gemini --mode analysis \
  --cd src/auth --includeDirs ../shared

# Multiple directories
ccw cli -p "..." \
  --tool gemini --mode analysis \
  --cd src/auth --includeDirs ../shared,../types,../utils
```

### Session Resume

**When to Use**:
- Multi-round planning (analysis → planning → implementation)
- Multi-model collaboration (tool A → tool B on same topic)
- Topic continuity (building on previous findings)

**Usage**:

```bash
ccw cli -p "Continue analyzing" --tool <tool-id> --mode analysis --resume              # Resume last
ccw cli -p "Fix issues found" --tool <tool-id> --mode write --resume <id>              # Resume specific
ccw cli -p "Merge findings" --tool <tool-id> --mode analysis --resume <id1>,<id2>      # Merge sessions
```

## Available Rule Templates

### Template System

Use `--rule <template-name>` to auto-load protocol + template appended to prompt

### Universal Templates
- `universal-rigorous-style` - Precise tasks (default)
- `universal-creative-style` - Exploratory tasks

### Analysis Templates
- `analysis-trace-code-execution` - Execution tracing
- `analysis-diagnose-bug-root-cause` - Bug diagnosis
- `analysis-analyze-code-patterns` - Code patterns
- `analysis-analyze-technical-document` - Document analysis
- `analysis-review-architecture` - Architecture review
- `analysis-review-code-quality` - Code review
- `analysis-analyze-performance` - Performance analysis
- `analysis-assess-security-risks` - Security assessment

### Planning Templates
- `planning-plan-architecture-design` - Architecture design
- `planning-breakdown-task-steps` - Task breakdown
- `planning-design-component-spec` - Component design
- `planning-plan-migration-strategy` - Migration strategy

### Development Templates
- `development-implement-feature` - Feature implementation
- `development-refactor-codebase` - Code refactoring
- `development-generate-tests` - Test generation
- `development-implement-component-ui` - UI component
- `development-debug-runtime-issues` - Runtime debugging

## Task-Type Specific Examples

### Example 1: Security Analysis (Read-Only)

```bash
ccw cli -p "PURPOSE: Identify OWASP Top 10 vulnerabilities in authentication module to pass security audit; success = all critical/high issues documented with remediation
TASK: • Scan for injection flaws (SQL, command, LDAP) • Check authentication bypass vectors • Evaluate session management • Assess sensitive data exposure
MODE: analysis
CONTEXT: @src/auth/**/* @src/middleware/auth.ts | Memory: Using bcrypt for passwords, JWT for sessions
EXPECTED: Security report with: severity matrix, file:line references, CVE mappings where applicable, remediation code snippets prioritized by risk
CONSTRAINTS: Focus on authentication | Ignore test files
" --tool gemini --mode analysis --rule analysis-assess-security-risks --cd src/auth
```

### Example 2: Feature Implementation (Write Mode)

```bash
ccw cli -p "PURPOSE: Implement rate limiting for API endpoints to prevent abuse; must be configurable per-endpoint; backward compatible with existing clients
TASK: • Create rate limiter middleware with sliding window • Implement per-route configuration • Add Redis backend for distributed state • Include bypass for internal services
MODE: write
CONTEXT: @src/middleware/**/* @src/config/**/* | Memory: Using Express.js, Redis already configured, existing middleware pattern in auth.ts
EXPECTED: Production-ready code with: TypeScript types, unit tests, integration test, configuration example, migration guide
CONSTRAINTS: Follow existing middleware patterns | No breaking changes
" --tool gemini --mode write --rule development-implement-feature
```

### Example 3: Bug Root Cause Analysis

```bash
ccw cli -p "PURPOSE: Fix memory leak in WebSocket connection handler causing server OOM after 24h; root cause must be identified before any fix
TASK: • Trace connection lifecycle from open to close • Identify event listener accumulation • Check cleanup on disconnect • Verify garbage collection eligibility
MODE: analysis
CONTEXT: @src/websocket/**/* @src/services/connection-manager.ts | Memory: Using ws library, ~5000 concurrent connections in production
EXPECTED: Root cause analysis with: memory profile, leak source (file:line), fix recommendation with code, verification steps
CONSTRAINTS: Focus on resource cleanup
" --tool gemini --mode analysis --rule analysis-diagnose-bug-root-cause --cd src
```

### Example 4: Code Review (Codex Review Mode)

```bash
# Option 1: Custom focus (reviews uncommitted by default)
ccw cli -p "Focus on security vulnerabilities and error handling" --tool codex --mode review

# Option 2: Target flag only (no prompt with target flags)
ccw cli --tool codex --mode review --uncommitted
ccw cli --tool codex --mode review --base main
ccw cli --tool codex --mode review --commit abc123
```

## Tool Selection Strategy

### Selection Algorithm

**STEP 0 (REQUIRED)**: Load configuration (memory-first strategy)

```bash
# Check if configuration exists in conversation memory
# If YES → Use in-memory configuration
# If NO → Read(file_path="~/.claude/cli-tools.json")
```

Then proceed with selection:

1. **Parse task intent** → Extract required capabilities
2. **Load configuration** → Parse enabled tools with tags from JSON
3. **Match tags** → Filter tools supporting required capabilities
4. **Select tool** → Choose by priority (explicit > tag-match > default)
5. **Select model** → Use primaryModel, fallback to secondaryModel

### Selection Decision Tree

```
0. LOAD CONFIGURATION (memory-first)
   ├─ In memory? → Use it
   └─ Not in memory? → Read ~/.claude/cli-tools.json
   ↓
1. Explicit --tool specified?
   YES → Validate tool is enabled in config → Use it
   NO  → Proceed to tag-based selection
         ├─ Extract task tags (security, analysis, implementation, etc.)
         │  ├─ Find tools with matching tags
         │  │  ├─ Multiple matches? Use first enabled
         │  │  └─ Single match? Use it
         │  └─ No tag match? Use default tool
         │
         └─ Default: Use first enabled tool in config
```

### Common Tag Routing

**Note**: Match task type to tags defined in `~/.claude/cli-tools.json`

| Task Type | Common Tags to Match |
|-----------|---------------------|
| Security audit | `分析`, `analysis`, `security` |
| Bug diagnosis | `Debug`, `分析`, `analysis` |
| Implementation | `implementation`, (any enabled tool) |
| Testing | `testing`, (any enabled tool) |
| Refactoring | `refactoring`, (any enabled tool) |
| Documentation | `documentation`, (any enabled tool) |

**Selection Logic**: Find tools where `tags` array contains matching keywords, otherwise use first enabled tool.

### Fallback Chain

When primary tool fails (based on `~/.claude/cli-tools.json` configuration):

1. Check `secondaryModel` for same tool (use `secondaryModel` from config)
2. Try next enabled tool with matching tags (scan config for enabled tools)
3. Fall back to default enabled tool (first enabled tool in config)

**Example Fallback**:
```
Tool1: primaryModel fails
  ↓
Try Tool1: secondaryModel
  ↓ (if fails)
Try Tool2: primaryModel (next enabled with matching tags)
  ↓ (if fails)
Try default: first enabled tool
```

## Permission Framework

**Single-Use Authorization**: Each execution requires explicit user instruction. Previous authorization does NOT carry over.

**Mode Hierarchy**:
- `analysis`: Read-only, safe for auto-execution
- `write`: Create/Modify/Delete files - requires explicit `--mode write`
- `review`: Git-aware code review (codex only) - requires explicit `--mode review`
- **Exception**: User provides clear instructions like "modify", "create", "implement"

## Auto-Invoke Triggers

**Proactive CLI invocation** - Auto-invoke `ccw cli` when encountering these scenarios:

| Trigger | Suggested Rule | When |
|---------|----------------|------|
| **Self-repair fails** | `analysis-diagnose-bug-root-cause` | After 1+ failed fix attempts |
| **Ambiguous requirements** | `planning-breakdown-task-steps` | Task description lacks clarity |
| **Architecture decisions** | `planning-plan-architecture-design` | Complex feature needs design |
| **Pattern uncertainty** | `analysis-analyze-code-patterns` | Unsure of existing conventions |
| **Critical code paths** | `analysis-assess-security-risks` | Security/performance sensitive |

### Execution Principles for Auto-Invoke

- **Default mode**: `--mode analysis` (read-only, safe)
- **No confirmation needed**: Invoke proactively when triggers match
- **Wait for results**: Complete analysis before next action
- **Tool selection**: Use context-appropriate tool or fallback chain
- **Rule flexibility**: Suggested rules are guidelines, adapt as needed

## Best Practices

### Core Principles

- **Configuration-driven** - All tool selection from `cli-tools.json`
- **Tag-based routing** - Match task requirements to tool capabilities
- **Use tools early and often** - Tools are faster and more thorough than manual analysis
- **Unified CLI** - Always use `ccw cli -p` for consistent parameter handling
- **Default to analysis** - Omit `--mode` for read-only, explicitly use `--mode write` for modifications
- **Use `--rule` for templates** - Auto-loads protocol + template appended to prompt
- **Write protection** - Require EXPLICIT `--mode write` for file operations

### Workflow Principles

- **Use unified interface** - Always `ccw cli -p` format
- **Always include template** - Use `--rule <template-name>` to load templates
- **Be specific** - Clear PURPOSE, TASK, EXPECTED fields
- **Include constraints** - File patterns, scope in CONSTRAINTS
- **Leverage memory context** - When building on previous work
- **Discover patterns first** - Use rg/MCP before CLI execution
- **Default to full context** - Use `@**/*` unless specific files needed

### Planning Checklist

- [ ] **Purpose defined** - Clear goal and intent
- [ ] **Mode selected** - `--mode analysis|write|review`
- [ ] **Context gathered** - File references + memory (default `@**/*`)
- [ ] **Directory navigation** - `--cd` and/or `--includeDirs` if needed
- [ ] **Tool selected** - Explicit `--tool` or tag-based auto-selection
- [ ] **Rule template** - `--rule <template-name>` loads template
- [ ] **Constraints** - Domain constraints in CONSTRAINTS field

## Integration with CLAUDE.md Instructions

**From global CLAUDE.md**:
- Always use `run_in_background: false` for Task tool agent calls
- Default: Use Bash `run_in_background: true` for CLI calls
- After CLI call: Stop output immediately, wait for hook callback
- Wait for results: MUST wait for CLI analysis before taking write actions
- Value every call: Never waste analysis results, aggregate before proposing solutions

**From cli-tools-usage.md**:
- Strict cli-tools.json configuration adherence
- Configuration-driven tool selection
- Template system with --rule auto-loading
- Permission framework with single-use authorization
- Auto-invoke triggers for common failure scenarios
