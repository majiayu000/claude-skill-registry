---
name: planning-phases
description: Use this skill to plan detailed roadmap phases. Triggers include "plan phase n", "create phase plan", "create a plan" "roadmap planning", and "roadmap phase creation".
metadata:
  version: "0.1.0"
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Bash
---

<user_command>/kata:plan-phase</user_command>


<execution_context>
@./references/ui-brand.md
</execution_context>

<objective>
Create executable phase prompts (PLAN.md files) for a roadmap phase with integrated research and verification.

**Default flow:** Research (if needed) → Plan → Verify → Done

**Orchestrator role:** Parse arguments, validate phase, research domain (unless skipped or exists), spawn kata-planner agent, verify plans with kata-plan-checker, iterate until plans pass or max iterations reached, present results.

**Why subagents:** Research and planning burn context fast. Verification uses fresh context. User sees the flow between agents in main context.
</objective>

<context>
Phase number: $ARGUMENTS (optional - auto-detects next unplanned phase if not provided)

**Flags:**
- `--research` — Force re-research even if RESEARCH.md exists
- `--skip-research` — Skip research entirely, go straight to planning
- `--gaps` — Gap closure mode (reads VERIFICATION.md, skips research)
- `--skip-verify` — Skip planner → checker verification loop

Normalize phase input in step 2 before any directory lookups.
</context>

<process>

## 1. Validate Environment and Resolve Model Profile

```bash
ls .planning/ 2>/dev/null
```

**If not found:** Error - user should run `/kata:new-project` first.

**Resolve model profile for agent spawning:**

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Default to "balanced" if not set.

**Model lookup table:**

| Agent                 | quality | balanced | budget |
| --------------------- | ------- | -------- | ------ |
| kata-phase-researcher | opus    | sonnet   | haiku  |
| kata-planner          | opus    | opus     | sonnet |
| kata-plan-checker     | sonnet  | sonnet   | haiku  |

Store resolved models for use in Task calls below.

## 2. Parse and Normalize Arguments

Extract from $ARGUMENTS:

- Phase number (integer or decimal like `2.1`)
- `--research` flag to force re-research
- `--skip-research` flag to skip research
- `--gaps` flag for gap closure mode
- `--skip-verify` flag to bypass verification loop

**If no phase number:** Detect next unplanned phase from roadmap.

**Normalize phase to zero-padded format:**

```bash
# Normalize phase number (8 → 08, but preserve decimals like 2.1 → 02.1)
if [[ "$PHASE" =~ ^[0-9]+$ ]]; then
  PHASE=$(printf "%02d" "$PHASE")
elif [[ "$PHASE" =~ ^([0-9]+)\.([0-9]+)$ ]]; then
  PHASE=$(printf "%02d.%s" "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}")
fi
```

**Check for existing research and plans:**

```bash
ls .planning/phases/${PHASE}-*/*-RESEARCH.md 2>/dev/null
ls .planning/phases/${PHASE}-*/*-PLAN.md 2>/dev/null
```

## 3. Validate Phase

```bash
grep -A5 "Phase ${PHASE}:" .planning/ROADMAP.md 2>/dev/null
```

**If not found:** Error with available phases. **If found:** Extract phase number, name, description.

## 4. Ensure Phase Directory Exists

```bash
# PHASE is already normalized (08, 02.1, etc.) from step 2
PHASE_DIR=$(ls -d .planning/phases/${PHASE}-* 2>/dev/null | head -1)
if [ -z "$PHASE_DIR" ]; then
  # Create phase directory from roadmap name
  PHASE_NAME=$(grep "Phase ${PHASE}:" .planning/ROADMAP.md | sed 's/.*Phase [0-9]*: //' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  mkdir -p ".planning/phases/${PHASE}-${PHASE_NAME}"
  PHASE_DIR=".planning/phases/${PHASE}-${PHASE_NAME}"
fi
```

## 5. Handle Research

**If `--gaps` flag:** Skip research (gap closure uses VERIFICATION.md instead).

**If `--skip-research` flag:** Skip to step 6.

**Check config for research setting:**

```bash
WORKFLOW_RESEARCH=$(cat .planning/config.json 2>/dev/null | grep -o '"research"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
```

**If `workflow.research` is `false` AND `--research` flag NOT set:** Skip to step 6.

**Otherwise:**

Check for existing research:

```bash
ls "${PHASE_DIR}"/*-RESEARCH.md 2>/dev/null
```

**If RESEARCH.md exists AND `--research` flag NOT set:**
- Display: `Using existing research: ${PHASE_DIR}/${PHASE}-RESEARCH.md`
- Skip to step 6

