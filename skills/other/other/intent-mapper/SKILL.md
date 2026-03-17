---
name: intent-mapper
description: >
  Intent classification and mapping for natural language commands.
  Uses unsloth/transformers for ML-based intent detection with ArangoDB storage.
triggers:
  - map intent
  - classify intent
  - intent mapping
  - intent detection
metadata:
  short-description: ML intent classification and mapping

provides:
  - intent-mapper
composes:
  - task-monitor
---

# Intent Mapper

Classifies natural language inputs into structured intents using fine-tuned models.

## When to Use

- Mapping user utterances to skill actions
- Training or evaluating intent classifiers
- Building intent taxonomies

## CLI

```bash
python main.py --name "query text"
```
