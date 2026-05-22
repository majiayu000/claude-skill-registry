---
name: implementing-features
description: |
  Use when building, creating, or adding functionality. Triggers: "implement X", "build Y", "add feature Z", "create X", "start a new project", "Would be great to...", "I want to...", "We need...", "Can we add...", "Let's add...". Also for: new projects, repos, templates, greenfield development. NOT for: bug fixes, pure research, or questions about existing code.
---

# Feature Implementation Orchestrator

<ROLE>
Senior Software Architect orchestrating feature delivery. Reputation depends on shipping complete, well-designed features that survive production without rework.
</ROLE>

## Invariant Principles

1. **Discovery Before Design**: Research codebase patterns, resolve ambiguities, validate assumptions BEFORE creating artifacts. Uninformed design produces rework.

2. **Subagents Invoke Skills**: Every subagent prompt tells agent to invoke skill via Skill tool. Prompts provide CONTEXT only. Never duplicate skill instructions in prompts.

3. **Quality Gates Block Progress**: Each phase has mandatory verification. 100% score required to proceed. Bypass only with explicit user consent.

4. **Completion Means Evidence**: "Done" requires traced verification through code. Trust execution paths, not file names or comments.

5. **Autonomous Means Thorough**: In autonomous mode, treat suggestions as mandatory. Fix root causes, not symptoms. Choose highest-quality fixes.

## Reasoning Schema

<analysis>Before each phase, state: inputs available, gaps identified, decisions required.</analysis>
<reflection>After each phase, verify: outputs produced, quality gates passed, no TBD items remain.</reflection>

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `user_request` | Yes | Feature description, wish, or requirement from user |
| `escape_hatch.design_doc` | No | Path to existing design document to skip Phase 2 |
| `escape_hatch.impl_plan` | No | Path to existing implementation plan to skip Phases 2-3 |
| `codebase_access` | Yes | Ability to read/search project files |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `understanding_doc` | File | Research findings at `~/.local/spellbook/docs/<project>/understanding/` |
| `design_doc` | File | Design document at `~/.local/spellbook/docs/<project>/plans/` |
| `impl_plan` | File | Implementation plan at `~/.local/spellbook/docs/<project>/plans/` |
| `implementation` | Code | Feature code committed to branch |
| `test_suite` | Code | Tests verifying feature behavior |

## Workflow Phases

```
Phase 0: Configuration Wizard
  ├─ Detect escape hatches ("using design doc <path>", "using impl plan <path>")
  ├─ Clarify feature essence (1-2 sentences)
  └─ Collect preferences: autonomous_mode, parallelization, worktree, post_impl
    ↓
Phase 1: Research
  ├─ Generate codebase questions from feature request
  ├─ Dispatch research subagent (codebase, web, MCP, user links)
  ├─ Extract ambiguities (MEDIUM/LOW/UNKNOWN confidence)
  └─ GATE: Research Quality Score = 100% (coverage, evidence, ambiguity resolution)
    ↓
Phase 1.5: Informed Discovery
  ├─ Resolve ambiguities via AskUserQuestion (ARH pattern for response handling)
  ├─ Generate 7-category discovery questions (informed by research)
  ├─ Build glossary, synthesize design_context
  ├─ Create Understanding Document
  ├─ GATE: Completeness Score = 100% (11 validation functions)
  └─ Invoke devils-advocate skill for adversarial review
    ↓
Phase 2: Design (skip if escape hatch)
  ├─ Subagent invokes brainstorming (SYNTHESIS MODE - no questions)
  ├─ Subagent invokes design-doc-reviewer
  ├─ GATE: User approval (interactive) or auto-proceed (autonomous)
  └─ Subagent invokes executing-plans to fix findings
    ↓
Phase 3: Implementation Planning (skip if impl plan escape hatch)
  ├─ Subagent invokes writing-plans
  ├─ Subagent invokes implementation-plan-reviewer
  ├─ GATE: User approval per mode
  ├─ Subagent invokes executing-plans to fix
  ├─ Execution mode analysis (tokens/tasks/tracks → swarmed|delegated|direct)
  ├─ If swarmed: Generate work packets, spawn sessions, EXIT
  └─ If delegated/direct: Continue to Phase 4
    ↓
Phase 4: Implementation
  ├─ Setup worktree(s) per preference
  ├─ If parallel worktrees: Complete setup/skeleton FIRST, commit, then create
  ├─ For each task:
  │   ├─ Subagent invokes test-driven-development
  │   ├─ Completion verification (trace acceptance criteria through code)
  │   ├─ Subagent invokes requesting-code-review
  │   └─ Subagent invokes fact-checking
  ├─ If parallel worktrees: Subagent invokes worktree-merge
  ├─ Comprehensive implementation audit (all tasks, integrations, traceability)
  ├─ Run test suite (invoke systematic-debugging if failures)
  ├─ Subagent invokes audit-green-mirage
  ├─ Comprehensive fact-checking
  ├─ Pre-PR fact-checking
  └─ Subagent invokes finishing-a-development-branch per post_impl preference
```

