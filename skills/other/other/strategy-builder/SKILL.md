---
name: strategy-builder
version: 1.0.0
description: '[Content] Build marketing strategy: positioning, channels, messaging, campaigns, budget, KPIs. Follows market-analysis.'
allowed-tools: Read, Write, Edit, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/web-research-protocol.md`

## Quick Summary

**Goal:** Build comprehensive marketing strategy with positioning, channels, messaging, campaigns, budget, and KPIs.

**Workflow:**

1. **Load market analysis** — Read market-analysis output
2. **Define positioning** — Value proposition, differentiation
3. **Plan channels** — Strategy with budget allocation + ROI
4. **Craft messaging** — Tagline, key messages, proof points
5. **Build campaign roadmap** — Phases with timeline and KPIs
6. **Risk assessment** — Marketing risks with mitigation

**Key Rules:**

- Positioning MUST reference competitive analysis
- Every channel: purpose, budget %, expected ROI, priority
- KPIs must be specific, measurable, time-bound

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Strategy Builder

## Step 1: Load Market Analysis

Read the market analysis output (from market-analysis skill or inline).
Extract: competitor landscape, target segments, SWOT, market size.

## Step 2: Positioning

Based on competitive analysis:

- **Value proposition** — What unique value do we offer?
- **Differentiation** — How are we different from competitor X, Y, Z?
- **Brand voice** — Tone, personality, communication style

## Step 3: Channel Strategy

For each channel:

| Channel   | Purpose                           | Budget % | Expected ROI | Priority |
| --------- | --------------------------------- | -------- | ------------ | -------- |
| {channel} | {awareness/acquisition/retention} | {%}      | {X:1}        | P0/P1/P2 |

Total budget % must equal 100%.

## Step 4: Messaging Framework

- **Tagline** — One memorable line
- **Key messages** (3-5 pillars) — Core themes
- **Proof points** — Evidence supporting each message
- **Elevator pitch** — 30-second version

## Step 5: Campaign Roadmap

| Phase  | Timeline | Objective   | Tactics | KPIs      | Budget |
| ------ | -------- | ----------- | ------- | --------- | ------ |
| Launch | M1-M3    | Awareness   | {list}  | {metrics} | {$}    |
| Growth | M4-M6    | Acquisition | {list}  | {metrics} | {$}    |
| Scale  | M7-M12   | Retention   | {list}  | {metrics} | {$}    |

## Step 6: Risk Assessment

| Risk   | Likelihood | Impact | Mitigation |
| ------ | ---------- | ------ | ---------- |
| {risk} | H/M/L      | H/M/L  | {strategy} |

## Output

Write to `docs/knowledge/strategy/marketing/{descriptive-slug}.md` using enforced template from `docs/templates/marketing-strategy-template.md`.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
