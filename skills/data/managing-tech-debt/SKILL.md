---
name: managing-tech-debt
description: Help users manage technical debt strategically. Use when someone is dealing with legacy code, planning refactoring work, deciding between rewrites vs. incremental fixes, trying to get buy-in for tech debt reduction, or balancing new features with maintenance.
---

# Managing Tech Debt

Help the user manage technical debt strategically using insights from 18 product leaders.

## How to Help

When the user asks for help with tech debt:

1. **Understand the situation** - Ask about the nature of the debt (legacy systems, code quality, architectural limitations), how it's manifesting (slow velocity, incidents, inability to ship), and the business context
2. **Diagnose the urgency** - Determine if this is blocking critical business needs or a slower-burning issue
3. **Choose the right approach** - Help them decide between incremental improvement, targeted refactoring, or (rarely) a full rewrite
4. **Build the business case** - Help quantify the cost of the debt and communicate value to stakeholders

## Core Principles

### Rewrites almost never work
Camille Fournier: "Engineers notoriously, notoriously, notoriously, massively underestimate the migration time for old system to new system. By the way, you still have to support the old system while you're working on the new system." Full rewrites are traps. Prefer incremental evolution - uplift specific components rather than starting from scratch.

### Tech debt is product debt
Ebi Atawodi: "Infrastructure is the product. Period. I cannot build a skyscraper on a shaky foundation. So it is your problem too - it's not for the engineer to be barging on the door." Technical debt should be owned by PMs as "product debt," not treated as an engineering-only concern. Include it in your Top 10 Problems list.

### Startups should strategically take on debt
Gaurav Misra: "As a startup your job is to take on technical debt because that is how you operate faster than a bigger company." Debt is leverage - evaluate if a problem can be solved by a future hire rather than today. But monitor the "interest" - if maintenance takes 80-90% of time, you've run out of runway.

### Delete code more than you write it
Farhan Thawar: "We have a Delete Code Club. We can almost always find a million-plus lines of code to delete. Everything gets easier - the codebase loads faster, it's easier to understand." Create dedicated time or teams focused solely on removing unused code. Deletion improves velocity and clarity.

### Tech debt is visible to users
Matt Mullenweg: "You can see [tech debt] in the interface or how their products integrate with themselves." Fragmented UIs and poor integration between features are user-facing symptoms of accumulated debt. Look for inconsistencies to identify where debt has accumulated.

### Quantify the value of paying down debt
Casey Winters: "The most impactful projects are the hardest to measure, so they get chronically underfunded. Build custom metrics to show the value, run small tests that prove the worthwhile-ness of the investment." Create custom metrics and run experiments to demonstrate business value. Align with engineering and design to present a unified front.

### Fix bugs immediately, don't backlog them
Geoff Charles: "We don't have a bug backlog. We fix every bug once they're surfaced almost." Assign bugs directly to the engineer on call to ensure immediate pain awareness. Bug backlogs become graveyards.

### Debt ceilings innovation
Eeke de Milliano: "Sometimes teams are just getting bogged down by urgent work - too much tech debt, bugs, instability. There's no way they can focus on bigger, creative stuff if they're heads-down dealing with incidents all day." Diagnose when a team is stuck in a "hierarchy of needs" trap. Prioritize debt reduction to free up headspace for creative work.

### Tech debt is a champagne problem
Julia Schottenstein: "We would be so lucky to have tech debt because that means people are using the product. What we didn't need at launch was a distributed scheduler - we had no users." Build the simplest, most naive version first. Accept debt as a trade-off for getting product into users' hands.

### Plan for dark tunnels
Melanie Perkins: "We thought it would take six months... it took two years of not shipping any product." Major rewrites are "dark tunnels" that stall shipping. If you must do them, gamify the work to maintain team momentum during the long slog.

### Design for 1-2 years out
Austin Hay: "Think one to two years down the road about what we're going to need. When setting up tools, ask: 'What happens a year from now if I don't change anything?'" Implement foundational elements like SSO or proper data schemas early to avoid catastrophic migrations later.

## Questions to Help Users

- "Is this debt blocking critical business needs, or is it a slower-burning issue?"
- "What percentage of engineering time is going to maintenance vs. new features?"
- "Have you tried to estimate how long a rewrite would actually take? Who made that estimate?"
- "What would happen if you did nothing for another 6 months?"
- "Is there a way to incrementally improve this rather than rewriting?"
- "How would you quantify the cost of this debt to stakeholders?"

## Common Mistakes to Flag

- **Planning a full rewrite** - Rewrites almost never work as planned. They take 2-3x longer than estimated and you must support both systems simultaneously
- **Treating tech debt as engineering's problem** - This is product debt. PMs should own it alongside engineers
- **Letting bug backlogs accumulate** - Bug backlogs become graveyards. Fix immediately or decide not to fix at all
- **Over-engineering before product-market fit** - Debt is a champagne problem. Build naive solutions first and accept debt as the cost of learning
- **Not quantifying the cost** - Tech debt investments get underfunded because their value isn't measured. Build metrics and run experiments to prove ROI

## Deep Dive

For all 20 insights from 18 guests, see `references/guest-insights.md`

## Related Skills

- Technical Roadmaps
- Platform & Infrastructure
- Engineering Culture
- Evaluating Trade-offs
