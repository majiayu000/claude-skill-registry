---
name: roadmap-integration
description: Manages product roadmap via GitHub Issues (brainstorm, prioritize, track). Auto-validates features against project vision (from overview.md) before adding to roadmap. Use when running /roadmap command or mentions 'roadmap', 'add feature', 'brainstorm ideas', or 'prioritize features'.
---

<objective>
Manage product roadmap via GitHub Issues with vision alignment validation and creation-order prioritization, ensuring features align with project goals before implementation.
</objective>

<quick_start>
<roadmap_workflow>
**Vision-aligned feature management:**

1. **Initialize**: Verify GitHub authentication (gh CLI or GITHUB_TOKEN)
2. **Load vision**: Read docs/project/overview.md for alignment validation
3. **Parse intent**: Identify action (add, brainstorm, move, delete, search, ship)
4. **Validate vision**: Check against out-of-scope exclusions and project vision
5. **Create issue**: Generate GitHub Issue with metadata (area, role, slug)
6. **Show summary**: Display roadmap state and suggest next action

**Quick actions:**
```bash
/roadmap add "student progress widget"
/roadmap brainstorm "CFI productivity tools"
/roadmap move auth-refactor Next
/roadmap search export
```

**Example workflow:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 VISION ALIGNMENT CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project Vision:
AKTR helps flight instructors track student progress against ACS standards.

Proposed Feature:
  Add student progress widget showing mastery percentage by ACS area

✅ Feature aligns with project vision

Target User Check:
Does this feature serve: CFIs, Flight students, School admins
Confirm primary user (or 'skip'): Flight students

✅ Vision alignment complete

✅ Created issue #123: student-progress-widget in Backlog
   Area: app | Role: student

📊 Roadmap Summary:
   Backlog: 12 | Next: 3 | In Progress: 2 | Shipped: 45

Top 3 in Backlog (oldest/highest priority):
1. #98 cfi-batch-export (Created: 2025-11-01)
2. #87 study-plan-generator (Created: 2025-11-05)
3. #123 student-progress-widget (Created: 2025-11-13)

💡 Next: /feature cfi-batch-export
```
</roadmap_workflow>

<trigger_conditions>
**Auto-invoke when:**
- `/roadmap` command executed
- User mentions "roadmap", "add feature", "brainstorm ideas", "prioritize features"
- Starting feature planning workflow

**Prerequisites:**
- GitHub authentication (gh CLI or GITHUB_TOKEN)
- Git repository with GitHub remote
- Optional: docs/project/overview.md for vision validation
</trigger_conditions>
</quick_start>

<workflow>
<step number="1" name="initialize_github_context">
**1. Initialize GitHub Context**

Verify GitHub authentication and repository access.

**Actions:**
- Check GitHub CLI authentication (gh auth status)
- Fallback to GITHUB_TOKEN environment variable
- Verify git repository has GitHub remote
- Source roadmap manager scripts

**Script location:** See [references/github-setup.md](references/github-setup.md) for platform-specific bash/powershell scripts

**Validation:**
```bash
AUTH_METHOD=$(check_github_auth)  # Returns: gh-cli, token, or none
REPO=$(get_repo_info)             # Returns: owner/repo-name

if [ "$AUTH_METHOD" = "none" ]; then
  echo "❌ GitHub authentication required"
  echo "Options: gh auth login OR export GITHUB_TOKEN=ghp_..."
  exit 1
fi
```

**Output:**
```
✅ GitHub authenticated (gh-cli)
✅ Repository: owner/repo-name
```
</step>

<step number="2" name="load_project_docs">
**2. Load Project Documentation Context**

Load project vision, scope boundaries, and target users from overview.md.

**When to execute:**
- Always before ADD/BRAINSTORM actions
- Skip for MOVE/DELETE/SEARCH operations

**Actions:**
```bash
PROJECT_OVERVIEW="docs/project/overview.md"
HAS_PROJECT_DOCS=false

if [ -f "$PROJECT_OVERVIEW" ]; then
  HAS_PROJECT_DOCS=true
  # Extract: Vision, Out-of-Scope, Target Users
  # (see detailed extraction logic in references)
