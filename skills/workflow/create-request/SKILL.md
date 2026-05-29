---
name: create-request
description: Create or update request documents. Auto-fills templates for new requests, updates progress based on implementation for existing ones.
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Create/Update Request Skill

## Trigger

- Keywords: create request, new request, write request, build request, update request, sync progress

## Modes

| Mode     | Trigger Condition             | Action                          |
| -------- | ----------------------------- | ------------------------------- |
| `create` | No file specified / new request | Gather info -> Fill template -> Create file |
| `update` | File specified / update request | Read current state -> Check implementation -> Update progress |

## When NOT to Use

- Viewing request structure (use request-tracking)
- Writing tech spec (use /tech-spec)
- Code development (use feature-dev)

---

## Create Mode Workflow

```
Phase 1: Gather    -> Collect feature, title, priority, requirements
Phase 2: Explore   -> Search related code + tech specs
Phase 3: Generate  -> Fill template + create file
Phase 4: Confirm   -> Display result + suggest next steps
```

## Create Mode: Interaction

If incomplete info, ask:

```
1. Feature area: Which feature? (e.g., auth, billing, notifications)
2. Title: Brief description
3. Priority: P0 (urgent) / P1 (high) / P2 (medium)
4. Background: Why is this needed?
5. Requirements: What needs to be done? (list)
6. Acceptance criteria: How do we know it's done?
```

---

## Update Mode Workflow

```
Phase 1: Load      -> Read existing request document
Phase 2: Analyze   -> Analyze Related Files + git changes
Phase 3: Map       -> Compare implementation with Acceptance Criteria
Phase 4: Update    -> Update Progress / Status / Checkboxes
Phase 5: Report    -> Output change summary
```

### Phase 2: Analyze Implementation Progress

```bash
# Get changes for Related Files from request document
git log --oneline --since="<created_date>" -- <related_files>

# Check test status
grep -r "describe\|it\(" test/ --include="*<feature>*"

# Check review status
git log --oneline --grep="codex-review" -- <related_files>
```

### Phase 3: Progress Mapping Rules

| Implementation Status               | Progress Update      |
| ------------------------------------ | -------------------- |
| Related Files have commits           | Development -> In Progress |
| Test files added/modified            | Testing -> In Progress |
| `/codex-review-fast` passed          | Development -> Done  |
| `/precommit` passed                  | Testing -> Done      |
| All Acceptance Criteria checked      | Acceptance -> Done   |

### Phase 4: Auto-Update Items

| Section               | Update Logic                              |
| --------------------- | ----------------------------------------- |
| `Status`              | Pending -> In Development -> Completed    |
| `Progress` table      | Update each phase status based on git changes |
| `Acceptance Criteria` | Check checkboxes based on implementation/test results |
| `Progress.Note`       | Add latest commit message summary         |

### Update Mode: Interaction

If confirmation needed, ask:

```
1. Confirm target request document path
2. Any manually completed items to check off?
3. Any blocked items to mark?
```

## File Naming

**Format**: `YYYY-MM-DD-kebab-case-title.md`

**Location**: `docs/features/{feature}/requests/`

## Verification

- File naming follows convention
- All template sections are filled
- Related file links are correct
- Acceptance criteria use checkboxes

## After Creation

Suggest next steps:

1. `/tech-spec` - Create technical specification
2. `/codex-architect` - Get architecture advice
3. Start implementation

## References

- `references/template.md` - Request template + naming convention

## Related Skills

| Skill              | Purpose                   |
| ------------------ | ------------------------- |
| `request-tracking` | Request structure knowledge base |
| `tech-spec`        | Tech spec writing         |
| `feature-dev`      | Development workflow      |

## Examples

### Create Mode

```
Input: /create-request Feature: Auth Title: Fix validation Priority: P1
Action: Explore related code -> Fill template -> Create file -> Suggest next steps
```

```
Input: Create a request document
Action: Ask for required info -> Explore -> Create -> Confirm
```

### Update Mode

```
Input: /create-request --update docs/features/auth/requests/2026-01-23-fix-login-validation.md
Action: Read request -> Analyze git changes -> Update Progress -> Output summary
```

```
Input: Update request progress
Action: Identify request from context -> Analyze implementation -> Auto-update -> Confirm
```

```
Input: (after development complete) Sync request document
Action:
  1. Read Related Files
  2. git log to check changes
  3. Update: Development unchecked -> done, Testing unchecked -> in progress
  4. Check completed Acceptance Criteria
  5. Status: Pending -> In Development
```
