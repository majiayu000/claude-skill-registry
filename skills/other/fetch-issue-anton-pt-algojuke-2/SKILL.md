---
name: fetch-issue
description: Fetch Linear issue and create branch
argument-hint: <ALG-XX>
user-invocable: true
---

# Fetch Linear Issue and Create Branch

## Input

Linear issue identifier: $ARGUMENTS
Examples: `ALG-27`, `27`, `alg-27`

## Steps

1. Parse issue identifier from `$ARGUMENTS`:
   - Accept formats: `ALG-27`, `27`, `alg-27`
   - Normalize to `ALG-{NUM}` for Linear API call
   - Extract number for folder naming

2. Fetch issue details using Linear MCP:

   ```
   mcp__linear-server__get_issue with:
   - id: ALG-{NUM}
   - includeRelations: true
   ```

3. Extract from issue response:
   - `identifier`: e.g., "ALG-27"
   - `title`: Issue title
   - `description`: Full description
   - `labels`: Array of label names
   - `status`: Current status
   - `relations.blocks`: Issues this blocks
   - `relations.blockedBy`: Issues blocking this
   - `relations.relatedTo`: Related issues

4. Parse description for mentioned issues:
   - Search for patterns: `ALG-\d+` (case-insensitive)
   - Extract unique issue identifiers mentioned in description
   - These are treated as "linked" issues alongside formal relations
   - Example: `[ALG-13](https://linear.app/...)` -> extract `ALG-13`

5. For each linked issue (from relations AND description mentions):
   - Use Glob to find `specs/alg-{related-num}-*/spec.md` (Glob matches files, not directories)
   - If spec.md exists, read the summary section
   - Collect related specs for context

6. Derive kebab-slug from title:
   - Lowercase the title
   - Replace spaces and special chars with hyphens
   - Remove consecutive hyphens
   - Truncate to reasonable length (40 chars max)

7. Create branch and spec directory:

   ```bash
   NUM={extracted number}
   SLUG={kebab-slug}
   git checkout -b alg-${NUM}-${SLUG}
   mkdir -p specs/alg-${NUM}-${SLUG}
   ```

8. Output context summary:
   - Issue identifier and title
   - Description preview
   - Labels and status
   - Related specs found (with summaries)
   - Created branch name
   - Created spec directory path
   - Prompt: "Run /plan-spec to create the specification"

## Notes

- Do NOT create spec.md yet - that's handled by /plan-spec
- Do NOT commit anything - branch creation is uncommitted
- If branch already exists, ask user whether to switch to it or create fresh
- If spec directory already exists, warn user and ask to proceed
