---
name: cascade-orchestrator
description: Creates sophisticated workflow cascades coordinating multiple micro-skills with sequential pipelines, parallel execution, conditional branching, and Codex sandbox iteration. Enhanced with multi-model routing (Gemini/Codex), ruv-swarm coordination, memory persistence, and audit-pipeline patterns for production workflows.
tags: [orchestration, workflows, cascades, multi-model, codex-integration, tier-2]
version: 2.0.0
---

# Cascade Orchestrator (Enhanced)

## Overview
Manages workflows (cascades) that coordinate multiple micro-skills into cohesive processes. This enhanced version integrates Codex sandbox iteration, multi-model routing, ruv-swarm coordination, and memory persistence across stages.

## Philosophy: Composable Excellence

Complex capabilities emerge from composing simple, well-defined components.

**Enhanced Capabilities**:
- **Codex Sandbox Iteration**: Auto-fix failures in isolated environment (from audit-pipeline)
- **Multi-Model Routing**: Use Gemini/Codex based on stage requirements
- **Swarm Coordination**: Parallel execution via ruv-swarm MCP
- **Memory Persistence**: Maintain context across stages
- **GitHub Integration**: CI/CD pipeline automation

**Key Principles**:
1. Separation of concerns (micro-skills execute, cascades coordinate)
2. Reusability through composition
3. Flexible orchestration patterns
4. Declarative workflow definition
5. Intelligent model selection

## Cascade Architecture (Enhanced)

### Definition Layer

**Extended Stage Types**:
```yaml
stages:
  - type: sequential     # One after another
  - type: parallel       # Simultaneous execution
  - type: conditional    # Based on runtime conditions
  - type: codex-sandbox  # NEW: Iterative testing with auto-fix
  - type: multi-model    # NEW: Intelligent AI routing
  - type: swarm-parallel # NEW: Coordinated via ruv-swarm
```

**Enhanced Data Flow**:
```yaml
data_flow:
  - stage_output: previous stage results
  - shared_memory: persistent across stages
  - multi_model_context: AI-specific formatting
  - codex_sandbox_state: isolated test environment
```

**Advanced Error Handling**:
```yaml
error_handling:
  - retry_with_backoff
  - fallback_to_alternative
  - codex_auto_fix        # NEW: Auto-fix via Codex
  - model_switching       # NEW: Try different AI
  - swarm_recovery        # NEW: Redistribute tasks
```

### Execution Engine (Enhanced)

**Stage Scheduling with AI Selection**:
```python
for stage in cascade.stages:
    if stage.type == "codex-sandbox":
        execute_with_codex_iteration(stage)
    elif stage.type == "multi-model":
        model = select_optimal_model(stage.task)
        execute_on_model(stage, model)
    elif stage.type == "swarm-parallel":
        execute_via_ruv_swarm(stage)
    else:
        execute_standard(stage)
```

**Codex Sandbox Iteration Loop**:
```python
def execute_with_codex_iteration(stage):
    """
    From audit-pipeline Phase 2: functionality-audit pattern
    """
    results = execute_tests(stage.tests)

    for test in failed_tests(results):
        iteration = 0
        max_iterations = 5

        while test.failed and iteration < max_iterations:
            # Spawn Codex in sandbox
            fix = spawn_codex_auto(
                task=f"Fix test failure: {test.error}",
                sandbox=True,
                context=test.context
            )

            # Re-test
            test.result = rerun_test(test)
            iteration += 1

            if test.passed:
                apply_fix_to_main(fix)
                break

        if still_failed(test):
            escalate_to_user(test)

    return aggregate_results(results)
```

**Multi-Model Routing**:
```python
def select_optimal_model(task):
    """
    Route to best AI based on task characteristics
    """
    if task.requires_large_context:
        return "gemini-megacontext"  # 1M tokens
    elif task.needs_current_info:
        return "gemini-search"        # Web grounding
    elif task.needs_visual_output:
        return "gemini-media"          # Imagen/Veo
    elif task.needs_rapid_prototype:
        return "codex-auto"            # Full Auto
    elif task.needs_alternative_view:
        return "codex-reasoning"       # GPT-5-Codex
    else:
        return "claude"                # Best overall
```

