---
name: strategist-cooperation
description: Guides effective collaboration with the strategist agent—a remote expert providing unbiased advice on complex architectural decisions, trade-offs, and problems where you're stuck or need outside perspective. The strategist cannot access the codebase.
---

# Strategist Cooperation

The strategist is a remote consultant offering fresh perspective on complex problems. They bring experience across many projects but cannot see your code.

## Session Continuity

The strategist can be **resumed** using the agent ID from a previous consultation. When resumed, the strategist retains full context from the conversation.

- **New consultation**: Start fresh when the problem is unrelated to previous work
- **Follow-up**: Use `resume` with the agent ID to continue with preserved context

```
Task tool:
  subagent_type: "advisor-skills:strategist"
  resume: "<agent-id-from-previous-consultation>"
  prompt: "I explored the codebase and found an existing session manager.
           How should we integrate caching with it?"
```

If starting a **new consultation** on a related topic (without resume), provide complete context since the strategist won't have prior memory.

## When to Consult

**Good fit:**
- Architecture decisions with multiple valid approaches
- Going in circles after multiple failed attempts
- Trade-off analysis between competing options
- Need validation before significant investment
- Lost objectivity, need fresh eyes

**Poor fit:**
- Straightforward implementation tasks
- Code-level questions (syntax, API usage, debugging)
- Questions requiring codebase access ("where is X defined?")

## Before Consulting: Explore First

The strategist provides strategic advice; you must ground it in your codebase reality. Before consulting:

1. Search for existing implementations of similar functionality
2. Understand current architecture patterns and constraints
3. Check dependencies and technical limitations
4. Note what's been tried and why it failed

## Preparing Context

**Avoid biasing the strategist.** You're seeking fresh perspective—don't contaminate it by presenting your preferred solution or framing the problem to lead toward a conclusion. State facts and constraints neutrally.

```
Biased:   "We need to add Redis for caching because our current approach
           is clearly inadequate and Redis is industry standard."
Neutral:  "Token validation hits the database on every request, causing
           latency under load. We're evaluating caching options."
```

Since the strategist cannot see code, translate technical details into concepts:

**Instead of:** "The `UserService.authenticate()` calls `TokenManager.validate()` hitting the database each request"

**Write:** "Authentication validates tokens via database query on every request, causing performance issues under load"

**Include:**
- Problem summary in plain language
- Constraints (team size, timeline, technical limitations)
- What you've tried and why it didn't work
- A specific question or decision to address

### Example Context

```
Problem: Authentication validates tokens against the database on every
request, degrading performance under load.

Constraints:
- 3-person team, limited DevOps expertise
- Must maintain current security guarantees
- Cannot add significant infrastructure complexity

Tried:
- Simple in-memory cache—token revocation became inconsistent
- Considered Redis—team lacks operational experience

Question: What caching strategies balance performance, security, and
operational simplicity for our situation?
```

## Invoking the Strategist

```
Task tool:
  subagent_type: "advisor-skills:strategist"
  description: "Architecture advice on [topic]"
  prompt: [Your prepared context and question]
```

## Handling Advice

Strategist recommendations are guidance, not implementation specs.

1. **Validate against codebase** — Check if existing code partially implements suggestions
2. **Adapt to local constraints** — Modify for technical debt, team conventions, dependencies
3. **Re-consult if needed** — If advice conflicts with reality, provide that context and ask for alternatives

## Ongoing Collaboration

Treat the strategist as a partner, not a one-shot oracle. **Don't ask once and disappear**—but also don't over-consult.

**Come back when:**
- Discoveries change the problem — "I found X, which invalidates our assumption"
- You hit a strategic blocker — "The approach won't work because of Y constraint"
- You need to pivot direction — "Based on findings, I'm considering a different path"

**Don't come back for:**
- Implementation details you can figure out
- Minor obstacles that don't change the strategy
- Validation of routine progress — just keep going

The goal is meaningful checkpoints, not constant hand-holding. Report back when your findings would change the strategist's advice.

## Iterative Consultation

Use `resume` to continue conversations efficiently across multiple rounds.

**Pattern:**
1. Initial consultation → Get direction and framework (save the agent ID)
2. Explore/implement → Discover specifics in your codebase
3. Follow-up → Resume the agent, share findings, ask about challenges
4. Refine → Adjust and implement
5. Repeat as needed

### Example: Iterative Flow

**Round 1:** (new consultation)
```
Problem: Token validation hits database on every request, causing
performance issues under load (~500 req/sec).

Constraints: Small team, can't add Redis, need simple solution.

Question: What caching approaches should we consider?
```
*Strategist suggests TTL-based in-memory caching with fallback validation.*
*Agent ID: `abc-123` returned.*

**You explore codebase, find existing session manager.**

**Round 2:** (resume with agent ID `abc-123`)
```
I've explored our codebase and found we have an existing session
manager that tracks user state.

Question: How should we integrate token caching with our existing
session infrastructure rather than building separate cache?
```
*Strategist provides integration guidance (already knows the original problem).*

**You implement, discover edge case with immediate revocation.**

**Round 3:** (resume with agent ID `abc-123`)
```
I've implemented caching but discovered our compliance requires immediate
token revocation (within 1 second). TTL-based caching can't guarantee this.

Question: How can we handle immediate revocation while keeping cache benefits?
```
*Strategist suggests event-driven invalidation pattern (full context preserved).*

## Common Mistakes

**Vague problem statements**
- Bad: "Our system is slow. What should we do?"
- Good: Describe metrics, what you've measured, where bottlenecks appear, constraints

**Asking for implementation details**
- Bad: "What Node.js caching library should we use?"
- Good: Ask about caching strategy and trade-offs for your constraints

**Multiple unrelated questions**
- Bad: "Should we use microservices? Also, what testing strategy? And deployment?"
- Good: One focused question per consultation

**Skipping post-consultation validation**
- Bad: Implement advice immediately without checking codebase fit
- Good: Validate against actual code, adapt to local constraints, re-consult if conflicts arise

**Ghosting when things change**
- Bad: Discover something that invalidates the advice, but keep implementing anyway
- Good: Report back when findings would change the strategist's recommendations

**Forgetting to resume**
- Bad: Starting a new consultation and manually re-explaining previous context
- Good: Use `resume` with the agent ID to continue with full context preserved

**Leading the witness**
- Bad: "Redis is clearly the right choice here, right?" or "Our architecture is fundamentally broken"
- Good: Present facts neutrally, let the strategist form their own conclusions
