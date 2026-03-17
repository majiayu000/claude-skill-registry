---
name: strategic-mindset
description: Assesses whether code reflects strategic or tactical thinking. Use when the user asks to evaluate design investment, when code was written under time pressure, when a developer consistently produces working code that degrades the system, or when assessing whether a codebase invests in design. Checks the 10-20% investment rule and tactical tornado patterns.
argument-hint: "[file, module, or codebase area]"
metadata:
  allowed-tools: Read, Grep
---

# Strategic Mindset Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file, module, or codebase area. Read the target code first, then apply the checks below.

> "The first step towards becoming a good software designer is to realize that working code isn't enough." — John Ousterhout, _A Philosophy of Software Design_

Evaluate whether code invests in design or just gets the job done.

## When to Apply

- When reviewing code written under time pressure
- When assessing technical debt in a codebase
- When a developer consistently produces working code that degrades the system
- When deciding how much time to invest in a design

## Core Principles

### Strategic vs. Tactical

#### Tactical Programming

Get it working, move on. Each shortcut is locally defensible. **This is precisely what makes it dangerous: it doesn't feel dangerous.**

#### Strategic Programming

Produce a great design that also happens to work. Two modes:

- **Proactive**: Explore alternatives before implementing. Write documentation before code to surface interface problems early.
- **Reactive**: When you discover a design problem, fix it.

> "Ideally, when you have finished with each change, the system will have the structure it would have had if you had designed it from the start with that change in mind." — John Ousterhout, _A Philosophy of Software Design_

**Test:** After this change, is the system easier or harder to work with for the next developer?

### The Unit of Development Should Be an Abstraction

Working in abstraction-sized chunks lets you consider trade-offs and arrive at general-purpose solutions. Once you discover the need for an abstraction, design it all at once. Don't create it in pieces over time. Working in test-sized chunks (write one test, make it pass) encourages tiny increments that never step back for the big picture. **TDD risks becoming tactical programming with a disciplined veneer**. Each increment is responsible, but the aggregate drifts toward specialization because no step encourages holistic design thinking.

### The 10-20% Investment Rule

- Not all upfront. Spread across the project
- Not separate "refactoring sprints." Woven into every task
- Each task should leave the system slightly better than it found it

Crossover point estimated at 6-18 months, after which design quality saves more time than investments cost. (Ousterhout calls this "just my opinion" with "no data to back it up.")

#### The Slippery Slope

Once you start cutting corners, it quickly becomes the default. "Add a TODO" and "make a backlog ticket" are how shortcuts you should have never taken become permanent. Tactical code is extremely difficult to fix after the fact and the payoff for good design comes quickly enough that cutting corners may not even save time on the current task.

Good software design makes every collaborator more effective. Humans, agents and subagents all produce better work in less time with fewer prompts/tokens when the code they're building on is clean. Bad design does the opposite: every contributor spends more time fighting the system than improving it, and their output degrades the system further.

### Design It Twice

Before committing to any significant design, generate at least two fundamentally different approaches and compare on concrete criteria. See the **design-it-twice** skill for the full procedure and comparison checklist.

### Tactical Tornado

A developer who produces impressive output by cutting design corners. **The damage is invisible**, or worse, looks like inefficiency from whoever follows them. The causal chain doesn't surface naturally.

Signs in code:

- Quick fixes layered on quick fixes
- Copy-paste with minor modifications instead of generalization
- "It works" treated as sufficient
- Undocumented dependencies

### Zero Tolerance

**Each shortcut makes the next one easier to justify.** The first accepted shortcut sets a precedent. The second cites the first. Selective tolerance is normalization in progress.

This doesn't mean over-engineer. It means: do the simple, clean thing instead of the hacky thing.

## Review Process

1. **Assess approach**: Strategic or tactical?
2. **Evaluate investment**: Did this change improve the system beyond the immediate requirement?
3. **Scan for tactical patterns**: Copy-paste, quick fixes, missing abstractions?
4. **Project forward**: If the next 10 changes follow this pattern, what happens?
5. **Recommend**: Specific investments with estimated effort

Red flag signals for strategic mindset are cataloged in **red-flags** (Tactical Momentum, Repetition).
