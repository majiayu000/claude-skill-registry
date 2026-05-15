# Personalization Rubric

Use this rubric when adapting a skill for one user's local environment.

## 1. Evidence Sources

Prefer live evidence in this order:

1. The target `SKILL.md` and bundled files.
2. Installed copies in `~/.codex/skills`, `~/.agents/skills`, or `~/.claude/skills`.
3. Project-local `AGENTS.md`, `CLAUDE.md`, README, scripts, and package metadata.
4. Relevant memories or session summaries.
5. Recent shell history, repo commands, or logs when the user asks for operational tuning.

Do not invent personal habits when evidence is unavailable. State the assumption and keep the change conservative.

## 2. Trigger Fit

Collect examples of:

- User phrases that should trigger the skill.
- User phrases that currently trigger the wrong skill.
- Related tasks where this skill should stay silent.
- Local shorthand, repo nicknames, host nicknames, and language preferences.

Tune the frontmatter description so the first 250 characters include the strongest real triggers. Avoid stuffing unrelated keywords.

## 3. Local Defaults

Useful personalization may include:

- Default paths, repo roots, or install directories.
- Preferred CLIs, aliases, MCP tools, or browser tools.
- Expected verification commands.
- The user's communication style, autonomy preference, or review format.
- Local safety boundaries such as dirty-worktree handling, credential handling, remote-host checks, or deployment surfaces.

Keep these defaults explicit enough to execute, but not so narrow that the skill fails outside one repository.

## 4. Behavior Changes

For every behavior change, record:

- What upstream/default behavior was.
- What local behavior is now preferred.
- Why the user's evidence supports the change.
- How to verify the change with a realistic prompt.

This can be a short note in the skill body, a reference file, or the final report. Avoid noisy changelogs inside the skill unless the user requests one.

## 5. Validation Scenarios

Run at least three prompt-level checks mentally or with subagents when available:

| Scenario | Expected result |
| --- | --- |
| Direct trigger | The skill clearly applies. |
| Natural shorthand | The skill still applies. |
| Neighbor task | A different skill or no skill should apply. |

Also validate:

- YAML frontmatter parses.
- Referenced paths exist or are documented as user-specific.
- Commands mentioned are installed or clearly optional.
- The skill body remains concise and actionable.
