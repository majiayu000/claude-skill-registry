---
name: regenerate-merged-rule-lists
description: Regenerate aggregated *Merged.list files from their source headers in this repo. Use when refreshing upstream sources or rebuilding merged rule lists.
---

# Regenerate Merged Rule Lists

## Overview

Regenerate `*Merged.list` files from the sources listed in their headers and keep the metadata intact.

## Workflow

- Open the target `*Merged.list` and read the header to identify source URLs and expected format.
- Fetch each source and merge the rules into a single list, preserving the expected order.
- Keep the header format consistent; update timestamps, counts, and source lines to match the new output.
- Ensure all rule lines use Clash classical format and keep one rule per line.

## Guardrails

- Avoid manual edits to merged lists unless you are regenerating from sources.
- Do not remove or rewrite the source header format; keep it consistent across updates.

## Quick checks

- Verify the first lines are the header with sources and update time.
- Spot-check a few entries to confirm correct formatting and no obvious truncation.
