/*============================================================================*/
/* WHEN-MAPPING-DEPENDENCIES-USE-DEPENDENCY-MAPPER SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-mapping-dependencies-use-dependency-mapper
version: 1.0.0
description: |
  [assert|neutral] Comprehensive dependency mapping, analysis, and visualization tool for software projects [ground:given] [conf:0.95] [state:confirmed]
category: analysis
tags:
- dependencies
- graph-analysis
- security
- visualization
- mece
author: Claude Code
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-mapping-dependencies-use-dependency-mapper workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic analysis processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-mapping-dependencies-use-dependency-mapper",
  category: "analysis",
  version: "1.0.0",
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
  keywords: ["when-mapping-dependencies-use-dependency-mapper", "analysis", "workflow"],
  context: "user needs when-mapping-dependencies-use-dependency-mapper capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Dependency Mapper Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

**When mapping dependencies, use dependency-mapper** to extract, analyze, visualize, and audit dependency trees across multiple package managers (npm, pip, cargo, maven, go.mod).

## MECE Breakdown

### Mutually Exclusive Components:
1. **Extraction Phase**: Parse lock files and manifests
2. **Analysis Phase**: Build dependency graph and detect issues
3. **Security Phase**: Audit for vulnerabilities
4. **Visualization Phase**: Generate interactive dependency graphs
5. **Reporting Phase**: Create actionable recommendations

### Collectively Exhaustive Coverage:
- All major package managers (npm, pip, cargo, maven, go)
- Direct and transitive dependencies
- Circular dependency detection
- License compliance checking
- Security vulnerability scanning
- Outdated package detection
- Duplicate dependency identification

## Features

### Core Capabilities:
- Multi-language dependency extraction
- Dependency graph construction
- Circular dependency detection
- Security vulnerability scanning
- License compliance auditing
- Outdated package detection
- Interactive visualization generation
- Dependency optimization recommendations

### Supported Package Managers:
- **JavaScript/Node**: npm, yarn, pnpm
- **Python**: pip, poetry, pipenv
- **Rust**: cargo
- **Java**: maven, gradle
- **Go**: go.mod
- **Ruby**: bundler
- **PHP**: composer
- **C#**: nuget

## Usage

### Slash Command:
```bash
/dep-map [path] [--format json|html|svg] [--security] [--circular] [--outdated]
```

### Subagent Invocation:
```javascript
Task("Dependency Mapper", "Analyze dependencies for ./project with security audit", "code-analyzer")
```

### MCP Tool:
```javascript
mcp__dependency-mapper__analyze({
  project_path: "./project",
  include_security: true,
  detect_circular: true,
  visualization_format: "html"
})
```

## Architecture

### Phase 1: Discovery
1. Detect project type and package manager
2. Locate manifest and lock files
3. Parse dependency declarations

### Phase 2: Extraction
1. Extract direct dependencies
2. Resolve transitive dependencies
3. Build dependency tree structure

### Phase 3: Analysis
1. Detect circular dependencies
2. Identify duplicate dependencies
3. Check for outdated packages
4. Analyze dependency depth

### Phase 4: Security
1. Query vulnerability databases
2. Check license compliance
3. Identify supply chain risks
4. Generate security scores

### Phase 5: Visualization
1. Generate graph data structure
2. Create interactive HTML visualization
3. Export SVG/PNG diagrams
4. Generate dependency reports

## Output Formats

### JSON Report:
```json
{
  "project": "my-app",
  "package_manager": "npm",
  "total_dependencies": 847,
  "direct_dependencies": 23,
  "vulnerabilities": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 12
  },
  "circular_dependencies": [],
  "outdated_packages": 15,
  "license_issues": 0,
  "dependency_tree": {...}
}
```

### HTML Visualization:
Interactive D3.js graph with:
- Zoomable dependency tree
- Vulnerability highlighting
- Circular dependency paths
- Click-to-expand nodes
- Search and filter capabilities

### SVG/PNG Export:
Static GraphViz-generated diagrams

## Examples

### Example 1: Basic Analysis
```bash
/dep-map ./my-project
```

### Example 2: Security-Focused Audit
```bash
/dep-map ./my-project --security --format json
```

### Example 3: Circular Dependency Detection
```bash
/dep-map ./my-project --circular --visualization svg
```

### Example 4: Full Comprehensive Analysis
```bash
/dep-map ./my-project --security --circular --outdated --format html
```

## Integration with Claude-Flow

### Coordination Pattern:
```javascript
// Step 1: Initialize swarm for complex analysis
mcp__claude-flow__swarm_init({ topology: "hierarchical", maxAgents: 4 })

// Step 2: Spawn agents via Claude Code Task tool
[Parallel Execution]:
  Task("Dependency Extractor", "Extract all

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
  pattern: "skills/analysis/when-mapping-dependencies-use-dependency-mapper/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-mapping-dependencies-use-dependency-mapper-{session_id}",
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

[commit|confident] <promise>WHEN_MAPPING_DEPENDENCIES_USE_DEPENDENCY_MAPPER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
