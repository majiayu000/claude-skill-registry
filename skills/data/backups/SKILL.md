---
name: skill-editor
description: Multi-agent workflow for editing Claude Code skills with quality gates
version: 1.0.0
tags: [meta, workflow, skill-development, multi-agent]
---

# Skill Editor

Comprehensive multi-agent workflow system for editing Claude Code skills with structured phases, quality gates, and expert review.

## When to Use This Skill

Use this skill when:

1. **Creating new skills**: User wants to add a new skill to the repository
2. **Modifying existing skills**: User wants to update, enhance, or refactor a skill
3. **Complex skill changes**: Change involves multiple files, agents, or architectural decisions
4. **Quality assurance needed**: Change requires thorough review and validation

This skill provides:
- Structured 4-phase workflow
- Interactive requirements refinement
- Parallel expert analysis (3 simultaneous agents)
- Adversarial review before implementation
- Automated validation and testing
- Integration with sync-config.py and planning journal

## When NOT to Use This Skill

Do NOT use this skill when:

- **Simple documentation fixes**: Typo fixes, minor documentation updates (edit directly)
- **Non-skill changes**: Modifying agents, settings, or other configuration
- **Urgent hotfixes**: Emergency fixes that can't wait for full workflow
- **Exploratory work**: Just browsing or understanding skills (use Read or Explore agent)

## Four-Phase Workflow

```
Phase 1: REFINEMENT (10-30 min)
├─→ request-refiner: Interactive specification
└─→ Quality Gate 1: User approves specification

Phase 2: PARALLEL ANALYSIS (30-60 min)
├─→ best-practices-reviewer ┐
├─→ external-researcher      ├─ Run in parallel
├─→ edge-case-simulator     ┘
└─→ Quality Gate 2: All analyses complete

Phase 3: DECISION & REVIEW (45-90 min)
├─→ decision-synthesizer: Synthesize + user collaboration
├─→ adversarial-reviewer: Expert review with exact file paths
└─→ Quality Gate 3: User approves plan

Phase 4: EXECUTION (60-120 min)
├─→ executor: Implement, validate, sync, test, commit
├─→ Quality Gate 4: Pre-sync validation
└─→ Quality Gate 5: Post-execution verification
```

## Workflow

### Pre-Workflow: Safety Checks

Before starting workflow:

```bash
# Check git status
git status
# Should be clean or show only tracked files

# Check sync status
./sync-config.py status
# Should show "No changes detected" or expected divergence

# Verify in correct directory
pwd
# Should be repo root: /Users/davidangelesalbores/repos/claude

# Create session directory for output files
mkdir -p /tmp/skill-editor-session
echo "Session directory: /tmp/skill-editor-session"
```

If checks fail: Ask user to resolve before proceeding.

### Phase 1: Refinement (Interactive)

**Objective**: Transform user's request into detailed, unambiguous specification.

**Agent**: `skill-editor-request-refiner`

**Model**: Opus 4.5

**Process**:

1. Launch request-refiner agent via Task tool
2. Agent asks clarifying questions to understand:
   - What user wants to change
   - Why they want this change
   - What success looks like
   - What's in scope vs. out of scope
3. Agent reads existing skill (if modifying)
4. Agent establishes clear boundaries and success criteria
5. Agent presents refined specification to user

**Output File**: `/tmp/skill-editor-session/refined-specification.md` containing:
- Objective (one sentence)
- Scope (IN/OUT lists)
- Success criteria (measurable)
- Files affected
- User approval

**Quality Gate 1: Specification Approval**

User must approve:
- [ ] Specification matches intent
- [ ] Scope is appropriate
- [ ] Success criteria are clear
- [ ] Ready to proceed to analysis

**If Gate 1 fails**: Return to request-refiner for more refinement.

**If Gate 1 passes**: Proceed to Phase 2.

---

### Phase 2: Parallel Analysis (3 Simultaneous Agents)

**Objective**: Analyze proposed change from multiple expert perspectives.

**Agents** (all run in parallel):
1. `skill-editor-best-practices-reviewer` (Opus 4.5)
2. `skill-editor-external-researcher` (Opus 4.5)
3. `skill-editor-edge-case-simulator` (Opus 4.5)

**Process**:

Launch all 3 agents in parallel (single message with 3 Task tool calls):

```markdown
Task 1: best-practices-reviewer
- Reviews against Anthropic guidelines
- Checks skill structure specification
- Identifies architectural concerns

Task 2: external-researcher
- Searches community patterns and forums
- Finds relevant documentation and examples
- Identifies recommended approaches

Task 3: edge-case-simulator
- Simulates failure scenarios
- Identifies edge cases
- Proposes handling strategies
```

