---
name: intel
description: "Gather and shape intelligence signals from collected feeds (RSS, HackerNews, Lobsters, EDGAR) into audience-aware output. Use when you need current context on a technology, industry trend, or domain — or when you need to present signals to a specific audience. NOT for forward-looking predictions (use forecast); NOT for architecture analysis (use archobs); NOT for writing specs (use spec)."
metadata: {"stage":"Define","tags":["intelligence","trends","signals","research","briefing","news","feeds","evidence","audience","executive","engineering","decision","digest","synthesis","presentation","stakeholder"],"aliases":["intel","intelligence","signals","executive-brief","daily-digest","decision-brief"]}
---

# Intel (Intelligence Briefs)

## Overview

Produce focused intelligence briefs on a topic by querying the `intel` CLI against locally collected feeds (RSS, HackerNews, Lobsters, EDGAR). Briefs combine trending signals, full-text search hits, and topic breakdowns into a concise, evidence-backed summary an agent or human can act on.

Use this skill when you need current signal on a technology, vendor, standard, or industry trend — or when you need to present signals to a specific audience.

Success looks like: a brief with ranked signals, source citations, and a clear "so what" tailored for the target audience — readable in under 2 minutes and actionable without needing to parse raw data.

## Prerequisites

1. **Build the tool**:
   ```bash
   cd tools/intelligence && npm install && npm run build
   ```

2. **Make `intel` available on PATH**:
   ```bash
   npm link          # from tools/intelligence/
   ```

3. **Create a config file**:
   ```bash
   mkdir -p ~/.config/intel ~/.local/share/intel
   cp config/feeds.example.yaml ~/.config/intel/config.yaml
   # Edit ~/.config/intel/config.yaml to customize feeds
   ```

4. **Seed the database** (first run):
   ```bash
   intel collect --once
   ```

5. **Install the collector as a background service** so data stays fresh:
   ```bash
   ./service/install.sh        # macOS (launchd) / Linux (systemd)
   ```
   This installs a LaunchAgent (macOS) or systemd user unit (Linux) that starts on login and restarts on crash. Verify it's running:
   ```bash
   # macOS
   launchctl print gui/$(id -u)/com.intel.collector
   tail -f ~/Library/Logs/intel-collector.log

   # Linux
   systemctl --user status intel-collector
   journalctl --user -u intel-collector -f
   ```
   To uninstall: `./service/install.sh uninstall`

6. **Verify**: `intel stats` — check `events_total > 0` and `newest_event` is recent.

## Chooser

### Content type (what data to gather)

| Type | When to use |
|---|---|
| **Topic brief** (default) | "What's happening with X?" |
| **Trend scan** | General landscape check |
| **Evidence pack** | Feeding context into another skill |
| **Source check** | Verify data quality |

### Audience (how to present — default: practitioner)

| Audience | Shape | When to use |
|---|---|---|
| **Practitioner** (default) | Ranked signals, trend context, gaps, so what | Feeding into your own work |
| **Executive** | 3-5 bullet TL;DR, "so what", recommended action, risk flags | Status updates, steering meetings |
| **Engineering** | Signals mapped to stack, migration/deprecation implications | Sprint planning, tech radar |
| **Decision** | Evidence mapped to options, recommendation | Buy-vs-build, adopt-vs-wait, vendor selection |
| **Daily digest** | Top-5 signals, one-line commentary | Morning standup, async channel |
| **Architecture decision** | Archobs risk + forecast lifecycle × decision options | Technology adoption, boundary redesign |

## Clarifying Questions

- What topic or domain do you want a brief on?
- What time horizon matters? (last few hours, last week, last month)
- Is this for general awareness or feeding into a specific decision?
- Any particular sources or subtopics to prioritize?
- Who is the audience for this brief?
- Which brief type fits? (practitioner, executive, engineering, decision, daily digest, architecture decision)

## Workflow

1. **Determine content type and audience** — ask or infer from context. If unclear, default to practitioner audience with topic brief.

2. **Verify data freshness**:
   ```bash
   intel stats
   ```
   Check `total_events` and `newest_event` — if the database is empty or stale, run `intel collect --once` first.

3. **Gather signals** (choose based on content type):

   **Topic brief** — run in parallel:
   ```bash
   intel search "<topic>" --since 7d --limit 20
   intel trends --window 60m --top 10
   intel topics --active
   ```

   **Trend scan**:
   ```bash
   intel trends --window 60m --top 15
   ```

   **Evidence pack**:
   ```bash
   intel pack --since 6h --top 10 --max-events 5
   ```

   **Source check**:
   ```bash
   intel sources
   ```

