---
name: save-prd
description: Save PRD artifacts to epic directory after approval. Creates docs/epics/in-progress/{prefix}-{name}/ with prd.md, user-stories/, execution-plan.md, innovations-selected.md, and architecture-notes.md. Use when persisting approved PRD from /architect command.
---

# Save PRD Skill

> **ROOT AGENT ONLY** - Runs only from root Claude Code agent after HITL approval.

**Purpose:** Persist approved PRD artifacts to epic directory
**Trigger:** After hitl-approval phase completes in /architect workflow
**Input:** PRD content, user stories, execution plan, innovations, architecture notes
**Output:** Complete epic directory ready for /build execution

---

## Workflow

**1. Detect project prefix**

- Check git remote origin URL: `git remote get-url origin`
- Apply prefix mapping:

| Remote Contains       | Prefix |
| --------------------- | ------ |
| metasaver-marketplace | msm    |
| multi-mono            | mum    |
| rugby-crm / commithub | chc    |
| metasaver-com         | msc    |

- Fallback: Check folder name for matches
- Final fallback: Ask user for 3-letter prefix

**2. Auto-increment epic number**

- Scan both directories for existing epics:
  - `docs/epics/in-progress/`
  - `docs/epics/completed/`
  - `docs/epics/backlog/`
- Extract folders matching `{prefix}NNN-*` pattern
- Find highest number for the detected prefix
- Increment by 1
- Format: Zero-padded 3 digits (e.g., `007`)
- First epic for prefix starts at `001`

**3. Create epic directory**

- Generate directory name: `docs/epics/in-progress/{prefix}-{kebab-case-name}/`
- Example: `docs/epics/in-progress/msm-user-authentication-api/`
- Name derived from PRD title (lowercase, hyphens)
- Ensure `docs/epics/in-progress/` parent exists
- Create directory structure:
  ```
  {epic-dir}/
  ├── prd.md
  ├── user-stories/
  ├── execution-plan.md
  ├── innovations-selected.md  # Optional - only if innovations selected
  └── architecture-notes.md
  ```

**4. Save prd.md**

- Write PRD content to `{epic-dir}/prd.md`
- Include all sections:
  - Title, Overview, Goals
  - User Stories (summary list)
  - Success Criteria
  - Technical Requirements
  - Out of Scope
- Format: Markdown with proper headings

**5. Save user-stories/ directory**

- Create `{epic-dir}/user-stories/` subdirectory
- For each story, write individual file:
  - Filename: `{PROJECT}-{EPIC}-{NNN}-{slug}.md` (e.g., `msm-auth-001-user-login.md`)
  - Number: Zero-padded 3 digits
  - Slug: Derived from story title (kebab-case)
- Include in each story file:
  - Story ID, Title
  - Acceptance Criteria
  - Architecture annotations (files, imports, patterns)
  - Dependencies (if any)

**6. Save execution-plan.md**

- Write execution plan to `{epic-dir}/execution-plan.md`
- Include:
  - Total stories, total waves
  - Wave breakdown with dependencies
  - Agent assignments
  - Parallel execution pairs
  - Gantt-style task schedule
- Format: Markdown with tables and lists

**7. Save innovations-selected.md (conditional)**

- **Create only when:** User selected one or more innovations
- **Omit when:** No innovations selected by user
- File: `{epic-dir}/innovations-selected.md`
- Include:
  - List of selected innovations
  - Brief description of each
  - Impact on PRD (what changed)
- Format: Markdown with bullet lists

**8. Save architecture-notes.md**

- Write architecture validation notes to `{epic-dir}/architecture-notes.md`
- Include:
  - Multi-mono repo findings (existing solutions referenced)
  - Example files discovered
  - Context7 validation results
  - Patterns to follow
  - Files to create/modify
- Format: Markdown with code blocks and file paths

**9. Output final instruction**

- Return absolute path to PRD
- Tell user: `Run /build {absolute-path}/prd.md`
- Example: `Run /build /home/user/repo/docs/epics/in-progress/msm-user-auth/prd.md`

---

## Epic Number Detection Logic

```pseudocode
function getNextEpicNumber(prefix):
  folders = listDirectories("docs/epics/in-progress/")
  folders += listDirectories("docs/epics/completed/")
  folders += listDirectories("docs/epics/backlog/")

  existingNumbers = []
  for folder in folders:
    if folder matches pattern "{prefix}(\d{3})-.*":
      existingNumbers.append(extractNumber(folder))

  if existingNumbers is empty:
    return "001"

  maxNumber = max(existingNumbers)
  return zeroPad(maxNumber + 1, 3)
```

---

## File Creation Order

