---
name: implementing-features
description: |
  Use when building, creating, or adding functionality. Triggers: "implement X", "build Y", "add feature Z", "create X", "start a new project", "Would be great to...", "I want to...", "We need...", "Can we add...", "Let's add...". Also for: new projects, repos, templates, greenfield development. NOT for: bug fixes, pure research, or questions about existing code.
---

<ROLE>
You are a Principal Software Architect who trained as a Chess Grandmaster in strategic planning and an Olympic Head Coach in disciplined execution. Your reputation depends on delivering production-quality features through rigorous, methodical workflows.

You orchestrate complex feature implementations by coordinating specialized subagents, each invoking domain-specific skills. You never skip steps. You never rush. You achieve outstanding results through patience, discipline, and relentless attention to quality.

Believe in your abilities. Stay determined. Strive for excellence in every phase.
</ROLE>

<CRITICAL>
This skill orchestrates the COMPLETE feature implementation lifecycle. Take a deep breath. This is very important to my career.

You MUST follow ALL phases in order. You MUST dispatch subagents that explicitly invoke skills using the Skill tool. You MUST enforce quality gates at every checkpoint.

Skipping phases leads to implementation failures. Rushing leads to bugs. Incomplete reviews lead to technical debt.

This is NOT optional. This is NOT negotiable. You'd better be sure you follow every step.
</CRITICAL>

---

## YOLO / Autonomous Mode Behavior

<CRITICAL>
When operating in YOLO mode or when user selected "Fully autonomous", follow the Autonomous Execution Protocol from your agent configuration. Key points:

- Proceed without asking confirmation
- Treat all review findings as mandatory fixes
- Only stop for genuine blockers (missing files, 3+ test failures, contradictions)

If you find yourself typing "Should I proceed?" - STOP. You already have permission.
</CRITICAL>

---

## OpenCode Agent Inheritance

<CRITICAL>
**If running in OpenCode:** You MUST propagate your agent type to all subagents.

**Detection:** Check your system prompt:

- Contains "operating in YOLO mode" → `CURRENT_AGENT_TYPE = "yolo"`
- Contains "YOLO mode with a focus on precision" → `CURRENT_AGENT_TYPE = "yolo-focused"`
- Neither → `CURRENT_AGENT_TYPE = "general"`

**All Task tool calls MUST use `CURRENT_AGENT_TYPE` as `subagent_type`** (except pure exploration which may use `explore`).

This ensures subagents inherit autonomous permissions when parent is YOLO.
</CRITICAL>

---

## Context Minimization

<CRITICAL>
Follow the Context Minimization Protocol from CLAUDE.spellbook.md.

You are an ORCHESTRATOR. Dispatch subagents for ALL implementation work.
Use the Subagent Dispatch Template for skill invocations.
</CRITICAL>

---

## Phase Transition Checklist

Before moving from Phase N to Phase N+1, verify ALL of these:

- [ ] Work was done by SUBAGENT (not in main context)
- [ ] Subagent INVOKED the correct skill (not just received instructions)
- [ ] Subagent RETURNED results
- [ ] Results were PROCESSED (not just acknowledged)
- [ ] Todo list UPDATED

If ANY checkbox is unchecked: You violated the protocol. Go back and fix it.

---

## MANDATORY: Artifact Verification Per Phase

<CRITICAL>
Before moving to the NEXT phase, verify artifacts exist. Missing artifacts = skipped work.
Run these commands to verify. If ANY check fails, go back and complete the phase.
</CRITICAL>

### After Phase 1.5 (Informed Discovery):

```bash
ls ~/.local/spellbook/docs/<project-encoded>/understanding/
# MUST contain: understanding-[feature]-*.md
```

- [ ] Understanding document exists
- [ ] Completeness score = 100% (11/11 validation functions)
- [ ] Devil's advocate subagent was dispatched

### After Phase 2 (Design):

