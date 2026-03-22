---
name: financial-modeling
description: Consolidated financial modeling skill aggregating Discounted Cash Flow (DCF), Leveraged Buyout (LBO), Merger Modeling, and 3-Statement financial projections.
---

# Financial Modeling Knowledge Base

This parent skill aggregates rigorous qualitative and quantitative modeling instructions for the `quant-developer` agent. By integrating the sub-skills below, the agent can structure complex, multi-statement forecasts and perform advanced valuation tasks.

## Available Sub-Skills

- **[DCF Model](skills/dcf-model/SKILL.md):** Instruction sets and templates for building intrinsic valuations using Discounted Cash Flows.
- **[LBO Model](skills/lbo-model/SKILL.md):** Private equity leveraged buyout modeling covering debt schedules, IRR, and MoM return analysis.
- **[Merger Model](skills/merger-model/SKILL.md):** M&A accretion/dilution analysis, purchase price allocation, and pro-forma balance sheets.
- **[3-Statements](skills/3-statements/SKILL.md):** Standard income statement, balance sheet, and cash flow historical extraction and projection protocols.

## Integration Notice
These sub-skills were ported from the specialized `financial-services-plugins` repository to fortify the baseline reasoning capabilities of the `quant-developer` agent. Ensure that assumptions (e.g., WACC, tax rates) are properly isolated when running backtests or algorithmic models based on these fundamental outputs.
