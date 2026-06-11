---
name: skill-composer
description: "DAG-based multi-skill orchestration with dependency resolution."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
routing:
  triggers:
    - "compose skills"
    - "DAG orchestration"
    - "multi-skill chain"
    - "skill pipeline"
    - "combine skills"
  category: meta-tooling
  pairs_with:
    - workflow
    - feature-lifecycle
---

# Skill Composer

## Overview

Orchestrate complex workflows by chaining multiple skills into validated execution DAGs. This skill discovers applicable skills, resolves dependencies, validates compatibility, presents execution plans, and manages skill-to-skill context passing. Use when a task requires 2+ skills chained together, parallel skill execution, or conditional branching between skills. Invoke the single skill directly when it can handle the request alone, or for simple sequential invocation that needs no dependency management.

**Core principle**: Minimize composition overhead. Prefer simple 2-3 skill chains. Add only skills directly needed or "nice to have" additions without explicit user request.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| checking skill chain compatibility and input/output type matching | `compatibility-matrix.md` | Loads detailed guidance from `compatibility-matrix.md`. |
| choosing sequential vs parallel composition; chain length limits | `composition-patterns.md` | Loads detailed guidance from `composition-patterns.md`. |
| composition walkthroughs: feature+tests, debug+docs, parallel quality checks, research-driven builds | `examples.md` | Loads detailed guidance from `examples.md`. |
| selecting a proven composition pattern; troubleshooting compositions | `skill-patterns.md` | Loads detailed guidance from `skill-patterns.md`. |

## Instructions

### Phase 1: DISCOVER

**Goal**: Analyze the task and find applicable skills.

**Step 1: Analyze the user's request**

Identify:
- Primary goals (what needs to be accomplished)
- Quality requirements (testing, verification, documentation)
- Domain constraints (language, framework, standards)
- Execution constraints (sequential vs parallel, conditionals)

**Step 2: Discover available skills**

