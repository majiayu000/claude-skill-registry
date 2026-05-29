---
name: assessor
description: 'Assess a plugin and create refactoring task files for parallel agent execution'
argument-hint: <plugin-name>
user-invocable: true
model: inherit
---

# Review Plugin for Refactor Workflow

You MUST assess a plugin and create comprehensive refactoring plans following this multi-phase workflow. After planning completes, the orchestrator can launch parallel agents to execute tasks.

<plugin_name>
$ARGUMENTS
</plugin_name>

## Mission

EXECUTE all four phases sequentially. Each phase depends on the previous phase's output. After each phase completes, DISPLAY a structured summary with key findings and file paths before proceeding to the next phase.

RETURN to the orchestrator after Phase 4 completes so parallel agent execution can begin.

---

## Completion Tracking (MANDATORY)

**IMMEDIATELY** after reading this command, you MUST create tasks using TaskCreate with this exact checklist:

```
TaskCreate(subject="Phase 1: Generate Plugin Assessment Report", description="Generate comprehensive Plugin Assessment Report by analyzing plugin structure, quality, and refactoring opportunities", activeForm="Generating Plugin Assessment Report")
TaskCreate(subject="Phase 2: Create refactoring design map", description="Create detailed refactoring design specification at .claude/plan/refactor-design-{slug}.md showing how each identified issue should be addressed", activeForm="Creating refactoring design map")
TaskCreate(subject="Phase 3: Create task file", description="Create implementation task file at .claude/plan/tasks-refactor-{slug}.md with dependencies, verification steps, and parallel execution opportunities", activeForm="Creating refactoring task file")
TaskCreate(subject="Phase 3: Update REFACTOR-PLAN.md", description="Update REFACTOR-PLAN.md index with new checklist items for this refactoring project", activeForm="Updating REFACTOR-PLAN.md index")
TaskCreate(subject="Phase 4: Gather refactoring context", description="Gather comprehensive refactoring context for task file including skill content summaries and cross-references", activeForm="Gathering refactoring context")
TaskCreate(subject="Final: Return to orchestrator", description="Return to orchestrator with execution plan and parallelization groups", activeForm="Returning execution plan to orchestrator")
```

**RULES**:

1. Create ALL tasks BEFORE starting Phase 1
2. Mark each task `in_progress` using TaskUpdate BEFORE starting that work
3. Mark each task `completed` using TaskUpdate AFTER verification passes
4. DO NOT display final summary until ALL tasks are `completed`
5. If any verification fails, keep task as `in_progress` and fix before proceeding

---

## Phase 1: Plugin Assessment

**Objective**: Generate a comprehensive Plugin Assessment Report by analyzing the plugin structure, quality, and refactoring opportunities.

**Action**: LAUNCH the plugin-assessor agent using the Task tool with this exact prompt:

