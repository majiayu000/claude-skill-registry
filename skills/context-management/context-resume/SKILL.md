---
name: context-resume
description: Load plugin context from handoff files to resume work. Invoked by /continue command, 'resume [PluginName]', 'continue working on [PluginName]', 'pick up where I left off with [PluginName]', or 'show me where [PluginName] is at'. Locates handoff across 2 locations, parses state, presents summary, and routes to appropriate continuation skill.
allowed-tools:
  - Read
  - Bash
  - Skill # To invoke next skill
preconditions:
  - Handoff file must exist in one of 2 locations
---

# context-resume Skill

**Purpose:** Universal entry point for resuming plugin work from `.continue-here.md` handoff files. Handles workflow, ideation, mockup, and improvement resume scenarios.

**Capabilities:**
- Locates handoff files (2 possible locations)
- Parses YAML frontmatter and markdown context
- Presents state summary with time-ago calculation
- Routes to appropriate continuation skill (via Skill tool)
- Graceful error recovery for missing/corrupt handoffs

## Orchestration Protocol

<delegation_rule>

**CRITICAL:** This skill MUST NOT implement workflow stages directly.

When resuming workflow (Stages 0-3), this skill:
1. Locates handoff file
2. Parses context
3. Presents summary to user
4. Checks for `orchestration_mode: true` in handoff YAML
5. If orchestration_mode enabled → Invokes plugin-workflow skill via Skill tool (resume context passed via handoff file, not invocation params)
6. If orchestration_mode disabled → Uses legacy direct routing

**NEVER bypass orchestration_mode.** This enforces the dispatcher pattern:
- plugin-workflow orchestrates
- Subagents implement
- context-resume just loads and routes

See **[references/continuation-routing.md](references/continuation-routing.md)** Step 4a-1 for complete protocol.

**What is orchestration_mode?**

When enabled in handoff YAML, this flag activates the dispatcher pattern: plugin-workflow orchestrates implementation by invoking subagents in fresh contexts. When disabled (legacy mode), context-resume directly routes to implementation skills. Modern workflows always use orchestration_mode for consistent subagent dispatch and clean context isolation.

</delegation_rule>

## Handoff File Locations

The system uses 2 handoff locations, checked in priority order:

**Priority 1: Main Workflow Handoff**
`plugins/[PluginName]/.continue-here.md`

Plugin in active development (Stages 0-3, ideation, improvement planning). Contains stage, phase, orchestration_mode, next_action, completed work, next steps.

**Priority 2: Mockup Handoff**
`plugins/[PluginName]/.ideas/mockups/.continue-here.md`

UI mockup iteration in progress. Contains mockup_version, iteration notes, finalization status.

**Search order:** Priority 1 → 2. If multiple found, present disambiguation menu to user (see references/handoff-location.md Step 1c).

---

## Resume Workflow

**Progress Tracking:**

Copy this checklist to track your progress:

```
Context Resume Progress:
- [ ] Step 1: Locate handoff file (check 2 locations, disambiguate if needed)
- [ ] Step 2: Parse context (YAML + markdown body)
- [ ] Step 3: Present summary (wait for user confirmation)
- [ ] Step 4: Route to continuation skill (load context files first)
```

### Step 1: Locate Handoff File

