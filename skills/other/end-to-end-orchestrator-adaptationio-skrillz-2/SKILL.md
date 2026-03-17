---
name: end-to-end-orchestrator
description: Complete development workflow orchestrator coordinating all multi-ai skills (research → planning → implementation → testing → verification) with quality gates, failure recovery, and state management. Single-command complete workflows from objective to production-ready code. Use when implementing complete features requiring full pipeline, coordinating multiple skills automatically, or executing production-grade development cycles end-to-end.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# End-to-End Orchestrator

## Overview

end-to-end-orchestrator provides single-command complete development workflows, coordinating all 5 multi-ai skills from research through production deployment.

**Purpose**: Transform "I want feature X" into production-ready code through automated skill coordination

**Pattern**: Workflow-based (5-stage pipeline with quality gates)

**Key Innovation**: Automatic orchestration of research → planning → implementation → testing → verification with failure recovery and quality gates

**The Complete Pipeline**:
```
Input: Feature description
  ↓
1. Research (multi-ai-research) [optional]
  ↓ [Quality Gate: Research complete]
2. Planning (multi-ai-planning)
  ↓ [Quality Gate: Plan ≥90/100]
3. Implementation (multi-ai-implementation)
  ↓ [Quality Gate: Tests pass, coverage ≥80%]
4. Testing (multi-ai-testing)
  ↓ [Quality Gate: Coverage ≥95%, verified]
5. Verification (multi-ai-verification)
  ↓ [Quality Gate: Score ≥90/100, all layers pass]
Output: Production-ready code
```

---

## When to Use

Use end-to-end-orchestrator when:

- Implementing complete features (not quick fixes)
- Want automated workflow (not manual skill chaining)
- Production-quality required (all gates must pass)
- Time optimization important (parallel where possible)
- Need failure recovery (automatic retry/rollback)

**When NOT to Use**:
- Quick fixes (<30 minutes)
- Exploratory work (uncertain requirements)
- Manual control preferred (step through each phase)

---

## Prerequisites

### Required
- All 5 multi-ai skills installed:
  - multi-ai-research
  - multi-ai-planning
  - multi-ai-implementation
  - multi-ai-testing
  - multi-ai-verification

### Optional
- agent-memory-system (for learning from past work)
- hooks-manager (for automation)
- Gemini CLI, Codex CLI (for tri-AI research)

---

## Complete Workflow

### Stage 1: Research (Optional)

**Purpose**: Ground implementation in proven patterns

**Process**:

1. **Determine if Research Needed**:
   ```typescript
   // Check if objective is familiar
   const similarWork = await recallMemory({
     type: 'episodic',
     query: objective
   });

   if (similarWork.length === 0) {
     // Unfamiliar domain → research needed
     needsResearch = true;
   } else {
     // Familiar → can skip research, use past learnings
     needsResearch = false;
   }
   ```

2. **Execute Research** (if needed):
   ```
   Use multi-ai-research for "[domain] implementation patterns and best practices"
   ```

   **What It Provides**:
   - Claude research: Official docs, codebase patterns
   - Gemini research: Web best practices, latest trends
   - Codex research: GitHub patterns, code examples
   - Quality: ≥95/100 with 100% citations

3. **Quality Gate: Research Complete**:
   ```markdown
   ✅ Research findings documented
   ✅ Patterns identified (minimum 2)
   ✅ Best practices extracted (minimum 3)
   ✅ Quality score ≥95/100
   ```

   **If Fail**: Research incomplete → retry research OR proceed without (user decides)

**Outputs**:
- Research findings (.analysis/ANALYSIS_FINAL.md)
- Patterns and best practices
- Implementation recommendations

**Time**: 30-60 minutes (can skip if familiar domain)

**Next**: Proceed to Stage 2

---

### Stage 2: Planning

**Purpose**: Create agent-executable plan with quality ≥90/100

**Process**:

