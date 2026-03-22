---
name: create-gtm-brief
description: Create a go-to-market brief with positioning, messaging, and launch plan when the user asks to plan a launch, create a GTM strategy, or write a go-to-market plan
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[feature or product to create a GTM brief for]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: product, go-to-market, strategy
---

# Create GTM Brief

## Overview

Generate a go-to-market brief covering positioning (Geoffrey Moore format), key messages per audience, launch tier classification, enablement checklist, and timeline. Aligns product, marketing, sales, and support around a coordinated launch.

## Workflow

1. **Read product context** -- Scan `.chalk/docs/product/` for the product profile, PRD for the feature being launched, competitive analysis, and any existing GTM materials. Understand the product positioning and target users before planning the launch.

2. **Parse the launch scope** -- Extract from `$ARGUMENTS` the feature or product to create a GTM brief for. If unspecified, ask the user to name the feature and its target launch timing.

3. **Determine the next file number** -- Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

4. **Write the positioning statement** -- Use Geoffrey Moore's format: "For [target customer] who [need/opportunity], [product name] is a [category] that [key benefit]. Unlike [primary competitor], our product [primary differentiation]."

5. **Define key messages per audience** -- Write 2-3 key messages tailored to each audience:
   - End users (focus on value and ease)
   - Technical buyers / developers (focus on capabilities and integration)
   - Business decision makers (focus on ROI and risk reduction)
   - Internal teams (focus on what changed and how to support it)

6. **Classify the launch tier**:
   - **Silent**: Ship it, update docs, no announcement (bug fixes, minor improvements)
   - **Soft**: Blog post, changelog entry, email to affected users (incremental features)
   - **Hard**: Full campaign, press, event, coordinated cross-functional launch (major features, new products)

7. **Build the enablement checklist** -- What must be ready before launch:
   - Documentation: user docs, API reference, migration guide
   - Support: runbooks, FAQ, escalation path, training
   - Sales: talk track, demo script, competitive positioning
   - Engineering: monitoring, feature flags, rollback plan

8. **Draft the timeline** -- Key milestones from now to launch and post-launch review.

9. **Write the file** -- Save to `.chalk/docs/product/<n>_gtm_brief_<feature-slug>.md`.

10. **Confirm** -- Share the file path and highlight any enablement gaps that need to be resolved before launch.

## Output

- **File**: `.chalk/docs/product/<n>_gtm_brief_<feature-slug>.md`
- **Format**: Plain markdown with positioning statement, audience messages, launch tier, enablement checklist, and timeline
- **First line**: `# GTM Brief: <Feature Name>`

## Anti-patterns

- **Positioning without differentiation** -- "We are the best solution for X" is not positioning. The Geoffrey Moore format forces you to name the competitor and state how you are different. Do not skip this.
- **One message for all audiences** -- Developers care about API design; executives care about ROI. Reusing the same message for every audience means it resonates with none.
- **Hard launch for everything** -- Not every feature deserves a full campaign. Over-launching fatigues your audience and dilutes impact. Match the launch tier to the significance of the change.
- **No enablement checklist** -- Launching a feature that support cannot explain, sales cannot demo, and docs do not cover creates a poor experience. Every launch needs an enablement check.
- **Missing post-launch review** -- The timeline should include a post-launch review milestone to assess what worked and capture learnings.
