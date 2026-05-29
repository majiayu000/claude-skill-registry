---
name: pal-mcp-expert
description: Expert guidance for using the Pal MCP Server (zen-pal-nas). This skill should be used when working with multi-model AI orchestration, tool workflows (chat, thinkdeep, planner, consensus, debug, codereview, precommit, clink), configuration troubleshooting, or optimizing model selection strategies. Activates automatically when user mentions Pal MCP, zen-pal-nas, or specific tool names.
---

# Pal MCP Server Expert Guide

Master guide for the Pal MCP Server - a Provider Abstraction Layer that orchestrates multiple AI models (Gemini, OpenAI, Grok, Azure, Ollama, custom) through a unified MCP interface. Formerly known as "Zen MCP".

## Core Concept

**PAL = Provider Abstraction Layer**

Think of it as "Claude Code for Claude Code" - super-glue that connects your AI CLI (Claude Code, Codex CLI, Gemini CLI, Cursor) to multiple AI models for enhanced collaboration. Claude stays in full control, but gains perspectives from the best AI model for each subtask.

**Key Principle:** You craft the prompts. PAL enables Claude to engage other models only when needed, maintaining context across all interactions.

## When to Use This Skill

Activate this skill when:

- Orchestrating multiple AI models in workflows
- Using specific PAL tools (chat, thinkdeep, planner, consensus, codereview, precommit, debug, clink)
- Troubleshooting zen-pal-nas configuration issues
- Optimizing model selection for complex tasks
- Implementing context revival after Claude resets
- Setting up CLI subagents for isolated workloads
- Configuring environment variables or API keys
- Managing tool timeouts or performance issues

**Auto-activation triggers:** "pal", "zen-pal-nas", tool names (chat, thinkdeep, consensus, clink), continuation_id references, multi-model workflows

## Revolutionary Features

### 1. Context Revival After Claude Resets

**The Problem:** When Claude's context resets/compacts, traditional conversations lose all history.

**PAL's Solution:** Other models (O3, Gemini, Flash) maintain complete conversation history and can "remind" Claude of everything discussed.

**Pattern:**
```
Session 1: "Design RAG system with gemini pro"
[Claude resets]
Session 2: "Continue our RAG discussion with o3"
→ O3 receives full history, reminds Claude, conversation continues
```

**Implementation:** **Always reuse continuation_id** from previous tool responses.

### 2. CLI Subagents (clink tool)

Spawn isolated CLI instances without polluting main context:

```
"clink with cli_name='codex' role='codereviewer' to audit auth module"
→ Codex explores full codebase in fresh context
→ Returns only final audit report
→ Main session context stays clean
```

**Supported CLIs:** claude, codex, gemini  
**Roles:** default, codereviewer, planner

### 3. MCP 25K Token Limit Bypass

Automatically works around MCP's 25,000 token limit for arbitrarily large prompts/responses to models like Gemini.

**No configuration needed** - PAL handles transparently.

### 4. Vision Support

All tools support vision-capable models for analyzing images, diagrams, screenshots:

```
"Debug this error with gemini pro using the stack trace screenshot"
"Analyze system architecture diagram for bottlenecks"
```

**Limits:** Gemini/O3 (20MB), Claude via OpenRouter (5MB), Custom (40MB max)

## Tool Ecosystem

### Core Tools (Always Enabled)

#### chat
Multi-model conversation with code generation.
- **Use for:** Quick questions, implementation, brainstorming
- **Code generation:** GPT-5-Pro/Gemini Pro generate complete implementations
- **Example:** `"Chat with gemini pro about API design best practices"`

#### thinkdeep
Extended reasoning with systematic investigation.
- **Use for:** Complex debugging, architecture decisions, edge case analysis
- **Multi-step:** Confidence tracking (exploring → certain)
- **Example:** `"Use thinkdeep with max thinking mode to investigate this race condition"`

#### planner
Break down complex projects with revision support.
- **Use for:** Feature roadmaps, refactoring strategies, migration planning
- **Features:** Branching, step revision, adaptive planning
- **Example:** `"Plan the database migration with planner"`

#### consensus
Multi-model expert opinions with stance steering.
- **Use for:** Architecture decisions, controversial choices, multi-angle validation
- **Stance options:** "for", "against", "neutral"
- **Example:** `"Use consensus with gpt-5-pro (for) and gemini-pro (against) to decide: microservices or monolith?"`

#### clink
Connect external AI CLIs as subagents.
- **Use for:** Heavy tasks without context pollution (code reviews, security audits)
- **Context isolation:** Subagent explores, returns results only
- **Example:** `"clink with cli_name='gemini' role='planner' to draft rollout plan"`

### Advanced Workflow Tools

#### codereview (enabled)
Systematic code review with expert validation.
- **Types:** full, security, performance, quick
- **Validation:** external (2 steps) or internal (1 step)

#### precommit (enabled)
Git change validation before commits.
- **Analyzes:** Diffs, security issues, test coverage
- **Max steps:** 3 (external) or 1 (internal)

#### debug (enabled)
Root cause analysis with hypothesis testing.
- **Confidence-based:** exploring → certain
- **Valid outcome:** "No bug found" is acceptable

### Specialized Tools (Disabled by Default)

Enable via `DISABLED_TOOLS` environment variable:

- **analyze**: Comprehensive codebase analysis (architecture, performance, security, quality)
- **refactor**: Code smell detection and improvement opportunities
- **testgen**: Generate comprehensive test suites with edge cases
- **tracer**: Execution flow or dependency mapping
- **secaudit**: Security audit (OWASP, compliance, infrastructure)
- **docgen**: Automated documentation generation

**Default disabled:** `"analyze,refactor,testgen,secaudit,docgen,tracer"`