1. **Load Research Context** (if research done):
   ```typescript
   let context = "";

   if (researchDone) {
     context = await readFile('.analysis/ANALYSIS_FINAL.md');
   }
   ```

2. **Invoke Planning**:
   ```
   Use multi-ai-planning to create plan for [objective]

   ${context ? `Research findings available in: .analysis/ANALYSIS_FINAL.md` : ''}

   Create comprehensive plan following 6-step workflow.
   ```

   **What It Does**:
   - Analyzes objective
   - Hierarchical decomposition (8-15 tasks)
   - Maps dependencies, identifies parallel
   - Plans verification for all tasks
   - Scores quality (0-100)

3. **Quality Gate: Plan Approved**:
   ```markdown
   ✅ Plan created
   ✅ Quality score ≥90/100
   ✅ All tasks have verification
   ✅ Dependencies mapped
   ✅ No circular dependencies
   ```

   **If Fail** (score <90):
   - Review gap analysis
   - Apply recommended fixes
   - Re-verify
   - Retry up to 2 times
   - If still <90: Escalate to human review

4. **Save Plan to Shared State**:
   ```bash
   # Save for next stage
   cp plans/[plan-id]/plan.json .multi-ai-context/plan.json
   ```

**Outputs**:
- plan.json (machine-readable)
- PLAN.md (human-readable)
- COORDINATION.md (execution guide)
- Quality ≥90/100

**Time**: 1.5-3 hours

**Next**: Proceed to Stage 3

---

### Stage 3: Implementation

**Purpose**: Execute plan with TDD, produce working code

**Process**:

1. **Load Plan**:
   ```typescript
   const plan = JSON.parse(readFile('.multi-ai-context/plan.json'));
   console.log(`📋 Loaded plan: ${plan.objective}`);
   console.log(`   Tasks: ${plan.tasks.length}`);
   console.log(`   Estimated: ${plan.metadata.estimated_total_hours} hours`);
   ```

2. **Invoke Implementation**:
   ```
   Use multi-ai-implementation following plan in .multi-ai-context/plan.json

   Execute all 6 steps:
   1. Explore & gather context
   2. Plan architecture (plan already created, refine as needed)
   3. Implement incrementally with TDD
   4. Coordinate multi-agent (if parallel tasks)
   5. Integration & E2E testing
   6. Quality verification before commit

   Success criteria from plan.
   ```

   **What It Does**:
   - Explores codebase (progressive disclosure)
   - Implements incrementally (<200 lines per commit)
   - Test-driven development (tests first)
   - Multi-agent coordination for parallel tasks
   - Continuous testing during implementation
   - Doom loop prevention (max 3 retries)

3. **Quality Gate: Implementation Complete**:
   ```markdown
   ✅ All plan tasks implemented
   ✅ All tests passing
   ✅ Coverage ≥80% (gate), ideally ≥95%
   ✅ No regressions
   ✅ Doom loop avoided (< max retries)
   ```

   **If Fail**:
   - Identify failing task
   - Retry with different approach
   - If 3 failures: Escalate to human
   - Save state for recovery

4. **Save Implementation State**:
   ```bash
   # Save for next stage
   echo '{
     "status": "implemented",
     "files_changed": [...],
     "tests_run": 95,
     "tests_passed": 95,
     "coverage": 87,
     "commits": ["abc123", "def456"]
   }' > .multi-ai-context/implementation-status.json
   ```

**Outputs**:
- Working code
- Tests passing
- Coverage ≥80%
- Commits created

**Time**: 3-10 hours (varies by complexity)

**Next**: Proceed to Stage 4

---

### Stage 4: Testing (Independent Verification)

**Purpose**: Verify tests are comprehensive and prevent gaming

**Process**:

