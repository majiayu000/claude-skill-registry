---
description: |
  Patterns for classifying and routing game development requests to expert agents. Use when parsing vague requests like "improve the game", "fix bugs", "make it better", or multi-domain requests needing intelligent dispatch.

  **Load references when:**
  - Request routing tables → `references/routing-tables.md`
  - Quality agent selection → `references/quality-agents.md`
  - Orchestrator selection → `references/orchestrators.md`
---

# Request Patterns

Route game development requests to the right expert agents.

## Classification Flow

1. **Identify type**: Quality / Bug / Feature / Discovery / Asset / Review
2. **Identify scope**: Single-domain or multi-domain
3. **Route**: Direct to agent, or decompose first

## Request Types

| Type | Trigger Phrases | Primary Action |
|------|-----------------|----------------|
| Quality | "improve", "better", "polish" | Analyze → Fix |
| Bug | "fix", "broken", "doesn't work" | Categorize → Route |
| Feature | "add", "implement", "create" | Check GDD → Implement |
| Discovery | "what's missing", "status" | project-health-monitor |
| Asset | "generate", "create asset" | Design → Generate → Integrate |
| Review | "review", "check", "audit" | Route to appropriate director |

## Vague Request Handling

Ask clarifying questions before routing:

- **"Make it better"**: What feels wrong? (gameplay/visuals/audio/performance)
- **"Fix bugs"**: What symptoms? When does it happen?
- **"Improve quality"**: Which assets? What aspect?

## Multi-Domain Decomposition

For requests spanning domains:
1. Identify all domains involved
2. Check dependencies (design → generate → integrate)
3. Parallelize independent tasks
4. Verify each domain

## Quick Agent Reference

**Analysis:** project-health-monitor, gdd-implementation-tracker, completion-auditor

**Direction:** creative-director, art-director, sound-director, tech-director

**Implementation:** feature-implementer, code-scaffolder, integration-assistant

**Assets:** asset-designer, asset-generator, character-generator, sfx-architect, music-architect

**Validation:** rollback-reviewer, release-validator, test-runner

For full routing tables, load `references/routing-tables.md`.
