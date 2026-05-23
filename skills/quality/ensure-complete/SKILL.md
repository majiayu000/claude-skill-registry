---
name: ensure-complete
description: 'Perform holistic review of completed refactoring, validate improvements, and create follow-up tasks if needed'
argument-hint: <task-file-path>
model: sonnet
user-invocable: true
---

# Complete Refactor Workflow

You MUST perform a holistic review and validation of the completed plugin refactoring. This workflow validates that the refactoring achieved its goals, improved the plugin score, and follows project standards. If issues are found, follow-up task files are created for resolution.

<task_file>
$ARGUMENTS
</task_file>

## Mission

EXECUTE this multi-phase review workflow to validate refactoring completeness. This workflow is **recursive** - if the review creates follow-up tasks, the orchestrator should run `/implement-refactor` again until no more tasks are generated.

---

## Completion Tracking (MANDATORY)

**IMMEDIATELY** after reading this command, you MUST create todos using TodoWrite:

```
TodoWrite(todos=[
    {"content": "Phase 1: Plugin Validation - Re-assess plugin structure and score", "status": "pending", "activeForm": "Running plugin validation"},
    {"content": "Phase 2: Code Review - Validate refactored code quality", "status": "pending", "activeForm": "Running code review"},
    {"content": "Phase 3: Documentation Audit - Check for documentation drift", "status": "pending", "activeForm": "Running documentation audit"},
    {"content": "Phase 4: Gap Identification - Create follow-up tasks if needed", "status": "pending", "activeForm": "Identifying gaps and creating follow-up tasks"},
    {"content": "Final: Display completion summary and next steps", "status": "pending", "activeForm": "Displaying completion summary"}
])
```

**RULES**:

1. Create ALL todos BEFORE starting Phase 1
2. Mark each todo `in_progress` BEFORE starting that work
3. Mark each todo `completed` AFTER the phase finishes
4. DO NOT display final summary until ALL todos are `completed`

---

## Phase 1: Plugin Validation

**Objective**: Re-run plugin assessment to measure improvement from refactoring.

**Action**: LAUNCH the plugin-assessor agent using the Task tool:

```
Task(
    subagent_type="plugin-assessor",
    prompt="""
Your ROLE_TYPE is sub-agent.

<task_file>
$ARGUMENTS
</task_file>

<context>
WHERE you are validating:
- Extract plugin path from task file header
- Compare against original assessment scores

WHAT to validate:
1. Plugin structure is valid after refactoring
2. All links resolve correctly
3. No orphaned files remain (that weren't marked for removal)
4. Frontmatter validates against schema
5. Score improved from original assessment
</context>

<success_criteria>
MUST deliver:
1. Post-refactoring assessment score
2. Comparison with pre-refactoring score (from REFACTOR-PLAN.md)
3. List of any remaining issues
4. STATUS: DONE or BLOCKED response
</success_criteria>

<instructions>
1. READ the task file to understand what was refactored
2. IDENTIFY the plugin path from task metadata
3. RUN full plugin assessment protocol
4. COMPARE scores with original (from .claude/plan/REFACTOR-PLAN.md)
5. RETURN STATUS output with validation findings
</instructions>
"""
)
```

**Phase 1 Completion Requirements**:

After the plugin-assessor agent completes:

1. CAPTURE the STATUS response (DONE or BLOCKED)
2. CAPTURE the score comparison (before vs after)
3. DISPLAY:

```
=== PHASE 1 COMPLETE: Plugin Validation ===

Status: [DONE/BLOCKED]
Original Score: [X/100]
New Score: [Y/100]
Improvement: [+Z points]

Remaining Issues: [count]
- [issue description if any]
```

4. Mark "Phase 1: Plugin Validation" as `completed`

### Plugin Validation Detailed Checks

The plugin-assessor agent MUST validate these plugin components against authoritative schemas:

#### 1.1 Plugin.json Schema Validation

Validate against authoritative plugin.json schema from claude-plugins-reference-2026:

**Required checks:**

```bash
# Validate plugin structure
claude plugin validate {plugin-directory}
```

**Common plugin.json issues after refactoring:**

