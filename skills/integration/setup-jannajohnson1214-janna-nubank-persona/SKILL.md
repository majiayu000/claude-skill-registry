# Setup Granola Integration Skill

Copy this to `.claude/skills/setup-granola/SKILL.md` to enable automatic installation.

---

```markdown
---
name: setup-granola
description: Install and configure Granola MCP server for meeting sync. Use when user says "set up Granola", "install Granola integration", or "connect Granola".
---

# Setup Granola Integration

Automatically install and configure the Granola MCP server for syncing meetings to Personal OS.

## Prerequisites Check

Before starting, verify:
1. User is on macOS (Granola is macOS only)
2. User has Granola.ai installed
3. Python 3.12+ is available
4. uv is installed (or can be installed)

## Instructions

### Step 1: Check Prerequisites

Run these checks and report any issues:

```bash
# Check OS
uname -s  # Should be Darwin

# Check Python version
python3 --version  # Should be 3.12+

# Check uv
uv --version  # Install if missing: brew install uv

# Check if Granola cache exists
ls ~/Library/Application\ Support/Granola/cache-v3.json
```

If uv is missing, offer to install it:
```bash
brew install uv
```

If Granola cache doesn't exist, inform user they need to:
1. Install Granola from https://granola.ai
2. Attend or record at least one meeting

### Step 2: Clone MCP Server

Ask user where to clone (suggest ~/Projects):

```bash
cd ~/Projects  # or user's preferred location
git clone https://github.com/proofgeist/granola-ai-mcp-server.git
cd granola-ai-mcp-server
uv sync
```

### Step 3: Test Server

Verify installation works:

```bash
cd ~/Projects/granola-ai-mcp-server
uv run python test_server.py
```

### Step 4: Create Transcripts Folder

```bash
mkdir -p Knowledge/Transcripts
```

### Step 5: Install Skills

Copy the Granola skills to the user's Claude skills folder:

```bash
mkdir -p .claude/skills/meeting-sync
cp core/integrations/granola/skills/meeting-sync/SKILL.md .claude/skills/meeting-sync/
```

### Step 6: Update .mcp.json

Read the current `.mcp.json` file and add the granola server config.

The config should be:

```json
{
  "mcpServers": {
    "granola": {
      "command": "uv",
      "args": [
        "--directory",
        "<GRANOLA_MCP_PATH>",
        "run",
        "granola-mcp-server"
      ],
      "env": {
        "KNOWLEDGE_PATH": "<PERSONAL_OS_PATH>/Knowledge"
      }
    }
  }
}
```

Replace:
- `<GRANOLA_MCP_PATH>` with absolute path to granola-ai-mcp-server
- `<PERSONAL_OS_PATH>` with absolute path to personal-os workspace

### Step 7: Verify Setup

Ask user to restart Claude Code, then test:

```
Search my meetings for "test"
```

or

```
Check for new Granola meetings
```

## Success Criteria

- [ ] Prerequisites verified
- [ ] granola-ai-mcp-server cloned and dependencies installed
- [ ] test_server.py passes
- [ ] Knowledge/Transcripts folder exists
- [ ] meeting-sync skill installed to .claude/skills/
- [ ] .mcp.json updated with granola config
- [ ] Claude Code restarted
- [ ] Granola tools accessible (search_meetings works)

## Troubleshooting

### Python version too old
```bash
brew install python@3.12
```

### uv sync fails
```bash
pip install uv  # Alternative installation
```

### Permission denied on cache
Granola must be running with proper permissions. User should open Granola app once.

### MCP not loading
Check .mcp.json syntax and ensure paths are absolute (not relative).

## After Setup

Inform user they can now:
- Say "Sync my Granola meetings" to sync new meetings
- Morning planning will automatically check for new meetings
- Search across all meeting content
```