```
Task(
    agent="plugin-assessor",
    prompt="""
Your ROLE_TYPE is sub-agent.

Assess the plugin at ./plugins/$ARGUMENTS for structural correctness, quality issues, and refactoring opportunities.

<context>
WHERE you are working:
- Plugin root: ./plugins/$ARGUMENTS
- Plugin manifest: ./plugins/$ARGUMENTS/.claude-plugin/plugin.json
- Skills directory: ./plugins/$ARGUMENTS/skills/
- Commands directory: ./plugins/$ARGUMENTS/commands/ (if exists)
- Agents directory: ./plugins/$ARGUMENTS/agents/ (if exists)

WHAT already exists:
- Reference skills for validation: claude-skills-overview-2026, claude-plugins-reference-2026, claude-hooks-reference-2026
- Plugin schema requirements from Claude Code marketplace
</context>

<success_criteria>
MUST deliver:
1. Complete Plugin Assessment Report with ALL sections populated
2. Overall score out of 100
3. Marketplace readiness determination (Yes / No / With Changes)
4. All skills analyzed with line counts and quality scores
5. All orphaned files identified and classified
6. Specific refactoring recommendations with severity levels
</success_criteria>

<exploration_steps>
EXECUTE the full plugin-assessor protocol:
1. Phase 1: Discovery - scan plugin structure
2. Phase 2: Manifest Validation - validate plugin.json
3. Phase 3: Skills Analysis - analyze all SKILL.md files and references
4. Phase 4: Commands Analysis - if commands/ exists
5. Phase 5: Agents Analysis - if agents/ exists
6. Phase 6: Hooks Validation - if hooks exist
7. Phase 7: MCP Configuration - if .mcp.json exists
8. Phase 8: Cross-Reference Analysis - link validation, orphan detection
9. Phase 9: Enhancement Identification - refactoring opportunities
</exploration_steps>

<output_specification>
GENERATE a Plugin Assessment Report with these key sections:

### Executive Summary
- Overall Score: X/100
- Marketplace Ready: Yes / No / With Changes
- Critical Issues: count
- Skills needing refactoring: list (>500 lines or multi-domain)
- Agents needing optimization: list
- Orphaned files: count

### Skills Analysis Table
| Skill | Lines | Status | Description Quality | Orphans | Refactor Needed |
|-------|-------|--------|---------------------|---------|-----------------|

### Refactoring Recommendations
Categorized by:
- SKILL_SPLIT: Skills >500 lines or covering multiple domains
- AGENT_OPTIMIZE: Agents with vague instructions or poor triggers
- DOC_IMPROVE: Skills/agents with low description quality
- ORPHAN_RESOLVE: Orphaned files needing integration or removal
- STRUCTURE_FIX: Structural issues (broken links, missing files)

Each recommendation must include:
- Target file path
- Issue type and severity (Critical/High/Medium/Low)
- Recommended agent: plugin-creator:refactor-skill | subagent-refactorer | claude-context-optimizer | plugin-docs-writer
- Expected outcome
</output_specification>

<available_resources>
- Full read access to ./plugins/$ARGUMENTS/ directory
- Reference skills loaded: claude-skills-overview-2026, claude-plugins-reference-2026
- Plugin schema validation knowledge
</available_resources>
"""
)
```

**Phase 1 Completion Requirements**:

After the plugin-assessor agent completes, YOU MUST:

1. **UPDATE TASK**: Mark "Phase 1: Generate Plugin Assessment Report" as `in_progress` before verification
2. VERIFY the agent produced a complete Plugin Assessment Report
3. DISPLAY this structured summary:

```
=== PHASE 1 COMPLETE: Plugin Assessed ===

Plugin: $ARGUMENTS
Overall Score: [X/100]
Marketplace Ready: [Yes / No / With Changes]
Critical Issues: [count]

Skills Analyzed: [count]
- Skills >500 lines (refactor candidates): [list]
- Skills with multi-domain coverage: [list]

Agents Analyzed: [count]
- Agents needing optimization: [list]

Orphaned Files: [count]
Documentation Quality Issues: [count]

Assessment Report: [inline or note that it's in agent output]
```

4. CONFIRM all sections are populated before proceeding to Phase 2
5. If any section is incomplete, STOP and request the agent to complete it
6. **UPDATE TASK**: Mark "Phase 1: Generate Plugin Assessment Report" as `completed`

---

## Phase 2: Refactoring Design Map

**Objective**: Create a detailed refactoring design specification showing how each identified issue should be addressed.

**Action**: LAUNCH the python-cli-design-spec agent using the Task tool with this exact prompt (substitute the complete Assessment Report from Phase 1 where indicated):

