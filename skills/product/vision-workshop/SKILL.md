# Vision Workshop Skill

> Version: 1.0.0
> Compiler: manual
> Last Updated: 2026-01-26

Interactive workshop for capturing product/project vision using the Product Vision Board methodology, producing a complete planning/vision.org artifact.

## When to Activate

Use this skill when:
- Creating a vision for a new project
- Defining or refining product vision
- Running a vision workshop session
- Starting a new project and need to establish "what are we building and why"
- Working with planning/vision.org template

## Methodology

**Chosen Methodology:** Product Vision Board (Roman Pichler)

**Rationale:** Selected based on research comparing Product Vision Board, PR/FAQ, Lean Canvas, and elevator pitch formats.

Why Product Vision Board wins for small teams:
1. Balances aspiration (vision) with pragmatics (strategy) on one page
2. Can be completed in 1-2 hours, not days (unlike PR/FAQ)
3. Explicitly designed for validation and iteration
4. Doesn't require narrative writing skill
5. Includes business goals without full business model complexity

### Alternatives Considered

| Methodology | Reason Not Selected | When Appropriate |
|-------------|---------------------|------------------|
| PR/FAQ (Amazon Working Backwards) | Time-intensive (hours to days); requires strong writing skill; overkill for solo/small teams | Complex products needing stakeholder alignment across large organizations |
| Lean Canvas | More business-model focused than vision-focused; present-state rather than aspirational | Business model validation, startup pitch preparation |
| Elevator Pitch / Vision Statement | Too compressed for strategic decision-making; doesn't guide product decisions | Communication tool after vision is already clear internally |

## Core Principles

### 1. WHAT Not HOW

Vision captures outcomes and value, never implementation details.

*Implementation changes; value proposition should be stable. Mixing in implementation constrains future solutions.*

**Test:** Could you describe this to someone in 1922 without referencing technology?

### 2. Specificity Over Generality

Prefer "Python developers building data pipelines" over "developers".

*Generic visions provide no decision guidance; anyone could copy them. Specificity enables focus.*

**Test:** Could a competitor copy this exact statement unchanged?

### 3. Testable Assumptions

Every element of the vision should be falsifiable.

*Visions that can't be proven wrong can't guide learning. Testability enables iteration.*

**Test:** How would you know if this assumption is wrong?

### 4. Anti-Goals Are Essential

Explicitly state what you are NOT building, even if asked.

*Scope creep starts when boundaries are unclear. Anti-goals provide "no" justification.*

**Test:** Can you point to this document when declining a feature request?

### 5. Inspiration Matters

Vision must motivate, not just inform.

*Visions without emotional resonance get ignored. People commit to what moves them.*

**Test:** Would you tell your family this is what you do? Would they care?

### 6. Progress Over Perfection

A good-enough vision now beats a perfect vision never.

*Vision will evolve as you learn. Waiting for perfection is procrastination.*

**Test:** Is this clear enough to make decisions and start validating?

---

## Workflow

**Output:** planning/vision.org with all sections populated from workshop

### Phase 1: North Star

**Question:** What world are we creating? What positive change do we want to see?

Establish the aspirational goal that motivates all subsequent work. One inspiring sentence describing the future state you're working toward.

**Good Examples:**
- "Every developer ships with confidence, knowing their code works."
- "Anyone can build a mobile app without writing code."
- "Teams spend time on creative work, not manual processes."

