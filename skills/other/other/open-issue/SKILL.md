---
name: open-issue
description: Create GitHub issues from conversation context with proper formatting and tag selection
---

# Open Issue

This skill instructs AI agents on how to create GitHub issues from conversation context
with meaningful titles, proper formatting, and appropriate tag selection. The AI agent
should analyze the conversation, extract issue details, and confirm with the user before
creating the issue.

## Issue Format

GitHub issues created by this skill must follow this exact structure:

```markdown
# [prefix][tag]: A Brief Summary of the Issue

## Description

Provide a detailed description of this issue, including the related modules and the
problem statement.

## Steps to Reproduce

(Optional, only for bug reports)
Provide a minimized step to reproduce the bug.

## Proposed Solution

(Optional, but mandatory for [plan] issues)
Provide a detailed proposed solution or plan to address the issue.

- The plan SHOULD NOT include code audits! Code audits are part of the result of planning.
- The plan SHOULD include the related files to be modified, added, or deleted.

## Related PR

(Optional, but mandatory when Proposed Solution is provided)
This can be a placeholder upon creating the issue, however, once the PR is created,
update the PR# here.
```

## Tag Selection

A `git-msg-tags.md` file should appear in `{ROOT_PROJ}/docs/git-msg-tags.md` which
defines the tags related to the corresponding modules or modifications. The AI agent
**MUST** refer to this file to select the appropriate tag for the issue title.

If the file does not exist, reject the issue creation and ask the user to provide a
list of tags in `docs/git-msg-tags.md`.

### Tag Prefix Logic

The AI agent must determine which prefix and tag combination to use based on the issue type:

**Use `[plan][tag]` when:**
- The issue includes a "Proposed Solution" section
- The proposed solution outlines specific files to modify, add, or delete
- The tag is from `git-msg-tags.md` (e.g., `feat`, `sdk`, `bugfix`, `docs`, `test`, `refactor`, `chore`, `agent.skill`, `agent.command`, `agent.settings`, `agent.workflow`)
- Example: `[plan][feat]: Add TypeScript SDK template support`

**Use standalone `[tag]` when:**
- The issue is about a change but doesn't include implementation details
- It's a simple bug report or feature request without a plan
- The tag is from `git-msg-tags.md`
- Example: `[bugfix]: Pre-commit hook fails to run tests`

**Use `[bug report]`, `[feature request]`, or `[improvement]` when:**
- The issue doesn't fit standard git-msg-tags categories
- It's a high-level request without technical implementation details
- Example: `[feature request]: Add support for custom plugins`

## Inputs

The open-issue skill takes the following inputs:

1. **For [plan] issues**: A complete implementation plan from the `plan-guideline` skill
   - The plan should include all sections: Goal, Codebase Analysis, Interface Design, Test Strategy, and Implementation Steps
   - The plan becomes the "Proposed Solution" section of the issue

2. **For other issues**: Context from conversation about bugs, feature requests, or improvements
   - Issue description and details
   - Steps to reproduce (for bugs)
   - General requirements (for feature requests)

## Workflow for AI Agents

When this skill is invoked, the AI agent **MUST** follow these steps:

### 1. Context Analysis Phase

Review the conversation to determine issue type and extract details:

**For [plan] issues:**
- Check if a plan was already created using the `plan-guideline` skill
- If yes, use that plan directly as the "Proposed Solution"
- If no, inform the user to run `make-a-plan` first before creating a [plan] issue

**For other issues (bug reports, feature requests, improvements):**
- Identify the problem/request being discussed
- Extract key details: what, why, affected modules
- Determine the specific issue type

Context signals for issue type:
- Bug report signals: "doesn't work", "error", "crash", "unexpected", "broken"
- Feature request signals: "add", "new", "would be nice", "enhancement", "support for"
- Improvement signals: "refactor", "optimize", "clean up", "better way"

### 2. Tag Selection Phase

- Read `docs/git-msg-tags.md` to understand available tags
- Analyze the issue type and scope
- Apply the tag prefix logic described above
- If multiple tags could apply, choose the most specific one
- If the tag is ambiguous, ask the user to choose from 2-3 most relevant options

### 3. Issue Draft Construction

Build the issue following the format specification:

**Title:**
- Format: `[prefix][tag]: Brief Summary`
- Keep summary concise (max 80 characters for the summary portion)
- Ensure the summary clearly describes the issue

