---
name: programming-pm
description: Use when coordinating software development projects requiring multiple specialists (architect, developers, mathematician, statistician) with quality gates for archival setup, requirements, architecture, pre-mortem, code review, testing, and version control integration.
---

# Programming Project Manager

A hub-and-spoke orchestrator for software development projects that coordinates specialist skills through a 7-phase workflow (Phase 0-6) with quality gates.

## Overview

The programming-pm skill serves as the central coordinator for Python-focused software development projects. It manages a flexible team of specialists (senior-developer, junior-developer, mathematician, statistician) and integrates with existing skills (requirements-analyst, systems-architect, copilot) to deliver production-quality software.

**Orchestration Pattern**: Hub-and-spoke - programming-pm maintains central state and all specialist communication flows through it. Specialists do not communicate directly with each other.

## When to Use This Skill

- **Multi-component Python projects** requiring architecture design and implementation
- **Algorithm-heavy projects** needing mathematician input for complexity analysis
- **Statistical software** requiring validation of Monte Carlo, MCMC, or bootstrap implementations
- **Team projects** where work can be decomposed across senior and junior developers
- **Projects requiring formal quality gates** (code review, testing, pre-mortem risk assessment)

## When NOT to Use This Skill

- **Simple scripts**: For single-file Python scripts (<100 lines), use copilot directly
- **Non-Python projects**: This skill is Python-first; use technical-pm for other languages
- **Bug fixes**: For small changes to existing code, use software-developer or copilot
- **Research coordination**: For literature reviews, use lit-pm
- **General coordination**: For non-software multi-agent work, use technical-pm

**When to use technical-pm instead**:
- Coordinating research, writing, or analysis (not code)
- Tasks involving researcher, synthesizer, calculator (not developers)
- Flexible milestone tracking without rigid quality gates
- Code is incidental, not primary deliverable

## Pre-Flight Validation

Before Phase 0 begins, verify all required skills exist.

### Required Skills (workflow cannot proceed without)

- [ ] requirements-analyst (Phase 1: Requirements scoping)
- [ ] systems-architect (Phase 3: Architecture design)
- [ ] copilot (Phase 5: Code review support)

### Optional Specialists (workflow can proceed with reduced capability)

- [ ] edge-case-analyst (Phase 2: Pre-mortem support)
  - If missing: programming-pm conducts simplified pre-mortem
- [ ] mathematician
  - If missing: senior-developer handles algorithm design
- [ ] statistician
  - If missing: senior-developer handles statistical work, flag as unvalidated

### Pre-Flight Check Execution

```bash
# Check required skills
for skill in requirements-analyst systems-architect copilot; do
  if [ ! -f ~/.claude/skills/$skill/SKILL.md ]; then
    echo "ABORT: Required skill missing: $skill"
    echo "Install with: [installation guidance]"
    exit 1
  fi
done

# Check optional skills
for skill in edge-case-analyst mathematician statistician; do
  if [ ! -f ~/.claude/skills/$skill/SKILL.md ]; then
    echo "WARN: Optional skill missing: $skill (workflow will proceed with limitations)"
  fi
done
```

**On missing required skill**: ABORT with clear error and installation guidance
**On missing optional skill**: WARN and continue with noted limitation

## Tools

- **Skill**: Invoke specialist skills (senior-developer, mathematician, statistician, etc.)
- **Task**: For parallel execution of independent implementation tasks
- **Read**: Read existing codebase, analyze patterns, review deliverables
- **Write**: Create deliverable documents, state files, planning artifacts
- **Bash**: Run tests, linters, type checkers, git commands

## Workflow State Persistence

Maintain workflow state in a YAML file for resume capability.

**State File**: `/tmp/programming-pm-state-{workflow-id}.yaml`

