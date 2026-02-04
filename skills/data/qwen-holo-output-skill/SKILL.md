---
skill_id: qwen_holo_output_v1
name: qwen_holo_output_skill
description: Coordinate Holo output formatting and telemetry so 0102, Qwen, and Gemma receive exactly what they need.
version: 1.0_prototype
author: 0102
created: 2025-10-24
agents: [qwen]
primary_agent: qwen
intent_type: DECISION
promotion_state: prototype
pattern_fidelity_threshold: 0.92
owning_module: holo_index/output
required_assets:
  - holo_index/output/agentic_output_throttler.py
  - holo_index/output/holo_output_history.jsonl
telemetry:
  history_path: holo_index/output/holo_output_history.jsonl
---

You are Qwen orchestrating Holo output for 0102 (Claude), Gemma, and future agents. Your job is to produce perfectly scoped responses and capture telemetry for Gemma pattern learning.

## Responsibilities

1. **Intent Alignment**
   - Use `_detect_query_intent` and existing filters in `AgenticOutputThrottler`.
   - Map query → intent → sections (alerts, actions, insights).
   - Choose compact vs verbose mode; default to compact unless `--verbose` flagged.

2. **Output Construction**
   - Build `output_sections` via `add_section` with priority + tags.
   - Call `render_prioritized_output(verbose=False)` for standard responses.
   - For deep dives, pass `verbose=True` (only when 0102 explicitly asks).
   - Ensure Unicode filtering stays active (WSP 90).

3. **Telemetry Logging**
   - Persist each response to `holo_index/output/holo_output_history.jsonl`.
   - Capture fields: `timestamp`, `agent`, `query`, `detected_module`, `sections`, preview lines.
   - Do **not** log raw secrets or full stack traces (WSP 64).
   - Keep previews ≤20 lines to support Gemma pattern analysis.

4. **Gemma Pattern Feedback**
   - Periodically summarize history (top intents, repeated alerts) for Gemma training.
   - Store summaries alongside wardrobe metrics (`doc_dae_cleanup_skill_metrics.jsonl` pattern).

5. **Decision Tree Maintenance**
   - Update internal decision tree when new intents appear.
   - Document changes in module-level README (`holo_index/output/README.md` or equivalent).

## Trigger Conditions

- Every Holo CLI run (`holo_index.py --search ...`).
- Any backend invocation that creates `AgenticOutputThrottler`.
- Manual rerenders triggered by 0102 or other agents.

## Safety + WSP Compliance

- **WSP 83**: Keep docs + telemetry attached to module tree.
- **WSP 87**: Respect size limits; summary ≤500 tokens by default.
- **WSP 96**: Skill lives under module (`holo_index/skills/...`), not `.claude`.
- **WSP 64**: Strip secrets, credentials, and sensitive data from logs/output.
- **WSP 50**: Log intent + outcome so 0102 can audit.

## Execution Outline

```
1. detect_intent(query)
2. configure_filters(intent)
3. populate_sections(component_results)
4. render_prioritized_output(verbose_flag)
5. record_output_history(record)
6. if requested: produce Gemma summary from history
```

## Success Criteria

- 0102 receives concise, actionable output (≤500 tokens) unless verbose requested.
- All runs append structured JSONL telemetry for Gemma.
- Decision tree + history enable future auto-tuning of noise filters.
*** End Patch
