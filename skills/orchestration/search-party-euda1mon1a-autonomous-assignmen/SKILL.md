---
name: search-party
description: Parallel 120-probe reconnaissance using G-2 RECON agents. Deploy 12 G-2s commanding 10 D&D-inspired probes each. Use for comprehensive codebase exploration.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [systematic-debugger, code-review]
  must_serialize_with: []
  preferred_batch_size: 12
context_hints:
  max_file_context: 200
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "security.*breach"
    reason: "Security findings require immediate escalation"
  - pattern: "credentials|secrets"
    reason: "Credential findings require security review"
---

# SEARCH_PARTY Skill

> **Purpose:** Coordinated parallel reconnaissance with 120 specialized probes
> **Created:** 2025-12-31
> **Trigger:** `/search-party` command
> **Aliases:** `/recon`, `/search`, `/sp`

---

## When to Use

Deploy SEARCH_PARTY when you need comprehensive codebase intelligence:

- Investigating unfamiliar code areas
- Pre-task reconnaissance for complex changes
- Bug investigation with unclear root cause
- Security or compliance reviews
- Technical debt assessment
- Architecture review

**Do NOT use for:**
- Simple, well-understood tasks
- Single-file changes with known impact
- When only one lens is needed

---

## Economics: Zero Marginal Wall-Clock Cost

**Critical Understanding:** Parallel agents with the same timeout cost nothing extra in wall-clock time.

```
Sequential (BAD):        Parallel (GOOD):
10 probes × 30s each     10 probes × 30s in parallel
Total: 300s              Total: 30s (10x faster)
```

**Implication:** Always spawn all probes. There is no cost savings from running fewer.

---

## Deployment Pattern

### Standard Deployment: 12 G-2s × 10 Probes = 120 Probes

Deploy 12 G-2 RECON agents in parallel, each commanding a party of 10 probes:

| G-2 Mission | Target Domain | 10 Probes |
|-------------|---------------|-----------|
| G2-BACKEND-CORE | `backend/app/api/`, `backend/app/services/` | Full party |
| G2-BACKEND-MODELS | `backend/app/models/`, `backend/alembic/` | Full party |
| G2-SCHEDULING | `backend/app/scheduling/` | Full party |
| G2-RESILIENCE | `backend/app/resilience/` | Full party |
| G2-FRONTEND-CORE | `frontend/src/components/`, `frontend/src/app/` | Full party |
| G2-FRONTEND-HOOKS | `frontend/src/hooks/`, `frontend/src/lib/` | Full party |
| G2-TESTS-BACKEND | `backend/tests/` | Full party |
| G2-TESTS-FRONTEND | `frontend/__tests__/` | Full party |
| G2-MCP | `mcp-server/` | Full party |
| G2-DOCS | `docs/`, `.claude/` | Full party |
| G2-INFRASTRUCTURE | `docker-compose.yml`, `.github/`, `scripts/` | Full party |
| G2-SECURITY | `backend/app/core/`, `backend/app/api/deps.py` | Full party |

### Probe Composition (Per Party)

Each G-2 deploys these 10 D&D-inspired probes in parallel:

| Probe | Lens | D&D Analog | What It Finds |
|-------|------|------------|---------------|
| **PERCEPTION** | Surface state | Spot check | Logs, errors, health checks, what's immediately visible |
| **INVESTIGATION** | Connections | Search check | Dependencies, imports, call chains, why things connect |
| **ARCANA** | Domain knowledge | Arcana check | ACGME rules, resilience patterns, security implications |
| **HISTORY** | What changed | History check | Git log, recent PRs, migrations, blame |
| **INSIGHT** | Intent/design | Insight check | Why built this way, design decisions, tech debt |
| **RELIGION** | Sacred law | Religion check | CLAUDE.md compliance, pattern heresies, rituals |
| **NATURE** | Organic growth | Nature check | Over-engineering, natural vs forced patterns |
| **MEDICINE** | System diagnostics | Medicine check | Unhealthy components, resource exhaustion, leaks |
| **SURVIVAL** | Edge resilience | Survival check | Brittleness, missing error handling, failure modes |
| **STEALTH** | Hidden elements | Stealth check | Hidden coupling, security blind spots, invisible state |