Search for handoff files across 2 locations (see [Handoff File Locations](#handoff-file-locations) above). Handle interactive plugin selection if no name provided, and present disambiguation menu when multiple handoffs exist for same plugin.

**Details:** [references/handoff-location.md](references/handoff-location.md)

**Validation:** MUST complete before Step 2. If no handoff found, proceed to error recovery.

---

### Step 2: Parse Context

Parse YAML frontmatter (plugin, stage, status, last_updated, etc.) and markdown body (current state, completed work, next steps, key decisions).

**Details:** [references/context-parsing.md](references/context-parsing.md)

**Validation:** MUST complete before Step 3.

---

### Step 3: Present Summary

Calculate "time ago" and build user-facing summary:
- Where we are in workflow
- What's completed
- What's next
- Build/test status
- Time since last session

**Details:** [references/context-parsing.md](references/context-parsing.md) (presentation logic)

**DECISION GATE:** MUST wait for user confirmation. DO NOT auto-proceed. Present numbered decision menu following checkpoint protocol.

---

**VALIDATION GATE:** Before proceeding to Step 4, verify:

1. Handoff parsed successfully (YAML + markdown body extracted)
2. User confirmed continuation (received explicit confirmation, not assumed)
3. Plugin name is known and valid
4. Stage type is identified (workflow/ideation/mockup/improvement)

If any verification fails:
- Return to failed step (Step 1 or Step 2)
- Present error recovery options (see [references/error-recovery.md](references/error-recovery.md))

Only proceed to Step 4 when all verifications pass.

---

### Step 4: Route to Continuation Skill

Determine routing based on stage type (workflow, ideation, mockup, improvement). Load relevant context files (contracts, source code, git history) BEFORE invoking continuation skill.

Routes to plugin-workflow (Stages 0-6), plugin-ideation (ideation/improvements), ui-mockup (mockup iteration), or plugin-improve (improvement implementation) based on stage type and orchestration_mode. See **[references/continuation-routing.md](references/continuation-routing.md)** for complete routing logic.

**Validation:** Requires user confirmation from Step 3.

---

## Error Recovery

Common error scenarios with recovery strategies:

- **No Handoff Found**: Check PLUGINS.md and git log to infer state, offer reconstruction options
- **Corrupted Handoff File**: Parse git log to infer stage, offer manual recreation
- **Stale Handoff (>2 weeks old)**: Warn about staleness, offer to verify code changes
- **Multiple Handoffs for Same Plugin**: Present disambiguation menu with recommendations

See **[references/error-recovery.md](references/error-recovery.md)** for all error scenarios and advanced features.

---

## Integration Points

<integration>

**Inbound (Command triggers):**

1. `/continue` command (no args) → Triggers interactive plugin selection
2. `/continue [PluginName]` command → Triggers specific plugin resume
3. Natural language: "resume [PluginName]", "continue working on [PluginName]"

**Backward Compatibility:**

Handles legacy handoffs with old stage references:
- Old validation stage → Maps to "Stage 3 complete, plugin validated, ready to install"
- Old preset/finalization stage → Maps to "Stage 3 complete, plugin validated, ready to install"
- Detects old stage numbers during parsing (Step 2)
- Automatically migrates to new workflow state
- Presents clear explanation to user

</integration>

<integration>

**Outbound (Skill delegation):**

1. `plugin-workflow` - For workflow resume at specific stage (Stages 0-3)
2. `plugin-ideation` - For ideation resume (improvements or refinement)
3. `ui-mockup` - For mockup iteration resume
4. `plugin-improve` - For improvement implementation resume
5. `workflow-reconciliation` - For corrupt handoff recovery scenarios (state mismatch detection)
6. `system-setup` - If error recovery detects missing dependencies

MUST use Skill tool for invocation, NEVER implement directly.

</integration>

<state_requirement>

**This skill is READ-ONLY for state files.**

MUST read:
- `.continue-here.md` files (all 2 locations)
- PLUGINS.md (status verification)
- Git log (commit history for inference)
- Contract files (creative-brief.md, parameter-spec.md, architecture.md, plan.md)
- Source files (if mentioned in handoff)
- CHANGELOG.md (for improvements)

MUST NOT write:
- Any `.continue-here.md` files
- PLUGINS.md
- Any source code or contract files

**Why:** This skill is an orchestrator - state updates are handled by the continuation skills it delegates to (plugin-workflow, plugin-ideation, ui-mockup, plugin-improve, etc.). Orchestrators read state and route; implementation skills update state and execute checkpoints. See Checkpoint Protocol in CLAUDE.md for state update requirements in implementation skills.

</state_requirement>

---

## Success Criteria

Resume is successful when:

1. **Handoff located:** Found correct handoff file(s) from 2 possible locations
2. **Context parsed:** YAML and markdown extracted without errors
3. **State understood:** User sees clear summary of where they left off
4. **Continuity felt:** User doesn't need to remember details, handoff provides everything
5. **Appropriate routing:** Correct continuation skill invoked with right parameters
6. **Context loaded:** Contract files and relevant code loaded before proceeding
7. **Error handled:** Missing/corrupt handoff handled gracefully with fallbacks
8. **User control:** User explicitly chooses to continue, not auto-proceeded

---

## Execution Requirements

<requirements>

**MUST do when executing this skill:**

1. **ALWAYS** search all 2 handoff locations before declaring "not found"
2. **MUST** parse YAML carefully - handle missing optional fields gracefully
3. **MUST** present time-ago in human-readable format (not raw timestamps)
4. **MUST** show enough context that user remembers where they were
5. **NEVER** auto-proceed - wait for explicit user choice
6. **MUST** load contract files BEFORE invoking continuation skill (provides context)
7. **MUST** use git log as backup IF handoff is missing, stale (>2 weeks old), or corrupt
8. **MUST** preserve user's mental model - summary should match how they think about plugin

</requirements>

<anti_patterns>

**NEVER do these common mistakes:**

- Checking only Priority 1 location and stopping early (MUST check both locations)
- Auto-proceeding after summary without waiting for user confirmation
- Invoking continuation skill before loading contract files
- Presenting raw YAML/markdown instead of formatted human-readable summary
- Auto-selecting when multiple handoffs exist (MUST present disambiguation menu)

</anti_patterns>
