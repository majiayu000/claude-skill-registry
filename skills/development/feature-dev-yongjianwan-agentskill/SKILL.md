---
name: feature-dev
description: Comprehensive feature development workflow with specialized agents for codebase exploration, architecture design, and quality review
source: Converted from Claude plugin
license: See original LICENSE
---

# feature-dev

Comprehensive feature development workflow with specialized agents for codebase exploration, architecture design, and quality review

A comprehensive, structured workflow for feature development with specialized agents for codebase exploration, architecture design, and quality review. The Feature Development Plugin provides a systematic 7-phase approach to building new features. Instead of jumping straight into code, it guides you through understanding the codebase, asking clarifying questions, designing architecture, and ensuring quality—resulting in better-designed features that integrate seamlessly with your existing code. Building features requires more than just writing code. You need to: - **Understand the codebase** before making changes - **Ask questions** to clarify ambiguous requirements 

## When to Use This Skill

Use this skill when you need to:
- Comprehensive feature development workflow with specialized agents for codebase exploration, architecture design, and quality review

## How It Works

  ## Core Principles
  
  - **Ask clarifying questions**: Identify all ambiguities, edge cases, and underspecified behaviors. Ask specific, concrete questions rather than making assumptions. Wait for user answers before proceeding with implementation. Ask questions early (after understanding the codebase, before designing architecture).
  - **Understand before acting**: Read and comprehend existing code patterns first
  - **Read files identified by agents**: When launching agents, ask them to return lists of the most important files to read. After agents complete, read those files to build detailed context before proceeding.
  - **Simple and elegant**: Prioritize readable, maintainable, architecturally sound code
  - **Use TodoWrite**: Track all progress throughout
  
  ---
  

## Key Features

     - Target a different aspect of the codebase (eg. similar features, high level understanding, architectural understanding, user experience, etc)
     - "Find features similar to [feature] and trace through their implementation comprehensively"
     - "Map the architecture and abstractions for [feature area], tracing through the code comprehensively"
     - "Analyze the current implementation of [existing feature/area], tracing through the code comprehensively"
     - "Identify UI patterns, testing approaches, or extension points relevant to [feature]"

## Usage Example

```
# Mention "feature-dev" in your request
# Example: "Can you review this code using feature-dev?"
# Or: "Run feature-dev on this pull request"
```

## Implementation Notes

- **Original command**: feature-dev
- **Agents used**: 3
- **Conversion**: Automated from Claude plugin format
- **Limitations**: Some interactive features may be simplified

## For Best Results

1. Provide clear context and code snippets
2. Specify what aspects to focus on
3. Include any relevant guidelines or requirements
4. Be specific about the review scope

---

*Converted from Claude plugin on 2026-02-22*
