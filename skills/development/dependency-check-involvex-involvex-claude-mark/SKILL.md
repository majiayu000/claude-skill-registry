---
name: dependency-check
description: Check for required dependencies (Chrome DevTools MCP, OpenRouter API) before running commands that need them. Use at the start of /implement, /review, /validate-ui commands to provide helpful setup guidance.
allowed-tools: Bash, AskUserQuestion
---

# Dependency Check Skill

This skill provides standardized dependency checking for frontend plugin commands that require external tools and services.

## When to Use This Skill

Claude should invoke this skill at the **start** of commands that require:

1. **Chrome DevTools MCP** - For automated UI verification, screenshot capture, DOM inspection
   - Commands: `/implement` (UI validation), `/validate-ui`, browser-debugger skill

2. **OpenRouter API Key** - For multi-model orchestration with external AI models
   - Commands: `/implement` (multi-model code review), `/review`

## Dependency Check Protocol

### Phase 1: Check Chrome DevTools MCP

**When to check:** Before any command that needs browser automation (screenshots, UI testing, DOM inspection)

**How to check:**

```bash
# Check if chrome-devtools MCP tools are available
# Try to list pages - if MCP is available, this will work
mcp__chrome-devtools__list_pages 2>/dev/null
```

**If MCP is NOT available, show this message:**

```markdown
## Chrome DevTools MCP Not Available

For automated UI verification (screenshots, DOM inspection, visual regression testing),
this command requires the **chrome-devtools-mcp** server.

### Why You Need It
- Capture implementation screenshots for design comparison
- Inspect DOM structure and computed CSS values
- Run automated UI tests in real browser
- Debug responsive layout issues
- Monitor console errors and network requests

### Easy Installation (Recommended)

Install `claudeup` - a CLI tool for managing Claude Code plugins and MCP servers:

\`\`\`bash
npm install -g claudeup@latest
claudeup mcp add chrome-devtools
\`\`\`

### Manual Installation

Add to your `.claude.json` or `.claude/settings.json`:

\`\`\`json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
\`\`\`

### Continue Without It?

You can continue, but:
- UI validation will be **skipped** (no design fidelity checks)
- Browser testing will be **unavailable**
- Manual verification will be required for UI changes

Do you want to continue without Chrome DevTools MCP?
```

**Use AskUserQuestion:**
```
Chrome DevTools MCP is not available. What would you like to do?

Options:
- "Continue without UI verification" - Skip automated UI checks, proceed with implementation
- "Cancel and install MCP first" - I'll install the MCP and restart
```

### Phase 2: Check OpenRouter API Key

**When to check:** Before any command that uses external AI models via Claudish

**How to check:**

```bash
# Check if OPENROUTER_API_KEY is set
if [[ -z "${OPENROUTER_API_KEY}" ]]; then
  echo "OPENROUTER_API_KEY not set"
else
  echo "OPENROUTER_API_KEY available"
fi

# Also check if Claudish is available
npx claudish --version 2>/dev/null || echo "Claudish not installed"
```

**If OpenRouter API key is NOT set, show this message:**

```markdown
## OpenRouter API Key Not Configured

For multi-model AI orchestration (parallel code reviews, multi-expert validation),
this command uses external AI models via OpenRouter.

### Why You Need It
- Run multiple AI models in parallel for 3-5x faster reviews
- Get diverse perspectives from different AI experts (Grok, Gemini, GPT-5, DeepSeek)
- Consensus analysis highlights issues flagged by multiple models
- Catch more bugs through AI diversity

### Getting Started with OpenRouter

1. **Sign up** at [https://openrouter.ai](https://openrouter.ai)
2. **Get your API key** from the dashboard
3. **Set the environment variable:**

\`\`\`bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export OPENROUTER_API_KEY="your-api-key-here"
\`\`\`

### Cost Information

OpenRouter is **affordable** and even has **free models**:

| Model | Cost | Notes |
|-------|------|-------|
| openrouter/polaris-alpha | **FREE** | Good for testing |
| x-ai/grok-code-fast-1 | ~$0.10/review | Fast coding specialist |
| google/gemini-2.5-flash | ~$0.05/review | Fast and affordable |
| deepseek/deepseek-chat | ~$0.05/review | Reasoning specialist |

Typical code review session: **$0.20 - $0.80** for 3-4 external models

### Easy Setup (Recommended)

Install `claudeup` for easy API key management:

\`\`\`bash
npm install -g claudeup@latest
claudeup config set OPENROUTER_API_KEY your-api-key
\`\`\`

### Continue Without It?

You can continue, but:
- Only **embedded Claude Sonnet** will be used for reviews
- No parallel multi-model validation
- Fewer diverse perspectives on code quality
- Still functional, just less comprehensive

Do you want to continue without external AI models?
```

