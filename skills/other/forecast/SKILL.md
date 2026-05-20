---
name: forecast
description: "Predict likely next developments from internal development patterns (git history, archobs clusters) and external signals (intel feeds). Use when you need forward-looking intelligence — what's GOING to happen, not what already happened. NOT for gathering raw signals (use intel); NOT for architecture analysis (use archobs); NOT for implementation planning (use plan)."
metadata: {"stage":"Define","tags":["forecast","prediction","scenarios","chains","lifecycle","convergence","trends","intelligence","bayesian","entropy","cusum","hmm","decay","trajectory","momentum","velocity","feature-prediction","git-history","development-patterns","change-analysis","adjacency"],"aliases":["forecast","predict","scenarios","what-next","forward-looking","trajectory","momentum","velocity","feature-prediction"]}
---

# Forecast (Predictive Intelligence)

## Overview

Predict likely next developments using two engines:

- **Internal engine** (trajectory): analyzes git history and archobs cluster context to predict what the team is likely to build next — where momentum is concentrated, what kinds of changes are happening, and what areas are growing.
- **External engine**: uses Bayesian scenario projection, exponential decay weighting, entropy-based surprise scoring, CUSUM change-point detection, and HMM lifecycle classification from collected intelligence feeds to predict external shifts.

While `intel` tells you what happened, `forecast` tells you what's likely to happen next — internally from development patterns and externally from ecosystem signals.

Success looks like: forward-looking intelligence with ranked scenarios, development momentum analysis, and actionable recommendations that a team can act on before events materialize.

## Chooser (When to Use)

| Situation | Mode |
|---|---|
| "What are we likely to build next?" | **Internal** |
| "Where is development concentrated?" | **Internal** |
| "What external shifts should we prepare for?" | **External** |
| "What's going to happen next?" (general) | **Combined** — cross-references internal velocity with external ecosystem signals |
| "What's the full picture?" | **Combined** — produces compound insights (e.g., "heavy investment in a sinking dependency") |
| "What's the market doing?" / "Technology landscape" | **External** |
| "What happened recently?" | `intel` |
| "How is our codebase structured?" | `archobs` |
| "Plan the implementation" | `plan` |

**Default to Combined mode** unless the user explicitly scopes to internal-only or external-only. Cross-referencing internal development velocity against external ecosystem signals produces compound insights that neither engine generates alone.

## Prerequisites

### Internal engine
1. **archobs data**: Run `archobs report` first to get cluster assignments, file risks, drift data, and commit history
2. **archobs CLI**: `pip install -e 'tools/archobs[full]'`

