---
name: trello
description: Enables Claude to create, manage, and organize boards, lists, and cards in Trello via Playwright MCP
category: productivity
---

# Trello Skill

## Overview
Claude can manage your Trello boards to organize projects with visual Kanban boards, lists, and cards. Create workflows, track progress, and collaborate with team members.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/trello/install.sh | bash
```

Or manually:
```bash
cp -r skills/trello ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TRELLO_EMAIL "your-email@example.com"
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
- Create and manage boards
- Add and organize lists
- Create and edit cards
- Move cards between lists
- Add labels and due dates
- Assign members to cards
- Create checklists
- Attach files and links
- Add comments
- Set card covers
- Use Power-Ups
- Archive and delete cards

## Usage Examples

### Example 1: Create Card
```
User: "Add a card 'Review designs' to the In Progress list"
Claude: Opens board, navigates to In Progress list, creates card.
        Confirms: "Card 'Review designs' added to In Progress"
```

### Example 2: View Board
```
User: "What's on the project board?"
Claude: Opens board, reads all lists and cards.
        Reports: "Board has 4 lists: Backlog (12 cards),
        In Progress (3 cards), Review (2 cards), Done (8 cards)"
```

### Example 3: Move Card
```
User: "Move the 'API integration' card to Done"
Claude: Finds card, drags to Done list.
        Confirms: "Moved 'API integration' to Done"
```

### Example 4: Add Checklist
```
User: "Add a deployment checklist to the release card"
Claude: Opens card, adds checklist with items.
        Confirms: "Added checklist with 5 items"
```

## Authentication Flow
1. Claude navigates to trello.com via Playwright MCP
2. Enters TRELLO_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for board operations

## Selectors Reference
```javascript
// Board list
'.boards-page-board-section'

// List on board
'.list-wrapper'

// List title
'.list-header-name'

// Card in list
'.list-card'

// Add card button
'.open-card-composer'

// Card title input
'.list-card-composer-textarea'

// Add card submit
'.confirm'

// Card detail
'.card-detail-window'

// Checklist
'.checklist'

// Labels
'.card-label'

// Due date
'.due-date-badge'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Board Not Found**: List available boards, ask user
- **Card Create Failed**: Retry, verify list exists
- **Move Failed**: Refresh board, retry
- **Permission Denied**: Notify user of access issue

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Trello:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific board organization patterns
4. Note useful Power-Ups

## Notes
- Boards can be personal or team-owned
- Power-Ups extend functionality
- Butler for automation rules
- Labels for categorization
- Due dates with reminders
- Voting for prioritization
- Board templates available
- Integrates with many apps
