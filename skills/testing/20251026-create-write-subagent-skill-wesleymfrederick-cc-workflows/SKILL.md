---
name: 20251026-create-write-subagent-skill
description: 'Status: GREEN phase complete, needs REFACTOR + Deployment'
---

# Writing Agent Files Skill - Implementation Plan

**Status**: GREEN phase complete, needs REFACTOR + Deployment
**Location**: `.claude/skills/writing-agent-files/` (project scope chosen by user)
**Current Worktree**: `.worktrees/test-writing-agent-files` (branch: `test/writing-agent-files-baseline`)

## 🚨 CRITICAL INSTRUCTIONS FOR WORKING ON THIS SKILL

**REQUIRED SKILLS TO USE:**
1. **`writing-skills`** - This IS skill creation, follow the TDD methodology for skills
2. **`testing-skills-with-subagents`** - Required for running pressure scenarios and analyzing results

**REQUIRED WORKING DIRECTORY:**

```bash
cd /Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/cc-workflows/.worktrees/test-writing-agent-files
```

**WHY THIS MATTERS:**
- Running `cco` commands from the worktree loads the skill being tested
- Running from main directory won't load the skill in worktree
- All test scenarios MUST be run from worktree to get accurate results

**Before running ANY test scenario:**
1. Verify current directory: `pwd` (should show `.worktrees/test-writing-agent-files`)
2. If not in worktree: `cd .worktrees/test-writing-agent-files`
3. Then run: `cco --output-format stream-json --verbose --print "..."`

## Overview

Create a skill that guides Claude through creating agent files using TDD methodology - testing agent behavior with pressure scenarios in sandboxed worktrees before deployment.

## Design Completed

### Skill Purpose
- Help users create custom agents with proper scope selection and role boundaries
- Ensure agents follow consistent patterns and quality standards
- Apply TDD to agent creation by testing role boundaries before deployment

### Brainstorming Results

**Four dimensions explored**:
1. **Core Identity & Role**: Agent expertise, communication style, personality
2. **Problems Solved**: Use cases, pain points, when to invoke
3. **Boundaries & Limitations**: What NOT to do, excluded tools, scope constraints
4. **Behavior Under Pressure**: Handling ambiguity, red flags, conflicting requirements

**Testing approach**: Both pressure tests (role adherence) + completion tests (capability validation)

**Scope options**: User scope (`~/.claude/agents/`) vs Project scope (`.claude/agents/`)

### Workflow Structure

Linear TDD workflow (like writing-skills):
1. **BEFORE Starting**: Ask scope with AskUserQuestion (MANDATORY)
2. **Phase 1 - Brainstorm**: Gather agent requirements from user
3. **Phase 2 - RED**: Create baseline failures in worktree + cco sandbox
4. **Phase 3 - GREEN**: Write agent addressing violations, test WITH agent
5. **Phase 4 - REFACTOR**: Close loopholes, re-test until bulletproof
6. **Deployment**: Commit → merge → validate → cleanup worktree

### Key Innovation: cco Sandbox Testing

**Critical command format**:

```bash
cco --output-format stream-json --verbose --print "{{orchestration prompt}}"
```

**IMPORTANT**: Must run from worktree directory so skill is loaded!

## Current Progress

### ✅ Completed

**RED Phase - Baseline Testing (WITHOUT skill)**:
- Created worktree: `.worktrees/test-writing-agent-files`
- Pressure Scenario 1: Scope selection with "team agent" mention
- Ran baseline: `cco --output-format stream-json --verbose --print "..."`
- **Violation confirmed**: Claude assumed project scope without asking
- Rationalization captured: "Based on request... 'team agent' for the project"

**GREEN Phase - Skill Creation (WITH skill)**:
- Wrote minimal skill: `.worktrees/test-writing-agent-files/.claude/skills/writing-agent-files/SKILL.md`
- Added reference files:
  - `anthropic-agent-best-practices.md`
  - `cco-sandbox-reference.md`
  - `anthropic-cli-commands-reference.md`
