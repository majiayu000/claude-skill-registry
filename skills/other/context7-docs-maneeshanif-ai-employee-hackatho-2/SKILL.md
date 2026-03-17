---
name: context7-docs
description: Fetches up-to-date documentation for technologies used in the Personal AI Employee project via Context7 MCP server. Use when you need current API documentation, library references, code examples, or implementation guidance for any technology in the stack.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Context7 Documentation Skill

This skill provides access to up-to-date documentation for all technologies used in the Personal AI Employee project through the Context7 MCP server.

## Supported Technologies

### Core Stack
| Technology | Context7 Library ID | Purpose |
|------------|---------------------|---------|
| Python | `python/cpython` | Core language |
| Claude Code | `anthropics/claude-code` | AI reasoning engine |
| Anthropic SDK | `anthropics/anthropic-sdk-python` | Claude API integration |

### Automation & Monitoring
| Technology | Context7 Library ID | Purpose |
|------------|---------------------|---------|
| Playwright | `microsoft/playwright-python` | Browser automation (WhatsApp) |
| Watchdog | `gorakhargosh/watchdog` | Filesystem monitoring |
| PM2 | `unitech/pm2` | Process management |

### APIs & Integrations
| Technology | Context7 Library ID | Purpose |
|------------|---------------------|---------|
| Gmail API | `googleapis/google-api-python-client` | Email integration |
| Google Auth | `googleapis/google-auth-library-python` | OAuth authentication |

### Data & Utilities
| Technology | Context7 Library ID | Purpose |
|------------|---------------------|---------|
| PyYAML | `yaml/pyyaml` | YAML parsing (frontmatter) |
| Requests | `psf/requests` | HTTP requests |
| Python-dotenv | `theskumar/python-dotenv` | Environment variables |

### MCP & Agent Framework
| Technology | Context7 Library ID | Purpose |
|------------|---------------------|---------|
| MCP SDK | `modelcontextprotocol/python-sdk` | MCP server development |
| FastMCP | `jlowin/fastmcp` | Quick MCP servers |

## Usage

### Via MCP Tool Call
When you need documentation, use the Context7 MCP tools:

```
1. resolve-library-id - Find the correct library ID
2. get-library-docs - Fetch documentation for a library
```

### Quick Reference
```bash
# Example: Get Playwright docs for browser automation
context7_resolve "playwright python"
context7_docs "/microsoft/playwright-python" --topic "browser automation"
```

## Documentation Cache

Fetched documentation is cached in:
```
/Vault/Docs/
├── python/
├── playwright/
├── gmail-api/
└── mcp/
```

## Reference

For detailed usage patterns, see [reference.md](reference.md)

For examples, see [examples.md](examples.md)