1. **Load Implementation Context**:
   ```typescript
   const implStatus = JSON.parse(
     readFile('.multi-ai-context/implementation-status.json')
   );

   console.log(`🧪 Testing implementation:`);
   console.log(`   Files changed: ${implStatus.files_changed.length}`);
   console.log(`   Current coverage: ${implStatus.coverage}%`);
   ```

2. **Invoke Independent Testing**:
   ```
   Use multi-ai-testing independent verification workflow

   Verify:
   - Tests in: tests/
   - Code in: src/
   - Specifications in: .multi-ai-context/plan.json

   Workflows to execute:
   1. Test quality verification (independent agent)
   2. Coverage validation (≥95% target)
   3. Edge case discovery (AI-powered)
   4. Multi-agent ensemble scoring (if critical feature)

   Score test quality (0-100).
   ```

   **What It Does**:
   - Independent verification (separate agent from impl)
   - Checks tests match specifications (not just what code does)
   - Generates additional edge case tests
   - Multi-agent ensemble for quality scoring
   - Prevents overfitting

3. **Quality Gate: Testing Verified**:
   ```markdown
   ✅ Test quality score ≥90/100
   ✅ Coverage ≥95% (target achieved)
   ✅ Independent verification passed
   ✅ No test gaming detected
   ✅ Edge cases covered
   ```

   **If Fail**:
   - Review test quality issues
   - Generate additional tests
   - Re-verify
   - Max 2 retries, then escalate

4. **Save Testing State**:
   ```bash
   echo '{
     "status": "tested",
     "test_quality_score": 92,
     "coverage": 96,
     "tests_total": 112,
     "edge_cases": 23,
     "gaming_detected": false
   }' > .multi-ai-context/testing-status.json
   ```

**Outputs**:
- Test quality ≥90/100
- Coverage ≥95%
- Independent verification passed

**Time**: 1-3 hours

**Next**: Proceed to Stage 5

---

### Stage 5: Verification (Multi-Layer QA)

**Purpose**: Final quality assurance before production

**Process**:

1. **Load All Context**:
   ```typescript
   const plan = JSON.parse(readFile('.multi-ai-context/plan.json'));
   const implStatus = JSON.parse(readFile('.multi-ai-context/implementation-status.json'));
   const testStatus = JSON.parse(readFile('.multi-ai-context/testing-status.json'));

   console.log(`🔍 Final verification:`);
   console.log(`   Objective: ${plan.objective}`);
   console.log(`   Implementation: ${implStatus.status}`);
   console.log(`   Testing: ${testStatus.coverage}% coverage`);
   ```

2. **Invoke Multi-Layer Verification**:
   ```
   Use multi-ai-verification for complete quality check

   Verify:
   - Code: src/
   - Tests: tests/
   - Plan: .multi-ai-context/plan.json

   Execute all 5 layers:
   1. Rules-based (linting, types, schema, SAST)
   2. Functional (tests, coverage, examples)
   3. Visual (if UI: screenshots, a11y)
   4. Integration (E2E, API compatibility)
   5. Quality scoring (LLM-as-judge, 0-100)

   All 5 quality gates must pass.
   ```

   **What It Does**:
   - Runs all 5 verification layers
   - Each layer is independent
   - LLM-as-judge for holistic assessment
   - Agent-as-a-Judge can execute tools to verify claims
   - Multi-agent ensemble for critical features

3. **Quality Gate: Production Ready**:
   ```markdown
   ✅ Layer 1 (Rules): PASS
   ✅ Layer 2 (Functional): PASS, coverage 96%
   ✅ Layer 3 (Visual): PASS or SKIPPED
   ✅ Layer 4 (Integration): PASS
   ✅ Layer 5 (Quality): 92/100 ≥90 ✅

   ALL GATES PASSED → PRODUCTION APPROVED
   ```

   **If Fail**:
   - Review gap analysis from failed layer
   - Apply recommended fixes
   - Re-verify from failed layer (not all 5)
   - Max 2 retries per layer
   - If still failing: Escalate to human

