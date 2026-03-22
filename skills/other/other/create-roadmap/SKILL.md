---
name: create-roadmap
description: Create a Now/Next/Later outcome-oriented roadmap when the user asks to plan a roadmap, prioritize features, or define product direction
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[product area or theme to roadmap]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: product, roadmap, planning
---

# Create Roadmap

## Overview

Generate a Now/Next/Later roadmap where every item ties to a measurable outcome, not just a feature name. This format communicates strategic intent without false precision on dates, and forces prioritization by time horizon and confidence level.

## Workflow

1. **Read product context** -- Scan `.chalk/docs/product/` for the product profile, PRDs, JTBD docs, and metrics frameworks. Check `.chalk/docs/engineering/` for architecture constraints and tech debt items. These inform what is feasible and what matters.

2. **Parse scope** -- Extract from `$ARGUMENTS` the product area, theme, or time horizon to roadmap. If unspecified, create a full-product roadmap using all available context.

3. **Determine the next file number** -- Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

4. **Categorize items into time horizons**:
   - **Now** (current cycle, high confidence): Actively being built or about to start. Clear problem definition, validated need, committed resources.
   - **Next** (1-2 cycles out, medium confidence): Problem is understood, solution is taking shape, not yet committed.
   - **Later** (future, low confidence): Strategic bets, exploration areas, things that depend on learning from Now/Next.

5. **Write each item** with columns: Item, Outcome (measurable result), Confidence (high/medium/low), Dependencies (what must be true or done first).

6. **Add strategic context** -- Above the roadmap table, write a brief narrative explaining the strategic themes connecting the items and what the roadmap is optimizing for.

7. **Write the file** -- Save to `.chalk/docs/product/<n>_roadmap.md`.

8. **Confirm** -- Share the file path and highlight any items with unresolved dependencies or low confidence that need validation.

## Output

- **File**: `.chalk/docs/product/<n>_roadmap.md`
- **Format**: Plain markdown with strategic narrative and Now/Next/Later tables
- **First line**: `# Roadmap: <Product Area or Theme>`

## Anti-patterns

- **Feature lists without outcomes** -- "Add filtering" is not a roadmap item. "Users can find records in <10 seconds (reduce support tickets by 30%)" ties the work to value.
- **Dates on everything** -- Now/Next/Later intentionally avoids specific dates for Next and Later items. Adding dates to low-confidence items creates false promises.
- **No dependencies called out** -- Roadmap items without dependencies hide sequencing risks. If B requires A, say so.
- **Confidence theater** -- Marking everything as "high confidence" defeats the purpose. Be honest about what is validated versus what is a bet.
- **Solution-shaped items** -- "Build GraphQL API" belongs in an engineering plan, not a product roadmap. Roadmap items should describe user or business outcomes.
