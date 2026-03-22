---
name: press-release-copy
description: Writes a professional launch press release with headline, dateline, summary, quotes, specs, pricing, availability, and media info.
---

# Press Release Copy

This skill composes a standard PR announcement optimized for crowdfunding product launches.

## Input Variables
- [BRAND_BIBLE]
- [PRODUCT_BIBLE]
- [LAUNCH_DETAILS]: dates, funding milestones, pricing

## The Protocol
1. Headline and subhead with core value.
2. Dateline and lead paragraph summarizing launch.
3. Founder quote and supporting quote.
4. Product overview: specs and benefits.
5. Pricing, perks, and availability timeline.
6. Boilerplate and media contact.

## Output Instructions
Render into `templates/press-release-copy.md`. Keep AP-style conventions where applicable.



## Integration & Technical Specs

### API Specification
- **ID**: `press-release-copy`
- **Path**: `skills/press-release-copy/templates/press-release-copy.md`
- **Context**: Part of *Continual Interest*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `press-release-copy.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate press-release-copy
```
