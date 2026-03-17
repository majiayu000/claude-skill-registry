---
name: codex-cli
description: Integrate OpenAI Codex CLI into Claude Code for AI collaboration, code generation, and automated development. Use when working with OpenAI models (GPT-5.2, GPT-5.1-Codex-Max, o3, o4-mini), code refactoring, git workflows, or needing full automation with permission bypass.
---

# OpenAI Codex CLI Integration

Integrates OpenAI's Codex CLI into Claude Code, enabling seamless AI collaboration between Claude and Codex for enhanced development workflows.

**Last Updated**: December 2025 (GPT-5.2 Release)

## When to Use

- Working with OpenAI models (GPT-5.2, GPT-5.1-Codex-Max, o3, o4-mini)
- Code generation and refactoring with latest models
- Git-aware workflows and PR reviews
- Full automation with permission bypass
- Reasoning-first development (o3 models, GPT-5.2 with xhigh reasoning)
- Multimodal tasks (code + images)
- Sandboxed execution environments
- Long-context tasks (400K tokens with GPT-5.2)

## Quick Start

### 1. Install Codex CLI

```bash
# Check current installation
codex --version

# Install/Update globally via NPM
npm install -g @openai/codex

# Or use Homebrew (macOS/Linux)
brew install openai/tap/codex-cli
```

### 2. Setup Authentication

#### Option A: ChatGPT Plus/Pro (Recommended)
```bash
# Login with ChatGPT account
codex login
# Opens browser for OAuth authentication
# Includes GPT-5-Codex access with subscription
```

#### Option B: API Key
```bash
# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Or create config file
mkdir -p ~/.codex
echo 'api_key = "your-api-key-here"' > ~/.codex/config.toml
```

### 3. Basic Usage

```bash
# Direct execution (like gemini -p)
codex exec "Analyze this codebase and suggest improvements"

# Full automation (BYPASS ALL APPROVALS)
codex exec --dangerously-bypass-approvals-and-sandbox "Refactor authentication module"

# Safe automation (sandboxed)
codex exec --full-auto "Generate tests for all functions"

# Interactive mode
codex "Let's work on improving this code"

# With specific model (December 2025)
codex exec -m gpt-5.2 "Complex task with latest model"
codex exec -m gpt-5.1-codex-max "Best for agentic coding (default)"
codex exec -m o3 "Deep reasoning task"
codex exec -m o4-mini "Quick code generation"
```

## Full Automation Mode - MAXIMUM POWER

**`--dangerously-bypass-approvals-and-sandbox`** - Complete automation, zero friction:

### ✅ When to Use Bypass Mode

```bash
# Trusted, repeatable workflows
codex exec --dangerously-bypass-approvals-and-sandbox "Add JSDoc comments to all ./src functions"

# Automated testing workflows
codex exec --dangerously-bypass-approvals-and-sandbox "Run tests and auto-fix all failures"

# Bulk operations
codex exec --dangerously-bypass-approvals-and-sandbox "Convert all .js files to TypeScript"

# CI/CD pipelines (externally sandboxed)
codex exec --dangerously-bypass-approvals-and-sandbox "Deploy to staging environment"
```

### ⚠️ Safer Automation Options

```bash
# --full-auto: Sandboxed with workspace write access
codex exec --full-auto "Refactor module safely"

# Custom approval + sandbox
codex exec -a never -s workspace-write "Controlled automation"

# On-failure approval (runs until error)
codex exec -a on-failure "Try operations, escalate on error"
```

### Approval Policies

```bash
# -a never: Full automation (no approvals)
codex exec -a never "Complete workflow automation"

# -a on-request: Model decides when to ask
codex exec -a on-request "Intelligent approval requests"

# -a on-failure: Only ask if command fails
codex exec -a on-failure "Run until failure, then ask"

# -a untrusted: Only run trusted commands (default)
codex exec -a untrusted "Safe, limited automation"
```

### Sandbox Modes

```bash
# -s read-only: Cannot modify files
codex exec -s read-only "Analysis only, no changes"

# -s workspace-write: Can modify workspace
codex exec -s workspace-write "Safe file modifications"

# -s danger-full-access: Full system access
codex exec -s danger-full-access "Complete control (use carefully)"
```

## Available Models (December 2025)

