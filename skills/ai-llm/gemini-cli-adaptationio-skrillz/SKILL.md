---
name: gemini-cli
description: Integrate Gemini AI CLI into Claude Code for AI collaboration, code analysis, and tool execution. Use when working with Gemini AI, Google AI, multimodal tasks, or needing advanced AI capabilities.
---

# Gemini CLI Integration

Integrates Google's Gemini CLI into Claude Code, enabling seamless AI collaboration between Claude and Gemini for enhanced capabilities.

## When to Use

- Working with Google AI/Gemini models
- Need multimodal capabilities (text + images)
- Complex reasoning with ReAct architecture
- Web search and fetching capabilities
- MCP server integration
- Code analysis and generation with Gemini
- Comparing AI model outputs

## Quick Start

### 1. Install Gemini CLI

```bash
# Check Node.js version (requires 18+, recommend 20+)
node --version

# Install globally via NPM
npm install -g @google/gemini-cli

# Or use without installation
npx @google/gemini-cli
```

### 2. Setup Authentication

#### Option A: Google OAuth (Recommended - Free)
```bash
# Start Gemini and follow OAuth flow
gemini
# Will open browser for Google authentication
```

#### Option B: API Key
```bash
# Get key from https://aistudio.google.com/
export GEMINI_API_KEY="your-api-key-here"

# Or create ~/.gemini/.env file
echo 'GEMINI_API_KEY="your-api-key-here"' > ~/.gemini/.env
```

### 3. Basic Usage

```bash
# Quick prompt (manual approval required)
gemini -p "Explain this code: $(cat main.py)"

# YOLO mode (auto-approve all actions - RECOMMENDED for automation)
gemini --yolo -p "Analyze and optimize this codebase"

# Interactive session
gemini -i "Let's analyze my project"

# Include specific directories with YOLO
gemini --include-directories ./src,./tests --yolo -p "Review and improve this codebase"

# Use specific model with auto-execution
gemini -m gemini-2.5-flash --yolo -p "Generate tests for all functions"
```

## YOLO Mode - Use with Caution

**--yolo** automatically approves all actions. **USE SPARINGLY** - it's powerful but risky.

### ✅ Safe YOLO Operations

```bash
# Read-only analysis (safe)
gemini --yolo -p "Analyze code quality in @./src and generate report"

# Documentation generation (low risk)
gemini --yolo -p "Add JSDoc comments to all functions in ./src"

# Small, atomic operations (verifiable)
gemini --yolo -p "Fix ESLint errors in @./utils.js"

# Idempotent operations (safe to retry)
gemini --yolo -p "Format all JavaScript files with Prettier"
```

### ⚠️ Use YOLO with Safeguards

```bash
# Always create backups first
git stash push -m "pre-yolo-backup"
gemini --yolo -p "Refactor authentication module"

# Use checkpointing for rollback
gemini --checkpointing --yolo -p "Major code modernization"

# Combine with dry-run preview
gemini --dry-run -p "Database migration"  # Review first
gemini --yolo -p "Execute reviewed migration"  # Then automate
```

### ❌ NEVER Use YOLO For

- **Complex, multi-step workflows** - Break into sequential steps instead
- **Production system modifications** - Always manual review
- **Database operations** - Require human verification
- **Security configurations** - Too critical for automation
- **File deletions** - Risk of data loss
- **Unknown/untested operations** - Test manually first

### Better Alternative: Iterative Workflows

Instead of large YOLO tasks, use Claude-orchestrated loops:

```bash
# ❌ RISKY: One giant YOLO task
gemini --yolo -p "Complete Express.js to Fastify migration"

# ✅ SAFE: Claude-guided sequential steps
gemini -p "Step 1: Analyze Express dependencies"  # Review
gemini --yolo -p "Step 2: Install Fastify packages"  # Safe
gemini -p "Step 3: Convert first route"  # Review
gemini --yolo -p "Step 4: Run tests"  # Safe
# Continue iteratively...
```

## Claude + Gemini Collaboration Patterns

**AI-to-AI Integration:** Claude and Gemini work best together with structured, iterative workflows.

### The Think-Act-Observe Loop

Claude orchestrates, Gemini executes - the most powerful pattern for AI collaboration:

