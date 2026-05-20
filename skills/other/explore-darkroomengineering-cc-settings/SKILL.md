---
name: explore
description: |
  Codebase exploration and understanding. Use when the user asks:
  - "how does X work?", "where is X?", "find X", "understand X"
  - "what files handle X?", "show me the X implementation"
  - "navigate to X", "explore the codebase"
  - any question about code structure, architecture, or implementation details
context: fork
agent: explore
---

# Codebase Exploration

Delegates to the Explore agent for fast, read-only investigation of the codebase.

## Strategy

1. **Start broad** - Use `tldr semantic` or `Glob` to find relevant files
2. **Narrow down** - Read specific files to understand implementation
3. **Trace connections** - Use `tldr impact` to find callers/dependencies
4. **Summarize findings** - Return clear, actionable summary

## Output Format

Return a concise summary:
- **Location**: Key files and their paths
- **How it works**: Brief explanation of the flow
- **Key functions/components**: Entry points
- **Dependencies**: What it relies on
- **Suggestions**: If the user needs to modify something

## Remember

- You are READ-ONLY - do not modify files
- Return summaries, not raw file contents
- Be specific with file paths and line numbers
