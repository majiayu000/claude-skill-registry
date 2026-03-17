---
name: localsetup-agentic-prd-batch
description: "Agentic PRD batch: when user says 'process PRDs' or 'run batch from PRD folder'; implement per spec; update status; write outcome; reference PRD schema + external-agent guide. Use when editing .agent/queue/**, prds/**, *.prd.md."
metadata:
  version: "1.2"
---

# Agentic PRD batch

When the user says **process PRDs**, **run batch from PRD folder**, **process the queue**, or similar, or when editing files in `.agent/queue/` with intent to implement:

1. **Locate specs:** Look for PRD/spec files in the configured path (e.g. `.agent/queue/` or path from config). Exclude README, INDEX, SPEC-TEMPLATE. Filter by front matter `status == ready` (or `in-progress` if resuming). Sort by priority (high first), then filename date (oldest first).
2. **Implement per spec:** Load each spec; follow Implementation steps and Acceptance criteria; satisfy Verification plan and Rollback plan. Use PRD schema and [_localsetup/docs/PRD_SCHEMA_EXTERNAL_AGENT_GUIDE.md](../../docs/PRD_SCHEMA_EXTERNAL_AGENT_GUIDE.md) for format and outcome template.
3. **Update status:** Set spec `status: in-progress` when starting; set `status: done` (or `blocked`) when finished. Update queue INDEX if present.
4. **Write outcome:** Append outcome block per spec (e.g. `## Outcome` or platform-specific section name, and/or `aq_outcome` YAML) with branch, commit SHA, files changed, verification, rollback command. See PRD_SCHEMA_EXTERNAL_AGENT_GUIDE for template.
5. **Clean-tree invariant:** Before marking a spec done, ensure repo is clean (no modified tracked files except intended commits; untracked queue specs allowed). Commit or revert as needed.
6. **External confirmation:** If spec front matter includes `external_confirmation: acknowledged` or `impact_review: confirmed_by: external_agent`, agent may skip human impact confirmation; otherwise follow guardrails (impact summary + user confirmation for big/destructive changes).

## Reference

- [_localsetup/docs/AGENTIC_AGENT_Q_PATTERN.md](../../docs/AGENTIC_AGENT_Q_PATTERN.md)  - queue pattern.
- [_localsetup/docs/PRD_SCHEMA_EXTERNAL_AGENT_GUIDE.md](../../docs/PRD_SCHEMA_EXTERNAL_AGENT_GUIDE.md)  - spec format, front matter, outcome template, clarification protocol.