**Description section:**
- Provide detailed context about the issue
- Mention related modules or components affected
- Explain the problem statement clearly

**Steps to Reproduce section (only for bug reports):**
- Provide a minimized sequence of steps to reproduce the bug
- Be specific and actionable

**Proposed Solution section (mandatory for [plan] issues):**

**For [plan] issues:** Use the complete plan output from the `plan-guideline` skill:
- Copy the entire plan structure: Goal, Codebase Analysis, Interface Design, Test Strategy, and Implementation Steps
- The plan from `plan-guideline` already includes all necessary details:
  - Specific files to modify/create/delete with line ranges
  - Implementation steps in Design-first TDD order (Docs → Tests → Implementation)
  - LOC estimates and complexity assessment
  - Milestone strategy for large features
- **DO NOT** modify or rewrite the plan - use it as-is from `plan-guideline`

**For other issue types without a formal plan:**
- Provide a brief description of the proposed approach (if applicable)
- Keep it high-level for feature requests and improvements
- Not required for simple bug reports

**Related PR section (when Proposed Solution exists):**
- Add placeholder text: "TBD - will be updated when PR is created"
- Or reference existing PR if available

### 4. User Confirmation Phase

**CRITICAL:** The AI agent **MUST** display the complete issue draft to the user
and wait for explicit confirmation before creating the issue.

Present the draft in a clear format:
```
I've prepared this GitHub issue:

---
[Full issue content here]
---

Should I create this issue?
```

- Wait for explicit "yes", "confirm", "create it", or similar affirmative response
- If the user requests modifications, update the draft and present again
- If the user declines, abort issue creation gracefully

### 5. GitHub Issue Creation

Once confirmed, create the issue using the GitHub CLI:

```bash
gh issue create --title "TITLE_HERE" --body "$(cat <<'EOF'
BODY_CONTENT_HERE
EOF
)"
```

**Important:**
- Use heredoc (`<<'EOF' ... EOF`) to preserve markdown formatting
- The body should include all sections from Description onwards (not the title)
- After successful creation, display the issue URL to the user
- Confirm: "GitHub issue created successfully: [URL]"

### 6. Error Handling

Handle common error scenarios gracefully:

**Missing git-msg-tags.md:**
```
Cannot create issue: docs/git-msg-tags.md not found.
Please create this file with your project's tag definitions.
```

**GitHub CLI not authenticated:**
```
GitHub CLI is not authenticated. Please run:
  gh auth login
```

**No conversation context:**
```
I don't have enough context to create an issue. Could you please provide:
- What is the issue about?
- Is this a bug, feature request, or improvement?
- Any additional details or proposed solutions?
```

**Issue creation failed:**
```
Failed to create GitHub issue: [error message]
Please check your GitHub CLI configuration and try again.
```

## Ownership

The AI agent **SHALL NOT** claim authorship or co-authorship of the GitHub issue.
The issue is created on behalf of the user, who is **FULLY** responsible for its content.

Do not add any "Created by AI" or similar attributions to the issue body unless
explicitly requested by the user.

## Examples

### Example 1: Plan Issue with Feature Tag

**Context:** User wants to add a new feature. A plan was created using the `plan-guideline` skill.

**Issue:**
```markdown
# [plan][feat]: Add new feature name

## Description

Brief description of what the feature does and why it's needed.

## Proposed Solution

[The complete plan output from plan-guideline skill is inserted here]

See the `plan-guideline` skill documentation for detailed examples of plan structure,
including Goal, Codebase Analysis, Interface Design, Test Strategy, and Implementation Steps.

## Related PR

TBD - will be updated when PR is created
```

### Example 2: Bug Report

**Context:** User reports that pre-commit hooks are not running tests.

**Issue:**
```markdown
# [bug report]: Pre-commit hook fails to run tests

## Description

The pre-commit hook defined in `.git/hooks/pre-commit` is not executing the
test suite before allowing commits. This allows broken code to be committed.

## Steps to Reproduce

1. Make changes to any Python file in `claude/skills/`
2. Run `git add .`
3. Run `git commit -m "test"`
4. Observe that no tests are executed before the commit succeeds

## Related PR

TBD
```

### Example 3: Feature Request

**Context:** User requests support for custom plugin architecture.

**Issue:**
```markdown
# [feature request]: Add support for custom plugins

## Description

Add a plugin system that allows users to extend agentize functionality with
custom plugins. This would enable community contributions and custom workflows
without modifying core code.
```
