---
name: issue
description: GitHub Issues + Project tracking. Use when creating, updating, or querying issues and managing the project board.
---

# GitHub Issues + Project

Issues live in `edochi/mdvs`. The project board is at `https://github.com/users/edochi/projects/2` (number 2, ID `PVT_kwHOA2NvhM4BQ-9Z`).

## Issue structure

Every issue follows this template:

```markdown
# Summary

One line or short paragraph.

# Changes

- Bullet list of concrete changes

# Description

Free-form, as detailed as needed.

## Sub-header
...

# Files

- `src/cmd/build.rs` — description
```

The Description section is optional but can be arbitrarily detailed with sub-headers.

## Metadata split

**On the issue (repo-level):**
- Title
- Body (template above)
- Labels — type only: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `perf`, `style`
- State: open / closed

**On the project (board-level):**
- Status: Todo / In Progress / Done (syncs with issue state automatically)
- Priority: high / medium / low

## Creating an issue

```bash
gh issue create --repo edochi/mdvs \
  --title "<title>" \
  --label "<type>" \
  --body "$(cat <<'EOF'
# Summary

...

# Changes

- ...

# Files

- ...
EOF
)"
```

The issue is auto-added to the project via the project's auto-add workflow.

## Setting priority on the project

After creating an issue, set its priority on the project board:

1. Get the project item ID:
```bash
gh project item-list 2 --owner edochi --format json --jq '.items[] | select(.content.number == <ISSUE_NUMBER>) | .id'
```

2. Set priority:
```bash
gh project item-edit --project-id "PVT_kwHOA2NvhM4BQ-9Z" \
  --id "<ITEM_ID>" \
  --field-id "PVTSSF_lAHOA2NvhM4BQ-9Zzg-8kwo" \
  --single-select-option-id "<OPTION_ID>"
```

Priority option IDs:
- high: `20a900f0`
- medium: `4fedbaba`
- low: `20cdb34f`

## Dependencies

Managed through GitHub issue relationships, not in the issue body. Use sub-issues or "tracked by" links in the project.

## Branch naming

Branches reference the issue number:

```
<issue-number>-<short-description>
```

Examples: `1-cargo-dist`, `5-enum-constraints`, `12-mdbook-site`

## Querying issues

```bash
gh issue list --repo edochi/mdvs                          # all open
gh issue list --repo edochi/mdvs --label feat              # by type
gh issue list --repo edochi/mdvs --state closed            # closed
gh issue view <number> --repo edochi/mdvs                  # single issue
```

## Closing an issue

```bash
gh issue close <number> --repo edochi/mdvs
```

The project's "Item closed" workflow auto-sets Status to Done.
