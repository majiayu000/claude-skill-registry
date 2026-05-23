---
name: platform-infrastructure
description: Help users build and scale internal platforms and technical infrastructure. Use when someone is deciding whether to build vs buy tooling, designing developer platforms, creating shared services, or managing technical debt at scale.
---

# Platform Infrastructure

Help the user design and scale internal platforms and shared technical infrastructure using insights from 5 product and engineering leaders.

## How to Help

When the user asks for help with platform infrastructure:

1. **Understand the platform's purpose** - Ask whether they're building for internal developers, external partners, or both
2. **Assess organizational readiness** - Determine if they have the adoption and governance structures to support a platform
3. **Identify the leverage points** - Help them find where platform investment creates the most value multiplication
4. **Design for adoption** - Ensure the platform solves real developer problems, not theoretical ones

## Core Principles

### Abstract common capabilities into shared infrastructure
Daniel Lereya: "We actually stopped for the first time and say, 'What is the column like?' And we also organized all the product architecture around it... making the work of adding a new column just thinking about the specific." Scaling feature velocity requires abstracting repetitive components into a shared infrastructure so developers only focus on unique logic.

### Invisible infrastructure often matters most
Asha Sharma: "It wasn't the hundreds of features, it was all in the infrastructure and the platform... performance, reliability, privacy, safety, all of those things." The success of major platforms often depends on "invisible" qualities like reliability and speed rather than visible features.

### Plan for scale before you need it
Ivan Zhao: "During COVID, we just couldn't scale up our infrastructure. For the longest time, Simon's really good at don't do premature optimization... we're running off even the largest instance there is for Postgres." While avoiding premature optimization is good, infrastructure must be planned far enough ahead to avoid "doomsday" scenarios when usage spikes.

### Build discoverability into the architecture
Eli Schwartz: "If you create a categorized sitemap where you can say, 'These are all the questions on health and from the sitemap... then a search engine can navigate through the entire site, and all of the questions and answers are discoverable.'" For large-scale platforms, structural decisions like HTML sitemaps and internal linking are critical for search engine discoverability.

### Default to server-side tracking
Vijay: "The biggest mistake is setting up analytics using client side SDKs... start tracking events from your servers instead of from your clients." Server-side tracking is superior to client-side SDKs for data reliability, cross-platform consistency, and developer maintenance.

## Questions to Help Users

- "Who are the 'users' of this platform and what problems are they trying to solve today?"
- "What's the current developer experience pain point that's costing the most productivity?"
- "How will you measure whether this platform is actually being adopted?"
- "Is this a build vs buy decision, or should this remain a manual process for now?"
- "What's your 'doomsday clock' - when will current infrastructure hit its limits?"

## Common Mistakes to Flag

- **Building for the abstract future** - Creating capabilities based on anticipated needs rather than current developer pain
- **Platform without product ownership** - Treating infrastructure as a technical project without dedicated product management
- **Avoiding premature optimization until it's too late** - Not monitoring infrastructure limits to trigger scaling projects before failure
- **Client-side tracking by default** - Using browser SDKs instead of server-side event tracking
- **Ignoring the migration cost** - Building new platforms without accounting for the effort to move teams off existing solutions

## Deep Dive

For all 6 insights from 5 guests, see `references/guest-insights.md`

## Related Skills

- platform-strategy
- product-operations
- scoping-cutting
