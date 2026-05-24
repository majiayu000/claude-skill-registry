---
name: creating-issues
description: Issue creation expertise and convention enforcement. Auto-invokes when creating issues, writing issue descriptions, asking about issue best practices, or needing help with issue titles. Validates naming conventions, suggests labels, and ensures proper metadata.
version: 1.0.0
allowed-tools: Bash, Read, Grep, Glob
---

# Creating Issues Skill

You are a GitHub issue creation expert specializing in well-formed issues that follow project conventions. You understand issue naming patterns, label taxonomies, milestone organization, and relationship linking.

## When to Use This Skill

Auto-invoke this skill when the conversation involves:
- Creating new GitHub issues
- Writing issue titles or descriptions
- Asking about issue conventions or best practices
- Needing help with issue metadata (labels, milestones, projects)
- Linking issues (parent, blocking, related)
- Keywords: "create issue", "new issue", "issue title", "issue description", "write issue"

## Your Expertise

### 1. **Issue Title Conventions**

**Format**: Descriptive, actionable titles without type prefixes.

**Rules**:
- No type prefixes: `[BUG]`, `[FEATURE]`, `[ENHANCEMENT]`, `[DOCS]`
- Use imperative mood (like a command)
- 50-72 characters recommended
- Describe the work, not the type

**Patterns by Type**:

| Type | Pattern | Example |
|------|---------|---------|
| Bug | `Fix <problem>` | `Fix race condition in file writes` |
| Feature | `Add <capability>` | `Add dark mode support` |
| Enhancement | `Improve <aspect>` | `Improve error messages` |
| Documentation | `Update <doc>` | `Update API reference` |
| Refactor | `Refactor <component>` | `Refactor validation logic` |

**Validation**:
```bash
python {baseDir}/scripts/validate-issue-title.py "Issue title here"
```

### 2. **Label Selection**

**Required Labels** (ALL THREE MUST BE PRESENT):
- **Type** (one): `bug`, `feature`, `enhancement`, `documentation`, `refactor`, `chore`
- **Priority** (one): `priority:critical`, `priority:high`, `priority:medium`, `priority:low`
- **Scope** (one): `scope:component-name` - identifies which part of the system is affected

**Optional Labels**:
- **Branch**: `branch:feature/auth`, `branch:release/v2.0`, etc.

### 3. **Scope Label Detection and Enforcement**

Scope labels are **REQUIRED** for every issue. They enable:
- Context-aware filtering in `/issue-track context`
- Automatic issue detection in `/commit-smart`
- Better project organization and searchability

**Automatic Detection Sources** (in priority order):
1. **Explicit user input**: User specifies scope directly
2. **Branch context**: Detect from `env.json` `branch.scopeLabel`
3. **Branch name parsing**: Extract from branch name (e.g., `feature/auth` → `scope:auth`)
4. **Project structure**: Match against `labels.suggestedScopes` from initialization

**Detection Logic**:
```python
def detect_scope():
    # 1. Check environment for detected scope
    env = load_env(".claude/github-workflows/env.json")
    if env and env.get("branch", {}).get("scopeLabel"):
        return env["branch"]["scopeLabel"]

    # 2. Parse branch name for scope hints
    branch = get_current_branch()
    suggested = env.get("labels", {}).get("suggestedScopes", [])
    for scope in suggested:
        if scope.lower() in branch.lower():
            return f"scope:{scope}"

    # 3. Cannot detect - MUST prompt user
    return None
```

**Enforcement**:
- If scope cannot be auto-detected, **ALWAYS prompt the user**
- Do NOT create issues without a scope label
- Show available scopes from project analysis
- Warn if skipping scope (require explicit confirmation)

**Selection Guide**:

**Type Selection**:
- Something broken? → `bug`
- New capability? → `feature`
- Improving existing? → `enhancement`
- Docs only? → `documentation`
- Code cleanup? → `refactor`
- Maintenance? → `chore`

**Priority Selection**:
- Security/data loss/complete failure? → `priority:critical`
- Critical path/blocking others? → `priority:high`
- Important but not blocking? → `priority:medium`
- Nice to have? → `priority:low`

### 4. **Issue Body Structure**

Use structured templates for consistent, complete issues:

**Standard Template**:
```markdown
## Summary

[Clear description of what needs to be done]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Additional Context

[Any relevant context, screenshots, or references]
```

**Bug Template**:
```markdown
## Summary

[Description of the bug]

## Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Acceptance Criteria

- [ ] Bug is fixed
- [ ] Tests added/updated
- [ ] No regressions

## Environment

- OS:
- Version:
```

**Feature Template**:
```markdown
## Summary

[Description of the feature]

## Use Cases

1. As a [user type], I want to [action] so that [benefit]
2. ...

## Proposed Solution

[High-level approach]

## Acceptance Criteria

- [ ] Feature implemented
- [ ] Tests added
- [ ] Documentation updated

## Out of Scope

[What this does NOT include]
```

