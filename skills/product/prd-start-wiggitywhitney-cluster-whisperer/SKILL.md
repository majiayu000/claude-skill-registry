---
name: prd-start
description: Start working on a PRD implementation
category: project-management
arguments:
  - name: prdNumber
    description: PRD number to start working on (e.g., 306)
    required: false
---

# PRD Start - Begin Implementation Work

## Instructions

You are helping initiate active implementation work on a specific Product Requirements Document (PRD). This command sets up the implementation context (validates readiness, creates branch, prepares environment) then hands off to `/prd-next` for task identification.

**IMPORTANT**: Do NOT include time estimates or effort estimates in your responses. Focus on setup and readiness without speculating on duration.

## Process Overview

1. **Select Target PRD** - Identify which PRD to implement
2. **Validate PRD Readiness** - Ensure the PRD is ready for implementation
3. **Set Up Implementation Context** - Create branch and prepare environment
4. **Hand Off to prd-next** - Delegate task identification to the appropriate prompt

## Step 0: Check for PRD Argument

**If `prdNumber` argument is provided ({{prdNumber}}):**
- Skip context check and auto-detection
- Use PRD #{{prdNumber}} directly
- Proceed to Step 2 (PRD Readiness Validation)

**If `prdNumber` argument is NOT provided:**
- Continue to context awareness check below

## Step 0b: Context Awareness Check

**Check if PRD context is already clear from recent conversation:**

**Skip detection if recent conversation shows:**
- **Recent PRD work discussed** - "We just worked on PRD 29", "Just completed PRD update", etc.
- **Specific PRD mentioned** - "PRD #X", "MCP Prompts PRD", etc.
- **PRD-specific commands used** - Recent use of `/prd-update-progress`, `/prd-start` with specific PRD
- **Clear work context** - Discussion of specific features, tasks, or requirements for a known PRD

**If context is clear:**
- Skip to Step 2 (PRD Readiness Validation) using the known PRD

**If context is unclear:**
- Continue to Step 1 (PRD Detection)

## Step 1: Smart PRD Detection (Only if Context Unclear)

**Auto-detect the target PRD using these context clues (in priority order):**

1. **Git Branch Analysis** - Check current branch name for PRD patterns:
   - `feature/prd-12-*` → PRD 12
   - `prd-13-*` → PRD 13
   - `feature/prd-*` → Extract PRD number

2. **Recent Git Commits** - Look at recent commit messages for PRD references:
   - "fix: PRD 12 documentation" → PRD 12
   - "feat: implement prd-13 features" → PRD 13

3. **Git Status Analysis** - Check modified/staged files for PRD clues:
   - Modified `prds/12-*.md` → PRD 12
   - Changes in feature-specific directories

4. **Available PRDs Discovery** - List all PRDs in `prds/` directory

5. **Fallback to User Choice** - Only if context detection fails, ask user to specify

**Detection Logic:**
- **High Confidence**: Branch name matches PRD pattern (e.g., `feature/prd-12-documentation-testing`)
- **Medium Confidence**: Modified PRD files in git status or recent commits mention PRD
- **Low Confidence**: Multiple PRDs available, use heuristics (most recent, largest)
- **No Context**: Present available options to user

**If context detection fails, ask the user:**

```markdown
## Which PRD would you like to start implementing?

Please provide the PRD number (e.g., "12", "PRD 12", or "36").

**Not sure which PRD to work on?**
Execute `dot-ai:prds-get` prompt to see all available PRDs organized by priority and readiness.

**Your choice**: [Wait for user input]
```

**Once PRD is identified:**
- Read the PRD file from `prds/[issue-id]-[feature-name].md`

## Step 2: PRD Readiness Validation

Before starting implementation, validate that the PRD is ready:

### Requirements Validation
- **Functional Requirements**: Are core requirements clearly defined and complete?
- **Success Criteria**: Are measurable success criteria established?
- **Dependencies**: Are all external dependencies identified and available?
- **Risk Assessment**: Have major risks been identified and mitigation plans created?

### Documentation Analysis
For documentation-first PRDs:
- **Specification completeness**: Is the feature fully documented with user workflows?
- **Integration points**: Are connections with existing features documented?
- **API/Interface definitions**: Are all interfaces and data structures specified?
- **Examples and usage**: Are concrete usage examples provided?

### Implementation Readiness Checklist
```markdown
## PRD Readiness Check
- [ ] All functional requirements defined
- [ ] Success criteria measurable
- [ ] Dependencies available
- [ ] Documentation complete
- [ ] Integration points clear
- [ ] Implementation approach decided
```

**If PRD is not ready:** Inform the user what's missing and suggest they complete PRD planning first.

## Step 3: Implementation Context Setup

**⚠️ MANDATORY: Complete this step BEFORE proceeding to Step 4**

### Git Branch Management

1. **Check current branch**: Run `git branch --show-current`
2. **If on `main` or `master`**: Create and switch to feature branch:
   ```bash
   git checkout -b feature/prd-[issue-id]-[feature-name]
   ```
3. **If already on a feature branch**: Verify it's the correct branch for this PRD

### Development Environment Setup
- **Dependencies**: Install any new dependencies required by the PRD
- **Configuration**: Set up any configuration needed for development
- **Test data**: Prepare test data or mock services

### Step 3 Checkpoint (REQUIRED)

**You MUST display this confirmation before proceeding to Step 4:**

```markdown
## Environment Setup ✅
- **Branch**: `[current-branch-name]` ✅
- **Status**: [Created new branch / Already on correct branch / Staying on main (reason)]
```

**DO NOT proceed to Step 4 until branch setup is confirmed.**

## Step 4: Hand Off to prd-next

Once the implementation context is set up, present this message to the user:

```markdown
## Ready for Implementation 🚀

**PRD**: [PRD Name] (#[PRD Number])
**Branch**: `[branch-name]`
**Status**: Ready for development

---

To identify and start working on your first task, run `/prd-next`.
```

**⚠️ STOP HERE - DO NOT:**
- Identify or recommend tasks to work on
- Analyze implementation priorities or critical paths
- Start any implementation work
- Continue beyond presenting the handoff message

`/prd-next` handles all task identification and implementation guidance.

## Success Criteria

This command should:
- ✅ Successfully identify the target PRD for implementation
- ✅ Validate that the PRD is ready for development work
- ✅ Set up proper implementation context (branch, environment)
- ✅ Hand off to `/prd-next` for task identification
- ✅ Bridge the gap between PRD planning and development setup

## Notes

- This command focuses on **setup only** - it validates readiness, creates the branch, and prepares the environment
- Once setup is complete, `/prd-next` handles all task identification, implementation guidance, and progress tracking
