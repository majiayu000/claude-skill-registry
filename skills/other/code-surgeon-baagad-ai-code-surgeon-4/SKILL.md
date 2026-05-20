---
name: code-surgeon-implementation-planner
description: Use when synthesizing code context to create detailed implementation plans with task breakdown and effort estimates
---

# code-surgeon Implementation Planner

## Overview

**implementation-planner** is the critical sub-skill that bridges detailed codebase analysis (Phase 3: Context Researcher) with precise implementation instructions (Phase 5: Surgical Prompt Generator).

**Core principle:** Transform all collected context (issue analysis, framework detection, file selection, dependencies, patterns, conventions) into a structured 6-section implementation plan that guides the actual coding work.

---

## When to Use

This skill runs automatically as **Subagent 4 in the code-surgeon pipeline**. It executes after:
- ✅ Phase 1: Issue analysis and framework detection (completed in parallel)
- ✅ Phase 2-3: Context research and file selection (completed sequentially)

The main orchestrator automatically dispatches the Implementation Planner when you invoke:

```bash
/code-surgeon "GitHub issue URL or plain text requirement"
```

---

## What It Does

### Input Processing

Receives outputs from all prior phases:

```typescript
Input: {
  // From Issue Analyzer
  issue_type: "feature" | "bug" | "refactor" | "performance" | "docs";
  requirements: string[];
  scope: "small" | "medium" | "large";
  deadline: string | null;

  // From Framework Detector
  primary_language: string;
  primary_framework: string | null;
  frameworks: Array<{name, version, language}>;
  is_monorepo: boolean;

  // From Context Researcher
  files_selected: Array<{path, tier, relevance_score, content}>;
  dependency_graph: {[file: string]: string[]};
  patterns_found: Array<{name, description, examples}>;
  team_conventions: Array<{convention, category, examples}>;
  token_analysis: {total_tokens, budget, utilization_percent};
}
```

### Output: 6-Section Implementation Plan

```typescript
Output: {
  // 1. SUMMARY SECTION
  summary: {
    overview: "2-3 sentence executive summary";
    key_challenges: ["challenge1", "challenge2"];
    estimated_effort: {
      optimistic_hours: number;
      realistic_hours: number;
      pessimistic_hours: number;
    };
    risk_level: "low" | "medium" | "high";
    risk_factors: string[];
  };

  // 2. RESEARCH SECTION
  research: {
    framework_patterns: [{name, reference_files, description}];
    architectural_patterns: [{name, applies_here, reason}];
    related_code: [{path, type, reason}];
  };

  // 3. DESIGN CHOICES SECTION
  design_choices: [{
    decision: "what decision";
    options: [{name, pros, cons}];
    recommended: "chosen option";
    rationale: "why chosen";
    team_convention_alignment: "how it aligns";
  }];

  // 4. PHASES SECTION
  phases: [{
    phase_number: number;
    name: string;
    description: string;
    tasks: string[];  // task IDs
    estimated_duration_hours: number;
    success_criteria: string[];
    dependencies: number[];
  }];

  // 5. TASKS SECTION
  tasks: [{
    task_id: string;
    title: string;
    description: string;
    files_affected: string[];
    estimated_effort_hours: number;
    dependencies: string[];
    success_criteria: string[];
    verification_approach: string;
  }];

  // 6. VERIFICATION SECTION
  verification: {
    testing_strategy: string;
    integration_points: [{after_task, validation}];
    final_validation: string[];
    rollback_procedure: string;
  };

  // ANALYSIS
  breaking_changes: [{type, description, impact, migration_path}];
  critical_path: {tasks: string[], total_duration_hours: number};
  assumptions: string[];
  unknowns: string[];
}
```

---

## Planning Algorithm

### Step 1: Synthesize Context

Combine all inputs into coherent understanding:

**Key Integration Points:**
- Issue type drives task categorization (feature→new files, bug→fix existing, refactor→reorganize)
- Framework patterns inform how tasks are structured
- File dependencies indicate task dependencies
- Team conventions enforce task ordering

**Algorithm:**
```
Input: All context from prior phases
1. Identify primary concern (what needs to change most)
2. Find affected file tiers (Tier 1 = direct impact)
3. Trace dependencies from Tier 1 through graph
4. Identify relevant patterns from pattern_found[]
5. Check team conventions for applicable standards
Output: coherent_context
```

