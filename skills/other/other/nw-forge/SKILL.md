---
name: nw-forge
description: "Creates new specialized agents using the 5-phase workflow (ANALYZE > DESIGN > CREATE > VALIDATE > REFINE). Use when building a new AI agent or validating an existing agent specification."
user-invocable: true
argument-hint: '[agent-name] - Optional: --type=[specialist|reviewer|orchestrator] --pattern=[react|reflection|router]'
---

# NW-FORGE: Create Agent (V2)

**Wave**: CROSS_WAVE
**Agent**: Zeus (nw-agent-builder)

## Overview

Create a new agent using research-validated v2 approach: focused core (200-400 lines) with Skills for domain knowledge.

1. **ANALYZE** — Identify single clear responsibility, check overlap with existing agents, classify type, determine minimum tools needed. Gate: responsibility defined, no overlap, classification chosen.
2. **DESIGN** — Select design pattern, define role and divergent principles, plan Skills extraction, draft frontmatter. Gate: pattern selected, principles drafted, frontmatter ready.
3. **CREATE** — Write agent `.md` using template. Workflow must be numbered task list. Create Skill files if domain knowledge exceeds 50 lines. Gate: agent file written, line count under 400.
4. **VALIDATE** — Run 14-point validation checklist. Check for anti-patterns. Verify workflow is numbered task list, not prose. Gate: all 14 items pass, zero anti-patterns.
5. **REFINE** — Address validation failures. Add instructions only for observed failure modes. Re-measure and re-validate. Gate: all items pass, line count reported.

## Agent Invocation

@nw-agent-builder

Execute \*forge to create {agent-name} agent.

**Configuration:**
- agent_type: specialist | reviewer | orchestrator
- design_pattern: react | reflection | router | planning | sequential | parallel | hierarchical

## Success Criteria

- [ ] Agent definition under 400 lines (`wc -l`)
- [ ] Official YAML frontmatter format (name, description, tools, maxTurns)
- [ ] 11-point validation checklist passes
- [ ] Only divergent behaviors specified (no Claude defaults)
- [ ] 3-5 canonical examples included
- [ ] Domain knowledge extracted to Skills if >50 lines
- [ ] No aggressive language (no CRITICAL/MANDATORY/ABSOLUTE)
- [ ] Safety via platform features (frontmatter/hooks), not prose

## Next Wave

**Handoff To**: Agent installation and deployment
**Deliverables**: Agent specification file + Skill files (if any)

## Expected Outputs

```
~/.claude/agents/nw/nw-{agent-name}.md
~/.claude/skills/nw-{skill-name}/SKILL.md*.md    (if Skills needed)
```
