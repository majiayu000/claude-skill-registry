---
name: tana
description: Enables Claude to create and manage notes with supertags in Tana via Playwright MCP
category: productivity
---

# Tana Skill

## Overview
Claude can manage your Tana workspace to capture thoughts, build structured data with supertags, and create a powerful knowledge base. A tool for structured note-taking and data management.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/tana/install.sh | bash
```

Or manually:
```bash
cp -r skills/tana ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TANA_EMAIL "your-email@example.com"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Create nodes and outlines
- Use supertags for structure
- Define fields on supertags
- Build live searches
- Create views and queries
- Use commands and AI
- Build templates
- Create bidirectional links
- Add date references
- Use inline references
- Build dashboards
- Share workspaces

## Usage Examples

### Example 1: Add Node
```
User: "Add a #task for reviewing the proposal"
Claude: Creates node with #task supertag.
        Confirms: "Task created: Review the proposal"
```

### Example 2: Create Supertag
```
User: "Create a #project supertag with status and deadline fields"
Claude: Creates supertag with defined fields.
        Confirms: "Created #project supertag with 2 fields"
```

### Example 3: Live Search
```
User: "Show all tasks due this week"
Claude: Creates live search with date filter.
        Reports: "Found 8 tasks due this week"
```

### Example 4: Daily Notes
```
User: "Add to today's daily note: Met with the design team"
Claude: Opens today's date node, adds content.
        Confirms: "Added to today's daily note"
```

## Authentication Flow
1. Claude navigates to tana.inc via Playwright MCP
2. Enters TANA_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for operations

## Selectors Reference
```javascript
// Main content
'.tana-editor'

// Node
'.node-container'

// Node content
'.node-content'

// Supertag
'.supertag'

// Field
'.field-container'

// Search
'.search-input'

// Daily notes
'.daily-notes'

// Live search
'.live-search'

// Command line
'.command-palette'

// References
'.references-panel'
```

## Tana Syntax
```
#supertag           // Apply supertag
^date               // Date reference
>inline reference   // Inline node
[[link]]            // Page link
@mention            // Mention
/command            // Run command
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Node Not Found**: Search with variations, ask user
- **Supertag Error**: Check definition, suggest fix
- **Search Failed**: Verify query syntax
- **Sync Failed**: Wait and retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Tana:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific supertag configurations
4. Note useful live search patterns

## Notes
- Supertags define structured data
- Fields for consistent data capture
- Live searches for dynamic views
- AI commands built-in
- Daily notes for journals
- Commands for automation
- Templates for patterns
- Currently invite-only access