### Step 2: Detect Breaking Changes

Identify potential impacts to other code:

**Breaking Change Categories:**

```
API Changes:
  - Function signature changes (parameter additions/removals)
  - Export changes (new/removed exports)
  - Return type changes
  - Async/sync conversion

Data Changes:
  - Data structure modifications
  - Field additions/removals
  - Type changes
  - Migration requirements

Behavior Changes:
  - Algorithm changes
  - Side effect changes
  - Performance/resource changes

Dependency Changes:
  - New library dependencies
  - Version upgrades
  - Transitive dependency changes
```

**Detection Algorithm:**
```
For each requirement:
  1. Identify affected files (from dependency_graph)
  2. Check what imports each file (dependents)
  3. Analyze if change affects those dependents
  4. Categorize as: none | low | medium | high impact
Output: breaking_changes[]
```

### Step 3: Decompose Requirements into Tasks

Convert requirements into atomic, assignable work:

**Task Granularity:** 1-4 hour tasks (preferred)
- Too small: overhead of task switching
- Too large: harder to verify incrementally
- Atomic: independent enough to complete without other tasks

**Decomposition Algorithm:**
```
For each requirement:
  1. Identify primary file(s) affected
  2. Create task for each distinct file group
  3. If file has >5 modifications needed, split into subtasks
  4. Group related tasks into logical phases
  5. Identify task-to-task dependencies

Example - Dark mode feature:
  Req: "Detect system preference"
    → Task 1: Add useSystemPreference hook
    → Task 2: Read prefers-color-scheme media query

  Req: "Store preference in localStorage"
    → Task 3: Create localStorage key abstraction
    → Task 4: Update useSystemPreference to read/write

  Req: "Apply theme to all pages"
    → Task 5: Create theme provider wrapper
    → Task 6: Apply to App root component
```

### Step 4: Analyze Task Dependencies

Determine execution order using dependency graph:

```
Algorithm:
1. For each task's affected files, find dependencies
2. If Task A modifies file X, and Task B imports file X:
   → Task A must precede Task B
3. Group independent tasks (can run in parallel)
4. Create task dependency chain

Critical Path:
  - Sequence of dependent tasks on longest path
  - Identifies minimum project duration
  - Helps prioritize risky items early
```

### Step 5: Estimate Effort

Provide realistic time estimates per task:

**Estimation Factors:**
```
Base Effort = 1 hour per 50 lines of code change

Modifiers:
  - Framework familiarity: 1.0x (familiar), 1.5x (unfamiliar)
  - File complexity: 1.0x (simple), 2.0x (very complex)
  - Testing overhead: +20% (tests required)
  - Integration overhead: +10% (integration points)
  - Confidence adjustment: -20% to +50% based on uncertainties

Formula:
  estimated_effort = (base_effort × framework_modifier × complexity) × (1 + test_overhead)

Three-point estimate:
  optimistic = estimated_effort × 0.7
  realistic = estimated_effort
  pessimistic = estimated_effort × 1.5
```

### Step 6: Organize into Phases

Group tasks into logical implementation phases:

**Phase Structure Principles:**
1. **Early phase:** Setup, infrastructure, no dependencies
2. **Middle phases:** Core implementation, each builds on previous
3. **Late phase:** Integration, verification, cleanup

**Example 3-phase structure:**
```
Phase 1: Setup (2-4 hours)
  - Create theme system infrastructure
  - Add necessary dependencies
  - Create type definitions

Phase 2: Core Implementation (6-8 hours)
  - Implement theme switching logic
  - Apply theme to components
  - Add user preference persistence

Phase 3: Testing & Integration (3-4 hours)
  - Unit test theme system
  - Integration test with other features
  - Manual testing and verification
```

### Step 7: Generate Plan Sections

Create each of the 6 sections:

**1. Summary Section:**
- Executive overview in 2-3 sentences
- Key technical challenges
- Estimated effort (realistic hours)
- Risk assessment

**2. Research Section:**
- Framework-specific patterns to review
- Architectural patterns that apply
- Related code examples to study
- Framework version compatibility notes

**3. Design Choices Section:**
- Each decision needed before coding
- Pros/cons of different options
- Recommended approach with rationale
- Team convention alignment