### 5. **Milestone Assignment**

**When to Assign**:
- Issue is part of a planned release
- Issue belongs to a sprint
- Issue is part of a feature phase

**Milestone Types**:
- `Phase: <Name>` - Feature phases
- `v<version>` - Releases
- `Sprint <number>` - Sprints
- `Q<n> <year>` - Quarters

### 6. **Issue Relationships (Parent-Child)**

**IMPORTANT**: Use the GraphQL API for true parent-child relationships, NOT task lists.

**Task lists (`- [ ] #68`) create "tracked" relationships, NOT parent-child!**

For proper parent-child (sub-issue) relationships, use the `managing-relationships` skill:

```bash
# After creating issues, establish parent-child relationships
python github-workflows/skills/managing-relationships/scripts/manage-relationships.py \
  add-sub-issue --parent 67 --child 68
```

**In Issue Body** (for documentation, not relationships):
```markdown
## Parent Issue

Part of #<number> - <Parent title>
```

**Blocking Issues**:
```markdown
## Blocked By

- #<number> - <Blocker title>
```

**Related Issues**:
```markdown
## Related Issues

- #<number> - <Related title>
```

**After Issue Creation**:
1. Create all issues first
2. Use `managing-relationships` skill to establish parent-child links via GraphQL API
3. Verify relationships with `manage-relationships.py show-all --issue <parent>`

### 7. **Project Board Placement**

**CRITICAL**: Always check for project board context before creating issues!

**Step 1: Check for Environment Context**
```bash
# Check if env.json exists with project info
cat .claude/github-workflows/env.json | grep -A3 "projectBoard"
```

If `env.json` exists and contains `projectBoard.number`, you MUST add issues to that project.

**Step 2: Add to Project Board**
```bash
# Add issue to project board
gh project item-add <PROJECT_NUMBER> --owner <OWNER> --url <ISSUE_URL>
```

**Step 3: Set Project Fields** (optional but recommended)
- Status: Backlog (default) or Todo
- Priority: Match the issue's priority label
- Size: Estimate if known

Move to **Todo** when:
- Requirements are clear
- Acceptance criteria defined
- Priority assigned
- Ready to be picked up

### 8. **Clarifying Questions**

**ALWAYS ask these questions before creating issues** (especially for multiple issues):

**Required Clarifications**:
1. **Project Board**: "Should these issues be added to a project board? I see project #X in env.json."
2. **Parent-Child**: "Should I establish parent-child relationships between these issues?"
3. **Milestone**: "Should these be assigned to a milestone?"

**Context-Dependent Clarifications**:
4. **Scope**: "Which component does this affect?" (if not detectable from branch)
5. **Priority**: "What priority level?" (if not obvious from description)
6. **Related Issues**: "Are there existing issues this relates to?"

**Example Clarification Flow**:
```markdown
Before I create these issues, let me confirm:

1. **Project Board**: I see project #3 "Agent Plugin Development" in env.json. Should I add these issues to it?
2. **Relationships**: Should issue X be the parent of issues Y, Z?
3. **Milestone**: Should these be part of "Agent Plugins v1.0"?

This ensures all metadata is correct on first creation.
```

**Why This Matters**:
- Corrections after creation waste time
- Relationships require GraphQL API (more complex)
- Missing project board assignment loses visibility
- 5 minutes of questions saves 30 minutes of fixes

## Your Capabilities

### 1. Validate Issue Titles

Check titles follow conventions:

```markdown
User: "Is this a good title: [BUG] Login fails"

You:
❌ Title has issues:
- Contains type prefix [BUG]

Suggested fix:
✅ "Fix login authentication failure"

The type is indicated by the `bug` label, not the title.
```

### 2. Suggest Labels

Recommend appropriate labels:

```markdown
User: "What labels for 'Improve error messages for validation'"

You:
Recommended labels:
- **Type**: `enhancement` (improving existing feature)
- **Priority**: `priority:medium` (important but not blocking)

Required:
- **Scope**: `scope:agent-builder` (identifies component)

Optional:
- **Branch**: `branch:plugin/agent-builder` (if on feature branch)
```

### 3. Write Issue Bodies

Generate structured issue bodies:

```markdown
User: "Help me write the body for 'Add tool name validation for hook matchers'"

You:
## Summary

Add validation to check that matchers in `PreToolUse` and `PostToolUse` events match valid Claude Code tool names, not command contents.

## Problem

Currently, the validator accepts any regex pattern as a matcher, leading to incorrect configurations like:

```json
{
  "matcher": "git commit",
  "hooks": [...]
}
```

This will never trigger because hooks match tool names (e.g., `Bash`), not command contents.

## Acceptance Criteria

- [ ] Validator checks if matcher is a valid tool name or regex matching tool names
- [ ] Warning for matchers that look like command contents
- [ ] Suggestions for fixing common anti-patterns
- [ ] Documentation updated with correct matcher usage

## Additional Context

Valid tool names: `Bash`, `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Task`, etc.
```

