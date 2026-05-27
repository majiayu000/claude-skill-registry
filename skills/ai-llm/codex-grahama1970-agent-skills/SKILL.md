---
name: codex
description: >
  High-reasoning agentic bridge via OpenAI Codex CLI.
  Supports gpt-5.3-codex with optional reasoning effort.
  Use for complex analysis, code generation, and structured extraction.
allowed-tools: ["run_command", "read_file"]
triggers:
  - codex
  - reason
  - reasoning
  - gpt-5.3
  - high reasoning
metadata:
  short-description: High-reasoning agentic bridge (gpt-5.3-codex)
provides:
  - llm-completion
composes: [, task-monitor]

taxonomy:
  - inference
  - reasoning
  - llm
---

# Codex Skill

Bridge to the **OpenAI Codex CLI** for high-reasoning tasks using `gpt-5.3-codex`.

## Features

1.  **High Reasoning**: Leverages `gpt-5.3-codex` with configurable reasoning effort (default: high).
2.  **Structured Output**: Supports JSON Schema for guaranteed output shapes.
3.  **Automatic OAuth**: Uses the existing `codex` CLI authentication.
4.  **Sandbox Aware**: Runs within the Codex sandbox policy if requested.

## Usage

### Simple Reasoning

```bash
./run.sh reason "Explain the relationship between CAPEC and ATT&CK"
```

### Structured Extraction

```bash
./run.sh extract "Find all entities in this text" --schema entities.json
```

### Direct CLI Access

```bash
# Pass prompts via stdin for complex multi-line tasks
echo "Analyze this code" | ./run.sh exec --model gpt-5.3-codex
```

## Integration with Dogpile

The `dogpile` skill uses this skill for:

1.  **Ambiguity Checks**: High-reasoning analysis of user intent.
2.  **Synthesis**: Consolidating search results from multiple sources into a coherent report.
