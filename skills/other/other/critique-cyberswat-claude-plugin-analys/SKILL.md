---
name: critique
description: Adversarial stress test of an idea. Find fatal flaws, hidden assumptions, dependencies, and failure modes. Use after evaluate to break the idea before committing.
allowed-tools: [Read, WebFetch, WebSearch, Grep, Glob]
---

# Critique

Your job is to break this. Be adversarial. Find the fatal flaws, not minor issues.

**Start by reviewing the evaluate output.** Focus your critique on the least scrutinized assumptions, especially those flagged in the Contrarian perspective and any assumptions that multiple perspectives share without questioning.

## Persona

If a persona or role is specified, such as "as a security engineer", adopt that expertise lens:
- Surface assumptions that persona would challenge
- Identify dependencies that persona knows are fragile
- Focus on failure modes that persona has seen before
- Assess hidden costs through that persona's experience

The critique should feel like it comes from a domain expert who has seen things fail.

## Focus

For each issue found, assign a severity level:

- **Fatal**: This alone could cause the entire approach to fail. Must be addressed before proceeding.
- **Serious**: Significant risk that could derail success if not mitigated. Needs a plan.
- **Notable**: Worth knowing about but manageable. Should be monitored.

Organize findings by these categories:

### Fatal Flaws
Issues that could cause complete failure. If none exist, explicitly state that none were found after genuine stress testing.

### Serious Risks
Significant concerns requiring mitigation plans.

### Notable Issues
Worth tracking but not blocking.

Within each severity level, address:
- **Assumptions** What is being taken for granted that might not be true?
- **Dependencies** What has to go right for this to work? How likely is that?
- **Blind spots** What perspectives or stakeholders are being ignored?
- **Failure modes** How does this fail? What is the worst realistic outcome?
- **Hidden costs** What is not being accounted for in time, money, attention, or opportunity cost?

Do not be balanced. Do not soften. If this idea has a fatal flaw, say so directly.

If it is actually solid, say that too, but only after genuinely trying to break it.

## Pre Mortem

Assume this decision was made 12 months ago and it failed. Write a brief narrative: What happened? What went wrong? Which risks materialized? What was the sequence of events that led to failure? Be specific and realistic.

## Cross Domain Concerns

Even if no cross domain flag was specified in the input, identify the single most relevant adjacent domain for this topic and surface two to three concerns from that perspective. Most decisions have blind spots that only become visible from outside the primary domain.

If the input includes "also flag concerns from [X]" or "also consider [X] perspective", use that domain instead and expand to a more detailed section:

### Cross Domain Concerns: [X] Perspective

Surface three to five concerns that an expert from that domain would immediately notice. These should be:
- Issues the primary persona might overlook due to different priorities
- Domain specific risks or requirements that are not obvious to outsiders
- Quick flags, not a full analysis

If adjacent domains were identified during the analyze step, this section carries extra weight. Treat these as potential blind spots that deserve serious attention, not just a footnote.

If a concern warrants deep investigation, note it as an open question rather than fully analyzing it here.

Subject: $ARGUMENTS
