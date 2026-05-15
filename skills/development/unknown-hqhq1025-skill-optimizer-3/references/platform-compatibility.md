# Platform Compatibility Notes

Use this when preparing public release copy or install instructions.

## Native Agent Skills Support

| Agent | Current support shape | Good default install path |
| --- | --- | --- |
| Codex | Native Agent Skills; skills are the workflow authoring format, while plugins are the installable distribution unit. Supports scripts, references, assets, and optional `agents/openai.yaml`. | `~/.codex/skills/` for user skills, `.agents/skills/` for repo-portable skills. |
| Claude Code | Native skills in personal, project, and plugin locations. Claude uses descriptions to decide when to apply a skill and supports Claude-specific metadata fields. | `~/.claude/skills/` for personal skills, `.claude/skills/` for project skills. |
| Cursor | Native Agent Skills alongside rules and commands. Project `.agents/skills/` and `.cursor/skills/` are the safest portable choices; global path behavior should be verified in the target Cursor version. | `.agents/skills/` for portable repo skills, `.cursor/skills/` for Cursor-specific repo skills, native global path for personal installs. |
| OpenCode | Native `skill` tool; discovers `.opencode/skills/`, `~/.config/opencode/skills/`, plus `.agents/skills/` and `.claude/skills/` compatibility paths. Skill loading can be governed with `skill` permissions (`allow`, `ask`, `deny`). | `.agents/skills/` for portable repo skills, `.opencode/skills/` for project-specific OpenCode skills, `~/.config/opencode/skills/` for global skills. |
| Gemini CLI / Google agents | Google publicly documents Agent Skills as an open format and announces installation into Gemini CLI via skill installers; Gemini CLI also uses `GEMINI.md` for always-on context. | `.agents/skills/` or installer-managed paths for skills; `GEMINI.md` for always-on project context. |

## Release Guidance

- Prefer `.agents/skills/<name>/SKILL.md` in public repos when the skill is meant to be portable across agents.
- Also mention platform-specific paths for users who want personal installs.
- Do not claim equal feature depth across agents. Discovery, metadata, permissions, and UI invocation differ.
- Keep frontmatter conservative: `name` and `description` are the safest cross-agent fields.
- Put agent-specific metadata in optional files, not in the shared `SKILL.md`.
- Cite public ecosystem examples and official docs only for the support level they actually demonstrate.
- For published packages, distinguish repo-portable skills from app-specific plugin packaging.
