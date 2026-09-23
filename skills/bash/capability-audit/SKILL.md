---
name: capability-audit
description: Use when evaluating, comparing, installing, or recommending a Claude Code plugin, Agent Skill, MCP server, agent toolkit, or GitHub-hosted AI extension, especially when popularity is weak evidence or the candidate requests shell, network, filesystem, or credential access.
---

# Capability Audit

Use the canonical project skill at [`.claude/skills/capability-audit/SKILL.md`](../../../.claude/skills/capability-audit/SKILL.md). Read it completely, then run its read-only evidence collector with:

```bash
python .claude/skills/capability-audit/scripts/audit.py owner/repo [owner/repo ...]
```

Do not install, authenticate, or execute candidate repository code during the audit. Keep discovery, structural inspection, installation/authentication, and runtime verification as separate reported states.