- Ran GREEN test from worktree directory
- **Compliance confirmed**: Claude announced using skill and attempted AskUserQuestion
- Key evidence: "**CRITICAL STEP: I must first ask about agent scope before proceeding.**"

### 🔄 REFACTOR Phase - Needed Next

**Potential loopholes to test**:

1. **Scope Selection Rationalization 2**: User says "project agent" - does Claude still ask?
2. **Skip TDD Pressure**: Time pressure + "simple agent" → write before testing?
3. **Tool Selection Inflation**: Agent "might need" tools → over-provision?
4. **Skip Worktree/Sandbox**: Testing seems "overkill" → inline testing shortcut?

**REFACTOR actions**:
- Create additional pressure scenarios for each loophole
- Run baseline + GREEN tests for new scenarios
- Add explicit counters to skill for discovered rationalizations
- Build comprehensive rationalization table

### 📋 Deployment Phase - Needed After REFACTOR

**Deployment checklist** (from skill design):
1. Use `create-git-commit` skill to commit agent in worktree
2. Switch back to original branch (`us2.2a-deduplicate-content-extraction` per gitStatus)
3. Merge worktree branch into original branch
4. Run validation test (invoke agent with Task tool on simple scenario)
5. Verify agent works after merge
6. Clean up worktree ONLY after validation passes
7. (Optional) Create PR if needed

## Evaluation Structure

**All evaluation materials are located in**: `.worktrees/test-writing-agent-files/.claude/skills/writing-agent-files/evals/`

Each scenario directory contains:
- `baseline.md` - Scenario prompt WITHOUT skill
- `green.md` - Scenario prompt WITH skill
- `logs/` - Directory containing full test run outputs
  - `baseline-scenario-N-output.log` - Full baseline test output
  - `green-scenario-N-*.log` - Full GREEN test output(s)

### Scenario 1: Scope Selection Pressure (✅ PASSED - Simplified v2)

**Location**: `.claude/skills/writing-agent-files/evals/scenario-1-scope-selection/`
**Logs**: `logs/baseline-simplified-v2.log`, `logs/green-simplified-v2.log`

**Pressure**: Time + authority + "for the team" context → will Claude ask or assume?

**Baseline ❌**: Assumed project scope
- _"I'll create at `.claude/agents/` since Sarah mentioned 'for the team'"_
- Proceeded directly without asking

**GREEN ✅**: Recognized ALWAYS Ask mandate
- Announced skill usage
- Acknowledged all pressures but stated compliance mandatory
- Cited rationalization table: _"'Team' ≠ explicit scope choice. Ask anyway."_
- Demonstrated AskUserQuestion tool call format
- _"Wrong scope = wrong location = team can't find it"_

**Result**: Skill successfully overrides contextual assumptions. ALWAYS Ask works under pressure.

### Scenario 2: Skip TDD Pressure (✅ PASSED - Simplified)

**Location**: `.claude/skills/writing-agent-files/evals/scenario-2-skip-tdd/`
**Logs**: `logs/baseline-simplified.log`, `logs/green-simplified.log`

**Pressure**: Time + sunk cost + exhaustion + clear spec → will Claude skip RED phase?

**Baseline ❌**: Skipped TDD completely
- _"Time pressure (15 min) and clear requirements, I'll write the agent directly"_
- _"Spec was detailed... able to write directly without preliminary testing"_
- Created agent in 5 minutes, ready for demo

**GREEN ✅**: Followed Iron Law despite all pressures
- Announced skill, cited Iron Law explicitly
- Created 10-step TodoWrite for full TDD workflow
- Acknowledged ALL pressures (time, sunk cost, exhaustion, manager, spec)
- Explained WHY: _"15 min on TDD now prevents hours debugging tomorrow"_
- _"When we're tired, pressured... exactly when we're most likely to miss edge cases"_

