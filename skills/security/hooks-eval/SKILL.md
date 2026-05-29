---
name: hooks-eval
description: |

Triggers: agent-sdk, eval, claude-sdk, performance, security
  detailed hook evaluation framework for Claude Code and Agent SDK hooks.

  Triggers: hook audit, hook security, hook performance, hook compliance,
  SDK hooks, hook evaluation, hook benchmarking, hook vulnerability

  Use when: auditing existing hooks for security vulnerabilities, benchmarking
  hook performance, implementing hooks using Python SDK, understanding hook
  callback signatures, validating hooks against compliance standards

  DO NOT use when: deciding hook placement - use hook-scope-guide instead.
  DO NOT use when: writing hook rules from scratch - use hook-authoring instead.
  DO NOT use when: validating plugin structure - use validate-plugin instead.

  Use this skill BEFORE deploying hooks to production.
version: 1.0.0
category: hook-management
tags: [hooks, evaluation, security, performance, claude-sdk, agent-sdk]
dependencies: [hook-scope-guide]
provides:
  infrastructure: ["hook-evaluation", "security-scanning", "performance-analysis"]
  patterns: ["hook-auditing", "sdk-integration", "compliance-checking"]
  sdk_features:
    - "python-sdk-hooks"
    - "hook-callbacks"
    - "hook-matchers"
estimated_tokens: 1200
---
## Table of Contents

- [Overview](#overview)
- [Key Capabilities](#key-capabilities)
- [Core Components](#core-components)
- [Quick Reference](#quick-reference)
- [Hook Event Types](#hook-event-types)
- [Hook Callback Signature](#hook-callback-signature)
- [Return Values](#return-values)
- [Quality Scoring (100 points)](#quality-scoring-(100-points))
- [Detailed Resources](#detailed-resources)
- [Basic Evaluation Workflow](#basic-evaluation-workflow)
- [Integration with Other Tools](#integration-with-other-tools)
- [Related Skills](#related-skills)


# Hooks Evaluation Framework

## Overview

This skill provides a detailed framework for evaluating, auditing, and implementing Claude Code hooks across all scopes (plugin, project, global) and both JSON-based and programmatic (Python SDK) hooks.

### Key Capabilities

- **Security Analysis**: Vulnerability scanning, dangerous pattern detection, injection prevention
- **Performance Analysis**: Execution time benchmarking, resource usage, optimization
- **Compliance Checking**: Structure validation, documentation requirements, best practices
- **SDK Integration**: Python SDK hook types, callbacks, matchers, and patterns

### Core Components

| Component | Purpose |
|-----------|---------|
| **Hook Types Reference** | Complete SDK hook event types and signatures |
| **Evaluation Criteria** | Scoring system and quality gates |
| **Security Patterns** | Common vulnerabilities and mitigations |
| **Performance Benchmarks** | Thresholds and optimization guidance |

## Quick Reference

### Hook Event Types

```python
HookEvent = Literal[
    "PreToolUse",       # Before tool execution
    "PostToolUse",      # After tool execution
    "UserPromptSubmit", # When user submits prompt
    "Stop",             # When stopping execution
    "SubagentStop",     # When a subagent stops
    "PreCompact"        # Before message compaction
]
```
**Verification:** Run the command with `--help` flag to verify availability.

**Note**: Python SDK does not support `SessionStart`, `SessionEnd`, or `Notification` hooks due to setup limitations.

### Hook Callback Signature

```python
async def my_hook(
    input_data: dict[str, Any],    # Hook-specific input
    tool_use_id: str | None,       # Tool ID (for tool hooks)
    context: HookContext           # Additional context
) -> dict[str, Any]:               # Return decision/messages
    ...
```
**Verification:** Run the command with `--help` flag to verify availability.

### Return Values

```python
return {
    "decision": "block",           # Optional: block the action
    "systemMessage": "...",        # Optional: add to transcript
    "hookSpecificOutput": {...}    # Optional: hook-specific data
}
```
**Verification:** Run the command with `--help` flag to verify availability.

### Quality Scoring (100 points)

| Category | Points | Focus |
|----------|--------|-------|
| Security | 30 | Vulnerabilities, injection, validation |
| Performance | 25 | Execution time, memory, I/O |
| Compliance | 20 | Structure, documentation, error handling |
| Reliability | 15 | Timeouts, idempotency, degradation |
| Maintainability | 10 | Code structure, modularity |

## Detailed Resources

- **SDK Hook Types**: See `modules/sdk-hook-types.md` for complete Python SDK type definitions, patterns, and examples
- **Evaluation Criteria**: See `modules/evaluation-criteria.md` for detailed scoring rubric and quality gates
- **Security Patterns**: See `modules/security-patterns.md` for vulnerability detection and mitigation
- **Performance Guide**: See `modules/performance-guide.md` for benchmarking and optimization

## Basic Evaluation Workflow

```bash
# 1. Run detailed evaluation
/hooks-eval --detailed

# 2. Focus on security issues
/hooks-eval --security-only --format sarif

# 3. Benchmark performance
/hooks-eval --performance-baseline

# 4. Check compliance
/hooks-eval --compliance-report
```
**Verification:** Run the command with `--help` flag to verify availability.

## Integration with Other Tools

```bash
# Complete plugin evaluation pipeline
/hooks-eval --detailed          # Evaluate all hooks
/analyze-hook hooks/specific.py      # Deep-dive on one hook
/validate-plugin .                   # Validate overall structure
```
**Verification:** Run the command with `--help` flag to verify availability.

## Related Skills

- `abstract:hook-scope-guide` - Decide where to place hooks (plugin/project/global)
- `abstract:hook-authoring` - Write hook rules and patterns
- `abstract:validate-plugin` - Validate complete plugin structure
## Troubleshooting

### Common Issues

**Hook not firing**
Verify hook pattern matches the event. Check hook logs for errors

**Syntax errors**
Validate JSON/Python syntax before deployment

**Permission denied**
Check hook file permissions and ownership
