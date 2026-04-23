---
name: context-optimization
description: 'Analyze and optimize context window usage with MECW principles, memory tiering, session routing, and subagent coordination.'
version: 1.9.0
alwaysApply: false
category: conservation
token_budget: 150
progressive_loading: true
modules:
- modules/context-waiting.md
- modules/findings-format.md
- modules/mecw-assessment.md
- modules/mecw-principles.md
- modules/memory-tiers.md
- modules/session-routing.md
- modules/subagent-coordination.md
hooks:
  PreToolUse:
  - matcher: Read
    command: 'echo "[skill:context-optimization] 📊 Context analysis started: $(date)"
      >> ${CLAUDE_CODE_TMPDIR:-/tmp}/skill-audit.log

      '
    once: true
  PostToolUse:
  - matcher: Bash
    command: "# Track context analysis tools\nif echo \"$CLAUDE_TOOL_INPUT\" | grep\
      \ -qE \"(wc|tokei|cloc|context)\"; then\n  echo \"[skill:context-optimization]\
      \ Context measurement executed: $(date)\" >> ${CLAUDE_CODE_TMPDIR:-/tmp}/skill-audit.log\n\
      fi\n"
  Stop:
  - command: 'echo "[skill:context-optimization] === Optimization completed at $(date)
      ===" >> ${CLAUDE_CODE_TMPDIR:-/tmp}/skill-audit.log

      # Could export: context pressure events over time

      '
model_hint: standard
---
## Table of Contents

- [When to Use](#when-to-use)
- [Core Hub Responsibilities](#core-hub-responsibilities)
- [Module Selection Strategy](#module-selection-strategy)
- [Context Classification](#context-classification)
- [Integration Points](#integration-points)
- [Resources](#resources)


# Context Optimization Hub

## When To Use

- **Threshold Alert**: When context usage approaches 50% of the window.
- **Complex Tasks**: For operations requiring multi-file analysis or long tool chains.

## When NOT To Use

- Simple single-step tasks with low context usage
- Already using mcp-code-execution for tool chains

## Core Hub Responsibilities

1. Assess context pressure and MECW compliance.
2. Route to appropriate specialized modules.
3. Coordinate subagent-based workflows.
4. Manage token budget allocation across modules.
5. Synthesize results from modular execution.

## Module Selection Strategy

```python
def select_optimal_modules(context_situation, task_complexity):
    if context_situation == "CRITICAL":
        return ['mecw-assessment', 'subagent-coordination']
    elif task_complexity == 'high':
        return ['mecw-principles', 'subagent-coordination']
    else:
        return ['mecw-assessment']
```

## Context Classification

| Utilization | Status | Action |
|-------------|--------|--------|
| < 30% | LOW | Continue normally |
| 30-50% | MODERATE | Monitor, apply principles |
| > 50% | CRITICAL | Immediate optimization required |

## Large Output Handling (Claude Code 2.1.2+)

**Behavior Change**: Large bash command and tool outputs are saved to disk instead of being truncated; file references are provided for access.

### Impact on Context Optimization

| Scenario | Before 2.1.2 | After 2.1.2 |
|----------|--------------|-------------|
| Large test output | Truncated, partial data | Full output via file reference |
| Verbose build logs | Lost after 30K chars | Complete, accessible on-demand |
| Context pressure | Less from truncation | Same - only loaded when read |

### Best Practices

- **Avoid pre-emptive reads**: Large outputs are referenced, not automatically loaded into context.
- **Read selectively**: Use `head`, `tail`, or `grep` on file references.
- **Leverage full data**: Quality gates can access complete test results via files.
- **Monitor growth**: File references are small, but reading the full files adds to context.

## Integration Points

- **Token Conservation**: Receives usage strategies, returns MECW-compliant optimizations.
- **CPU/GPU Performance**: Aligns context optimization with resource constraints.
- **MCP Code Execution**: Delegates complex patterns to specialized MCP modules.

## Resources

- **MECW Theory**: See `modules/mecw-principles.md` for core concepts, the 50% rule, and quick-start code examples.
- **Context Analysis**: See `modules/mecw-assessment.md` for risk identification.
- **Workflow Delegation**: See `modules/subagent-coordination.md` for decomposition patterns.
- **Context Waiting**: See `modules/context-waiting.md` for deferred loading strategies.
## Troubleshooting

### Common Issues

If context usage remains high after optimization, check for large files that were read entirely rather than selectively. If MECW assessments fail, ensure that your environment provides accurate token count metadata. For permission errors when writing output logs to `/tmp`, verify that the project's temporary directory is writable.
