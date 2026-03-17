---
name: ask-council
description: Multi-model ensemble consultation. Runs 3 models in parallel for diverse perspectives.
---

Consult multiple models in parallel about: $ARGUMENTS

---

Use the Task tool with `subagent_type='consultant:consultant'`. Specify multi-model consultation.

**Default models** (use all 3 unless user specifies otherwise):
- `gpt-5.2-pro`
- `gemini/gemini-3-pro-preview`
- `claude-opus-4-5-20251101`

The agent handles parallel execution, polling, and output relay.