else
  echo "ℹ️  No project documentation found"
  echo "   Run /init-project to create (optional)"
fi
```

**Extracted context:**
- **Vision**: 1 paragraph describing project purpose
- **Out-of-Scope**: Bullet list of explicit exclusions
- **Target Users**: Bullet list of intended users

**See:** [references/vision-validation.md](references/vision-validation.md) for extraction logic and validation rules

**Token budget:** ~5-8K tokens (overview.md typically 2-3 pages)
</step>

<step number="3" name="parse_user_intent">
**3. Parse User Intent**

Identify action type and extract parameters.

**Action types:**
- `add` - Add new feature (vision-validated, prioritized by creation order)
- `brainstorm` - Generate feature ideas via web research
- `move` - Change feature status (Backlog → Next → In Progress)
- `delete` - Remove feature from roadmap
- `search` - Find features by keyword/area/role/sprint
- `ship` - Mark feature as shipped

**Parse logic:**
| User Input | Action | Parameters |
|------------|--------|------------|
| "Add student progress widget" | add | title: "student progress widget" |
| "Brainstorm ideas for CFI tools" | brainstorm | topic: "CFI tools" |
| "Move auth-refactor to Next" | move | slug: "auth-refactor", target: "Next" |
| "Delete deprecated-feature" | delete | slug: "deprecated-feature" |
| "Search for export features" | search | keywords: "export" |
</step>

<step number="4" name="vision_alignment_validation">
**4. Vision Alignment Validation**

Validate feature against project vision before creating GitHub Issue.

**Executes for:** ADD and BRAINSTORM actions only

**Validation checks:**
1. **Out-of-scope check**: Feature not in explicit exclusion list
2. **Vision alignment**: Feature supports project vision (semantic analysis)
3. **Target user check**: Feature serves documented target users

**Decision tree:**
```
Feature proposed
    ↓
overview.md present? → No → Skip validation, proceed to creation
    ↓ Yes
Extract: Vision, Out-of-Scope, Target Users
    ↓
Out-of-scope check → Match → Prompt: Skip/Update/Override
    ↓ No match
Vision alignment → Misaligned → Prompt: Add anyway/Revise/Skip
    ↓ Aligned
Target user check → Select primary user → Add role label
    ↓
✅ Validation passed → Proceed to GitHub Issue creation
```

**Blocking gates:**
- Out-of-scope feature detected → User must skip, update overview.md, or provide justification
- Vision misalignment → User must revise, skip, or override with note

**Overrides:**
- Add ALIGNMENT_NOTE to issue body when user overrides validation
- Document justification for future reference

**See:** [references/vision-validation.md](references/vision-validation.md) for complete validation logic, prompts, and output examples
</step>

<step number="5" name="github_issue_creation">
**5. GitHub Issue Creation**

Create GitHub Issue with metadata after vision validation passes.

**Actions:**
1. Generate URL-friendly slug from title (max 30 chars)
2. Check for duplicate slugs
3. Extract area (backend, frontend, api, infra, design)
4. Extract role (all, free, student, cfi, school)
5. Create issue with YAML frontmatter metadata
6. Auto-apply labels (area, role, type:feature, status:backlog)

**Issue structure:**
```yaml
---
metadata:
  area: app
  role: student
  slug: student-progress-widget
---

## Problem
[User pain point or need]

## Proposed Solution
[High-level approach]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

---

⚠️  **Alignment Note**: Validated against project vision (overview.md)
```

**Prioritization:**
- Features prioritized by **creation order** (oldest issue = highest priority)
- No ICE scoring required (creation timestamp determines priority)
- Top of Backlog = oldest unworked issue

**Labels auto-applied:**
- `area:$AREA` - System area (backend, frontend, api, etc.)
- `role:$ROLE` - Target user role
- `type:feature` - Issue type
- `status:backlog` - Initial status

**See:** [references/issue-creation.md](references/issue-creation.md) for bash/powershell scripts and examples
</step>

<step number="6" name="return_roadmap_summary">
**6. Return Roadmap Summary**

Display current roadmap state and suggest next action.

**Actions:**
1. Fetch all issues from GitHub via gh CLI
2. Count features by status (Backlog, Next, In Progress, Shipped)
3. Show top 3 features in Backlog (oldest first = highest priority)
4. Suggest next action (/feature [oldest-slug])

**Summary format:**
```
✅ Created issue #123: student-progress-widget in Backlog
   Area: app | Role: student

