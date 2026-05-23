---
name: skill-miner
description: Use when mining coding-agent session history, archived transcripts, memories, or repeated local work to discover recurring workflows that should become new Agent Skills.
---

# Skill Miner

## Overview

Mine real agent usage for new skill opportunities. The goal is to find repeated workflows, extract the reusable technique, and turn strong candidates into draft skills with evidence.

## When To Use

- A user wants to scan past coding-agent sessions for repeated workflows.
- The user suspects they keep asking agents to do similar tasks manually.
- A team wants a backlog of candidate skills based on actual work rather than brainstorming.
- Existing memories, session logs, or project notes contain recurring procedures that have not been packaged.

Do not use to tune an existing skill; use `skill-personalizer`. Do not use to publish a private skill publicly; use `skill-generalizer`.

## Workflow

1. Locate real evidence: session JSONL, memory summaries, repo notes, repeated scripts, and recent project folders.
2. Run `scripts/scan_sessions.py` for a first-pass sanitized cluster report when local session files or exported transcripts are available.
3. Cluster repeated work by intent, trigger phrasing, tools used, files touched, and verification pattern.
4. Filter out one-off tasks, ordinary coding knowledge, and project-specific instructions better suited for `AGENTS.md`.
5. Score candidates by recurrence, friction, risk, portability, and future value.
6. For each strong candidate, draft a concise skill name, trigger description, workflow outline, bundled-resource needs, and validation prompts.
7. Recommend whether each candidate should stay personal, become a public skill via `skill-generalizer`, or be skipped.
8. If the user asks to proceed, create the selected skill folders and verify frontmatter/layout.

## Evidence Rules

- Quote or summarize enough source evidence to justify each candidate.
- Do not expose sensitive transcript content unless the user explicitly asks for raw evidence.
- Avoid turning every repeated task into a skill; prefer workflows where guidance changes future behavior.
- Treat broad intent clusters as navigation hints, not skill drafts.
- Check sampled positives and near misses before trusting a regex-based workflow candidate.
- If session access is incomplete, label findings as partial and list what was scanned.

## References

Read [discovery-rubric.md](references/discovery-rubric.md) before doing a full session-history scan or creating candidate skill drafts.

Use `scripts/scan_sessions.py --help` for the deterministic scanner. It supports native Codex/Claude/Gemini-style local evidence, `--export` inputs for other agents, and `--patterns` for personalized workflow definitions. Treat its output as evidence for review, not as an automatic decision to create skills.