**Important**: All 3 agents run simultaneously (not sequential). Wait for all to complete before proceeding.

**Output Files** (must be created before proceeding to Phase 3):
- `/tmp/skill-editor-session/best-practices-review.md`
- `/tmp/skill-editor-session/external-research.md`
- `/tmp/skill-editor-session/edge-cases.md`

**Verification**: Before Phase 3, verify all output files exist:
```bash
ls -lh /tmp/skill-editor-session/*.md
# Should show all 3 files with content
```

**Quality Gate 2: Analysis Completion**

Check agent completion status:
- **All 3 agents complete**: ✅ Proceed to Phase 3
- **2 of 3 agents complete**: ⚠️ Ask user to proceed with partial analysis or retry failed agent
- **<2 agents complete**: ❌ Must retry failed agents or abort workflow

Additional checks:
- [ ] No critical blocking issues flagged
- [ ] No conflicting recommendations (or conflicts documented for synthesis)
- [ ] Sufficient information for decision-making

**If all 3 agents fail**: Stop workflow, investigate environment/configuration issues.

**If partial completion (2/3)**:
```
The [failed-agent-name] agent did not complete.

Options:
1. Proceed with analysis from 2 agents (faster, less comprehensive)
2. Retry failed agent (more thorough, takes more time)
3. Abort workflow

Recommendation: If failed agent is external-researcher, safe to proceed.
If best-practices-reviewer or edge-case-simulator failed, retry recommended.
```

**If Gate 2 passes**: Proceed to Phase 3.

---

### Phase 3: Decision & Review (Synthesis + Adversarial)

**Objective**: Synthesize analyses, make decisions, create plan, get expert approval.

#### Part A: Decision Synthesis

**Agent**: `skill-editor-decision-synthesizer`

**Model**: Opus 4.5 (critical decision-making)

**Process**:

1. Read all 3 analysis reports + refined specification
2. Identify consensus and conflicts
3. Resolve conflicts or present options to user:
   - **Major decisions**: MUST ask user (new agents, structure changes)
   - **Medium decisions**: SHOULD ask user (workflow changes)
   - **Minor decisions**: Agent decides (examples, docs)
4. Create detailed implementation plan with:
   - Exact file paths
   - Specific changes (line numbers if possible)
   - Edge case handling
   - Git workflow
   - Validation steps
   - Rollback plan

**Output File**: `/tmp/skill-editor-session/implementation-plan.md`

#### Part B: Adversarial Review

**Agent**: `skill-editor-adversarial-reviewer`

**Model**: Opus 4.5 (expert review)

**Process**:

1. Read implementation plan with expert skepticism
2. Challenge assumptions and approach
3. Identify failure modes not caught by analysis
4. Verify exact file paths (run bash checks)
5. Verify git workflow safety
6. Check alignment with original specification
7. Provide go/no-go decision

**Output File**: `/tmp/skill-editor-session/adversarial-review.md` containing:
- Architecture assessment
- Failure mode analysis
- Integration risk assessment
- Exact file path verification
- Git workflow verification
- Final decision: ✅ GO / ⚠️ CONDITIONAL / ❌ NO-GO

**Quality Gate 3: Plan Approval**

Check:
- [ ] Implementation plan has exact file paths
- [ ] Git workflow is safe and correct
- [ ] Integration points identified
- [ ] No architectural concerns
- [ ] Adversarial reviewer approved (GO or CONDITIONAL with fixes applied)
- [ ] User approves plan

**If Gate 3 fails**:
- If CONDITIONAL: Fix issues, re-review
- If NO-GO: Return to decision-synthesizer, revise plan
- If user doesn't approve: Refine plan or return to Phase 1

**If Gate 3 passes**: Proceed to Phase 4.

---

### Phase 4: Execution (Implement + Validate + Commit)

**Objective**: Execute approved plan with validation at each step.

**Agent**: `skill-editor-executor`

**Model**: Opus 4.5

**Process**:

#### Step 1: Pre-Implementation Safety

```bash
git status  # Must be clean
./sync-config.py status  # Must be synced
pwd  # Must be repo root
```

Stop if any check fails.

#### Step 2: Implement Changes

For each file in implementation plan:
- **Edit**: Read first, then Edit with exact string replacement
- **Create**: Write new file
- **Delete**: Remove file

#### Step 3: Quality Gate 4 - Pre-Sync Validation

Validate before syncing to `~/.claude/`:

