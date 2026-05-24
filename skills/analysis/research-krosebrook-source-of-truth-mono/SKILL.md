---
name: research
description:
  Web research skill for augmenting agent context with current information. Used when
  outdated information could lead to broken implementations or wasted effort.
---

# Research

## Core Philosophy

Research when **getting it right matters**. When current information saves hours of
debugging, ensures secure implementations, or guides you to the right
abstraction—research first.

## Natural Triggers

Clear signals that research is needed:

- Hitting an error that smells like an API change
- Implementing something security-critical (auth, payments, file handling)
- Making architecture decisions you'll live with for months
- Working with libraries you know evolve rapidly
- That moment of "wait, is this still how we do this?"

## Two Modes

### Quick Check

**When:** Mid-flow verification **Time:** Under a minute **Examples:**

- "Is `useEffect` still the way to handle this in React 18?"
- "Did Stripe change their webhook payload?"
- "What's the current Node LTS version?"

Just search, grab the answer, keep coding. No storage, no ceremony, no permission
needed.

### Deep Dive

**When:** The decision really matters **Time:** 5-15 minutes **Examples:**

- Choosing between competing technologies
- Understanding a new architectural pattern
- Debugging something that doesn't match documentation

**Always ask first**: "This needs deeper research (5-15 min). Should I dig into this
now?" Let the user decide if they want to pause for research or continue with existing
knowledge.

Research thoroughly, save findings in `research/[topic].md` for team reference.

## How to Research

### 1. Select Best Search Tool

Always use the best available web search. Priority order:

**MCP servers (preferred when available):**

- Tavily MCP server
- Exa MCP server
- Other specialized search MCP servers

**Built-in tools (fallback):**

- Cursor: `web_search` tool
- Claude Code: Built-in web search

**Tell the user which you're using:**

- "Using Tavily MCP server for enhanced search capabilities"
- "Using Exa MCP server for code-focused research"
- "Using built-in web search (no MCP servers configured)"

This transparency helps users understand tool selection and configure MCP servers if
desired.

### 2. Search Strategy

Start with official sources - docs, changelogs, GitHub releases. Then expand to
community discussions if needed.

### 3. Write Output

Output should be scannable and actionable. Skip the fluff, get to what matters.

## Output Style

### Do This

```markdown
## Stripe Checkout v4 Migration

**Breaking change**: `redirectToCheckout()` removed in v4

**New pattern**:

- Use Payment Element (unified UI)
- Or Checkout Sessions API (hosted page)

**Migration**: [Specific code example]

**Source**: Stripe docs v2024.11.15
```

### Not This

```markdown
After extensive research into the evolving landscape of payment processing... It's
important to note that Stripe has made significant changes... Let's dive into the
migration process...
```

## Real Examples

### Quick Check in Action

```
[User struggling with Vite error]
Agent: "That error usually means a Vite config issue. Let me check v6 changes..."
[30 seconds later]
Agent: "Found it—Vite 6 requires explicit `server.fs.allow` for parent directories. Adding it now."
```

### Deep Dive for Architecture

```
[User asking about state management for new project]
Agent: "State management in 2025 has some new players. Let me research current options for your scale..."
[10 minutes of research]
Agent: "For your use case (e-commerce, 50K users):
        - Zustand if you want simplicity (2KB, no boilerplate)
        - TanStack Store if you need framework agnostic
        - Redux Toolkit still solid for complex async flows

        Skip Redux unless you need time-travel debugging.
        Here's Zustand handling your cart state..."
```

## Key Principles

**Recognize patterns** - When you see version-specific errors, deprecated methods, or
post-2023 technologies, that signals research is needed.

**Be transparent** - Say "I should verify this" or "Let me check current best practices"
rather than guessing.

**Speed over perfection** - For quick checks, first good answer wins. For deep dives,
thoroughness matters.

**No unnecessary storage** - Quick research lives in the conversation. Only save deep
research that others might reference.

## Common Pitfall

Don't research everything. If your React knowledge from 2023 still works and the user
isn't hitting issues, just build. Research is a tool, not a crutch.