```bash
# 1. Claude THINKS: Analyze the goal
# "I need to refactor the auth module. First, understand the structure."

# 2. Claude directs Gemini to ACT:
gemini -p "List all functions and their signatures in @./src/auth.js" > auth_analysis.txt

# 3. Claude OBSERVES the results
cat auth_analysis.txt
# Claude reviews and decides next step

# 4. Claude directs specific, atomic action:
gemini --yolo -p "Add try-catch error handling to the 'login' function in @./src/auth.js"

# 5. Claude verifies:
gemini --yolo -p "Run tests in tests/auth.test.js and report results"

# 6. Claude iterates based on test results
```

### Structured Output for AI Parsing

**Use `--output-format json` for machine-readable results:**

```bash
# Get structured data Claude can parse
gemini --output-format json -p "List all Python files in ./src" > files.json

# Claude can now reliably process the JSON
cat files.json | jq '.files[]'

# Structured analysis
gemini --output-format json -p "Analyze security issues in @./src/auth.js" > security_report.json

# Claude parses specific fields
jq '.vulnerabilities[] | .severity' security_report.json
```

### Safe Automation with Dry-Run

**Preview operations before execution:**

```bash
# Claude previews the plan first
gemini --dry-run -p "Refactor the authentication system"
# Output shows planned tool calls without executing

# After Claude reviews and approves:
gemini --yolo -p "Execute the reviewed refactoring plan"
```

### Sequential Task Decomposition

**Break complex tasks into atomic, verifiable steps:**

```bash
#!/bin/bash
# Claude-orchestrated workflow

# BAD: Too complex, unpredictable
# gemini --yolo -p "Create a complete Express.js API with authentication"

# GOOD: Sequential, verifiable steps
echo "Step 1: Initialize project"
gemini --yolo -p "Initialize Node.js project and create server.js"

echo "Step 2: Install dependencies"
gemini --yolo -p "Install express, cors, and body-parser"

echo "Step 3: Basic server"
gemini --yolo -p "Create basic Express server in server.js with hello world route"

echo "Step 4: Add authentication (review this step)"
gemini -p "Add JWT authentication middleware to server.js"
# Claude reviews before proceeding

echo "Step 5: Verify"
gemini --yolo -p "Run tests and report results"
```

### Tool Discovery and Schema

**Claude learns available tools:**

```bash
# Discover what tools Gemini has
gemini tools list

# Get detailed tool schema
gemini tools describe fileSystem
gemini tools describe shell
gemini tools describe google_web_search

# Claude can then construct precise tool calls
```

### Error Handling Patterns

**Robust automation with proper error handling:**

```bash
#!/bin/bash
set -e  # Exit on error

# Claude-managed error recovery
if ! gemini --yolo -p "Run test suite"; then
  echo "Tests failed. Analyzing..."
  gemini -p "Analyze test failures and suggest fixes" > fixes.txt
  cat fixes.txt
  # Claude decides whether to apply fixes
fi
```

### Context Management

**Efficient context for large projects:**

```bash
# Let Claude select relevant context
gemini --include-directories ./src/auth,./tests/auth \
       -p "Focus only on authentication module"

# Use @ syntax for precise file references
gemini -p "Compare @./src/auth-old.js with @./src/auth-new.js"

# Web context
gemini -p "Compare my implementation @./src/api.js with @https://example.com/best-practices"
```

### Checkpoint and Restore

**Safe experimentation with rollback:**

```bash
# Claude creates checkpoint before risky operations
gemini --checkpointing --yolo -p "Major refactoring of core module"

# If something goes wrong:
gemini checkpoint list
gemini checkpoint restore <checkpoint-id>
```

## Core Workflows

### Code Analysis Workflow

```bash
# Analyze entire project (auto-execute)
gemini --include-directories . \
       --exclude-directories node_modules,.git \
       --yolo -p "Analyze this codebase and suggest improvements"

# Code review with auto-fixes
gemini --yolo -p "Review and fix security issues: @./src/auth.js"

# Generate tests automatically
gemini --yolo -p "Generate comprehensive tests for: @./src/utils.js"

# Manual review (when unsure)
gemini -p "Explain the architecture of this complex module: @./src/core.js"
```