| Issue                         | Cause                                                | Fix                                                                         |
| ----------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------- |
| `agents: Invalid input`       | Used `"./agents/"` directory string instead of array | Change to array of file paths: `["./agents/file1.md", "./agents/file2.md"]` |
| `name: Required`              | Missing required name field                          | Add `"name": "plugin-name"` in kebab-case                                   |
| Invalid path format           | Absolute paths or missing `./` prefix                | All paths must be relative and start with `./`                              |
| Referenced file doesn't exist | Path in plugin.json points to moved/deleted file     | Update paths to match new file locations after refactoring                  |

**SOURCE:** Lines 25-92 of claude-plugins-reference-2026/SKILL.md

#### 1.2 Hook Configuration Validation

If plugin includes hooks, validate hook configuration:

**Hook validation checklist:**

- [ ] Hook config file exists at path specified in plugin.json
- [ ] Hook matchers reference valid tool names (Read, Write, Edit, etc.)
- [ ] Hook script paths use `${CLAUDE_PLUGIN_ROOT}` variable
- [ ] Hook scripts are executable (`chmod +x script.sh`)
- [ ] Hook event types are valid (PreToolUse, PostToolUse, SessionStart, etc.)

**Valid hook events:**

- PreToolUse, PostToolUse, PostToolUseFailure
- PermissionRequest, UserPromptSubmit, Notification
- Stop, SubagentStart, SubagentStop
- Setup, SessionStart, SessionEnd, PreCompact

**SOURCE:** Lines 186-227 of claude-plugins-reference-2026/SKILL.md

#### 1.3 MCP Server Validation

If plugin bundles MCP servers, validate MCP configuration:

**MCP validation checklist:**

- [ ] MCP config file exists (`.mcp.json` or inline in plugin.json)
- [ ] Server commands use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths
- [ ] Server binaries are executable or installed as dependencies
- [ ] Server `args` arrays are properly formatted
- [ ] Environment variables are properly defined

**SOURCE:** Lines 235-270 of claude-plugins-reference-2026/SKILL.md

#### 1.4 LSP Server Validation

If plugin provides LSP servers, validate LSP configuration:

**LSP validation checklist:**

- [ ] LSP config file exists (`.lsp.json` or inline in plugin.json)
- [ ] LSP server binary is documented as separate installation requirement
- [ ] `extensionToLanguage` mapping is defined for all supported file types
- [ ] `command` references binary in PATH or uses absolute path with `${CLAUDE_PLUGIN_ROOT}`

**IMPORTANT:** LSP servers require separate binary installation. Plugin only configures connection, doesn't bundle the server.

**Example LSP validation error:**

```
LSP server 'gopls' not found in $PATH
→ User must install separately: go install golang.org/x/tools/gopls@latest
```

**SOURCE:** Lines 271-338 of claude-plugins-reference-2026/SKILL.md

#### 1.5 Plugin Caching Path Resolution

**CRITICAL:** Plugins are copied to cache directory during installation. Validate path resolution:

**Path resolution warnings to check:**

- [ ] No `../` parent directory references (will break after caching)
- [ ] All paths relative to plugin root with `./` prefix
- [ ] External dependencies documented (symlinks or restructure required)
- [ ] `${CLAUDE_PLUGIN_ROOT}` used in all hook/MCP/LSP commands

**Common caching issues:**

| Issue                                       | Problem                              | Solution                                                     |
| ------------------------------------------- | ------------------------------------ | ------------------------------------------------------------ |
| `../shared-utils` reference                 | Parent directory not copied to cache | Use symlink or restructure marketplace to include shared dir |
| Hook script uses relative path without `./` | Ambiguous path resolution            | Change to `./scripts/hook.sh` or use `${CLAUDE_PLUGIN_ROOT}` |
| MCP server references user home directory   | Won't work for other users           | Use plugin-relative paths or environment variables           |

**SOURCE:** Lines 349-398 of claude-plugins-reference-2026/SKILL.md

#### 1.6 External Agent Dependencies

Document any agents referenced in tasks that are NOT included in the plugin:

**Action if external agent required:**

1. Check if agent exists in user's `~/.claude/agents/` or project `.claude/agents/`
2. If missing, document as required dependency in plugin README
3. OR create follow-up task to include agent in plugin
4. OR modify workflows to use only included agents

