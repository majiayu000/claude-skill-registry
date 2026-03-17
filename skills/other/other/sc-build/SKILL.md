---
name: sc-build
description: Build, compile, and package projects with intelligent error handling and optimization. Use when building projects, creating artifacts, debugging build failures, or preparing deployments.
---

# Build & Package Skill

Project building and packaging with optimization and error handling.

## Quick Start

```bash
# Standard build
/sc:build [target]

# Production with optimization
/sc:build --type prod --clean --optimize

# Verbose development build
/sc:build frontend --type dev --verbose
```

## Behavioral Flow

1. **Analyze** - Project structure, configs, dependencies
2. **Validate** - Build environment, toolchain components
3. **Execute** - Build process with real-time monitoring
4. **Optimize** - Apply optimizations, minimize bundles
5. **Package** - Generate artifacts and build reports

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | dev | dev, prod, test |
| `--clean` | bool | false | Clean build (remove previous artifacts) |
| `--optimize` | bool | false | Enable advanced optimizations |
| `--verbose` | bool | false | Detailed build output |
| `--validate` | bool | false | Include validation steps |

## Personas Activated

- **devops-engineer** - Build optimization and deployment preparation

## Evidence Requirements

This skill requires evidence. You MUST:
- Show build command output and exit codes
- Reference generated artifacts
- Report timing metrics and optimization results

## Build Types

### Development (`--type dev`)
- Fast compilation
- Source maps enabled
- Debug symbols included
- No minification

### Production (`--type prod`)
- Full optimization
- Minification enabled
- Tree-shaking applied
- Dead code elimination

### Test (`--type test`)
- Test coverage instrumentation
- Mock configurations
- Test-specific environment

## Examples

### Clean Production Build
```
/sc:build --type prod --clean --optimize
# Minification, tree-shaking, deployment prep
```

### Component Build
```
/sc:build frontend --verbose
# Targeted build with detailed output
```

### Validation Build
```
/sc:build --type dev --validate
# Development build with quality gates
```

## Error Handling

Build failures trigger:
1. Error log analysis
2. Dependency verification
3. Configuration validation
4. Actionable resolution guidance

## Tool Coordination

- **Bash** - Build system execution
- **Read** - Configuration analysis
- **Grep** - Error parsing and log analysis
- **Glob** - Artifact discovery
- **Write** - Build reports
