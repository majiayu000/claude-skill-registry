---
name: ondevice-ml
description: Core ML integration + on-device pipelines (NLP/Vision/SoundAnalysis) with privacy/compliance guardrails.
allowed-tools: Read, Grep, Glob, Edit, Write
---

Load:
- @docs/ondevice-ml/README.md
- @docs/ondevice-ml/coreml.md
- @docs/ondevice-ml/deployment.md
- @docs/ondevice-ml/privacy.md

Output:
- Model I/O contract checklist
- Swift inference pipeline (caching, threading, error handling)
- Optional: Vision/NLP/SoundAnalysis scaffolds
- Test + validation plan
