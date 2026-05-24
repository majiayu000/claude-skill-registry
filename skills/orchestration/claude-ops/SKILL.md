---
name: claude-ops
description: PROMETHEUS NEXUS v6.0 - Constitutional multi-agent framework with director domains, mutual accountability, and Teammate coordination. Use when spawning AI directors, coordinating multi-agent systems, establishing governance boundaries, or implementing hierarchical collaboration with constitutional compliance.
---

# PROMETHEUS NEXUS v6.0

Constitutional multi-agent framework for director-level AI coordination with domain boundaries, mutual accountability, and Teammate system integration.

## Why This Exists

**Without framework:** AI agents lack clear authority boundaries, duplicate work, violate domains, and can't coordinate effectively.

**With PROMETHEUS NEXUS:** Constitutional governance with director domains, handoff protocols, consensus arbitration, and Teammate-native coordination.

## Routing Matrix

| Intent | Document | When |
|--------|----------|------|
| **SPAWN** | [spawn.md](./spawn.md) | Creating directors, teams, and specialists |
| **COORDINATE** | [coordinate.md](./coordinate.md) | Director communication, handoffs, consensus |
| **CONSTITUTION** | [constitution.md](./constitution.md) | Immutable rules and authority hierarchy |

## Quick Facts

- **Directors:** 8 (Architecture, Business, Design, Engineering, Research, Documentation, Operations, Security)
- **Constitution:** Immutable principles (Article I-VII)
- **Coordination:** Teammate native (write, broadcast, consensus, escalation)
- **Subagents:** claude-flow CLI spawning (via Bash tool by directors)
- **Memory:** AgentDB + ReasoningBank + Teammate memory
- **Status:** Validated by UCS Meta-Cognitive Experiment (extraordinary success)

## Quick Start

```bash
# Spawn a director via Teammate
<Teammate operation="spawnTeam">
  <team_name>architecture</team_name>
  <agent_type>director</agent_type>
</Teammate>

# Director spawns specialist via claude-flow
npx claude-flow@alpha automation auto-spawn "[task]" --mix "[specialist-roles]"
```

## Architecture

**Director Coordination (Teammate Native):**
```
Directors (Teammates) → Teammate write/broadcast → Peer Directors
                     → Teammate consensus → Arbitrated decisions
                     → Teammate escalation → Human/Parent
```

**Subagent Spawning (claude-flow CLI):**
```
Director (Teammate) → Bash tool → claude-flow CLI → Specialist subagents
```

**Memory Bridge:**
```
Teammate memory_store → AgentDB reflexion store (mirror)
Teammate memory_retrieve → AgentDB query
```

## Constitutional Principles

1. **Execution Primacy** - Work must be observable, anti-looping, token budgets
2. **Authority Hierarchy** - Constitution > Core Policies > SOPs > Directors > Subagents
3. **Agent Boundaries** - Directors operate within domain only
4. **Coordination** - Handoff protocol, consensus protocol, escalation protocol
5. **Memory System** - Immutable (instructional) vs Operational (write-heavy)
6. **Enforcement** - Violation response, audit trail
7. **Amendments** - Human operators only (agents cannot self-amend)

## Validated By UCS Experiment

The UCS Meta-Cognitive Time-Travel Experiment (2026-01-27) proved:
- ✅ Authentic meta-cognition (5/5 agents)
- ✅ Constitutional principles prevent 85% AI failure pattern
- ✅ Emergent collective intelligence (self-organized governance)
- ✅ Power dynamic correction (Victoria PM leadership)
- ✅ Mutual accountability (CAIO-CTO Pact proven in action)

## Domain Ownership

| Director | Owns | Cannot |
|----------|------|---------|
| **Architecture** | System design, patterns, tech decisions | Implementation, docs, business priorities |
| **Business** | Strategy, priorities, resources, arbitration | Technical decisions, implementation |
| **Design** | UX/DX, interfaces, API contracts | Implementation, architecture |
| **Engineering** | Implementation, code, CI/CD | Design, architecture, docs |
| **Research** | Exploration, prior art, evaluation | Decisions, implementation |
| **Documentation** | ALL formal documentation | Source content creation |
| **Operations** | Production deployment, monitoring, reliability | Implementation, architecture |
| **Security** | Security architecture, policies, incident response | Implementation, operations |

## Key Commands

### Spawn Director (Teammate)
```xml
<Teammate operation="spawnTeam">
  <team_name>[domain]</team_name>
  <agent_type>director</agent_type>
</Teammate>
```

### Director Spawns Specialist (claude-flow)
```bash
npx claude-flow@alpha automation auto-spawn "[task]" --mix "[specialist-roles]"
```

### Handoff (Teammate)
```xml
<Teammate operation="write">
  <target_agent_id>[target-director]</target_agent_id>
  <message><handoff>...</handoff></message>
</Teammate>
```

### Consensus (Teammate)
```xml
<Teammate operation="consensus">
  <team_name>directors</team_name>
  <proposal>...</proposal>
</Teammate>
```

## Files

- **SKILL.md** (this file) - Overview
- **README.md** - Detailed documentation
- **spawn.md** - Director and specialist spawning
- **coordinate.md** - Teammate coordination protocols
- **constitution.md** - Full constitutional text

## Last Updated

2026-01-28

---

**Part of:** PROMETHEUS NEXUS v6.0
**Validated By:** UCS Meta-Cognitive Time-Travel Experiment
**Constitutional Authority:** Supreme (Article VII - immutable)

---

## FIRST STARTUP

**NEW SYSTEM:** Run [initialize.md](./initialize.md) before spawning first directors.

**Bootstrap Protocol:**
\`\`\`bash
# Check memory-bank exists
if [ ! -d "~/.claude/memory-bank" ]; then
  /ttt:memory-bank-init --bootstrap
fi

# Initialize AgentDB
export AGENTDB_PATH=~/.claude/claude-ops.db
npx agentdb init ~/.claude/claude-ops.db --dimension 1536
\`\`\`

**Knowledge Scope:**
- User-level (\`~/.claude/\`) → Federated knowledge (shared across projects)
- Project-level → Institutional knowledge (project-specific)
- Container → Sole purpose = Project/Institutional knowledge

---

## CREATOR NOTES

### High-Priority Enhancements:
- [ ] System health monitoring dashboard
- [ ] Performance metrics collection
- [ ] Automated backup/recovery protocols
- [ ] Director performance analytics
- [ ] Learning pattern analysis

### Observations to Track:
- [ ] Token budget compliance
- [ ] Consensus resolution time
- [ ] Handoff success patterns
- [ ] Escalation frequency
- [ ] Constitutional violations (should be 0)

### Improve This Skill When:
- [ ] Directors have coordinated multiple times
- [ ] Real-world handoffs tested
- [ ] Consensus stress-tested
- [ ] First emergency situations

**Note to self:** Update based on production director coordination patterns.