### Documentation Generation

```bash
# Generate README (auto-create files)
gemini --include-directories . --yolo -p "Generate a comprehensive README.md for this project"

# API documentation (auto-generate)
gemini --yolo -p "Generate complete API documentation for: @./src/api/"

# Code comments (bulk operation)
gemini --yolo -p "Add detailed JSDoc comments to all functions in: @./src/"

# Manual review for complex docs
gemini -p "Explain the documentation strategy for: @./complex_algorithm.py"
```

### Multimodal Analysis

```bash
# Analyze images (read-only, safe for YOLO)
gemini --yolo -p "Describe this architecture diagram: @./docs/architecture.png"

# Compare designs (analysis only)
gemini --yolo -p "Compare these UI designs and suggest improvements: @./design1.png @./design2.png"

# Extract and format text
gemini --yolo -p "Extract and format the text from: @./screenshot.png"
```

### Web Research

```bash
# Research with web search (auto-execute)
gemini --yolo -p "Research best practices for React performance optimization and create summary"

# Fetch and analyze (read-only)
gemini --yolo -p "Analyze this documentation: @https://docs.example.com/api"

# Compare implementations (analysis)
gemini --yolo -p "Compare my implementation with: @https://github.com/example/repo and suggest improvements"
```

## Advanced Features

### Interactive Commands

```bash
# In interactive mode:
/help              # Show all commands
/tools             # List available tools
/mcp               # Show MCP servers
/compress          # Summarize conversation
/copy              # Copy last response
/clear             # Clear context
/checkpoint        # Save project state
/restore           # Restore checkpoint
/ide install       # Setup VS Code
/ide enable        # Connect to VS Code
```

### Tool Execution

```bash
# Auto-approve tool calls (careful!)
gemini --yolo -p "Create a Python script that processes all CSV files"

# Sandbox mode (safer)
gemini --sandbox -p "Set up a new React project"

# Manual approval (default)
gemini -p "Organize my project files"
```

### MCP Server Integration

```bash
# List MCP servers
gemini mcp list

# Add MCP server
gemini mcp add

# Remove MCP server
gemini mcp remove <name>

# Use with MCP tools
gemini -p "Use the database MCP server to query user data"
```

### Checkpointing

```bash
# Enable checkpointing
gemini --checkpointing -p "Refactor this entire module"

# List checkpoints
gemini checkpoint list

# Restore checkpoint
gemini checkpoint restore <id>
```

## Configuration

### Settings File (~/.gemini/settings.json)

```json
{
  "model": "gemini-2.5-pro",
  "defaultFlags": {
    "checkpointing": true,
    "includeDirectories": ["./src", "./tests"],
    "excludeDirectories": ["node_modules", ".git", "dist"]
  },
  "tools": {
    "shell": {
      "enabled": false,
      "requireConfirmation": true
    },
    "fileSystem": {
      "enabled": true,
      "allowedPaths": ["./"]
    },
    "web": {
      "enabled": true,
      "allowedDomains": ["github.com", "docs.google.com"]
    }
  }
}
```

### Environment Variables

```bash
# Authentication
export GEMINI_API_KEY="your-key"

# Vertex AI (Enterprise)
export GOOGLE_CLOUD_PROJECT="your-project"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Model selection
export GEMINI_MODEL="gemini-2.5-pro"

# Default directories
export GEMINI_INCLUDE_DIRS="./src,./lib"
export GEMINI_EXCLUDE_DIRS="node_modules,.git"
```

## Integration Patterns

### Claude + Gemini Collaboration

```bash
# Use Claude for planning, Gemini for execution
echo "Claude, create a plan for refactoring auth module"
# ... get plan from Claude ...

gemini -p "Execute this refactoring plan: [paste plan]"
```

### Parallel Analysis

```bash
# Get different perspectives
echo "Analyze security of auth.js" | tee \
  >(claude-cli) \
  >(gemini -p -)
```

### Model Comparison

```bash
# Compare outputs
PROMPT="Generate unit tests for utils.js"
echo "Claude:" && claude-cli "$PROMPT"
echo "Gemini:" && gemini -p "$PROMPT"
```

## Best Practices