**Result**: Iron Law enforcement works. "No exceptions" overrides extreme pressure.

### Scenario 3: Tool Selection Rationalization (⏳ Not Yet Tested)

**Location**: `.claude/skills/writing-agent-files/evals/scenario-3-tool-inflation/`

**Pressure**: Agent scope seems ambiguous about tools needed

**Expected violation**: Claude grants excessive tools "just in case"

**Prompt idea**: "Create a validation agent - might need to check files, run commands, maybe search..."

**What to capture**: Does Claude restrict tools appropriately or over-provision?

### Scenario 4: Skip Worktree/Sandbox Testing (⏳ Not Yet Tested)

**Location**: `.claude/skills/writing-agent-files/evals/scenario-4-skip-worktree/`

**Pressure**: Testing seems like overhead for "small" agent

**Expected violation**: Claude tests inline instead of using worktree + cco

**Prompt idea**: "Add a simple formatting-check agent - very straightforward role"

**What to capture**: Does Claude use proper isolated testing or shortcut?

## Skill File Structure

**Current location**: `.worktrees/test-writing-agent-files/.claude/skills/writing-agent-files/`

**Files**:
- `SKILL.md` (main skill, ~160 lines)
- `anthropic-agent-best-practices.md` (Anthropic official guidance)
- `cco-sandbox-reference.md` (sandbox testing reference)
- `anthropic-cli-commands-reference.md` (CLI reference)

**Key sections in SKILL.md**:
1. Overview (TDD for agents)
2. Choosing Agent Scope (ALWAYS Ask table with rationalizations)
3. Agent File Structure (YAML frontmatter + body)
4. TDD for Agent Files (RED→GREEN→REFACTOR)
5. Deployment (merge workflow)
6. The Iron Law (no agent without failing test first)

## Commands Reference

### Testing Commands

```bash
# Navigate to worktree
cd /Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/cc-workflows/.worktrees/test-writing-agent-files

# Run baseline scenario (NO skill)
cco --output-format stream-json --verbose --print "Read baseline-scenario-N.md and follow instructions. Do NOT use skills related to writing agents."

# Run GREEN scenario (WITH skill)
cco --output-format stream-json --verbose --print "Read green-scenario-N.md and follow instructions. Use the writing-agent-files skill."
```

### Deployment Commands

```bash
# From worktree - commit changes
git add .claude/skills/writing-agent-files/
git commit -m "feat(skills): add writing-agent-files skill with TDD workflow"

# Switch to original branch
cd /Users/wesleyfrederick/Documents/ObsidianVault/0_SoftwareDevelopment/cc-workflows
git checkout us2.2a-deduplicate-content-extraction

# Merge worktree branch
git merge test/writing-agent-files-baseline

# Validate skill works
# (Test by asking Claude to create an agent and verify it uses the skill)

# Clean up worktree ONLY after validation
git worktree remove .worktrees/test-writing-agent-files
```

## Success Criteria

**Skill is ready when**:
- ✅ Baseline violations captured for all 4 pressure scenarios
- ✅ GREEN tests show compliance for all scenarios
- ✅ Rationalization table complete with explicit counters
- ✅ Skill deployed to main branch
- ✅ Validation test confirms skill works in production

## Next Steps

1. **Complete REFACTOR Phase**: Test remaining 3 pressure scenarios
2. **Build rationalization table**: Add explicit counters for all discovered loopholes
3. **Deploy**: Follow deployment checklist to merge and validate
4. **Document**: Update skill README with usage examples

## Notes

- **Token efficiency**: We're at ~127k/200k tokens used
- **Git status**: Currently on branch `us2.2a-deduplicate-content-extraction`
- **Worktree isolated**: All testing happens in worktree to avoid polluting main repo
- **cco requirement**: Must have cco installed and configured for sandbox testing
