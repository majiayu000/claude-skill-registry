---
name: skill-orchestrator
version: 1.0.0
author: claude-command-control
created: 2025-11-22
status: active
complexity: complex
---

# Skill Orchestrator

## Description
Coordinates execution of multiple specialized skills in complex workflows, managing dependencies, parallel execution, and result synthesis.

## When to Use This Skill
- When workflow requires 3+ different specialized skills
- When skills have dependencies on each other's outputs
- When parallel skill execution would improve performance
- When complex multi-phase workflow needs coordination

## When NOT to Use This Skill
- For simple single-skill workflows
- For agent-only workflows (use MULTI_AGENT_PLAN.md)
- For simple sequential skill calls (just call them directly)

## Prerequisites
- All required skills available and tested
- Understanding of skill dependencies
- Clear workflow requirements
- Performance targets defined

## Workflow

### Phase 1: Workflow Analysis

#### Step 1.1: Decompose Requirements

Create workflow specification:

```


## Workflow Spec: [Workflow Name]

**Goal**: [High-level objective]

**Skills Involved:**

1. 
2. 
3. 
4. 

**Dependency Graph:**

```
skill-1 (start)
    ↓
skill-2 (depends on skill-1)
    ├→ skill-3 (parallel A, depends on skill-2)
    └→ skill-4 (parallel B, depends on skill-2)
        ↓
skill-5 (depends on skill-3 AND skill-4)
    ↓
skill-6 (finalization)
```

**Success Criteria:**

- [Criterion 1]
- [Criterion 2]

```

#### Step 1.2: Identify Parallelization Opportunities

Analyze dependency graph for:
- Independent skills that can run parallel
- Blocking dependencies
- Resource constraints

**Parallelization Plan:**
```

**Parallel Groups:**

- Group 1: [skill-3, skill-4] (both depend only on skill-2)
- Group 2: [skill-7, skill-8] (independent of each other)

**Sequential Constraints:**

- skill-5 MUST wait for Group 1 completion
- skill-6 MUST wait for skill-5

```

### Phase 2: Execution Planning

#### Step 2.1: Create Execution Plan

```


## Execution Plan

### Phase 1: Initialization

**Skills**: [skill-1](%5BPurpose%5D)
**Estimated Duration**: [X min]
**Output**: [Description]

### Phase 2: Parallel Processing

**Skills**: [skill-3, skill-4] (parallel)
**Dependencies**: Phase 1 complete
**Estimated Duration**: max([skill-3 duration], [skill-4 duration])
**Outputs**:

- skill-3: [output]
- skill-4: [output]


### Phase 3: Synthesis

**Skills**: [skill-5]
**Dependencies**: Phase 2 complete
**Inputs**: Outputs from skill-3 AND skill-4
**Estimated Duration**: [Y min]
**Output**: [Description]

### Phase 4: Finalization

**Skills**: [skill-6]
**Dependencies**: Phase 3 complete
**Estimated Duration**: [Z min]
**Output**: [Final deliverable]

**Total Estimated Duration**: [X + max(skill-3,skill-4) + Y + Z] min

```

#### Step 2.2: Resource Allocation

```


## Resource Budget

**Token Budget**: [Total tokens]

- skill-1: [tokens]
- skill-2: [tokens]
- ...
- Orchestration overhead: [tokens]

**Time Budget**: [Total time]

- Sequential time: [sum of sequential]
- Parallelization savings: [time saved]
- Net time: [actual estimated time]

**External Resources:**

- MCP Server calls: [count]
- Agent invocations: [count]

```

### Phase 3: Orchestrated Execution

#### Step 3.1: Execute Sequential Skills

For each sequential skill:

```


### Execute: [skill-name]

1. **Prepare Input:**

```json
{
  "parameter1": "value from previous skill or requirement",
  "parameter2": "value",
  "context": {
    // Context from previous steps
  }
}
```

2. **Invoke Skill:**
"Use [skill-name] skill with the input above"
3. **Capture Output:**

```json
{
  "execution_id": "[skill-exec-id]",
  "status": "success | failure",
  "output": {
    // Skill output
  },
  "metadata": {
    "duration": "[X min]",
    "tokens_used": "[Y]"
  }
}
```

4. **Validate Output:**
    - [ ] Status = success
    - [ ] Output format matches expected
    - [ ] Quality criteria met
5. **Store for Next Phase:**
Save output to orchestration context:

```json
{
  "workflow_context": {
    "[skill-name]_output": {
      // Output data
    }
  }
}
```

```

#### Step 3.2: Execute Parallel Skills

For parallel skill groups:

```


### Execute Parallel Group: [group-name]

**Skills in Group:** [skill-A, skill-B, skill-C]

**Launch All:**

1. Prepare inputs for each skill
2. Invoke all skills concurrently:
    - "Use skill-A with input-A"
    - "Use skill-B with input-B"
    - "Use skill-C with input-C"

**Track Completion:**

```json
{
  "parallel_group_status": {
    "skill-A": "running",
    "skill-B": "running",
    "skill-C": "running"
  }
}
```

**Wait for All Completions:**
Monitor each skill until all complete

**Collect Results:**

```json
{
  "parallel_group_results": {
    "skill-A": {
      "status": "success",
      "output": {},
      "duration": "X min"
    },
    "skill-B": {
      "status": "success",
      "output": {},
      "duration": "Y min"
    },
    "skill-C": {
      "status": "success",
      "output": {},
      "duration": "Z min"
    }
  },
  "group_duration": "max(X,Y,Z) min"
}
```

**Validate All Outputs:**

- [ ] All skills completed successfully
- [ ] All outputs valid
- [ ] Ready for next phase

```

#### Step 3.3: Handle Errors and Recovery

```


### Error Handling

**IF any skill fails:**

1. **Assess Impact:**
    - Critical skill? (blocks entire workflow)
    - Optional skill? (can proceed without)
2. **Attempt Recovery:**

```
IF retryable error:
    Retry skill (max 2 retries)
    IF retry succeeds:
        Continue workflow
    ELSE:
        Proceed to Step 3
```

3. **Decide Path Forward:**

```
IF critical skill failed:
    - Use fallback approach if available
    - Request human intervention
    - Abort workflow with detailed error report

IF optional skill failed:
    - Log warning
    - Continue with partial results
    - Note limitation in final output
```

4. **Document Failure:**

```json
{
  "workflow_errors": [
    {
      "skill": "skill-name",
      "phase": "phase-N",
      "error": "error message",
      "recovery_attempted": true,
      "recovery_successful": false,
      "impact": "critical | degraded | minimal"
    }
  ]
}
```

```

### Phase 4: Result Synthesis

#### Step 4.1: Aggregate Outputs

```


### Synthesize Results

Collect all skill outputs:

```json
{
  "workflow_results": {
    "skill-1": { "output": {} },
    "skill-2": { "output": {} },
    "skill-3": { "output": {} },
    "skill-4": { "output": {} },
    "skill-5": { "output": {} }
  }
}
```

Synthesize into final deliverable:

1. Extract key components from each skill
2. Combine according to workflow spec
3. Resolve any conflicts or overlaps
4. Format per requirements
```

#### Step 4.2: Quality Validation

```


### Validate Final Output

Run validation checks:

**Completeness:**

- [ ] All required components present
- [ ] No missing data from any skill

**Consistency:**

- [ ] Outputs from different skills align
- [ ] No contradictions
- [ ] Unified format

**Quality:**

- [ ] Meets acceptance criteria
- [ ] Performance within targets
- [ ] No errors or warnings

**IF validation fails:**

- Identify which skill output is problematic
- Re-run that skill with adjustments
- Re-synthesize
- Re-validate

```

### Phase 5: Reporting and Handoff

```


## Orchestration Summary Report

**Workflow**: [Workflow Name]
**Execution ID**: [unique-id]
**Timestamp**: [ISO 8601]
**Total Duration**: [X min]
**Total Tokens**: [Y tokens]

**Execution Trace:**


| Phase | Skills | Status | Duration | Tokens |
| :-- | :-- | :-- | :-- | :-- |
| 1 | skill-1 | ✅ Success | X min | Y tokens |
| 2 | skill-3, skill-4 | ✅ Success | Z min | W tokens |
| 3 | skill-5 | ✅ Success | A min | B tokens |
| 4 | skill-6 | ✅ Success | C min | D tokens |

**Parallelization Savings**: [Time saved by parallel execution]

**Quality Metrics:**

- Success Rate: [100%]
- Average Quality Score: [95%]
- Performance: [Within targets]

**Outputs:**

- Primary Deliverable: [Location/description]
- Supporting Artifacts: [List]

**Issues Encountered:**

- [Issue 1](%5BResolution%5D): [How resolved]
- [Issue 2](%5BResolution%5D): [How resolved]

**Recommendations:**

- [Recommendation for future runs]
- [Optimization opportunity]

```

## Examples

### Example 1: Multi-Skill Content Generation Workflow

**Workflow**: Generate technical blog post with code examples, diagrams, and SEO optimization

**Skills Involved:**
1. `research-skill`: Gather technical information
2. `code-example-generator`: Create code snippets
3. `diagram-generator`: Create architecture diagrams
4. `content-writer`: Write blog post content
5. `seo-optimizer`: Optimize for search engines
6. `proofreader`: Final quality check