4. **Generate Final Report**:
   ```markdown
   # Feature Implementation Complete

   **Objective**: [from plan]

   ## Pipeline Execution Summary

   ### Stage 1: Research
   - Status: ✅ Complete
   - Quality: 97/100
   - Time: 52 minutes

   ### Stage 2: Planning
   - Status: ✅ Complete
   - Quality: 94/100
   - Tasks: 23
   - Time: 1.8 hours

   ### Stage 3: Implementation
   - Status: ✅ Complete
   - Files changed: 15
   - Lines added: 847
   - Commits: 12
   - Time: 6.2 hours

   ### Stage 4: Testing
   - Status: ✅ Complete
   - Test quality: 92/100
   - Coverage: 96%
   - Tests: 112
   - Time: 1.5 hours

   ### Stage 5: Verification
   - Status: ✅ Complete
   - Quality score: 92/100
   - All layers: PASS
   - Time: 1.2 hours

   ## Final Metrics

   - **Total Time**: 11.3 hours
   - **Quality**: 92/100
   - **Coverage**: 96%
   - **Status**: ✅ PRODUCTION READY

   ## Commits
   - abc123: feat: Add database schema
   - def456: feat: Implement OAuth integration
   - [... 10 more ...]

   ## Next Steps
   - Create PR for team review
   - Deploy to staging
   - Production release
   ```

5. **Save to Memory** (if agent-memory-system available):
   ```typescript
   await storeMemory({
     type: 'episodic',
     event: {
       description: `Complete implementation: ${objective}`,
       outcomes: {
         total_time: 11.3,
         quality_score: 92,
         test_coverage: 96,
         stages_completed: 5
       },
       learnings: extractedDuringPipeline
     }
   });
   ```

**Outputs**:
- Production-ready code
- Comprehensive final report
- Commits created
- PR ready (if requested)
- Memory saved for future learning

**Time**: 30-90 minutes

**Result**: ✅ PRODUCTION READY

---

## Failure Recovery

### Failure Handling at Each Stage

**Stage Fails** → **Recovery Strategy**:

**Research Fails**:
- Retry with different sources
- Skip research (use memory if available)
- Escalate to human if critical gap

**Planning Fails** (score <90):
- Review gap analysis
- Apply fixes automatically if possible
- Retry planning (max 2 attempts)
- Escalate if still <90

**Implementation Fails**:
- Identify failing task
- Automatic rollback to last checkpoint
- Retry with alternative approach
- Doom loop prevention (max 3 retries)
- Escalate with full error context

**Testing Fails** (coverage <80% or quality <90):
- Generate additional tests for gaps
- Retry verification
- Max 2 retries
- Escalate with coverage report

**Verification Fails** (score <90 or layer fails):
- Apply auto-fixes for Layer 1-2 issues
- Manual fixes needed for Layer 3-5
- Re-verify from failed layer (not all 5)
- Max 2 retries per layer
- Escalate with quality report

---

### Escalation Protocol

**When to Escalate to Human**:
1. Any stage fails 3 times (doom loop)
2. Planning quality <80 after 2 retries
3. Implementation doom loop detected
4. Verification score <80 after 2 retries
5. Budget exceeded (if cost tracking enabled)
6. Circular dependency detected
7. Irrecoverable error (file system, permissions)

**Escalation Format**:
```markdown
# ⚠️ ESCALATION REQUIRED

**Stage**: Implementation (Stage 3)
**Failure**: Doom loop detected (3 failed attempts)

## Context
- Objective: Implement user authentication
- Failing Task: 2.2.2 Token generation
- Error: Tests fail with "undefined userId" repeatedly

## Attempts Made
1. Attempt 1: Added userId to payload → Same error
2. Attempt 2: Changed payload structure → Same error
3. Attempt 3: Different JWT library → Same error

## Root Cause Analysis
- Tests expect `user.id` but implementation uses `user.userId`
- Mismatch in data model between test and implementation
- Auto-fix failed 3 times

## Recommended Actions
1. Review test specifications vs. implementation
2. Align data model (user.id vs. user.userId)
3. Manual intervention required

## State Saved
- Checkpoint: checkpoint-003 (before attempts)
- Rollback available: `git checkout checkpoint-003`
- Continue after fix: Resume from Task 2.2.2
```

