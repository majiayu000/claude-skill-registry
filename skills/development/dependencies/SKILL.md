/*============================================================================*/
/* DEPENDENCIES SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: dependencies
version: 2.1.0
description: |
  [assert|neutral] Dependency management and analysis hub. Map project dependencies, analyze dependency graphs, identify vulnerabilities, and manage package versions. Routes to dependency-mapper and related analysis too [ground:given] [conf:0.95] [state:confirmed]
category: tooling
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute dependencies workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic tooling processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "dependencies",
  category: "tooling",
  version: "2.1.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["dependencies", "tooling", "workflow"],
  context: "user needs dependencies capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Dependencies

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Dependency management, analysis, and vulnerability detection for projects.

## Phase 0: Expertise Loading

```yaml
expertise_check:
  domain: dependencies
  file: .claude/expertise/dependencies.yaml

  if_exists:
    - Load package ecosystems
    - Load vulnerability databases
    - Apply version policies

  if_not_exists:
    - Flag discovery mode
    - Document patterns learned
```

## When to Use This Skill

Use dependencies when:
- Mapping project dependency graphs
- Analyzing package vulnerabilities
- Managing version upgrades
- Identifying circular dependencies
- Auditing security issues

## Sub-Skills

| Skill | Use Case |
|-------|----------|
| dependency-mapper | Visualize dependency graphs |

## Dependency Analysis

### Package Ecosystems
```yaml
supported:
  - npm/yarn (JavaScript)
  - pip/poetry (Python)
  - cargo (Rust)
  - go mod (Go)
  - maven/gradle (Java)
  - composer (PHP)
```

### Analysis Types
```yaml
analyses:
  graph: "Dependency tree visualization"
  vulnerabilities: "CVE/security scanning"
  outdated: "Version freshness check"
  circular: "Circular dependency detection"
  unused: "Dead dependency identification"
```

## Commands

```bash
# Map dependencies
npm ls --all
pip list --format=freeze
cargo tree

# Security audit
npm audit
pip-audit
cargo audit
```

## MCP Requirements

- **claude-flow**: For orchestration
- **Bash**: For package commands

## Recursive Improvement Integration (v2.1)

### Eval Harness Integration

```yaml
benchmark: dependencies-benchmark-v1
  tests:
    - dep-001: Graph generation
    - dep-002: Vulnerability detection
  minimum_scores:
    graph_accuracy: 0.95
    vuln_detection: 0.90
```

### Memory Namespace

```yaml
namespaces:
  - dependencies/graphs/{id}: Dependency graphs
  - dependencies/audits/{id}: Security audits
  - improvement/audits/dependencies: Skill audits
```

### Uncertainty Handling

```yaml
confidence_check:
  if confidence >= 0.8:
    - Proceed with analysis
  if confidence 0.5-0.8:
    - Confirm package ecosystem
  if confidence < 0.5:
    - Ask for package.json/requirements.txt
```

### Cross-Skill Coordination

Works with: **security**, **code-review-assistant**, **deployment-readiness**

---

## !! SKILL COMPLETION VERIFICATION (MANDATORY) !!

- [ ] **Agent Spawning**: Spawned agent via Task()
- [ ] **Agent Registry Validation**: Agent from registry
- [ ] **TodoWrite Called**: Called with 5+ todos
- [ ] **Work Delegation**: Delegated to agents

**Remember: Skill() -> Task() -> TodoWrite() - ALWAYS**

---

## Core Principles

### 1. Transitive Dependency Awareness as Security Priority
Direct dependencies are visible and reviewed, but transitive dependencies (dependencies-of-dependencies) often escape scrutiny despite comprising 80-95% of total dependency count. A single vulnerable transitive dependency deep in the graph creates exploitable attack surface. Dependency analysis must traverse the full graph, flagging high-risk transitives (unmaintained packages, known CVEs, excessive permissions) with equal priority to direct dependencies.

### 2. Version Freshness Balanced Against Stability Risk
Outdated dependencies accumulate security vulnerabilities and miss performance improvements, but aggressive version upgrades introduce breaking changes and untested code paths. The optimal strategy is risk-stratified: security patches applied immediately, minor updates batched and tested weekly, major updates evaluated for breaking changes and scheduled deliberately. Blanket "always latest" or "never update" policies fail by ignoring risk context.

### 3. Circular Dependencies as Architectural Code Smell
Circular dependencies (package A depends on B, B depends on A) indicate architectural coupling that prevents independent evolution, complicates testing, and signals unclear separation of concerns. While sometimes unavoidable in legacy codebases, new circular dependenc

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/tooling/dependencies/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "dependencies-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>DEPENDENCIES_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
