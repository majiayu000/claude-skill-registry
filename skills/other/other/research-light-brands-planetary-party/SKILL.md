---
name: research
description: "Use when current web info needed to avoid broken implementations"
version: 1.0.0
---

<philosophy>
Research when getting it right matters. When current information saves hours of debugging, ensures secure implementations, or guides you to the right abstraction—research first.
</philosophy>

<natural-triggers>
Clear signals that research is needed:
- Hitting an error that smells like an API change
- Implementing something security-critical (auth, payments, file handling)
- Making architecture decisions you'll live with for months
- Working with libraries you know evolve rapidly
- That moment of "wait, is this still how we do this?"
</natural-triggers>

<quick-check>
When: Mid-flow verification
Time: Under a minute

Examples: "Is useEffect still the way to handle this in React 18?", "Did Stripe change
their webhook payload?", "What's the current Node LTS version?"

Just search, grab the answer, keep coding. No storage, no ceremony, no permission
needed. </quick-check>

<deep-dive>
When: The decision really matters
Time: 5-15 minutes

Examples: Choosing between competing technologies, understanding a new architectural
pattern, debugging something that doesn't match documentation.

Always ask first: "This needs deeper research (5-15 min). Should I dig into this now?"
Let the user decide if they want to pause for research or continue with existing
knowledge.

Research thoroughly, save findings in research/[topic].md for team reference.
</deep-dive>

<tool-selection>
Always use the best available web search. Priority order:

MCP servers (preferred when available):

- Tavily MCP server
- Exa MCP server
- Other specialized search MCP servers

Built-in tools (fallback):

- Cursor: web_search tool
- Claude Code: Built-in web search

Tell the user which you're using:

- "Using Tavily MCP server for enhanced search capabilities"
- "Using Exa MCP server for code-focused research"
- "Using built-in web search (no MCP servers configured)"

This transparency helps users understand tool selection and configure MCP servers if
desired. </tool-selection>

<search-strategy>
Start with official sources - docs, changelogs, GitHub releases. Then expand to community discussions if needed.
</search-strategy>

<output-format>
Output should be scannable and actionable. Skip the fluff, get to what matters.

Good pattern:

## Stripe Checkout v4 Migration

Breaking change: redirectToCheckout() removed in v4

New pattern:

- Use Payment Element (unified UI)
- Or Checkout Sessions API (hosted page)

Migration: [Specific code example]

Source: Stripe docs v2024.11.15 </output-format>

<key-principles>
Recognize patterns: When you see version-specific errors, deprecated methods, or post-2023 technologies, that signals research is needed.

Be transparent: Say "I should verify this" or "Let me check current best practices"
rather than guessing.

Speed over perfection: For quick checks, first good answer wins. For deep dives,
thoroughness matters.

No unnecessary storage: Quick research lives in the conversation. Only save deep
research that others might reference. </key-principles>

<common-pitfall>
Don't research everything. If your React knowledge from 2023 still works and the user isn't hitting issues, just build. Research is a tool, not a crutch.
</common-pitfall>
