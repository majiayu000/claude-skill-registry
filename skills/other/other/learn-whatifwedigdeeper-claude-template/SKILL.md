---
skill: learn
description: Extract lessons from conversation and persist to project configuration
trigger: |
  Suggest this skill when the conversation reveals:
  - Mistakes that had to be corrected
  - Undocumented dependencies or workarounds
  - Missing prerequisites discovered mid-task
  - Repeated manual processes that could be automated
  - Knowledge gaps about the codebase
---

# Learn from Conversation

Analyze the current conversation to extract lessons learned, mistakes made, or knowledge gaps discovered, then persist them to the project configuration.

## Process

### 1. Analyze Conversation

Review the entire conversation for:

**Mistakes & Corrections:**
- Commands that failed and had to be retried
- Missing prerequisites discovered mid-task
- Incorrect assumptions about the codebase
- Configuration issues encountered

**Knowledge Gaps:**
- Information Claude didn't know but should have
- Patterns that weren't documented
- Dependencies between systems not captured
- Environment setup requirements

**Workarounds Discovered:**
- Solutions to common problems
- Non-obvious configuration requirements
- Integration quirks between tools/libraries

**Process Improvements:**
- Steps that should be automated
- Checks that should happen earlier
- Prerequisites that should be validated first

### 2. Categorize Learnings

For each learning, determine where it belongs:

| Category | Destination | When to Use |
|----------|-------------|-------------|
| Project knowledge | CLAUDE.md | Facts about the codebase, patterns, conventions |
| Prerequisites | CLAUDE.md | Things that must be true before actions |
| Workflow automation | Skills | Multi-step processes Claude should suggest |
| User-initiated flow | Commands | Explicit workflows users will request |

### 3. Present Findings

Format findings as:

```
## Lessons Learned

### For CLAUDE.md
1. **[Section]**: [What to add/update]
   - Reason: [Why this was learned]
   - Suggested text: [Actual content to add]

### For Skills
1. **[Skill name]**: [What it would do]
   - Trigger: [When Claude should suggest it]
   - Reason: [Why this would help]

### For Commands
1. **[Command name]**: [What it would do]
   - Reason: [Why users would want this]
```

### 4. Confirm and Apply

For each learning:
1. Show the proposed change
2. Ask for confirmation
3. Apply the change if approved

**For CLAUDE.md updates:**
- Find the appropriate section
- Add new content or update existing
- Preserve existing structure and formatting

**For new skills/commands:**
- Create the file in the appropriate directory
- Follow existing patterns for format
- Update CLAUDE.md to document the new skill/command

### 5. Summary

After applying changes, show:
- Files modified
- New files created
- Sections updated in CLAUDE.md

## Examples of Learnable Patterns

**Missing Prerequisites:**
> "The tests failed because a required service wasn't running"
→ Add to CLAUDE.md: "Before running tests, ensure [service] is running"

**Undocumented Dependency:**
> "Library X doesn't work with tool Y without configuration"
→ Add to CLAUDE.md: Technical note about the workaround

**Repeated Manual Process:**
> "Every time I add a [file type], I have to create tests, run linting, run build..."
→ Create skill that automates this workflow

**Environment Issue:**
> "The build kept failing because a required variable wasn't set"
→ Add to CLAUDE.md: Required environment variables

## Guidelines

- **Be specific**: Include exact commands, file paths, and error messages
- **Be actionable**: Write content that directly helps future Claude sessions
- **Be minimal**: Only add what's truly useful, avoid over-documenting
- **Preserve structure**: Fit new content into existing CLAUDE.md organization
- **Avoid duplication**: Check if similar content already exists before adding
- **Protect sensitive data**: Before persisting to docs/config, redact secrets, credentials, tokens, private URLs, API keys, passwords, and customer data. Generalize examples to avoid exposing sensitive information.
