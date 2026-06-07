---
name: gemini-native
description: "Run gemini native."
---

# gemini-native (Codex)

Codex-native entry point for the `gemini-native` operator skill.

The AgentOps source skill `../../skills/gemini-native/SKILL.md` is the source of truth
for domain behavior, commands, examples, references, and output expectations.
Read it first, then use `prompt.md` for the Codex runtime profile.

## Codex Runtime Contract

- Use Codex plus the local shell for this wrapper's execution.
- Treat Gemini CLI commands as target-runtime commands to inspect, configure, or dispatch deliberately.
- Load only the relevant source references or scripts for the task.
- Verify command syntax from local `gemini --help` or checked-in references before acting.
- Return concrete evidence: commands run, files touched, exit codes, and any remaining blocker.