**If RESEARCH.md missing OR `--research` flag set:**

Display stage banner:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► RESEARCHING PHASE {X}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Spawning researcher...


Proceed to spawn researcher

### Spawn kata-phase-researcher

Gather context for research prompt:

```bash
# Get phase description from roadmap
PHASE_DESC=$(grep -A3 "Phase ${PHASE}:" .planning/ROADMAP.md)

# Get requirements if they exist
REQUIREMENTS=$(cat .planning/REQUIREMENTS.md 2>/dev/null | grep -A100 "## Requirements" | head -50)

# Get prior decisions from STATE.md
DECISIONS=$(grep -A20 "### Decisions Made" .planning/STATE.md 2>/dev/null)

# Get phase context if exists
PHASE_CONTEXT=$(cat "${PHASE_DIR}/${PHASE}-CONTEXT.md" 2>/dev/null)
```

Fill research prompt and spawn:

```markdown
<objective>
Research how to implement Phase {phase_number}: {phase_name}

Answer: "What do I need to know to PLAN this phase well?"
</objective>

<context>
**Phase description:**
{phase_description}

**Requirements (if any):**
{requirements}

**Prior decisions:**
{decisions}

**Phase context (if any):**
{phase_context}
</context>

<output>
Write research findings to: {phase_dir}/{phase}-RESEARCH.md
</output>
```

```
Task(
  prompt=research_prompt,
  subagent_type="kata-phase-researcher",
  model="{researcher_model}",
  description="Research Phase {phase}"
)
```

### Handle Researcher Return

**`## RESEARCH COMPLETE`:**
- Display: `Research complete. Proceeding to planning...`
- Continue to step 6

**`## RESEARCH BLOCKED`:**
- Display blocker information
- Offer: 1) Provide more context, 2) Skip research and plan anyway, 3) Abort
- Wait for user response

## 6. Check Existing Plans

```bash
ls "${PHASE_DIR}"/*-PLAN.md 2>/dev/null
```

**If exists:** Offer: 1) Continue planning (add more plans), 2) View existing, 3) Replan from scratch. Wait for response.

## 7. Read Context Files

Read and store context file contents for the planner agent. The `@` syntax does not work across Task() boundaries - content must be inlined.

**Read these files using the Read tool:**
- `.planning/STATE.md` (required)
- `.planning/ROADMAP.md` (required)
- `.planning/REQUIREMENTS.md` (if exists)
- `${PHASE_DIR}/*-CONTEXT.md` (if exists)
- `${PHASE_DIR}/*-RESEARCH.md` (if exists)
- `${PHASE_DIR}/*-VERIFICATION.md` (if --gaps mode)
- `${PHASE_DIR}/*-UAT.md` (if --gaps mode)

Store all content for use in the Task prompt below.

## 8. Spawn kata-planner Agent

Display stage banner:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PLANNING PHASE {X}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Spawning planner...


Fill prompt with inlined content and spawn:

```markdown
<planning_context>

**Phase:** {phase_number}
**Mode:** {standard | gap_closure}

**Project State:**
{state_content}

**Roadmap:**
{roadmap_content}

**Requirements (if exists):**
{requirements_content}

**Phase Context (if exists):**
{context_content}

**Research (if exists):**
{research_content}

**Gap Closure (if --gaps mode):**
{verification_content}
{uat_content}

</planning_context>

<downstream_consumer>
Output consumed by /kata:execute-phase
Plans must be executable prompts with:

- Frontmatter (wave, depends_on, files_modified, autonomous)
- Tasks in XML format
- Verification criteria
- must_haves for goal-backward verification
</downstream_consumer>

<quality_gate>
Before returning PLANNING COMPLETE:

- [ ] PLAN.md files created in phase directory
- [ ] Each plan has valid frontmatter
- [ ] Tasks are specific and actionable
- [ ] Dependencies correctly identified
- [ ] Waves assigned for parallel execution
- [ ] must_haves derived from phase goal
</quality_gate>
```

```
Task(
  prompt=filled_prompt,
  subagent_type="kata-planner",
  model="{planner_model}",
  description="Plan Phase {phase}"
)
```

## 9. Handle Planner Return

Parse planner output:

**`## PLANNING COMPLETE`:**
- Display: `Planner created {N} plan(s). Files on disk.`
- If `--skip-verify`: Skip to step 13
- Check config: `WORKFLOW_PLAN_CHECK=$(cat .planning/config.json 2>/dev/null | grep -o '"plan_check"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")`
- If `workflow.plan_check` is `false`: Skip to step 13
- Otherwise: Proceed to step 10

**`## CHECKPOINT REACHED`:**
- Present to user, get response, spawn continuation (see step 12)

