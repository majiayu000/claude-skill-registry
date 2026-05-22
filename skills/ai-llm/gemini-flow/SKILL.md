---
name: gemini-flow
description: Google Gemini API integration and model orchestration
allowed-tools: [Bash, Read, WebFetch]
---

# Gemini Flow Skill

## Overview

Google Gemini API integration. 90%+ context savings.

## Requirements

- GOOGLE_API_KEY environment variable
- gemini-pro or gemini-pro-vision model access

## Tools (Progressive Disclosure)

### Generation

| Tool     | Description             |
| -------- | ----------------------- |
| generate | Generate text content   |
| chat     | Multi-turn conversation |
| embed    | Generate embeddings     |

### Vision

| Tool           | Description           |
| -------------- | --------------------- |
| analyze-image  | Analyze image content |
| describe-image | Describe image        |

### Models

| Tool        | Description            |
| ----------- | ---------------------- |
| list-models | List available models  |
| model-info  | Get model capabilities |

## Agent Integration

- **llm-architect** (primary): Model orchestration
- **model-orchestrator** (primary): Multi-model routing
- **developer** (secondary): API integration
