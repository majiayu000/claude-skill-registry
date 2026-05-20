---
name: analyze-competitors
description: Build a competitive positioning matrix and strategy canvas when the user asks to analyze competitors, compare products, or assess competitive landscape
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[competitor names and/or dimensions to compare]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: analysis, competitive, strategy
---

# Analyze Competitors

## Overview

Generate a competitive positioning matrix and Blue Ocean Strategy canvas that compares your product against named competitors across key dimensions: features, pricing, target market, UX, strengths, and weaknesses. Surfaces differentiation opportunities and strategic white space.

## Workflow

1. **Read product context** -- Scan `.chalk/docs/product/` for the product profile (`0_product_profile.md`), JTBD docs, and any existing competitive analyses. If no product context exists, ask the user to describe their product before proceeding.

2. **Parse competitors and dimensions** -- Extract from `$ARGUMENTS` the competitor names and any specific dimensions the user wants compared. If no competitors are named, ask the user to list 2-5 direct competitors. If no dimensions are specified, use the defaults: core features, pricing model, target market, UX quality, integration ecosystem, go-to-market approach.

3. **Determine the next file number** -- Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

4. **Build the competitive matrix** -- For each competitor, analyze across every dimension. Use a consistent rating or description per cell. Be specific -- "freemium with $29/mo pro tier" not "has free plan."

5. **Create the strategy canvas** -- Describe a Blue Ocean Strategy canvas: list the competing factors on the X-axis and value level (low to high) on the Y-axis. Plot your product and each competitor. Identify factors where you can eliminate, reduce, raise, or create to find uncontested market space.

6. **Identify positioning insights** -- Summarize: where you are differentiated, where you are at parity, where competitors have an advantage, and where white space exists.

7. **Write the file** -- Save to `.chalk/docs/product/<n>_competitive_analysis.md`.

8. **Confirm** -- Share the file path and highlight the top 2-3 differentiation opportunities or competitive risks.

## Output

- **File**: `.chalk/docs/product/<n>_competitive_analysis.md`
- **Format**: Plain markdown with comparison table, strategy canvas description, and positioning insights
- **First line**: `# Competitive Analysis: <Your Product> vs. <Competitors>`

## Anti-patterns

- **Feature checklist without context** -- A grid of checkmarks tells you nothing about competitive dynamics. Every cell should describe the *quality* and *approach*, not just presence/absence.
- **Ignoring indirect competitors** -- Products in adjacent categories that solve the same job often matter more than direct feature competitors.
- **Stale data presented as current** -- If you do not have current information about a competitor, say so. Do not fabricate pricing or feature details.
- **Missing "so what"** -- A comparison table without positioning insights is just data. Always conclude with what the analysis means for product strategy.
- **Only comparing features** -- Pricing, distribution, brand, and go-to-market are often more decisive than feature parity. Compare across all strategic dimensions.
