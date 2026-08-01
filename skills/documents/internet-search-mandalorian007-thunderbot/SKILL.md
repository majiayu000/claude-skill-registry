---
name: internet-search
description: 'Search the internet using Perplexity API. Use for current information,
  news, or web research. Keywords: search, web, internet, perplexity, news, research.'
---

---
name: Internet Search
description: Search the internet using Perplexity API. Use for current information, news, or web research. Keywords: search, web, internet, perplexity, news, research.
---

# Internet Search

Web search powered by Perplexity API.

## Variables

- **SEARCH_CLI_PATH**: `.claude/skills/internet-search/search_cli/`

## Instructions

Run from SEARCH_CLI_PATH:
```bash
cd .claude/skills/internet-search/search_cli/
uv run search --help                # Discover usage
```

**Rules:**
- **Quote multi-word queries** - `uv run search "latest AI news"`
- **Use for current information** - training data has cutoff dates

## Troubleshooting

- **"PERPLEXITY_API_KEY not found"**: Run `/prime` to validate environment