## Enhanced Cascade Patterns

### Pattern 1: Linear Pipeline with Multi-Model

```yaml
cascade:
  name: enhanced-data-pipeline
  stages:
    - stage: extract
      model: auto-select
      skill: extract-data

    - stage: validate
      model: auto-select
      skill: validate-data
      error_handling:
        strategy: codex-auto-fix  # NEW

    - stage: transform
      model: codex-auto           # Fast prototyping
      skill: transform-data

    - stage: report
      model: gemini-media         # Generate visuals
      skill: generate-report
```

### Pattern 2: Parallel Fan-Out with Swarm

```yaml
cascade:
  name: code-quality-swarm
  stages:
    - stage: quality-checks
      type: swarm-parallel        # NEW: Via ruv-swarm
      skills:
        - lint-code
        - security-scan
        - complexity-analysis
        - test-coverage
      swarm_config:
        topology: mesh
        max_agents: 4
        strategy: balanced

    - stage: aggregate
      skill: merge-quality-reports
```

### Pattern 3: Codex Sandbox Iteration

```yaml
cascade:
  name: test-and-fix
  stages:
    - stage: functionality-audit
      type: codex-sandbox         # NEW
      test_suite: comprehensive
      codex_config:
        mode: full-auto
        max_iterations: 5
        sandbox: true
      error_recovery:
        auto_fix: true
        escalate_after: 5

    - stage: validate-fixes
      skill: regression-tests
```

### Pattern 4: Conditional with Model Switching

```yaml
cascade:
  name: adaptive-workflow
  stages:
    - stage: analyze
      model: gemini-megacontext   # Large context
      skill: analyze-codebase

    - stage: decide
      type: conditional
      condition: ${analyze.quality_score}
      branches:
        high_quality:
          model: codex-auto       # Fast path
          skill: deploy-fast
        low_quality:
          model: multi-model      # Comprehensive path
          cascade: deep-quality-audit
```

### Pattern 5: Iterative with Memory

```yaml
cascade:
  name: iterative-refinement
  stages:
    - stage: refactor
      model: auto-select
      skill: refactor-code
      memory: persistent          # NEW

    - stage: check-quality
      skill: quality-metrics

    - stage: repeat-decision
      type: conditional
      condition: ${quality < threshold}
      repeat: refactor            # Loop back
      max_iterations: 3
      memory_shared: true         # Context persists
```

## Creating Enhanced Cascades

### Step 1: Define with AI Considerations

**Identify Model Requirements**:
```markdown
For each stage, determine:
- Large context needed? → Gemini
- Current web info needed? → Gemini Search
- Visual output needed? → Gemini Media
- Rapid prototyping needed? → Codex
- Testing with auto-fix? → Codex Sandbox
- Best overall reasoning? → Claude
```

### Step 2: Design with Swarm Parallelism

**When to Use Swarm**:
- Multiple independent tasks
- Resource-intensive operations
- Need load balancing
- Want fault tolerance

**Swarm Configuration**:
```yaml
swarm_config:
  topology: mesh | hierarchical | star
  max_agents: number
  strategy: balanced | specialized | adaptive
  memory_shared: true | false
```

### Step 3: Add Codex Iteration for Quality

**Pattern from audit-pipeline**:
```yaml
stages:
  - type: codex-sandbox
    tests: ${test_suite}
    fix_strategy:
      auto_fix: true
      max_iterations: 5
      sandbox_isolated: true
      network_disabled: true
      regression_check: true
```

### Step 4: Enable Memory Persistence

**Shared Memory Across Stages**:
```yaml
memory:
  persistence: enabled
  scope: cascade | global
  storage: mcp__ruv-swarm__memory
  keys:
    - analysis_results
    - intermediate_outputs
    - learned_patterns
```

## Enhanced Cascade Definition Format

