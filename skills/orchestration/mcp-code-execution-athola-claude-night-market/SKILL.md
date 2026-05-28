---
name: mcp-code-execution
description: |

Triggers: execution, code
  Transform tool-heavy workflows into MCP code execution patterns for token savings and optimized processing.

  Triggers: MCP, code execution, tool chain, data pipeline, tool transformation, batch processing, workflow optimization

  Use when: >3 tools chained sequentially, large datasets (>10k rows), large files (>50KB), context usage >25%

  DO NOT use when: simple tool calls that don't chain.
  DO NOT use when: context pressure is low and tools are fast.

  Use this skill BEFORE building complex tool chains. Optimize proactively.
location: plugin
token_budget: 200
progressive_loading: true
dependencies:
  hub: [context-optimization, token-conservation]
  modules: [mcp-subagents, mcp-patterns, mcp-validation]
version: 1.3.5
---
## Table of Contents

- [Quick Start](#quick-start)
- [When to Use](#when-to-use)
- [Core Hub Responsibilities](#core-hub-responsibilities)
- [Required TodoWrite Items](#required-todowrite-items)
- [Step 1 – Assess Workflow](#step-1-assess-workflow-mcp-code-executionassess-workflow)
- [Workflow Classification](#workflow-classification)
- [MECW Risk Assessment](#mecw-risk-assessment)
- [Step 2 – Route to Modules](#step-2-route-to-modules-mcp-code-executionroute-to-modules)
- [Module Orchestration](#module-orchestration)
- [Step 3 – Coordinate MECW](#step-3-coordinate-mecw-mcp-code-executioncoordinate-mecw)
- [Cross-Module MECW Management](#cross-module-mecw-management)
- [Step 4 – Synthesize Results](#step-4-synthesize-results-mcp-code-executionsynthesize-results)
- [Result Integration](#result-integration)
- [Module Integration](#module-integration)
- [With Context Optimization Hub](#with-context-optimization-hub)
- [Performance Skills Integration](#performance-skills-integration)
- [Emergency Protocols](#emergency-protocols)
- [Hub-Level Emergency Response](#hub-level-emergency-response)
- [Success Metrics](#success-metrics)


# MCP Code Execution Hub

## Quick Start

### Basic Usage
\`\`\`bash
# Run the main command
python -m module_name

# Show help
python -m module_name --help
\`\`\`

**Verification**: Run with `--help` flag to confirm installation.
## When to Use
- **Automatic**: Keywords: `code execution`, `MCP`, `tool chain`, `data pipeline`, `MECW`
- **Tool Chains**: >3 tools chained sequentially
- **Data Processing**: Large datasets (>10k rows) or files (>50KB)
- **Context Pressure**: Current usage >25% of total window (proactive context management)

> **MCP Tool Search (Claude Code 2.1.7+)**: When MCP tool descriptions exceed 10% of context, tools are automatically deferred and discovered via MCPSearch instead of being loaded upfront. This reduces token overhead by ~85% but means tools must be discovered on-demand. Haiku models do not support tool search. Configure threshold with `ENABLE_TOOL_SEARCH=auto:N` where N is the percentage.

## Core Hub Responsibilities
- Orchestrates MCP code execution workflow
- Routes to appropriate specialized modules
- Coordinates MECW compliance across submodules
- Manages token budget allocation for submodules

## Required TodoWrite Items
1. `mcp-code-execution:assess-workflow`
2. `mcp-code-execution:route-to-modules`
3. `mcp-code-execution:coordinate-mecw`
4. `mcp-code-execution:synthesize-results`

## Step 1 – Assess Workflow (`mcp-code-execution:assess-workflow`)

### Workflow Classification
```python
def classify_workflow_for_mecw(workflow):
    """Determine appropriate MCP modules and MECW strategy"""

    if has_tool_chains(workflow) and workflow.complexity == 'high':
        return {
            'modules': ['mcp-subagents', 'mcp-patterns'],
            'mecw_strategy': 'aggressive',
            'token_budget': 600
        }
    elif workflow.data_size > '10k_rows':
        return {
            'modules': ['mcp-patterns', 'mcp-validation'],
            'mecw_strategy': 'moderate',
            'token_budget': 400
        }
    else:
        return {
            'modules': ['mcp-patterns'],
            'mecw_strategy': 'conservative',
            'token_budget': 200
        }
```
**Verification:** Run the command with `--help` flag to verify availability.

### MECW Risk Assessment
Delegate to mcp-validation module for detailed risk analysis:
```python
def delegate_mecw_assessment(workflow):
    return mcp_validation_assess_mecw_risk(
        workflow,
        hub_allocated_tokens=self.token_budget * 0.5
    )
```
**Verification:** Run the command with `--help` flag to verify availability.

## Step 2 – Route to Modules (`mcp-code-execution:route-to-modules`)

### Module Orchestration
```python
class MCPExecutionHub:
    def __init__(self):
        self.modules = {
            'mcp-subagents': MCPSubagentsModule(),
            'mcp-patterns': MCPatternsModule(),
            'mcp-validation': MCPValidationModule()
        }

    def execute_workflow(self, workflow, classification):
        results = []

        # Execute modules in optimal order
        for module_name in classification['modules']:
            module = self.modules[module_name]
            result = module.execute(
                workflow,
                mecw_budget=classification['token_budget'] //
                len(classification['modules'])
            )
            results.append(result)

        return self.synthesize_results(results)
```
**Verification:** Run the command with `--help` flag to verify availability.

## Step 3 – Coordinate MECW (`mcp-code-execution:coordinate-mecw`)

### Cross-Module MECW Management
- Monitor total context usage across all modules
- Enforce 50% context rule globally
- Coordinate external state management
- Implement MECW emergency protocols

## Step 4 – Synthesize Results (`mcp-code-execution:synthesize-results`)

### Result Integration
```python
def synthesize_module_results(module_results):
    """Combine results from MCP modules into structured output"""

    return {
        'status': 'completed',
        'token_savings': calculate_savings(module_results),
        'mecw_compliance': verify_mecw_rules(module_results),
        'hallucination_risk': assess_hallucination_prevention(module_results),
        'results': consolidate_results(module_results)
    }
```
**Verification:** Run the command with `--help` flag to verify availability.

## Module Integration

### Available Modules
- See `modules/mcp-coordination.md` for cross-module orchestration
- See `modules/mcp-patterns.md` for common MCP execution patterns
- See `modules/mcp-subagents.md` for subagent delegation strategies
- See `modules/mcp-validation.md` for MECW compliance validation

### With Context Optimization Hub
- Receives high-level MECW strategy from context-optimization
- Returns detailed execution metrics and compliance data
- Coordinates token budget allocation

### Performance Skills Integration
- uses python-performance-optimization through mcp-patterns
- Aligns with cpu-gpu-performance for resource-aware execution
- validates optimizations maintain MECW compliance

## Emergency Protocols

### Hub-Level Emergency Response
When MECW limits exceeded:
1. Delegates immediately to mcp-validation for risk assessment
2. Route to mcp-subagents for further decomposition
3. Apply compression through mcp-patterns
4. Return minimal summary to preserve context

## Success Metrics
- **Workflow Success Rate**: >95% successful module coordination
- **MECW Compliance**: 100% adherence to 50% context rule
- **Token Efficiency**: Maintain >80% savings vs traditional methods
- **Module Coordination**: <5% overhead for hub orchestration
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
