---
name: optimize-plugin
description: This skill should be used when the user asks to "validate a plugin", "optimize plugin", "check plugin quality", "review plugin structure", or mentions plugin optimization and validation tasks.
argument-hint: <plugin-path>
user-invocable: true
allowed-tools: ["Read", "Glob", "Bash(realpath *)", "Bash(bash:*)", "Task", "AskUserQuestion", "TaskCreate", "TaskUpdate"]
---

# Plugin Optimization

Execute plugin validation and optimization workflow. **Target:** $ARGUMENTS

## Background Knowledge

**Template Compliance**: Components MUST conform to templates in `${CLAUDE_PLUGIN_ROOT}/examples/`. See `references/template-validation.md` for complete requirements (instruction-type/knowledge-type skills, agents).

**Tool Patterns**: See `references/tool-patterns.md` for invocation styles. Key: Skill/AskUserQuestion/TaskCreate require explicit "Use [tool] tool" phrasing.

## Initialization

**Use TaskCreate tool** to track all four phases before starting work.

## Phase 1: Discovery & Validation
**Goal**: Validate structure and detect issues. Orchestrator MUST NOT apply fixes.

**Actions**:
1. Resolve path with `realpath` and verify existence
2. Validate `.claude-plugin/plugin.json` exists
3. Validate components against `${CLAUDE_PLUGIN_ROOT}/examples/` templates
4. Assess architecture (ask about command migration if needed)
5. Run validation: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin.py "$TARGET"`
6. Compile issues by severity (Critical, Warning, Info)

## Phase 2: Agent-Based Optimization
**Goal**: Launch agent to apply ALL fixes. Orchestrator does NOT make fixes directly.

**Condition**: Skip this phase if Phase 1 found no issues (proceed directly to Phase 4).

**Actions**:
1. Launch `plugin-optimizer:plugin-optimizer` agent with the following prompt content:
   - Target plugin path (absolute path from Phase 1)
   - Complete list of validation issues with severity levels
   - Template compliance results from Phase 1
   - Any user decisions from architecture assessment
2. Agent autonomously applies fixes (uses AskUserQuestion for template fix approvals)
3. Agent increments version in `.claude-plugin/plugin.json` after fixes (patch: fixes/optimizations, minor: new components, major: breaking changes)

## Phase 3: Final Verification
**Goal**: Re-run validation to verify fixes.

**Condition**: Only execute if Phase 2 applied fixes.

**Actions**:
1. Re-run all validation scripts from Phase 1
2. Compare results with initial findings
3. If critical issues remain: resume agent with remaining issues
4. Document outcome (fixed vs remaining with rationale)

## Phase 4: Final Deliverables
**Goal**: Deliver comprehensive optimization report and updated documentation to user.

**Actions**:
1. Generate complete validation report with all findings, fixes, and verification results
2. Produce component inventory summary showing plugin structure
3. Update README.md to accurately reflect current plugin state
4. See `./references/workflow-phases.md` for detailed steps and `./references/report-template.md` for format
