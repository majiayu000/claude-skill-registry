---
name: coda
description: Enables Claude to create and manage documents with tables and automation in Coda via Playwright MCP
category: productivity
---

# Coda Skill

## Overview
Claude can manage your Coda workspace to create docs with tables, build automations, and create interactive documents. Combines documents and spreadsheets in one powerful tool.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/coda/install.sh | bash
```

Or manually:
```bash
cp -r skills/coda ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CODA_EMAIL "your-email@example.com"
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
- Create and edit docs
- Build tables with views
- Create formulas and calculations
- Set up automations
- Build buttons and controls
- Create charts and visualizations
- Use templates (Packs)
- Share and collaborate
- Create cross-doc connections
- Build interactive pages
- Add conditional formatting
- Integrate with external services

## Usage Examples

### Example 1: Create Doc
```
User: "Create a Coda doc for tracking team tasks"
Claude: Creates doc with Tasks table, adds views for status.
        Returns: "Created Tasks doc with table and views"
```

### Example 2: Add Table
```
User: "Add a contacts table to my CRM doc"
Claude: Opens doc, adds table with name, email, company columns.
        Confirms: "Contacts table added with 3 columns"
```

### Example 3: Create Automation
```
User: "Set up a reminder when tasks are due"
Claude: Creates automation rule for due date reminders.
        Confirms: "Automation created for due date alerts"
```

### Example 4: Build View
```
User: "Create a kanban view for the projects table"
Claude: Adds kanban view grouped by status.
        Confirms: "Kanban view created for projects"
```

## Authentication Flow
1. Claude navigates to coda.io via Playwright MCP
2. Enters CODA_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for doc operations

## Selectors Reference
```javascript
// Doc list
'.docs-list'

// Page content
'.page-content'

// Table
'.table-wrapper'

// Row
'.table-row'

// Add row button
'.add-row-button'

// Formula bar
'.formula-bar'

// View selector
'.view-selector'

// Automation button
'.automation-button'

// Pack settings
'.pack-settings'

// Share button
'.share-button'
```

## Coda Formulas
```
Filter(table, condition)    // Filter rows
Lookup(table, col, value)   // Find value
FormulaMap(list, fn)        // Transform list
If(cond, true, false)       // Conditional
Concatenate(str1, str2)     // Join strings
Today()                     // Current date
User()                      // Current user
Button()                    // Interactive button
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Doc Not Found**: List available docs, ask user
- **Formula Error**: Identify syntax issue, suggest fix
- **Automation Failed**: Check rule configuration
- **Pack Error**: Verify Pack connection

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Coda:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific formula patterns
4. Note useful Pack integrations

## Notes
- Documents with database power
- Formulas similar to spreadsheets
- Automations for workflows
- Packs for integrations
- Buttons for interactivity
- Cross-doc for data sharing
- Templates gallery available
- API for advanced automation
