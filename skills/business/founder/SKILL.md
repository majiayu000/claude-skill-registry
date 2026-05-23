---
name: founder
description: Use when validating ideas, sizing markets, building pitch decks, preparing for investors, modeling financials, planning launches, or creating board reports. Auto-activates on fundraising, pitch, investor, TAM/SAM/SOM, unit economics, runway, or board deck tasks.
---

# Founder Skill

Router skill for startup workflows. Detects task type and routes to appropriate workflow that produces usable artifacts.

## When This Skill Activates

You're working on:

- Validating a product idea or value proposition
- Calculating market size (TAM/SAM/SOM)
- Analyzing competitive landscape or threats
- Building or evaluating a pitch deck
- Preparing for investor meetings
- Modeling unit economics, projections, or cash flow
- Planning a product launch
- Creating board reports or updates

## Workflow Selection

Announce which workflow you're using before starting:

| Task Type                         | Workflow            | Reference                     | Output Artifact               |
| --------------------------------- | ------------------- | ----------------------------- | ----------------------------- |
| Idea validation, stress testing   | Validate Idea       | `references/validate.md`      | JSON scores + GO/ITERATE/KILL |
| TAM/SAM/SOM, market opportunity   | Size Market         | `references/market-size.md`   | Tables + Marp slide           |
| Competition, threats, positioning | Analyze Competition | `references/compete.md`       | Threat matrix + heat map      |
| Pitch deck creation or eval       | Build Pitch Deck    | `references/pitch.md`         | Marp deck (10-12 slides)      |
| Investor Q&A, meeting prep        | Prep for Investors  | `references/investor-prep.md` | Q&A document                  |
| Unit economics, projections, cash | Model Financials    | `references/financials.md`    | Spreadsheet-ready tables      |
| Launch planning, 90-day roadmap   | Plan Launch         | `references/launch.md`        | Phased execution plan         |
| Board deck, metrics summary       | Report to Board     | `references/board.md`         | Marp deck + summary           |

## Related Thinking Tools

From `hope/skills/soul/references/tools/`:

| Tool                                                                                | When to Use                                  |
| ----------------------------------------------------------------------------------- | -------------------------------------------- |
| [Abstraction Ladder](../../hope/skills/soul/references/tools/abstraction-ladder.md) | Reframe pivot decisions                      |
| [Hard Choice](../../hope/skills/soul/references/tools/hard-choice.md)               | GO/KILL verdicts with no clear winner        |
| [Zwicky Box](../../hope/skills/soul/references/tools/zwicky-box.md)                 | Generate creative business model variations  |
| [First Principles](../../hope/skills/soul/references/tools/first-principles.md)     | Challenge "that's how it's done" assumptions |
| [Pre-Mortem](../../hope/skills/soul/references/tools/pre-mortem.md)                 | Anticipate launch/funding failures           |
| [Circle of Competence](../../hope/skills/soul/references/tools/circle-of-competence.md) | Know when to hire vs build yourself      |

From this skill's `references/`:

| Tool                                              | When to Use                             |
| ------------------------------------------------- | --------------------------------------- |
| [Regret Minimization](references/regret-minimization.md) | Major founder decisions (quit job, pivot, shut down) |

## Dimensions

This skill has multiple configuration dimensions. See [compatibility-matrix.md](references/compatibility-matrix.md) for:

- Workflow x Stage (Pre-Seed to Growth)
- Validation Verdict x Next Workflow
- Pitch Deck x Audience
- Financial Model Depth x Funding Stage
- Board Report x Company Health
- Market Size Approach x Market Type
- Launch Phase x Traction Level

Use ✓✓ combinations when possible; avoid ✗ combinations.

## Usage

1. Detect which workflow applies based on user's task
2. Check [compatibility matrix](references/compatibility-matrix.md) for dimension compatibility
3. Announce: "I'm using the founder skill for [workflow]"
4. Load the appropriate reference file
5. Execute the workflow with confirmation gates (see below)
6. Produce the specified artifact

## Confirmation Gates

Multi-step workflows pause at checkpoints to prevent wasted work when intent drifts.

**Gate Points:**

| Phase | Gate |
|-------|------|
| After research/discovery | ⚠️ CHECKPOINT: "Does this understanding match your intent?" |
| After approach/structure | ⚠️ CHECKPOINT: "Here's my proposed approach. Should I proceed?" |
| Before final artifact | ⚠️ CHECKPOINT: "Ready to generate [artifact]. Confirm?" |

**Skip gates:** Say "proceed without confirmation" to run uninterrupted.

**In workflows:** Each reference file should pause at these points:

```
### Phase 2: Analysis

[... phase content ...]

⚠️ **CHECKPOINT**: Present findings summary. Ask: "Does this capture the key insights? Any adjustments before I continue?"
```

## Artifact Tooling

After generating markdown artifacts, users can convert them:

| Artifact      | Tool        | Command                                        |
| ------------- | ----------- | ---------------------------------------------- |
| Slides (Marp) | Marp CLI    | `npx @marp-team/marp-cli slides.md --pptx`     |
| Documents     | md-to-pdf   | `npx md-to-pdf document.md`                    |
| Spreadsheets  | Copy tables | Paste markdown tables into Google Sheets/Excel |

## Rules

- Always ask clarifying questions before generating artifacts
- Produce complete, usable outputs (not partial drafts)
- Use Marp format for all slide decks
- Use markdown tables for spreadsheet data (easy paste)
- Be brutally honest in evaluations (2% YC acceptance rate mindset)
- Include confidence levels and key assumptions

## Quality Footer (Required for High-Stakes Outputs)

All validation, pitch, and financial outputs MUST end with:

```
---
| Confidence | X-Y% |
| Key Assumption | [What would change this verdict] |
| Reversibility | Type 2A/2B/1 |
```

**Verdict rules:**
- GO verdict requires ≥70% confidence
- ITERATE requires identifying specific unknowns to resolve
- KILL must cite specific evidence, not intuition

## Common Rationalizations (All Wrong)

| Thought | Reality |
|---------|---------|
| "The market is huge" | TAM without SAM/SOM is meaningless. |
| "Nobody's doing this" | If nobody's doing it, ask why. |
| "We just need 1% of the market" | That's not a strategy, it's wishful math. |
| "First mover advantage" | First movers usually lose. Execution wins. |
| "Build it and they will come" | Distribution is harder than product. |
| "We're different" | Every founder says this. Prove it with evidence. |
