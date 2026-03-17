---
description: Auto-prioritize unprioritized feedback
allowed-tools: Bash
---

# Prioritize Feedback

## Run

```bash
node F:/_CODE/shared-scripts/feedback/fetch-feedback.js prioritize --json
```

## Priority Criteria

**HIGH:** Article accuracy errors, template breakage, security issues, anti-spam filter failures, data loss risk
**MEDIUM:** Missing content, broken categories, CSS/skin issues, extension misconfiguration, SEO problems
**LOW:** Polish/cosmetic, edge cases, nice-to-haves, minor formatting

## Wiki Context

When prioritizing, consider the wiki's purpose:
- Article accuracy is critical - wrong technique descriptions could cause injury
- Template integrity affects every page that uses them
- Anti-spam is essential for a public wiki
- SEO matters for discoverability of flow arts content
- Skin/CSS issues affect readability for all visitors

## Workflow

1. Fetch unprioritized items
2. Analyze each with wiki context
3. Present table with recommendations
4. Get confirmation
5. Apply: `node F:/_CODE/shared-scripts/feedback/fetch-feedback.js <id> priority <level>`