**4. Phases Section:**
- Clear phase boundaries
- Tasks in each phase
- Success criteria per phase
- Dependencies between phases

**5. Tasks Section:**
- Atomic work items
- Ordered by dependencies
- Files modified per task
- Success criteria per task

**6. Verification Section:**
- Testing approach per task
- Integration verification points
- Final validation criteria
- How to roll back if needed

---

## Framework-Specific Planning

### JavaScript/React

**Task Structure Pattern:**
```
1. Type definitions (if TypeScript)
2. Component structure (component files)
3. Hook logic (state, effects)
4. Integration (parent component updates)
5. Styling (CSS/styled-components)
6. Tests (unit + integration)
```

**Common Patterns:**
- State management decisions (props, context, Redux)
- Hook dependency arrays are critical
- Testing requires act() wrapping
- CSS-in-JS vs external stylesheets

### Python/Django

**Task Structure Pattern:**
```
1. Model changes (if needed)
2. Serializer/validation (if needed)
3. View implementation
4. URL routing
5. Tests (model, view, integration)
6. Documentation (docstrings)
```

**Common Patterns:**
- Model migrations required
- View tests need client factory
- Serializer validation central
- URL configuration must be precise

### Go

**Task Structure Pattern:**
```
1. Interface definitions
2. Struct implementation
3. Handler functions
4. Integration with router
5. Tests (unit + integration)
```

**Common Patterns:**
- Error handling on every function
- Interfaces enable testing
- Struct composition over inheritance
- Tests use table-driven patterns

---

## Team Convention Integration

### Reading Conventions

Check `.claude/team-guidelines.md` for:
- Task ordering preferences
- Code structure conventions
- Testing requirements
- File organization standards
- Documentation standards

### Enforcing Conventions

Ensure plan:
- ✅ Follows code structure conventions
- ✅ Includes testing at required levels
- ✅ Adheres to task sizing guidelines
- ✅ Respects file organization
- ✅ Includes documentation tasks if required

**Example Convention Check:**
```
If team_conventions includes "No breaking changes without deprecation":
  → Flag any breaking changes
  → Add deprecation task
  → Include migration window in plan
```

---

## Token Budget Management

### Budget Constraint

Implementation plan must respect downstream token budget:

```
Total Available: 30K/60K/90K (depending on depth mode)
Already Used by Phases 1-3: ~15K-40K
Remaining for Phase 5 (Surgical Prompt Generator): 10K-30K
```

### Task Planning for Token Efficiency

When creating tasks, note:
- Files modified per task (limits prompt size)
- Context required per task (reduces prompt scope)
- File separation points (natural boundaries)

**Token-aware task breakdown:**
```
Instead of:
  Task: "Implement dark mode" (requires 25 files, 40K tokens)

Use:
  Task 1: "Add theme provider" (3 files, 5K tokens)
  Task 2: "Update page components" (8 files, 8K tokens)
  Task 3: "Add persistence" (2 files, 3K tokens)
```

---

## Output Formatting

### Markdown Format (For Humans)

Plan saved to `.claude/planning/sessions/{session_id}/PLAN.md`:

```markdown
# Implementation Plan: [Title]

## Summary

[2-3 sentence overview]
[Key challenges]
[Effort estimate and risk]

## Research

### Framework Patterns
[Framework-specific patterns to understand]

### Related Code Examples
[Files to study before coding]

## Design Choices

### Choice 1: [Decision Name]
[Pros/Cons/Rationale]

## Phases

### Phase 1: [Name]
[Description]
**Tasks:** [list]
**Duration:** X hours

## Tasks

### Task 1: [Name]
**Files:** [list]
**Effort:** X hours
**Success Criteria:** [list]

## Verification

[Testing strategy]
[Integration points]
[Final validation]
```

### JSON Format (For Tools)

Plan saved to `.claude/planning/sessions/{session_id}/plan.json`:

```json
{
  "plan_id": "plan-uuid",
  "title": "...",
  "summary": {...},
  "research": {...},
  "design_choices": [...],
  "phases": [...],
  "tasks": [...],
  "verification": {...}
}
```

---

## Error Handling

### Error Categories

