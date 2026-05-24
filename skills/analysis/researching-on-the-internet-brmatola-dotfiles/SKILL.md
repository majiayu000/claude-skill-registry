---
name: researching-on-the-internet
description: Use when planning features and need current API docs, library patterns, or external knowledge - gathers well-sourced, current information from the internet to inform technical decisions
---

# Researching on the Internet

## Overview

Gather accurate, current, well-sourced information from the internet to inform planning and design decisions. Test hypotheses, verify claims, and find authoritative sources for APIs, libraries, and best practices.

## When to Use

**Use for:**
- Finding current API documentation before integration design
- Testing hypotheses ("Is library X faster than Y?", "Does approach Z work with version N?")
- Verifying technical claims or assumptions
- Researching library comparison and alternatives
- Finding best practices and current community consensus

**Don't use for:**
- Information already in codebase (use codebase investigation)
- General knowledge within Claude's training (just answer directly)
- Project-specific conventions (check CLAUDE.md)

## Core Research Workflow

1. **Define question clearly** - specific beats vague
2. **Search official sources first** - docs, release notes, changelogs
3. **Cross-reference** - verify claims across multiple sources
4. **Evaluate quality** - tier sources (official → verified → community)
5. **Report concisely** - lead with answer, provide links and evidence

## Hypothesis Testing

When given a hypothesis to test:

1. **Identify falsifiable claims** - break hypothesis into testable parts
2. **Search for supporting evidence** - what confirms this?
3. **Search for disproving evidence** - what contradicts this?
4. **Evaluate source quality** - weight evidence by tier
5. **Report findings** - supported/contradicted/inconclusive with evidence
6. **Note confidence level** - strong consensus vs single source vs conflicting info

**Example:**
```
Hypothesis: "Library X is faster than Y for large datasets"

Search for:
✓ Benchmarks comparing X and Y
✓ Performance documentation for both
✓ GitHub issues mentioning performance
✓ Real-world case studies

Report:
- Supported: [evidence with links]
- Contradicted: [evidence with links]
- Conclusion: [supported/contradicted/mixed] with [confidence level]
```

## Quick Reference

| Task | Strategy |
|------|----------|
| **API docs** | Official docs → GitHub README → Recent tutorials |
| **Library comparison** | Official sites → npm/PyPI stats → GitHub activity |
| **Best practices** | Official guides → Recent posts → Stack Overflow |
| **Troubleshooting** | Error search → GitHub issues → Stack Overflow |
| **Current state** | Release notes → Changelog → Recent announcements |
| **Hypothesis testing** | Define claims → Search both sides → Weight evidence |

## Source Evaluation Tiers

| Tier | Sources | Usage |
|------|---------|-------|
| **1 - Most reliable** | Official docs, release notes, changelogs | Primary evidence |
| **2 - Generally reliable** | Verified tutorials, maintained examples, reputable blogs | Supporting evidence |
| **3 - Use with caution** | Stack Overflow, forums, old tutorials | Check dates, cross-verify |

Always note source tier in findings.

## Search Strategies

**Multiple approaches:**
- WebSearch for overview and current information
- WebFetch for specific documentation pages
- Check MCP servers (Context7, search tools) if available
- Follow links to authoritative sources
- Search official documentation before community resources

**Cross-reference:**
- Verify claims across multiple sources
- Check publication dates - prefer recent
- Flag breaking changes or deprecations
- Note when information might be outdated
- Distinguish stable APIs from experimental features

## Reporting Findings

**Lead with answer:**
- Direct answer to question first
- Supporting details with source links second
- Code examples when relevant (with attribution)

**Include metadata:**
- Version numbers and compatibility requirements
- Publication dates for time-sensitive topics
- Security considerations or best practices
- Common gotchas or migration issues
- Confidence level based on source consensus

**Handle uncertainty clearly:**
- "No official documentation found for [topic]" is valid
- Explain what you searched and where you looked
- Distinguish "doesn't exist" from "couldn't find reliable information"
- Present what you found with appropriate caveats
- Suggest alternative search terms or approaches

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Searching only one source | Cross-reference minimum 2-3 sources |
| Ignoring publication dates | Check dates, flag outdated information |
| Treating all sources equally | Use tier system, weight accordingly |
| Reporting before verification | Verify claims across sources first |
| Vague hypothesis testing | Break into specific falsifiable claims |
| Skipping official docs | Always start with tier 1 sources |
| Over-confident with single source | Note source tier and look for consensus |
