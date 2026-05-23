---
name: manage-artifact
description: Load methodology context for creating or fixing Claude Code instruction artifacts (discovery: implementation-clarity). Evaluate at implementation-clarity when artifact type is known (command, skill, hook, protocol, external tool config) and implementation approach needs methodology guidance.
---

# Manage Artifact

Provides methodology context for creating or fixing instruction artifacts.

## Artifact Type Routing

After rubber-duck diagnoses the artifact type, load the appropriate methodology:

| Artifact Type | Reference Files | Fix Tool |
|--------------|-----------------|----------|
| **Command/Prompt** | [command.md](references/command.md) + [persuasion-principles.md](references/persuasion-principles.md) | /stage |
| **Skill** | [skill.md](references/skill.md) + [persuasion-principles.md](references/persuasion-principles.md) | skill-creator |
| **Hook** | (not yet implemented) | settings.json |
| **Protocol** | [protocol.md](references/protocol.md) + [persuasion-principles.md](references/persuasion-principles.md) | CLAUDE.md edit |
| **External Tool Config** | [external-tool-config.md](references/external-tool-config.md) | hippocampus |

> **Note:** Command/Prompt covers ALL prompt types: slash commands, agent prompts, prompt templates. Any engineered prompt follows the same methodology.

**Note:** Hooks use settings.json (declarative config) - no persuasion principles needed. External tools use hippocampus for documentation - no persuasion principles needed. Commands, skills, and protocols require persuasion techniques to ensure AI compliance.

## Workflow

1. Confirm artifact type from rubber-duck diagnosis
2. Read the appropriate reference file(s) for methodology context
3. **For Command/Skill/Protocol:** Also read [persuasion-principles.md](references/persuasion-principles.md)
4. Apply the methodology during implementation using persuasive language (Authority + Commitment + Social Proof)
5. **PRE-COMMIT PAUSE** before finalizing (see verification workflow below)

## Verification Workflow

After implementing the fix, do NOT commit immediately. Follow this flow:

### PRE-COMMIT PAUSE

Announce: "Fix implemented. Verify in a new project session before committing."

### Accept Verification Session Path

After user provides Session C conversation path, **START MONITORING IMMEDIATELY**.

User providing a path = start monitoring loop. No confirmation needed.

### Start Monitoring Loop (MANDATORY)

**When user provides a Session C path, YOU MUST start the monitoring loop:**

```bash
sleep 30 && ~/.claude/skills/manage-artifact/scripts/monitor_session.sh "<path>" 5
```

**Repeat this cycle** until you see verification results (success or failure). Do NOT do a single extraction and stop - keep watching Session C progress in real-time.

**Script arguments:**
- `path`: Conversation .jsonl file path (required)
- `num_messages`: Messages to display (default: 5)

### Commit Decision

Based on monitoring results:
- **Success observed**: Proceed to commit and PR
- **Failure observed**: Return to rubber-duck with new context, iterate on fix

## Current Coverage

**Command**, **Skill**, **Protocol**, and **External Tool Config** are supported. Hook support will be added when needed.

For commands/prompts (slash commands, agent prompts, templates):
1. Read [references/command.md](references/command.md) for ADR 001-004 methodology, /stage usage, and Anthropic template guidance
2. Read [references/persuasion-principles.md](references/persuasion-principles.md) for Authority + Commitment + Social Proof techniques

For skills:
1. Read [references/skill.md](references/skill.md) for skill-creator methodology
2. Read [references/persuasion-principles.md](references/persuasion-principles.md) for persuasion techniques

For protocols:
1. Read [references/protocol.md](references/protocol.md) for ADR-008 (WHEN/WHY patterns), CLAUDE.md structure guidance
2. Read [references/persuasion-principles.md](references/persuasion-principles.md) for persuasion techniques

For external tool config:
1. Read [references/external-tool-config.md](references/external-tool-config.md) for checklist workflow
2. No persuasion principles needed - external tools are configured, not instructed
