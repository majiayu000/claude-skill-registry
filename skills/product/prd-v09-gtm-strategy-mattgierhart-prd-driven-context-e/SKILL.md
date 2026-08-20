---
name: prd-v09-gtm-strategy
description: >
  Orchestrate go-to-market strategy by running positioning, offer construction, and channel
  allocation as a sequenced workflow during PRD v0.9 Go-to-Market. Triggers on requests to
  plan launch, define GTM strategy, or when user asks "how do we launch?", "go-to-market",
  "launch plan", "marketing strategy", "GTM", "launch this product". Chains three
  framework-grounded sub-skills (Dunford → Hormozi → ORB) and reconciles their outputs.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# GTM Strategy (Orchestrator)

Position in workflow: v0.8 Monitoring Setup → **v0.9 GTM Strategy (Orchestrator)** → v0.9 Launch Metrics

> **This skill is an orchestrator, not a primary skill.** GTM strategy is composed of three
> framework-grounded sub-skills that run in sequence. This skill chains them and reconciles
> outputs. New work on positioning, offers, or channels should invoke the sub-skills directly.

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | Each sub-skill in quick mode; reconciled GTM index |
| **standard** | Each sub-skill in standard mode; full reconciliation pass over outputs |
| **deep** | Each sub-skill in deep mode; multi-pass reconciliation + risk register |

## The Three Sub-Skills

GTM is **positioning before offer before channels**. Running them out of order produces channel plans that don't reach the right people with the right pitch.

| Step | Sub-skill | Framework | Owner |
|------|-----------|-----------|-------|
| 1 | [`prd-v09-positioning-dunford`](../prd-v09-positioning-dunford/SKILL.md) | April Dunford, *Obviously Awesome* (5-step) | Founder + PM |
| 2 | [`prd-v09-offer-construction-hormozi`](../prd-v09-offer-construction-hormozi/SKILL.md) | Alex Hormozi, *$100M Offers* (value equation + Grand Slam) | Founder + Sales |
| 3 | [`prd-v09-launch-channels-orb`](../prd-v09-launch-channels-orb/SKILL.md) | Corey Haines, ORB framework (Owned / Rented / Borrowed) | Growth |

Use the v0.9 tactical playbooks ([`prd-v09-aeo-audit`](../prd-v09-aeo-audit/SKILL.md), [`prd-v09-alternatives-pages`](../prd-v09-alternatives-pages/SKILL.md), [`prd-v09-cold-outreach-tiered`](../prd-v09-cold-outreach-tiered/SKILL.md), [`prd-v09-hn-reddit-launch`](../prd-v09-hn-reddit-launch/SKILL.md)) **after** these three are complete — each plugs into a specific channel from step 3.

## Orchestration Workflow

```
1. Positioning (Dunford)         →  GTM-*(positioning), BR-POS-*
              ↓
2. Offer (Hormozi)                →  GTM-*(offer, guarantee), BR-PRICING-*
              ↓
3. Channels (ORB)                 →  GTM-*(channel, sequence, mix-matrix)
              ↓
4. Reconciliation (this skill)    →  GTM-*(index) with cross-skill checks
              ↓
5. Tactical playbooks             →  AEO audit, alt pages, cold outreach, HN/Reddit (v0.9 tactical)
              ↓
6. Launch Metrics + Feedback      →  v0.9 Launch Metrics, Feedback Loop Setup
```

## Reconciliation (this skill's actual work)

After the three sub-skills run, check for cross-skill consistency:

| Check | Question | Fix if no |
|-------|----------|-----------|
| **Best-fit alignment** | Are channels (step 3) actually used by the best-fit segment defined in positioning (step 1)? | Re-run step 3 with corrected segment lens |
| **Promise consistency** | Does the offer (step 2) promise more or less than the positioning supports? | Adjust offer down; do not silently inflate positioning |
| **Guarantee viability** | Can the guarantee in the offer survive the launch volume from step 3? | Tighten guarantee terms or reduce paid-channel reach until guarantee can scale |
| **Category-channel fit** | Is the launch channel mix appropriate for the market category claimed in positioning? | Drop channels that don't fit the category (e.g., enterprise category → no TikTok) |
| **KPI rollup** | Do per-channel attribution targets sum to v0.3 baseline KPI- targets? | Adjust channel budget/effort allocation |

Reconciliation is the load-bearing work — without it, the three sub-skill outputs are incoherent.

## Consumes

This skill's `Consumes` is the **union** of the three sub-skills' `Consumes`:

- From v0.2 (CFD-, BR-product-type), v0.3 (FEA-, KPI-, BR-pricing), v0.4 (PER-), v0.8 (DEP-, MON-)
- See each sub-skill for the specific IDs it pulls

## Produces

This skill produces the **reconciled GTM- index** — a single entry pointing at all GTM- entries created by the three sub-skills, with reconciliation notes:

```
GTM-XXX: GTM Strategy Index
Type: Index
Owner: Launch Coordinator
Status: Approved

Positioning: GTM-AAA (statement), BR-POS-* (rules)
Offer: GTM-BBB (card), GTM-CCC (guarantee)
Channels: GTM-DDD/EEE/FFF (channel entries), GTM-GGG (mix matrix), GTM-HHH (sequence)
Tactical (when active): GTM-* from AEO, alternatives, cold outreach, HN/Reddit playbooks

Reconciliation notes:
  - Best-fit alignment: [PASS | issue + fix]
  - Promise consistency: [...]
  - Guarantee viability: [...]
  - Category-channel fit: [...]
  - KPI rollup: [...]

Linked IDs: All GTM-* created in this lifecycle iteration
```

## Migration Note (legacy entries)

Prior to this refactor, this skill produced GTM-* entries directly with Type=Messaging, Type=Channel, Type=Timeline, Type=Task, Type=Asset. Existing entries with those types remain valid — the sub-skills produce comparable types structured around their respective frameworks.

If you have legacy GTM-* entries created before the split, run each sub-skill once over the existing material to:

- Reclassify messaging entries as Type=Positioning (anchored in Dunford's 5 steps)
- Validate offer-related entries against the Hormozi value equation
- Reclassify channel entries by ORB layer (Owned / Rented / Borrowed)

No automatic migration — the reclassification is a deliberate decision that surfaces gaps in the original work.

## Quality Gates

Before proceeding to Launch Metrics:

- [ ] All three sub-skills have completed (or quick-mode placeholders exist for each)
- [ ] Reconciliation table filled with all five checks (PASS or fix logged)
- [ ] GTM- index entry created pointing at all sub-skill outputs
- [ ] No unreconciled contradictions between positioning, offer, and channels

## Downstream Connections

See each sub-skill for direct downstream connections. This orchestrator's downstream is:

| Consumer | What it uses |
|----------|--------------|
| **v0.9 Tactical playbooks** | The GTM index identifies which channels are active for tactical-skill plug-in |
| **v0.9 Launch Metrics** | The reconciled KPI rollup |
| **v0.9 Feedback Loop Setup** | The reconciled channel list |