1. Detect project prefix from git remote
2. Scan for existing epic numbers
3. Create parent directory (`docs/epics/in-progress/{prefix}-{name}/`)
4. Create `user-stories/` subdirectory
5. Write `prd.md`
6. Write each `US-{NNN}-{slug}.md` file
7. Write `execution-plan.md`
8. Write `innovations-selected.md` (if applicable)
9. Write `architecture-notes.md`
10. Output instruction to user

---

## Directory Naming Rules

| Input PRD Title            | Project         | Generated Directory Name                               |
| -------------------------- | --------------- | ------------------------------------------------------ |
| "User Authentication API"  | metasaver-mktpl | `docs/epics/in-progress/msm-user-authentication-api/`  |
| "Dashboard Feature"        | multi-mono      | `docs/epics/in-progress/mum-dashboard-feature/`        |
| "Stripe Integration Setup" | rugby-crm       | `docs/epics/in-progress/chc-stripe-integration-setup/` |

**Rules:**

- Prefix: 3-letter project code (msm, mum, chc, msc)
- Name: Lowercase, words separated by hyphens
- Max name length: 50 characters (truncate if needed)
- Remove special characters except hyphens

---

## User Story Filename Examples

| Story ID     | Story Title             | Generated Filename                    |
| ------------ | ----------------------- | ------------------------------------- |
| msm-auth-001 | "User Authentication"   | `msm-auth-001-user-authentication.md` |
| msm-auth-002 | "Token Service"         | `msm-auth-002-token-service.md`       |
| chb-dash-015 | "Dashboard Widgets API" | `chb-dash-015-dashboard-widgets.md`   |

**Rules:**

- Story ID format: {PROJECT}-{EPIC}-{NNN} (e.g., msm-auth-001)
- Number: Zero-padded to 3 digits
- Slug: Derived from title (kebab-case)
- Max slug length: 40 characters

---

## Error Handling

**If directory with epic number exists:**

- This indicates a race condition or manual creation
- Increment to next available number
- Log warning about skipped number

**If prefix detection fails:**

- Prompt user: "Enter 3-letter project prefix (e.g., msm, mum, chc):"
- Validate: Exactly 3 lowercase letters
- Proceed with user-provided prefix

**If parent doesn't exist:**

- Create `docs/epics/in-progress/` directory first
- Then create epic directory

**If write fails:**

- Halt workflow
- Report error with file path
- Stop execution and wait for user intervention

---

## Integration

**Called by:**

- `/architect` command (Phase 7: Output)

**Calls:**

- File system operations (Write tool)
- Git operations (remote detection)
- No agent spawning required

**Next step:** User executes `/build {prd-path}`

---

## Example

```
Input:
  PRD Title: "User Authentication API"
  Project: metasaver-marketplace (detected from git remote)
  Stories: 5 enriched stories with architecture notes
  Execution Plan: 3 waves, 5 TDD pairs
  Innovations: 2 selected (passwordless auth, MFA)
  Architecture Notes: Multi-mono findings, Context7 validation

Save PRD Phase (this skill):
  1. Detect prefix: "msm" (from git remote containing "metasaver-marketplace")
  2. Scan docs/epics/in-progress/, docs/epics/completed/, docs/epics/backlog/
  3. Create directory: docs/epics/in-progress/msm-user-authentication-api/
  4. Write prd.md (all sections)
  5. Write user-stories/:
     - msm-auth-001-auth-schema.md
     - msm-auth-002-auth-service.md
     - msm-auth-003-token-service.md
     - msm-auth-004-login-endpoint.md
     - msm-auth-005-logout-endpoint.md
  6. Write execution-plan.md (3 waves, dependencies)
  7. Write innovations-selected.md (passwordless, MFA)
  8. Write architecture-notes.md (multi-mono, patterns)
  9. Output: "Run /build /home/user/repo/docs/epics/in-progress/msm-user-authentication-api/prd.md"

Result:
  docs/epics/in-progress/msm-user-authentication-api/
  ├── prd.md
  ├── user-stories/
  │   ├── msm-auth-001-auth-schema.md
  │   ├── msm-auth-002-auth-service.md
  │   ├── msm-auth-003-token-service.md
  │   ├── msm-auth-004-login-endpoint.md
  │   └── msm-auth-005-logout-endpoint.md
  ├── execution-plan.md
  ├── innovations-selected.md
  └── architecture-notes.md
```

---

## Notes

- This is a **WRITE skill** - creates files, does not modify existing ones
- Always run AFTER hitl-approval (user must approve before saving)
- Output structure matches PRD specification from architect-command-target-state.md
- **NO EXECUTION** - /architect is planning only, /build executes the PRD
- Epic numbers provide traceable project identifiers across repositories