```
Task(
    agent="python-cli-design-spec",
    prompt="""
Your ROLE_TYPE is sub-agent.

<assessment_report>
[SUBSTITUTE: Insert the complete Plugin Assessment Report from Phase 1 here]
</assessment_report>

<context>
WHERE you are designing:
- Plugin root: ./plugins/$ARGUMENTS
- Existing skill structure: ./plugins/$ARGUMENTS/skills/
- Claude Code skill format reference: claude-skills-overview-2026

WHAT patterns to follow:
- Skills should be <500 lines with progressive disclosure via references/
- Skills should cover single domain (not multi-domain)
- Agent descriptions need trigger keywords for delegation matching
- Frontmatter must follow Claude Code schema exactly
- Reference files must be linked from SKILL.md
</context>

<success_criteria>
MUST deliver:
1. Refactoring design file written to .claude/plan/refactor-design-{plugin-slug}.md
2. Design addresses ALL issues from assessment report
3. Clear transformation specifications for each refactoring target
4. Dependency mapping between refactoring tasks
5. Parallelization opportunities identified
</success_criteria>

<exploration_steps>
EXECUTE these steps in order:
1. READ the assessment report to understand all issues
2. READ ./plugins/$ARGUMENTS/skills/*/SKILL.md to understand current structure
3. READ reference skills (claude-skills-overview-2026) to understand target format
4. For skills needing split: ANALYZE content domains and propose partition plan
5. For agents needing optimization: IDENTIFY specific improvements
6. For orphaned files: DETERMINE integration or removal strategy
</exploration_steps>

<design_specifications>
DESIGN and DOCUMENT these aspects for each refactoring target:

### For SKILL_SPLIT targets:
- Current skill path and line count
- Identified domains within the skill
- Proposed new skills with names and scopes
- Content distribution plan (which sections go where)
- Shared references strategy
- Backward compatibility (if skill is externally referenced)

### For AGENT_OPTIMIZE targets:
- Current agent path
- Current description (problems identified)
- Proposed new description with trigger keywords
- Instruction clarity improvements
- Tool restrictions review

### For DOC_IMPROVE targets:
- Current file path
- Current description quality score
- Specific improvements needed
- Target description with trigger phrases

### For ORPHAN_RESOLVE targets:
- Orphaned file path
- Classification (New Content / Duplicate / Notes / Outdated)
- Integration target or removal justification
- Proposed link location if integrating
</design_specifications>

<file_naming>
Generate a slug from the plugin name using these rules:
1. Use the plugin directory name directly (already lowercase with hyphens)
Example: "python3-development" → "python3-development"
</file_naming>

<output_file_structure>
WRITE the specification to: .claude/plan/refactor-design-{plugin-slug}.md

MUST use this exact structure:

# Refactoring Design Map: {Plugin Name}

## Overview
[2-3 sentence description of refactoring scope and goals]

## Source Assessment
- Plugin: ./plugins/{plugin-name}
- Overall Score: [from Phase 1]
- Total Refactoring Targets: [count]

## Skill Splits

### {original-skill-name} Split Plan
**Source**: ./plugins/{plugin}/skills/{skill}/SKILL.md
**Lines**: [count]
**Domains Identified**: [list]

**Proposed Split**:
| New Skill | Scope | Sections from Original |
|-----------|-------|------------------------|
| {name-1} | {domain} | {sections} |
| {name-2} | {domain} | {sections} |

**Shared References**: [files that both new skills will reference]
**Migration Notes**: [any backward compatibility concerns]

## Agent Optimizations

### {agent-name} Optimization
**Source**: ./plugins/{plugin}/agents/{agent}.md
**Current Description**: "{current}"
**Issues**: [list of problems]

**Proposed Description**: "{new description with trigger keywords}"
**Instruction Improvements**:
- [specific improvement 1]
- [specific improvement 2]

## Documentation Improvements

### {file-path}
**Current Score**: [X/10]
**Issues**: [list]
**Target Improvements**: [specific changes]

## Orphan Resolution

### {orphan-path}
**Classification**: [New Content / Duplicate / Notes / Outdated]
**Resolution**: [Integrate into X / Remove / Merge with Y]
**Implementation**: [specific steps]

## Dependency Map

```

{visual or list showing which tasks depend on others}

```

## Parallelization Opportunities

Tasks that can run simultaneously:
- Group A: [task list] - No shared files
- Group B: [task list] - No shared files
</output_file_structure>

<available_resources>
- Full codebase read/write access
- Existing skill files as reference
- Claude Code skill format documentation
</available_resources>
"""
)
```

**Phase 2 Completion Requirements**:

After the python-cli-design-spec agent completes, YOU MUST:

1. **UPDATE TASK**: Mark "Phase 2: Create refactoring design map" as `in_progress` before verification
2. VERIFY the agent created the design file at .claude/plan/refactor-design-{plugin-slug}.md
3. READ the design file to confirm all sections are populated
4. DISPLAY this structured summary:

```
=== PHASE 2 COMPLETE: Refactoring Designed ===

Design File: .claude/plan/refactor-design-{plugin-slug}.md
Total Refactoring Targets: [count]

Skill Splits Planned: [count]
- {skill-name}: Split into {N} new skills
...

Agent Optimizations Planned: [count]
- {agent-name}: {brief improvement}
...

Documentation Improvements: [count]
Orphan Resolutions: [count]

Parallelization Groups: [count]
```