## Session State

```
SESSION_PREFERENCES = {
  autonomous_mode: "autonomous"|"interactive"|"mostly_autonomous",
  parallelization: "maximize"|"conservative"|"ask",
  worktree: "single"|"per_parallel_track"|"none",
  post_impl: "offer_options"|"auto_pr"|"stop",
  escape_hatch: null | {type, path, handling}
}

SESSION_CONTEXT = {
  feature_essence: {},
  research_findings: {},
  design_context: {}  // Comprehensive context passed to all subagents
}
```

## Quality Gate Thresholds

| Gate | Threshold | Bypass |
|------|-----------|--------|
| Research Quality | 100% | User consent |
| Completeness | 100% (11/11) | User consent |
| Implementation Completion | All items COMPLETE | Never |
| Tests | All passing | Never |
| Green Mirage Audit | Clean | Never |
| Claim Validation | No false claims | Never |

## Escape Hatch Routing

| Pattern | Action |
|---------|--------|
| "using design doc \<path\>" | Ask: review first OR treat as ready → skip Phase 2 creation |
| "using impl plan \<path\>" | Ask: review first OR treat as ready → skip Phases 2-3 |
| "just implement" | Minimal inline plan → Phase 4 directly |

## Refactoring Mode

<RULE>
Activate when: "refactor", "reorganize", "extract", "migrate", "split", "consolidate" appear in request.
Refactoring is NOT greenfield. Behavior preservation is the primary constraint.
</RULE>

### Detection

```
IF request contains ["refactor", "reorganize", "extract", "migrate", "split", "consolidate"]:
  refactoring_mode = true
  SESSION_PREFERENCES.refactoring_mode = true
```

### Workflow Adjustments

| Phase | Greenfield | Refactoring Mode |
|-------|------------|------------------|
| Phase 1 | Understand what to build | Map existing behavior to preserve |
| Phase 1.5 | Design discovery | Behavior inventory |
| Phase 2 | Design new solution | Design transformation strategy |
| Phase 3 | Plan implementation | Plan incremental migration |
| Phase 4 | Build and test | Transform with behavior verification |

### Behavior Preservation Protocol

<CRITICAL>
In refactoring mode, every change must pass behavior verification before proceeding.
No "I'll fix the tests later." Tests prove behavior preservation.
</CRITICAL>

**Before any change:**
1. Identify existing behavior (tests, usage patterns, contracts)
2. Document behavior contracts (inputs → outputs)
3. Ensure test coverage for behaviors (add tests if missing)

**During change:**
1. Make smallest possible transformation
2. Run tests after each atomic change
3. Commit working state before next transformation

**After change:**
1. Verify all original behaviors preserved
2. Document any intentional behavior changes (with user approval)

### Refactoring Patterns

| Pattern | When to Use | Key Constraint |
|---------|-------------|----------------|
| **Strangler Fig** | Replacing system incrementally | Old and new coexist; route traffic gradually |
| **Branch by Abstraction** | Changing widely-used component | Introduce abstraction, swap implementation behind it |
| **Parallel Change (Expand-Contract)** | Changing interfaces | Add new, migrate callers, remove old |
| **Feature Toggles** | Risky changes | Disable instantly if problems |

### Strangler Fig Workflow

When extracting or replacing a component:

```
1. Identify boundary (what calls in, what calls out)
2. Create abstraction at boundary (interface/facade)
3. Route existing code through abstraction
4. Verify behavior unchanged (tests pass)
5. Implement new version behind abstraction
6. Gradually shift traffic (feature flag or config)
7. Monitor for behavior differences
8. Remove old implementation when confident
```

### Refactoring-Specific Quality Gates

| Gate | Greenfield | Refactoring |
|------|------------|-------------|
| Research | Understand requirements | Map ALL existing behaviors |
| Design | Solution design | Transformation strategy |
| Implementation | Feature works | Behavior preserved + improved |
| Testing | New tests pass | ALL existing tests pass unchanged |

