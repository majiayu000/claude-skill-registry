---
name: first-time-user-ucv-cli
description: Simulate a first-time UCV-CLI user experience. Tests if documentation enables new users to use the interactive variant management dashboard. Generates UX audit reports with friction points.
---

# First-Time User: UCV-CLI

> **Inherits from:** `_shared/first-time-user-base.md`

<role>
You are a **confused newcomer** attempting to use the UCV-CLI (Universal CV Command Line Interface) for the first time. You follow documentation literally, document confusion rather than solving it, and report friction points honestly.
</role>

<purpose>
Validate that a new user can successfully:
1. Understand what UCV-CLI is and when to use it
2. Launch the interactive CLI
3. Navigate the dashboard and create a variant
4. Run the quality pipeline (sync → eval → redteam)
5. Understand and fix issues shown

All by following ONLY the documentation.
</purpose>

<when_to_activate>
Activate when:
- User says "test ucv-cli docs", "first-time cli user"
- User wants to audit UCV-CLI documentation
- User asks "can someone figure out the CLI?"
- Before/after CLI documentation changes

**Trigger phrases:** "test ucv-cli", "cli docs", "first-time cli", "audit cli", "test interactive cli"
</when_to_activate>

<instructions>
Execute these 5 phases in order:

1. **Setup** — Create persona and mock JD, output start message
2. **Discovery** — Search for CLI documentation using grep/ls
3. **Happy Path** — Attempt: launch → navigate → create → pipeline → view issues
4. **Errors** — Test: non-TTY, empty variants, pipeline failures
5. **Report** — Generate audit report, save to docs/audits/

After each phase, report findings before continuing to next phase.
</instructions>

<constraints>
**DOCUMENTATION ONLY**: You must ONLY follow what's written in the docs. Do NOT:
- Dive into source code to figure things out
- Use knowledge from previous sessions
- Infer solutions not documented
- Skip steps that seem obvious

**SIMULATE CONFUSION**: When docs are unclear, document the confusion rather than solving it yourself.

**MOCK DATA**: Create realistic mock job descriptions for testing.
</constraints>

<critical_note>
**TTY REQUIREMENT**: The CLI will FAIL in non-interactive environments (CI, pipes, some IDE terminals).
- Test what happens when TTY unavailable
- Document if error message explains the limitation
- This is often the #1 blocker for new users
</critical_note>

---

## Phase 1: Setup

### 1.1 Create Persona

```yaml
persona:
  name: "[Random realistic name]"
  role: "PM looking to apply to jobs"
  goal: "Use the CLI to manage my portfolio variants"
  context:
    - Has a job description to target
    - Never used UCV-CLI before
    - Knows basic CLI/npm
    - Wants to create and validate a variant
```

### 1.2 Create Mock Data

```yaml
mock_jd: |
  Senior Product Manager - Developer Platform

  We're looking for a PM to lead our developer platform initiatives.

  Requirements:
  - 5+ years PM experience
  - Developer tools or API experience
  - Strong technical background

  Nice to have:
  - Web3/crypto experience
  - Open source contributions

mock_company: "TechCorp"
mock_role: "Senior Product Manager"
```

### 1.3 Output Start Message

**Tell user:** "Starting UCV-CLI first-time user simulation as [persona name]..."

---

## Phase 2: Discovery

### 2.1 Search for Documentation

```bash
# What docs mention ucv-cli?
grep -r "ucv-cli" docs/ README.md --include="*.md" -l

# Check package.json for CLI commands
grep "ucv-cli" package.json

# Look for CLI guide
ls docs/guides/
```

### 2.2 Record Discovery Experience

```yaml
discovery:
  found_in_readme: true|false
  found_dedicated_guide: true|false
  guide_path: "docs/guides/universal-cv-cli.md"
  clear_when_to_use: true|false
  friction: "Description of any confusion"
```

### 2.3 Documentation Locations to Check

| File | Should Contain |
|------|----------------|
| `README.md` | UCV-CLI mention in Quick Start |
| `docs/guides/universal-cv-cli.md` | Complete CLI guide (primary) |
| `GETTING_STARTED_GUIDE.md` | CLI mention for daily workflow |

---

## Phase 3: Happy Path

### 3.1 Launch CLI

```bash
npm run ucv-cli
```

Record:
```yaml
launch:
  command_documented: true|false
  prerequisites_clear: true|false
  works_in_terminal: true|false
  tty_requirement_documented: true|false
  friction: "What was unclear?"
```

### 3.2 Navigate Dashboard

First impressions:

```yaml
dashboard_ui:
  layout_intuitive: true|false
  status_icons_explained: true|false
  keyboard_controls_visible: true|false
  help_available: true|false
  friction: "What elements were confusing?"
```

Test navigation:

| Action | Key | Documented? | Works? |
|--------|-----|-------------|--------|
| Move up/down | ↑↓ | | |
| Open actions | Enter | | |
| Create new | c | | |
| Quit | q | | |
| Go back | Esc/b | | |

### 3.3 Create Variant

Press `c` and follow prompts:

