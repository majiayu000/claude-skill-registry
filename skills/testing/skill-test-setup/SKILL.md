---
name: test-setup
description: Complete testing environment setup and tool verification. Use at project start, when onboarding new developers, or when testing tools need configuration. Detects environment (codespace/local/container), analyzes existing test setup, verifies and installs testing tools and MCPs. Triggers on "setup testing", "configure tests", "install test tools", "verify testing environment".
---

# Test Setup

## Purpose

Analyze the development environment and configure all testing tools and MCPs. Ensures the testing stack is ready for development.

**Approach:** Detect what exists, verify it works, install what's missing. Always ask user confirmation before making changes.

## When to Use

- Starting a new project
- Onboarding to existing project
- Testing tools not working
- Setting up new development environment
- After cloning a repository

**When NOT to use:**
- Tools already verified working
- Quick test execution (use specific testing skills)
- CI/CD setup (different skill)

## Quick Start

```bash
# Run complete setup analysis
# This skill will:
# 1. Detect environment type
# 2. Analyze existing test configuration
# 3. Verify available tools
# 4. Propose installations
```

## Step 1: Environment Detection

### Detect Environment Type

```bash
# Check for codespace indicators
if [ -n "$CODESPACE_NAME" ] || [ -n "$GITHUB_CODESPACE_TOKEN" ]; then
    ENV_TYPE="codespace"
elif [ -f "/.dockerenv" ] || [ -n "$CONTAINER_ID" ]; then
    ENV_TYPE="container"
else
    ENV_TYPE="local"
fi
```

### Detect Project Type

```bash
# Check for common project indicators
if [ -f "package.json" ]; then
    PROJECT_TYPE="node"
    # Check for frameworks
    if grep -q "vite" package.json; then FRAMEWORK="vite"; fi
    if grep -q "svelte" package.json; then FRAMEWORK="svelte"; fi
    if grep -q "react" package.json; then FRAMEWORK="react"; fi
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    PROJECT_TYPE="python"
elif [ -f "Cargo.toml" ]; then
    PROJECT_TYPE="rust"
fi
```

## Step 2: Analyze Existing Test Setup

### Check for Existing Test Configuration

| File | Indicates |
|------|-----------|
| `jest.config.js/ts` | Jest configured |
| `vitest.config.ts` | Vitest configured |
| `playwright.config.ts` | Playwright configured |
| `pytest.ini` | pytest configured |
| `package.json` scripts.test | Test command defined |

### Verify Existing Setup Works

```bash
# Try to run existing tests
if [ -f "package.json" ]; then
    npm test -- --version 2>/dev/null || echo "Test command not working"
fi

# Check for test files
find . -name "*.test.*" -o -name "*.spec.*" | head -5
```

## Step 3: Tool Verification & Installation

### 3.1 Unit Testing Framework

**If Node.js project:**

```bash
# Check existing setup
if ! grep -q "jest\|vitest" package.json 2>/dev/null; then
    echo "⚠️ No unit test framework detected"
    
    # Propose installation
    echo "Recommended: Vitest for Vite projects, Jest for others"
    
    # Ask user confirmation
    read -p "Install Vitest? (y/n) " confirm
    
    if [ "$confirm" = "y" ]; then
        npm install -D vitest @vitest/ui
        # Create vitest.config.ts
        cat > vitest.config.ts << 'EOF'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    coverage: {
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'tests/']
    }
  }
})
EOF
    fi
fi
```

**If Python project:**

```bash
# Check for pytest
if ! command -v pytest &> /dev/null; then
    echo "⚠️ pytest not found"
    pip install pytest pytest-cov pytest-asyncio
fi
```

### 3.2 Wallaby MCP (VS Code)

**Check if in VS Code:**

```bash
# Detect VS Code
if [ "$TERM_PROGRAM" = "vscode" ] || [ -n "$VSCODE_CWD" ]; then
    echo "✓ VS Code detected"
    
    # Check for Wallaby extension
    if [ -d "$HOME/.vscode/extensions/wallaby*" ] 2>/dev/null; then
        echo "✓ Wallaby extension installed"
        
        # Test Wallaby MCP connection
        # (Would need actual MCP check)
        echo "⚠️ Verify Wallaby MCP server configured in settings"
    else
        echo "⚠️ Wallaby extension not found"
        echo "Install from: https://marketplace.visualstudio.com/items?itemName=WallabyJs.wallaby-vscode"
    fi
else
    echo "ℹ️ Not in VS Code - Wallaby not applicable"
fi
```

### 3.3 Agent Browser CLI (Vercel)

```bash
# Check for agent-browser
if ! command -v agent-browser &> /dev/null; then
    echo "⚠️ Agent Browser CLI not found"
    
    # Propose installation
    echo "Install: npm install -g @vercel/agent-browser"
    echo "Or: npx @vercel/agent-browser"
    
    # Ask user
    read -p "Install Agent Browser CLI? (y/n) " confirm
    if [ "$confirm" = "y" ]; then
        npm install -g @vercel/agent-browser
    fi
else
    echo "✓ Agent Browser CLI found"
    agent-browser --version
fi
```