5. CONFIRM the design file exists and is complete before proceeding to Phase 3
6. If the file is missing or incomplete, STOP and request the agent to complete it
7. **UPDATE TASK**: Mark "Phase 2: Create refactoring design map" as `completed`

---

## Phase 3: Task Planning

**Objective**: Generate detailed implementation tasks with dependencies, verification steps, and parallel execution opportunities.

**Action**: LAUNCH a swarm-task-planner agent using the Task tool with this exact prompt:

````
Task(
    agent="swarm-task-planner",
    prompt="""
Your ROLE_TYPE is sub-agent.

<design_file_location>
READ the refactoring design from Phase 2 at: .claude/plan/refactor-design-{plugin-slug}.md
</design_file_location>

<context>
WHERE you are planning:
- Plan directory: .claude/plan/
- Task file destination: .claude/plan/tasks-refactor-{plugin-slug}.md
- Plan index: .claude/plan/REFACTOR-PLAN.md (create if not exists)

WHAT task structure to follow:
- Dependency-based ordering (NO temporal language)
- Explicit parallelization opportunities
- Verification steps for each task
- Status tracking: ❌ NOT STARTED, 🔄 IN PROGRESS, ✅ COMPLETE
</context>

<success_criteria>
MUST deliver:
1. Task file written to .claude/plan/tasks-refactor-{plugin-slug}.md
2. REFACTOR-PLAN.md created/updated with checklist items
3. ALL tasks follow the exact format specified
4. Dependencies correctly mapped between tasks
5. Parallelization opportunities explicitly identified
6. Each task has acceptance criteria and verification steps
</success_criteria>

<exploration_steps>
EXECUTE these steps in order:
1. READ .claude/plan/refactor-design-{plugin-slug}.md (design from Phase 2)
2. READ .claude/plan/REFACTOR-PLAN.md if it exists
3. GLOB .claude/plan/tasks-*.md to identify existing task files
</exploration_steps>

<planning_steps>
PERFORM these planning steps:

1. **Create task file**:
   WRITE to .claude/plan/tasks-refactor-{plugin-slug}.md

   MUST follow this exact format for each task:

   ```markdown
   ## Task {ID}: {Descriptive Name}

   **Status**: ❌ NOT STARTED
   **Dependencies**: [Comma-separated Task IDs or "None"]
   **Priority**: [Integer 1-5, where 1 is highest]
   **Complexity**: [Low/Medium/High]
   **Agent**: [plugin-creator:refactor-skill | subagent-refactorer | claude-context-optimizer | plugin-docs-writer]

   **Target**: [File path being refactored]
   **Issue Type**: [SKILL_SPLIT | AGENT_OPTIMIZE | DOC_IMPROVE | ORPHAN_RESOLVE | STRUCTURE_FIX]

   **Acceptance Criteria**:
   1. [Specific, measurable criterion]
   2. [Another testable requirement]
   3. [At least 3 criteria total]

   **Required Inputs**:
   - Design spec section: [which section of refactor-design-{slug}.md]
   - Source files: [paths to read]

   **Expected Outputs**:
   - [File paths to be created/modified]

   **Can Parallelize With**: [Comma-separated Task IDs or "None"]
   **Reason**: [Why parallelization is safe - no shared files/dependencies]

   **Verification Steps**:
   1. [How to verify criterion 1]
   2. [How to verify criterion 2]
   3. [At least 3 verification steps]
   ```

   **Agent Selection Rules**:
   - SKILL_SPLIT tasks → `plugin-creator:refactor-skill`
   - AGENT_OPTIMIZE tasks → `subagent-refactorer`
   - DOC_IMPROVE tasks (skills/agents) → `claude-context-optimizer`
   - ORPHAN_RESOLVE tasks → `claude-context-optimizer` (integrate) or orchestrator (remove)
   - Documentation generation → `plugin-docs-writer`

   AFTER all refactoring tasks, ALWAYS include these verification tasks:

   ```markdown
   ## Task V1: Validate Plugin Structure

   **Status**: ❌ NOT STARTED
   **Dependencies**: [All refactoring task IDs]
   **Priority**: 1
   **Complexity**: Low
   **Agent**: plugin-assessor

   **Acceptance Criteria**:
   1. Plugin passes structural validation
   2. All links resolve correctly
   3. No orphaned files remain
   4. Frontmatter validates against schema

   **Verification Steps**:
   1. Run plugin-assessor on refactored plugin
   2. Verify score improved from original assessment
   3. Verify no critical issues remain
   ```

   ```markdown
   ## Task V2: Update Plugin Documentation

   **Status**: ❌ NOT STARTED
   **Dependencies**: Task V1
   **Priority**: 2
   **Complexity**: Low
   **Agent**: plugin-docs-writer

   **Acceptance Criteria**:
   1. README.md reflects current capabilities
   2. All skills documented
   3. Usage examples accurate

   **Verification Steps**:
   1. README.md exists and is comprehensive
   2. All skills listed with descriptions
   3. Installation instructions accurate
   ```

2. **Create/Update REFACTOR-PLAN.md**:

   IF .claude/plan/REFACTOR-PLAN.md does not exist, CREATE it:

   ```markdown
   # Plugin Refactoring Plan Index

   ## Active Refactoring Projects

   | Plugin | Task File | Status | Score Before | Score After |
   |--------|-----------|--------|--------------|-------------|

   ## Completed Refactoring Projects

   | Plugin | Task File | Completion Date | Score Improvement |
   |--------|-----------|-----------------|-------------------|
   ```

   ADD new entry to Active Refactoring Projects:
   ```markdown
   | {plugin-name} | [tasks-refactor-{slug}.md](tasks-refactor-{slug}.md) | ❌ NOT STARTED | {score}/100 | TBD |
   ```

</planning_steps>

<constraints>
NEVER use temporal language:
- ❌ "First, then, finally, before, after"
- ✓ "Dependencies: Task 1, Task 2"

ALWAYS specify:
- Minimum 3 acceptance criteria per task
- Minimum 3 verification steps per task
- Explicit parallelization analysis
- Complete file paths for inputs and outputs
</constraints>

<available_resources>
- Full read/write access to .claude/plan/ directory
- Refactoring design document from Phase 2
</available_resources>
"""
)
````