Before building any DAG, scan skills/*/SKILL.md for available skills:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/discover_skills.py ./skills
```

Review the discovered skills. Categorize by type (workflow, testing, quality, documentation, code-analysis, debugging) with dependency metadata.

**Step 3: Select skills (Apply minimum-skills principle)**

Choose only skills directly needed for the stated goals. This prevents over-composition and unnecessary failure points:

- Can a single skill handle this? If yes, invoke it directly. Invoke it directly.
- Can 2 skills handle this? Prefer that over 3+.
- Is a skill being added "for quality" or "just in case"? Remove it.

Cross-reference selections against `references/compatibility-matrix.md` to confirm chaining is valid before proceeding.

**Gate**: Task goals identified. Available skills indexed. Selected skills directly address stated goals with no extras. Proceed only when gate passes.

### Phase 2: PLAN

**Goal**: Build a validated execution DAG.

**Step 1: Build the DAG**

Construct the execution DAG as a JSON structure with nodes (skills) and edges (dependencies) based on the task analysis:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/build_dag.py skill-index.json task-description.json
```

**Step 2: Validate the DAG (MANDATORY before execution)**

ALWAYS validate the execution graph is acyclic before moving to execution. Validation checks:
- **Acyclic**: No circular dependencies exist between skills
- **Compatibility**: Output types from each skill match input requirements of downstream skills (consult `references/compatibility-matrix.md`)
- **Availability**: All referenced skills exist in the skill index
- **Ordering**: Dependencies satisfy topological ordering

If validation fails, fix the issue and re-validate. Common fixes:
- Circular dependency: Remove one edge or split into two independent compositions
- Type mismatch: Choose different skill or add transformation step
- Missing skill: Check spelling, re-run discovery
- Ordering violation: Reorder phases to satisfy dependencies

**Step 3: Present the execution plan (Dry run is MANDATORY)**

ALWAYS show the execution plan and get user confirmation before running skills. This prevents wasting time on composition errors:

```
=== Execution Plan ===

Phase 1 (Sequential):
  -> skill-name
    Purpose: [what it does in this context]
    Output: [what it produces]

Phase 2 (Parallel):
  -> skill-a
    Purpose: [what it does]
    Input: [from Phase 1]
  -> skill-b
    Purpose: [what it does]
    Input: [from Phase 1]

Phase 3 (Sequential):
  -> skill-c
    Purpose: [what it does]
    Input: [from Phase 2]

Skills: N | Phases: N | Parallel phases: N

Proceed? [Y/n]
```

**Gate**: DAG is acyclic. All skills exist. Input/output types are compatible. Topological ordering is valid. User has seen the plan. Proceed only when gate passes.

### Phase 3: EXECUTE

**Goal**: Run skills in topological order, passing context between them.

**Step 1: Execute each phase**

For sequential phases:
1. Invoke skill with context from previous phases
2. Capture output
3. Verify output/input compatibility between chained skills
4. Proceed to next phase

For parallel phases:
1. Launch all independent skills using Task tool (execute independent skills concurrently when no shared resources or dependencies exist)
2. Wait for all to complete
3. Aggregate results for next phase

**Step 2: Pass context between skills**

ALWAYS verify output/input compatibility between chained skills before passing context:

1. Capture output from completed skill
2. Transform to format expected by next skill (validate using `references/compatibility-matrix.md`)
3. Inject as context when invoking next skill
4. Verify transformation succeeded

**Step 3: Report progress**

After each phase completes, report:
- Phase number and skills completed
- Output summary
- Overall progress (e.g., "Phase 2/3 complete")

Show command output rather than describing it. Be concise but informative.

**Step 4: Handle failures during execution**

ALWAYS catch skill failures and determine if remaining chain can continue. If a skill fails mid-chain:

1. **Assess impact**: Does this block downstream skills?
   - Critical (blocks all downstream): Stop chain, report what completed
   - Isolated (blocks one branch): Continue other branches
   - Recoverable (transient failure): Retry with adjusted parameters (max 2 attempts)

2. **Report failure context**:
```
Skill failed: [skill-name]
  Phase: N
  Error: [error message]
  Downstream impact: [list blocked skills]
  Continuing branches: [list unaffected skills]
  Recovery options:
    1. Fix error and retry
    2. Skip skill and continue (if non-critical)
    3. Abort entire workflow
```

3. **Execute recovery**: Based on user selection or automatic policy (if auto-retry enabled)

**Gate**: All phases executed. All skill outputs captured. Context passed successfully between all transitions. Proceed only when gate passes.

### Phase 4: REPORT

**Goal**: Collect results and clean up.

**Step 1: Generate results summary**

```
=== Composition Results ===

Execution Summary:
  Total phases: N
  Skills executed: N
  Duration: X minutes

Phase Results:
  Phase 1: [skill-name] - [status]
    Output: [summary]
  Phase 2: [skill-a] - [status]
           [skill-b] - [status]
    Output: [summary]
  Phase 3: [skill-c] - [status]
    Output: [summary]

Final Output:
  [Key deliverables with file paths]
```

**Step 2: Clean up temporary files**

Remove temporary files at task completion. Keep only files explicitly needed for final output:
- `/tmp/skill-index.json`
- `/tmp/execution-dag.json`
- Any intermediate output files created during composition

**Gate**: Results reported. Temporary files cleaned up. Composition complete.

---

## Error Handling

### Error: "Circular dependency detected"
Cause: Skills reference each other cyclically in the DAG
Solution:
1. Review dependency graph for cycles
2. Remove or reorder the problematic dependency
3. Consider splitting into independent compositions
4. Re-validate DAG before proceeding

### Error: "Skill output incompatible with next skill input"
Cause: Output type from one skill does not match expected input of the next
Solution:
1. Consult `references/compatibility-matrix.md` for valid chains
2. Add an intermediate transformation skill if one exists
3. Choose a different skill combination that has compatible types
4. Re-validate after changes

### Error: "Skill failed during execution"
Cause: A skill in the chain encountered an error
Solution:
1. Determine failure impact: critical (blocks downstream), isolated (one branch), or recoverable
2. If isolated: continue other branches, report partial results
3. If recoverable: retry with adjusted parameters (max 2 attempts)
4. If critical: abort chain, report what completed, suggest recovery options

### Error: "Skill not found in index"
Cause: Referenced skill does not exist or name is misspelled
Solution:
1. Check spelling against skill index output
2. Re-run discovery script to refresh the index
3. Verify the skill directory exists under skills/
4. Use the suggested alternative from the discovery output if the name was close

## References

- `${CLAUDE_SKILL_DIR}/references/composition-patterns.md`: Proven multi-skill composition patterns with duration estimates
- `${CLAUDE_SKILL_DIR}/references/compatibility-matrix.md`: Skill input/output compatibility and valid chains
- `${CLAUDE_SKILL_DIR}/references/skill-patterns.md`: Common skill patterns with sequential/parallel decision trees
