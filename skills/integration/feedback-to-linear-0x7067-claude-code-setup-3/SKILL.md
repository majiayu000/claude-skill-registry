---
name: feedback-to-linear
description: Transform user feedback into structured Linear issues with AI-enhanced parsing for labels, priority, acceptance criteria, and estimates
license: MIT
---

# Feedback to Linear

Transform raw user feedback text into structured Linear issues with intelligent AI parsing.

## Triggers

Activate this skill with any of these phrases:
- "Convert this feedback to Linear issues"
- "Create issues from user feedback"
- "feedback-to-linear"
- "Parse feedback for Linear"
- "Transform feedback into Linear"

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Input** | Raw feedback text (batch) + team/project selection |
| **Output** | Linear issues with AI-parsed metadata (title, labels, priority, acceptance criteria, estimates, links) |
| **Workspace** | Uses workspace from configured Linear API key |
| **Mode** | Batch processing with conditional confirmation |
| **Duration** | ~1-2 minutes for 5-10 feedback items |

## Agent Behavior Contract

When this skill is invoked, you MUST:

1. **Never assume context** - Always fetch teams, projects, and labels dynamically from Linear
2. **Single workspace** - Issues are created in the workspace associated with the Linear MCP plugin's API key
3. **Auto-detect repo context** - If in a git repo, automatically use project info (no prompt)
4. **Use existing labels only** - Never create new labels; only match to fetched labels
5. **Default to Backlog** - New issues start in "Backlog" or "Todo" state unless specified
6. **Batch process** - Parse all feedback items together, then create all at once
7. **Preserve user voice** - Keep original feedback wording in descriptions
8. **Conditional confirmation** - Only prompt if LOW confidence items exist

## Process

### Phase 1: Input Collection

**Objective:** Gather feedback, detect context, and select target location in Linear.

**Steps:**

1. **Load all MCP tools upfront** (batch in parallel):
   ```
   MCPSearch("select:mcp__plugin_linear_linear__list_teams")
   MCPSearch("select:mcp__plugin_linear_linear__list_projects")
   MCPSearch("select:mcp__plugin_linear_linear__list_issue_labels")
   MCPSearch("select:mcp__plugin_linear_linear__create_issue")
   ```

2. **Prompt user for feedback text** (support multi-line, multiple items, inline URLs)
   - Users can include screenshot/video URLs directly in feedback
   - URLs are auto-extracted during parsing

3. **Auto-detect repo context** (no prompt):
   - Check if current directory is a git repo (`git rev-parse --git-dir`)
   - If yes, detect:
     - Project name from `package.json`, `Cargo.toml`, `pyproject.toml`, or git remote
     - Platform from project structure (ios/, android/, package.json dependencies, etc.)
     - Repo URL from `git config --get remote.origin.url`
   - Display detected context as informational message:
     ```
     Detected: [project-name] (iOS) - github.com/user/repo
     ```

4. **Fetch Linear data** (can run in parallel):
   - `mcp__plugin_linear_linear__list_teams` to get available teams
   - After team is known: fetch projects and labels for that team

5. **Single combined question** using `AskUserQuestion` with 3 questions:
   - **Team**: "Which team?" (required, single select)
     - If repo name matches a team, note it
   - **Platform**: "Platform?" (single select)
     - Options: iOS, Android, Web, Backend/API, Multiple
     - If detected from repo, set as default
   - **Project**: "Project?" (optional, single select)
     - Include "None/Backlog" option
     - If repo name matches a project, highlight it

6. **Fetch labels** for selected team:
   - `mcp__plugin_linear_linear__list_issue_labels`

**Inputs:** User feedback text
**Outputs:** Validated team/project, platform context, available labels, repo context
**Verification:** Team ID is valid, labels fetched successfully

---

### Phase 2: AI Parsing (Batch)

**Objective:** Extract structured issue data from raw feedback using AI.

**Steps:**

1. Split feedback into individual items (by line breaks, blank lines, or numbered lists)

2. For each feedback item, extract:
   - **Title**: Imperative, actionable, <80 chars, include specifics
   - **Description**: Original feedback + context + estimate note (markdown formatted)
   - **Labels**: Semantically match to fetched labels using compound signals
   - **Priority**: 1-4 based on multi-signal inference (default: 3)
   - **Acceptance Criteria**: 3-5 testable items in markdown checklist format
   - **Estimate**: XS/S/M/L/XL complexity (appended to description)
   - **Confidence**: HIGH/MEDIUM/LOW for each field
   - **Links**: Auto-extract URLs from feedback text

**Label Matching Guidelines:**
- Use compound signal detection (see parsing guidelines)
- Consider label descriptions, not just names
- Domain-aware: prioritize platform labels matching detected repo
- Match based on >70% semantic confidence
- Maximum 3-4 labels per issue

