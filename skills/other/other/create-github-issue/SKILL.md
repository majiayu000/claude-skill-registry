---
name: create-github-issue
description: Research a bug, improvement, or feature request thoroughly, ask clarifying questions, then create a detailed GitHub issue with acceptance criteria.
allowed-tools: Task, TodoWrite, TaskOutput, AskUserQuestion, Bash, Read, Glob, Grep
---

# Create GitHub Issue Skill

**Transform a rough idea into a well-documented GitHub issue through deep research and clarifying questions.**

This skill is for creating issues, not implementing them. Focus on:
- **What** needs to happen (functionality)
- **Why** it matters (user value)
- **How to verify** it's done (acceptance criteria)

Do NOT include:
- Specific code changes
- Implementation details
- File paths to modify
- Technical approach

---

## Input Types

| Type | Examples |
|------|----------|
| **Bug** | "The theme toggle doesn't persist", "Animation flickers on mobile" |
| **Improvement** | "Make the site faster", "Add hover effects to links" |
| **Feature** | "Add a blog section", "Add dark mode support" |
| **Refactor** | "The components are inconsistent", "Hooks need cleanup" |

---

## Phase 1: Understand the Request

Parse the user's input to identify:

1. **Issue Type**: bug, enhancement, feature, refactor
2. **Affected Area**: Which part of the site? (pages, components, styling, scripts)
3. **Initial Scope**: How big does this seem? (small fix, medium feature, large epic)

---

## Phase 2: Deep Research

Spawn research subagents to understand the current state:

```
Task(Explore, model: opus, run_in_background: true):

Research the current state of [affected area] in the codebase.

Find:
- How does this feature/area currently work?
- What user flows are involved?
- Are there similar features we can reference?
- What are the current limitations or pain points?

Focus on FUNCTIONALITY, not implementation. We need to understand:
- What the user can currently do
- What the user experience is like
- Where the friction points are

DO NOT report file paths or code - report functional findings only.
```

For bugs, also research:
- Can we reproduce or understand the conditions?
- What is the expected vs actual behavior?
- What is the impact on users?

---

## Phase 3: Clarifying Questions

Based on research, identify gaps in understanding. Use `AskUserQuestion` to clarify:

**Always ask about:**
1. **Priority**: How urgent is this? (critical, high, medium, low)
2. **Scope confirmation**: "Based on my research, this seems to involve [X]. Is that correct?"
3. **Edge cases**: "What should happen when [edge case]?"
4. **Success criteria**: "How will we know this is working correctly?"

**For bugs, ask:**
- Steps to reproduce (if not clear)
- Frequency (always, sometimes, rarely)
- Workarounds available?

**For features/improvements, ask:**
- Who is the primary user?
- Are there similar features we should match?
- Any constraints or requirements?

**Example questions:**

```
AskUserQuestion(
  questions: [
    {
      question: "What priority should this issue have?",
      header: "Priority",
      options: [
        { label: "Critical", description: "Blocking users, needs immediate fix" },
        { label: "High", description: "Important, should be addressed soon" },
        { label: "Medium", description: "Should be done, but not urgent" },
        { label: "Low", description: "Nice to have, can wait" }
      ],
      multiSelect: false
    },
    {
      question: "Which areas are affected?",
      header: "Areas",
      options: [
        { label: "Pages", description: "The Next.js pages/routes" },
        { label: "Components", description: "React components" },
        { label: "Styling", description: "Tailwind/CSS styling" },
        { label: "Scripts", description: "Build or generation scripts" }
      ],
      multiSelect: true
    }
  ]
)
```

**Keep asking until you have clarity on:**
- [ ] The problem/opportunity is well understood
- [ ] The desired outcome is clear
- [ ] Success criteria are defined
- [ ] Edge cases are considered
- [ ] Priority and scope are confirmed

---

## Phase 4: Draft the Issue

Structure the GitHub issue using this template:

```markdown
## Summary

[1-2 sentences describing what this issue is about]

## Background

[Context: Why does this matter? What's the current situation?]

## User Story

**As a** visitor to wouterwisse.com
**I want** [goal/desire]
**So that** [benefit/value]

## Current Behavior (for bugs)

[What happens now that shouldn't happen, or doesn't happen that should]

## Expected Behavior

[What should happen after this is implemented]

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] [Edge case handling]
- [ ] [Error states are handled appropriately]

## Out of Scope

[Explicitly list what this issue does NOT cover to prevent scope creep]

## Notes

[Any additional context, constraints, or considerations]
```

### Acceptance Criteria Guidelines

Good acceptance criteria are:
- **Specific**: "User can toggle between light and dark mode" not "Theme works"
- **Testable**: Someone can verify yes/no if it's done
- **User-focused**: Describe what the user experiences, not technical details
- **Complete**: Cover happy path AND edge cases

Bad examples:
- "Fix the bug" (not specific)
- "Refactor the code" (not testable)
- "Use framer-motion" (technical, not user-focused)

Good examples:
- "When user clicks theme toggle, the entire site switches to dark mode"
- "If JavaScript is disabled, site displays in a sensible default state"
- "Loading state shows skeleton while images load"

---

## Phase 5: Create the Issue

Create the GitHub issue directly (can be edited later on GitHub if needed):

```bash
gh issue create \
  --title "[issue title]" \
  --label "[type]" \
  --label "[priority]" \
  --body "$(cat <<'EOF'
[issue body from Phase 4]
EOF
)"
```

### Label Mapping

| Type | Label |
|------|-------|
| Bug | `bug` |
| Feature | `enhancement` |
| Improvement | `enhancement` |
| Refactor | `refactor` |

| Priority | Label |
|----------|-------|
| Critical | `priority: critical` |
| High | `priority: high` |
| Medium | `priority: medium` |
| Low | `priority: low` |

---

## Phase 6: Report to User

```markdown
## Issue Created

**Issue**: #[number] - [title]
**URL**: [github url]
**Labels**: [labels]

### Next Steps

When ready to implement this issue:
1. Run `/next-github-issue` to pick up the oldest issue
2. Or run `/feature` with this issue's details

The issue is ready to be picked up.
```

---

## Progress Tracking

Use TodoWrite throughout:

```yaml
todos:
  - content: "Understand the request"
    status: completed
  - content: "Research current state"
    status: completed
  - content: "Ask clarifying questions"
    status: in_progress
  - content: "Draft and create GitHub issue"
    status: pending
```

---

## Key Principles

1. **Research first** - Understand before asking questions
2. **Ask good questions** - Don't assume, clarify
3. **Focus on functionality** - What, not how
4. **User-centric criteria** - Testable from user perspective
5. **No implementation details** - The codebase may change
6. **Well-labeled** - Type and priority for easy triage
7. **Just create it** - Issues can be edited on GitHub later