**Use AskUserQuestion:**
```
OpenRouter API key is not configured. What would you like to do?

Options:
- "Continue with embedded Claude only" - Use only Claude Sonnet for reviews (still good!)
- "Cancel and configure API key first" - I'll set up OpenRouter and restart
```

## Implementation Patterns

### Pattern 1: Check Both Dependencies (for /implement command)

```bash
# At the start of /implement command

echo "Checking required dependencies..."

# Check 1: Chrome DevTools MCP
CHROME_MCP_AVAILABLE=false
if mcp__chrome-devtools__list_pages 2>/dev/null; then
  CHROME_MCP_AVAILABLE=true
  echo "✓ Chrome DevTools MCP: Available"
else
  echo "✗ Chrome DevTools MCP: Not available"
fi

# Check 2: OpenRouter API Key
OPENROUTER_AVAILABLE=false
if [[ -n "${OPENROUTER_API_KEY}" ]]; then
  OPENROUTER_AVAILABLE=true
  echo "✓ OpenRouter API Key: Configured"
else
  echo "✗ OpenRouter API Key: Not configured"
fi

# Check 3: Claudish CLI (for external models)
CLAUDISH_AVAILABLE=false
if npx claudish --version 2>/dev/null; then
  CLAUDISH_AVAILABLE=true
  echo "✓ Claudish CLI: Available"
else
  echo "✗ Claudish CLI: Not available"
fi
```

### Pattern 2: Conditional Workflow Adaptation

Based on dependency availability, adapt the workflow:

```markdown
## Workflow Adaptation Based on Dependencies

| Dependency | Available | Workflow Impact |
|------------|-----------|-----------------|
| Chrome DevTools MCP | ✓ | Full UI validation with screenshots |
| Chrome DevTools MCP | ✗ | Skip PHASE 2.5 (Design Fidelity Validation) |
| OpenRouter + Claudish | ✓ | Multi-model parallel code review (3-5x faster) |
| OpenRouter + Claudish | ✗ | Single-model embedded Claude review only |

### Graceful Degradation

Commands should ALWAYS complete, even with missing dependencies:

1. **Missing Chrome DevTools MCP:**
   - Skip: Design fidelity validation, browser testing
   - Keep: Code implementation, code review, testing
   - Message: "UI validation skipped - please manually verify visual changes"

2. **Missing OpenRouter API:**
   - Skip: External multi-model reviews
   - Keep: Embedded Claude Sonnet review (still comprehensive!)
   - Message: "Using embedded Claude Sonnet reviewer only"

3. **Missing Both:**
   - Still functional for core implementation
   - Skip: UI validation, multi-model review
   - Message: "Running in minimal mode - core functionality preserved"
```

### Pattern 3: One-Time Check with Session Cache

Store dependency status in session metadata to avoid repeated checks:

```bash
# In session-meta.json
{
  "dependencies": {
    "chromeDevToolsMcp": true,
    "openrouterApiKey": false,
    "claudishCli": true,
    "checkedAt": "2025-12-10T10:30:00Z"
  }
}
```

## Quick Reference Messages

### claudeup Installation (Copy-Paste Ready)

```bash
# Install claudeup globally
npm install -g claudeup@latest

# Add Chrome DevTools MCP
claudeup mcp add chrome-devtools

# Configure OpenRouter API key
claudeup config set OPENROUTER_API_KEY your-api-key
```

### OpenRouter Quick Start

1. Visit: https://openrouter.ai
2. Sign up (free account)
3. Get API key from dashboard
4. Set in terminal: `export OPENROUTER_API_KEY="sk-or-..."`

### Why Multi-Model Matters

| Single Model | Multi-Model |
|--------------|-------------|
| 1 perspective | 4-5 perspectives |
| ~5 min review | ~5 min (parallel!) |
| May miss issues | Consensus catches more |
| Good | Better |

## Integration Example

Here's how to integrate this skill at the start of a command:

```markdown
## STEP 0.5: Dependency Check (Before Session Init)

**Check required dependencies and inform user of any limitations.**

1. Run dependency checks using dependency-check skill patterns
2. Store results in workflow state
3. If critical dependencies missing:
   - Show helpful setup instructions
   - Ask user if they want to continue with reduced functionality
4. Adapt workflow based on available dependencies:
   - chromeDevToolsMcp=false → Skip UI validation phases
   - openrouterApiKey=false → Use embedded-only review
5. Continue to STEP 0 (Session Init) with dependency status known
```

## Notes

- **Non-blocking by default**: Always allow users to continue with reduced functionality
- **Clear messaging**: Explain what will be skipped and why
- **Easy setup paths**: Recommend claudeup for simplified management
- **Cost transparency**: Be clear about OpenRouter costs (affordable/free options exist)
- **One-time per session**: Cache dependency status to avoid repeated checks