**Execution:**

```


## Phase 1: Research (Sequential)

Execute: research-skill
Input: "Gather information on microservices architecture patterns"
Output: research-notes.md (3500 words of research)

## Phase 2: Parallel Content Creation

Execute in parallel:

- code-example-generator (uses research output)
Output: code-examples/ (5 code snippets)
- diagram-generator (uses research output)
Output: diagrams/ (3 architecture diagrams)

Wait for both to complete
Duration: max(code gen: 8min, diagrams: 12min) = 12min

## Phase 3: Content Writing (Sequential)

Execute: content-writer
Inputs:

- research-notes.md
- code-examples/
- diagrams/
Output: blog-draft.md (2000 word article)


## Phase 4: Parallel Optimization (Parallel)

Execute in parallel:

- seo-optimizer (optimize blog-draft.md)
Output: blog-seo-optimized.md
- proofreader (review blog-draft.md)
Output: proofreading-notes.md

Wait for both
Duration: max(SEO: 5min, proof: 7min) = 7min

## Phase 5: Finalization (Sequential)

Synthesize:

- Merge SEO optimizations
- Apply proofreading corrections
- Generate metadata

Final Output: published-blog-post.md

- 2000 words
- 5 code examples
- 3 diagrams
- SEO optimized
- Proofread

Total Duration:

- Sequential: research(10) + writing(15) + synthesis(3) = 28min
- Parallel savings: Would be 40min without parallelization
- Actual: 28 + max(12,7) = 40min vs 55min = 15min saved

```

### Example 2: Code Review Orchestration

**Workflow**: Comprehensive PR review using multiple specialized skills

**Skills:**
1. `pr-analyzer`: Extract PR metadata
2. `security-scanner`: Security vulnerability scan
3. `performance-profiler`: Performance analysis
4. `test-coverage-checker`: Test coverage validation
5. `code-quality-checker`: Code quality metrics
6. `review-synthesizer`: Compile final review

**Orchestration:**

```


## Phase 1: Analysis

skill-1 (pr-analyzer)
Output: PR metadata, changed files, commit history

## Phase 2: Parallel Checks (All independent)

Parallel execution:
├─ skill-2 (security-scanner)
├─ skill-3 (performance-profiler)
├─ skill-4 (test-coverage-checker)
└─ skill-5 (code-quality-checker)

All use PR metadata from Phase 1
Wait for all 4 to complete

## Phase 3: Synthesis

skill-6 (review-synthesizer)
Inputs: All 4 reports from Phase 2
Output: Comprehensive review document

Result:

## PR Review Summary

**Security**: ⚠️ 1 medium vulnerability found

- CVE-2024-XXXX in dependency X
- Recommendation: Upgrade to v2.3.1

**Performance**: ✅ No issues

- No N+1 queries
- Response times within targets

**Test Coverage**: ✅ 94%

- Exceeds 90% requirement
- All critical paths covered

**Code Quality**: ✅ High

- Complexity within limits
- No code smells
- Follows style guide

**Overall**: APPROVED WITH COMMENTS
Merge after addressing security finding

```

## Quality Standards

- All skill invocations must include unique execution_id
- Parallel skills must be truly independent (no hidden dependencies)
- Token budget must account for orchestration overhead (+20%)
- Error recovery must be implemented for each skill
- Final synthesis must resolve conflicts between skill outputs

## Common Pitfalls

### Pitfall 1: Hidden Dependencies in "Parallel" Skills
**Issue**: Skills marked as parallel actually depend on each other
**Example**: skill-A modifies file that skill-B reads
**Solution**: Carefully analyze data dependencies before parallelizing

### Pitfall 2: No Timeout for Long-Running Skills
**Issue**: Workflow hangs waiting for stuck skill
**Solution**: Implement timeout for each skill with fallback

```


## Execute with Timeout

timeout = 15 minutes
start_time = now()

invoke skill-X

while skill-X not complete:
if (now() - start_time) > timeout:
log error
attempt graceful degradation
break

```

### Pitfall 3: Poor Error Aggregation
**Issue**: One skill failure causes unclear error
**Solution**: Aggregate errors with context

```

{
"workflow_status": "partial_failure",
"successful_skills": ["skill-1", "skill-3", "skill-5"],
"failed_skills": [
{
"skill": "skill-4",
"error": "API timeout",
"impact": "missing performance analysis in final report",
"workaround": "manual performance review recommended"
}
],
"final_output": "available with noted limitations"
}

```

## Version History
- 1.0.0 (2025-11-22): Initial release

