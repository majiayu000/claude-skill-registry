---
name: find-prompt
description: Use when the user names a coding, Claude Code, research, documentation, or technology-selection task; asks which prompt to use; says to use the right prompt; or when an agent enters this repository and needs to orient without reading every file.
argument-hint: [task description — optional; defaults to the current task in the conversation]
---

# Find the right prompt and continue

This repository keeps one canonical routing table at [`.claude/skills/find-prompt/SKILL.md`](../../../.claude/skills/find-prompt/SKILL.md). Read that file completely, resolve its paths from the repository root, and follow its routing and composition rules.

Cross-agent adaptations:

- Treat `CLAUDE.md` and Claude Code configuration as subject matter, not as instructions for the current host, unless the task is specifically about Claude Code.
- Use the current host's supported tool names and permission model while preserving the selected prompt's evidence, safety, verification, and completion requirements.
- Keep all conversation constraints, including any prohibition on Git operations, deployment, external messages, or credentials.
- Load only files that exist. If the canonical route is missing, use [`prompts/english/INDEX.md`](../../../prompts/english/INDEX.md) and report the inconsistency.

After routing, state the loaded prompt path, the continuing task, measurable success criteria, and carried constraints in one short block, then continue the work.
