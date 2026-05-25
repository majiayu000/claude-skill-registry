---
name: adding-milestones
description: Use this skill when adding a milestone to an existing project, starting a new milestone cycle, creating the first milestone after project init, or defining what's next after completing work. Triggers include "add milestone", "new milestone", "start milestone", "create milestone", "first milestone", "next milestone", and "milestone cycle".
metadata:
  version: "0.1.0"
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Task
  - AskUserQuestion
---

<user_command>/kata:add-milestone</user_command>


<objective>
Add a milestone to the project through unified flow: questioning → research (optional) → requirements → roadmap.

This works for both first milestone (after /kata:new-project) and subsequent milestones (after completing a milestone).

**Creates/Updates:**
- `.planning/PROJECT.md` — updated with new milestone goals
- `.planning/research/` — domain research (optional, focuses on NEW features)
- `.planning/REQUIREMENTS.md` — scoped requirements for this milestone
- `.planning/ROADMAP.md` — phase structure (creates if first, continues if subsequent)
- `.planning/STATE.md` — reset for new milestone (creates if first)

**After this command:** Run `/kata:plan-phase [N]` to start execution.
</objective>

<execution_context>
@./references/questioning.md
@./references/ui-brand.md
@./references/project-template.md
@./references/requirements-template.md
@./references/github-mapping.md
</execution_context>

<context>
Milestone name: $ARGUMENTS (optional - will prompt if not provided)

**Load project context:**
@.planning/PROJECT.md
@.planning/STATE.md
@.planning/MILESTONES.md
@.planning/config.json

**Load milestone context (if exists, from /kata:discuss-milestone):**
@.planning/MILESTONE-CONTEXT.md
</context>

<process>

## Phase 1: Load Context

- Read PROJECT.md (existing project, Validated requirements, decisions)
- Read MILESTONES.md (what shipped previously)
- Read STATE.md (pending todos, blockers)
- Check for MILESTONE-CONTEXT.md (from /kata:discuss-milestone)

## Phase 2: Gather Milestone Goals

**If MILESTONE-CONTEXT.md exists:**
- Use features and scope from discuss-milestone
- Present summary for confirmation

**If no context file:**
- Present what shipped in last milestone
- Ask: "What do you want to build next?"
- Use AskUserQuestion to explore features
- Probe for priorities, constraints, scope

## Phase 3: Determine Milestone Version

- Parse last version from MILESTONES.md
- Suggest next version (v1.0 → v1.1, or v2.0 for major)
- Confirm with user

## Phase 4: Update PROJECT.md

Add/update these sections:

```markdown
## Current Milestone: v[X.Y] [Name]

**Goal:** [One sentence describing milestone focus]

**Target features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]
```

Update Active requirements section with new goals.

Update "Last updated" footer.

## Phase 5: Update STATE.md

```markdown
## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements
Last activity: [today] — Milestone v[X.Y] started
```

Keep Accumulated Context section (decisions, blockers) from previous milestone.

## Phase 5.5: Create GitHub Milestone (if enabled)

Read GitHub config:
```bash
GITHUB_ENABLED=$(cat .planning/config.json 2>/dev/null | grep -o '"enabled"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
```

**If `GITHUB_ENABLED=true`:**

**Step 1: Validate GitHub remote exists**

```bash
HAS_GITHUB_REMOTE=$(git remote -v 2>/dev/null | grep -q 'github\.com' && echo "true" || echo "false")
```

**If `HAS_GITHUB_REMOTE=false`:**

Display warning and skip GitHub operations:
```
Warning: GitHub tracking enabled but no GitHub remote found.
Skipping GitHub Milestone creation.

To enable GitHub Milestones:
1. Create a repository: gh repo create --source=. --public --push
2. Re-run milestone creation or manually create via: gh api --method POST /repos/:owner/:repo/milestones -f title="v${VERSION}"
```

Continue with local milestone initialization (do NOT set github.enabled=false in config - user may add remote later).

**If `HAS_GITHUB_REMOTE=true`:**

**Step 2: Check authentication (non-blocking)**

