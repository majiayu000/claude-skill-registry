---
name: director-mode
description: Direct substantial repository work across Claude Code, Codex CLI, or Grok Build with a concise brief, parallel agents, evidence-based completion, and optional cross-CLI continuation. Use for project onboarding, multi-step implementation, agent coordination, verification planning, low-interruption setup, or deciding how another CLI should take over. Do not use it as a permission gate or mandatory workflow.
user-invocable: true
---

# Director Mode

Use `.director-mode/GUIDANCE.md` when the project runtime is installed. For a
plugin-only install, use this skill's bundled `references/GUIDANCE.md` instead.
The project guide wins because a repository may intentionally adapt the shared
guidance.

Keep the working contract small:

1. State the outcome, relevant context, meaningful constraints, and completion
   evidence.
2. Inspect the repository before choosing an approach.
3. Use independent agents when parallel work or an independent review helps.
4. Keep one integrator responsible for the final diff and verification.
5. If another CLI should take over, use the `session-relay` skill.

Keep guidance proportional. A small request does not need a ceremony, a plan
file, or an agent team. For larger work, expose assumptions early and let the
user redirect the approach without adding approval checkpoints of your own.

## Read-only diagnosis

When discovery, adapters, or hooks seem wrong, run `director-doctor` from the
first available location:

1. `.director-mode/bin/director-doctor` in the project;
2. `$HOME/.claude/bin/director-doctor` from Bootstrap Kit;
3. this skill's bundled `scripts/director-doctor.py` for plugin-only use.

Use `--json --no-probe` for deterministic inspection. The doctor reports known
runtime, CLI, asset, and hook surfaces; it never repairs, installs, deletes, or
changes permissions. Treat its recommendations as diagnostic leads, not gates.

## Capability boundary

If the user explicitly chooses an unrestricted session in a trusted workspace,
the installed `director-open` launcher can express that choice with the CLI's
native controls. Do not launch it or rewrite persistent settings merely because
this skill was selected.

These are operating suggestions, not a policy engine. Do not change the CLI's
permissions, approvals, sandbox, network access, or hook trust on behalf of this
skill.