---

## Parallel Execution Optimization

### Identifying Parallel Opportunities

**From Plan**:
```typescript
const plan = readFile('.multi-ai-context/plan.json');

// Plan identifies parallel groups
const parallelGroups = plan.parallel_groups;

// Example:
// Group 1: Tasks 2.1, 2.2, 2.3 (independent)
// Can execute in parallel
```

### Executing Parallel Tasks

**Pattern**:
```typescript
// Stage 3: Implementation with parallel tasks

const parallelGroup = plan.parallel_groups.find(g => g.group_id === 'pg2');

// Spawn parallel implementation agents
const results = await Promise.all(
  parallelGroup.tasks.map(taskId => {
    const task = plan.tasks.find(t => t.id === taskId);

    return task({
      description: `Implement ${task.description}`,
      prompt: `Implement task ${task.id}: ${task.description}

      Specifications from plan:
      ${JSON.stringify(task, null, 2)}

      Success criteria:
      ${task.verification.success_criteria.join('\n')}

      Write implementation and tests.
      Report completion status.`
    });
  })
);

// Verify all parallel tasks completed
const allSucceeded = results.every(r => r.status === 'complete');

if (allSucceeded) {
  // Proceed to integration
} else {
  // Handle failures
}
```

**Time Savings**: 20-40% faster than sequential execution

---

## State Management

### Cross-Skill State Sharing

**Shared Context Directory**: `.multi-ai-context/`

**Standard Files**:
```
.multi-ai-context/
├── research-findings.json     # From multi-ai-research
├── plan.json                  # From multi-ai-planning
├── implementation-status.json # From multi-ai-implementation
├── testing-status.json        # From multi-ai-testing
├── verification-report.json   # From multi-ai-verification
├── pipeline-state.json        # Orchestrator state
└── failure-history.json       # For doom loop detection
```

**Benefits**:
- Skills don't duplicate work
- Later stages read earlier outputs
- Failure recovery knows full state
- Memory can be saved from shared state

---

### Progress Tracking

**Real-Time Progress**:
```json
{
  "pipeline_id": "pipeline_20250126_1200",
  "objective": "Implement user authentication",
  "started_at": "2025-01-26T12:00:00Z",
  "current_stage": 3,
  "stages": [
    {
      "stage": 1,
      "name": "Research",
      "status": "complete",
      "duration_minutes": 52,
      "quality": 97
    },
    {
      "stage": 2,
      "name": "Planning",
      "status": "complete",
      "duration_minutes": 108,
      "quality": 94
    },
    {
      "stage": 3,
      "name": "Implementation",
      "status": "in_progress",
      "started_at": "2025-01-26T13:48:00Z",
      "tasks_total": 23,
      "tasks_complete": 15,
      "tasks_remaining": 8,
      "percent_complete": 65
    },
    {
      "stage": 4,
      "name": "Testing",
      "status": "pending"
    },
    {
      "stage": 5,
      "name": "Verification",
      "status": "pending"
    }
  ],
  "estimated_completion": "2025-01-26T20:00:00Z",
  "quality_target": 90,
  "current_quality_estimate": 92
}
```

**Query Progress**:
```bash
# Check current status
cat .multi-ai-context/pipeline-state.json | jq '.current_stage, .stages[2].percent_complete'

# Output: Stage 3, 65% complete
```

---

## Workflow Modes

### Standard Mode (Full Pipeline)

**All 5 Stages**:
```
Research → Planning → Implementation → Testing → Verification
```

