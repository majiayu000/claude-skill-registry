---
name: review-feedback-schema
description: Schema for tracking code review outcomes to enable feedback-driven skill improvement. Use when logging review results or analyzing review quality.
---

# Review Feedback Schema

## Purpose

Structured format for logging code review outcomes. This data enables:
1. Identifying rules that produce false positives
2. Tracking skill accuracy over time
3. Automated skill improvement via pattern analysis

## Schema

```csv
date,file,line,rule_source,category,severity,issue,verdict,rationale
```

| Field | Type | Description | Example Values |
|-------|------|-------------|----------------|
| `date` | ISO date | When review occurred | `2025-12-23` |
| `file` | path | Relative file path | `amelia/agents/developer.py` |
| `line` | string | Line number(s) | `128`, `190-191` |
| `rule_source` | string | Skill and rule that triggered issue | `python-code-review/common-mistakes:unused-variables`, `pydantic-ai-common-pitfalls:tool-decorator` |
| `category` | enum | Issue taxonomy | `type-safety`, `async`, `error-handling`, `style`, `patterns`, `testing`, `security` |
| `severity` | enum | As flagged by reviewer | `critical`, `major`, `minor` |
| `issue` | string | Brief description | `Return type list[Any] loses type safety` |
| `verdict` | enum | Human decision | `ACCEPT`, `REJECT`, `DEFER`, `ACKNOWLEDGE` |
| `rationale` | string | Why verdict was chosen | `pydantic-ai docs explicitly support this pattern` |

## Verdict Types

| Verdict | Meaning | Action |
|---------|---------|--------|
| `ACCEPT` | Issue is valid, will fix | Code change made |
| `REJECT` | Issue is invalid/wrong | No change; may improve skill |
| `DEFER` | Valid but not fixing now | Tracked for later |
| `ACKNOWLEDGE` | Valid but intentional | Document why it's intentional |

### When to Use Each

**ACCEPT**: The reviewer correctly identified a real issue.
```csv
2025-12-27,amelia/agents/developer.py,128,python-code-review:type-safety,type-safety,major,Return type list[Any] loses type safety,ACCEPT,Changed to list[AgentMessage]
```

**REJECT**: The reviewer was wrong - the code is correct.
```csv
2025-12-23,amelia/drivers/api/openai.py,102,python-code-review:line-length,style,minor,Line too long (104 > 100),REJECT,ruff check passes - no E501 violation exists
```

**DEFER**: Valid issue but out of scope for current work.
```csv
2025-12-22,api/handlers.py,45,fastapi-code-review:error-handling,error-handling,minor,Missing specific exception type,DEFER,Refactoring planned for Q1
```

**ACKNOWLEDGE**: Intentional design decision.
```csv
2025-12-21,core/cache.py,89,python-code-review:optimization,patterns,minor,Using dict instead of dataclass,ACKNOWLEDGE,Performance-critical path - intentional
```

## Rule Source Format

Format: `skill-name/section:rule-id` or `skill-name:rule-id`

Examples:
- `python-code-review/common-mistakes:unused-variables`
- `pydantic-ai-common-pitfalls:tool-decorator`
- `fastapi-code-review:dependency-injection`
- `pytest-code-review:fixture-scope`

Use the skill folder name and identify the specific rule or section that triggered the issue.

## Category Taxonomy

| Category | Description | Examples |
|----------|-------------|----------|
| `type-safety` | Type annotation issues | Missing types, incorrect types, `Any` usage |
| `async` | Async/await issues | Blocking in async, missing await |
| `error-handling` | Exception handling | Bare except, missing error handling |
| `style` | Code style/formatting | Line length, naming conventions |
| `patterns` | Design patterns | Anti-patterns, framework misuse |
| `testing` | Test quality | Missing coverage, flaky tests |
| `security` | Security issues | Injection, secrets exposure |

## Writing Good Rationales

### For ACCEPT

Explain what you fixed:
- "Changed Exception to (FileNotFoundError, OSError)"
- "Fixed using model_copy(update={...})"
- "Removed unused Any import"

### For REJECT

Explain why the issue is invalid:
- "ruff check passes - no E501 violation exists" (linter authoritative)
- "pydantic-ai docs explicitly support this pattern" (framework idiom)
- "Intentional optimization documented in code comment" (documented decision)

