---
name: craft-docs
description: Enables Claude to create and manage documents in Craft via Playwright MCP
category: productivity
---

# Craft Docs Skill

## Overview
Claude can manage your Craft documents to create beautiful documents, organize content, and collaborate with others. A native document editor with powerful block-based editing.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/craft-docs/install.sh | bash
```

Or manually:
```bash
cp -r skills/craft-docs ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CRAFT_EMAIL "your-email@example.com"
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
- Create and edit documents
- Organize with folders and spaces
- Apply block styling
- Add images and media
- Create links between documents
- Share and collaborate
- Export in multiple formats
- Use templates
- Create tables and cards
- Toggle blocks for organization
- Add code blocks
- Create backlinks

## Usage Examples

### Example 1: Create Document
```
User: "Create a new Craft doc for meeting notes"
Claude: Creates document "Meeting Notes" with date.
        Confirms: "Document created in default space"
```

### Example 2: Organize Content
```
User: "Move my project docs to the Work folder"
Claude: Finds project documents, moves to Work folder.
        Confirms: "Moved 6 documents to Work folder"
```

### Example 3: Share Document
```
User: "Share the proposal document with the team"
Claude: Opens sharing settings, generates share link.
        Returns: "Share link created: [link]"
```

### Example 4: Search Docs
```
User: "Find my docs about the marketing campaign"
Claude: Searches for "marketing campaign".
        Reports: "Found 3 documents: Campaign Strategy, Q4 Plan..."
```

## Authentication Flow
1. Claude navigates to craft.do via Playwright MCP
2. Enters CRAFT_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for document operations

## Selectors Reference
```javascript
// Document list
'.documents-list'

// Document item
'.document-item'

// Editor
'.craft-editor'

// Block
'.block-container'

// Title
'.document-title'

// Folder sidebar
'.folders-sidebar'

// New document
'.new-document-button'

// Share button
'.share-button'

// Export menu
'.export-menu'

// Search
'.search-input'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Document Not Found**: Search with variations, ask user
- **Share Failed**: Check permissions, retry
- **Export Failed**: Try alternative format
- **Sync Failed**: Wait and retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Craft:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific document organization strategies
4. Note useful block types

## Notes
- Native Apple experience
- Block-based editing
- Beautiful typography
- Markdown import/export
- Real-time collaboration
- Offline support
- Backlinks for connections
- Spaces for organization
- Web version available