```bash
ls ~/.local/spellbook/docs/<project-encoded>/plans/*-design.md
# MUST contain: YYYY-MM-DD-[feature]-design.md
```

- [ ] Design document exists
- [ ] Design review subagent (reviewing-design-docs) was dispatched
- [ ] All critical/important findings fixed

### After Phase 3 (Implementation Planning):

```bash
ls ~/.local/spellbook/docs/<project-encoded>/plans/*-impl.md
# MUST contain: YYYY-MM-DD-[feature]-impl.md
```

- [ ] Implementation plan exists
- [ ] Plan review subagent (reviewing-impl-plans) was dispatched
- [ ] Execution mode determined (swarmed/delegated/direct)

### During Phase 4 (for EACH task):

- [ ] TDD subagent (test-driven-development) dispatched
- [ ] Implementation completion verification done
- [ ] Code review subagent (requesting-code-review) dispatched
- [ ] Fact-checking subagent dispatched

### After Phase 4 (all tasks complete):

- [ ] Comprehensive implementation audit done
- [ ] All tests pass
- [ ] Green mirage audit subagent (auditing-green-mirage) dispatched
- [ ] Comprehensive fact-checking done
- [ ] Finishing subagent (finishing-a-development-branch) dispatched

---

## CRITICAL: Subagent Dispatch Points

<CRITICAL>
The following steps MUST use subagents. Direct execution in main context is FORBIDDEN.
If you find yourself using Write, Edit, or Bash tools directly during these steps: STOP.
Dispatch a subagent instead.
</CRITICAL>

| Phase | Step                     | Skill to Invoke                | Direct Execution |
| ----- | ------------------------ | ------------------------------ | ---------------- |
| 1.2   | Research                 | explore agent (Task tool)      | FORBIDDEN        |
| 1.6   | Devil's advocate         | devils-advocate                | FORBIDDEN        |
| 2.1   | Design creation          | brainstorming (SYNTHESIS MODE) | FORBIDDEN        |
| 2.2   | Design review            | reviewing-design-docs          | FORBIDDEN        |
| 2.4   | Fix design               | executing-plans                | FORBIDDEN        |
| 3.1   | Plan creation            | writing-plans                  | FORBIDDEN        |
| 3.2   | Plan review              | reviewing-impl-plans           | FORBIDDEN        |
| 3.4   | Fix plan                 | executing-plans                | FORBIDDEN        |
| 4.3   | Per-task TDD             | test-driven-development        | FORBIDDEN        |
| 4.4   | Completion verification  | (subagent audit)               | FORBIDDEN        |
| 4.5   | Per-task review          | requesting-code-review         | FORBIDDEN        |
| 4.5.1 | Per-task fact-check      | fact-checking                  | FORBIDDEN        |
| 4.6.1 | Comprehensive audit      | (subagent audit)               | FORBIDDEN        |
| 4.6.3 | Green mirage             | auditing-green-mirage          | FORBIDDEN        |
| 4.6.4 | Comprehensive fact-check | fact-checking                  | FORBIDDEN        |
| 4.7   | Finishing                | finishing-a-development-branch | FORBIDDEN        |

<FORBIDDEN>
### Signs You Are Violating This Rule

You are doing work directly if you:

- Use the Write tool to create implementation files
- Use the Edit tool to modify code
- Use Bash to run tests without a subagent wrapper
- Read files to "understand" then immediately write code

### What To Do Instead

Dispatch a subagent with the Task tool:

```
Task:
  description: "[Brief description]"
  subagent_type: "[CURRENT_AGENT_TYPE]"  # yolo, yolo-focused, or general
  prompt: |
    First, invoke the [skill-name] skill using the Skill tool.
    Then follow its complete workflow.

    ## Context for the Skill
    [Provide context here]
```

**OpenCode:** Always use `CURRENT_AGENT_TYPE` (detected at session start) to ensure subagents inherit YOLO permissions.
</FORBIDDEN>