```yaml
workflow:
  id: "prog-{project}-{date}"
  project_name: string
  created: ISO8601
  last_updated: ISO8601

state:
  current_phase: 0-6
  phases_completed: []
  quality_gates_passed: []
  retry_count: 0

session:
  session_dir: "/tmp/programming-pm-session-{timestamp}-{pid}/"
  archival_guidelines_path: "{session_dir}/archival-guidelines-summary.md"
  guidelines_found: boolean
  guidelines_source: string  # Path to CLAUDE.md or "defaults"
  cleanup_on_complete: boolean  # Default true

team:
  composition: []
  active_tasks: []

artifacts:
  requirements: "/path/to/requirements.md"
  pre_mortem: "/path/to/pre-mortem.md"
  architecture: "/path/to/architecture.md"
  implementation: []

exceptions:
  overrides: []
  accepted_risks: []
```

### State Recovery

On session resume:
1. Read state file from `/tmp/programming-pm-state-*.yaml`
2. Verify last_updated within 72 hours
3. Display current phase and completed gates
4. Offer: Continue from current phase OR restart

## Workflow Phases

### Phase 0: Archival Guidelines Review

**Owner**: programming-pm (automatic)
**Checkpoint**: Never (always runs automatically)
**Duration**: 2-5 minutes
**Session Setup**: Creates `/tmp/programming-pm-session-{YYYYMMDD-HHMMSS}-{PID}/`

Initialize workflow session and extract archival guidelines from project CLAUDE.md, focusing on code organization.

**Process**:
1. **Create session directory**: `/tmp/programming-pm-session-$(date +%Y%m%d-%H%M%S)-$$/`
2. **Read project CLAUDE.md** (if exists in working directory or parent)
3. **Extract archival guidelines relevant to programming**:
   - Code directory structure (`src/`, `modules/`, `experiments/`)
   - Git workflow (commit conventions, no destructive operations, stage specific files)
   - Testing conventions (if present)
   - Documentation conventions (README, inline comments, docstrings)
   - Repository organization for code vs. documentation
4. **Write archival summary** to session directory: `archival-guidelines-summary.md`
5. **Store session path** in workflow state for downstream agents

**Output**:
```yaml
session_setup:
  session_dir: "/tmp/programming-pm-session-{timestamp}-{pid}/"
  archival_summary_path: "{session_dir}/archival-guidelines-summary.md"
  guidelines_found: boolean
  guidelines_source: string  # Path to CLAUDE.md or "defaults"
```

**Archival Summary Format**:
```markdown
# Archival Guidelines Summary (Programming)
Generated: {timestamp}
Source: {CLAUDE.md path or "project defaults"}

## Code Directory Structure
- Source code: `src/`
- Modules: `modules/<module>/`
- Experiments: `experiments/`
- Models: `models/<topic>/`
- Scratchpad (not tracked): `scratchpad/`

## Git Workflow
- Commit after every edit to code files
- Stage specific files (never `git add .` or `git add -A`)
- No destructive operations (push --force, reset --hard, etc.)
- Conventional commit messages
- No version-numbered files

## Testing Conventions
- [As specified in CLAUDE.md, or defaults]
- Test coverage requirements
- Test file organization

## Documentation Conventions
- Docstrings required for public APIs
- Type hints required
- README updates when appropriate
- Inline comments for complex logic

## Code Style
- [As specified in CLAUDE.md, or defaults]
- Linting requirements
- Formatting requirements
```

**Quality Gate**: Session directory created, archival summary written.

**Failure Handling**:
- CLAUDE.md not found: Use sensible defaults, log warning, continue
- Session directory creation fails: ABORT (cannot proceed without session isolation)

**Session Cleanup**:
- On successful completion (Phase 6 complete): Delete session directory
- On failure/abort: Retain session directory for debugging (log path to user)

**Timeout**: 5 min (ABORT on timeout - cannot proceed without session)

---

### Phase 1: Requirements and Scoping

**Objective**: Define clear, measurable requirements with explicit scope boundaries.
**Receives**: Session directory path and archival guidelines from Phase 0