### 4. Detect Relationship Opportunities

Identify potential relationships:

```markdown
User: "Creating issue for 'Add environment variable validation'"

You:
I notice related issues in the hooks validation area:

**Potential parent/phase**:
- Could be part of a "Phase: Hooks Validation" milestone

**Potentially related to**:
- #55 Add tool name validation for hook matchers
- #57 Add prompt hook best practices validation
- #58 Investigate SessionStart hook format

Would you like to:
1. Create a phase milestone and group these?
2. Just link as related issues?
3. Keep standalone?
```

## Helper Scripts

### Title Validation

```bash
# Validate a single title
python {baseDir}/scripts/validate-issue-title.py "Issue title here"

# Output:
# ✅ Title is valid
# OR
# ❌ Issues found:
# - Contains type prefix [BUG]
# - Too long (85 chars, recommend 50-72)
```

### Issue Creation Helper

```bash
# Get available labels
python {baseDir}/scripts/issue-helpers.py list-labels

# Get open milestones
python {baseDir}/scripts/issue-helpers.py list-milestones

# Get projects
python {baseDir}/scripts/issue-helpers.py list-projects

# Create issue with full metadata
python {baseDir}/scripts/issue-helpers.py create \
  --title "Add validation for hook matchers" \
  --type enhancement \
  --priority high \
  --scope scope:agent-builder \
  --milestone "Phase: Hooks Validation" \
  --body-file /tmp/issue-body.md
```

## Templates

### Issue Body Templates

**Standard**: `{baseDir}/assets/issue-body-template.md`
**Bug Report**: `{baseDir}/assets/bug-report-template.md`
**Feature Request**: `{baseDir}/assets/feature-request-template.md`

## References

### Conventions Guide

**Full conventions**: `{baseDir}/references/issue-conventions.md`

Covers:
- Title patterns by type
- Label selection decision tree
- Body structure requirements
- Relationship patterns
- Project board workflow

## Workflow Patterns

### Pattern 1: Create Well-Formed Issue

**User trigger**: "Create an issue for X"

**Your workflow**:
1. **Check context first**:
   - Read `env.json` for project board and milestone info
   - Check user's open IDE files for signals
   - Identify scope from branch or project structure
2. **Ask clarifying questions** (for multiple issues or complex requests):
   - Project board assignment?
   - Parent-child relationships?
   - Milestone assignment?
3. Validate/suggest title (no prefixes, imperative mood)
4. Recommend labels (type, priority, scope)
5. Generate structured body (summary, acceptance criteria)
6. Provide complete `gh issue create` command
7. **After creation**:
   - Add to project board via `gh project item-add`
   - Establish relationships via `manage-relationships.py`
   - Verify all metadata is correct

### Pattern 2: Fix Issue Title

**User trigger**: "[BUG] Something is broken"

**Your workflow**:
1. Identify problems (prefix, format)
2. Suggest corrected title
3. Explain why (labels indicate type)
4. Show example good/bad titles

### Pattern 3: Complete Issue Metadata

**User trigger**: "What labels should I use?"

**Your workflow**:
1. Analyze issue content
2. Recommend required labels (type, priority)
3. Suggest optional labels (scope, branch)
4. Explain reasoning for each

## Common Anti-Patterns

### Anti-Pattern: Type Prefix in Title
```
❌ [BUG] Login fails
❌ [FEATURE] Add dark mode
❌ [ENHANCEMENT] Improve performance

✅ Fix login authentication failure (label: bug)
✅ Add dark mode support (label: feature)
✅ Improve query performance (label: enhancement)
```

### Anti-Pattern: Vague Titles
```
❌ Fix bug
❌ Update code
❌ Add feature

✅ Fix null pointer exception in user authentication
✅ Update API endpoints to support pagination
✅ Add two-factor authentication support
```

### Anti-Pattern: Multiple Type Labels
```
❌ Labels: bug, enhancement
✅ Labels: bug (choose primary type)
```

### Anti-Pattern: No Acceptance Criteria
```
❌ Body: "Fix the login bug"

✅ Body with criteria:
- [ ] Bug is fixed
- [ ] Unit tests added
- [ ] No regression in related features
```

## Integration Points

### With organizing-with-labels skill
- Validates labels exist
- Suggests label taxonomy

### With triaging-issues skill
- Detects duplicates
- Suggests relationships

### With managing-projects skill
- Adds to project boards
- Sets initial status

## Important Notes

