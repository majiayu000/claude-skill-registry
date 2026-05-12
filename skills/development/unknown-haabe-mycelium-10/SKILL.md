---
name: canvas-update
description: "Update canvas sections with new evidence. Ensures canvas stays current as the single source of truth."
instruction_budget: 12
---

# Canvas Update

## Preflight: Read target canvas file(s) before any Write/Edit

**Hard rule.** Before issuing `Write` or `Edit` against any `.claude/canvas/*.yml`, use the **Read tool** on that file in this session. Claude Code's Read-before-Write check requires the `Read` tool specifically — `cat`/`head`/`grep` via Bash do NOT satisfy it. Reaching for `Write` first produces a tool error and forces a remedial Read, which costs ~14k tokens of pure ceremony at typical canvas sizes (anti-pattern #7 instance #5, 2026-05-09).

If this skill writes to multiple canvas files, Read each one first. If unsure whether a write is needed, Read first anyway — Read is cheap, the recovery loop is not.

See `CLAUDE.md` *Canvas writes — Read before Write* for the canonical rule.

## Rules
1. **Never update without evidence** -- every canvas change must have a source
2. **Maintain cross-file consistency** -- if you update opportunities.yml, check if north-star.yml or gist.yml need updates too
3. **Log the update** -- add an entry to .claude/harness/decision-log.md explaining what changed and why

## Which Canvas File for Which Information

| Information Type | Canvas File | Source |
|-----------------|-------------|--------|
| Purpose, mission, why | purpose.yml | Sinek |
| North Star metric, inputs | north-star.yml | North Star Framework |
| BVSSH health scores | bvssh-health.yml | Smart |
| Value chain, competitive | landscape.yml | Wardley |
| Team structure | team-shape.yml | Skelton |
| User opportunities, OST | opportunities.yml | Torres |
| User needs map | user-needs.yml | Allen |
| Goals, ideas, steps | gist.yml | Gilad |
| Service quality scores | services.yml | Downe |
| Go-to-market, positioning | go-to-market.yml | Lauchengco |
| Delivery performance | dora-metrics.yml | Forsgren |
| Security threats | threat-model.yml | OWASP |
| Privacy assessment | privacy-assessment.yml | GDPR/PbD |
| Trust architecture | trust-signals.yml | Digital Trust |
| Jobs to be done | jobs-to-be-done.yml | Christensen |
| Bounded contexts | bounded-contexts.yml | Evans (DDD) |
| Value stream map | value-stream.yml | Rother & Shook (VSM) |
| Content delivery metrics | content-metrics.yml | v0.11.0 |
| AI tool delivery metrics | ai-tool-metrics.yml | v0.11.0 |
| Service delivery metrics | service-metrics.yml | v0.11.0 |
| Human task tracking | human-tasks.yml | v0.11.0 |
| Archived/discarded solutions | archived-solutions.yml | v0.12.0 |
| Leaf lifecycle calibration | cycle-history.yml | v0.12.0 |
| Adaptive thresholds | thresholds.yml | v0.12.0 |
| User scenarios (Hoskins) | scenarios.yml | Hoskins |

## Workflow
1. Identify which canvas file(s) need updating
2. Read current state
3. Make the update with evidence citation
4. Check cross-file consistency
5. Log in .claude/harness/decision-log.md

## Counter-Argument Check (Bias Mitigation)

Before applying the canvas update, draft a one-line counter-argument: *"What's the strongest case AGAINST this update — what evidence or perspective would invalidate it?"* If you can't articulate one, run `/mycelium:devils-advocate` before proceeding.

This addresses the bias cluster documented in corrections.md (L5 sycophancy 2026-04-20, eval overfitting 2026-04-30, sharper-framing-isn't-righter 2026-05-03). Common shape: agent prefers what feels right over what evidence supports under competing pressure (be helpful vs. be honest, sharpen framing vs. preserve evidence base). The counter-argument step forces the missing perspective explicit, so the bias surfaces before it lands in canvas.

Especially important when interpolating user-supplied content (already untrusted per ${CLAUDE_PLUGIN_ROOT}/harness/security-trust.md#prompt-injection-defense) AND when increasing a confidence value — both contexts where the agent is most likely to default toward the optimistic read.