**CRITICAL (Plan Invalid):**
```
- No tasks can be derived from requirements
- Circular task dependencies detected
- Breaking changes cannot be mitigated
Recovery: Return error, explain issue
```

**HIGH (Warnings):**
```
- Very high effort estimate (>80 hours)
- Significant breaking changes identified
- Requirements conflict with conventions
Recovery: Create plan with clear warnings
```

**MEDIUM (Clarifications):**
```
- Ambiguous requirements
- Missing framework-specific guidance
- Unclear task granularity
Recovery: Document assumptions, continue
```

**LOW (Informational):**
```
- Some patterns not found
- Minor convention mismatches
- Confidence scores below thresholds
Recovery: Continue with defaults
```

---

## Examples

### Example 1: Feature Request (Dark Mode)

**Input:**
```
Issue Type: feature
Requirements: [
  "Detect system preference using prefers-color-scheme",
  "Allow manual toggle in settings",
  "Store preference in localStorage",
  "Apply theme to all pages"
]
Framework: React 18
Scope: medium
```

**Output Summary:**
```
Summary:
  Dark mode feature using system preference + manual override.
  Challenges: CSS variable system, global theme application.
  Estimate: 16 hours (realistic)
  Risk: Low (well-established pattern)

Phases:
  Phase 1: Theme infrastructure (4 hours)
  Phase 2: UI implementation (8 hours)
  Phase 3: Testing & verification (4 hours)

Tasks:
  T1: Create theme context (3h)
  T2: Implement useTheme hook (2h)
  T3: Create theme provider (2h)
  T4: Update global CSS (2h)
  T5: Add settings UI (4h)
  T6: Persistence logic (2h)
  T7: Test theme switching (1h)

Critical Path: T1 → T2 → T3 → T4 → T5 (13 hours minimum)
```

### Example 2: Bug Fix (Authentication)

**Input:**
```
Issue Type: bug
Requirements: [
  "Login fails with special characters in password",
  "Fix validation regex",
  "Ensure UTF-8 support"
]
Framework: Express.js
Scope: small
```

**Output Summary:**
```
Summary:
  Password validation regex blocking valid UTF-8 characters.
  Fix: Update regex to allow Unicode, add tests.
  Estimate: 4 hours (realistic)
  Risk: Medium (affects authentication, needs thorough testing)

Breaking Changes:
  None - fixing bug, not changing API

Tasks:
  T1: Identify current regex (0.5h)
  T2: Fix regex for Unicode (1h)
  T3: Add test cases (1.5h)
  T4: Verify existing users unaffected (1h)

Critical Path: T1 → T2 → T3 (2.5 hours minimum)
```

### Example 3: Refactoring (Extract Service)

**Input:**
```
Issue Type: refactor
Requirements: [
  "Extract authentication into separate service",
  "Maintain backward compatibility",
  "Add type definitions"
]
Framework: Django
Scope: medium
```

**Output Summary:**
```
Summary:
  Extract auth service for reusability.
  Challenges: Maintain compatibility, test coverage.
  Estimate: 24 hours (realistic)
  Risk: Medium (many dependencies, careful refactoring needed)

Phases:
  Phase 1: Service structure (4h)
  Phase 2: Migrate logic (10h)
  Phase 3: Testing & compatibility (8h)
  Phase 4: Documentation (2h)

Design Choices:
  - Keep old imports working via wrapper (maintain compatibility)
  - Add type hints for better IDE support
  - Create comprehensive tests before migration

Critical Path: Full sequence (24 hours, cannot parallelize much)
```

---

## Integration with Phase 5

The Implementation Planner output directly feeds Phase 5 (Surgical Prompt Generator):

```
Phase 5 receives:
  - tasks[] array (precise scope per prompt)
  - affected_files per task (which files to modify)
  - success_criteria per task (how to verify)
  - team_conventions (which to enforce)
  - context from phases 1-3 (for reference)

Phase 5 uses this to:
  ├─ Create one prompt per task
  ├─ Include only relevant context per task
  ├─ Enforce success criteria in prompt
  └─ Guide implementation file by file
```

---

## Performance Targets

