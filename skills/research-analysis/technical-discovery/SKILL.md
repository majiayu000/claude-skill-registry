---
name: technical-discovery
description: Performs technical research and analysis without implementation. Use when asked to "analyze this", "research this change", "investigate", "what would be involved", "where would changes occur", "scope this work", "technical discovery", or before creating complex Trellis issues to understand the technical landscape.
allowed-tools:
  - Glob
  - Grep
  - LS
  - Read
  - WebFetch
  - WebSearch
  - TodoWrite
  - AskUserQuestion
  - mcp__perplexity-ask__perplexity_ask
  - mcp__task-trellis__get_issue
  - mcp__task-trellis__list_issues
---

# Technical Discovery

Perform technical research and analysis to understand a problem, question, or proposed change. Produce a comprehensive report without any code implementation.

## Goal

Investigate the codebase and relevant context to provide findings that inform decision-making or subsequent issue creation. This skill answers "what would be involved?" without actually doing the work.

## Required Inputs

- **Problem or Question**: Description of what to analyze (e.g., "How would we add user authentication?" or "Why is the API slow?")
- **Additional Context** (optional): Constraints, related issues, or specific areas to focus on

## When to Ask Questions

Use `AskUserQuestion` to clarify before proceeding when:

- The problem statement is too vague to research meaningfully
- Multiple interpretations exist and the correct one significantly affects the analysis
- You discover a decision point where user input would focus the research
- You need domain knowledge or context that isn't in the codebase

Ask focused questions early rather than making assumptions. One good clarifying question up front saves wasted research down the wrong path.

## Process

### 1. Understand the Request

Parse the problem or question to identify:

- **Core question**: What specifically needs to be answered?
- **Scope boundaries**: What's in scope vs. out of scope for this analysis?
- **Success criteria**: What would a useful answer look like?

### 2. Research the Codebase

Investigate relevant areas:

- **Find affected files**: Use Glob and Grep to locate code related to the problem
- **Read key files**: Understand current implementations, patterns, and conventions
- **Trace dependencies**: Follow imports and call chains to understand relationships
- **Check tests**: Review existing tests to understand expected behavior

### 3. Research External Context

When the problem involves libraries, APIs, or concepts outside the codebase:

- **Use Perplexity**: Query for up-to-date documentation, best practices, or known issues
- **Check documentation**: Fetch relevant docs via WebFetch if URLs are known
- **Search for solutions**: Look for common approaches to similar problems

### 4. Analyze Findings

Synthesize your research:

- **Identify patterns**: What approaches does this codebase already use for similar problems?
- **Locate change points**: Where would modifications likely occur?
- **Spot risks**: What could go wrong? What edge cases exist?
- **Note dependencies**: What other systems or components would be affected?

### 5. Formulate Recommendations

Based on your analysis:

- **Suggest approaches**: What are the viable options?
- **Compare tradeoffs**: What are the pros/cons of each approach?
- **Flag open questions**: What decisions need to be made?

## Output

Provide a structured report:

```
## Technical Discovery: [Brief Title]

### Summary
[2-3 sentence overview of findings and key takeaway]

### Problem Understanding
[Restate the problem/question as you understood it, including any scope assumptions]

### Findings

#### Codebase Analysis
- **Relevant Files**: [List key files with brief descriptions of their role]
- **Current Patterns**: [How does the codebase handle similar concerns today?]
- **Change Points**: [Where would modifications likely occur?]

#### External Research
[Relevant findings from Perplexity, documentation, or web searches—omit if not applicable]

### Impact Assessment
- **Components Affected**: [What parts of the system would be touched?]
- **Dependencies**: [What other systems or code depends on affected areas?]
- **Risks**: [Potential issues, edge cases, or concerns]

### Recommendations
[Suggested approaches with tradeoffs, or answers to the original question]

### Open Questions
[Decisions that need to be made or information still needed—omit if none]

### Files Reviewed
[Bulleted list of files examined during research]
```

## Guidelines

- **Evidence-based**: Support findings with specific file references and code observations
- **Neutral**: Present options objectively; let the user make decisions
- **Focused**: Stay within the scope of the original question
- **No implementation**: Do not write, edit, or create any code or files beyond this report