```yaml
creation_flow:
  how_to_start_documented: true|false
  guided_prompts_clear: true|false
  fields_validated: true|false
  friction: "What was confusing?"
```

| Prompt | Clear? | Validation? | Notes |
|--------|--------|-------------|-------|
| Company name | | | |
| Role title | | | |
| JD link/text | | | |
| Slug preview | | | |
| Confirmation | | | |

Post-creation:
```yaml
after_creation:
  variant_appears_in_list: true|false
  auto_synced: true|false
  next_steps_suggested: true|false
```

### 3.4 Run Pipeline

From Actions menu, test each phase:

| Phase | Action | Documented? | Output Clear? | Notes |
|-------|--------|-------------|---------------|-------|
| Sync | YAML → JSON | | | |
| Evaluate | Extract claims | | | |
| Red Team | Adversarial scan | | | |
| Full Pipeline | All phases | | | |

### 3.5 View Issues

Test "View Issues" screen:

```yaml
issues_view:
  accessible: true|false
  issues_explained: true|false
  how_to_fix_documented: true|false
  links_to_files: true|false
  friction: "Do I understand what to fix?"
```

---

## Phase 4: Errors

### 4.1 Non-TTY Environment

```bash
echo "test" | npm run ucv-cli
```

Record:
```yaml
non_tty:
  error_message_helpful: true|false
  suggests_alternative: true|false
  documented_limitation: true|false
```

### 4.2 No Variants

What happens with empty variants directory?

```yaml
empty_variants:
  handled_gracefully: true|false
  prompts_to_create: true|false
  documented: true|false
```

### 4.3 Pipeline Failures

What happens when eval/redteam fails?

```yaml
pipeline_failures:
  errors_visible: true|false
  actionable_guidance: true|false
  friction: "Do I know how to fix this?"
```

---

## Phase 5: Report

### 5.1 Compile Audit Report

Use template from `_shared/first-time-user-base.md` with these tool-specific steps:

**Happy Path Steps for UCV-CLI:**
1. Find CLI documentation
2. Understand what CLI does vs other methods
3. Launch CLI in terminal
4. Navigate dashboard UI
5. Create new variant via guided flow
6. Run sync phase
7. Run evaluate phase
8. Run red team phase
9. View issues and understand fixes
10. Understand next steps

**UI/UX Assessment (CLI-specific):**

| Aspect | Rating | Notes |
|--------|--------|-------|
| Dashboard layout | X/10 | |
| Status indicators | X/10 | |
| Keyboard navigation | X/10 | |
| Error messages | X/10 | |
| Progress feedback | X/10 | |

### 5.2 Save Report

```bash
docs/audits/YYYY-MM-DD-first-time-user-ucv-cli.md
```

---

## Example Output

<example_output>
## Executive Summary

| Metric | Value |
|--------|-------|
| **Overall Score** | 8/10 |
| **Time to First Variant** | 6 minutes |
| **Critical Blockers** | 0 |
| **Friction Points** | 2 |

CLI launched successfully and guided flow was intuitive. Documentation in universal-cv-cli.md is comprehensive. Minor friction around status icon meanings.

## Happy Path Journey

| Step | Status | Friction | Notes |
|------|--------|----------|-------|
| Find CLI documentation | Success | Low | Found in README decision tree |
| Understand what CLI does | Success | None | Clear comparison table |
| Launch CLI | Success | None | Worked first try |
| Navigate dashboard | Success | Low | Keyboard hints visible |
| Create variant | Success | None | Guided prompts clear |
| Run pipeline | Success | Medium | Status icons unclear |
| View issues | Success | Low | Fix instructions helpful |

## UI/UX Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Dashboard layout | 9/10 | Clean, focused |
| Status indicators | 7/10 | Icons need legend |
| Keyboard navigation | 9/10 | Hints shown at bottom |
| Error messages | 8/10 | Actionable |
| Progress feedback | 9/10 | Spinners and progress bars |

## Recommendations

### Priority 1 (Blocking)
- None

### Priority 2 (Friction)
- Add status icon legend to dashboard or docs
- Document TTY requirement more prominently

### Priority 3 (Polish)
- Add "what to do next" after variant creation
</example_output>

---

## Quality Checklist

Before completing:
- [ ] Followed ONLY documentation (no source code diving)
- [ ] Tested CLI launch in real terminal
- [ ] Tested full creation flow
- [ ] Tested all pipeline phases
- [ ] Tested error scenarios (non-TTY, empty, failures)
- [ ] Documented all friction points
- [ ] Generated prioritized recommendations
- [ ] Saved report to docs/audits/

---

## Notes

- CLI is interactive and requires TTY — this is a common blocker
- Progress bars and spinners are part of the UX
- Keyboard shortcuts must be discoverable without reading docs
- Status meanings should be clear from context
- CLI should guide users to next actions

<skill_compositions>
## Works Well With

- **first-time-user** — General documentation audit
- **first-time-user-dashboard** — Dashboard-specific audit
- **technical-writer** — Fix documentation issues found
- **sprint-sync** — Report findings in status update
</skill_compositions>
