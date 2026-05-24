---
name: share-plan
description: Use when sharing an implementation plan to a GitHub issue. Formats plans with collapsible details sections so issues are scannable but comprehensive.
argument-hint: "[#issue-number | new] [plan source or context]"
model: sonnet
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Share Plan

Format an implementation plan into a GitHub issue using collapsible `<details><summary>` sections. The issue stays scannable at a glance while preserving full implementation depth for whoever picks it up.

## Arguments

```
$ARGUMENTS
```

## Instructions

### 1. Identify the Plan

Find the implementation plan from one of these sources (in priority order):

1. **Explicit file path** in arguments -- read it directly
2. **Conversation context** -- extract from the current session's discussion

If no plan is found, stop and tell the user.

### 2. Determine Target

- **`#NNN` in arguments** -- update that existing issue
- **`new` in arguments** -- create a new issue (derive title from plan context or remaining args)
- **Neither** -- ask whether to update an existing issue or create a new one

**For existing issues:** fetch the body with `gh issue view NNN --json body,title`. Preserve the **Problem** and **Goal** sections if they exist -- only add/replace implementation sections.

### 4. Format the Issue Body

Structure the updated issue body using this template:

```markdown
## Problem

[Keep existing or write from plan context]

## Goal

[Keep existing or write from plan context]

## Approach

[High-level summary: 3-5 bullets max. What technology/pattern, why this approach,
key design decisions. This is the only section most readers will read.]

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `path/to/file` | Create/Edit | One-line purpose |

## Implementation

<details>
<summary>[Component or step name]</summary>

[Full implementation detail -- logic, pseudocode, config snippets, etc.]

</details>

<details>
<summary>[Another component]</summary>

[Details...]

</details>

<details>
<summary>Edge cases</summary>

[Known edge cases, limitations, things to verify during implementation]

</details>

## Notes

[Cross-references to related issues, links to plan files, etc. Optional.]
```

**Formatting rules:**
- Every `<details>` block needs a blank line after `<summary>` and before `</details>` for GitHub rendering
- Keep the **Approach** section above the fold -- no `<details>` wrapper
- Put code snippets, config examples, and step-by-step logic inside `<details>`
- Use the **Files** table as a quick-reference index
- Group implementation details by component, not by step number
- Edge cases always get their own `<details>` block

### 5. Publish

Commands will prompt for approval since they're not in `allowed-tools`.

**Update existing issue:**
```bash
gh issue edit NNN --body "$(cat <<'EOF'
...formatted body...
EOF
)"
```

**Create new issue:**
```bash
gh issue create --title "TITLE" --body "$(cat <<'EOF'
...formatted body...
EOF
)"
```

## Examples

```
/share-plan #108                              -> Format current plan into issue 108
/share-plan #108 from path/to/plan.md         -> Use specific plan file
/share-plan new tmux session naming           -> Create new issue with plan from conversation
/share-plan                                   -> Ask for target, use conversation context
```

## Anti-patterns

- Dumping raw plan prose without collapsible sections
- Hiding the approach summary inside a `<details>` block
- Overwriting Problem/Goal sections the user already wrote
- Creating a wall of text with no scannable structure
- Putting every sentence in its own `<details>` block (group by component)