---

## Phase 2: Code Review

**Objective**: Validate that refactored skills, agents, and documentation follow project standards.

**Action**: LAUNCH the python-code-reviewer agent using the Task tool:

```
Task(
    subagent_type="python-code-reviewer",
    prompt="""
Your ROLE_TYPE is sub-agent.

<task_file>
$ARGUMENTS
</task_file>

<context>
WHERE you are reviewing:
- Plugin directory from task file
- All files created or modified during refactoring

WHAT to validate:
1. Skills follow Claude Code skill format
2. Agents follow prompt engineering best practices
3. Reference files are properly linked
4. Frontmatter is correctly formatted
5. No broken cross-references
</context>

<success_criteria>
MUST deliver:
1. Code review findings categorized by severity
2. List of issues requiring follow-up tasks
3. STATUS: DONE or BLOCKED response
</success_criteria>

<instructions>
1. READ the task file to understand what was changed
2. IDENTIFY all files modified from task "Expected Outputs"
3. REVIEW each file against skill/agent format standards
4. CHECK all links and cross-references
5. RETURN STATUS output with review findings
</instructions>
"""
)
```

**Phase 2 Completion Requirements**:

After the code-reviewer agent completes:

1. CAPTURE the STATUS response
2. CAPTURE the list of issues found
3. DISPLAY:

```
=== PHASE 2 COMPLETE: Code Review ===

Status: [DONE/BLOCKED]
Files Reviewed: [count]
Issues Found: [count]
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]
```

4. Mark "Phase 2: Code Review" as `completed`

---

## Phase 3: Documentation Audit

**Objective**: Check if plugin documentation has drifted from the refactored implementation.

**Action**: LAUNCH the doc-drift-auditor agent using the Task tool:

```
Task(
    subagent_type="doc-drift-auditor",
    prompt="""
Your ROLE_TYPE is sub-agent.

<task_file>
$ARGUMENTS
</task_file>

<context>
WHERE you are auditing:
- Plugin README.md
- Skill SKILL.md files
- Agent .md files
- Reference documentation

WHAT changed during refactoring:
- Skills may have been split
- Agents may have new descriptions
- Documentation structure may have changed
</context>

<success_criteria>
MUST deliver:
1. Audit of README.md accuracy
2. Cross-reference validation
3. List of drift items
4. STATUS: DONE or BLOCKED response
</success_criteria>

<instructions>
1. READ the task file to understand what was refactored
2. IDENTIFY all documentation files that should reflect changes
3. COMPARE documented capabilities vs actual implementation
4. IDENTIFY any drift or missing documentation
5. RETURN STATUS output with audit findings
</instructions>
"""
)
```

**Phase 3 Completion Requirements**:

After the doc-drift-auditor agent completes:

1. CAPTURE the STATUS response
2. CAPTURE the drift findings
3. DISPLAY:

```
=== PHASE 3 COMPLETE: Documentation Audit ===

Status: [DONE/BLOCKED]
Documentation Files Checked: [count]
Drift Items Found: [count]
- README outdated: [yes/no]
- Missing skill docs: [count]
- Broken references: [count]
```

4. Mark "Phase 3: Documentation Audit" as `completed`

---

## Phase 4: Gap Identification

**Objective**: Analyze all findings and create follow-up task file if issues require resolution.

**Action**: Based on findings from Phases 1-3, determine if follow-up tasks are needed.

**Decision Logic**:

```
IF (score_improvement < expected) OR
   (critical_issues > 0) OR
   (high_issues > 2) OR
   (drift_items > 0):
    → CREATE follow-up task file
ELSE:
    → Refactoring is complete
```

**If follow-up tasks needed**, CREATE a new task file:

