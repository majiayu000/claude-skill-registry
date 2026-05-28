---
name: {{SKILL_ID}}
description: {{DESCRIPTION}}
category: {{CATEGORY}}
tags: [{{TAGS}}]
icon: "{{ICON}}"
version: "1.0.0"
author: "Canifi"
authType: {{AUTH_TYPE}}
requiresBrowser: {{REQUIRES_BROWSER}}
---

# {{SKILL_NAME}} Skill

## Overview
Claude can interact with {{SKILL_NAME}} to help you manage and automate tasks. {{DESCRIPTION}}

## Capabilities
- Connect to {{SKILL_NAME}} and authenticate
- Read and retrieve data from your account
- Create, update, and delete records
- Search and filter content
- Automate common workflows
- Handle errors gracefully with retry logic

## Required Environment Variables

Add to `~/.claude/canifi-env`:
```bash
{{ENV_VARS}}
```

## Usage Examples

### Example 1: Basic Connection
```
User: "Connect to {{SKILL_NAME}} and show me my recent activity"
Claude: Navigates to {{SKILL_NAME}}, authenticates using stored credentials,
        and retrieves recent activity. Provides a summary of findings.
```

### Example 2: Search
```
User: "Search for [query] in {{SKILL_NAME}}"
Claude: Uses {{SKILL_NAME}}'s search functionality to find matching results.
        Returns relevant items with key details.
```

### Example 3: Create New Item
```
User: "Create a new [item type] in {{SKILL_NAME}} with [details]"
Claude: Creates the requested item with the provided details.
        Confirms successful creation with link/reference.
```

### Example 4: Update Existing Item
```
User: "Update [item] in {{SKILL_NAME}} to [new values]"
Claude: Locates the specified item, makes the requested changes,
        and confirms the update was successful.
```

### Example 5: Batch Operations
```
User: "Archive all [items] from [time period] in {{SKILL_NAME}}"
Claude: Searches for matching items, processes them in batches,
        and reports the total number of items archived.
```

## Authentication Flow

{{#if AUTH_TYPE_BROWSER}}
1. Claude navigates to {{SKILL_NAME}} via Playwright MCP
2. If not already logged in:
   - Enters email/username from canifi-env
   - Handles password entry if stored
   - Handles 2FA if prompted (notifies user via iMessage)
3. Maintains session cookies for subsequent requests
4. Re-authenticates automatically when session expires
{{/if}}

{{#if AUTH_TYPE_API_KEY}}
1. Claude reads API credentials from canifi-env
2. Adds authentication header to all API requests
3. Handles token refresh if applicable
4. Falls back to browser auth if API fails
{{/if}}

{{#if AUTH_TYPE_OAUTH}}
1. Claude initiates OAuth flow via browser
2. Redirects user to {{SKILL_NAME}} authorization page
3. User approves access in the popup
4. Claude captures and stores access/refresh tokens
5. Automatically refreshes tokens before expiration
{{/if}}

{{#if AUTH_TYPE_NONE}}
1. No authentication required for this skill
2. Claude can access {{SKILL_NAME}} directly
{{/if}}

## Selectors Reference
```javascript
// Common selectors for {{SKILL_NAME}}
// Update these as the UI changes

// Login elements
const loginButton = '[data-testid="login-button"]';
const emailInput = 'input[type="email"]';
const passwordInput = 'input[type="password"]';

// Navigation
const mainNav = '[role="navigation"]';
const searchInput = 'input[type="search"]';

// Content areas
const mainContent = '[role="main"]';
const listItems = '[role="listitem"]';

// Action buttons
const createButton = '[data-testid="create-button"]';
const saveButton = '[data-testid="save-button"]';
const deleteButton = '[data-testid="delete-button"]';
```

## API Reference
```javascript
// If {{SKILL_NAME}} has an API, document key endpoints here

// Base URL
const API_BASE = 'https://api.{{SKILL_ID}}.com/v1';

// Common endpoints
// GET /items - List all items
// POST /items - Create new item
// GET /items/:id - Get single item
// PUT /items/:id - Update item
// DELETE /items/:id - Delete item
// GET /search?q=query - Search items
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| **Authentication Failed** | Invalid credentials or expired session | Retry 3 times, then notify user to check credentials |
| **Rate Limited** | Too many requests | Wait 60 seconds, retry with exponential backoff |
| **Not Found** | Item doesn't exist | Confirm query with user, suggest alternatives |
| **Permission Denied** | Insufficient access | Notify user to check account permissions |
| **Network Error** | Connection issues | Retry with increasing delays (1s, 2s, 4s, 8s) |
| **Timeout** | Page load too slow | Increase timeout, retry once, then notify user |
| **2FA Required** | Two-factor auth needed | Send iMessage: "{{SKILL_NAME}} requires 2FA approval" |
| **Account Locked** | Too many failed attempts | Notify user immediately, do not retry |

## Rate Limits
- **API Requests**: [X] requests per minute/hour
- **Batch Operations**: Process in groups of [Y]
- **Wait Between Actions**: [Z] seconds minimum

## Self-Improvement Instructions

When you discover a better approach for {{SKILL_NAME}}:

1. **Document the improvement** in your response to the user
2. **Suggest an update** to this skill file with specific changes
3. **Include working selectors** or API endpoints that performed better
4. **Note any UI/API changes** that broke previous functionality
5. **Record successful patterns** for future reference

### Update Format
When suggesting updates, use this format:
```
SKILL_UPDATE: {{SKILL_NAME}}
Section: [section name]
Change: [description of change]
New Content:
[new content to add/replace]
Reason: [why this is better]
```

## Known Issues & Workarounds

<!-- Document any known issues and their workarounds here -->

1. **Issue**: [Description of known issue]
   **Workaround**: [How to work around it]

## Changelog

### Version 1.0.0 ({{DATE}})
- Initial skill implementation
- Basic CRUD operations
- Authentication flow
- Error handling

## Notes

- This skill was generated from a template and may need customization
- Selectors should be verified against the current UI
- API endpoints should be confirmed with official documentation
- Test all operations in a safe environment before production use
- Report any issues to the Canifi community

## Related Skills

<!-- List related skills that work well with this one -->

- [Related Skill 1]
- [Related Skill 2]
- [Related Skill 3]