### 3.4 Chrome DevTools MCP

```bash
# Check MCP configuration
MCP_CONFIG="$HOME/.config/claude/mcp.json"
if [ -f "$MCP_CONFIG" ]; then
    if grep -q "chrome-devtools" "$MCP_CONFIG"; then
        echo "✓ Chrome DevTools MCP configured"
    else
        echo "⚠️ Chrome DevTools MCP not in config"
        echo "Add to $MCP_CONFIG:"
        cat << 'EOF'
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["@chrome-devtools/mcp-server"]
    }
  }
}
EOF
    fi
else
    echo "⚠️ No MCP config found"
fi
```

### 3.5 TestSprite MCP

```bash
# Check TestSprite MCP configuration
if [ -f "$MCP_CONFIG" ] && grep -q "testsprite" "$MCP_CONFIG"; then
    echo "✓ TestSprite MCP configured"
else
    echo "⚠️ TestSprite MCP not configured"
    echo "Requires API key from testsprite.ai"
    
    read -p "Have TestSprite API key? (y/n) " has_key
    if [ "$has_key" = "y" ]; then
        read -p "Enter API key: " api_key
        # Add to MCP config
        echo "Add to $MCP_CONFIG:"
        cat << EOF
{
  "mcpServers": {
    "testsprite": {
      "command": "npx",
      "args": ["@testsprite/mcp-server"],
      "env": {
        "TESTSPRITE_API_KEY": "$api_key"
      }
    }
  }
}
EOF
    fi
fi
```

### 3.6 Container-Use MCP by Dagger (Optional)

```bash
# Check Container-Use MCP
echo ""
echo "=== Optional: Container-Use MCP by Dagger ==="
echo "Use case: Isolated build tests, experiments, A/B testing"
echo "Environment: Local only (not codespace/CI)"
echo ""

if [ "$ENV_TYPE" = "local" ]; then
    if [ -f "$MCP_CONFIG" ] && grep -q "container-use\|dagger" "$MCP_CONFIG"; then
        echo "✓ Container-Use MCP configured"
    else
        echo "ℹ️ Container-Use MCP not configured (optional)"
        echo "Benefits:"
        echo "  - Isolated container tests independent of codebase"
        echo "  - Quick build tests from local"
        echo "  - Experiments and A/B testing"
        echo "  - Cloud-like environment on local machine"
        echo ""
        echo "Install: https://github.com/dagger/container-use-mcp"
        
        read -p "Configure Container-Use MCP? (y/n) " confirm
        if [ "$confirm" = "y" ]; then
            echo "Add to $MCP_CONFIG:"
            cat << 'EOF'
{
  "mcpServers": {
    "container-use": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "dagger/container-use-mcp"]
    }
  }
}
EOF
        fi
    fi
else
    echo "ℹ️ Container-Use MCP only for local development"
fi
```

## Step 4: Configuration Summary

### Generate Setup Report

```markdown
## Test Environment Setup Report

**Environment:** $ENV_TYPE
**Project:** $PROJECT_TYPE ($FRAMEWORK)

### Unit Testing
- [ ] Framework: $TEST_FRAMEWORK
- [ ] Config file: $TEST_CONFIG
- [ ] Test command: $TEST_COMMAND

### E2E/Browser Testing
- [ ] Agent Browser CLI: $AGENT_BROWSER_STATUS
- [ ] Playwright: $PLAYWRIGHT_STATUS
- [ ] TestSprite MCP: $TESTSPRITE_STATUS

### MCP Servers
- [ ] Wallaby: $WALLABY_STATUS
- [ ] Chrome DevTools: $CHROME_DEVTOOLS_STATUS
- [ ] TestSprite: $TESTSPRITE_MCP_STATUS
- [ ] Container-Use: $CONTAINER_USE_STATUS

### Next Steps
1. Install missing tools (marked with ⚠️)
2. Configure MCP servers with API keys
3. Run skill-testing-workflow for usage guidelines
```

## Progressive Disclosure

For detailed tool documentation, see:

- `references/wallaby-setup.md` - Wallaby configuration details
- `references/testsprite-setup.md` - TestSprite MCP setup
- `references/chrome-devtools-setup.md` - Chrome DevTools MCP
- `references/container-use-setup.md` - Container-Use by Dagger

## Integration with Other Skills

| Next Step | Skill | Purpose |
|-----------|-------|---------|
| TDD mindset | skill-testing-philosophy | Understand TDD principles |
| Testing workflow | skill-testing-workflow | Learn tool combinations |
| Pre-PR testing | skill-testsprite-pre-pr | Run TestSprite before PR |

## Version

v1.0.0 (2025-01-28) - Complete testing environment setup