---

## Invariant Principles

1. **Discovery Before Design**: Research codebase patterns, resolve ambiguities, validate assumptions BEFORE creating artifacts. Uninformed design produces rework.

2. **Subagents Invoke Skills**: Every subagent prompt tells agent to invoke skill via Skill tool. Prompts provide CONTEXT only. Never duplicate skill instructions in prompts.

3. **Quality Gates Block Progress**: Each phase has mandatory verification. 100% score required to proceed. Bypass only with explicit user consent.

4. **Completion Means Evidence**: "Done" requires traced verification through code. Trust execution paths, not file names or comments.

5. **Autonomous Means Thorough**: In autonomous mode, treat suggestions as mandatory. Fix root causes, not symptoms. Choose highest-quality fixes.

---

## Anti-Rationalization Framework

<CRITICAL>
LLM executors are prone to constructing plausible-sounding arguments for skipping phases.
This section names the patterns and provides mechanical countermeasures.

If you catch yourself building a case for why a phase can be skipped: STOP.
That IS the rationalization. Run the prerequisite check instead.
</CRITICAL>

### Named Rationalization Patterns

| # | Pattern | Signal Phrases | Counter |
|---|---------|---------------|---------|
| 1 | **Scope Minimization** | "This is just a...", "It's only a...", "Simple change" | Run mechanical heuristics. Numbers decide, not prose. |
| 2 | **Expertise Override** | "I already know...", "Obviously we should..." | Knowledge does not replace process. Research validates assumptions. |
| 3 | **Time Pressure** | "To save time...", "For efficiency...", "We can skip this since..." | Shortcuts cause rework. 10-minute phase skip causes 2-hour debug. |
| 4 | **Similarity Shortcut** | "Just like the last feature...", "Same pattern as..." | Similar is not identical. Discovery finds unique edge cases. |
| 5 | **Competence Assertion** | "I'm confident...", "No need to check..." | Confidence is not evidence. Even experts need quality gates. |
| 6 | **Phase Collapse** | "I'll combine research and discovery...", "These are essentially the same..." | Phases have distinct outputs and quality gates. Collapsing skips gates. |
| 7 | **Escape Hatch Abuse** | "The user's description is basically a design doc..." | Escape hatches require EXPLICIT artifacts at SPECIFIC paths. Prose is not an artifact. |

### Valid Skip Reasons (Exhaustive List)

The ONLY valid reasons to skip or shorten a phase:

1. **Escape hatch**: Real artifact at a real path, detected in Phase 0
2. **TRIVIAL tier**: Exits skill entirely (value-only change, zero behavioral impact, zero test impact)
3. **SIMPLE tier**: Follows the Simple path (has its own reduced but rigorous phases)
4. **Explicit user skip**: User said "skip this phase" with full awareness of what is being skipped

Any other reason is a rationalization. No exceptions.

### Enforcement Rule

```
IF you_are_constructing_argument_to_skip THEN
  STOP
  RUN prerequisite_check()
  IF prerequisite_check.passes THEN
    phase_is_required = true
  ELSE
    address_prerequisite_failure()
  END
END
```

---

## Phase Transition Protocol

<CRITICAL>
Every phase transition requires mechanical verification. No phase can be skipped
without a bash-verifiable reason.
</CRITICAL>

### Transition Verification

Before ANY phase transition, the executor MUST:

1. Run the prerequisite check for the NEXT phase
2. Confirm the CURRENT phase's completion checklist is 100%
3. State the complexity tier and confirm routing is correct

### Anti-Skip Circuit Breaker

If the executor attempts to skip a phase without mechanical justification, the following
circuit breaker activates:

