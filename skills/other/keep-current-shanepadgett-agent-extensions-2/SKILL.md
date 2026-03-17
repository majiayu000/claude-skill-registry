---
name: keep-current
description: Research current online documentation and information. Use when working with external libraries, frameworks, APIs, services, version-specific issues, trends, or any topic where LLM training cutoff may impact accuracy. Guides when to use websearch, codesearch, or webfetch.
---

# Keep Current

Ensure responses are accurate and up-to-date by doing targeted research (use helper agents when available) before answering.

## When to Research

Research when working with:

- **External dependencies**: Libraries, frameworks, languages, SDKs
- **External services**: APIs, SaaS products (WorkOS, Stripe, morphllm, etc.)
- **Version-specific topics**: Migration guides, breaking changes, version compatibility
- **Time-sensitive topics**: Recent developments, trends, "latest" features, deprecations
- **Uncertain knowledge**: When not confident in the recency of your answer

## What NOT to Research

Skip research for:

- **Language basics**: Syntax, core operators, standard data structures
- **Stable APIs**: Well-established features that rarely change
- **Universal concepts**: Programming patterns, algorithms, design principles
- **Confident knowledge**: When certain the answer is in your knowledge base and unchanged
- **General knowledge**: Topics that don't depend on recent changes

**Rule of thumb**: If it's core programming knowledge that hasn't changed in years, don't research it.

## Research Assistance

When research is needed, use available research assistance (for example, a general-purpose research agent) to gather up-to-date information:

### Provide Context

Include in your prompt:
- **The research question**: What specific information is needed
- **Context**: What you're building, version requirements, language/framework
- **Scope**: Level of detail needed (high-level overview vs deep dive)
- **Constraints**: Any specific requirements or limitations

### Emphasize Thoroughness

The subagent must:
- Continue researching until it has a **complete, confident understanding**
- Explore multiple sources (official docs, community discussions, examples)
- Verify information across sources
- Not return until it has thoroughly researched the topic
- Provide distilled findings with source URLs

### Example Prompt

```
I need to integrate WorkOS for authentication in a Next.js app.
Research the current WorkOS documentation to understand:
- Integration setup and configuration
- SDK usage and code examples
- Authentication flow implementation
- Common patterns and best practices

Thoroughly research this topic. Do not return until you have a complete understanding of how to integrate WorkOS based on current documentation. Provide distilled findings with source URLs.
```

### Using Subagent Results

- The subagent returns distilled, synthesized information
- Apply findings to the user's request
- Reference sources when appropriate
- If findings are insufficient, ask for more specific research