4. **Audience-specific signal gathering** (in addition to content type above):

   **Executive / Daily digest**:
   ```bash
   intel pack --since 24h --top 10 --max-events 5
   ```

   **Engineering** — run in parallel:
   ```bash
   intel pack
   intel search "<stack-relevant terms>"
   intel topics --active
   ```

   **Decision** — run in parallel:
   ```bash
   intel search "<decision topic>"
   intel trends
   ```

   **Architecture decision** — requires archobs + forecast data:
   ```bash
   archobs show clusters --format json
   archobs show risks --format json
   intel forecast    # lifecycle phases for relevant technologies
   ```

5. **Deepen on high-signal hits** — for the most relevant results, fetch full event detail:
   ```bash
   intel events --id <event_id>
   ```

6. **Filter and rank** — select the top signals by relevance to the audience:
   - Practitioner: prioritize signal strength and relevance to stated topic
   - Executive: prioritize business impact, risk, competitive signals
   - Engineering: prioritize stack relevance, deprecations, security advisories
   - Decision: prioritize evidence that differentiates the options
   - Daily digest: prioritize breadth and recency
   - Architecture decision: prioritize signals that affect boundary/technology choices

7. **Synthesize the brief** using the output template for the chosen audience (see below). Do not mix templates.

8. **Flag gaps** — note stale sources, missing coverage, low-confidence signals.

## Guardrails

- Do not present intel output as authoritative fact — these are signals from configured feeds, not exhaustive research.
- Do not skip the freshness check — stale data produces misleading briefs.
- Do not dump raw JSON to the user — always synthesize into the output template.
- Do not run `intel collect` in long-running daemon mode during a brief — use `--once` if a refresh is needed.
- Do not mix brief types — pick one audience and commit.
- Do not fabricate signals — only use data returned by `intel` commands.
- Executive briefs must be readable by non-technical stakeholders — no jargon, no acronyms without expansion.

## Output Template

### Practitioner (default)

- **Topic**: the subject of the brief
- **Data window**: time range covered, event count, source count
- **Top signals** (3-5): title, source, timestamp, why it matters
- **Trend context**: what's rising/falling, velocity of change
- **Gaps**: stale sources, missing coverage areas, low-confidence signals
- **So what**: 1-2 sentence synthesis of what this means for the user's context
- **Next skill**: where to go from here (plan, spec, architecture, etc.)

### Executive

- **Headline**: 1 sentence — what's the most important thing to know
- **Top signals** (3-5 bullets): plain language, no jargon, each with why it matters
- **So what**: 1-2 sentences — implication for us specifically
- **Recommended action / next step**: what to do with this information
- **Risk flags** (if any): things that could go wrong if we ignore this

### Engineering

- **Data window**: time range covered, event count, source count
- **Signals by relevance to our stack**: grouped by topic (e.g., runtime, framework, infra, tooling)
- **Migration / deprecation watch**: things to track that may force future work
- **New tools / releases worth evaluating**: notable releases relevant to our stack
- **Security advisories** (if any): CVEs, supply-chain risks, dependency alerts
- **Links to deeper reads**: URLs from source events for follow-up

### Decision

- **Decision statement**: what we're choosing between (frame as a clear question)
- **Evidence for each option**: sourced from signals, with citations
- **Gaps in evidence**: what we don't know and how it affects confidence
- **Recommendation**: selected option with confidence level (high / medium / low)
- **Next skill**: `plan` or `spec` to act on the decision

### Daily Digest

- **Date + data window**: date, time range, source count
- **Top 5 signals**: title + one-line take for each
- **One thing to watch**: emerging trend that hasn't peaked yet
- **Source health note** (if degraded): flag stale or unreachable sources

### Architecture Decision

- **Decision statement**: what we're choosing between
- **Structural context** (from archobs): cluster coupling, boundary health, risk scores for affected areas
- **Ecosystem context** (from forecast): lifecycle phase, chain activity, system dynamics for relevant technologies
- **Cross-domain synthesis**: where structural reality and ecosystem signals align or conflict
- **Options matrix**: each option scored against structural + ecosystem evidence
- **Recommendation**: selected option with confidence level
- **Next skill**: `plan` or `spec`

## References

- Forward-looking predictions: [`forecast`](../forecast/SKILL.md)
- Architecture observability: [`archobs`](../archobs/SKILL.md)
- Implementation planning: [`plan`](../plan/SKILL.md)
- Spec-driven development: [`spec`](../spec/SKILL.md)
- Architecture decisions: [`architecture`](../architecture/SKILL.md)
