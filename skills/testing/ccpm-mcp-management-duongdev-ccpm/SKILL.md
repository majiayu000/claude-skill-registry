---
name: ccpm-mcp-management
description: 'Discovers, manages, and troubleshoots MCP servers with three-tier classification
  (required: Linear/GitHub/Context7, optional: Jira/Confluence/Slack/BitBucket). Auto-activates
  when user asks "MCP serve'
---

---
name: ccpm-mcp-management
description: Discovers, manages, and troubleshoots MCP servers with three-tier classification (required: Linear/GitHub/Context7, optional: Jira/Confluence/Slack/BitBucket). Auto-activates when user asks "MCP server", "tools available", "Linear not working", "what tools do I have", or when plugin installation fails. Provides automatic server discovery, configuration validation, and health monitoring. Diagnoses connection issues (missing env vars, wrong config, network problems) with specific fix suggestions. Requires setup confirmation for optional PM integrations. Shows rate limit status and recommends optimizations when performance degrades.
---

# CCPM MCP Management

MCP server discovery, configuration, and troubleshooting for CCPM workflows.

## When to Use

This skill auto-activates when:

- User asks: **"MCP server"**, **"tools available"**, **"Linear not working"**, **"what tools do I have"**
- Running **`/ccpm:work`** command
- Plugin installation issues
- MCP tools failing to load
- Troubleshooting CCPM setup

## CCPM Required MCP Servers

### Critical Servers (Must Have)

**1. Linear MCP Server**
- **Purpose**: Task tracking, issue management, Linear Documents
- **Used by**: All `/ccpm:*` commands
- **Tools**: `linear_create_issue`, `linear_update_issue`, `linear_create_document`, etc.
- **Setup**: Required in `.claude/mcp.json`

**2. GitHub MCP Server**
- **Purpose**: PR creation, repository operations
- **Used by**: `/ccpm:done`
- **Tools**: `github_create_pr`, `github_list_prs`, `github_get_repo`
- **Setup**: Required for completion workflow

**3. Context7 MCP Server**
- **Purpose**: Latest library documentation
- **Used by**: `/ccpm:plan`, `docs-seeker` skill
- **Tools**: `context7_fetch_docs`, `context7_search`
- **Setup**: Required for spec writing

### Optional Servers (PM Integrations)

**4. Jira MCP Server** (if using Jira)
- **Purpose**: Jira ticket integration
- **Used by**: `/ccpm:plan`, `/ccpm:done`
- **Tools**: `jira_get_issue`, `jira_update_status`
- **Setup**: Optional, only if syncing with Jira

**5. Confluence MCP Server** (if using Confluence)
- **Purpose**: Confluence page integration
- **Used by**: `/ccpm:plan`
- **Tools**: `confluence_get_page`, `confluence_search`
- **Setup**: Optional, for gathering context

**6. Slack MCP Server** (if using Slack)
- **Purpose**: Team notifications
- **Used by**: `/ccpm:done`
- **Tools**: `slack_post_message`, `slack_list_channels`
- **Setup**: Optional, for notifications

## MCP Server Discovery

### Check Available Servers

```
User: "What MCP servers are available?"

Claude: [ccpm-mcp-management activates]

Discovering MCP servers...

✅ REQUIRED SERVERS (All present):
1. Linear MCP
   Status: Connected
   Tools: 15 available
   - linear_create_issue
   - linear_update_issue
   - linear_get_issue
   - linear_create_document
   - linear_list_teams
   [+ 10 more]

2. GitHub MCP
   Status: Connected
   Tools: 8 available
   - github_create_pr
   - github_list_prs
   - github_get_repo
   [+ 5 more]

3. Context7 MCP
   Status: Connected
   Tools: 3 available
   - context7_fetch_docs
   - context7_search
   - context7_list_sources

⚠️ OPTIONAL SERVERS (Not configured):
4. Jira MCP - Not configured
   Impact: Cannot sync with Jira
   Setup: Add to .claude/mcp.json if needed

5. Confluence MCP - Not configured
   Impact: Cannot fetch Confluence pages
   Setup: Add to .claude/mcp.json if needed

6. Slack MCP - Not configured
   Impact: Cannot send notifications
   Setup: Add to .claude/mcp.json if needed

All required servers operational ✅
```

### Troubleshooting Server Issues

```
User: "Linear tools not working"

Claude: [ccpm-mcp-management activates]

Troubleshooting Linear MCP server...

Step 1: CHECK CONNECTION
Testing Linear MCP connection...
❌ Connection failed: ECONNREFUSED

Step 2: DIAGNOSE
Possible causes:
1. Linear MCP server not running
2. Incorrect configuration in .claude/mcp.json
3. Missing Linear API key
4. Network connectivity issues

Step 3: VERIFY CONFIGURATION
Checking .claude/mcp.json...

Found configuration:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "${LINEAR_API_KEY}"
      }
    }
  }
}
```

Step 4: CHECK ENVIRONMENT
Checking LINEAR_API_KEY...
❌ Environment variable not set

ROOT CAUSE: Missing LINEAR_API_KEY

FIX:
1. Get Linear API key from https://linear.app/settings/api
2. Add to environment:
   export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxx"

3. Restart Claude Code

Would you like help setting up the API key?
```

## Configuration Guide

### Minimal CCPM Configuration

**`.claude/mcp.json` (required servers only)**:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "${LINEAR_API_KEY}"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"],
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      }
    }
  }
}
```

### Full CCPM Configuration

