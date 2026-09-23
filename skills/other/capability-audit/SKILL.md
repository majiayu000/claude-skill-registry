---
name: capability-audit
description: Use when evaluating, comparing, installing, or recommending a Claude Code plugin, Agent Skill, MCP server, agent toolkit, or GitHub-hosted AI extension, especially when popularity is weak evidence or the candidate requests shell, network, filesystem, or credential access.
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/audit.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py *)
---

# Capability Audit

## Purpose

Collect comparable evidence about GitHub-hosted agent capabilities before installation. The bundled script uses the GitHub API without cloning a repository. It reports maintenance metadata, license, distribution files, executable surfaces, test signals, and high-risk text patterns. It does not install, authenticate, or declare a project safe.

## Workflow

1. Convert each candidate to `owner/repo` or a GitHub repository URL.
2. Run the script for all credible candidates, not only the popularity leader:

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/audit.py owner/repo another/repo
   ```

3. Read the exact pinned commit or package that would be installed. The script inspects the current default branch only; say so explicitly.
4. Open every discovered plugin manifest, `SKILL.md` frontmatter, hook, MCP configuration, and executable script before recommending installation.
5. Compare candidates using task fit, blast radius, runtime proof, maintenance, interoperability, rollback, documentation, and adoption. Cap adoption at 5% of the decision.
6. Report four states separately: discovered, structurally inspected, installed/authenticated, and runtime-tested.

Use `--json` for machine-readable output and `--token-env NAME` only when an existing GitHub token environment variable is needed for rate limits. Never paste a token into the command.

## Interpretation rules

- A clean report means only that no configured heuristic fired.
- Stars are context, not a quality score.
- Recent pushes can be automated noise; inspect the changed content.
- Missing `SECURITY.md` is a review signal, not proof of insecurity.
- Marketplace inclusion and pinned SHAs improve provenance but do not establish runtime safety.
- Hooks, MCP servers, `allowed-tools`, install scripts, and downloaded binaries define the effective trust boundary.
- The official MCP reference servers are teaching implementations; evaluate production hardening independently.

## Additional resource

Read [`ecosystem-discovery-guide.md`](../../../prompts/english/workflows/ecosystem-discovery-guide.md) for the source order, weighted scorecard, research seeds, and installation gate.

## Remember

> Inspect the artifact you will execute, at the version you will execute—not the reputation of its repository.