```bash
if ! gh auth status &>/dev/null; then
  echo "Warning: GitHub CLI not authenticated. Run 'gh auth login' to enable GitHub integration."
  # Continue without GitHub operations - local milestone still created
else
  # Proceed with milestone creation
fi
```

**Step 3: Check if milestone exists (idempotent)**

```bash
MILESTONE_EXISTS=$(gh api /repos/:owner/:repo/milestones 2>/dev/null | jq -r ".[] | select(.title==\"v${VERSION}\") | .number" 2>/dev/null)
```

**Step 4: Create milestone if doesn't exist**

```bash
if [ -z "$MILESTONE_EXISTS" ]; then
  # Extract milestone description (first paragraph of goal, truncated to 500 chars)
  MILESTONE_DESC=$(echo "$MILESTONE_GOALS" | head -1 | cut -c1-500)

  gh api \
    --method POST \
    -H "Accept: application/vnd.github.v3+json" \
    /repos/:owner/:repo/milestones \
    -f title="v${VERSION}" \
    -f state='open' \
    -f description="${MILESTONE_DESC}" \
    2>/dev/null && echo "GitHub Milestone v${VERSION} created" || echo "Warning: Failed to create GitHub Milestone (continuing)"
else
  echo "GitHub Milestone v${VERSION} already exists (#${MILESTONE_EXISTS})"
fi
```

**If `GITHUB_ENABLED=false`:**

Skip GitHub operations silently (no warning needed - user opted out).

**Error handling principle:**
- All GitHub operations are non-blocking
- Missing remote warns but does not stop milestone initialization
- Auth failures warn but do not stop milestone initialization
- Planning files always persist locally regardless of GitHub status

## Phase 6: Cleanup and Commit

Delete MILESTONE-CONTEXT.md if exists (consumed).

Check planning config:
```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

If `COMMIT_PLANNING_DOCS=false`: Skip git operations

If `COMMIT_PLANNING_DOCS=true` (default):
```bash
git add .planning/PROJECT.md .planning/STATE.md
git commit -m "docs: start milestone v[X.Y] [Name]"
```

## Phase 6.5: Resolve Model Profile

Read model profile for agent spawning:

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Default to "balanced" if not set.

**Model lookup table:**

| Agent                     | quality | balanced | budget |
| ------------------------- | ------- | -------- | ------ |
| kata-project-researcher   | opus    | sonnet   | haiku  |
| kata-research-synthesizer | sonnet  | sonnet   | haiku  |
| kata-roadmapper           | opus    | sonnet   | sonnet |

Store resolved models for use in Task calls below.

## Phase 7: Research Decision

Use AskUserQuestion:
- header: "Research"
- question: "Research the domain ecosystem for new features before defining requirements?"
- options:
  - "Research first (Recommended)" — Discover patterns, expected features, architecture for NEW capabilities
  - "Skip research" — I know what I need, go straight to requirements

**If "Research first":**

Display stage banner:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► RESEARCHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Researching [new features] ecosystem...


Create research directory:
```bash
mkdir -p .planning/research
```

Display spawning indicator:
```
◆ Spawning 4 researchers in parallel...
  → Stack research (for new features)
  → Features research
  → Architecture research (integration)
  → Pitfalls research