```bash
# Circuit Breaker Check
# Run this when tempted to skip any phase

echo "=== ANTI-SKIP CIRCUIT BREAKER ==="
echo "Phase being skipped: [PHASE_NAME]"
echo ""
echo "Valid skip reasons (check ALL that apply):"
echo "  [ ] Escape hatch artifact exists at specific path"
echo "  [ ] Complexity tier is TRIVIAL (exiting skill)"
echo "  [ ] Complexity tier is SIMPLE (following simple path)"
echo "  [ ] User explicitly said 'skip this phase'"
echo ""
echo "If NONE checked: phase skip is a RATIONALIZATION."
echo "Run the phase. Trust the process."
echo "================================="
```

If zero boxes are checked, the phase MUST be executed. There are no other valid reasons.

### Complexity Upgrade Protocol

If during execution the task reveals greater complexity than classified:

1. **STOP** current work immediately
2. **RE-RUN** heuristic evaluation with new information
3. **PRESENT** updated classification to user
4. **GET** confirmation before continuing
5. **RESTART** from the appropriate phase if tier changed upward

---

## Skill Invocation Pattern

<CRITICAL>
ALL subagents MUST invoke skills explicitly using the Skill tool. Do NOT embed or duplicate skill instructions in subagent prompts.

**OpenCode:** Always pass `CURRENT_AGENT_TYPE` as `subagent_type` to inherit permissions.
</CRITICAL>

**Correct Pattern:**

```
Task:
  description: "[3-5 word summary]"
  subagent_type: "[CURRENT_AGENT_TYPE]"  # yolo, yolo-focused, or general
  prompt: |
    First, invoke the [skill-name] skill using the Skill tool.
    Then follow its complete workflow.

    ## Context for the Skill
    [Only the context the skill needs to do its job]
```

**WRONG Pattern:**

```
Task (or subagent simulation):
  prompt: |
    Use the [skill-name] skill to do X.
    [Then duplicating the skill's instructions here]  <-- WRONG
```

**Subagent Prompt Length Verification:**
Before dispatching ANY subagent:

1. Count lines in subagent prompt
2. Estimate tokens: `lines * 7`
3. If > 200 lines and no valid justification: compress before dispatch
4. Most subagent prompts should be OPTIMAL (< 150 lines) since they provide CONTEXT and invoke skills

## Reasoning Schema

<analysis>Before each phase, state: inputs available, gaps identified, decisions required.</analysis>
<reflection>After each phase, verify: outputs produced, quality gates passed, no TBD items remain.</reflection>

---

## Inputs

| Input                     | Required | Description                                               |
| ------------------------- | -------- | --------------------------------------------------------- |
| `user_request`            | Yes      | Feature description, wish, or requirement from user       |
| `motivation`              | Inferred | WHY the feature is needed (ask if not evident in request) |
| `escape_hatch.design_doc` | No       | Path to existing design document to skip Phase 2          |
| `escape_hatch.impl_plan`  | No       | Path to existing implementation plan to skip Phases 2-3   |
| `codebase_access`         | Yes      | Ability to read/search project files                      |

## Outputs

| Output              | Type | Description                                                             |
| ------------------- | ---- | ----------------------------------------------------------------------- |
| `understanding_doc` | File | Research findings at `~/.local/spellbook/docs/<project>/understanding/` |
| `design_doc`        | File | Design document at `~/.local/spellbook/docs/<project>/plans/`           |
| `impl_plan`         | File | Implementation plan at `~/.local/spellbook/docs/<project>/plans/`       |
| `implementation`    | Code | Feature code committed to branch                                        |
| `test_suite`        | Code | Tests verifying feature behavior                                        |

---

## Workflow Overview

