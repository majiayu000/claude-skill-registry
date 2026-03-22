---
name: ai-create
description: "Use when creating a new skill or agent for the ai-engineering framework, with TDD-based pressure testing and CSO-optimized descriptions."
effort: high
argument-hint: "skill <name>|agent <name>"
---


# Create

## Purpose

Create new skills and agents for the ai-engineering framework using TDD. Skills go through a pressure-test cycle (RED/GREEN/REFACTOR) to ensure they actually change agent behavior. Agents are scaffolded with mandate, self-challenge protocol, and capability declarations.

## Trigger

- Command: `/ai-create skill <name>` or `/ai-create agent <name>`
- Context: framework needs a new capability that no existing skill or agent covers.

## Modes

### skill <name> -- Create a new skill

**Phase RED -- Baseline without the skill**:

1. **Define test scenarios** -- write 3-5 prompts that the skill should handle. These are the "pressure tests."
2. **Run baseline** -- execute the prompts WITHOUT the new skill loaded. Record how the agent behaves.
3. **Identify gaps** -- document specific failures: wrong approach, missed steps, bad output format, skipped governance.

**Phase GREEN -- Write minimal skill**:

4. **Scaffold** -- create `.claude/skills/ai-{name}/SKILL.md` with frontmatter:
   ```yaml
   ---
   name: ai-{name}
   description: "{CSO-optimized: Use when [triggering conditions]}"
   argument-hint: "{expected arguments}"
   ---
   ```
5. **Write skill body** -- address ONLY the gaps found in RED phase. Include:
   - Purpose (2-3 lines)
   - Trigger (command + context)
   - Procedure (numbered steps)
   - When NOT to Use (differentiation from similar skills)
6. **CSO-optimize description** -- the `description` field is the skill's search ranking. It must describe triggering conditions, not summarize what the skill does. Pattern: "Use when [specific situation the user is in]".
7. **Run pressure tests again** -- verify the skill changes behavior for all test scenarios.

**Phase REFACTOR -- Close loopholes**:

8. **Test edge cases** -- try prompts that should NOT trigger this skill. Verify they do not.
9. **Add guardrails** -- if edge-case prompts incorrectly triggered the skill, add "When NOT to Use" entries.
10. **Final validation** -- all pressure tests pass, no false triggers.

### agent <name> -- Create a new agent

1. **Define mandate** -- what is this agent's singular responsibility? An agent does ONE thing.
2. **Scaffold** -- create `.claude/agents/ai-{name}.md` with:
   - Identity (role, experience level, specialization)
   - Mandate (what it owns, what it does not own)
   - Capabilities (declared permissions: read-only, read-write, which files/paths)
   - Behavior (modes, procedures)
   - Boundaries (hard limits, escalation protocol)
   - Self-challenge protocol (questions the agent asks itself before acting)
3. **Register** -- add to `manifest.yml` agents section.
4. **Create skill entry point** -- create matching `/ai-{name}` skill that activates the agent.

## Registration Checklist

After creating any skill or agent:

- [ ] File created at correct path
- [ ] Frontmatter has `name`, `description`, `argument-hint`
- [ ] Description is CSO-optimized (triggering conditions, not summary)
- [ ] Registered in `manifest.yml`
- [ ] Mirror files created for other IDE surfaces (`.agents/`, `.github/prompts/`)
- [ ] No overlap with existing skills (checked `/ai-find` or skill list)

## CSO Description Patterns

| Bad (summary) | Good (CSO trigger) |
|---------------|-------------------|
| "Generates standup notes" | "Use when preparing daily standup notes or summarizing recent PR activity" |
| "Sprint planning tool" | "Use when planning a new sprint or running a retrospective" |
| "Resolves git conflicts" | "Use when git reports merge conflicts during rebase, merge, or cherry-pick" |

## Quick Reference

```
/ai-create skill standup     # create a new standup skill with TDD
/ai-create agent reviewer    # create a new reviewer agent
```

## Integration

- **Calls**: `handlers/create-skill.md`, `handlers/create-agent.md`, `handlers/validate.md`
- **Triggers sync**: `python scripts/sync_command_mirrors.py` after creation

$ARGUMENTS