### GPT-5.2 Series (NEW - December 11, 2025)
```bash
# GPT-5.2 Thinking - Latest frontier model
# 400K context, 128K output, knowledge cutoff Aug 31, 2025
# Pricing: $1.75/1M input, $14/1M output (90% cached discount)
codex exec -m gpt-5.2 "Complex multi-step task with deep reasoning"

# GPT-5.2 Instant - Speed optimized for routine queries
codex exec -m gpt-5.2-chat-latest "Fast information seeking and writing"

# GPT-5.2 Pro - Maximum accuracy (Responses API only)
# Pricing: $21/1M input, $168/1M output
# Supports reasoning.effort: medium, high, xhigh
codex exec -m gpt-5.2-pro "Critical high-accuracy tasks"
```

### GPT-5.1 Codex Series (Recommended for Coding)
```bash
# GPT-5.1-Codex-Max - DEFAULT for Codex CLI
# Best for agentic coding with native compaction support
codex exec -m gpt-5.1-codex-max "Complex development workflows"

# GPT-5.1-Codex - Optimized for long-running agentic tasks
codex exec -m gpt-5.1-codex "Extended coding sessions"

# GPT-5.1-Codex-Mini - Cost-efficient coding
codex exec -m gpt-5.1-codex-mini "Quick code tasks"
```

### Legacy GPT-5 Series
```bash
# GPT-5 - General model (use GPT-5.2 for latest)
codex exec -m gpt-5 "General tasks"

# GPT-5-Codex - Previous coding model
codex exec -m gpt-5-codex "Code generation"
```

### o-Series (Reasoning Models)
```bash
# o3 - Smartest reasoning model
codex exec -m o3 "Complex architectural decisions"

# o4-mini - Efficient reasoning
codex exec -m o4-mini "Quick reasoning tasks"
```

### New GPT-5.2 Features
```bash
# Extended reasoning with xhigh effort (GPT-5.2 Pro/Thinking)
codex exec -m gpt-5.2-pro --reasoning-effort xhigh "Maximum accuracy task"

# Context compaction for long sessions
codex exec -m gpt-5.2 --compact "Long document analysis"

# Concise reasoning summaries
codex exec -m gpt-5.2 --concise-reasoning "Explain this code"
```

## Claude + Codex Collaboration Patterns

**Claude orchestrates, Codex executes** - The Think-Act-Observe Loop:

### Structured Workflows

```bash
#!/bin/bash
# Claude directs Codex for complete feature development

# THINK: Claude analyzes requirements
echo "Goal: Add user profile caching"

# ACT: Codex researches best practices (with web search)
codex exec --search --dangerously-bypass-approvals-and-sandbox \
  "Research Redis caching patterns and create implementation plan" \
  > plan.md

# OBSERVE: Claude reviews the plan
cat plan.md

# ACT: Codex implements (full automation)
codex exec --dangerously-bypass-approvals-and-sandbox --json \
  "Implement the caching system according to @plan.md" \
  > implementation.json

# OBSERVE: Claude verifies
jq '.changes[]' implementation.json

# ACT: Codex tests
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Generate and run comprehensive tests"

# Loop continues...
```

### JSON Output for AI Parsing

```bash
# Get structured output for Claude to parse
codex exec --json "List all exported functions in ./src" > functions.json

# Claude processes reliably
for func in $(jq -r '.functions[].name' functions.json); do
  echo "Processing: $func"
  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Add input validation to $func function"
done
```

### Sequential Task Decomposition

```bash
#!/bin/bash
# Claude breaks down complex goal into safe atomic steps

echo "=== Feature: Add OAuth2 Authentication ==="

# Step 1: Research (safe, read-only)
codex exec --search --full-auto "Research OAuth2 best practices 2025" > research.md

# Step 2: Plan (Claude reviews)
codex exec "Create detailed OAuth2 implementation plan based on @research.md"
read -p "Review plan. Continue? [y/N] " -r

# Step 3: Install dependencies
codex exec --dangerously-bypass-approvals-and-sandbox "Install OAuth2 packages"

# Step 4: Generate code
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Generate OAuth2 auth module according to plan"

# Step 5: Tests
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Generate comprehensive OAuth2 tests"

# Step 6: Verify
codex exec --dangerously-bypass-approvals-and-sandbox "Run all tests and fix failures"
```

## Advanced Features

### Web Search Integration