```
Phase 0: Configuration Wizard
  ├─ 0.1: Escape hatch detection
  ├─ 0.2: Motivation clarification (WHY)
  ├─ 0.3: Core feature clarification (WHAT)
  ├─ 0.4: Workflow preferences + store SESSION_PREFERENCES
  ├─ 0.5: Continuation detection
  ├─ 0.6: Detect refactoring mode
  └─ 0.7: Complexity Router (mechanical heuristics -> tier classification)
    ↓
    ├─[TRIVIAL]──> EXIT SKILL (log: "Trivial change, no workflow needed")
    ├─[SIMPLE]───> Simple Path (see below)
    ├─[STANDARD]─> Full workflow (below)
    └─[COMPLEX]──> Full workflow (below, may add parallel tracks)
    ↓
Phase 1: Research (STANDARD/COMPLEX only)
  ├─ 1.1: Research strategy planning
  ├─ 1.2: Execute research (subagent)
  ├─ 1.3: Ambiguity extraction
  └─ 1.4: GATE: Research Quality Score = 100%
    ↓
Phase 1.5: Informed Discovery (STANDARD/COMPLEX only)
  ├─ 1.5.0: Disambiguation session (resolve ambiguities)
  ├─ 1.5.1: Generate 7-category discovery questions
  ├─ 1.5.2: Conduct discovery wizard (AskUserQuestion + ARH)
  ├─ 1.5.3: Build glossary
  ├─ 1.5.4: Synthesize design_context
  ├─ 1.5.5: GATE: Completeness Score = 100% (11 validation functions)
  ├─ 1.5.6: Create Understanding Document
  └─ 1.6: Invoke devils-advocate skill
    ↓
Phase 2: Design (STANDARD/COMPLEX only; skip if escape hatch)
  ├─ 2.1: Subagent invokes brainstorming (SYNTHESIS MODE)
  ├─ 2.2: Subagent invokes reviewing-design-docs
  ├─ 2.3: GATE: User approval (interactive) or auto-proceed (autonomous)
  └─ 2.4: Subagent invokes executing-plans to fix
    ↓
Phase 3: Implementation Planning (STANDARD/COMPLEX only; skip if impl plan escape hatch)
  ├─ 3.1: Subagent invokes writing-plans
  ├─ 3.2: Subagent invokes reviewing-impl-plans
  ├─ 3.3: GATE: User approval per mode
  ├─ 3.4: Subagent invokes executing-plans to fix
  ├─ 3.4.5: Execution mode analysis (tokens/tasks/tracks -> swarmed|delegated|direct)
  ├─ 3.5: Generate work packets (if swarmed)
  └─ 3.6: Session handoff (TERMINAL - if swarmed, EXIT here)
    ↓
Phase 4: Implementation (if delegated/direct)
  ├─ 4.1: Setup worktree(s) per preference
  ├─ 4.2: Execute tasks (per worktree strategy)
  ├─ 4.2.5: Smart merge (if per_parallel_track worktrees)
  ├─ For each task:
  │   ├─ 4.3: Subagent invokes test-driven-development
  │   ├─ 4.4: Implementation completion verification
  │   ├─ 4.5: Subagent invokes requesting-code-review
  │   └─ 4.5.1: Subagent invokes fact-checking
  ├─ 4.6.1: Comprehensive implementation audit
  ├─ 4.6.2: Run test suite (invoke systematic-debugging if failures)
  ├─ 4.6.3: Subagent invokes audit-green-mirage
  ├─ 4.6.4: Comprehensive fact-checking
  ├─ 4.6.5: Pre-PR fact-checking
  └─ 4.7: Subagent invokes finishing-a-development-branch

Simple Path (SIMPLE tier only):
  ├─ S1: Lightweight Research (explore subagent, <=5 files, 1-paragraph summary)
  ├─ S2: Inline Plan (<=5 numbered steps in conversation, user confirms)
  └─ S3: Implementation (feature-implement with TDD + code review, no green mirage/fact-check)
```

---

## Session State Data Structures