### For DEFER

Explain when/why it will be addressed:
- "Tracked in issue #123"
- "Refactoring planned for Q1"
- "Blocked on dependency upgrade"

### For ACKNOWLEDGE

Explain why it's intentional:
- "Performance-critical path per CLAUDE.md"
- "Legacy API compatibility requirement"
- "Matches upstream library pattern"

## Example Log

```csv
date,file,line,rule_source,category,severity,issue,verdict,rationale
2025-12-20,tests/integration/test_cli_flows.py,407,pytest-code-review:parametrization,testing,minor,Unused extra_args parameter in parametrization,ACCEPT,Fixed - removed dead parameter
2025-12-20,tests/integration/test_cli_flows.py,237-242,pytest-code-review:coverage,testing,major,Missing review --local in git repo error test,REJECT,Not applicable - review uses different error path
2025-12-21,amelia/server/orchestrator/service.py,1702,python-code-review:immutability,patterns,critical,Direct mutation of frozen ExecutionState,ACCEPT,Fixed using model_copy(update={...})
2025-12-23,amelia/drivers/api/tools.py,48-53,pydantic-ai-common-pitfalls:tool-decorator,patterns,major,Misleading RunContext pattern - should use decorators,REJECT,pydantic-ai docs explicitly support passing raw functions with RunContext to Agent(tools=[])
2025-12-23,amelia/drivers/api/openai.py,102,python-code-review:line-length,style,minor,Line too long (104 > 100),REJECT,ruff check passes - no E501 violation exists
2025-12-27,amelia/core/orchestrator.py,190-191,python-code-review:exception-handling,error-handling,major,Generic exception handling in get_code_changes_for_review,ACCEPT,Changed Exception to (FileNotFoundError OSError)
2025-12-27,amelia/agents/developer.py,128,python-code-review:type-safety,type-safety,major,Return type list[Any] loses type safety,ACCEPT,Changed to list[AgentMessage] and removed unused Any import
```

## Pre-Review Verification Checklist

Before reporting ANY finding, reviewers MUST verify:

### Verification Steps

1. **Confirm the issue exists**: Read the actual code, don't infer from context
2. **Check surrounding code**: The issue may be handled elsewhere (guards, earlier checks)
3. **Trace state/variable usage**: Search for all references before claiming "unused"
4. **Verify assertions**: If claiming "X is missing", confirm X isn't present
5. **Check framework handling**: Many frameworks handle validation/errors automatically
6. **Validate syntax understanding**: Verify against current docs (Tailwind v4, TS 5.x, etc.)

### Common False Positive Patterns

| Pattern | Root Cause | Prevention |
|---------|------------|------------|
| "Unused variable" | Variable used elsewhere | Search all references |
| "Missing validation" | Framework validates | Check Pydantic/Zod/etc. |
| "Type assertion" | Actually annotation | Confirm `as` vs `:` |
| "Memory leak" | Cleanup exists | Check effect returns |
| "Wrong syntax" | New framework version | Verify against current docs |
| "Style issue" | Preference not rule | Both approaches valid |

### Signals of False Positive Risk

If you're about to flag any of these, double-check:
- "This variable appears unused" → Search for ALL references first
- "Missing error handling" → Check parent/framework handling
- "Should use X instead of Y" → Both may be valid
- "This syntax looks wrong" → Verify against current version docs

Reference: [review-verification-protocol](../review-verification-protocol/SKILL.md) for full verification workflow.

## How This Feeds Into Skill Improvement

1. **Aggregate by rule_source**: Identify which rules have high REJECT rates
2. **Analyze rationales**: Find common themes in rejections
3. **Update skills**: Add exceptions, clarifications, or verification steps
4. **Track impact**: Measure if changes reduce rejection rate

See `review-skill-improver` skill for the full analysis workflow.

### Improvement Signals

| Pattern | Skill Improvement |
|---------|-------------------|
| "linter passes" rejections | Add linter verification step before flagging style issues |
| "docs support this" rejections | Add exception for documented framework patterns |
| "intentional" rejections | Add codebase context check before flagging |
| "wrong code path" rejections | Add code tracing step before claiming gaps |