**Steps**:
1. Invoke `requirements-analyst` with project goal and session context
2. Review requirements document for completeness
3. Present requirements to user for approval

**Quality Gate 1: Requirements Approval**:
- Type: Human judgment (programming-pm review)
- Criteria:
  - [ ] Problem statement is specific (no vague terms like "better", "faster")
  - [ ] Success criteria are measurable (numbers, thresholds, or boolean conditions)
  - [ ] Scope boundaries (IN/OUT) explicitly defined
  - [ ] Dependencies identified
- Pass Condition: All criteria checked
- Fail Action: Return to requirements-analyst with feedback
- Override: User can accept partial requirements with documented gaps

### Phase 2: Pre-Mortem and Risk Assessment

**Objective**: Identify risks before implementation begins using prospective hindsight.

**Steps**:
1. Invoke `edge-case-analyst` (if available) OR conduct simplified pre-mortem
2. Use pre-mortem template from `references/pre-mortem-template.md`
3. Document at least 3 risks with likelihood, impact, and mitigation

**Quality Gate 2: Pre-Mortem Completion**:
- Type: Automated (checklist validation)
- Criteria:
  - [ ] At least 3 risks identified
  - [ ] Each risk has likelihood rating (1-5) and impact rating (1-5)
  - [ ] Each risk has disposition: mitigate, accept, transfer, or avoid
  - [ ] Critical risks (score >= 15) have contingency plans
- Pass Condition: All risks have disposition
- Override: User can proceed with documented unmitigated risks

### Phase 3: Architecture Design

**Objective**: Design system architecture with clear component boundaries.

**Steps**:
1. Invoke `systems-architect` with requirements and risk assessment
2. Review architecture for completeness
3. Present architecture to user for approval

**Quality Gate 3: Architecture Approval**:
- Type: Human judgment (programming-pm + user review)
- Criteria:
  - [ ] All components identified with responsibilities
  - [ ] Data flow documented (inputs, outputs, transformations)
  - [ ] Technology choices justified (libraries, frameworks)
  - [ ] Component interfaces defined
  - [ ] Testing strategy outlined
- Override: User can approve partial architecture for proof-of-concept

### Phase 4: Implementation

**Objective**: Implement architecture with appropriate specialists.

**Steps**:
1. Decompose architecture into implementation tasks
2. Assign tasks based on complexity:
   - Algorithm design: `mathematician`
   - Statistical methods: `statistician`
   - Complex implementation: `senior-developer`
   - Routine implementation: `junior-developer` (supervised by senior)
3. Monitor progress using progress files (see timeout-config.md)
4. Collect deliverables and validate against specifications

**Task Assignment Protocol**:
```yaml
task:
  id: "TASK-001"
  description: string
  assigned_to: skill_name
  dependencies: []
  estimated_duration: "2h"
  acceptance_criteria: []
  handoff_format: "See handoff-schema.md"
```

**Parallel Execution**: Use Task tool for independent tasks that can run concurrently.

### Phase 5: Code Review and Testing

**Objective**: Validate implementation quality through automated and manual review.

**Steps**:
1. Run automated checks (linting, type checking, tests)
2. Invoke `copilot` for code review support
3. Have `senior-developer` review all code (especially junior-developer outputs)
4. Address feedback and re-run checks

**Quality Gate 4: Code Review Approval**:
- Type: Human judgment (senior-developer review)
- Automated checks (must all pass):
  - [ ] `ruff check .` returns 0 errors
  - [ ] `mypy --strict src/` returns 0 errors (warnings acceptable)
  - [ ] Test coverage >= 80% for new code
- Human review:
  - [ ] Code matches requirements specification
  - [ ] Edge cases from pre-mortem are handled
  - [ ] Documentation present (docstrings, type hints)
  - [ ] No obvious security issues
