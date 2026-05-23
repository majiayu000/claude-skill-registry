---
name: webresearcher
description: Also called "wr". Optional research agent for broad multi-source research without polluting context. Use when user requests it or when research needs depth across many sites.
---

# webresearcher

A research agent you can delegate broad research to. Keeps your context clean by doing synthesis externally.

## When to use

- User asks for it ("use wr", "use webresearcher")
- Query needs research across many sources with heavy synthesis
- You want to preserve your context window

Otherwise, WebSearch works fine.

## Usage

```bash
bunx webresearcher "detailed prompt briefing the agent"
bunx webresearcher --effort medium "complex topic"
```

## How to prompt it

Brief it like an agent:
- Explain what you're trying to understand
- Give context about why you need it
- Ask for specific details you care about

After it returns, feel free to use WebFetch/WebSearch yourself if you need to dig into specific references or confirm details.