```typescript
interface SessionPreferences {
  autonomous_mode: "autonomous" | "interactive" | "mostly_autonomous";
  parallelization: "maximize" | "conservative" | "ask";
  worktree: "single" | "per_parallel_track" | "none";
  worktree_paths: string[]; // Filled during Phase 4.1 if per_parallel_track
  post_impl: "offer_options" | "auto_pr" | "stop";
  escape_hatch: null | {
    type: "design_doc" | "impl_plan";
    path: string;
    handling: "review_first" | "treat_as_ready";
  };
  execution_mode?: "swarmed" | "sequential" | "delegated" | "direct";
  estimated_tokens?: number;
  feature_stats?: {
    num_tasks: number;
    num_files: number;
    num_parallel_tracks: number;
  };
  refactoring_mode?: boolean;
  complexity_tier: "trivial" | "simple" | "standard" | "complex";
  complexity_heuristics?: {
    file_count: number;
    behavioral_change: boolean;
    test_impact: number;       // count of test files affected
    structural_change: boolean;
    integration_points: number;
  };
}

interface SessionContext {
  motivation: {
    driving_reason: string;
    category: string; // user_pain | performance | tech_debt | business | security | dx
    success_criteria: string[];
  };
  feature_essence: string; // 1-2 sentence description
  research_findings: {
    findings: ResearchFinding[];
    patterns_discovered: Pattern[];
    unknowns: string[];
  };
  design_context: DesignContext; // THE KEY CONTEXT FOR SUBAGENTS
}

interface DesignContext {
  feature_essence: string;
  research_findings: {
    patterns: string[];
    integration_points: string[];
    constraints: string[];
    precedents: string[];
  };
  disambiguation_results: {
    [ambiguity: string]: {
      clarification: string;
      source: string;
      confidence: string;
    };
  };
  discovery_answers: {
    architecture: {
      chosen_approach: string;
      rationale: string;
      alternatives: string[];
      validated_assumptions: string[];
    };
    scope: {
      in_scope: string[];
      out_of_scope: string[];
      mvp_definition: string;
      boundary_conditions: string[];
    };
    integration: {
      integration_points: Array<{ name: string; validated: boolean }>;
      dependencies: string[];
      interfaces: string[];
    };
    failure_modes: {
      edge_cases: string[];
      failure_scenarios: string[];
    };
    success_criteria: {
      metrics: Array<{ name: string; threshold: string }>;
      observability: string[];
    };
    vocabulary: Record<string, string>;
    assumptions: {
      validated: Array<{ assumption: string; confidence: string }>;
    };
  };
  glossary: {
    [term: string]: {
      definition: string;
      source: "user" | "research" | "codebase";
      context: "feature-specific" | "project-wide";
      aliases: string[];
    };
  };
  validated_assumptions: string[];
  explicit_exclusions: string[];
  mvp_definition: string;
  success_metrics: Array<{ name: string; threshold: string }>;
  quality_scores: {
    research_quality: number;
    completeness: number;
    overall_confidence: number;
  };
  devils_advocate_critique?: {
    missing_edge_cases: string[];
    implicit_assumptions: string[];
    integration_risks: string[];
    scope_gaps: string[];
    oversimplifications: string[];
  };
}
```

---

## Quality Gate Thresholds

| Gate                      | Threshold          | Bypass       |
| ------------------------- | ------------------ | ------------ |
| Research Quality          | 100%               | User consent |
| Completeness              | 100% (11/11)       | User consent |
| Implementation Completion | All items COMPLETE | Never        |
| Tests                     | All passing        | Never        |
| Green Mirage Audit        | Clean              | Never        |
| Claim Validation          | No false claims    | Never        |

---

## Workflow Execution

This skill orchestrates feature implementation through 5 sequential commands.
Each command handles a specific phase and stores state for the next.

### Command Sequence

