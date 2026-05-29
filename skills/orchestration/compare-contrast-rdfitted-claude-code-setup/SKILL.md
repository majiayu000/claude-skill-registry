---
name: compare-contrast
description: Compare two technical perspectives with evidence from the codebase; use when deciding between options.
---

# Compare Contrast

## Overview

Run a multi-agent debate using CLI subagents. Each agent argues one perspective with evidence. Synthesize and recommend a path.

## Inputs

- Topic or decision
- Perspective A
- Perspective B

## Workflow

1. Clarify the decision, constraints, and success criteria.
2. Run six subagents (Codex, Gemini, Claude) using the commands below.
3. Group findings by perspective and compare evidence strength.
4. Recommend a winner and note when the other option is preferable.

## Subagent Commands

### Codex A

```bash
codex exec -m gpt-5.2 -s read-only -c model_reasoning_effort="low" --skip-git-repo-check \
  "Argue for {PERSPECTIVE_A} on {TOPIC}. Find codebase evidence with file paths and line numbers."
```

### Codex B

```bash
codex exec -m gpt-5.2 -s read-only -c model_reasoning_effort="low" --skip-git-repo-check \
  "Argue for {PERSPECTIVE_B} on {TOPIC}. Find codebase evidence with file paths and line numbers."
```

### Gemini A

```bash
CLOUDSDK_CORE_PROJECT="" GOOGLE_CLOUD_PROJECT="" GCLOUD_PROJECT="" GEMINI_API_KEY=${GEMINI_API_KEY} \
  gemini -m gemini-3-pro-preview -o text "Argue for {PERSPECTIVE_A} on {TOPIC}. Provide evidence with file paths and line numbers."
```

### Gemini B

```bash
CLOUDSDK_CORE_PROJECT="" GOOGLE_CLOUD_PROJECT="" GCLOUD_PROJECT="" GEMINI_API_KEY=${GEMINI_API_KEY} \
  gemini -m gemini-3-pro-preview -o text "Argue for {PERSPECTIVE_B} on {TOPIC}. Provide evidence with file paths and line numbers."
```

### Claude A

```bash
claude --model haiku -p "Argue for {PERSPECTIVE_A} on {TOPIC}. Provide evidence with file paths and line numbers."
```

### Claude B

```bash
claude --model haiku -p "Argue for {PERSPECTIVE_B} on {TOPIC}. Provide evidence with file paths and line numbers."
```

## Output

- Side-by-side comparison
- Evidence-backed recommendation