**With optional PM integrations**:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "${LINEAR_API_KEY}"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"],
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      }
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-jira"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_EMAIL": "${JIRA_EMAIL}",
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}"
      }
    },
    "confluence": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-confluence"],
      "env": {
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_EMAIL": "${CONFLUENCE_EMAIL}",
        "CONFLUENCE_API_TOKEN": "${CONFLUENCE_API_TOKEN}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

## Common Issues & Solutions

### Issue 1: MCP Server Not Found

**Symptom**: "MCP server 'linear' not found"

**Solution**:
```bash
# Check if MCP server package exists
npx @modelcontextprotocol/server-linear --version

# If not found, package name might be wrong
# Check official MCP registry

# Update .claude/mcp.json with correct package name
```

### Issue 2: Authentication Failures

**Symptom**: "Unauthorized" or "Invalid API key"

**Solution**:
```bash
# Check environment variables are set
echo $LINEAR_API_KEY
echo $GITHUB_TOKEN

# If empty, add to shell profile
echo 'export LINEAR_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc

# Or use .env file
cat > .env << EOF
LINEAR_API_KEY=lin_api_xxxxx
GITHUB_TOKEN=ghp_xxxxx
CONTEXT7_API_KEY=ctx7_xxxxx
EOF

# Restart Claude Code to pick up changes
```

### Issue 3: Command Not Found

**Symptom**: "npx: command not found"

**Solution**:
```bash
# Install Node.js and npm
# macOS
brew install node

# Linux
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows
# Download from https://nodejs.org

# Verify installation
node --version
npm --version
npx --version
```

### Issue 4: Permission Denied

**Symptom**: "EACCES: permission denied"

**Solution**:
```bash
# Fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc

# Or use sudo (not recommended)
sudo npx @modelcontextprotocol/server-linear
```

## Integration with CCPM Commands

### `/ccpm:work` Integration

```
User: "/ccpm:work"

Claude: [ccpm-mcp-management activates]

CCPM Help - Available Tools

MCP Server Status:
✅ Linear (15 tools) - Task tracking
✅ GitHub (8 tools) - PR creation
✅ Context7 (3 tools) - Documentation
❌ Jira (not configured) - Optional
❌ Slack (not configured) - Optional

Available CCPM Commands: 37 total
- Spec Management: 6 commands
- Planning: 4 commands
- Implementation: 3 commands
- Verification: 3 commands
- Completion: 1 command
- Utilities: 20 commands

For setup help: Ask "How do I configure Jira MCP?"
For troubleshooting: Mention "Linear not working"
```

### Plugin Installation Verification

```
After installing CCPM plugin:

Claude: [ccpm-mcp-management auto-activates]

Verifying CCPM plugin requirements...

Checking required MCP servers:
✅ Linear MCP - Connected
✅ GitHub MCP - Connected
❌ Context7 MCP - Not found

CCPM plugin requires Context7 for documentation features.

Setup instructions:
1. Add to .claude/mcp.json:
   ```json
   "context7": {
     "command": "npx",
     "args": ["-y", "@context7/mcp-server"],
     "env": {
       "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
     }
   }
   ```

2. Get API key: https://context7.ai/signup

3. Set environment variable:
   export CONTEXT7_API_KEY="ctx7_xxxxx"

4. Restart Claude Code

Would you like help with any of these steps?
```

## Server Health Monitoring

### Health Check Command

```
User: "Check MCP server health"

Claude: [ccpm-mcp-management activates]

Running health checks on all MCP servers...

LINEAR MCP:
Status: ✅ Healthy
Response time: 45ms
Tools available: 15/15
Last successful call: 2 minutes ago
Rate limit: 4,800 / 5,000 remaining

GITHUB MCP:
Status: ✅ Healthy
Response time: 120ms
Tools available: 8/8
Last successful call: 15 minutes ago
Rate limit: 4,950 / 5,000 remaining

CONTEXT7 MCP:
Status: ⚠️ Degraded
Response time: 3,200ms (slow)
Tools available: 3/3
Last successful call: 1 hour ago
Note: Docs fetching slower than usual, still functional

JIRA MCP:
Status: ❌ Not configured
Impact: Cannot sync Jira tickets
Action: Configure if Jira integration needed

Overall health: Good (2/3 required servers healthy)
```

## Best Practices

### Do's

- ✅ Set environment variables in shell profile (persistent)
- ✅ Use `.env` file for project-specific keys
- ✅ Test MCP connections after setup
- ✅ Monitor rate limits
- ✅ Keep MCP server packages updated
- ✅ Document custom MCP configurations

### Don'ts

- ❌ Hardcode API keys in `.claude/mcp.json`
- ❌ Commit API keys to git
- ❌ Ignore authentication errors
- ❌ Run with sudo unnecessarily
- ❌ Use outdated MCP server versions
- ❌ Skip health checks

## Summary

This skill provides:

- ✅ MCP server discovery
- ✅ Configuration validation
- ✅ Troubleshooting guidance
- ✅ CCPM-specific server requirements
- ✅ Health monitoring
- ✅ Setup assistance

**Focus**: CCPM required servers (Linear, GitHub, Context7) + optional PM integrations (Jira, Confluence, Slack)

**Philosophy**: Reliable infrastructure for reliable PM workflows. Monitor, maintain, troubleshoot proactively.

---

**Source**: Adapted from [claudekit-skills/mcp-management](https://github.com/mrgoonie/claudekit-skills)
**License**: MIT
**CCPM Integration**: `/ccpm:work`, plugin installation, troubleshooting
**Required Servers**: Linear, GitHub, Context7
**Optional Servers**: Jira, Confluence, Slack, BitBucket