📊 Roadmap Summary:
   Backlog: 12 | Next: 3 | In Progress: 2 | Shipped: 45

Top 3 in Backlog (oldest/highest priority):
1. #98 cfi-batch-export (Created: 2025-11-01)
2. #87 study-plan-generator (Created: 2025-11-05)
3. #123 student-progress-widget (Created: 2025-11-13)

💡 Next: /feature cfi-batch-export
```

**Priority guidance:**
- Work on oldest Backlog item first (creation-order prioritization)
- Move items to "Next" when ready to plan (3-5 item queue)
- Move to "In Progress" when actively implementing
- Close with "Shipped" label when deployed
</step>
</workflow>

<anti_patterns>
**Avoid these roadmap management mistakes:**

<pitfall name="skip_vision_alignment">
**❌ Adding features without vision validation**
```bash
# BAD: Skip vision check, add any feature
HAS_PROJECT_DOCS=false  # Force skip even if docs exist
/roadmap add "social media integration"
```
**✅ Always run vision validation when overview.md exists**
```bash
# GOOD: Load project docs, validate alignment
if [ -f "docs/project/overview.md" ]; then
  HAS_PROJECT_DOCS=true
  # Extract vision context, run validation
fi
```
**Impact:** Roadmap fills with out-of-scope features, dilutes project focus
**Prevention:** Never set `HAS_PROJECT_DOCS=false` if docs exist
</pitfall>

<pitfall name="override_out_of_scope_without_justification">
**❌ Overriding out-of-scope exclusions without updating docs**
```bash
# BAD: Add out-of-scope feature, provide vague justification
Feature: "flight scheduling"
Matches exclusion: "Flight scheduling or aircraft management"
Justification: "it would be nice to have"
```
**✅ Update overview.md if scope legitimately changed**
```bash
# GOOD: Update source docs first
# Edit docs/project/overview.md:
# - Remove "Flight scheduling" from Out-of-Scope section
# - Document scope expansion in Vision section
# Then add feature normally
```
**Impact:** Overview.md becomes outdated, vision validation unreliable
**Prevention:** Treat overview.md as source of truth, update before overriding
</pitfall>

<pitfall name="missing_metadata">
**❌ Manually creating GitHub Issues without metadata**
```bash
# BAD: Create issue via gh CLI directly
gh issue create --title "new feature" --body "description"
# Missing: area, role, slug, YAML frontmatter
```
**✅ Always use create_roadmap_issue() function**
```bash
# GOOD: Use roadmap manager function
create_roadmap_issue \
  "$TITLE" \
  "$BODY" \
  "$AREA" \
  "$ROLE" \
  "$SLUG" \
  "type:feature,status:backlog"
# Auto-adds metadata, labels, frontmatter
```
**Impact:** Cannot filter/search issues, roadmap state tracking breaks
**Prevention:** Never create roadmap issues manually, always use manager functions
</pitfall>

<pitfall name="duplicate_slugs">
**❌ Creating features with duplicate slugs**
```bash
# BAD: Don't check for existing slug
SLUG="user-auth"
create_roadmap_issue ...  # Issue #50 already has slug "user-auth"
```
**✅ Check for duplicates before creation**
```bash
# GOOD: Validate slug uniqueness
EXISTING_ISSUE=$(get_issue_by_slug "$SLUG")
if [ -n "$EXISTING_ISSUE" ]; then
  echo "⚠️  Slug '$SLUG' already exists (Issue #$EXISTING_ISSUE)"
  SLUG="${SLUG}-v2"  # Append version suffix