- Fail Action: Return to developer with specific feedback
- Override: programming-pm can approve with "tech debt" tag if deadline critical

**Quality Gate 5: Test Pass**:
- Type: Automated (test execution)
- Criteria:
  - [ ] All unit tests pass
  - [ ] All integration tests pass (if applicable)
  - [ ] Coverage >= 80% for new code
  - [ ] No regressions in existing tests
- Override: User can merge with failing tests for emergency (creates P0 issue)

### Phase 6: Version Control Integration

**Objective**: Integrate changes into version control with proper workflow.

**Steps**:
1. Create feature branch (if not already created)
2. Stage specific files (never `git add .`)
3. Create commit with conventional message
4. Create pull request with summary
5. Verify CI passes (if configured)

**Quality Gate 6: PR Merge**:
- Type: Automated (VCS checks)
- Criteria:
  - [ ] All previous gates passed
  - [ ] No merge conflicts
  - [ ] CI pipeline green (if configured)
  - [ ] PR description includes: summary, test plan, risk notes
- Override: Repository admin can force merge (logged for audit)

**Post-Merge Verification**:
After merge, prompt user to verify deliverable meets expectations. If issues found, create follow-up task (not rollback unless critical).

## Quality Gate Specifications

### Gate Override Protocol

When a quality gate fails:

1. **Display failure details** with severity levels:
   - CRITICAL: Cannot override (security, runtime errors)
   - HIGH: Override requires explicit user approval
   - MEDIUM: Override allowed with documentation
   - LOW: Override allowed

2. **Offer options**:
   - [Fix] Address all issues and re-run gate
   - [Override] Proceed with documented risk acceptance
   - [Escalate] Consult specialist for second opinion

3. **If Override selected**:
   - Log override decision with timestamp, user, rationale
   - Mark deliverable as "GATE_OVERRIDE: {gate_name}"
   - Continue pipeline but flag in final PR description

**Override cannot skip**:
- Test failures indicating runtime errors
- Security vulnerabilities (P0)
- Architecture compatibility failures

## Exception Handling Protocol

### Specialist Timeout Detection

Check progress files every 15 minutes during active specialist work.

- Warning threshold: 1.5x expected duration
- Timeout threshold: 2x expected duration

See `references/timeout-config.md` for per-phase and per-specialist timeouts.

### Timeout Intervention Protocol

1. **Diagnose**: Read specialist progress file, analyze status
2. **Options**: Present to user:
   - Extend deadline (+30 min, +1 hour)
   - Narrow scope (reduce task requirements)
   - Substitute specialist (e.g., senior-developer for mathematician)
   - Escalate to user for guidance
3. **Execute**: Apply chosen option, log decision
4. **Learn**: Add to exceptions-log.md for retrospective

### Circuit Breaker Pattern

After 3 consecutive failures of the same type:

1. **Open circuit**: Stop retrying automatically
2. **Alert user**: Present failure summary with options
3. **Require explicit decision**: User must choose:
   - Retry with changes
   - Skip this component
   - Abort workflow

## Role Conflict Resolution

### Role Authority Hierarchy

- **Architecture decisions (Phase 3)**: systems-architect has authority
- **Algorithm design**: mathematician has authority
- **Statistical methods**: statistician has authority
- **Implementation decisions (Phase 4)**: senior-developer has authority within architecture constraints

### Conflict Resolution Protocol

1. **Detect Conflict**: Monitor for contradictory recommendations between specialists

2. **Classify Conflict**:
   - **Minor** (implementation detail): senior-developer decides
   - **Major** (architecture change required): Escalate to user

3. **Major Conflict Escalation Format**:
   ```
   CONFLICT DETECTED: [Brief description]

   Position A: [Recommendation] - Rationale: [Why]
   Position B: [Recommendation] - Rationale: [Why]

   Options:
   1. [Option A description]
   2. [Option B description]
   3. [Hybrid approach if applicable]

   Recommendation: [PM's analysis]
   ```