```
Single Plan Generation:
  - Small scope (1-5 tasks): <2 minutes
  - Medium scope (6-15 tasks): <5 minutes
  - Large scope (15+ tasks): <10 minutes

Accuracy:
  - Task decomposition: 90%+ coverage of requirements
  - Effort estimation: ±25% accuracy (optimistic/realistic/pessimistic)
  - Breaking change detection: 85%+ coverage
  - Critical path calculation: 95%+ accuracy

Quality:
  - All requirements addressed: 100%
  - All tasks have success criteria: 100%
  - All files identified: 95%+
  - Assumptions documented: 100%
```

---

## Testing

This skill is tested with:
- **5 Feature requests** (varying complexity)
- **5 Bug reports** (different issue types)
- **3 Refactoring tasks** (large scope changes)
- **2 Performance optimizations** (focused changes)
- **3 Edge cases** (ambiguous requirements, impossible timelines)
- **4 Error scenarios** (conflicting requirements, breaking changes)

See TDD_TEST_SPECIFICATION.md for complete test cases and expected outputs.

---

## Common Mistakes

### ❌ Over-Planning

Creating 50 tiny tasks when 10 logical tasks suffice.

→ **Instead:** Aim for 1-4 hour tasks. Group related work.

### ❌ Missing Task Dependencies

Ordering tasks linearly when they could run in parallel.

→ **Instead:** Analyze file dependencies carefully. Enable parallelization.

### ❌ Ignoring Framework Patterns

Generic plans that don't respect framework conventions.

→ **Instead:** Use framework-specific task structure patterns.

### ❌ Underestimating Effort

Treating refactoring as simple work, missing testing overhead.

→ **Instead:** Use 3-point estimates. Account for testing (20%) and integration (10%).

### ❌ Missing Breaking Changes

Creating plan that breaks other code without migration strategy.

→ **Instead:** Analyze dependents carefully. Flag breaking changes explicitly.

### ❌ Ignoring Token Budgets

Creating tasks that exceed Phase 5 token limits.

→ **Instead:** Plan file modifications per task. Estimate Phase 5 token usage.

---

## Data Contract

```typescript
interface ImplementationPlan {
  // Metadata
  plan_id: string;
  title: string;
  created_at: string;
  issue_type: "feature" | "bug" | "refactor" | "performance" | "docs";
  scope: "small" | "medium" | "large";

  // 6 Sections
  summary: {
    overview: string;
    key_challenges: string[];
    estimated_effort: {
      optimistic_hours: number;
      realistic_hours: number;
      pessimistic_hours: number;
    };
    risk_level: "low" | "medium" | "high";
    risk_factors: string[];
  };

  research: {
    framework_patterns: Array<{
      name: string;
      description: string;
      reference_files: string[];
      framework: string;
    }>;
    architectural_patterns: Array<{
      name: string;
      applies_here: boolean;
      examples: string[];
    }>;
    related_code: Array<{
      path: string;
      type: "example" | "similar" | "baseline";
      reason: string;
    }>;
  };

  design_choices: Array<{
    decision: string;
    problem: string;
    options: Array<{
      name: string;
      pros: string[];
      cons: string[];
      effort_impact: string;
    }>;
    recommended: string;
    rationale: string;
    team_convention_alignment: string;
  }>;

  phases: Array<{
    phase_id: string;
    number: number;
    name: string;
    description: string;
    task_ids: string[];
    estimated_hours: number;
    success_criteria: string[];
    dependencies: number[];
  }>;

  tasks: Array<{
    task_id: string;
    title: string;
    description: string;
    phase_id: string;
    files_affected: string[];
    estimated_hours: number;
    complexity: "simple" | "moderate" | "complex";
    dependencies: string[];
    success_criteria: string[];
    verification_approach: string;
    team_convention_checks: string[];
  }>;

  verification: {
    testing_strategy: string;
    integration_points: Array<{
      after_phase: number;
      validation_steps: string[];
    }>;
    final_validation: string[];
    rollback_procedure: string;
    verification_checklist: string[];
  };

  analysis: {
    breaking_changes: Array<{
      type: "api" | "data" | "behavior" | "dependency";
      description: string;
      impact_scope: string;
      affected_dependents: string[];
      migration_path: string;
    }>;
    critical_path: {
      task_ids: string[];
      total_hours: number;
      phase_sequence: number[];
    };
    parallelizable_tasks: Array<string[]>;
    assumptions: string[];
    unknowns: string[];
    constraints: string[];
  };
}
```

---

