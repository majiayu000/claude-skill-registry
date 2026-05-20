---
name: workflow-research-codebase
description: This skill should be used when conducting comprehensive codebase research to answer questions, understand architecture, or prepare context for implementation planning. It spawns parallel sub-agents and synthesizes findings into a structured research document.
---

# Research Codebase Workflow

## Overview

Conduct comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings into a structured research document.

**Type:** FLEXIBLE - Adapt research depth and agent spawning to the complexity of the question.

**Output:** `research.md` with YAML frontmatter containing findings, code references, and architecture insights.

## When to Use

Use this workflow when:
- Exploring unfamiliar parts of a codebase
- Preparing context for implementation planning
- Understanding how existing features work
- Answering architectural questions
- Gathering context before creating PRDs or implementation plans

**Announce at start:** "I'm using the research-codebase workflow to investigate this thoroughly."

## Initial Setup

When this workflow is invoked, respond with:

```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```

Then wait for the user's research query.

## Steps to Follow

### Step 1: Read Directly Mentioned Files First

If the user mentions specific files (tickets, docs, JSON), read them FULLY first:
- Use the Read tool WITHOUT limit/offset parameters to read entire files
- **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
- This ensures you have full context before decomposing the research

### Step 2: Analyze and Decompose the Research Question

- Break down the user's query into composable research areas
- Take time to ultrathink about the underlying patterns, connections, and architectural implications
- Identify specific components, patterns, or concepts to investigate
- Create a research plan using todowrite to track all subtasks
- Consider which directories, files, or architectural patterns are relevant

### Step 3: Spawn Parallel Sub-Agent Tasks

Create multiple Task agents to research different aspects concurrently.

The key is to use these agents intelligently:
- Start with locator agents to find what exists
- Then use analyzer agents on the most promising findings
- Run multiple agents in parallel when they're searching for different things
- Each agent knows its job - just tell it what you're looking for
- Don't write detailed prompts about HOW to search - the agents already know

### Step 4: Wait and Synthesize

- **IMPORTANT**: Wait for ALL sub-agent tasks to complete before proceeding
- Compile all sub-agent results
- Prioritize live codebase findings as primary source of truth
- Connect findings across different components
- Include specific file paths and line numbers for reference
- Highlight patterns, connections, and architectural decisions
- Answer the user's specific questions with concrete evidence

### Step 5: Gather Metadata

Generate all relevant metadata:
- Filename: `research.md`
- Current date and time with timezone in ISO format
- Current commit hash via: `git rev-parse HEAD`
- Current branch via: `git branch --show-current`
- Repository name (infer from git remote or env)

### Step 6: Generate Research Document

Structure the document with YAML frontmatter followed by content:

```markdown
---
date: [Current date and time with timezone in ISO format]
researcher: opencode
git_commit: [Current commit hash]
branch: [Current branch name]
repository: [Repository name]
topic: "[User's Question/Topic]"
tags: [research, codebase, relevant-component-names]
status: complete
last_updated: [Current date in YYYY-MM-DD format]
last_updated_by: opencode
---

# Research: [User's Question/Topic]

**Date**: [Current date and time with timezone from step 5]
**Researcher**: opencode
**Git Commit**: [Current commit hash from step 5]
**Branch**: [Current branch name from step 5]
**Repository**: [Repository name]

## Research Question
[Original user query]

## Summary
[High-level findings answering the user's question]

## Detailed Findings

### [Component/Area 1]
- Finding with reference ([file.ext:line](link))
- Connection to other components
- Implementation details

### [Component/Area 2]
...

## Code References
- `path/to/file.py:123` - Description of what's there
- `another/file.ts:45-67` - Description of the code block

## Architecture Insights
[Patterns, conventions, and design decisions discovered]

## Open Questions
[Any areas that need further investigation]
```

### Step 7: Sync and Present Findings

- Present a concise summary of findings to the user
- Include key file references for easy navigation
- Ask if they have follow-up questions or need clarification

### Step 8: Handle Follow-Up Questions

If the user has follow-up questions:
- Append to the same research document
- Update the frontmatter fields `last_updated` and `last_updated_by`
- Add `last_updated_note: "Added follow-up research for [brief description]"`
- Add a new section: `## Follow-up Research [timestamp]`
- Spawn new sub-agents as needed for additional investigation
- Continue updating the document and syncing

## Important Notes

- Always use parallel Task agents to maximize efficiency and minimize context usage
- Always run fresh codebase research - never rely solely on existing research documents
- Focus on finding concrete file paths and line numbers for developer reference
- Research documents should be self-contained with all necessary context
- Each sub-agent prompt should be specific and focused on read-only operations
- Consider cross-component connections and architectural patterns
- Include temporal context (when the research was conducted)
- Link to GitHub/GitLab when possible for permanent references
- Keep the main agent focused on synthesis, not deep file reading
- Encourage sub-agents to find examples and usage patterns, not just definitions

## Critical Ordering

Follow the numbered steps exactly:
1. ALWAYS read mentioned files first before spawning sub-tasks (step 1)
2. ALWAYS wait for all sub-agents to complete before synthesizing (step 4)
3. ALWAYS gather metadata before writing the document (step 5 before step 6)
4. NEVER write the research document with placeholder values

## Frontmatter Consistency

- Always include frontmatter at the beginning of research documents
- Keep frontmatter fields consistent across all research documents
- Update frontmatter when adding follow-up research
- Use snake_case for multi-word field names (e.g., `last_updated`, `git_commit`)
- Tags should be relevant to the research topic and components studied

## Integration with Other Workflows

This workflow naturally flows into:
1. **workflow-create-prd** - Formalize requirements from research findings
2. **workflow-create-plan** - Create implementation plan using research as input