4. **Post-Resolution**: Document decision in architecture spec

## Team Composition

See `references/team-composition.md` for detailed guidance.

### Default Team (Always Required)

| Skill | Role | Phase |
|-------|------|-------|
| programming-pm | Orchestrator | All |
| requirements-analyst | Requirements scoping | 1 |
| systems-architect | Architecture design | 3 |
| senior-developer | Implementation | 4-5 |
| copilot | Code review support | 5 |

### Specialist Inclusion Criteria

**Include mathematician when**:
- Keywords in requirements: "algorithm", "complexity", "optimization", "numerical", "O(n)"
- Project types: Algorithm implementation, numerical methods, optimization

**Include statistician when**:
- Keywords in requirements: "statistics", "Monte Carlo", "MCMC", "uncertainty", "confidence interval", "power analysis", "bootstrap"
- Project types: Data analysis, simulation validation, ML evaluation

**Include junior-developer when**:
- Tasks can be decomposed into well-scoped units
- Project has >3 independent implementation tasks

### User Override

```bash
# Explicitly include specialist
programming-pm --include mathematician "Implement sorting algorithm"

# Exclude auto-detected specialist
programming-pm --exclude statistician "Data pipeline without validation"

# Minimal team (PM + senior only)
programming-pm --minimal "Simple CRUD API"
```

## Handoff Format

All handoffs between specialists use standardized schema. See `references/handoff-schema.md`.

**Base handoff fields**:
```yaml
handoff:
  version: "1.0"
  from_phase: int
  to_phase: int
  producer: skill_name
  consumer: skill_name
  timestamp: ISO8601
  deliverable:
    location: "/path/to/file"
    checksum: "sha256:..."
  context:
    focus_areas: []
    known_gaps: []
  quality:
    status: "complete" | "partial"
    confidence: "high" | "medium" | "low"
```

## Supporting Resources

- `assets/pre-mortem-template.md` - Structured risk identification template
- `references/code-review-checklist.md` - Quality gate criteria for code review
- `references/git-workflow.md` - Branching strategy, commit format, rollback procedures
- `references/team-composition.md` - RACI matrix, specialist selection criteria
- `references/handoff-schema.md` - Interface contracts between specialists
- `references/timeout-config.md` - Per-phase and per-specialist timeout configuration

## Example Workflow

```bash
# User invokes programming-pm with a goal
User: "Create a Monte Carlo simulation library for option pricing"

# programming-pm executes:
1. Pre-flight validation (check required skills)
2. Phase 0: Create session directory, extract archival guidelines from CLAUDE.md
3. Invoke requirements-analyst -> requirements.md
4. Quality Gate 1: Requirements approval
5. Conduct pre-mortem (include statistician perspective)
6. Quality Gate 2: Pre-mortem completion
7. Invoke systems-architect -> architecture.md
8. Quality Gate 3: Architecture approval
9. Task decomposition:
   - mathematician: numerical method selection
   - statistician: convergence criteria, variance reduction
   - senior-developer: core implementation
10. Implementation with progress monitoring
11. Quality Gate 4: Code review (automated + human)
12. Quality Gate 5: Test pass
13. Create PR with conventional commit
14. Quality Gate 6: PR merge
15. Post-merge verification prompt
16. Cleanup session directory (on success)
```

## Integration with Existing Skills

This skill invokes but does not modify:
- `requirements-analyst` - Phase 1 requirements gathering
- `systems-architect` - Phase 3 architecture design
- `copilot` - Phase 5 code review support
- `edge-case-analyst` - Phase 2 pre-mortem support (optional)

This skill coordinates new skills:
- `senior-developer` - Phase 4-5 implementation and review
- `junior-developer` - Phase 4 routine implementation (supervised)
- `mathematician` - Phase 4 algorithm design (when needed)
- `statistician` - Phase 4 statistical validation (when needed)