**Phase 3 Completion Requirements**:

After the swarm-task-planner agent completes, YOU MUST:

1. **UPDATE TASKS**: Mark these as `in_progress` before verification:
   - "Phase 3: Create task file at .claude/plan/tasks-refactor-{slug}.md"
   - "Phase 3: Update REFACTOR-PLAN.md with new checklist items"
2. VERIFY the task file was created at .claude/plan/tasks-refactor-{plugin-slug}.md
3. VERIFY REFACTOR-PLAN.md exists and has the new entry
4. READ both files to confirm completeness
5. DISPLAY this structured summary:

```
=== PHASE 3 COMPLETE: Tasks Planned ===

Task File: .claude/plan/tasks-refactor-{plugin-slug}.md
REFACTOR-PLAN.md: Updated

Total Tasks: [count]
- Skill Split Tasks: [count]
- Agent Optimization Tasks: [count]
- Documentation Tasks: [count]
- Orphan Resolution Tasks: [count]
- Verification Tasks: [count]

Parallelization Groups:
- Group A (can run together): [task IDs]
- Group B (can run together): [task IDs]
...

Task Summary:
- Task {ID}: {Name} | Agent: {agent} | Dependencies: {deps}
...
```

6. CONFIRM all files exist and are complete
7. If any file is missing or incomplete, STOP and request completion
8. **UPDATE TASKS**: Mark both Phase 3 items as `completed`

---

## Phase 4: Context Gathering

**Objective**: Gather comprehensive refactoring context before execution begins.

**Action**: LAUNCH the context-gathering agent using the Task tool:

```
Task(
    agent="context-gathering",
    prompt="""
Your ROLE_TYPE is sub-agent.

<task_file>
.claude/plan/tasks-refactor-{plugin-slug}.md
</task_file>

<design_spec>
.claude/plan/refactor-design-{plugin-slug}.md
</design_spec>

<context>
WHERE you are researching:
- Plugin: ./plugins/$ARGUMENTS
- Design spec: .claude/plan/refactor-design-{plugin-slug}.md
- Task file: .claude/plan/tasks-refactor-{plugin-slug}.md

WHAT to gather:
1. Current skill content summaries (for split planning)
2. Existing patterns in reference files
3. Cross-references between skills
4. External dependencies on skills being modified
</context>

<success_criteria>
MUST deliver:
1. Context manifest written to the task file
2. All relevant skill content summarized
3. Cross-reference map documented
4. STATUS: DONE or BLOCKED response
</success_criteria>

<instructions>
1. READ the design spec to understand what will change
2. READ the task file to understand all tasks
3. READ each skill being refactored to understand current content
4. MAP cross-references between files
5. IDENTIFY external dependencies (other plugins/skills referencing these)
6. WRITE context manifest to the task file
7. RETURN STATUS output with summary
</instructions>
"""
)
```

