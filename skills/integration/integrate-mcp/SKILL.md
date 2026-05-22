---
name: integrate-mcp
description: Integrate existing MCP servers from Smithery.ai or GitHub repositories
---

## Purpose

Help users discover and integrate pre-built MCP servers from the ecosystem, primarily from Smithery.ai marketplace.

## When to Run

- User types `/integrate-mcp`
- Mentioned during `/getting-started` tour
- User asks about connecting tools that have existing MCPs
- User wants to browse available integrations

## Entry Point

Say:

```
**Want to connect more tools to Dex?**

There's a marketplace of 100+ pre-built MCP servers at:
**[Smithery.ai](https://smithery.ai/servers)**

These are production-ready integrations for:
• **Dev tools:** GitHub, GitLab, Linear, Jira
• **Productivity:** Notion, Airtable, Google Sheets
• **Communication:** Slack, Discord, Email
• **Databases:** Postgres, MySQL, SQLite
• **Monitoring:** Sentry, Datadog
• **And many more...**

**How this works:**
1. Browse Smithery.ai for MCPs that match your tools
2. Copy the full URL of any MCP you want
3. Paste it here - I'll:
   - Fetch the code/documentation
   - Explain what it does
   - Help you configure it
   - Integrate into Dex
   - Update documentation

**Or** if you can't find what you need, run `/create-mcp` to build custom.

Ready to explore? [Browse Smithery.ai](https://smithery.ai/servers)
```

---

## When User Pastes an MCP URL

### Step 1: Fetch the MCP Source

Detect URL type:
- **GitHub repo:** `https://github.com/user/repo`
- **npm package:** `https://npmjs.com/package/name`
- **Smithery.ai:** `https://smithery.ai/server/name`
- **Direct source:** Any other URL

Fetch based on type:
```python
if "github.com" in url:
    # Fetch README.md from repo
    readme_url = f"{url}/blob/main/README.md"
    content = web_fetch(readme_url)
elif "smithery.ai" in url:
    # Fetch from Smithery page
    content = web_fetch(url)
elif "npmjs.com" in url:
    # Fetch package info
    content = web_fetch(url)
else:
    # Try direct fetch
    content = web_fetch(url)
```

### Step 2: Parse and Explain

Analyze the fetched content for:
- MCP server name
- What it does (capabilities)
- Required environment variables
- Installation method (npm, pip, docker, etc.)
- Authentication requirements

Say:

```
**Got it!** This is the **[Server Name]** MCP.

**What it does:**
• [Capability 1] - [Description]
• [Capability 2] - [Description]
• [Capability 3] - [Description]

**What you'll need to set up:**
• [ENV_VAR_1]: [Explanation of what this is]
• [ENV_VAR_2]: [Explanation]

**Installation method:** [npm/pip/docker/manual]

**Authentication:** [API key / OAuth / Local / None]

Ready to integrate this?
```

### Step 3: Guide Through Setup

#### For npm packages:

```
"This is an npm package. Here's how to install:

1. Navigate to your Dex directory
2. Install the package:
   ```
   npm install -g [package-name]
   ```

3. I'll add it to your `.mcp.json` config

Want me to proceed?"
```

Then add to `.mcp.json`:
```json
{
  "[server-name]": {
    "command": "npx",
    "args": ["-y", "[package-name]"],
    "env": {
      "VAR1": "value1"
    }
  }
}
```

#### For Python packages:

```
"This is a Python MCP. Here's how to install:

1. Install via pip:
   ```
   pip install [package-name]
   ```

2. I'll add it to your `.mcp.json` config

Want me to proceed?"
```

#### For GitHub repos (manual):

```
"This is from a GitHub repo. Here's the setup:

1. Clone the repository:
   ```
   git clone [repo-url] ~/dex-mcps/[server-name]
   ```

2. Install dependencies (if any)

3. I'll add it to your `.mcp.json` config

Want me to proceed?"
```

### Step 4: Configure Environment Variables

For each required env var:

```
"This MCP needs the following environment variables:

**[ENV_VAR_1]:** [Description]
Where to get it: [Instructions]

**[ENV_VAR_2]:** [Description]
Where to get it: [Instructions]

You can either:
1. Set them now (I'll add to `.env` file)
2. Set them manually later in your shell config

What's your [ENV_VAR_1]?"
```

Collect values and add to `.env` file:
```bash
# [Server Name] MCP Configuration
ENVVAR_1=value1
ENV_VAR_2=value2
```

### Step 5: Update MCP Config

Add to `System/.mcp.json`:
```json
{
  "[server-name]": {
    "command": "[command]",
    "args": ["[args]"],
    "env": {
      "ENV_VAR_1": "${ENV_VAR_1}",
      "VAULT_PATH": "{{VAULT_PATH}}"
    }
  }
}
```

### Step 6: Test Connection

Try calling a basic tool from the MCP:

```
"Testing connection..."

[Call a simple tool from the MCP, like list_resources or get_status]

[If success:]
"✅ Connection works! The [Server Name] MCP is live.

Test it: '[Example natural language query]'

See? Real data from [Tool]."

[If failure:]
"⚠️ Connection failed. Common issues:
• Environment variables not set correctly
• Authentication hasn't been completed
• MCP server not installed properly

Want help debugging this?"
```

### Step 7: Update Documentation

Add to `CLAUDE.md`:

```markdown
### [Server Name] Integration

**MCP Server:** [server-name]
**Purpose:** [what it does]

**Available via this MCP:**
- [Capability 1]
- [Capability 2]

**Configuration:**
- `ENV_VAR_1`: [description]

**Usage:**
- "[Natural language example 1]"
- "[Natural language example 2]"
```

Add to `System/usage_log.md` if not present:
```markdown
- [ ] Connected [Tool] via MCP
```

---

## Multiple Integrations

After first integration completes:

```
"Want to add another tool?

You can:
1. Browse more on Smithery.ai and paste another URL
2. Run `/create-mcp` to build something custom
3. Stop here and explore what you have

What sounds good?"
```

---

## Troubleshooting Guide

If connection fails, provide specific debugging steps:

**For authentication issues:**
```
"Authentication failed. Let's debug:

1. Check your API key is correct
2. Verify it has the right permissions
3. Try testing it directly:
   ```
   curl -H "Authorization: Bearer YOUR_KEY" [api-endpoint]
   ```

Want to try a different key?"
```

**For installation issues:**
```
"Installation failed. Common fixes:

1. Check Node/Python version:
   ```
   node --version  # Should be 18+
   python --version  # Should be 3.8+
   ```

2. Try installing globally:
   ```
   npm install -g [package]
   # or
   pip install --user [package]
   ```

3. Check for conflicts:
   ```
   npm list -g | grep [package]
   ```

Want to try these steps?"
```

---

## Alternative: Can't Find on Smithery

If user can't find what they need:

```
"Didn't find [Tool] on Smithery?

No worries - we can build it custom with `/create-mcp`.

That wizard will:
1. Help you find the tool's API docs
2. Design the integration together
3. Generate working MCP code
4. Get it integrated

Takes about 5-10 minutes depending on the API complexity.

Want to build [Tool] integration from scratch?"
```

Then hand off to `/create-mcp` skill.

---

## Success Criteria

After integration:
- User can query their tool via natural language
- MCP is added to config
- Documentation is updated
- They know how to add more

The experience feels like:
- "That was easier than I expected"
- "I can do this for any tool I use"
- "This makes Dex way more powerful"