```bash
# Enable web search for research
codex exec --search --dangerously-bypass-approvals-and-sandbox \
  "Research latest React 19 features and create migration guide"

# Research-driven development
codex exec --search --full-auto \
  "Find best practices for microservices and implement API gateway"
```

### Multimodal (Code + Images)

```bash
# Attach design screenshots
codex exec -i design.png --dangerously-bypass-approvals-and-sandbox \
  "Implement this UI design in React"

# Multiple images
codex exec -i mockup1.png -i mockup2.png --full-auto \
  "Compare these designs and implement the better approach"
```

### Git-Aware Workflows

```bash
# Apply Codex changes as git patch
codex apply
# or
codex a

# Work on git branch
git checkout -b feature/new-auth
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Implement authentication with clean commits"

# Codex respects .gitignore and git history
```

### Resume Sessions

```bash
# Resume last session
codex exec resume --last

# Pick from previous sessions
codex resume
```

### Configuration Profiles

```bash
# Create profile in ~/.codex/config.toml
[profiles.auto-dev]
model = "gpt-5.1-codex"
ask_for_approval = "never"
sandbox = "workspace-write"
search = true

# Use profile
codex exec -p auto-dev "Develop new feature automatically"
```

### MCP Server Integration

```bash
# Run as MCP server
codex mcp

# Manage MCP servers (experimental)
codex mcp list
codex mcp add <server-name>
```

## Core Workflows

### Automated Code Generation

```bash
#!/bin/bash
# Complete automation for code generation

generate_api() {
  local spec="$1"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    --json \
    --search \
    "Read API specification @$spec and generate:
    1. Data models with validation
    2. API endpoints with OpenAPI docs
    3. Database migrations
    4. Comprehensive tests
    5. Error handling middleware
    6. Authentication middleware
    7. Rate limiting
    8. API documentation"
}

# Usage
generate_api "./specs/user-api.yaml"
```

### Automated Refactoring

```bash
#!/bin/bash
# Safe, automated refactoring workflow

refactor_module() {
  local module="$1"

  # Backup first
  git stash push -m "pre-refactor-$(date +%s)"

  # Full automation with git safety
  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Refactor $module:
    1. Analyze current code structure
    2. Identify improvements
    3. Apply modern patterns
    4. Add comprehensive tests
    5. Run all tests
    6. Fix any test failures
    7. Update documentation
    8. Create clean git commits"

  if [ $? -eq 0 ]; then
    echo "Refactoring complete!"
  else
    git stash pop
    echo "Refactoring failed, restored backup"
  fi
}

# Usage
refactor_module "./src/auth"
```

### Test Generation & Fixing

```bash
#!/bin/bash
# Automated test generation and fixing

automate_testing() {
  local target="$1"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Complete testing workflow for $target:
    1. Analyze code coverage gaps
    2. Generate comprehensive unit tests
    3. Generate integration tests
    4. Generate end-to-end tests
    5. Run all tests
    6. Fix any failing tests
    7. Achieve 100% coverage
    8. Generate test report"
}

# Usage
automate_testing "./src"
```

### CI/CD Integration

```yaml
# GitHub Actions with Codex
name: Codex Automation
on: [push, pull_request]

jobs:
  codex-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install Codex CLI
        run: npm install -g @openai/codex

      - name: Run Codex Analysis
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex exec --dangerously-bypass-approvals-and-sandbox \
            --json \
            "Analyze code changes, run tests, fix issues, generate report" \
            > codex-report.json

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: codex-analysis
          path: codex-report.json
```

## Configuration

### Config File (~/.codex/config.toml)

```toml
# Default model (December 2025)
model = "gpt-5.1-codex-max"  # Best for agentic coding

# Approval policy
ask_for_approval = "on-request"  # or "never", "on-failure", "untrusted"

# Sandbox mode
sandbox = "workspace-write"  # or "read-only", "danger-full-access"

# Enable web search
search = true

# Additional writable directories
add_dirs = ["./docs", "./tests"]

# Feature flags
[features]
web_search = true
multimodal = true
mcp = true

# Profiles for different workflows
[profiles.safe]
ask_for_approval = "untrusted"
sandbox = "read-only"

[profiles.auto]
ask_for_approval = "never"
sandbox = "workspace-write"
search = true

[profiles.danger]
ask_for_approval = "never"
sandbox = "danger-full-access"
search = true

# NEW: GPT-5.2 optimized profiles
[profiles.gpt52]
model = "gpt-5.2"
ask_for_approval = "never"
sandbox = "workspace-write"
search = true

[profiles.gpt52-pro]
model = "gpt-5.2-pro"
reasoning_effort = "xhigh"
ask_for_approval = "on-request"
sandbox = "workspace-write"

[profiles.long-context]
model = "gpt-5.2"
ask_for_approval = "never"
sandbox = "workspace-write"
compact = true  # Enable context compaction
```