**Phase 4 Completion Requirements**:

After the context-gathering agent completes:

1. **UPDATE TASK**: Mark "Phase 4: Gather refactoring context" as `in_progress` before verification
2. VERIFY the task file now contains a "Context Manifest" section
3. DISPLAY:

```
=== PHASE 4 COMPLETE: Context Gathered ===

Task File: .claude/plan/tasks-refactor-{plugin-slug}.md
Context Manifest: [added/updated]
Skills Analyzed: [count]
Cross-References Mapped: [count]
External Dependencies: [count or "none found"]
```

4. **UPDATE TASK**: Mark "Phase 4: Gather refactoring context" as `completed`

---

## Final Summary - Return to Orchestrator

**BEFORE displaying the final summary, YOU MUST:**

1. **VERIFY ALL TODOS COMPLETE**: Check that ALL tasks are marked `completed`
2. If ANY task is still `pending` or `in_progress`, go back and complete the missing work
3. **UPDATE TASK**: Mark "Final: Return to orchestrator with execution plan" as `in_progress`

<final_summary_structure>

```
================================================================================
                    PLUGIN REFACTORING PLANNING COMPLETE
================================================================================

Plugin: $ARGUMENTS
Plugin Path: ./plugins/$ARGUMENTS

DELIVERABLES:
-------------
✓ Assessment Report: Generated (Phase 1)
✓ Refactoring Design: .claude/plan/refactor-design-{plugin-slug}.md
✓ Task File: .claude/plan/tasks-refactor-{plugin-slug}.md
✓ REFACTOR-PLAN.md: Updated
✓ Context Manifest: Added to task file

PHASE 1 SUMMARY - Assessment:
- Original Score: {X}/100
- Critical Issues: {count}
- Refactoring Targets: {count}

PHASE 2 SUMMARY - Design:
- Skill Splits: {count}
- Agent Optimizations: {count}
- Documentation Improvements: {count}
- Orphan Resolutions: {count}

PHASE 3 SUMMARY - Planning:
- Total Tasks: {count}
- Parallelizable Tasks: {count}
- Estimated Complexity: {Low/Medium/High}

PHASE 4 SUMMARY - Context:
- Context Manifest: Added
- Cross-References: {count}

================================================================================
                         READY FOR PARALLEL EXECUTION
================================================================================

ORCHESTRATOR: You can now launch parallel agents using:

/plugin-creator:implement-refactor {plugin-slug}

This will:
1. Load the task file
2. Build dependency graph
3. Launch parallel agents for independent tasks
4. Track progress and handle completions
5. Trigger review loop when tasks complete

PARALLELIZATION GROUPS (can launch simultaneously):
- Group A: {task IDs} - Agent: {agent type}
- Group B: {task IDs} - Agent: {agent type}
...

FILES TO REVIEW BEFORE EXECUTION:
---------------------------------
- .claude/plan/refactor-design-{plugin-slug}.md (refactoring design)
- .claude/plan/tasks-refactor-{plugin-slug}.md (implementation tasks)
================================================================================
```

</final_summary_structure>

4. **UPDATE TASK**: Mark "Final: Return to orchestrator with execution plan" as `completed`

**WORKFLOW COMPLETE** - Control returns to orchestrator for parallel execution.

---

## Workflow Guidelines

**Sequential Dependency Requirements**:

Each phase MUST complete before the next begins:

- Phase 1 output (assessment) → Phase 2 input
- Phase 2 output (design map) → Phase 3 input
- Phase 3 output (task file) → Phase 4 input
- Phase 4 output (context) → Orchestrator execution

**Slug Generation**:

Use the plugin directory name directly (already lowercase with hyphens):

- `python3-development` → `python3-development`
- `gitlab-skill` → `gitlab-skill`

**Quality Assurance**:

At each phase completion:

- VERIFY all required files exist
- CONFIRM all sections are populated
- VALIDATE format matches specifications
- STOP if incomplete and request agent to fix