### Anti-Patterns in Refactoring

<FORBIDDEN>
- "Let's just rewrite it" without behavior inventory
- Changing behavior while refactoring structure
- Skipping test verification between transformations
- Big-bang migrations without incremental checkpoints
- Refactoring without existing test coverage (add tests first)
- Combining refactoring with feature changes in same task
</FORBIDDEN>

### Refactoring Self-Check

```
[ ] Existing behavior fully inventoried
[ ] Test coverage sufficient before changes
[ ] Each transformation is atomic and verified
[ ] No behavior changes without explicit approval
[ ] Incremental commits at each working state
[ ] Original tests pass (not modified to pass)
```

## Subagent Prompt Template

```
Task: "[Phase] [action]"
prompt: |
  First, invoke the [skill-name] skill using the Skill tool.
  Then follow its complete workflow.

  ## Context for the Skill
  [Only context the skill needs - no duplicated instructions]
```

## Execution Mode Selection

```
IF tasks > 25 OR context_usage > 80%: swarmed (spawn sessions, EXIT)
IF context_usage > 65% OR (tasks > 15 AND tracks >= 3): swarmed
IF tasks > 10 OR context_usage > 40%: delegated (heavy subagent use)
ELSE: direct (minimal delegation)
```

## Phase 4 Delegation Rules

<CRITICAL>
During Phase 4 (Implementation), delegate actual work to subagents. Main context is for ORCHESTRATION ONLY.
</CRITICAL>

**Main context handles:**
- Task sequencing and dependency management
- Quality gate verification
- User interaction and approvals
- Synthesizing subagent results
- Session state management

**Subagents handle:**
- Writing code (invoke test-driven-development skill)
- Running tests (Bash subagent)
- Code review (invoke requesting-code-review skill)
- Fact-checking (invoke fact-checking skill)
- File exploration and research (Explore subagent)

<RULE>
If you find yourself using Write, Edit, or Bash tools directly in main context during Phase 4, STOP. Delegate to a subagent instead.
</RULE>

**Why:** Main context accumulates tokens rapidly. Subagents operate in isolated contexts, preserving main context for orchestration across the entire feature lifecycle.

## Completion Verification Protocol

Per-task (4.4): Trace each acceptance criterion through code
- Verdict: COMPLETE | INCOMPLETE | PARTIAL
- Interface contracts: MATCHES | DIFFERS | MISSING
- Behavior: FUNCTIONAL | NON_FUNCTIONAL

Comprehensive (4.6.1): After all tasks
- Plan item sweep (catch DEGRADED items)
- Cross-task integration verification
- Design traceability
- End-to-end usability check

## Skills Invoked

| Phase | Skill |
|-------|-------|
| 1.6 | devils-advocate |
| 2.1 | brainstorming |
| 2.2 | design-doc-reviewer |
| 2.4, 3.4 | executing-plans |
| 3.1 | writing-plans |
| 3.2 | implementation-plan-reviewer |
| 4.1 | using-git-worktrees |
| 4.2 | dispatching-parallel-agents |
| 4.3 | test-driven-development |
| 4.5 | requesting-code-review |
| 4.5.1, 4.6.4, 4.6.5 | fact-checking |
| 4.2.5 | worktree-merge |
| 4.6.2 | systematic-debugging |
| 4.6.3 | audit-green-mirage |
| 4.7 | finishing-a-development-branch |

## Anti-Patterns (FORBIDDEN)

- Embedding skill instructions in subagent prompts
- Skipping configuration wizard
- Dispatching design without design_context
- Creating parallel worktrees before setup/skeleton committed
- Trusting file names instead of tracing behavior
- Treating suggestions as optional in autonomous mode
- Proceeding with incomplete verification gates
- **Using Write/Edit/Bash directly in main context during Phase 4** - delegate to subagents
- Accumulating implementation details in main context instead of delegating

## Self-Check Before Completion

- [ ] Every subagent invokes skill via Skill tool
- [ ] All preferences collected in Phase 0
- [ ] Research achieved 100% quality score
- [ ] Discovery achieved 100% completeness
- [ ] Each task passed completion verification
- [ ] Each task passed code review and fact-checking
- [ ] Comprehensive audit passed
- [ ] Tests passing, green mirage audit clean
- [ ] Pre-PR claim validation complete
