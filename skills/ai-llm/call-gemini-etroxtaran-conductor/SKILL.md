---
name: call-gemini
description: Invoke the Gemini CLI for architecture and scalability review.
version: 1.1.0
tags: [gemini, architecture, review, validation]
owner: orchestration
status: active
---

# Call Gemini Skill

Wrapper for invoking Gemini agent via CLI for architecture and scalability review.

## Overview

Gemini is specialized for:
- Architecture pattern analysis
- Scalability assessment
- Design principle compliance
- Technical debt evaluation

## Prerequisites

- `gemini` CLI installed and accessible on PATH.

## Usage

```
/call-gemini
```

## Expertise Weights

| Area | Weight | Description |
|------|--------|-------------|
| Architecture | 0.7 | Design patterns, modularity |
| Scalability | 0.8 | Performance at scale, bottlenecks |
| Patterns | 0.6 | Design patterns, anti-patterns |

## CLI Invocation

```bash
gemini --yolo "<prompt>"
```

### Flags

| Flag | Purpose |
|------|---------|
| `--yolo` | Auto-approve tool calls (required for non-interactive) |
| `--model` | Select model (optional, default: gemini-2.0-flash) |

**IMPORTANT**:
- Gemini does NOT support `--output-format`
- Output must be parsed from raw response
- Prompt is a positional argument

## Standard Prompts

### Plan Validation (Phase 2)

```bash
gemini --yolo "
You are reviewing an implementation plan for architecture and scalability.

Read the plan JSON provided by the orchestrator (phase_outputs export).

Evaluate for:
1. Architecture patterns - Are they appropriate for the use case?
2. Modularity - Is the design properly decomposed?
3. Scalability - Will this scale with increased load?
4. Maintainability - Is the code easy to maintain and extend?
5. Technical debt - Does this introduce unnecessary complexity?
6. Design principles - SOLID, DRY, KISS compliance

Return your assessment as JSON (wrap in code block):
\`\`\`json
{
  \"agent\": \"gemini\",
  \"phase\": \"validation\",
  \"approved\": true|false,
  \"score\": 1-10,
  \"assessment\": \"Brief summary of your review\",
  \"architecture_review\": {
    \"patterns_identified\": [\"List of patterns found\"],
    \"patterns_recommended\": [\"Patterns that should be used\"],
    \"anti_patterns\": [\"Any anti-patterns detected\"]
  },
  \"concerns\": [
    {
      \"area\": \"architecture|scalability|maintainability\",
      \"severity\": \"high|medium|low\",
      \"description\": \"Specific concern\",
      \"recommendation\": \"How to address it\"
    }
  ],
  \"blocking_issues\": [\"Issues that MUST be fixed\"],
  \"strengths\": [\"Positive aspects of the design\"]
}
\`\`\`

Focus on design quality. Only block for fundamental architecture flaws.
"
```

### Code Review (Phase 4)

```bash
gemini --yolo "
You are performing an architecture-focused code review of recently implemented changes.

Review the implementation for:
1. Architecture compliance - Does code match the plan?
2. Design pattern correctness - Are patterns implemented correctly?
3. Separation of concerns - Is responsibility properly divided?
4. Coupling and cohesion - Are modules appropriately connected?
5. Extensibility - Can this be easily extended?
6. Performance implications - Any obvious bottlenecks?

Also check:
- Code organization and structure
- Naming conventions and clarity
- Documentation adequacy
- Error handling patterns
- Resource management

Return your assessment as JSON (wrap in code block):
\`\`\`json
{
  \"agent\": \"gemini\",
  \"phase\": \"verification\",
  \"approved\": true|false,
  \"score\": 1-10,
  \"assessment\": \"Brief summary of code review\",
  \"architecture_compliance\": {
    \"matches_plan\": true|false,
    \"deviations\": [\"Any deviations from plan\"]
  },
  \"issues\": [
    {
      \"file\": \"path/to/file.py\",
      \"concern\": \"What's the issue\",
      \"severity\": \"high|medium|low\",
      \"category\": \"architecture|scalability|maintainability\",
      \"recommendation\": \"How to improve\"
    }
  ],
  \"blocking_issues\": [\"Critical architecture issues\"],
  \"quality_score\": {
    \"modularity\": 1-10,
    \"extensibility\": 1-10,
    \"maintainability\": 1-10
  }
}
\`\`\`

Be constructive. Focus on significant architecture concerns, not style nitpicks.
"
```

## Output Parsing

Gemini returns markdown with embedded JSON. Parse with:

```python
import re
import json

# Extract JSON from code block
match = re.search(r'```json\s*(.*?)\s*```', gemini_output, re.DOTALL)
if match:
    result = json.loads(match.group(1))
else:
    # Try to find raw JSON
    match = re.search(r'\{.*\}', gemini_output, re.DOTALL)
    if match:
        result = json.loads(match.group(0))
```

## Error Handling

### Timeout
- Default timeout: 300 seconds
- On timeout: Retry once with 600 seconds
- If still fails: Log and continue with warning

### Parse Error
- If no JSON found: Extract key points manually
- Create synthetic feedback from text analysis
- Mark as "parse_warning" in state

### Agent Unavailable
- If gemini not installed: Skip with warning
- Log to `logs` with type `escalation` or `blocker`
- Cursor alone can proceed for security-critical reviews

## Integration with Workflow

1. **Phase 2 (Validation)**:
   - Run in parallel with Cursor
   - Store output in `phase_outputs` as `gemini_feedback`
   - Weight: 0.7 for architecture concerns

2. **Phase 4 (Verification)**:
   - Run in parallel with Cursor
   - Store output in `phase_outputs` as `gemini_review`
   - Must approve for workflow to complete

## Approval Thresholds

| Phase | Min Score | Blocking Issues |
|-------|-----------|-----------------|
| Validation | 6.0 | None allowed |
| Verification | 7.0 | None allowed |

## Outputs

- JSON review payload for validation or verification phases.

## Example Usage

```bash
# From project directory
cd projects/my-app

# Run validation
gemini --yolo "Review the plan JSON provided in this prompt for architecture..."

# Parse the output (may need to extract JSON from markdown)
cat gemini-output.txt
```

## Conflict Resolution

When Gemini disagrees with Cursor:

| Issue Type | Resolution |
|------------|------------|
| Architecture concern | Gemini wins (weight 0.7) |
| Security concern | Cursor wins (weight 0.8) |
| Code quality | Average scores |
| Both blocking | Human escalation |

## Model Selection

```bash
# Use specific model
gemini --model gemini-2.0-flash --yolo "prompt"

# Available models
# - gemini-2.0-flash (default, fastest)
# - gemini-2.0-pro (more thorough)
```

## Related Skills

- `/validate` - Plan validation workflow
- `/verify` - Code review workflow
- `/resolve-conflict` - Merge Cursor and Gemini feedback