```yaml
cascade:
  name: cascade-name
  description: What this accomplishes
  version: 2.0.0

  config:
    multi_model: enabled
    swarm_coordination: enabled
    memory_persistence: enabled
    github_integration: enabled

  inputs:
    - name: input-name
      type: type
      description: description

  stages:
    - stage_id: stage-1
      name: Stage Name
      type: sequential | parallel | codex-sandbox | multi-model | swarm-parallel
      model: auto-select | gemini | codex | claude

      # For micro-skill execution
      skills:
        - skill: micro-skill-name
          inputs: {...}
          outputs: {...}

      # For Codex sandbox
      codex_config:
        mode: full-auto
        sandbox: true
        max_iterations: 5

      # For swarm execution
      swarm_config:
        topology: mesh
        max_agents: 4

      # For memory
      memory:
        read_keys: [...]
        write_keys: [...]

      error_handling:
        strategy: retry | codex-auto-fix | model-switch | swarm-recovery
        max_retries: 3
        fallback: alternative-skill

  memory:
    persistence: enabled
    scope: cascade

  github_integration:
    create_pr: on_success
    report_issues: on_failure
```

## Real-World Enhanced Cascades

### Example 1: Complete Development Workflow

```yaml
cascade: complete-dev-workflow
stages:
  1. gemini-search: "Research latest framework best practices"
  2. codex-auto: "Rapid prototype with best practices"
  3. codex-sandbox: "Test everything, auto-fix failures"
  4. gemini-media: "Generate architecture diagrams"
  5. style-audit: "Polish code to production standards"
  6. github-pr: "Create PR with comprehensive report"
```

### Example 2: Legacy Modernization

```yaml
cascade: modernize-legacy-code
stages:
  1. gemini-megacontext: "Analyze entire 50K line codebase"
  2. theater-detection: "Find all mocks and placeholders"
  3. [swarm-parallel]:
     - codex-auto: "Complete implementations" (parallel)
     - gemini-media: "Document architecture"
  4. codex-sandbox: "Test all changes with auto-fix"
  5. style-audit: "Final polish"
  6. generate-pr: "Create PR with before/after comparison"
```

### Example 3: Bug Fix with RCA

```yaml
cascade: intelligent-bug-fix
stages:
  1. root-cause-analyzer: "Deep RCA analysis"
  2. multi-model-decision:
     condition: ${rca.complexity}
     simple: codex-auto (quick fix)
     complex: [
       gemini-megacontext (understand broader context),
       codex-reasoning (alternative approaches),
       claude (implement best approach)
     ]
  3. codex-sandbox: "Test fix thoroughly"
  4. regression-suite: "Ensure no breakage"
  5. github-issue-update: "Document fix with RCA report"
```

## Integration Points

### With Micro-Skills
- Executes micro-skills in stages
- Passes data between skills
- Handles skill errors gracefully

### With Multi-Model System
- Routes stages to optimal AI
- Uses gemini-* skills for unique capabilities
- Uses codex-* skills for prototyping/fixing
- Uses Claude for best reasoning

### With Audit Pipeline
- Incorporates theater → functionality → style pattern
- Uses Codex sandbox iteration from Phase 2
- Applies quality gates throughout

### With Slash Commands
- Commands trigger cascades
- Parameter mapping from command to cascade
- Progress reporting to command interface

### With Ruv-Swarm MCP
- Parallel stage coordination
- Memory persistence
- Neural training
- Performance tracking

## Working with Enhanced Cascade Orchestrator

**Invocation**:
"Create a cascade that [end goal] using [micro-skills] with [Codex/Gemini/swarm] capabilities"

**The orchestrator will**:
1. Design workflow with optimal AI model selection
2. Configure Codex sandbox for testing stages
3. Set up swarm coordination for parallel stages
4. Enable memory persistence across stages
5. Integrate with GitHub for CI/CD
6. Generate executable cascade definition

**Advanced Features**:
- Automatic model routing based on task
- Codex iteration loop for auto-fixing
- Swarm coordination for parallelism
- Memory sharing across stages
- GitHub PR/issue integration
- Performance monitoring and optimization

---

**Version 2.0 Enhancements**:
- Codex sandbox iteration pattern
- Multi-model intelligent routing
- Ruv-swarm MCP integration
- Memory persistence
- GitHub workflow automation
- Enhanced error recovery
