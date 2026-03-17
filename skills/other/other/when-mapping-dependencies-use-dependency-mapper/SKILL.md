---
name: when-mapping-dependencies-use-dependency-mapper
version: 1.0.0
description: Comprehensive dependency mapping, analysis, and visualization tool for software projects
author: Claude Code
category: analysis
complexity: MEDIUM
tags: [dependencies, graph-analysis, security, visualization, mece]
agents:
  - code-analyzer
  - researcher
  - security-manager
components:
  - subagent
  - slash-command
  - mcp-tool
dependencies:
  - claude-flow@alpha
  - graphviz (optional)
  - npm/pip/cargo (auto-detected)
---

# Dependency Mapper Skill

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
  Task("Dependency Extractor", "Extract all dependencies from package.json and package-lock.json", "code-analyzer")
  Task("Security Auditor", "Run npm audit and cross-reference CVE databases", "security-manager")
  Task("Graph Builder", "Construct dependency graph and detect circular deps", "code-analyzer")
  Task("Visualization Generator", "Create interactive HTML dependency graph", "coder")
```

## Configuration

### Default Settings:
```json
{
  "max_depth": 10,
  "include_dev_dependencies": true,
  "security_scan_enabled": true,
  "circular_detection_enabled": true,
  "license_check_enabled": true,
  "outdated_check_enabled": true,
  "visualization_default_format": "html",
  "cache_results": true,
  "cache_ttl": 3600
}
```

## Performance Considerations

- **Caching**: Results cached for 1 hour by default
- **Parallel Processing**: Multiple package managers analyzed concurrently
- **Incremental Analysis**: Only re-analyze changed dependencies
- **Lazy Loading**: Visualization loads nodes on-demand for large graphs

## Error Handling

- Graceful degradation if package manager unavailable
- Fallback to partial analysis if network issues
- Clear error messages for invalid project structures
- Retry logic for transient failures

## Best Practices

1. Run dependency mapping before major releases
2. Integrate into CI/CD pipelines for automated auditing
3. Set up alerts for critical vulnerabilities
4. Review circular dependencies regularly
5. Keep dependency depth shallow (< 5 levels)
6. Audit licenses for compliance requirements
7. Update outdated packages incrementally

## Troubleshooting

### Issue: No dependencies found
**Solution**: Ensure lock files are present (package-lock.json, yarn.lock, etc.)

### Issue: Visualization too large to render
**Solution**: Use `--max-depth 5` to limit tree depth

### Issue: Security scan taking too long
**Solution**: Use cached results or run offline mode

## See Also

- PROCESS.md - Detailed step-by-step workflow
- README.md - Quick start guide
- subagent-dependency-mapper.md - Agent implementation details
- slash-command-dep-map.sh - Command-line interface
- mcp-dependency-mapper.json - MCP tool schema