### Utility Tools

- **listmodels**: Display available models with intelligence scores
- **version**: Server version and configuration
- **challenge**: Critical analysis to prevent reflexive agreement
- **apilookup**: Search current API/SDK documentation (requires web search)

## Critical Parameters

### continuation_id (MOST IMPORTANT)

**Always reuse the last continuation_id received** - this maintains context across:
- Claude resets/compaction
- Different tools in same workflow
- Multi-session conversations

**Pattern:**
```
Step 1: Use chat → returns continuation_id: "abc123"
Step 2: Use codereview with continuation_id="abc123"
→ Seamless context handoff
```

### File Paths

**Always use absolute paths:**
- ✅ `/home/user/project/src/auth.ts`
- ❌ `src/auth.ts` (may fail)

### Model Selection

**Auto mode (recommended):**
```
DEFAULT_MODEL=auto  # Intelligent selection per task
```

**Per-request override:**
```
"Use chat with gpt-5-pro to implement auth"  # Overrides default
```

### Temperature & Thinking Modes

**Temperature (0-1):**
- 0: Deterministic
- 0.5: Balanced
- 1: Creative

**Thinking Modes:**
- minimal: Fast lightweight
- medium: Standard
- high: Deep thinking
- max: Maximum reasoning depth

### Working Directory

Required for code generation - where `pal_generated.code` is saved:
```
working_directory_absolute_path: "/absolute/path/to/project"
```

## Configuration

### Installation Status
- **Active as:** zen-pal-nas (in Claude Desktop)
- **Docker container:** zen-mcp-stack (Synology NAS 192.168.86.97)
- **Local repository:** W:\pal-mcp-server
- **Current version:** v9.8.2

### Environment Variables (Key Ones)

```bash
# Model Provider (at least one required)
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key

# Model Selection
DEFAULT_MODEL=auto  # Recommended

# Tool Management
DISABLED_TOOLS="analyze,refactor,testgen,secaudit,docgen,tracer"

# Conversation Settings
CONVERSATION_TIMEOUT_HOURS=5
MAX_CONVERSATION_TURNS=20

# Model Restrictions (optional)
GOOGLE_ALLOWED_MODELS="flash,pro"
OPENAI_ALLOWED_MODELS="gpt-5.1-codex-mini,o4-mini"

# Multi-Client Conflicts
FORCE_ENV_OVERRIDE=true  # .env takes precedence

# Logging
LOG_LEVEL=DEBUG  # or INFO, WARNING, ERROR
```

### Timeout Configuration

**Recommended:** 20 minutes (1200 seconds)

**Why:** Multi-step workflows (thinkdeep, consensus, codereview) can take 5-20 minutes.

**Claude Code (.mcp.json):**
```json
{
  "tool_timeout_sec": 1200
}
```

**Claude Desktop (settings.json):**
```json
{
  "timeout": 1200000  // milliseconds
}
```

## Workflow Patterns

### Multi-Model Code Review → Planning → Implementation

```
1. "Use codereview with gemini pro to analyze auth/"
   → continuation_id: "auth-refactor"
   
2. "Use planner with continuation_id='auth-refactor' to plan refactoring"
   → Plan based on review findings
   
3. "Use chat with gpt-5-pro and continuation_id='auth-refactor' to implement step 1"
   → Implementation with full context
   
4. "Use precommit with continuation_id='auth-refactor' to validate"
   → Final validation
```

### Collaborative Debates

```
"Use consensus with models:
  [{model: 'gpt-5-pro', stance: 'for'},
   {model: 'gemini-pro', stance: 'against'},
   {model: 'o3', stance: 'neutral'}]
to decide architecture"
→ continuation_id: "arch-decision"

"Continue with clink gemini - implement recommended architecture with continuation_id='arch-decision'"
→ Gemini receives full debate, implements immediately
```

### CLI Subagent Isolation

```
Main session: "Design API interface"
Subagent: "clink codex codereviewer - audit database performance"
→ Codex analyzes in isolation, returns report only
→ Main context stays focused on design
```

## Intelligence Scoring & Auto Mode

When `DEFAULT_MODEL=auto`, Claude selects best model per subtask:

**Score Ranges:**
- **18-20**: Highest reasoning (GPT-5 Pro, Gemini 3.0 Pro, O3)
- **15-17**: Strong (GPT-5.1-Codex, Gemini Pro)
- **10-14**: Efficient (Flash, GPT-4o-mini)
- **5-9**: Fast lightweight

**Example:**
```
"Debug complex race condition" → Auto selects O3 (score 19)
"Format JSON" → Auto selects Flash (score 12)
```

## Troubleshooting

### Tool Not Triggering
1. Check DISABLED_TOOLS configuration
2. Verify tool name spelling
3. Try explicit call: `"Use pal chat with..."`

### API Key Errors
1. Verify key validity
2. Check FORCE_ENV_OVERRIDE if using multiple clients
3. Restart MCP client after config changes

### Timeout Errors
1. Increase tool_timeout_sec to 1200
2. Check network connectivity
3. Verify model availability

### Context Loss
1. **Always reuse continuation_id** - this is the key
2. Check CONVERSATION_TIMEOUT_HOURS (default: 5)
3. Verify conversation thread hasn't expired

## Reference Documentation

For comprehensive details, reference:
- `references/tool-catalog.md` - Complete tool parameter documentation
- `references/advanced-features.md` - Context revival, vision support, web search, workflows
- `references/installation-config.md` - Setup, API keys, environment variables, Docker integration

**Usage Pattern:**
1. Read tool catalog to understand parameters
2. Use advanced features for complex workflows
3. Check installation guide for configuration issues