### External engine
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
   ```
4. **Seed the database** (first run):
   ```bash
   intel collect --once
   ```
5. **Install the collector as a background service** so data stays fresh:
   ```bash
   ./service/install.sh        # macOS (launchd) / Linux (systemd)
   ```
6. **Run the published_at migration** (if upgrading from an older database):
   ```bash
   sqlite3 ~/.local/share/intel/intel.db < tools/intelligence/migrations/003-published-at-analysis.sql
   ```
7. **Verify**: `intel stats` — check `events_total > 0` and `newest_event` is recent.

---

## Workflow

Choose the mode based on the chooser table, then follow the engine-specific workflow:

- **Internal**: [`references/internal-engine.md`](references/internal-engine.md)
- **External**: [`references/external-engine.md`](references/external-engine.md)
- **Combined**: see below

### Combined Mode

When the user asks "what's going to happen next?" or wants the full picture, run both engines and cross-reference.

1. Run internal and external engines in parallel (they have independent data sources)
2. **Cross-reference**: cluster velocity x lifecycle phase of ecosystem dependencies
   - Which archobs clusters map to technologies that forecast tracks?
   - Is the team investing heavily in an area where the ecosystem is decaying?
   - Is there an emerging ecosystem opportunity where the team has no current investment?
3. **Surface compound signals**: "cluster X has high acceleration AND its primary ecosystem dependency shows a reinforcing loop"

#### Cross-reference patterns

| Internal signal | External signal | Synthesis |
|---|---|---|
| High velocity cluster wrapping external dep | Decaying lifecycle for that dep | Urgent: heavy investment in a sinking dependency |
| Emerging cluster using new technology | Accelerating lifecycle for that tech | Aligned: team is riding a growth wave |
| No cluster activity for a technology | Reinforcing loop detected for that tech | Gap: ecosystem is moving and we're not |
| High velocity in an area | Stable lifecycle for related tech | Normal: team building on solid ground |

---

## Guardrails

| Rule | When it matters | What to do |
|---|---|---|
| **Scores ≠ probabilities** | Always | Scenario scores are relative rankings (temperature-sharpened softmax), not calibrated probabilities. Present as "high/medium/low confidence" not as percentage likelihoods |
| **Trajectory = evidence** | Internal engine | Use "evidence suggests" / "development patterns indicate" framing |
| **Adjacency is heuristic** | Internal engine | The adjacency table reflects common patterns, not rules. Domain context overrides |
| **Freshness check** | Before synthesis | Stale data → stale forecasts. Verify recency via `intel stats` |
| **Spurious correlations** | Chains with support < 3 or low source diversity | Flag as lower confidence |
| **Temporal artifacts** | Chains where `temporal_pattern` = `weekday_correlated` or `weekday_ratio` > 0.7 | Likely a calendar cadence, not causal. `weekday_ratio` is always present for programmatic assessment. Discount unless you can identify a mechanism |
| **Decay reveals staleness** | `decay_weighted_support` ≪ `support` | Co-movement hasn't recurred recently (half-life = 14d) |
| **Entropy = predictability** | `normalized_entropy` > 0.8 | Target is bursty and less predictable; widen confidence window |
| **CUSUM change points** | Change point within last 7 days | History may not hold — always surface these prominently. Highest-priority signal |
| **Signal quality** | Scenario ranking | Scenarios rank by chain confidence × source diversity × trigger specificity, not just lift. Low-fanout triggers rank higher |
| **Base rate noise** | `trigger_base_rate` > 0.5 | Topic spikes most days — chains from it are less informative |
| **Target base rate noise** | `target_base_rate` > 0.8 | Target topic is omnipresent — predicting it will spike is trivially true. Pre-filtered when evidence is weak (no 'high' relevance) |
| **Evidence relevance** | `evidence_relevance` = `low` | Likely a classifier false positive (event tagged with 5+ topics). Weight scenario lower. Scenarios where ALL evidence is 'low' are pre-filtered out |
| **Classifier over-tagging** | High-volume topics (e.g. `lang.typescript`) | Topic classifier assigns these broadly — evidence titles may not be topically relevant even when marked `high`. Cross-check titles before citing. Scenarios with high `target_base_rate` (> 0.8) and no 'high'-relevance evidence are now pre-filtered. **Volume inflation**: over-tagged topics have inflated volume counts and chain support — discount both when evidence titles look off-topic |
| **Co-movement ≠ causation** | All chains and scenarios | Chains detect statistical co-occurrence (A spikes, then B spikes), not causal mechanisms. High lift means "more than random" but does not mean A causes B. Always frame as "associated with" or "tends to follow," never "causes" or "leads to." The weekday-ratio filter catches some calendar artifacts, but spurious correlation is an inherent limitation |
| **Source bias** | All forecasts | 128 sources skew toward developer communities (HN), vendor blogs (AWS/Azure/GCP), and financial news (Seeking Alpha, Yahoo Finance). Enterprise procurement signals, analyst reports behind paywalls (Gartner, Forrester, IDC), and non-English-language markets are underweighted. Treat coverage gaps as blind spots, not absence of activity |
| **Attention ≠ fundamentals** | Lifecycle phases, scenarios | "Accelerating" means more coverage and developer activity, not necessarily more revenue, better margins, or enterprise adoption. The system tracks technology momentum (where engineering attention is concentrating), not market fundamentals. Do not use lifecycle phases as investment or procurement signals without supplementary research |
| **Accumulation freshness** | Accumulation dynamics | Requires `published_at` in window. Backfill-only topics are excluded |
| **HMM vs rule-based** | Phase classification | HMM overrides rule-based when confidence is +0.15 higher. `phase_probabilities` only present when HMM was used |
| **Transitive diversity** | A→B→C chains | Per-prefix cap of 3 ensures diverse paths. If all top results share the same A→B prefix, lower-ranked cross-domain paths are more interesting |
| **Transitive uncertainty** | A→B→C chains | `combined_lift` is a product, `min_support` is the weakest link — uncertainty compounds. Use `normalized_confidence` (geometric mean of leg confidences, 0-1) for calibrated comparison |
| **Cluster staleness** | Internal engine | Low `drift.ari_prev` means cluster boundaries are shifting. Path-based analysis still valid |
| **120-day retention** | All forecasts | System sees patterns within 120-day retention window with a 90d lifecycle timescale. Can detect quarterly trends and seasonal cycles within a single quarter, but cannot detect year-over-year patterns. Good at "what's happening now, what's about to happen, and how does the current quarter compare to the last." For longer-horizon questions, supplement with analyst reports and historical research |
| **No fabrication** | Always | Only use data returned by tools. Never invent scenarios or probabilities |
| **No raw JSON** | Output | Always synthesize through the output template |

---

## Output Template

### Internal mode (trajectory)

- **Analysis window**: date range, total commits, total file changes
- **Development focus**: which clusters are most active (momentum ranking)
- **Active areas** (top 2-3 clusters):
  - **Cluster**: ID, label, top paths, archobs metrics
  - **Change profile**: growth/churn ratios — what kind of work is happening
  - **Velocity**: accelerating/steady/decelerating (from --compare)
  - **Key paths**: recently added (what's new), most modified (what's being iterated)
  - **Edge relationships**: which other clusters this one connects to
- **Thematic patterns**: frequent tokens, recent subjects
- **Feature adjacency reasoning**: based on observed patterns, what features are logically next
- **Confidence notes**: window size, cluster stability (drift), concentration level
- **Recommended action**: what to investigate, plan for, or build next

### External mode (forecast)

- **Analysis window**: date range, events analyzed, source count
- **Structural breaks** (ALWAYS include if non-empty): topics with CUSUM change points from `change_points_summary`, sorted by recency. These are the highest-signal items — a recent structural break means a topic's trajectory changed and historical patterns may not hold.
- **Active triggers**: topics currently spiking that have historical chain patterns
- **Top scenarios** (3-5):
  - **Topic**: the predicted target topic
  - **Score**: relative scenario score (0-1), explain as high/medium/low. Not a calibrated probability — use for ranking, not for estimating real-world likelihood
  - **Timeframe**: expected window in days (entropy-widened)
  - **Triggers**: which active topics are driving this prediction (sorted by contribution strength — first trigger matters most for this specific target)
  - **Evidence**: top supporting article titles (up to 3). Check `evidence_relevance` — flag any 'low' relevance titles as potential classifier false positives.
  - **Predictability**: if `target_entropy` > 0.8, note the target is bursty
  - **CUSUM discount**: if trigger/target has a recent change point, note reduced confidence
- **Transitive chains**: noteworthy A->B->C paths, especially cross-domain
- **Lifecycle context**: notable phase transitions
- **Entropy landscape**: topics with extreme entropy values
- **Multi-scale alignment**: topics where all timeframes agree on direction
- **System dynamics**: reinforcing loops, delays, accumulations, dampening
- **Ranked chains**: top active chains by composite score. Note chains with high `trigger_base_rate` (> 0.5) as lower-confidence.
- **Confidence notes**: data depth, source diversity, chain support levels, decay-weighted support, CUSUM discounts
- **So what**: 1-2 sentence synthesis of the most actionable insight
- **Recommended action**: what to watch, prepare for, or investigate further

### Combined mode

- **Development momentum** (from internal engine): top active clusters, velocity, feature adjacency
- **Ecosystem signals** (from external engine): top scenarios, lifecycle phases, dynamics
- **Cross-domain synthesis**: where internal development patterns and external ecosystem signals align or conflict — compound signals, gaps, and urgent mismatches
- **Recommended action**: what to prioritize, investigate, or prepare for based on the full picture

## References

- Internal engine workflow: [`references/internal-engine.md`](references/internal-engine.md)
- External engine workflow: [`references/external-engine.md`](references/external-engine.md)
- Velocity interpretation details: [`references/velocity-interpretation.md`](references/velocity-interpretation.md)
- Feature adjacency patterns: [`references/feature-adjacency.md`](references/feature-adjacency.md)
- Git-only fallback: [`references/manual-fallback.md`](references/manual-fallback.md)
- Raw signal gathering: [`intel`](../intel/SKILL.md)
- Architecture observability: [`archobs`](../archobs/SKILL.md)
- Implementation planning: [`plan`](../plan/SKILL.md)
- Architecture decisions: [`architecture`](../architecture/SKILL.md)