```
Task(
    subagent_type="swarm-task-planner",
    prompt="""
Your ROLE_TYPE is sub-agent.

<findings>
Phase 1 Issues: [list from plugin validation]
Phase 2 Issues: [list from code review]
Phase 3 Issues: [list from documentation audit]
</findings>

<context>
WHERE to write:
- Task file: .claude/plan/tasks-refactor-{plugin-slug}-followup-{N}.md
- N = next sequential number

WHAT to include:
- Tasks for each unresolved issue
- Appropriate agent assignments
- Dependency mapping
</context>

<success_criteria>
MUST deliver:
1. Follow-up task file created
2. All issues mapped to tasks
3. STATUS: DONE response with file path
</success_criteria>

<instructions>
1. ANALYZE all issues from phases 1-3
2. GROUP related issues into tasks
3. ASSIGN appropriate agents
4. WRITE follow-up task file
5. UPDATE REFACTOR-PLAN.md with follow-up reference
6. RETURN STATUS with file path
</instructions>
"""
)
```

**Phase 4 Completion Requirements**:

After determining follow-up status:

1. DISPLAY:

```
=== PHASE 4 COMPLETE: Gap Identification ===

Follow-up Tasks Needed: [YES/NO]
[If YES]:
  Follow-up Task File: .claude/plan/tasks-refactor-{slug}-followup-{N}.md
  Tasks Created: [count]
[If NO]:
  All issues resolved or within acceptable thresholds
```

2. Mark "Phase 4: Gap Identification" as `completed`

---

## Final Summary

**BEFORE displaying the final summary, YOU MUST:**

1. **VERIFY ALL TODOS COMPLETE**: Check that ALL todos are marked `completed`
2. If ANY todo is still `pending` or `in_progress`, go back and complete the missing work
3. **UPDATE TODO**: Mark "Final: Display completion summary" as `in_progress`

<final_summary_structure>

```
================================================================================
                 REFACTORING COMPLETION WORKFLOW FINISHED
================================================================================

Task File: $ARGUMENTS
Plugin: {plugin_name}

PHASE RESULTS:
--------------
Phase 1 - Plugin Validation:    [DONE/BLOCKED]
  Original Score:               [X/100]
  New Score:                    [Y/100]
  Improvement:                  [+Z points]

Phase 2 - Code Review:          [DONE/BLOCKED]
  Issues Found:                 [count]

Phase 3 - Documentation Audit:  [DONE/BLOCKED]
  Drift Items Found:            [count]

Phase 4 - Gap Identification:   [DONE/BLOCKED]
  Follow-up Tasks Created:      [yes/no]

FOLLOW-UP TASKS:
----------------
[If tasks were created, list them here]
- .claude/plan/tasks-refactor-{slug}-followup-{N}.md

NEXT STEPS:
-----------
[If follow-up tasks exist]:
→ Run: /implement-refactor {followup-task-file} to continue refactoring

[If no follow-up tasks]:
→ Refactoring is COMPLETE
→ Plugin score improved from [X] to [Y]
→ Update REFACTOR-PLAN.md to move entry to Completed section
================================================================================
```

</final_summary_structure>

4. **UPDATE TODO**: Mark "Final: Display completion summary" as `completed`

---

## Recursive Workflow

This workflow supports **recursive validation**:

1. If Phase 4 creates follow-up task files
2. The orchestrator should run `/implement-refactor` to address those tasks
3. Then run `/complete-refactor` again on the new task file
4. Repeat until Phase 4 creates NO new tasks

This ensures the plugin is truly refactored and meets all quality standards.

---

## Update REFACTOR-PLAN.md on Completion

When refactoring is complete (no follow-up tasks):

1. READ .claude/plan/REFACTOR-PLAN.md
2. MOVE the plugin entry from "Active Refactoring Projects" to "Completed Refactoring Projects"
3. ADD completion date and score improvement

```markdown
## Completed Refactoring Projects

| Plugin              | Task File                            | Completion Date | Score Improvement |
| ------------------- | ------------------------------------ | --------------- | ----------------- |
| python3-development | tasks-refactor-python3-development.md | 2026-01-21      | 72 → 91 (+19)     |
```

---

## Error Handling

**IF any agent returns BLOCKED**:

1. DISPLAY the BLOCKED status with the missing requirements
2. DO NOT proceed to the next phase
3. RETURN to user with instructions to resolve the blocker
4. User can re-run `/complete-refactor` after resolving

**IF task file path is invalid**:

1. DISPLAY error message: "Task file not found: {path}"
2. LIST available task files in .claude/plan/
3. ASK user to provide correct path