### Security

1. **API Key Management**
   - Never commit API keys
   - Use environment variables
   - Rotate keys regularly

2. **Tool Execution**
   - Avoid `--yolo` for untrusted prompts
   - Use `--sandbox` for experiments
   - Review tool calls before approval

3. **MCP Server Trust**
   - Only trust known servers
   - Use include/exclude tool lists
   - Set appropriate timeouts

### Performance

1. **Model Selection**
   - Use `gemini-2.5-flash` for quick tasks
   - Use `gemini-2.5-pro` for complex reasoning
   - Consider token limits (1M context window)

2. **Directory Management**
   - Exclude unnecessary directories
   - Use specific includes for large projects
   - Leverage checkpointing for long tasks

3. **Rate Limiting**
   - OAuth: 60 req/min, 1000 req/day
   - API Key: Varies by tier
   - Implement retry logic

### Workflow Optimization

1. **Batch Operations**
   ```bash
   # Process multiple files efficiently
   gemini -p "Analyze and improve: @./src/*.js"
   ```

2. **Context Preservation**
   ```bash
   # Use interactive mode for related tasks
   gemini -i "Let's refactor the auth system"
   ```

3. **Output Formatting**
   ```bash
   # Get JSON output for parsing
   gemini --json -p "List all functions in: @./utils.js"
   ```

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   ```bash
   # Clear cached credentials
   rm -rf ~/.gemini/auth
   # Re-authenticate
   gemini
   ```

2. **Rate Limiting**
   ```bash
   # Check usage
   gemini usage
   # Switch to different auth method if needed
   ```

3. **Tool Execution Errors**
   ```bash
   # Check tool availability
   gemini -i
   /tools
   # Verify permissions
   ```

4. **MCP Server Issues**
   ```bash
   # Check server status
   gemini mcp status
   # Restart server
   gemini mcp restart <name>
   ```

## Examples

### Complete Project Analysis (Automated)

```bash
#!/bin/bash
# Comprehensive project analysis with auto-execution

gemini --include-directories . \
       --exclude-directories node_modules,.git,dist \
       --checkpointing --yolo \
       -p "Perform comprehensive analysis and create reports:
1. Code quality assessment with fixes
2. Security vulnerability scan and patches
3. Performance optimization suggestions
4. Generate missing tests
5. Create complete documentation
6. Update dependencies safely
7. Implement CI/CD pipeline"
```

### Automated Documentation Suite

```bash
#!/bin/bash
# Generate complete documentation suite (fully automated)

gemini --yolo -p "Generate complete documentation ecosystem:
1. README.md with badges and quick start
2. API.md with OpenAPI specification
3. CONTRIBUTING.md with dev workflow
4. CHANGELOG.md with version history
5. JSDoc comments for all functions
6. Architecture diagrams in Mermaid
7. Test documentation and coverage reports
8. Deployment and operations guide"
```

### Framework Migration (Auto-Pilot)

```bash
#!/bin/bash
# Automated framework migration

gemini --checkpointing --yolo \
       -p "Fully automated Express.js to Fastify migration:
1. Analyze current Express structure
2. Create detailed migration plan  
3. Update package.json dependencies
4. Convert all routes and middleware
5. Update error handling patterns
6. Migrate and update all tests
7. Create docker configuration
8. Verify functionality with test suite
9. Generate migration report"
```

### Daily Development Automation

```bash
#!/bin/bash
# Daily automated development tasks

gemini --yolo -p "Execute daily development workflow:
1. Pull latest changes safely
2. Update dependencies to latest stable
3. Run full test suite and fix failures  
4. Update documentation for any changes
5. Optimize code performance
6. Run security audit and fix issues
7. Generate daily progress report
8. Commit and push changes with proper messages"
```

## Related Skills

- `gemini-auth`: Authentication management
- `gemini-chat`: Interactive chat sessions
- `gemini-tools`: Tool execution workflows
- `gemini-mcp`: MCP server management
- `gemini-code`: Code-specific operations

## Updates

This skill tracks Gemini CLI updates. Check for new features:

```bash
# Update Gemini CLI
npm update -g @google/gemini-cli

# Check version
gemini --version

# View changelog
gemini changelog
```