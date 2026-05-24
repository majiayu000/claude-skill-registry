---
name: uni-research
description: |
  Research tools via uni CLI. Use when user wants to search the web, find academic papers, browse Reddit, read Hacker News, or look up Wikipedia.
  Services: exa (web search), arxiv (papers), reddit, hn (Hacker News), wiki (Wikipedia).
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Research Tools (uni)

Free APIs, no auth required.

## Web Search (exa)

```bash
uni exa search "React 19 features"
uni exa search "TypeScript best practices" --num 10
uni exa code "Express.js middleware"         # Code docs
uni exa code "Python pandas groupby" --tokens 10000
uni exa research "AI agent frameworks 2025"  # Deep research
uni exa research "microservices" --mode deep
uni exa company "Anthropic"                  # Company info
```

## Academic Papers (arxiv)

```bash
uni arxiv search "transformer attention"
uni arxiv search "machine learning" -n 5
uni arxiv paper 2401.12345              # Get paper details
uni arxiv recent cs.AI                  # Recent in category
uni arxiv recent --list                 # List categories
```

Common categories: `cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`, `stat.ML`

## Reddit

```bash
uni reddit hot programming              # Hot posts
uni reddit new askscience               # New posts
uni reddit top rust --time week         # Top (hour/day/week/month/year/all)
uni reddit search "ai agents"           # Search all
uni reddit search "typescript" -r programming  # Search subreddit
uni reddit post <id>                    # Post with comments
```

## Hacker News (hn)

```bash
uni hn top                              # Top stories
uni hn new                              # New stories
uni hn best                             # Best stories
uni hn ask                              # Ask HN
uni hn show                             # Show HN
uni hn search "rust programming"        # Search
uni hn story <id>                       # Story with comments
```

## Wikipedia (wiki)

```bash
uni wiki "Alan Turing"                  # Summary
uni wiki search "quantum computing"     # Search
uni wiki random                         # Random article
uni wiki full "Rust (programming)"      # Full article
```