### Environment Variables

```bash
# Authentication
export OPENAI_API_KEY="your-key"

# Default model (December 2025)
export CODEX_MODEL="gpt-5.1-codex-max"  # For agentic coding
# export CODEX_MODEL="gpt-5.2"          # For general tasks with 400K context
# export CODEX_MODEL="gpt-5.2-pro"      # For maximum accuracy

# Default config path
export CODEX_CONFIG_PATH="~/.codex/config.toml"

# GPT-5.2 specific options
export CODEX_REASONING_EFFORT="high"  # medium, high, xhigh
```

## Best Practices

### Security with Bypass Mode

When using `--dangerously-bypass-approvals-and-sandbox`:

1. **Use in Controlled Environments**
   - CI/CD with external sandboxing
   - Docker containers
   - Disposable development environments

2. **Always Have Backups**
   ```bash
   git stash push -m "pre-codex-$(date +%s)"
   codex exec --dangerously-bypass-approvals-and-sandbox "task"
   ```

3. **Use Git for Safety**
   - Work on feature branches
   - Review diffs before pushing
   - Use `codex apply` to review changes

4. **Limit Scope**
   ```bash
   codex exec --dangerously-bypass-approvals-and-sandbox \
     -C ./specific/directory \
     "Only affect this directory"
   ```

### Model Selection Strategy (December 2025)

```bash
# Quick tasks: o4-mini or gpt-5.1-codex-mini
codex exec -m o4-mini "Format code with Prettier"
codex exec -m gpt-5.1-codex-mini "Quick code fixes"

# Standard development: gpt-5.1-codex-max (DEFAULT)
codex exec -m gpt-5.1-codex-max "Implement user authentication"

# Long-context tasks: gpt-5.2 (400K context)
codex exec -m gpt-5.2 "Analyze entire codebase"

# Complex reasoning: o3 or gpt-5.2-pro with xhigh
codex exec -m o3 "Design scalable microservices architecture"
codex exec -m gpt-5.2-pro --reasoning-effort xhigh "Critical architecture decisions"

# Speed-optimized: gpt-5.2-chat-latest (Instant)
codex exec -m gpt-5.2-chat-latest "Quick information retrieval"

# Maximum accuracy: gpt-5.2-pro
codex exec -m gpt-5.2-pro "High-stakes production code"
```

### Performance Optimization

```bash
# Use JSON for faster parsing
codex exec --json "task" | jq .

# Skip git checks if not needed
codex exec --skip-git-repo-check "task"

# Specify working directory
codex exec -C ./project "task"

# Use profiles to avoid repetitive flags
codex exec -p auto-dev "task"
```

## Troubleshooting

### Common Issues

**Authentication Failed**
```bash
codex logout
codex login
```

**Model Not Available**
```bash
# Check available models (December 2025)
codex exec -m gpt-5.2 "test" || echo "GPT-5.2 not available"

# Fall back to stable coding model
codex exec -m gpt-5.1-codex-max "task"

# Or use previous generation
codex exec -m gpt-5.1-codex "task"
```

**Sandbox Errors**
```bash
# Try different sandbox mode
codex exec -s danger-full-access "task"

# Or bypass entirely (if safe)
codex exec --dangerously-bypass-approvals-and-sandbox "task"
```

## Related Skills

- `codex-auth`: Authentication and API key management
- `codex-chat`: Interactive REPL workflows
- `codex-tools`: Tool execution and file operations
- `codex-review`: Code review and git workflows
- `codex-git`: Git-aware development patterns

## Updates

```bash
# Update Codex CLI
npm update -g @openai/codex

# Check version
codex --version

# Check for new models
codex exec "What models are available?"
```

---

**Created for Claude Code** - Full automation for AI-to-AI collaboration