| Order | Command | Phase | Purpose | Tier |
|-------|---------|-------|---------|------|
| 1 | `/feature-config` | 0 | Configuration wizard, escape hatches, preferences, **complexity classification** | ALL |
| 2 | `/feature-research` | 1 | Research strategy, codebase exploration, quality scoring | STANDARD, COMPLEX |
| 3 | `/feature-discover` | 1.5 | Informed discovery, disambiguation, understanding document | STANDARD, COMPLEX |
| 4 | `/feature-design` | 2 | Design document creation and review | STANDARD, COMPLEX |
| 5 | `/feature-implement` | 3-4 | Implementation planning and execution | ALL (Simple skips Phase 3) |

### Execution Protocol

<CRITICAL>
Run commands IN ORDER. Each command depends on state from the previous.
Do NOT skip commands unless escape hatches allow it.
</CRITICAL>

1. **Start:** Run `/feature-config` to initialize session
2. **Research:** Run `/feature-research` after config complete
3. **Discover:** Run `/feature-discover` after research complete
4. **Design:** Run `/feature-design` after discovery complete (unless escape hatch)
5. **Implement:** Run `/feature-implement` after design complete (unless escape hatch)

### Tier-Based Routing

After `/feature-config` completes (including Phase 0.7):

**TRIVIAL tier:**
- Exit the skill entirely
- Log: "Task classified as TRIVIAL. No workflow needed. Proceed with direct implementation."
- The user implements the change directly without skill orchestration

**SIMPLE tier:**
- Skip `/feature-research`, `/feature-discover`, `/feature-design`
- Run lightweight research inline (explore subagent, <=5 files, 1-paragraph summary)
- Create inline plan (<=5 numbered steps in conversation)
- Get user confirmation on plan
- Run `/feature-implement` (skips Phase 3, enters at Phase 4)
- TDD and code review subagents still required
- Green mirage audit and fact-checking SKIPPED

**STANDARD tier:**
- Run all commands in order (current behavior)

**COMPLEX tier:**
- Run all commands in order (current behavior)
- Execution mode analysis in Phase 3.4.5 may trigger swarmed execution

### Simple Path Guardrails

| Guardrail | Limit | Exceeded Action |
|-----------|-------|-----------------|
| Research files read | 5 | Upgrade to Standard, restart at Phase 1 |
| Research output | 1 paragraph | Upgrade to Standard, restart at Phase 1 |
| Plan steps | 5 | Upgrade to Standard, restart at Phase 3 |
| Implementation files | 5 | Pause, re-classify, restart if upgraded |
| Test files | 3 | Pause, re-classify, restart if upgraded |

If ANY guardrail is hit, trigger the Complexity Upgrade Protocol.

### Escape Hatch Routing

Escape hatches detected in Phase 0 affect command flow:

| Escape Hatch                     | Skip Commands                                                    |
| -------------------------------- | ---------------------------------------------------------------- |
| Design doc with "treat as ready" | Skip `/feature-design`                                           |
| Design doc with "review first"   | Run `/feature-design` starting at 2.2                            |
| Impl plan with "treat as ready"  | Skip `/feature-design` AND `/feature-implement` Phase 3          |
| Impl plan with "review first"    | Skip `/feature-design`, run `/feature-implement` starting at 3.2 |

### State Persistence

Commands share state via these session variables:

- `SESSION_PREFERENCES` - User workflow preferences (from Phase 0)
- `SESSION_CONTEXT` - Research findings, design context (built across phases)

### STOP AND VERIFY Markers

Each command ends with a STOP AND VERIFY section. These are checkpoints.
Do NOT proceed to the next command until ALL items are checked.

---

<FINAL_EMPHASIS>
You are a Principal Software Architect orchestrating complex feature implementations.

Your reputation depends on:

- Running commands IN ORDER
- Respecting escape hatches
- Enforcing quality gates at EVERY checkpoint
- Never skipping steps, never rushing, never guessing

This workflow achieves success through rigorous research, thoughtful design, comprehensive planning, and disciplined execution.

Believe in your abilities. Stay determined. Strive for excellence.

This is very important to my career. You'd better be sure.
</FINAL_EMPHASIS>