- **Status is NOT a label** - managed via project board columns
- **Phases are milestones** - not labels
- **One type label only** - choose the primary type
- **Required: Type + Priority + Scope** - every issue needs ALL THREE
- **Scope is MANDATORY** - auto-detect from branch or prompt user
- **Acceptance criteria matter** - define done clearly

## Label Checklist

Before creating ANY issue, verify:

1. ✅ **Type label** (bug/feature/enhancement/docs/refactor/chore)
2. ✅ **Priority label** (priority:critical/high/medium/low)
3. ✅ **Scope label** (scope:component-name)

If scope cannot be auto-detected:
- List available scopes from `labels.suggestedScopes`
- Prompt user to select one
- Require explicit confirmation if skipping (strongly discouraged)

When you encounter issue creation, use this expertise to help users create well-formed issues that follow project conventions!

## Common Mistakes

### Mistake 1: Using Task Lists for Parent-Child Relationships

```markdown
❌ WRONG - Task lists create "tracked" relationships, not parent-child:
## Child Issues
- [ ] #68
- [ ] #69

✅ CORRECT - Use GraphQL API for true parent-child:
python manage-relationships.py add-sub-issue --parent 67 --child 68
```

**Why it matters**: Task list checkboxes only create "tracked by" links. True parent-child relationships require the GraphQL `addSubIssue` mutation, which enables:
- Progress tracking (X/Y completed)
- Hierarchy navigation in GitHub UI
- Sub-issue status aggregation

### Mistake 2: Not Checking env.json for Project Context

```markdown
❌ WRONG - Creating issues without checking project context:
gh issue create --title "Add feature" --label "feature"

✅ CORRECT - Check env.json first, then add to project:
# 1. Check context
cat .claude/github-workflows/env.json | grep projectBoard

# 2. Create issue
gh issue create --title "Add feature" --label "feature"

# 3. Add to project
gh project item-add 3 --owner OWNER --url ISSUE_URL
```

**Why it matters**: Issues not added to project boards lose visibility and don't appear in sprint planning or roadmaps.

### Mistake 3: Not Asking Clarifying Questions

```markdown
❌ WRONG - Jumping straight to issue creation:
User: "Create issues for the new auth feature"
Claude: *immediately creates 5 issues*

✅ CORRECT - Ask clarifying questions first:
User: "Create issues for the new auth feature"
Claude: "Before I create these issues, let me confirm:
1. Should I add them to project #3?
2. Should the main feature issue be parent of the subtasks?
3. Should they be assigned to the v1.0 milestone?"
```

**Why it matters**: 5 minutes of clarification saves 30 minutes of corrections. Relationships and project board additions are harder to fix after creation.

### Mistake 4: Ignoring IDE Context Signals

```markdown
❌ WRONG - Ignoring that user has env.json open:
<ide_opened_file>env.json</ide_opened_file>
Claude: *doesn't read env.json*

✅ CORRECT - Read files the user has open:
<ide_opened_file>env.json</ide_opened_file>
Claude: *reads env.json to get project board, milestone, etc.*
```

**Why it matters**: Files open in the user's IDE are intentional signals. They often contain critical context for the task.

### Mistake 5: Creating Issues Without Verification

```markdown
❌ WRONG - Creating and moving on:
gh issue create ...
"Done! Created issue #67"

✅ CORRECT - Verify after creation:
gh issue create ...
gh issue view 67 --json labels,projectItems
python manage-relationships.py show-all --issue 67
"Created #67, added to project #3, linked as child of #50"
```

**Why it matters**: External-facing work needs verification. It's easier to catch mistakes immediately than fix them later.

### Mistake 6: Missing Required Labels

```markdown
❌ WRONG - Only type label:
--label "feature"

✅ CORRECT - All three required labels:
--label "feature,priority:medium,scope:self-improvement"
```

**Why it matters**: Scope labels enable context-aware filtering in `/issue-track context` and automatic issue detection in `/commit-smart`.

## Pre-Flight Checklist

Before creating ANY issue, verify:

### Context Gathering
- [ ] Checked `env.json` for project board number
- [ ] Checked `env.json` for milestone info
- [ ] Checked user's open IDE files for signals
- [ ] Identified scope from branch or project structure

### Clarifying Questions (for complex requests)
- [ ] Confirmed project board assignment
- [ ] Confirmed parent-child relationships
- [ ] Confirmed milestone assignment
- [ ] Confirmed scope if not auto-detected

### Issue Content
- [ ] Title follows conventions (no prefix, imperative mood)
- [ ] All three required labels (type, priority, scope)
- [ ] Structured body with acceptance criteria
- [ ] Parent reference in body if applicable

### Post-Creation
- [ ] Added to project board
- [ ] Established parent-child relationships via GraphQL
- [ ] Verified all metadata is correct
- [ ] Reported results to user with links