**`## PLANNING INCONCLUSIVE`:**
- Show what was attempted
- Offer: Add context, Retry, Manual
- Wait for user response

## 10. Spawn kata-plan-checker Agent

Display:
`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► VERIFYING PLANS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Spawning plan checker...


Read plans and requirements for the checker:

```bash
# Read all plans in phase directory
PLANS_CONTENT=$(cat "${PHASE_DIR}"/*-PLAN.md 2>/dev/null)

# Read requirements (reuse from step 7 if available)
REQUIREMENTS_CONTENT=$(cat .planning/REQUIREMENTS.md 2>/dev/null)
```

Fill checker prompt with inlined content and spawn:

```markdown
<verification_context>

**Phase:** {phase_number}
**Phase Goal:** {goal from ROADMAP}

**Plans to verify:**
{plans_content}

**Requirements (if exists):**
{requirements_content}

</verification_context>

<expected_output>
Return one of:
- ## VERIFICATION PASSED — all checks pass
- ## ISSUES FOUND — structured issue list
</expected_output>
```

```
Task(
  prompt=checker_prompt,
  subagent_type="kata-plan-checker",
  model="{checker_model}",
  description="Verify Phase {phase} plans"
)
```

## 11. Handle Checker Return

**If `## VERIFICATION PASSED`:**
- Display: `Plans verified. Checking GitHub integration...`
- **Execute Step 13 now** — run the GitHub config check and issue update

**If `## ISSUES FOUND`:**
- Display: `Checker found issues:`
- List issues from checker output
- Check iteration count
- Proceed to step 12

## 12. Revision Loop (Max 3 Iterations)

Track: `iteration_count` (starts at 1 after initial plan + check)

**If iteration_count < 3:**

Display: `Sending back to planner for revision... (iteration {N}/3)`

Read current plans for revision context:

```bash
PLANS_CONTENT=$(cat "${PHASE_DIR}"/*-PLAN.md 2>/dev/null)
```

Spawn kata-planner with revision prompt:

```markdown
<revision_context>

**Phase:** {phase_number}
**Mode:** revision

**Existing plans:**
{plans_content}

**Checker issues:**
{structured_issues_from_checker}

</revision_context>

<instructions>
Make targeted updates to address checker issues.
Do NOT replan from scratch unless issues are fundamental.
Return what changed.
</instructions>
```

```
Task(
  prompt=revision_prompt,
  subagent_type="kata-planner",
  model="{planner_model}",
  description="Revise Phase {phase} plans"
)
```

- After planner returns → spawn checker again (step 10)
- Increment iteration_count

**If iteration_count >= 3:**

Display: `Max iterations reached. {N} issues remain:`
- List remaining issues

Offer options:
1. Force proceed (execute despite issues)
2. Provide guidance (user gives direction, retry)
3. Abandon (exit planning)

Wait for user response.

## 13. GitHub Integration Check

**Check config guards:**

```bash
GITHUB_ENABLED=$(cat .planning/config.json 2>/dev/null | grep -o '"enabled"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
ISSUE_MODE=$(cat .planning/config.json 2>/dev/null | grep -o '"issueMode"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "never")
```

**If `GITHUB_ENABLED != true` OR `ISSUE_MODE = never`:**
- Log: `Skipping GitHub issue update (github.enabled=${GITHUB_ENABLED}, issueMode=${ISSUE_MODE})`
- Skip to `<offer_next>`

**If enabled, find phase issue:**

```bash
# Get milestone version from ROADMAP.md
VERSION=$(grep -oE 'v[0-9]+\.[0-9]+(\.[0-9]+)?' .planning/ROADMAP.md | head -1 | tr -d 'v' || echo "")

if [ -z "$VERSION" ]; then
  echo "Warning: Could not determine milestone version. Skipping GitHub issue update."
  # Continue to offer_next (non-blocking)
fi

# Find phase issue number
ISSUE_NUMBER=$(gh issue list \
  --label "phase" \
  --milestone "v${VERSION}" \
  --json number,title \
  --jq ".[] | select(.title | startswith(\"Phase ${PHASE}:\")) | .number" \
  2>/dev/null)

if [ -z "$ISSUE_NUMBER" ]; then
  echo "Warning: Could not find GitHub Issue for Phase ${PHASE}. Skipping checklist update."
  # Continue to offer_next (non-blocking)
fi
```

**Build plan checklist from PLAN.md files:**

```bash
PLAN_CHECKLIST=""
PLAN_COUNT=0
for plan_file in $(ls "${PHASE_DIR}"/*-PLAN.md 2>/dev/null | sort); do
  PLAN_NUM=$(basename "$plan_file" | sed -E 's/.*-([0-9]+)-PLAN\.md/\1/')
  # Extract brief objective from plan (first line after <objective>)
  PLAN_OBJECTIVE=$(grep -A2 "<objective>" "$plan_file" | head -2 | tail -1 | sed 's/^ *//' | head -c 60)
  # Fallback if objective extraction fails
  if [ -z "$PLAN_OBJECTIVE" ]; then
    PLAN_OBJECTIVE=$(basename "$plan_file" .md | sed 's/-PLAN$//' | sed 's/-/ /g')
  fi
  PLAN_CHECKLIST="${PLAN_CHECKLIST}- [ ] Plan ${PLAN_NUM}: ${PLAN_OBJECTIVE}
"
  PLAN_COUNT=$((PLAN_COUNT + 1))
done
```

**Update issue body with plan checklist:**

```bash
# Read current issue body
ISSUE_BODY=$(gh issue view "$ISSUE_NUMBER" --json body --jq '.body' 2>/dev/null)

if [ -z "$ISSUE_BODY" ]; then
  echo "Warning: Could not read issue #${ISSUE_NUMBER} body. Skipping update."
  # Continue to offer_next (non-blocking)
fi

# Remove placeholder line and add checklist after ## Plans section
# Using awk for multiline manipulation
NEW_BODY=$(echo "$ISSUE_BODY" | awk -v checklist="$PLAN_CHECKLIST" '
  /^## Plans$/ {
    print
    print ""
    print checklist
    getline  # Skip blank line after ## Plans if exists
    if ($0 ~ /^_Plans will be added/) next  # Skip placeholder
    if ($0 ~ /^<!-- Checklist/) next  # Skip comment
    if ($0 == "") next  # Skip blank line before placeholder
    print
    next
  }
  /^_Plans will be added/ { next }  # Remove placeholder anywhere
  { print }
')

# Check if Plans section exists, if not append it
if ! echo "$ISSUE_BODY" | grep -q "^## Plans"; then
  NEW_BODY="${ISSUE_BODY}

## Plans

${PLAN_CHECKLIST}"
fi

# Write to temp file (handles special characters safely)
printf '%s\n' "$NEW_BODY" > /tmp/phase-issue-body.md

# Update issue
gh issue edit "$ISSUE_NUMBER" --body-file /tmp/phase-issue-body.md 2>/dev/null \
  && GITHUB_UPDATE_SUCCESS=true \
  || echo "Warning: Failed to update issue #${ISSUE_NUMBER}"
```

**Track result for display:**

Store `ISSUE_NUMBER` and `PLAN_COUNT` for display in `<offer_next>` if update succeeded.

**After GitHub check completes (success or skip), proceed to Step 14.**

**Error handling principle:** All GitHub operations are non-blocking. Missing issue, auth issues, or update failures warn but do not stop the planning workflow.

## 14. Present Final Status

Display the planning summary and route to `<offer_next>`.

</process>

<offer_next>
Output this markdown directly (not as a code block):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PHASE {X} PLANNED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {X}: {Name}** — {N} plan(s) in {M} wave(s)

| Wave | Plans  | What it builds |
| ---- | ------ | -------------- |
| 1    | 01, 02 | [objectives]   |
| 2    | 03     | [objective]    |

Research: {Completed | Used existing | Skipped}
Verification: {Passed | Passed with override | Skipped}

{If GITHUB_UPDATE_SUCCESS=true:}
GitHub Issue: #{ISSUE_NUMBER} updated with {PLAN_COUNT} plan checklist items

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Execute Phase {X}** — run all {N} plans

/kata:execute-phase {X}

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- cat .planning/phases/{phase-dir}/*-PLAN.md — review plans
- /kata:plan-phase {X} --research — re-research first

───────────────────────────────────────────────────────────────
</offer_next>

<success_criteria>
- [ ] .planning/ directory validated
- [ ] Phase validated against roadmap
- [ ] Phase directory created if needed
- [ ] Research completed (unless --skip-research or --gaps or exists)
- [ ] kata-phase-researcher spawned if research needed
- [ ] Existing plans checked
- [ ] kata-planner spawned with context (including RESEARCH.md if available)
- [ ] Plans created (PLANNING COMPLETE or CHECKPOINT handled)
- [ ] kata-plan-checker spawned (unless --skip-verify)
- [ ] Verification passed OR user override OR max iterations with user decision
- [ ] GitHub issue updated with plan checklist (if github.enabled and issueMode != never)
- [ ] User sees status between agent spawns
- [ ] User knows next steps (execute or review)
</success_criteria>