```bash
# Validate YAML (for skills)
for skill in claude-config/skills/*/SKILL.md; do
  python3 -c "import yaml; yaml.safe_load(open('$skill').read().split('---')[1])"
done

# Validate JSON (for agents)
for agent in claude-config/agents/*.json; do
  python3 -m json.tool "$agent" > /dev/null
done

# Dry-run sync
./sync-config.py push --dry-run
```

**Quality Gate 4 Checklist**:
- [ ] YAML frontmatter validates
- [ ] JSON validates (if agents modified)
- [ ] Skill structure follows specification
- [ ] File naming conventions followed
- [ ] No conflicting settings
- [ ] Dry-run sync succeeds

**If Gate 4 fails**: Fix issues, re-validate, do NOT proceed until pass.

#### Step 4: Sync to ~/.claude/

```bash
# Sync (prompts user for confirmation)
./sync-config.py push

# Verify
./sync-config.py status  # Should show no divergence
```

#### Step 5: Test Skill Invocation

```bash
# Create test script
cat > /tmp/test-skill.sh << 'EOF'
#!/bin/bash
SKILL_NAME="$1"
# Check skill exists
[ -f "$HOME/.claude/skills/$SKILL_NAME/SKILL.md" ] || exit 1
# Check YAML parses
python3 -c "import yaml; yaml.safe_load(open('$HOME/.claude/skills/$SKILL_NAME/SKILL.md').read().split('---')[1])"
EOF
chmod +x /tmp/test-skill.sh

# Test skill
/tmp/test-skill.sh {skill-name}

# Smoke test existing skills (no regressions)
/tmp/test-skill.sh skill-editor
/tmp/test-skill.sh completion-verifier
```

#### Step 6: Quality Gate 5 - Post-Execution Verification

**Quality Gate 5 Checklist**:
- [ ] Original requirement met (from refined spec)
- [ ] Edge cases handled (from edge-case report)
- [ ] sync-config.py push successful
- [ ] Skill invokes without errors
- [ ] No regressions in existing skills
- [ ] Planning journal entry ready

**If Gate 5 fails**: Rollback via `git reset --hard HEAD`, re-sync, fix, retry.

#### Step 7: Update Planning Journal

```bash
./sync-config.py plan --title "[Brief description from refined spec]"

# Document in entry:
# - Objective
# - Changes made (files, lines)
# - Testing results
# - Outcome: Success
```

#### Step 8: Commit Changes

```bash
# Stage specific files (NEVER -A or .)
git add claude-config/skills/{skill-name}/SKILL.md
git add claude-config/skills/{skill-name}/examples/example.md  # if created
git add claude-config/agents/{agent-name}.json  # if modified
git add planning/$(hostname)/*.md

# Commit with HEREDOC (multi-line message)
git commit -m "$(cat <<'EOF'
feat(skill-name): [Brief description]

[Detailed description from implementation plan]

Changes:
- Modified SKILL.md: [what changed]
- Added example: [why]

Testing:
- Validated YAML
- Tested invocation
- No regressions

See planning/$(hostname)/[date]-[title].md

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Verify commit
git log -1 --stat
```

**Git Safety Checklist**:
- [ ] Specific files staged (not -A or .)
- [ ] Conventional commit format (feat/fix/docs)
- [ ] Descriptive message
- [ ] Co-authored-by line
- [ ] No destructive operations
- [ ] No hook bypasses

#### Step 9: Report Completion

Generate completion report with:
- Summary of changes
- Validation results (Gates 4 & 5)
- Testing results
- Commit SHA
- Planning journal entry path
- Success criteria verification

---

## Escalation Framework

Decision thresholds (from CONFIG_MANAGEMENT.md):

### Major Decisions → User Approval Required

- Add new agent to workflow
- Change skill structure specification
- Modify core workflow phases

**Action**: Use AskUserQuestion before proceeding

### Medium Decisions → User Approval Required

- Modify existing skill's core workflow
- Add new supporting skill
- Change skill naming convention

**Action**: Use AskUserQuestion with options

### Minor Decisions → Agent Decides

- Add example to existing skill
- Fix documentation typo
- Update reference material

**Action**: Proceed, notify user

## Error Handling

### If Any Phase Fails

1. **Stop immediately**
2. **Document error**
3. **Rollback if needed**: `git reset --hard HEAD`
4. **Re-sync**: `./sync-config.py push`
5. **Report to user**
6. **Ask**: Retry, skip, or abort?

### If Validation Fails (Gate 4 or 5)