```

Spawn 4 parallel kata-project-researcher agents with milestone-aware context:

```
Task(prompt="
<research_type>
Project Research — Stack dimension for [new features].
</research_type>

<milestone_context>
SUBSEQUENT MILESTONE — Adding [target features] to existing app.

Existing validated capabilities (DO NOT re-research):
[List from PROJECT.md Validated requirements]

Focus ONLY on what's needed for the NEW features.
</milestone_context>

<question>
What stack additions/changes are needed for [new features]?
</question>

<project_context>
[PROJECT.md summary - current state, new milestone goals]
</project_context>

<downstream_consumer>
Your STACK.md feeds into roadmap creation. Be prescriptive:
- Specific libraries with versions for NEW capabilities
- Integration points with existing stack
- What NOT to add and why
</downstream_consumer>

<quality_gate>
- [ ] Versions are current (verify with Context7/official docs, not training data)
- [ ] Rationale explains WHY, not just WHAT
- [ ] Integration with existing stack considered
</quality_gate>

<output>
Write to: .planning/research/STACK.md
Format: Standard research output forSTACK.md
</output>
", subagent_type="kata-project-researcher", model="{researcher_model}", description="Stack research")

Task(prompt="
<research_type>
Project Research — Features dimension for [new features].
</research_type>

<milestone_context>
SUBSEQUENT MILESTONE — Adding [target features] to existing app.

Existing features (already built):
[List from PROJECT.md Validated requirements]

Focus on how [new features] typically work, expected behavior.
</milestone_context>

<question>
How do [target features] typically work? What's expected behavior?
</question>

<project_context>
[PROJECT.md summary - new milestone goals]
</project_context>

<downstream_consumer>
Your FEATURES.md feeds into requirements definition. Categorize clearly:
- Table stakes (must have for these features)
- Differentiators (competitive advantage)
- Anti-features (things to deliberately NOT build)
</downstream_consumer>

<quality_gate>
- [ ] Categories are clear (table stakes vs differentiators vs anti-features)
- [ ] Complexity noted for each feature
- [ ] Dependencies on existing features identified
</quality_gate>

<output>
Write to: .planning/research/FEATURES.md
Format: Standard research output forFEATURES.md
</output>
", subagent_type="kata-project-researcher", model="{researcher_model}", description="Features research")

Task(prompt="
<research_type>
Project Research — Architecture dimension for [new features].
</research_type>

<milestone_context>
SUBSEQUENT MILESTONE — Adding [target features] to existing app.

Existing architecture:
[Summary from PROJECT.md or codebase map]

Focus on how [new features] integrate with existing architecture.
</milestone_context>

<question>
How do [target features] integrate with existing [domain] architecture?
</question>

<project_context>
[PROJECT.md summary - current architecture, new features]
</project_context>

<downstream_consumer>
Your ARCHITECTURE.md informs phase structure in roadmap. Include:
- Integration points with existing components
- New components needed
- Data flow changes
- Suggested build order
</downstream_consumer>

<quality_gate>
- [ ] Integration points clearly identified
- [ ] New vs modified components explicit
- [ ] Build order considers existing dependencies
</quality_gate>

<output>
Write to: .planning/research/ARCHITECTURE.md
Format: Standard research output forARCHITECTURE.md
</output>
", subagent_type="kata-project-researcher", model="{researcher_model}", description="Architecture research")

Task(prompt="
<research_type>
Project Research — Pitfalls dimension for [new features].
</research_type>

<milestone_context>
SUBSEQUENT MILESTONE — Adding [target features] to existing app.

Focus on common mistakes when ADDING these features to an existing system.
</milestone_context>

<question>
What are common mistakes when adding [target features] to [domain]?
</question>

<project_context>
[PROJECT.md summary - current state, new features]
</project_context>

<downstream_consumer>
Your PITFALLS.md prevents mistakes in roadmap/planning. For each pitfall:
- Warning signs (how to detect early)
- Prevention strategy (how to avoid)
- Which phase should address it
</downstream_consumer>

<quality_gate>
- [ ] Pitfalls are specific to adding these features (not generic)
- [ ] Integration pitfalls with existing system covered
- [ ] Prevention strategies are actionable
</quality_gate>

<output>
Write to: .planning/research/PITFALLS.md
Format: Standard research output forPITFALLS.md
</output>
", subagent_type="kata-project-researcher", model="{researcher_model}", description="Pitfalls research")
```

After all 4 agents complete, spawn synthesizer to create SUMMARY.md:

```
Task(prompt="
<task>
Synthesize research outputs into SUMMARY.md.
</task>

<research_files>
Read these files:
- .planning/research/STACK.md
- .planning/research/FEATURES.md
- .planning/research/ARCHITECTURE.md
- .planning/research/PITFALLS.md
</research_files>

<output>
Write to: .planning/research/SUMMARY.md
Format: Standard research output forSUMMARY.md
Commit after writing.
</output>
", subagent_type="kata-research-synthesizer", model="{synthesizer_model}", description="Synthesize research")
```

Display research complete banner and key findings:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► RESEARCH COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Key Findings

**Stack additions:** [from SUMMARY.md]
**New feature table stakes:** [from SUMMARY.md]
**Watch Out For:** [from SUMMARY.md]

Files: `.planning/research/`


**If "Skip research":** Continue to Phase 8.

## Phase 8: Define Requirements

Display stage banner:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► DEFINING REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


**Load context:**

Read PROJECT.md and extract:
- Core value (the ONE thing that must work)
- Current milestone goals
- Validated requirements (what already exists)

**If research exists:** Read research/FEATURES.md and extract feature categories.

**Present features by category:**

```
Here are the features for [new capabilities]:

## [Category 1]
**Table stakes:**
- Feature A
- Feature B

**Differentiators:**
- Feature C
- Feature D

**Research notes:** [any relevant notes]

---

## [Next Category]
...
```

**If no research:** Gather requirements through conversation instead.

Ask: "What are the main things users need to be able to do with [new features]?"

For each capability mentioned:
- Ask clarifying questions to make it specific
- Probe for related capabilities
- Group into categories

**Scope each category:**

For each category, use AskUserQuestion:

- header: "[Category name]"
- question: "Which [category] features are in this milestone?"
- multiSelect: true
- options:
  - "[Feature 1]" — [brief description]
  - "[Feature 2]" — [brief description]
  - "[Feature 3]" — [brief description]
  - "None for this milestone" — Defer entire category

Track responses:
- Selected features → this milestone's requirements
- Unselected table stakes → future milestone
- Unselected differentiators → out of scope

**Identify gaps:**

Use AskUserQuestion:
- header: "Additions"
- question: "Any requirements research missed? (Features specific to your vision)"
- options:
  - "No, research covered it" — Proceed
  - "Yes, let me add some" — Capture additions

**Generate REQUIREMENTS.md:**

Create `.planning/REQUIREMENTS.md` with:
- v1 Requirements for THIS milestone grouped by category (checkboxes, REQ-IDs)
- Future Requirements (deferred to later milestones)
- Out of Scope (explicit exclusions with reasoning)
- Traceability section (empty, filled by roadmap)

**REQ-ID format:** `[CATEGORY]-[NUMBER]` (AUTH-01, NOTIF-02)

Continue numbering from existing requirements if applicable.

**Requirement quality criteria:**

Good requirements are:
- **Specific and testable:** "User can reset password via email link" (not "Handle password reset")
- **User-centric:** "User can X" (not "System does Y")
- **Atomic:** One capability per requirement (not "User can login and manage profile")
- **Independent:** Minimal dependencies on other requirements

**Present full requirements list:**

Show every requirement (not counts) for user confirmation:

```
## Milestone v[X.Y] Requirements

### [Category 1]
- [ ] **CAT1-01**: User can do X
- [ ] **CAT1-02**: User can do Y

### [Category 2]
- [ ] **CAT2-01**: User can do Z

[... full list ...]

---

Does this capture what you're building? (yes / adjust)
```

If "adjust": Return to scoping.

**Commit requirements:**

Check planning config (same pattern as Phase 6).

If committing:
```bash
git add .planning/REQUIREMENTS.md
git commit -m "$(cat <<'EOF'
docs: define milestone v[X.Y] requirements

[X] requirements across [N] categories
EOF
)"
```

## Phase 9: Create Roadmap

Display stage banner:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► CREATING ROADMAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Spawning roadmapper...


**Determine starting phase number:**

Read MILESTONES.md to find the last phase number from previous milestone.
New phases continue from there (e.g., if v1.0 ended at phase 5, v1.1 starts at phase 6).

Spawn kata-roadmapper agent with context:

```
Task(prompt="
<planning_context>

**Project:**
@.planning/PROJECT.md

**Requirements:**
@.planning/REQUIREMENTS.md

**Research (if exists):**
@.planning/research/SUMMARY.md

**Config:**
@.planning/config.json

**Previous milestone (for phase numbering):**
@.planning/MILESTONES.md

</planning_context>

<instructions>
Create roadmap for milestone v[X.Y]:
1. Start phase numbering from [N] (continues from previous milestone)
2. Derive phases from THIS MILESTONE's requirements (don't include validated/existing)
3. Map every requirement to exactly one phase
4. Derive 2-5 success criteria per phase (observable user behaviors)
5. Validate 100% coverage of new requirements
6. Write files immediately (ROADMAP.md, STATE.md, update REQUIREMENTS.md traceability)
7. Return ROADMAP CREATED with summary

Write files first, then return. This ensures artifacts persist even if context is lost.
</instructions>
", subagent_type="kata-roadmapper", model="{roadmapper_model}", description="Create roadmap")
```

**Handle roadmapper return:**

**If `## ROADMAP BLOCKED`:**
- Present blocker information
- Work with user to resolve
- Re-spawn when resolved

**If `## ROADMAP CREATED`:**

Read the created ROADMAP.md and present it nicely inline:

```
---

## Proposed Roadmap

**[N] phases** | **[X] requirements mapped** | All milestone requirements covered ✓

| #     | Phase  | Goal   | Requirements | Success Criteria |
| ----- | ------ | ------ | ------------ | ---------------- |
| [N]   | [Name] | [Goal] | [REQ-IDs]    | [count]          |
| [N+1] | [Name] | [Goal] | [REQ-IDs]    | [count]          |
...

### Phase Details

**Phase [N]: [Name]**
Goal: [goal]
Requirements: [REQ-IDs]
Success criteria:
1. [criterion]
2. [criterion]

[... continue for all phases ...]

---
```

**CRITICAL: Ask for approval before committing:**

Use AskUserQuestion:
- header: "Roadmap"
- question: "Does this roadmap structure work for you?"
- options:
  - "Approve" — Commit and continue
  - "Adjust phases" — Tell me what to change
  - "Review full file" — Show raw ROADMAP.md

**If "Approve":** Continue to commit.

**If "Adjust phases":**
- Get user's adjustment notes
- Re-spawn roadmapper with revision context:
  ```
  Task(prompt="
  <revision>
  User feedback on roadmap:
  [user's notes]

  Current ROADMAP.md: @.planning/ROADMAP.md

  Update the roadmap based on feedback. Edit files in place.
  Return ROADMAP REVISED with changes made.
  </revision>
  ", subagent_type="kata-roadmapper", model="{roadmapper_model}", description="Revise roadmap")
  ```
- Present revised roadmap
- Loop until user approves

**If "Review full file":** Display raw `cat .planning/ROADMAP.md`, then re-ask.

**Commit roadmap (after approval):**

Check planning config (same pattern as Phase 6).

If committing:
```bash
git add .planning/ROADMAP.md .planning/STATE.md .planning/REQUIREMENTS.md
git commit -m "$(cat <<'EOF'
docs: create milestone v[X.Y] roadmap ([N] phases)

Phases:
[N]. [phase-name]: [requirements covered]
[N+1]. [phase-name]: [requirements covered]
...

All milestone requirements mapped to phases.
EOF
)"
```

## Phase 9.5: Create Phase Issues (if enabled)

**1. Check github.enabled** - Skip silently if false

**If `GITHUB_ENABLED=false`:** Skip to Phase 10.

**2. Check github.issueMode** (auto | ask | never):

```bash
ISSUE_MODE=$(cat .planning/config.json 2>/dev/null | grep -o '"issueMode"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "auto")
```

- If "never": Skip phase issue creation silently, continue to Phase 10
- If "ask": Use AskUserQuestion to prompt:
  - header: "GitHub Phase Issues"
  - question: "Create GitHub Issues for each phase in this milestone?"
  - options:
    - "Yes" — Create issues for all phases
    - "No" — Skip issue creation for this milestone

- If "auto" or user approved "Yes": Proceed with creation

**3. Create phase label (idempotent)**:

```bash
gh label create "phase" --color "0E8A16" --description "Kata phase tracking" --force 2>/dev/null || true
```

**4. Get milestone number** (from Phase 5.5):

```bash
MILESTONE_NUM=$(gh api /repos/:owner/:repo/milestones --jq ".[] | select(.title==\"v${VERSION}\") | .number" 2>/dev/null)
if [ -z "$MILESTONE_NUM" ]; then
  echo "Warning: Could not find GitHub Milestone v${VERSION}. Skipping phase issue creation."
  # Continue without phase issues - skip to Phase 10
fi
```

**5. Parse phases from ROADMAP.md** (for this milestone only):

The ROADMAP.md structure uses:
- Milestone headers: `### v1.1.0 GitHub Integration (Planned)` or `### v{VERSION} {Name} (Status)`
- Phase headers: `#### Phase N: Phase Name`
- Goal line: `**Goal**: description text`
- Requirements line: `**Requirements**: REQ-01, REQ-02` (optional)
- Success criteria: `**Success Criteria** (what must be TRUE):` followed by numbered list

```bash
# Find the milestone section and extract phases
# VERSION is already set (e.g., "1.1.0")

ROADMAP_FILE=".planning/ROADMAP.md"

# Get line numbers for milestone section boundaries
MILESTONE_START=$(grep -n "^### v${VERSION}" "$ROADMAP_FILE" | head -1 | cut -d: -f1)
NEXT_MILESTONE=$(awk -v start="$MILESTONE_START" 'NR > start && /^### v[0-9]/ {print NR; exit}' "$ROADMAP_FILE")

# If no next milestone, use end of file
if [ -z "$NEXT_MILESTONE" ]; then
  NEXT_MILESTONE=$(wc -l < "$ROADMAP_FILE")
fi

# Extract phase blocks within this milestone section
# Each phase starts with "#### Phase N:" and ends at next "#### Phase" or section boundary
PHASE_HEADERS=$(sed -n "${MILESTONE_START},${NEXT_MILESTONE}p" "$ROADMAP_FILE" | grep -n "^#### Phase [0-9]")

# Process each phase
echo "$PHASE_HEADERS" | while IFS= read -r phase_line; do
  # Extract phase number and name from "#### Phase N: Name"
  PHASE_NUM=$(echo "$phase_line" | sed -E 's/.*Phase ([0-9.]+):.*/\1/')
  PHASE_NAME=$(echo "$phase_line" | sed -E 's/.*Phase [0-9.]+: (.*)/\1/')

  # Get relative line number within milestone section
  PHASE_REL_LINE=$(echo "$phase_line" | cut -d: -f1)
  PHASE_ABS_LINE=$((MILESTONE_START + PHASE_REL_LINE - 1))

  # Find next phase or section end
  NEXT_PHASE_LINE=$(sed -n "$((PHASE_ABS_LINE+1)),${NEXT_MILESTONE}p" "$ROADMAP_FILE" | grep -n "^#### Phase\|^### \|^## " | head -1 | cut -d: -f1)
  if [ -z "$NEXT_PHASE_LINE" ]; then
    PHASE_END=$NEXT_MILESTONE
  else
    PHASE_END=$((PHASE_ABS_LINE + NEXT_PHASE_LINE - 1))
  fi

  # Extract phase block
  PHASE_BLOCK=$(sed -n "${PHASE_ABS_LINE},${PHASE_END}p" "$ROADMAP_FILE")

  # Extract goal (line starting with **Goal**:)
  PHASE_GOAL=$(echo "$PHASE_BLOCK" | grep "^\*\*Goal\*\*:" | sed 's/\*\*Goal\*\*: *//')

  # Extract requirements (line starting with **Requirements**:) - may not exist
  REQUIREMENT_IDS=$(echo "$PHASE_BLOCK" | grep "^\*\*Requirements\*\*:" | sed 's/\*\*Requirements\*\*: *//')

  # Extract success criteria (numbered list after **Success Criteria**)
  # Convert to checklist format: "  1. item" -> "- [ ] item"
  SUCCESS_CRITERIA_AS_CHECKLIST=$(echo "$PHASE_BLOCK" | \
    awk '/^\*\*Success Criteria\*\*/{found=1; next} found && /^  [0-9]+\./{print} found && /^\*\*/{exit}' | \
    sed -E 's/^  [0-9]+\. /- [ ] /')

  # --- Issue creation code (step 6) ---

  # Check if issue already exists (idempotent)
  EXISTING=$(gh issue list --label "phase" --milestone "v${VERSION}" --json number,title --jq ".[] | select(.title | startswith(\"Phase ${PHASE_NUM}:\")) | .number" 2>/dev/null)

  if [ -n "$EXISTING" ]; then
    echo "Phase ${PHASE_NUM} issue already exists: #${EXISTING}"
  else
    # Build issue body using temp file (handles special characters safely)
    cat > /tmp/phase-issue-body.md << PHASE_EOF
## Goal

${PHASE_GOAL}

## Success Criteria

${SUCCESS_CRITERIA_AS_CHECKLIST}
$([ -n "$REQUIREMENT_IDS" ] && echo "
## Requirements

${REQUIREMENT_IDS}")

## Plans

<!-- Checklist added by /kata:planning-phases (Phase 4) -->
_Plans will be added after phase planning completes._

---
<sub>Created by Kata | Phase ${PHASE_NUM} of milestone v${VERSION}</sub>
PHASE_EOF

    # Create issue
    gh issue create \
      --title "Phase ${PHASE_NUM}: ${PHASE_NAME}" \
      --body-file /tmp/phase-issue-body.md \
      --label "phase" \
      --milestone "v${VERSION}" \
      2>/dev/null && echo "Created issue: Phase ${PHASE_NUM}: ${PHASE_NAME}" || echo "Warning: Failed to create issue for Phase ${PHASE_NUM}"
  fi
done
```

**6. Display summary** (after loop):

```
◆ GitHub Phase Issues: [N] created for milestone v${VERSION}
```

**Error handling principle:** All operations are non-blocking. Missing milestone, auth issues, or creation failures warn but do not stop the milestone flow.

**IMPORTANT:** Use temp file approach (--body-file) to handle special characters in phase goals. Direct --body strings break with quotes/backticks.

## Phase 10: Done

Present completion with next steps:


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► MILESTONE INITIALIZED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Milestone v[X.Y]: [Name]**

| Artifact     | Location                    |
| ------------ | --------------------------- |
| Project      | `.planning/PROJECT.md`      |
| Research     | `.planning/research/`       |
| Requirements | `.planning/REQUIREMENTS.md` |
| Roadmap      | `.planning/ROADMAP.md`      |

**If `GITHUB_ENABLED=true` and milestone created:**

| GitHub       | Milestone v${VERSION} created |

**[N] phases** | **[X] requirements** | Ready to build ✓

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Phase [N]: [Phase Name]** — [Goal from ROADMAP.md]

`/kata:discuss-phase [N]` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/kata:plan-phase [N]` — skip discussion, plan directly

───────────────────────────────────────────────────────────────


</process>

<success_criteria>
- [ ] PROJECT.md updated with Current Milestone section
- [ ] STATE.md reset for new milestone
- [ ] MILESTONE-CONTEXT.md consumed and deleted (if existed)
- [ ] Research completed (if selected) — 4 parallel agents spawned, milestone-aware
- [ ] Requirements gathered (from research or conversation)
- [ ] User scoped each category
- [ ] REQUIREMENTS.md created with REQ-IDs
- [ ] kata-roadmapper spawned with phase numbering context
- [ ] Roadmap files written immediately (not draft)
- [ ] User feedback incorporated (if any)
- [ ] ROADMAP.md created with phases continuing from previous milestone
- [ ] All commits made (if planning docs committed)
- [ ] User knows next step is `/kata:discuss-phase [N]`

**Atomic commits:** Each phase commits its artifacts immediately. If context is lost, artifacts persist.
</success_criteria>
