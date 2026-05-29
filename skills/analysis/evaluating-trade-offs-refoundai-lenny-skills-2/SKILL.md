---
name: evaluating-trade-offs
description: Help users make better decisions between competing options. Use when someone is weighing pros and cons, comparing alternatives, struggling with a difficult choice, deciding between speed and quality, or asking "should we do X or Y?"
---

# Evaluating Trade-offs

Help the user make clearer decisions between competing options using frameworks and mental models from 40 product leaders.

## How to Help

When the user asks for help evaluating trade-offs:

1. **Understand the decision context** - Ask what they're optimizing for (short-term vs. long-term, growth vs. quality, speed vs. thoroughness) and what makes this decision difficult
2. **Identify the real constraints** - Help distinguish between actual constraints and assumed ones. Ask "What would you do if [constraint] weren't an issue?"
3. **Surface hidden costs** - Help quantify the full cost of each option, including maintenance burden, opportunity cost, and second-order effects
4. **Apply the right framework** - Use weighted criteria matrices for complex multi-factor decisions, or simple "would I start this today?" tests for continuation decisions

## Core Principles

### Optimize for order-of-magnitude, not precision
Alex Komoroske: "It doesn't really matter if it's 1,000 or 1,001, who cares? It's orders of magnitude larger than the alternative, and so it is better." Don't waste effort on false precision in uncertain environments - focus on whether one option is dramatically better, not marginally better.

### Apply the "would I start this today?" test
Annie Duke: "If you wouldn't start this today, then that means that everything that you're putting into this going forward is the actual waste." When evaluating whether to continue a project, ignore sunk costs entirely. The only relevant question is whether you'd begin this effort with today's knowledge.

### Think more, ship better
Anuj Rathi: "Most experiments should be thought experiments. They should not even be tried out because they're obviously going to fail." Don't default to "let's just try it" - rigorous upfront thinking eliminates weak ideas before they consume engineering resources.

### Accept "worse first" for long-term gains
Graham Weaver: "Everything you want is on the other side of worse first." Meaningful change requires accepting short-term decline. Ask what your 5-year future self would want, not what makes tomorrow easier.

### Create decision tenets to eliminate recurring debates
Bob Baxley: "Tenets are really decision-making tools... you sort of make a rule for yourself." Identify debates your team has repeatedly and create a tenet to decide the direction once. Good tenets are specific enough that someone could reasonably argue the opposite.

### Quantify countervailing metrics
Ronny Kohavi: "Here's the money that we generate from the emails. Here's the money that we're losing on long-term value. What's the trade-off?" Assign dollar values to negative user actions (unsubscribes, churn) to make objective trade-offs against short-term gains.

### Use a weighted criteria matrix
Nicole Forsgren: "Identify the criteria that are most important to you... give everything a score, and just multiply it out." Create a decision-making spreadsheet with options as rows and weighted criteria as columns. The process often reveals the answer before the math is finished.

### Present clear "either/or" choices to leadership
Geoff Charles: "Be very clear with the tradeoffs... present those tradeoffs back to your leadership team. Here's what we're doing and here's what we're not doing." Communicate what the team is NOT doing as clearly as what they are doing. Present a "menu" of options to force a decision.

### Separate "can" from "should"
John Cutler: "Some people are just locked into the can. They're uber pragmatic... others ask 'What should we do here?'" Don't let feasibility constraints dominate strategic thinking. Explicitly ask what you should do if technical debt weren't an issue.

### Diagnose with data, treat with design
Julie Zhuo: "Data is not a tool that's going to tell you what you should build... but it can tell you if you have a problem." Use data to identify problems and gaps, but rely on design and intuition to invent solutions.

### Beware the cost of analysis itself
Stewart Butterfield: "The cost of doing the analysis was this much. So it's guaranteed to be a loser." Evaluate whether the person-hours spent analyzing a decision exceed the maximum possible upside of the improvement.

### Identify who loses
Ramesh Johari: "Many of the changes that are most consequential create winners and losers." When launching a feature, explicitly identify who will lose and decide if the winners provide more net value to the ecosystem.

## Questions to Help Users

- "What are you optimizing for - today, this quarter, or this year?"
- "If you weren't already committed to this, would you start it today?"
- "What's the full 'all-in' cost of each option, including maintenance and opportunity cost?"
- "Is this decision reversible or a one-way door?"
- "Who loses if you choose option A? Is that trade-off acceptable?"
- "What would your 5-year future self wish you had done?"

## Common Mistakes to Flag

- **False precision** - Spending excessive time distinguishing between options that are only marginally different when the real question is order-of-magnitude
- **Sunk cost fallacy** - Continuing a failing path because of what's already been invested rather than evaluating future value
- **Analysis paralysis** - When the cost of deciding exceeds the value difference between options
- **Ignoring second-order effects** - Not accounting for maintenance burden, feature creep, or organizational complexity that comes after launch
- **Defaulting to your skillset** - As Bret Taylor notes, "If you're a great engineer, the answer to almost every problem is engineering... you probably should question it"

## Deep Dive

For all 42 insights from 40 guests, see `references/guest-insights.md`

## Related Skills

- Prioritizing Roadmap
- Running Decision Processes
- Scoping and Cutting
- Managing Tech Debt