1. **Do NOT proceed**
2. **Fix issues in claude-config/**
3. **Re-validate**
4. **Continue only when validated**

### If User Cancels (Ctrl+C)

1. **Check git status**
2. **Rollback uncommitted changes**: `git reset --hard HEAD`
3. **Re-sync**: `./sync-config.py push`
4. **Document in planning journal**: "Cancelled by user"

## Integration with Existing Tools

### CONFIG_MANAGEMENT.md

This workflow extends the 7-step CONFIG_MANAGEMENT.md process:

- **Step 1 (Safety Check)**: Pre-workflow checks
- **Step 2 (Planning Entry)**: Phase 4, Step 7
- **Step 3 (Implement)**: Phase 4, Step 2
- **Step 4 (Quality Analysis)**: Phases 2-3, Quality Gates
- **Step 5 (Preview/Sync)**: Phase 4, Steps 3-4
- **Step 6 (Test)**: Phase 4, Step 5
- **Step 7 (Commit)**: Phase 4, Step 8

### sync-config.py

Executor agent uses sync-config.py:
- `./sync-config.py status` (pre-flight check)
- `./sync-config.py push --dry-run` (validation)
- `./sync-config.py push` (apply changes)
- `./sync-config.py plan` (create planning entry)

### Planning Journal

Planning entry created in Phase 4, Step 7:
- Title: Brief description from refined spec
- Objective: From refined specification
- Changes: Files modified
- Testing: Validation and test results
- Outcome: Success/Partial/Failed

## Quality Gates Summary

| Gate | Phase | Owner | Criteria | Failure Action |
|------|-------|-------|----------|----------------|
| 1 | Phase 1 | request-refiner | Spec approved | Return to refinement |
| 2 | Phase 2 | decision-synthesizer | All analyses complete | Re-run agents |
| 3 | Phase 3 | adversarial-reviewer | Plan approved | Revise plan |
| 4 | Phase 4 | executor | Syntax validated | Fix issues |
| 5 | Phase 4 | executor | Implementation verified | Rollback |

## Examples

### Example 1: Add Parallel Execution to Researcher

**User Request**:
```
/skill-editor "Add parallel web search to researcher skill"
```

**Phase 1 Output**:
```markdown
Objective: Modify researcher skill to execute 3 WebSearch calls in parallel

Scope:
- IN: researcher/SKILL.md Phase 2 workflow
- OUT: No changes to agents or other phases

Success Criteria:
- 3 WebSearch calls execute simultaneously
- Results synthesized correctly
- No regressions
```

**Phase 2 Findings**:
- Best practices: Use Task tool for parallel calls ✅
- Research: Community uses this pattern ✅
- Edge cases: Handle timeout, network failure

**Phase 3 Plan**:
```markdown
Edit: claude-config/skills/researcher/SKILL.md
Lines 45-60: Replace sequential WebSearch with parallel

Implementation:
[3 Task tool calls in single message]
```

**Phase 4 Result**:
```bash
✅ YAML validates
✅ Sync succeeds
✅ Skill invokes correctly
✅ Commit: feat(researcher): Add parallel web search
```

### Example 2: Create New Skill

**User Request**:
```
/skill-editor "Create a new skill for API documentation"
```

**Process**:
- Phase 1: Refine requirements (which APIs? format? tools?)
- Phase 2: Analyze (best practices for doc skills, community patterns, edge cases)
- Phase 3: Plan (file structure, workflow steps, examples)
- Phase 4: Create files, validate, sync, test, commit

## Notes

- **Parallel execution in Phase 2**: All 3 agents run simultaneously (3x faster than sequential)
- **All agents use Opus 4.5**: Maximum quality for all workflow phases (requirements analysis, research, edge cases, decision-making, review, execution)
- **Quality gates enforce standards**: No bypassing validation
- **Rollback on failure**: Safe to abort at any point
- **Planning journal provides traceability**: Full documentation of changes
- **Integration tested**: Works with sync-config.py and existing workflows

## References

See `skill-editor/references/` for:
- `anthropic-guidelines-summary.md`: Anthropic best practices
- `skill-structure-specification.md`: Skill format and validation
- `quality-gates.md`: Detailed quality gate checklists
- `config-management-integration.md`: Integration with CONFIG_MANAGEMENT.md

## Success Criteria

Skill-editor workflow succeeds when:

- [ ] User's original request is fulfilled
- [ ] All quality gates pass
- [ ] Changes are synced to `~/.claude/`
- [ ] Skill invokes without errors
- [ ] No regressions in existing skills
- [ ] Planning journal documents changes
- [ ] Changes committed to git
- [ ] User confirms satisfaction
