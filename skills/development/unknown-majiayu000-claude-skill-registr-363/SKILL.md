---
name: analyze-issue
description: Analyze a GitHub issue and create detailed analysis in workflows/
argument-hint: <issue-number>
allowed-tools: Read, Grep, Glob, Write, Bash, mcp__github__get_issue
context: fork
agent: Explore
---

# Analyze Issue

Perform detailed analysis of a GitHub issue and write the analysis to the workflows directory.

## Instructions

1. **Fetch Issue Details**
   - Get issue #$ARGUMENTS from gittower/git-flow-next
   - Extract: title, description, labels, any linked issues

2. **Create Workflow Directory**
   - Create `workflows/issue-<number>-<slug>/`
   - Slug: lowercase, hyphenated version of key words from title (max 4 words)
   - Example: Issue #42 "Add squash merge support" → `workflows/issue-42-squash-merge/`

3. **Explore the Codebase**
   - Search for related code, files, and patterns
   - Identify affected components
   - Understand current implementation
   - Find similar patterns or prior art in the codebase

4. **Write Analysis Document**
   - Create `analysis.md` in the workflow folder
   - Use the template below

5. **Propose TODO Comments**
   - If specific code locations need attention, suggest TODO comments
   - Format: `// TODO(#<issue>): <description>`

## Analysis Template

Write to `workflows/issue-<number>-<slug>/analysis.md`:

```markdown
# Issue #<number>: <title>

## Summary
<1-2 sentence summary of the issue>

## Issue Details
- **Type**: <bug/enhancement/feature>
- **Labels**: <labels from GitHub>
- **Link**: <GitHub issue URL>

## Analysis

### Understanding
<What is being requested/reported? Clarify any ambiguity>

### Root Cause (for bugs)
<What's causing this behavior? Include file:line references>

### Affected Components
List all files/packages that will need changes:

- `cmd/<file>.go` - <why this file is affected>
- `internal/<package>/<file>.go` - <why>

### Current Behavior
<How does the system currently work in this area?>

### Proposed Solution
<High-level approach to solving this>

### Implementation Approach
<More detailed technical approach>

1. <Step 1>
2. <Step 2>
3. <Step 3>

### Edge Cases
- <Edge case 1 and how to handle it>
- <Edge case 2 and how to handle it>

### Testing Considerations
Based on TESTING_GUIDELINES.md:
- <Test case 1>
- <Test case 2>

### Documentation Impact
- [ ] Manpage updates needed?
- [ ] CONFIGURATION.md updates?
- [ ] README changes?

### Related Code References
<Key code snippets or file:line references that are relevant>

## Open Questions
- [ ] <Any clarifications needed from issue author>

## Next Steps
1. Create feature branch: `git flow feature start <number>-<slug>`
2. Create implementation plan: `/create-plan`
```

6. **Report Completion**
   - Show path to created analysis file
   - Summarize key findings
   - Suggest next step: create feature branch and run `/create-plan`
