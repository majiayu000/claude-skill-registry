---
name: api-connector
description: Connect to REST APIs, manage authentication, and process responses. Use for API integration tasks.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
  - TodoWrite
  - AskUserQuestion
  - SlashCommand
  - Skill
  - NotebookEdit
  - BashOutput
  - KillShell
---

# api-connector - Claude Code Skill

Connect to REST APIs, manage authentication, and process responses. Use for API integration tasks.

## Configuration

This skill requires the following environment variables:

- `API_BASE_URL`: Base URL for API requests (default: https://api.example.com)
- `API_KEY`: API authentication key **(required)**
- `API_TIMEOUT`: Request timeout in milliseconds (default: 30000)

Set these in your environment or Claude Code configuration.

Connect to REST APIs, manage authentication, and process responses.

## Features

- Make GET, POST, PUT, DELETE requests
- Automatic authentication header management
- JSON response parsing
- Rate limiting and retry logic
- Response caching

## Configuration

**Required:**
- `API_KEY`: Your API authentication key

**Optional:**
- `API_BASE_URL`: Base URL (default: https://api.example.com)
- `API_TIMEOUT`: Timeout in ms (default: 30000)

## Usage

```
"Get data from /users endpoint"
"POST this JSON to /api/create"
"Check the API status"
```

## Safety

This extension operates in read-only mode:
- Cannot execute bash commands
- Cannot edit local files
- Cannot write files to disk

Only makes HTTP requests to configured API endpoints.

---

*This skill was converted from a Gemini CLI extension using [skill-porter](https://github.com/jduncan-rva/skill-porter)*