---

## Invocation

### Full Deployment (120 probes)

```
/search-party
```

Deploys all 12 G-2s with full probe parties.

### Targeted Deployment (10 probes)

```
/search-party backend/app/scheduling/
```

Deploys single G-2 on specific target.

### Quick Search (focused)

```
/search-party --quick backend/
```

Deploys 6 critical probes (PERCEPTION, INVESTIGATION, ARCANA, HISTORY, INSIGHT, STEALTH).

---

## IDE Crash Prevention (CRITICAL)

**DO NOT** have ORCHESTRATOR spawn 12 G-2 agents directly. This causes IDE seizure and crashes.

**CORRECT Pattern:**
```
ORCHESTRATOR → spawns 1 G2_RECON (G-2 Commander)
                    ↓
              G2_RECON deploys 12 G-2 teams internally
              (manages parallelism, synthesizes results)
```

**WRONG Pattern:**
```
ORCHESTRATOR → spawns 12 G-2 agents directly → IDE CRASH
```

The G-2 Commander (G2_RECON) absorbs the parallelism complexity. ORCHESTRATOR only ever spawns 1 coordinator.

---

## Spawn Pattern

### Via G2_RECON Commander (CORRECT)

```python
# ORCHESTRATOR spawns G2_RECON who manages the 12 G-2 teams
Task(
    subagent_type="general-purpose",
    description="G2_RECON: SEARCH_PARTY Commander",
    prompt="""
## Agent: G2_RECON (G-2 Commander)

You are the G-2 Intelligence Commander for SEARCH_PARTY deployment.

## Mission
Deploy 12 G-2 reconnaissance teams in parallel. Each team runs 10 probes.
Collect all reports and synthesize into unified intel brief.

## Your G-2 Teams to Deploy
1. G2-BACKEND-CORE
2. G2-BACKEND-MODELS
3. G2-SCHEDULING
4. G2-RESILIENCE
5. G2-FRONTEND-CORE
6. G2-FRONTEND-HOOKS
7. G2-TESTS-BACKEND
8. G2-TESTS-FRONTEND
9. G2-MCP
10. G2-DOCS
11. G2-INFRASTRUCTURE
12. G2-SECURITY

## Spawn each using Task tool with subagent_type="Explore"

## After all report back:
1. Cross-reference findings
2. Flag discrepancies (high-signal)
3. Generate consolidated intel brief
4. Report to ORCHESTRATOR
"""
)
```

### Direct Deployment (Only if G2_RECON unavailable)

```python
# Deploy all 12 G-2s in parallel
# WARNING: Only use if spawning from within a coordinator, NOT from ORCHESTRATOR
# Total: 120 probes, wall-clock = single probe timeout

spawn_parallel([
    Task(subagent_type="Explore", description="G2-BACKEND-CORE",
         prompt="Deploy SEARCH_PARTY on backend/app/api/ and backend/app/services/"),
    Task(subagent_type="Explore", description="G2-BACKEND-MODELS",
         prompt="Deploy SEARCH_PARTY on backend/app/models/ and backend/alembic/"),
    Task(subagent_type="Explore", description="G2-SCHEDULING",
         prompt="Deploy SEARCH_PARTY on backend/app/scheduling/"),
    Task(subagent_type="Explore", description="G2-RESILIENCE",
         prompt="Deploy SEARCH_PARTY on backend/app/resilience/"),
    Task(subagent_type="Explore", description="G2-FRONTEND-CORE",
         prompt="Deploy SEARCH_PARTY on frontend/src/components/ and frontend/src/app/"),
    Task(subagent_type="Explore", description="G2-FRONTEND-HOOKS",
         prompt="Deploy SEARCH_PARTY on frontend/src/hooks/ and frontend/src/lib/"),
    Task(subagent_type="Explore", description="G2-TESTS-BACKEND",
         prompt="Deploy SEARCH_PARTY on backend/tests/"),
    Task(subagent_type="Explore", description="G2-TESTS-FRONTEND",
         prompt="Deploy SEARCH_PARTY on frontend/__tests__/"),
    Task(subagent_type="Explore", description="G2-MCP",
         prompt="Deploy SEARCH_PARTY on mcp-server/"),
    Task(subagent_type="Explore", description="G2-DOCS",
         prompt="Deploy SEARCH_PARTY on docs/ and .claude/"),
    Task(subagent_type="Explore", description="G2-INFRASTRUCTURE",
         prompt="Deploy SEARCH_PARTY on docker-compose.yml, .github/, scripts/"),
    Task(subagent_type="Explore", description="G2-SECURITY",
         prompt="Deploy SEARCH_PARTY on backend/app/core/ and backend/app/api/deps.py"),
])
```

