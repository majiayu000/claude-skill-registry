---
name: enhancing-authors
description: Enhance author profiles by filling missing fields. Use when asked to "enhance author", "complete author profile", "find author info", or "update author details". Fills bio, avatar, website, and social links via parallel web research.
allowed-tools: Read, Write, Edit, Bash, WebFetch, Glob, Grep, Task, TaskOutput, WebSearch, AskUserQuestion
---

# Enhancing Author Profiles

This skill fills in missing author profile fields (bio, avatar, website, socials) via web research.

## Workflow Overview

```text
Phase 1: Author Identification
   └─ Find and validate author file

Phase 2: Parallel Research (for missing fields only)
   ├─ WebSearch agent 1: bio/background
   ├─ WebSearch agent 2: avatar URL
   └─ WebSearch agent 3: website + socials

Phase 3: User Review (BLOCKING GATE)
   └─ Present findings, await approval

Phase 4: Save Enhanced Author
   └─ Update frontmatter fields

Phase 5: Quality Check
   └─ Run pnpm lint:fix && pnpm typecheck
```

---

## Phase 1: Author Identification

### 1.1 Find the Author File

Accept an author slug, name, or partial name as argument:

1. **Try exact slug match first**: Check if `content/authors/{slug}.md` exists (convert spaces to hyphens, lowercase)
2. **If no exact match**: Use Grep to search for the name in author files:
   ```text
   Grep pattern: "name:.*{search term}" with glob: "content/authors/*.md"
   ```

**Outcomes:**
- Single match → proceed with that file
- Multiple matches → list options for user to choose
- No match → list available authors

### 1.2 Identify Missing Fields

Read the author file and check which fields are missing or empty:

**Required fields (always present):**
- `name`
- `slug`

**Optional fields to enhance:**
- `bio` - Professional background and expertise
- `avatar` - URL to profile picture
- `website` - Personal website URL
- `socials.twitter` - Twitter/X handle
- `socials.github` - GitHub username
- `socials.linkedin` - LinkedIn username
- `socials.youtube` - YouTube channel

A field is "missing" if:
- It doesn't exist in the frontmatter
- It exists but is empty (`""` or `null`)

If all fields are already populated, inform the user and offer to update specific fields.

---

## Phase 2: Parallel Research

Spawn **up to 3 WebSearch agents in parallel** based on what fields are missing:

```markdown
**Agent 1 - Bio/Background:**
Task tool with subagent_type: "general-purpose"
prompt: "Use WebSearch to find professional background info for [Author Name].
  Query: '[Author Name]' bio background expertise
  Extract: Job title, company, areas of expertise, notable projects.
  Return: A 1-2 sentence professional bio."

**Agent 2 - Avatar URL:**
Task tool with subagent_type: "general-purpose"
prompt: "Use WebSearch to find a profile picture URL for [Author Name].
  Query: '[Author Name]' site:github.com OR site:twitter.com
  Extract: GitHub username or Twitter handle to construct avatar URL.
  Return: Avatar URL (prefer GitHub format: https://github.com/{username}.png)"

**Agent 3 - Website & Socials:**
Task tool with subagent_type: "general-purpose"
prompt: "Use WebSearch to find social media profiles for [Author Name].
  Query: '[Author Name]' twitter github linkedin youtube
  Extract: Personal website, Twitter handle, GitHub username, LinkedIn profile, YouTube channel.
  Return: List of found profiles with URLs/handles."
```

Only spawn agents for missing fields. If bio already exists, skip Agent 1.

Collect all results via `TaskOutput` (blocking).

---

## Phase 3: User Review (BLOCKING GATE)

**This is a mandatory approval step.** Present the proposed changes before saving.

### 3.1 Present Changes

Display proposed updates as a comparison table:

```markdown
## Proposed Updates for [Author Name]

| Field | Current | Proposed |
|-------|---------|----------|
| bio | (empty) | "Founder of X, creator of Y..." |
| avatar | (empty) | "https://github.com/username.png" |
| website | (empty) | "https://example.com" |
| socials.twitter | (empty) | "username" |
| socials.github | (empty) | "username" |
| socials.linkedin | (empty) | "username" |
| socials.youtube | (empty) | (not found) |
```

### 3.2 Request Approval

Use the `AskUserQuestion` tool:

```yaml
question: "Save these changes to the author profile?"
header: "Review"
multiSelect: false
options:
  - label: "Save"
    description: "Update the author file with these values"
  - label: "Edit"
    description: "Tell me what to change"
  - label: "Cancel"
    description: "Don't modify the file"
```

### 3.3 Handle Response

- **Save**: Proceed to Phase 4
- **Edit**: Apply user feedback, show updated preview
- **Cancel**: Exit without changes

**Do NOT proceed to Phase 4 without explicit user approval.**

---

## Phase 4: Save Enhanced Author

### 4.1 Update Frontmatter

Use the Edit tool to update only the approved fields:

**Before:**
```yaml
---
name: "John Doe"
slug: "john-doe"
bio: ""
avatar: ""
website: ""
socials:
  twitter: ""
  github: ""
  linkedin: ""
  youtube: ""
---
```

**After:**
```yaml
---
name: "John Doe"
slug: "john-doe"
bio: "Software engineer specializing in distributed systems..."
avatar: "https://github.com/johndoe.png"
website: "https://johndoe.dev"
socials:
  twitter: "johndoe"
  github: "johndoe"
  linkedin: "johndoe"
  youtube: ""
---
```

### 4.2 Preserve Existing Values

**Critical:** Never overwrite existing non-empty values unless explicitly requested:
- Keep existing `name` and `slug` unchanged
- Only update fields that were empty/missing
- Preserve any additional custom fields

### 4.3 Confirmation

Report to user:
```markdown
Updated: content/authors/{slug}.md
  - bio: added
  - avatar: added
  - website: added
  - socials.twitter: added
  - socials.github: added
```

---

## Phase 5: Quality Check

Run linter and type check to catch any issues:

```bash
pnpm lint:fix && pnpm typecheck
```

If errors are found, fix them before completing the task.

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| Author not found | List available authors in `content/authors/` |
| No missing fields | Inform user, offer to update specific fields |
| WebSearch fails | Try alternative query patterns |
| User rejects changes | Allow editing or cancel |
| Could not find info | Mark field as "(not found)", proceed with others |

---

## Quality Checklist

Before saving, verify:
- [ ] Author file exists in `content/authors/`
- [ ] Only updating empty/missing fields
- [ ] Bio is 1-2 sentences, professional tone
- [ ] Avatar URL is valid (prefer GitHub format)
- [ ] Social handles are usernames only (no URLs)
- [ ] Existing non-empty values preserved
- [ ] User explicitly approved changes
