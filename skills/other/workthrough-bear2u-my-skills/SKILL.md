---
name: workthrough
description: Automatically document all development work and code modifications in a structured workthrough format. Use this skill after completing any development task, bug fix, feature implementation, or code refactoring to create comprehensive documentation.
license: MIT
---

This skill automatically generates detailed workthrough documentation for all development work, capturing the context, changes made, and verification results in a clear, structured format.

## When to Use This Skill

Use this skill automatically after:
- Implementing new features or functionality
- Fixing bugs or errors
- Refactoring code
- Making configuration changes
- Updating dependencies
- Resolving build/compilation issues
- Any significant code modifications

## Documentation Structure

The workthrough documentation follows this structure:

1. **Title**: Clear, descriptive title of the work completed
2. **Overview**: Brief summary of what was accomplished and why
3. **Changes Made**: Detailed breakdown of all modifications
4. **Code Examples**: Key code snippets showing important changes
5. **Verification Results**: Build/test results confirming success

## Implementation Guidelines

When generating workthrough documentation:

### 1. Capture Complete Context
- What problem was being solved?
- What errors or issues existed before?
- What approach was taken?
- Why were specific decisions made?

### 2. Document All Changes Systematically
- List each file modified with full paths
- Describe what changed in each file
- Include before/after code snippets for significant changes
- Note any dependencies added or removed
- Document configuration updates

### 3. Show Code Examples
Use clear, well-formatted code blocks:
```language
// file: src/path/to/file.tsx
<div className="example">
  {/* Show relevant code changes */}
</div>
```

### 4. Include Verification
- Build output showing success
- Test results
- Error messages (if any remain)
- Exit codes
- Screenshots (if relevant)

### 5. Use Clear Formatting
- Use markdown headers (##, ###)
- Use bullet points and numbered lists
- Use code blocks with syntax highlighting
- Use blockquotes for output/logs
- Keep paragraphs concise

## Document Organization

Save workthrough documents with this naming convention:
```
workthrough/YYYY-MM-DD-brief-description.md
```

Or organize by feature/project:
```
workthrough/feature-name/implementation.md
workthrough/bugfix/issue-123.md
```

## Example Workthrough Structure

```markdown
# [Clear Descriptive Title]

## Overview
Brief 2-3 sentence summary of what was accomplished.

## Context
- Why was this work needed?
- What was the initial problem/requirement?
- Any relevant background information

## Changes Made

### 1. [First Major Change]
- Specific modification 1
- Specific modification 2
- File: `path/to/file.tsx`

### 2. [Second Major Change]
- Specific modification 1
- File: `path/to/another-file.ts`

### 3. [Additional Changes]
- Dependencies added: `package-name@version`
- Configuration updates: `config-file.json`

## Code Examples

### [Feature/Fix Name]
```typescript
// src/path/to/file.tsx
const example = () => {
  // Show the key code changes
}
```

## Verification Results

### Build Verification
```bash
> build command output
✓ Compiled successfully
Exit code: 0
```

### Test Results
```bash
> test command output
All tests passed
```

## Next Steps
- Any follow-up tasks needed
- Known limitations or future improvements
```

## Automation Instructions

After completing ANY development work:

1. **Gather Information**
   - Review all files modified during the session
   - Collect build/test output
   - Identify the main objective that was accomplished

2. **Create Document**
   - Generate workthrough document in `workthrough/` directory
   - Use timestamp or descriptive filename
   - Follow the structure guidelines above

3. **Be Comprehensive**
   - Include all relevant details
   - Don't assume future readers have context
   - Document decisions and reasoning
   - Show concrete examples

4. **Verify Completeness**
   - Confirm all changes are documented
   - Include verification results
   - Add any relevant warnings or notes

## Quality Standards

Good workthrough documentation should:
- Be readable by other developers
- Provide enough detail to understand changes
- Include verification that changes work
- Serve as a reference for similar future work
- Capture important decisions and context

Avoid:
- Overly verbose descriptions
- Unnecessary technical jargon
- Missing verification steps
- Vague or unclear explanations
- Incomplete code examples

## Output Location

Unless specified otherwise, save workthrough documents to:
```
workthrough/YYYY-MM-DD-brief-description.md
```

Create the `workthrough/` directory if it doesn't exist.

## Integration with Workflow

This skill should be triggered automatically at the end of development sessions. The documentation serves as:
- A development log/journal
- Knowledge base for the project
- Onboarding material for new developers
- Reference for debugging similar issues
- Record of architectural decisions

Remember: Good documentation is a gift to your future self and your team.