fi
```
**Impact:** Multiple issues with same slug, /feature command ambiguous
**Prevention:** Always call get_issue_by_slug() before creation
</pitfall>

<pitfall name="unclear_feature_descriptions">
**❌ Vague feature descriptions that fail vision check**
```bash
# BAD: Ambiguous description
FEATURE="Make it better for users"
# Vision validator cannot assess alignment
```
**✅ Use Problem + Solution + Requirements format**
```bash
# GOOD: Structured description
PROBLEM="Students struggle to track mastery across ACS areas"
SOLUTION="Add progress widget showing mastery percentage by area"
REQUIREMENTS="
- [ ] Display mastery % per ACS area
- [ ] Color-code by proficiency level
- [ ] Export progress report"
```
**Impact:** Vision alignment validation fails, feature rejected
**Prevention:** Prompt user for Problem/Solution/Requirements if description unclear
</pitfall>

<pitfall name="roadmap_state_sync_issues">
**❌ Not updating issue labels when feature progresses**
```bash
# BAD: Create spec but don't update GitHub Issue
/feature user-auth  # Creates spec
# Issue #50 still has status:backlog (should be status:in-progress)
```
**✅ Update labels when feature state changes**
```bash
# GOOD: Mark in progress when spec created
mark_issue_in_progress "user-auth"  # Updates to status:in-progress
# Later: mark_issue_shipped when deployed
```
**Impact:** Roadmap summary shows stale counts, misleading prioritization
**Prevention:** Hook /feature, /ship commands to update issue labels
</pitfall>
</anti_patterns>

<success_criteria>
**Roadmap management successful when:**

- ✓ GitHub authenticated (gh CLI or GITHUB_TOKEN verified)
- ✓ Project documentation loaded (if docs/project/overview.md exists)
- ✓ Vision alignment validated (out-of-scope check, vision match, target user)
- ✓ Metadata extracted (area, role, slug from feature description)
- ✓ GitHub Issue created with YAML frontmatter metadata
- ✓ Labels auto-applied (area:*, role:*, type:feature, status:backlog)
- ✓ Roadmap summary displayed (counts by status, top 3 by creation order)
- ✓ Next action suggested (/feature [oldest-slug])

**Quality gates passed:**
- Out-of-scope gate: Feature not in explicit exclusion list (or override justified)
- Vision alignment gate: Feature supports project vision (or override justified)
- Duplicate check: Slug is unique across all issues
- Metadata completeness: Area, role, slug present in YAML frontmatter

**Integration working:**
- /roadmap feeds into /feature command (issue → spec)
- /feature updates issue labels (backlog → in-progress)
- /ship-prod marks issue as shipped (in-progress → closed with shipped label)
</success_criteria>

<reference_guides>
For detailed scripts, validation logic, and integration patterns:

- **[references/github-setup.md](references/github-setup.md)** - Platform-specific authentication and initialization scripts (bash/powershell)
- **[references/vision-validation.md](references/vision-validation.md)** - Complete validation logic, decision tree, prompts, and output examples
- **[references/issue-creation.md](references/issue-creation.md)** - GitHub Issue creation scripts, metadata structure, label application
- **[references/project-integration.md](references/project-integration.md)** - How roadmap integrates with /init-project, /feature, /ship workflows

**Scripts:**
- `.spec-flow/scripts/bash/github-roadmap-manager.sh`
- `.spec-flow/scripts/powershell/github-roadmap-manager.ps1`

**Command:** `.claude/commands/project/roadmap.md`
</reference_guides>

<performance>
**Token budget per action:**
- ADD (with vision validation): ~8-12K tokens
  - overview.md read: ~5-8K
  - Vision alignment analysis: ~2-3K
  - GitHub Issue creation: ~1K
- ADD (without docs): ~2-3K tokens
- BRAINSTORM (quick): ~15-20K tokens
- BRAINSTORM (deep): ~40-60K tokens
- MOVE/DELETE/SEARCH: ~1-2K tokens

**Execution time:**
- ADD with vision check: 30-60 seconds
- MOVE/DELETE/SEARCH: <10 seconds
- BRAINSTORM quick: 30-60 seconds
- BRAINSTORM deep: 2-5 minutes
</performance>