**Time**: 8-20 hours
**Quality**: Maximum (all gates, ≥90)
**Use For**: Production features, complex implementations

---

### Fast Mode (Skip Research)

**4 Stages** (familiar domains):
```
Planning → Implementation → Testing → Verification
```

**Time**: 6-15 hours
**Quality**: High (all gates except research)
**Use For**: Familiar domains, time-sensitive features

---

### Quick Mode (Essential Gates Only)

**Implementation + Basic Verification**:
```
Planning → Implementation → Testing (basic) → Verification (Layers 1-2 only)
```

**Time**: 3-8 hours
**Quality**: Good (essential gates only)
**Use For**: Internal tools, prototypes

---

## Best Practices

### 1. Always Run Planning Stage
Even for "simple" features - planning quality ≥90 prevents issues

### 2. Use Memory to Skip Research
If similar work done before, recall patterns instead of researching

### 3. Monitor Progress
Check `.multi-ai-context/pipeline-state.json` to track progress

### 4. Trust the Quality Gates
If gate fails, there's a real issue - don't skip fixes

### 5. Save State Frequently
Each stage completion saves state (enables recovery)

### 6. Review Final Report
Complete understanding of what was built and quality achieved

---

## Integration Points

### With All 5 Multi-AI Skills

**Coordinates**:
1. multi-ai-research (Stage 1)
2. multi-ai-planning (Stage 2)
3. multi-ai-implementation (Stage 3)
4. multi-ai-testing (Stage 4)
5. multi-ai-verification (Stage 5)

**Provides**:
- Automatic skill invocation
- Quality gate enforcement
- Failure recovery
- State management
- Progress tracking
- Final reporting

---

### With agent-memory-system

**Before Pipeline**:
- Recall similar past work
- Load learned patterns
- Skip research if memory sufficient

**After Pipeline**:
- Save complete episode to memory
- Extract learnings
- Update procedural patterns
- Improve estimation accuracy

---

### With hooks-manager

**Session Hooks**:
- SessionStart: Load pipeline state
- SessionEnd: Save pipeline progress
- PostToolUse: Track stage completions

**Notification Hooks**:
- Send telemetry on stage completions
- Alert on gate failures
- Track quality scores

---

## Quick Reference

### The 5-Stage Pipeline

| Stage | Skill | Time | Quality Gate | Output |
|-------|-------|------|--------------|--------|
| 1 | multi-ai-research | 30-60m | ≥95/100 | Research findings |
| 2 | multi-ai-planning | 1.5-3h | ≥90/100 | Executable plan |
| 3 | multi-ai-implementation | 3-10h | Tests pass, ≥80% cov | Working code |
| 4 | multi-ai-testing | 1-3h | ≥95% cov, quality ≥90 | Verified tests |
| 5 | multi-ai-verification | 1-3h | ≥90/100, all layers | Production ready |

**Total**: 8-20 hours → Production-ready feature

### Workflow Modes

| Mode | Stages | Time | Quality | Use For |
|------|--------|------|---------|---------|
| **Standard** | All 5 | 8-20h | Maximum | Production features |
| **Fast** | 2-5 (skip research) | 6-15h | High | Familiar domains |
| **Quick** | 2,3,4,5 (basic) | 3-8h | Good | Internal tools |

### Quality Gates

- **Research**: ≥95/100, patterns identified
- **Planning**: ≥90/100, all tasks verifiable
- **Implementation**: Tests pass, coverage ≥80%
- **Testing**: Quality ≥90/100, coverage ≥95%
- **Verification**: ≥90/100, all 5 layers pass

---

**end-to-end-orchestrator provides complete automation from feature description to production-ready code, coordinating all 5 multi-ai skills with quality gates, failure recovery, and state management - delivering enterprise-grade development workflows in a single command.**

For examples, see examples/. For failure recovery, see Failure Recovery section.
