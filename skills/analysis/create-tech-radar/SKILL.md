---
name: create-tech-radar
description: Creates tech radar entries with opinionated but balanced technical analysis following the BYOR (Build Your Own Radar) structure. Use when the user wants to add a technology to the tech radar, assess a new tool/framework/platform, document technology recommendations, or evaluate whether to adopt/trial/assess/hold a technology.
---

# Tech Radar Entry Creation

Creates opinionated tech radar entries that provide actionable guidance on technology adoption decisions.

## When to Use

Activate this skill when users ask to:
- Add a technology to the radar
- Assess or evaluate a tool, framework, or platform
- Document technology recommendations
- Compare technologies for adoption decisions
- Update an existing radar entry's ring position

## Required Information

Gather these before generating:

1. **Title** - Technology name (e.g., "Bun", "htmx", "Kubernetes")
2. **Description** - Brief description (1-2 sentences)
3. **Quadrant** - Technology category (see below)
4. **Ring** - Recommendation level (see below)

## Optional Information

- **Tags** - Technology categorization tags
- **Date** - Assessment date (defaults to today)
- **Context** - Specific context for the recommendation

## Ring Definitions

Rings represent adoption recommendations with specific implications:

| Ring | Meaning | User Action | Content Tone |
|------|---------|-------------|--------------|
| **adopt** | Production-ready, proven | Use confidently for new projects | Confident, encouraging |
| **trial** | Promising, worth piloting | Evaluate for specific use cases | Cautiously optimistic |
| **assess** | Emerging, worth watching | Research and experiment only | Exploratory, measured |
| **hold** | Avoid or migrate from | Plan migration, no new adoption | Direct but fair |

### Ring-Specific Analysis Focus

**ADOPT:**
- Implementation best practices
- Production deployment guidance
- Long-term maintenance considerations
- Team training resources
- Success patterns from the ecosystem

**TRIAL:**
- When and where to pilot
- Success criteria for evaluation
- Comparison with established alternatives
- Risk mitigation strategies
- Fallback plan recommendations

**ASSESS:**
- Key questions to answer before adoption
- Evaluation criteria and metrics
- Community and ecosystem health indicators
- Research and prototyping guidance
- Timeline for reassessment

**HOLD:**
- Reasons for the hold recommendation
- Migration path to alternatives
- Risk assessment for existing usage
- Security and maintenance concerns
- Recommended replacements

## Quadrant Examples

| Quadrant | Description | Examples |
|----------|-------------|----------|
| **techniques** | Development practices and methodologies | TDD, pair programming, GitOps, IaC, trunk-based development |
| **tools** | Development and operations tools | Bun, Vite, Webpack, CI/CD platforms, linters |
| **platforms** | Infrastructure and deployment platforms | AWS, Kubernetes, serverless, edge computing |
| **languages-and-frameworks** | Programming languages and frameworks | Rust, TypeScript, React, Next.js, htmx |

## Generation Process

### Step 1: Gather Requirements

Ask the user for the required information. If they provide a technology name without other details, research and propose appropriate values.

### Step 2: Generate Opinionated Analysis

Create content that is:
- **Opinionated** - Take a clear position on the technology
- **Balanced** - Acknowledge both strengths and weaknesses
- **Evidence-based** - Support opinions with ecosystem signals
- **Actionable** - Provide concrete next steps

**Content Sections to Generate:**

1. Overview (ring-specific framing)
2. Key Features (factual capabilities)
3. Strengths (what it does well)
4. Weaknesses (honest limitations)
5. Use Cases (where it shines)
6. Ring Recommendation (with justification)
7. Ecosystem Assessment (community health)
8. Adoption Considerations (practical guidance)
9. Conclusion (maturity + future outlook)

### Step 3: Create Hugo Bundle

Create content at `content/tools/technology-slug/index.md`:

**Frontmatter (BYOR-compatible):**
```yaml
---
title: "Technology Name"
date: YYYY-MM-DD
draft: true
description: "Brief description for SEO and radar display"
quadrant: "quadrant-slug"
ring: "ring-slug"
tags:
  - tag1
  - tag2
---
```

### Step 4: Review

Present the draft to the user for review. **Never auto-publish** - always keep `draft: true` until explicit approval.

## Writing Guidelines

**Tone:** Opinionated but balanced and informed

**Do:**
- Provide technical depth and context
- Consider practical adoption implications
- Assess maturity and ecosystem support
- Be forward-looking but realistic
- Use evidence from real-world usage
- Acknowledge when context matters

**Don't:**
- Be purely opinionated without evidence
- Use hype-driven language
- Ignore potential drawbacks or limitations
- Be overly negative about technologies
- Make absolute statements without qualification
- Dismiss legitimate use cases

**Vocabulary:**
- adopt, trial, assess, hold
- maturity, ecosystem, production-ready
- trade-offs, considerations, implications
- community, governance, long-term viability

## Example Frontmatter

```yaml
---
title: "htmx"
date: 2025-12-26
draft: true
description: "Lightweight library for AJAX, CSS transitions, and WebSockets directly in HTML"
quadrant: "languages-and-frameworks"
ring: "trial"
tags:
  - javascript
  - html
  - hypermedia
  - ajax
---
```

## Validation

After generation, verify:
- Required frontmatter fields present
- Quadrant is valid value
- Ring is valid value
- Description is concise but informative
- Content has all required sections
- No H1 heading in content (title comes from frontmatter)

## Voice Learning

Record user feedback to improve future analysis:

```
Feedback location: .cody/project/library/style-docs/tech-radar-style.json

Record positive feedback for good patterns.
Record negative feedback for issues to avoid.
```

## File Locations

- **Tech radar entries:** `content/tools/{technology-slug}/index.md`
- **Style guidelines:** `.cody/project/library/style-docs/tech-radar-style.json`
- **Agent implementation:** `src/agents/tech-radar/tech-radar-agent.ts`

## Example Interaction

**User:** Add Bun to the tech radar

**Response Flow:**
1. Acknowledge the request
2. Ask which ring (or propose one with justification)
3. Confirm quadrant (likely "tools")
4. Ask for any specific context or tags
5. Generate the entry
6. Present for review with explanation of the analysis