**Weak Examples:**
- "To be the best in our industry." (generic, not inspiring)
- "Increase revenue by 50%." (that's a goal, not a vision)
- "Build a great product." (says nothing specific)

**Validation:**
- [ ] Is it one sentence?
- [ ] Does it describe a future state (not an activity)?
- [ ] Is it inspiring enough to motivate during hard times?
- [ ] Is it specific to your project (not generic)?

### Phase 2: Target Users

**Question:** Who will use this? Who benefits indirectly?

Define primary and secondary users with enough specificity to guide decisions.

**Primary Users:** Who will interact with this daily? Be specific - not "developers" but "backend developers at startups building APIs."

Specificity checklist:
- Role/job title
- Organization type/size
- Context of use
- Current constraints or frustrations

**Secondary Users:** Who benefits indirectly? Managers who see reports, customers who benefit from improved primary user work.

**Warning Signs of Too-Generic:**
- "Everyone", "All developers", "Any business"
- No mention of context, constraints, or pain
- Could describe any product's users

**Validation:**
- [ ] Is the primary user specific enough to make decisions?
- [ ] Would you recognize this person if you met them?
- [ ] Are there constraints or context mentioned?

### Phase 3: Core Problem

**Question:** What problem does this solve that matters enough to act on?

Articulate the pain point or unmet need clearly enough to validate.

**Good Problem Statements:**
- "Developers spend 40% of their time debugging configuration issues instead of writing features."
- "Small teams can't afford enterprise tools but need the same capabilities."

**Weak Problem Statements:**
- "People need better tools." (vague, generic)
- "Our competitors don't have this." (not user-centered)
- "We want to build this because it's interesting." (not a problem)

**Test:** If you told this problem to a stranger in your target audience, would they nod vigorously?

**Validation:**
- [ ] Is the problem concrete and specific?
- [ ] Is there evidence the problem exists (not just assumption)?
- [ ] Is it important enough to motivate action?

### Phase 4: Value Proposition

**Question:** Why would someone choose this over alternatives or doing nothing?

Articulate the compelling reason to switch from the current approach.

Consider:
- What are current alternatives (including "doing nothing")?
- Why are those alternatives inadequate?
- What unique value does this provide that alternatives don't?

**Good Value Propositions:**
- "Get the power of enterprise CI/CD without the enterprise price or complexity."
- "Ship features in hours instead of weeks, with built-in best practices."

**Weak Value Propositions:**
- "Better than the competition." (vague, unverifiable)
- "Has more features." (features aren't value)
- "Uses cutting-edge technology." (implementation, not value)

**Test:** Why would someone go through the pain of switching to this?

**Validation:**
- [ ] Does it articulate why someone would switch?
- [ ] Is it an outcome, not a feature list?
- [ ] Is it differentiated from alternatives?

### Phase 5: Standout Capabilities

**Question:** What 3-5 capabilities most directly solve the core problem?

Define key differentiators (NOT a feature list) that deliver the value.

Capabilities are NOT features. Features are implementations; capabilities are outcomes.

| Feature | Capability |
|---------|------------|
| YAML configuration files | Configuration that works across any environment without modification |
| WebSocket real-time sync | Real-time collaboration without sync conflicts |

**Constraints:**
- Minimum 3 capabilities
- Maximum 5 capabilities
- Each must connect to the core problem

**Warning:** If you have more than 5, you're probably listing features or you lack focus.

**Validation:**
- [ ] Are there 3-5 capabilities (not more, not fewer)?
- [ ] Are they capabilities (outcomes) not features (implementations)?
- [ ] Does each connect to solving the core problem?

### Phase 6: Success Criteria

**Question:** How will we know this succeeded? What metrics move?

Define BOTH business and user success metrics.

**Business Success:** How does the organization benefit?
- Revenue, cost reduction, market share, retention
- Must be measurable, not vague

**User Success:** How does the user's life improve?
- Time saved, errors reduced, capability gained
- Should be something users would confirm if asked

**Good Criteria:**
- "50% reduction in time from idea to deployed feature"
- "Users complete complex tasks in half the time with fewer errors"
- "90% of users complete onboarding without support intervention"

**Weak Criteria:**
- "Users are happy" (how do you measure?)
- "Product is successful" (circular)
- "Better than before" (compared to what baseline?)

**Validation:**
- [ ] Is there at least one business metric?
- [ ] Is there at least one user metric?
- [ ] Are metrics measurable and specific?

### Phase 7: Anti-Goals

**Question:** What are we deliberately NOT doing, even if someone asks?

Explicitly capture scope exclusions to prevent feature creep.

Anti-goals are things you COULD do but WON'T do. They're not obvious exclusions - they're tempting extensions you're deliberately avoiding.

**Good Anti-Goals:**
- "We will not support on-premise deployment, even for enterprise customers."
- "We will not build a mobile app; this is desktop-first."
- "We will not compete on price; we're premium."

**Weak Anti-Goals:**
- "We won't do things that are bad." (obvious)
- "We won't violate user privacy." (that's a requirement, not an anti-goal)
- "We won't build things users don't want." (circular)

**Test:** When someone asks for something in this list, you can point here and say "no, we decided not to do that."

**Validation:**
- [ ] Are there at least 2 anti-goals?
- [ ] Are they specific enough to actually exclude things?
- [ ] Could they reasonably be requested features/directions?

### Phase 8: Synthesis and Validation

**Question:** Is this vision complete, consistent, and clear enough to proceed?

Update planning/vision.org with all captured content:
- North Star
- Target Users (Primary and Secondary)
- Core Problem
- Value Proposition
- Standout Capabilities (3-5 items)
- Success Criteria (Business and User)
- What This Is NOT (anti-goals)
- Open Questions (if any surfaced during workshop)

**Final Validation:**
- [ ] All sections populated (no [REPLACE] markers remaining)?
- [ ] Vision passes the 60-second explanation test?
- [ ] Team members would give the same summary if asked?
- [ ] Biggest risk/assumption identified for validation?

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| Start with Why | User is jumping to features or implementation | Redirect to North Star - "Before we talk about how, let's clarify what future we're creating" | Premature implementation focus leads to building the wrong thing well |
| Specificity Prompt | User gives generic answers ("developers", "better experience") | Ask "Can you give me a specific example?" or "Who specifically? In what context?" | Generic visions provide no decision guidance |
| Problem-Value Link | Value proposition doesn't connect to problem | Ask "How does this specifically address the core problem we identified?" | Disconnected value propositions signal fuzzy thinking |
| Capability vs Feature Check | User lists features in standout capabilities | Ask "That sounds like a feature - what outcome does it enable?" | Features are implementation; capabilities are value. Keep vision at capability level |
| Anti-Goal Mining | User struggles to identify anti-goals | Ask "What have you been tempted to add but decided against? What would be scope creep?" | Anti-goals are often already implicit; this makes them explicit |
| Validation Planning | Workshop complete | Ask "What's your biggest assumption? How would you test it quickly?" | Vision is hypothesis; validation is how you learn if it's right |

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Empty Platitude | Vision filled with buzzwords ("excellence", "synergy") provides no decision-making guidance; gets ignored | Apply competitor test - if rival could use it unchanged, it's too generic |
| Vision-Action Disconnect | Compelling vision that exists only as wall art destroys credibility; hypocrisy worse than no vision | Before major decisions, explicitly ask "How does this advance our vision?" |
| Founder Imposition | Vision created in isolation lacks ownership and gets passive resistance | Involve stakeholders in creation; validate before finalizing |
| Scope Miscalibration | Too broad = no focus; too narrow = obsolete quickly | Vision should be abstract enough for flexibility, specific enough for prioritization |
| Missing Emotional Resonance | Logically sound but uninspiring visions get ignored; no discretionary effort | Focus on outcomes for humans, not organizational metrics |
| Temporal Confusion | Confusing vision (future state) with mission (current activities) loses long-term guidance value | Ask "If we fully succeeded, what would the world look like?" |
| Consensus Paralysis | Trying to make everyone happy results in a vision that says everything and therefore nothing | Leadership decides (with input); set deadline and stick to it |

---

## Quality Checklist

Before completing, verify:

- [ ] North Star is one inspiring sentence (not a paragraph)
- [ ] Primary target user is specific enough to recognize
- [ ] Core problem has evidence of existence (not just assumption)
- [ ] Value proposition articulates why someone would switch
- [ ] 3-5 standout capabilities defined (not features)
- [ ] Business success metric is measurable
- [ ] User success metric is measurable
- [ ] At least 2 specific anti-goals documented
- [ ] Vision passes 60-second explanation test
- [ ] Biggest risk/assumption identified for validation
- [ ] planning/vision.org updated with all content
- [ ] No [REPLACE] placeholders remaining

---

## Examples

### Complete Vision Workshop for a CLI Tool

**Workshop Flow:**

Agent: Let's create a vision for your project. We'll use the Product Vision Board methodology - a structured approach that captures vision and strategy in about an hour.

First, let's start with the North Star. What world are you trying to create? What positive change do you want to see?

User: I want developers to stop wasting time on manual deployment tasks.

Agent: Good start! Let me help you make that more inspiring. Right now it's problem-focused ("stop wasting time"). Can we reframe it as the positive state? Something like "Developers spend their time on creative work, not deployment mechanics"?

User: Yes, that's better. "Developers spend their creative energy on code, not infrastructure."

Agent: That's a strong North Star. Let's capture it.

Now, who are your target users? Be specific - not just "developers" but what kind, in what context, with what constraints?

User: Developers at startups who don't have dedicated DevOps but need production deployments.

Agent: Good specificity! Any particular tech stack or size of team?

User: Early-stage startups, 2-10 developers, using cloud platforms like AWS or GCP.

Agent: Perfect. That's specific enough to make decisions. Now, what's the core problem? What pain are they experiencing?

User: They spend hours configuring CI/CD, managing secrets, debugging failed deployments - time they should spend shipping features.

Agent: That's concrete and relatable. Have you validated this is a real problem?

User: Yes, I've talked to 5 startup CTOs and all of them mentioned deployment complexity as a top-3 pain point.

Agent: Excellent - that's real validation. Now, why would they choose your tool over alternatives like GitHub Actions, CircleCI, or just writing scripts?

User: Those tools require significant configuration and maintenance. My tool is zero-config - it detects your project structure and just works.

Agent: "Zero-config deployment that just works" - that's a clear differentiator.

What are the 3-5 capabilities that make this possible? Remember, capabilities are outcomes, not features.

User: Automatic project detection, one-command deployments, built-in secrets management, instant rollbacks, and... wait, are those features?

Agent: Good catch - let's translate to capabilities:
- "Works with any project structure without configuration"
- "Deploy to production with a single command"
- "Secure secrets management without additional setup"
- "Instant recovery from failed deployments"

Does that capture what you meant?

User: Yes, exactly.

Agent: Now let's define success. How will you know if this works - for the business and for users?

User: Business: I want 1000 active users in year one. User: They should be able to deploy in under 5 minutes on their first try.

Agent: Both measurable - good. Finally, what are you NOT doing? What would be scope creep?

User: We're not building a full platform like Vercel. Not doing containers or Kubernetes. Not supporting on-premise.

Agent: Those are clear anti-goals. Let me synthesize this into your vision.org...

[Agent updates planning/vision.org with all content]

Agent: Your vision document is complete. Before we proceed to features, let's check: what's your biggest assumption that could be wrong?

User: That developers actually want zero-config. Some might want control.

Agent: Good awareness. How might you test that quickly?

User: I could offer a beta to those 5 CTOs and see if they actually use the zero-config mode or immediately ask for configuration options.

Agent: That's a solid validation plan. Your vision is ready for feature discovery.

---

## References

- Roman Pichler - Product Vision Board: https://www.romanpichler.com/tools/product-vision-board/
- Marty Cagan - Inspired: How to Create Tech Products Customers Love
- Amazon Working Backwards: PR/FAQ methodology
- Ash Maurya - Running Lean: Lean Canvas
- HBR research on vision statement effectiveness
- MIT Sloan Management Review: Making Your Vision Statement Work

---

## Metadata

- **Domain:** strategic-planning
- **Energy:** medium-high
- **Time Estimate:** 60-90 minutes for complete workshop
- **Prerequisites:** Rough idea of what you're building; access to planning/vision.org template; willingness to be specific
- **Outputs:** planning/vision.org with STATUS: draft
- **Next Steps:** Validate biggest assumption; use feature-discovery skill to derive features from vision