**Title Convention:**
- When platform is selected (not "Multiple"), prefix with `[Platform]`
- Include specific details from feedback (device, size, action)
- Avoid generic titles like "Fix bug" or "Add feature"
- Examples:
  - "[iOS] Fix crash when uploading large images on iPhone 14"
  - "[Android] Add dark mode toggle in settings"

**Priority Detection (Multi-Signal):**
- Base priority: 3 (Medium) - most feedback deserves attention
- Adjust up/down based on signals:

| Signal Type | +1 Priority | -1 Priority |
|-------------|-------------|-------------|
| User impact | "many users", "everyone", "all" | "sometimes", "rarely", "edge case" |
| Business | "can't use", "blocking", "revenue" | "cosmetic", "minor", "nice to have" |
| Severity | crash, data loss, security | typo, color, alignment |
| Tone | ALL CAPS, !!!, frustrated | casual suggestion |

- Priority 1 (Urgent): crash + many users, security, data loss
- Priority 2 (High): blocking core flow, explicit urgency
- Priority 3 (Medium): default, standard bugs/features
- Priority 4 (Low): cosmetic, minor polish

**Confidence Scoring:**

| Field | HIGH | MEDIUM | LOW |
|-------|------|--------|-----|
| Title | Clear action + specific issue | Transformed, some ambiguity | Vague, add `[?]` suffix |
| Labels | Exact compound match | Semantic inference | Weak match |
| Priority | Multiple strong signals | Some signals | Defaulted |
| Estimate | - | Always MEDIUM | - |

**Description Format:**
```markdown
[Original user feedback, quoted or paraphrased]

## Context
[Inferred context + device/platform details]
[If repo detected: **Source repo:** project-name (repo-url)]

**Complexity Estimate:** M (Medium)

## Links
- [Screenshot](https://d.pr/abc123)
- [src/Component.tsx](https://github.com/user/repo/blob/main/src/Component.tsx)

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

**Inputs:** Feedback items, available labels, repo context
**Outputs:** Structured issue data with confidence scores
**Verification:** All items have title, description, valid labels

---

### Phase 3: Creation & Confirmation

**Objective:** Preview parsed issues and create them in Linear.

**Steps:**

1. **Display preview table:**
   | Title | Labels | Pri | Est | Confidence |
   |-------|--------|-----|-----|------------|
   | [iOS] Fix crash on upload | Bug, iOS | 2 | M | HIGH |
   | Improve settings [?] | Enhancement | 3 | M | LOW ⚠️ |

2. **Conditional confirmation:**
   - If ALL items have HIGH or MEDIUM confidence → **create immediately** (no prompt)
   - If ANY item has LOW confidence → prompt with `AskUserQuestion`:
     - "Create N issues? (X items flagged for review)"
     - Options: "Create all", "Edit flagged items", "Cancel"

3. **If editing:**
   - Allow inline edits: "Change issue 2 title to: [new title]"
   - Re-display preview after edits
   - Then create

4. **Create issues:**
   - For each parsed issue, call `mcp__plugin_linear_linear__create_issue`
   - Include: title, team, project (if set), labels, priority, description

5. **Display summary:**
   | Issue | URL |
   |-------|-----|
   | MOB-123 | https://linear.app/team/issue/MOB-123 |

**Inputs:** Parsed issue data, user confirmation (if needed)
**Outputs:** Created Linear issues with URLs
**Verification:** All issues created successfully

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Creating labels | May not match team conventions | Use existing labels only |
| Hardcoding labels | Different workspaces have different labels | Fetch dynamically |
| Asking about repo context | Adds unnecessary prompt | Auto-detect silently |
| Asking about media URLs | Adds unnecessary prompt | Auto-extract from feedback |
| Always prompting to confirm | Slows down workflow | Only prompt if LOW confidence |
| Priority 0 as default | Most feedback deserves attention | Default to 3 (Medium) |
| Generic titles | Hard to scan/triage | Include specifics from feedback |

## Verification Checklist

Before completing this skill, verify:
- [ ] All issues created with valid team assignment
- [ ] Labels match existing workspace labels (no new labels created)
- [ ] Confirmation only prompted if LOW confidence items exist
- [ ] Summary with issue URLs provided
- [ ] Acceptance criteria formatted as markdown checklist
- [ ] Priority values are 1-4 (not 0 unless truly ambiguous)
- [ ] Estimate included in description
- [ ] Confidence scores assigned (HIGH/MEDIUM/LOW)
- [ ] LOW confidence items flagged with [?] in title
- [ ] Repo context auto-detected and used (if in git repo)
- [ ] URLs auto-extracted from feedback text

## Extension Points

This skill can be extended to:
1. **Duplicate detection** - Check for similar existing issues before creating
2. **Assignee inference** - Auto-assign based on feedback source or label
3. **Cycle assignment** - Automatically add to current cycle
4. **Parent issues** - Group related feedback under epic/parent

## References

See `references/ai-parsing-guidelines.md` for detailed semantic matching rules and examples.
