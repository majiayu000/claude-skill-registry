---
name: first-time-user-dashboard
description: Simulate a first-time CV Dashboard user experience. Tests if documentation enables new users to generate and access the password-protected variant dashboard. Generates UX audit reports.
---

# First-Time User: CV Dashboard

> **Inherits from:** `_shared/first-time-user-base.md`

<role>
You are a **confused newcomer** attempting to use the CV Dashboard for the first time. You follow documentation literally, document confusion rather than solving it, and report friction points honestly.
</role>

<purpose>
Validate that a new user can successfully:
1. Understand what the CV Dashboard is
2. Generate the dashboard with their password
3. Access and use the dashboard in a browser
4. Navigate variants, filter, and download resumes

All by following ONLY the documentation.
</purpose>

<when_to_activate>
Activate when:
- User says "test dashboard docs", "first-time dashboard user"
- User wants to audit CV Dashboard documentation
- User asks "can someone figure out the dashboard?"
- Before/after dashboard documentation changes

**Trigger phrases:** "test dashboard", "dashboard docs", "first-time dashboard", "audit dashboard"
</when_to_activate>

<instructions>
Execute these 5 phases in order:

1. **Setup** — Create persona, output start message to user
2. **Discovery** — Search for dashboard documentation using grep/ls
3. **Happy Path** — Attempt: prerequisites → generate → access → use
4. **Errors** — Test: missing password, no variants
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

**NO REAL PASSWORDS**: Use mock passwords like "test123" for simulation.
</constraints>

---

## Phase 1: Setup

### 1.1 Create Persona

```yaml
persona:
  name: "[Random realistic name]"
  role: "PM/Developer who has variants generated"
  goal: "Access my CV Dashboard to manage job applications"
  context:
    - Has variants in content/variants/
    - Never used the dashboard before
    - Knows basic CLI/npm
    - Wants to share links with recruiters
```

### 1.2 Output Start Message

**Tell user:** "Starting CV Dashboard first-time user simulation as [persona name]..."

---

## Phase 2: Discovery

### 2.1 Search for Documentation

```bash
# What docs mention dashboard?
grep -r "dashboard" docs/ README.md --include="*.md" -l
grep -r "generate:dashboard" . --include="*.md" -l

# Check package.json for dashboard commands
grep "dashboard" package.json
```

### 2.2 Record Discovery Experience

```yaml
discovery:
  found_in_readme: true|false
  found_in_guides: true|false
  guide_path: "[path if found]"
  clear_entry_point: true|false
  friction: "Description of any confusion"
```

### 2.3 Documentation Locations to Check

| File | Should Contain |
|------|----------------|
| `README.md` | Dashboard mention in Quick Start |
| `GETTING_STARTED_GUIDE.md` | Dashboard setup section |
| `docs/guides/universal-cv-cli.md` | Dashboard integration |
| `scripts/generate-dashboard.ts` | Usage comment at top |

---

## Phase 3: Happy Path

### 3.1 Prerequisites Check

Document if these are clearly stated:
- [ ] Need `DASHBOARD_PASSWORD` env var?
- [ ] Need variants already generated?
- [ ] Need to run `npm install` first?

### 3.2 Generate Dashboard

```bash
DASHBOARD_PASSWORD=test123 npm run generate:dashboard
```

Record:
```yaml
generate:
  command_documented: true|false
  documented_in: "[file path]"
  result: "success|failure|confusion"
  output_path: "public/cv-dashboard/index.html"
  friction: "What was unclear?"
```

### 3.3 Access Dashboard

```bash
# Check if file was created
ls public/cv-dashboard/

# How to view? (npm run dev? open file? URL?)
```

Record:
```yaml
access:
  file_created: true|false
  how_to_view_documented: true|false
  url_documented: true|false
  friction: "How do I actually see this?"
```

### 3.4 Use Dashboard Features

Test each feature (if accessible):

| Feature | Documented? | Works? | Notes |
|---------|-------------|--------|-------|
| Password entry | | | |
| View variants list | | | |
| Filter by status | | | |
| Search variants | | | |
| Download resume | | | |
| View portfolio link | | | |
| Logout | | | |

---

## Phase 4: Errors

### 4.1 Missing Password

```bash
npm run generate:dashboard  # No password
```

Record:
```yaml
missing_password:
  clear_error_message: true|false
  suggests_fix: true|false
  error_text: "[actual error message]"
```

### 4.2 No Variants

What happens if `content/variants/` is empty?

```yaml
empty_variants:
  documented: true|false
  handled_gracefully: true|false
  error_or_empty_state: "[what shows]"
```

---

## Phase 5: Report

### 5.1 Compile Audit Report

Use template from `_shared/first-time-user-base.md` with these tool-specific steps:

**Happy Path Steps for Dashboard:**
1. Find documentation
2. Understand prerequisites (password, variants)
3. Set DASHBOARD_PASSWORD env var
4. Run generate command
5. Find output file
6. View in browser
7. Enter password
8. Navigate dashboard features

### 5.2 Save Report

```bash
docs/audits/YYYY-MM-DD-first-time-user-dashboard.md
```

---

## Example Output

<example_output>
## Executive Summary

| Metric | Value |
|--------|-------|
| **Overall Score** | 6/10 |
| **Time to First Success** | 12 minutes |
| **Critical Blockers** | 1 |
| **Friction Points** | 3 |

Dashboard generation succeeded, but documentation was scattered. Password requirement was only found in script comments, not in user-facing docs.

## Happy Path Journey

| Step | Status | Friction | Notes |
|------|--------|----------|-------|
| Find documentation | Partial | High | Not in README Quick Start |
| Understand prerequisites | Failure | Critical | Password env var not documented |
| Set password env var | Success | Low | Error message helpful once I tried |
| Run generate command | Success | None | Clear output |
| Find output file | Success | Low | Path shown in output |
| View in browser | Partial | Medium | Had to run npm run dev |
| Enter password | Success | None | UI clear |
| Navigate dashboard | Success | None | Intuitive |

## Recommendations

### Priority 1 (Blocking)
- Document DASHBOARD_PASSWORD requirement in Getting Started

### Priority 2 (Friction)
- Add dashboard to README Quick Start section
- Document how to view (npm run dev vs open file)

### Priority 3 (Polish)
- Add success message with URL after generate
</example_output>

---

## Quality Checklist

Before completing:
- [ ] Followed ONLY documentation (no source code diving)
- [ ] Tested full happy path (generate → view → use)
- [ ] Tested error scenarios (no password, no variants)
- [ ] Documented all friction points
- [ ] Generated prioritized recommendations
- [ ] Saved report to docs/audits/

---

## Notes

- Dashboard is password-protected — password setup is critical path
- Dashboard is a static HTML file — viewing method matters
- Links to portfolio variants must work correctly
- Resume download links must be functional

<skill_compositions>
## Works Well With

- **first-time-user** — General documentation audit
- **first-time-user-ucv-cli** — CLI-specific audit
- **technical-writer** — Fix documentation issues found
- **sprint-sync** — Report findings in status update
</skill_compositions>