---

## Intel Synthesis

After all 12 G-2s report back:

1. **Cross-reference findings** across domains
2. **Flag discrepancies** (high-signal findings)
3. **Identify gaps** requiring follow-up
4. **Generate consolidated intel brief**

### Discrepancy Analysis

**Key Insight:** Same target, different perspectives. Discrepancies between probes are high-signal:

| Discrepancy Type | Signal Meaning |
|-----------------|----------------|
| PERCEPTION says X, HISTORY says Y | Recent regression - something changed |
| INVESTIGATION says connected, INSIGHT says isolated | Undocumented coupling |
| ARCANA flags violation, PERCEPTION shows green | Silent failure or misconfigured checks |
| HISTORY shows change, PERCEPTION shows no effect | Change not deployed or cached |
| INSIGHT expects behavior A, INVESTIGATION shows B | Implementation drift from design |

---

## Output Format

### Per-G-2 Report

```markdown
## G-2 Intel: [DOMAIN]

### Health Grade: [A-F]

### Key Findings
- [Finding 1 with severity]
- [Finding 2 with severity]

### Discrepancies Detected
- [Probe A vs Probe B disagreement]

### Gaps Identified
- [What wasn't checked]

### Priority Actions
1. [Most urgent fix]
2. [Next priority]
```

### Consolidated Brief

```markdown
## SEARCH_PARTY Intel Brief (120 Probes Deployed)

| Domain | Health | Issues Found | Priority Findings |
|--------|--------|--------------|-------------------|
| Backend Core | A- | 3 | [findings] |
| Frontend | B | 12 | [findings] |
| Scheduling | A | 0 | Clean |
| ... | ... | ... | ... |

### Cross-Domain Discrepancies
[High-signal findings where domains/probes disagreed]

### Global Gaps
[What wasn't checked across all domains]

### Recommended Actions
1. [Highest priority fix]
2. [Next priority]
```

---

## Timeout Profiles

| Profile | Duration | Best For |
|---------|----------|----------|
| **DASH** | 60s | Quick triage, P0 emergencies |
| **RECON** | 120s | Normal reconnaissance (default) |
| **INVESTIGATION** | 300s | Deep analysis, security audits |

---

## Failure Recovery

### Minimum Viable Intel

Mission can proceed if:
- PERCEPTION (baseline state) ✓
- INVESTIGATION (dependencies) ✓
- ARCANA (domain safety) ✓
- At least 4 of remaining 7 probes

### Circuit Breaker

If > 3 consecutive probe failures: Trip to OPEN state, suspend missions.

---

## Protocol Reference

Full protocol documentation: `.claude/protocols/SEARCH_PARTY.md`

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `startup` | Session initialization |
| `startupO` | ORCHESTRATOR mode initialization |
| `systematic-debugger` | Post-recon debugging |
| `parallel-explore` | Quick parallel exploration |

---

*SEARCH_PARTY: Ten lenses, one target, zero marginal cost. The discrepancies are the signal.*
