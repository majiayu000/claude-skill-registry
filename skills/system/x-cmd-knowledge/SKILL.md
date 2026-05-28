---
name: x-cmd-knowledge
description: This skill provides access to various knowledge search tools through x-cmd CLI, including Hacker News, Wikipedia, DuckDuckGo search, RFC documents, Project Gutenberg books, and Stack Exchange. This skill should be used when users need to search for technical information, browse online knowledge bases, or access documentation from command line interfaces.
---

# x-cmd Knowledge Search Tools

## Overview

This skill provides comprehensive command-line access to major knowledge sources and search engines through the x-cmd ecosystem. The tools enable efficient information retrieval, technical documentation browsing, and knowledge discovery directly from the terminal.

## Available Tools

### Hacker News (hn)
Browse and search Hacker News content with interactive table interface.

- **Usage**: `x hn [subcommand]`
- **Key subcommands**:
  - `top` - Display top posts
  - `new` - Display new posts
  - `best` - Display best posts
  - `ask` - Display ask posts
  - `::` - Search with DuckDuckGo and AI assistance
- **Examples**:
  - `x hn` - View top posts
  - `x hn :: llama3` - Search for llama3 with AI assistance
  - `x hn top --json 11,20` - Get posts 11-20 in JSON format

### Wikipedia (wkp)
Search Wikipedia and extract article summaries.

- **Usage**: `x wkp [subcommand] [query]`
- **Key subcommands**:
  - `search` - Search Wikipedia pages
  - `extract` - Get article summaries
  - `suggest` - Get search suggestions
  - `:` - Search with DuckDuckGo
- **Examples**:
  - `x wkp search AI` - Search for AI articles
  - `x wkp extract OpenAI` - Get OpenAI summary
  - `x wkp suggest pythen` - Get spelling suggestions

### DuckDuckGo Search (ddgo)
Web search engine with AI-powered results.

- **Usage**: `x ddgo [query]`
- **Key subcommands**:
  - `--ai` - Use AI to select and summarize results
  - `--top N` - Get top N results
  - `dump --json` - Output results in JSON format
  - `init` - Configure proxy settings
- **Examples**:
  - `x ddgo bash` - Search for bash information
  - `x ddgo --ai bash` - AI-assisted bash search
  - `x ddgo --top 10 bash` - Get top 10 bash results

### RFC Documents (rfc)
Browse and search Internet RFC documents.

- **Usage**: `x rfc [subcommand]`
- **Key subcommands**:
  - `ls` - List all RFC documents
  - `txt` - Read RFC document content
  - `:` - Search RFC content
  - `::` - Search with AI summary
- **Examples**:
  - `x rfc ls` - List all RFCs
  - `x rfc 1003` - Read RFC 1003
  - `x rfc : csv` - Search for CSV-related RFCs

### Project Gutenberg Books (gtb)
Search and browse free ebooks from Project Gutenberg.

- **Usage**: `x gtb [subcommand]`
- **Key subcommands**:
  - `search` - Search books by keyword
  - `show` - View book details interactively
  - `txt` - Get book text content
  - `:` - Search with DuckDuckGo
- **Examples**:
  - `x gtb` - List all books
  - `x gtb search Dumas` - Search for Dumas books
  - `x gtb show 100` - View book ID 100

### Stack Exchange (se)
Search across Stack Exchange sites.

- **Usage**: `x se [subcommand] [query]`
- **Key subcommands**:
  - `search` - Search questions
  - `question` - Get question answers
  - `:` - Search with DuckDuckGo
  - `site` - View available sites
- **Examples**:
  - `x se search "how to use jq"` - Search for jq usage
  - `x se :au "how to use jq"` - Search Ask Ubuntu
  - `x se question 75261408` - Get question answers

## Installation and Setup

### Prerequisites
- x-cmd CLI installed
- Internet connection

### Configuration
Each tool supports configuration through:
- `init` - Interactive configuration setup
- `cfg` - Proxy and API endpoint configuration
- `cur` - Session default management

### Proxy Setup
For tools requiring proxy access:
```bash
x ddgo init  # Configure proxy for DuckDuckGo
x hn init    # Configure proxy for Hacker News
```

## Usage Patterns

### Quick Information Retrieval
- Use `x ddgo --ai` for AI-assisted search
- Use `x wkp extract` for quick summaries
- Use `x hn top` for latest tech news

### Technical Documentation
- Use `x rfc` for protocol specifications
- Use `x se` for programming questions
- Use `x gtb` for reference books

### Interactive Browsing
- Most tools support interactive table interfaces
- Use arrow keys for navigation
- Press `o` to open links in browser
- Press `u` to open user profiles

## Troubleshooting

### Common Issues
- **Network errors**: Check proxy configuration with `init` subcommand
- **No results**: Verify search query syntax
- **Permission errors**: Ensure x-cmd has network access

### Performance Tips
- Use `--json` flag for programmatic output
- Use `--top N` to limit results
- Configure data retention settings with `cfg` subcommand

## Integration

These tools can be combined with other x-cmd modules:
- Pipe output to `@zh` for Chinese translation
- Use with `x jq` for JSON processing
- Combine with `x curl` for advanced HTTP requests

## Support

For additional help:
- Visit: https://x-cmd.com
- Use `x [tool] --help` for specific tool documentation
- Check individual module pages for detailed usage

