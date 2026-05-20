---
name: jira-ticket-fetcher
description: This skill should be used when users need to fetch Jira ticket content using either a specific ticket ID (like RD-3891) or search for tickets by title/description. It defaults to searching within the current sprint but can extend to all tickets when needed. The skill uses the Jira CLI to retrieve ticket details, status, assignee, and descriptions.
---

# Jira Ticket Fetcher

## Overview

This skill enables fetching Jira ticket content using the Jira CLI. It supports retrieving specific tickets by ID or searching for tickets by text content, with configurable search scope (current sprint vs all projects).

## Quick Start

To fetch a Jira ticket, determine the input type:

1. **Ticket ID** (e.g., "RD-3891") → Use direct ticket retrieval
2. **Text Search** (e.g., "engine i18n epic") → Use search functionality

## System Dependencies

Before using this skill, ensure the following are installed:

- **uv** (https://github.com/astral-sh/uv) - Python package and project manager
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`
- **Python 3.x** (fallback if uv is not available)
- **jira-cli** (https://github.com/ankitpokhrel/jira-cli)
  - macOS: `brew install jira-cli`
  - Other: `go install github.com/ankitpokhrel/jira-cli/cmd/jira@latest`

### Authentication Setup

The Jira CLI requires authentication before use:

1. **Generate an API token:**
   - For Atlassian Cloud: https://id.atlassian.com/manage-profile/security/api-tokens
   - For local/on-premise server: Use your Jira password or PAT from your profile

2. **Set up authentication** (choose one method):
   - Export as environment variable: `export JIRA_API_TOKEN=your_token`
   - Use `.netrc` file with machine details
   - Run interactive setup: `jira init`

3. **Test authentication:** `jira me`

For detailed setup instructions: https://github.com/ankitpokhrel/jira-cli#getting-started

## Core Capabilities

### 1. Fetch Ticket by ID

Use when the user provides a specific ticket identifier:

```bash
# Primary (recommended)
uv run scripts/fetch_ticket.py RD-3891

# Alternative (if uv not available)
python scripts/fetch_ticket.py RD-3891
```

The script automatically detects ticket ID patterns (PROJECT-NUMBER format) and retrieves full ticket details including:
- Ticket key and summary
- Current status and assignee
- Issue type and creation dates
- Full description

### 2. Search Tickets by Text

Use when the user provides descriptive text or vague ticket references:

```bash
# Search in current sprint (default)
uv run scripts/fetch_ticket.py "engine i18n epic"

# Search across all projects
uv run scripts/fetch_ticket.py "engine i18n epic" all

# Alternative (if uv not available)
python scripts/fetch_ticket.py "engine i18n epic"
python scripts/fetch_ticket.py "engine i18n epic" all
```

Search functionality includes:
- Text matching in ticket summaries and descriptions
- Configurable search scope (current sprint vs all projects)
- Multiple result formatting options

## Workflow Decision Tree

1. **Is the input a ticket ID?** (Pattern: PROJECT-NUMBER)
   - Yes → Use `get_ticket_by_id()` function
   - No → Proceed to step 2

2. **Is the user looking for current sprint tickets only?**
   - Yes → Use `search_tickets_by_text()` with scope='current'
   - No → Use `search_tickets_by_text()` with scope='all'

3. **Handle errors gracefully**
   - Ticket not found → Suggest searching by text
   - No search results → Suggest broadening search scope
   - CLI errors → Check Jira CLI installation and authentication

## Implementation Details

### Script Functions

The `scripts/fetch_ticket.py` provides these key functions:

- `get_ticket_by_id(ticket_id)`: Retrieves specific ticket details
- `search_tickets_by_text(search_text, scope)`: Searches tickets by content
- `get_current_sprint_tickets()`: Gets all current sprint tickets
- `is_ticket_id(input_text)`: Validates ticket ID format

### CLI Usage

```bash
# Primary (recommended)
uv run scripts/fetch_ticket.py <ticket_id_or_search_text> [scope]

# Alternative (if uv not available)
python scripts/fetch_ticket.py <ticket_id_or_search_text> [scope]
```

- `<ticket_id_or_search_text>`: Either a ticket ID (e.g., RD-3891) or search text
- `[scope]`: Optional. Either `current` (default) or `all`

### Error Handling

The script includes comprehensive error handling for:
- Invalid ticket IDs or access permissions
- Network timeouts and connection issues
- JSON parsing errors
- Empty search results

### Output Formatting

Results are formatted for readability with:
- Emoji indicators for different fields
- Structured display of key ticket information
- Clear error messages with suggestions

## Resources

### scripts/
- `fetch_ticket.py`: Main Python script for Jira ticket operations
  - Handles ticket ID detection and validation
  - Implements search functionality with scope control
  - Provides formatted output and error handling
  - Includes timeout protection and JSON parsing

### references/
- `jira_cli_commands.md`: Comprehensive Jira CLI command reference
  - Core commands for ticket viewing and searching
  - Search patterns and filter examples
  - Output format specifications
  - Error handling best practices

## Usage Examples

### Example 1: Direct Ticket Lookup
```
User: "Show me ticket RD-3891"
→ Execute: uv run scripts/fetch_ticket.py RD-3891
→ Returns: Full ticket details with status, assignee, description
```

### Example 2: Text Search in Current Sprint
```
User: "Find the engine i18n epic"
→ Execute: uv run scripts/fetch_ticket.py "engine i18n epic"
→ Returns: Matching tickets from current sprint
```

### Example 3: Broad Search
```
User: "Search for all tickets about authentication"
→ Execute: uv run scripts/fetch_ticket.py "authentication" all
→ Returns: Matching tickets from all projects
```

## Prerequisites

- System dependencies installed (see [System Dependencies](#system-dependencies) section)
- Jira CLI authenticated (see [Authentication Setup](#authentication-setup) section)
- User must have appropriate Jira access permissions
