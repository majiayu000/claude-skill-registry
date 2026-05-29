# Feature Discovery Skill

> Version: 1.0.0
> Compiler: manual
> Last Updated: 2026-01-26

Guide discovery of features from vision using hybrid Opportunity Solution Tree and Story Mapping methodology, producing planning/features.org entries.

## When to Activate

Use this skill when:
- Discovering features from an established vision
- Defining what to build and why
- Working with planning/features.org
- Translating vision success criteria to implementation
- Answering "what should we build?"

## Methodology

**Chosen:** Hybrid (Opportunity Solution Tree + Story Mapping + Job Stories)

**Rationale:** Research compared Opportunity Solution Trees (OST), Story Mapping, Jobs-to-be-Done (JTBD), and Impact Mapping. For solo developers or small teams with an established vision:

1. Story Mapping is excellent for release planning but doesn't validate opportunities
2. OST is rigorous but requires ongoing customer interviews (heavy for solo devs)
3. JTBD (Job Stories) improves story quality without process overhead
4. Impact Mapping is too strategic, doesn't help with feature-level detail

The hybrid approach takes:
- OST's outcome-first hierarchy (Vision -> Outcomes -> Opportunities -> Solutions)
- Story Mapping's visual release planning (backbone, walking skeleton, slices)
- Job Story format for articulating opportunities (When..., I want..., So I can...)

### Alternatives Considered

| Methodology | Reason Not Selected | When Appropriate |
|-------------|---------------------|------------------|
| Pure Opportunity Solution Trees | Requires regular customer interviews; too heavy for solo developers | Product teams with dedicated discovery time and customer access |
| Pure Story Mapping | Assumes you know what to build; doesn't challenge opportunity validity | When problem space is well understood, focus is on release planning |
| Impact Mapping | Strategic/portfolio level; doesn't help with feature granularity | Stakeholder alignment, roadmap communication |

## Core Principles

### 1. Outcomes Before Outputs

Start with what user behavior must change, not what features to build.

*Features are bets on outcomes. If you don't know the outcome, you can't know if the feature worked.*

**Test:** Can you articulate what success looks like without mentioning the feature?

### 2. Opportunity Is Not a Solution

An opportunity is a customer problem; a solution is how you address it.

*Jumping to solutions limits creativity. Good opportunities have multiple possible solutions.*

**Test:** Are there at least 2 ways to address this opportunity?

### 3. Evidence Over Intuition

Every opportunity should have supporting evidence (interview, data, observation).

*Solutions looking for problems is a failure mode. Evidence prevents building things nobody wants.*

**Test:** Can you cite a source for this opportunity?

### 4. Job Story Format

Use "When [situation], I want [motivation], so I can [outcome]" for opportunities.

*This format captures context (when), separates motivation from solution (want), and articulates value (so I can).*

**Test:** Does the statement describe a situation rather than a persona?

### 5. Scope Boundaries Upfront

Define what a feature will NOT do before building.

*Scope creep starts when boundaries are undefined. Anti-scope is a forcing function for focus.*

**Test:** Are there at least 2 explicit exclusions?

### 6. Small Batches

Slice features horizontally into releasable increments.

*Large batches delay feedback, increase risk, and hide problems. Ship smaller, learn faster.*

**Test:** Can the first slice be delivered in days, not weeks?

---

## Workflow

**Output:** planning/features.org with feature entries

### Phase 1: Outcome Definition

**Question:** What user behavior would change if the vision succeeds?

Extract measurable outcomes from vision success criteria. Review planning/vision.org and translate success criteria into observable behaviors.

**Outcomes should be:**
- Behavior-focused (what users DO differently)
- Measurable (can track progress)
- Time-bound (when do we expect change)

**Good Examples:**
- "Users complete onboarding in under 5 minutes"
- "Developers deploy without external help"
- "Teams reduce time-to-first-value by 50%"

**Avoid:**
- "Users like the product" (not behavior)
- "Feature X is shipped" (output, not outcome)

**Validation:**
- [ ] Is this a behavior change, not a feature?
- [ ] Is it measurable or at least observable?
- [ ] Does it connect to vision success criteria?

### Phase 2: Opportunity Discovery

**Question:** What customer problems, if solved, would drive those outcomes?

For each outcome, identify unmet needs, pain points, or desires. Write opportunities as Job Stories.

**Job Story Format:**
```
When [situation],
I want to [motivation],
so I can [outcome].
```

**Good Job Story Examples:**
- "When I'm configuring a new project, I want sensible defaults, so I can start coding immediately."
- "When deployment fails, I want clear error messages, so I can fix the problem without googling."
- "When I return to a project after time away, I want to see where I left off, so I can resume quickly."

**Anti-patterns:**
- "Users want a dashboard" (solution, not opportunity)
- "As a developer, I..." (persona, not situation)
- "The system should..." (requirement, not job)

**Evidence Types:**
- interview: Quote from user research
- analytics: Data showing the problem
- support-ticket: User complaint
- observation: Witnessed behavior

**Validation:**
- [ ] Is this a job story (When..., I want..., So I can...)?
- [ ] Is there at least one piece of evidence?
- [ ] Does solving this plausibly drive the target outcome?

### Phase 3: Opportunity Prioritization

**Question:** Which opportunities are most important to address first?

Evaluate by impact and evidence strength:

| Impact | Evidence | Action |
|--------|----------|--------|
| High | Strong | Do first |
| High | Weak | Validate before committing |
| Low | Strong | Maybe later |
| Low | Weak | Skip |

**For solo developers without extensive research:**
- Prioritize based on your own pain points (you're often the target user)
- Start with the opportunity that, if solved, unlocks others
- Prefer opportunities where you can easily validate the solution

**Validation:**
- [ ] Is there a clear rationale for the priority order?
- [ ] Are the top 2-3 opportunities identified for this cycle?

### Phase 4: Solution Brainstorming

**Question:** What features could address the top opportunities?

For each target opportunity, brainstorm 2-3 solutions:

1. **The obvious solution** (what comes to mind first)
2. **The minimal solution** (simplest thing that could work)
3. **The creative solution** (what if we approached this differently?)

**Compare solutions by:**
- Effort to build
- Risk of failure
- Learning potential
- Reusability

**For each solution, identify the riskiest assumption:**
- What must be true for this to work?
- How could we test this before building?

**Validation:**
- [ ] Are there at least 2 solution options per opportunity?
- [ ] Is the riskiest assumption identified for each?
- [ ] Have you considered the minimal viable version?

### Phase 5: Solution Selection

**Question:** Which solution should we build first?

Assess each solution on:

**Effort:**
- How long to build MVP? (days/weeks/months)
- What dependencies exist?
- What skills are required?

**Impact:**
- How fully does this address the opportunity?
- What's the learning potential?
- Does this create a foundation for future work?

**Risk:**
- How testable is the core assumption?
- What happens if it doesn't work?
- Can we recover/pivot easily?

**Selection criteria:**
- Prefer solutions that address the opportunity meaningfully with minimal effort
- Prefer solutions where assumptions can be tested quickly
- Prefer solutions that create learning (even if they fail)

The winner becomes a Feature entry in planning/features.org.

**Validation:**
- [ ] Is there a clear rationale for the selected solution?
- [ ] Is the effort estimate realistic?
- [ ] Is there a plan to test the riskiest assumption?

### Phase 6: Feature Definition

**Question:** What exactly does this feature include and exclude?

Create a feature entry with:

1. **Opportunity** (job story + evidence)
2. **Success Criteria** (measurable outcome)
3. **Scope:**
   - In Scope: What this feature WILL do (3-5 capabilities)
   - Out of Scope: What this feature will NOT do (2-3 exclusions)
4. **Journeys:** Leave empty (populated in journey-mapping)
5. **Assumptions:** The riskiest beliefs that must be true

**Success criteria should be:**
- Measurable (number, percentage, time)
- Observable (we can see/track it)
- Time-bound (by when do we expect this)

Good: "80% of users complete first deployment within 10 minutes"
Bad: "Users find deployment easy"

**Validation:**
- [ ] Does the feature have a job story and evidence?
- [ ] Is success criteria measurable?
- [ ] Are there at least 2 scope exclusions?
- [ ] Are assumptions identified with tests?

### Phase 7: Assumption Identification

**Question:** What's the riskiest assumption for each feature?

Identify assumptions about:

1. **Desirability:** Do users actually want this?
2. **Viability:** Does this make business sense?
3. **Feasibility:** Can we build this?
4. **Usability:** Can users figure it out?

For each assumption, rate risk (high/medium/low) and note a test:
- **High:** Could invalidate the whole feature
- **Medium:** Would require significant rework
- **Low:** Might need minor adjustments

**Tests should be cheap, fast, and informative:**
- Prototype test: Show mockup to 5 users
- Wizard of Oz: Manually deliver the experience
- Data analysis: Look at existing behavior
- Competitor analysis: How do others solve this?

**Validation:**
- [ ] Is there at least one assumption per feature?
- [ ] Are risks rated appropriately?
- [ ] Are tests actionable and low-cost?

### Phase 8: Synthesis

**Question:** Is the feature registry complete and ready for journey mapping?

Update planning/features.org with all feature entries. Cross-check with vision:
- Does each feature trace back to vision success criteria?
- Do features together address the vision's value proposition?
- Are there vision elements without features? (gaps)
- Are there features without vision connection? (scope creep)

**Validation:**
- [ ] Are all features documented in planning/features.org?
- [ ] No [REPLACE] placeholders remaining?
- [ ] Each feature has STATUS, VISION reference, and dates?
- [ ] Feature list reviewed for coherence with vision?

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| Job Story Elicitation | User describes a feature instead of a problem | Ask "What situation are you in when you need this? What happens if you can't do it?" | Features are solutions; we need the underlying job to explore alternatives |
| Evidence Mining | Opportunity seems intuitive but lacks evidence | Ask "How do you know users have this problem? What would convince a skeptic?" | Intuition is often right but needs validation to prioritize |
| Outcome Laddering | User states an output goal ("ship feature X") | Ask "Why does feature X matter? What changes when it exists?" | Surfaces the underlying outcome that the output is meant to achieve |
| Scope Boundary Prompt | Feature scope is ambiguous | Ask "What have you been tempted to add but decided against? What would be scope creep?" | Anti-scope prevents the feature from growing indefinitely |
| Minimal Viable Feature | Feature seems large | Ask "What's the smallest version that would let us learn if this works?" | Smaller batches = faster feedback = lower risk |
| Assumption Surfacing | Feature is defined but assumptions aren't explicit | Ask "What must be true for this to succeed? What would make you abandon this approach?" | Explicit assumptions can be tested; implicit ones become surprises |

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Feature Factory | Shipping features without measuring outcomes creates false sense of progress | Assign outcomes, not features. Measure whether features moved the needle |
| Skipping the Opportunity Space | Jumping from vision to features builds solutions for nonexistent problems | Use opportunity discovery. Require evidence for each opportunity |
| Solutions Looking for Problems | Starting with solutions wastes effort on things that don't deliver value | Always ask "what problem does this solve?" before accepting a feature |
| Scope Creep | Expanding scope during development delays delivery and loses focus | Define anti-goals upfront. Link every addition to the target opportunity |
| Feature Bloat | Accumulating features creates product that serves everyone poorly | Measure feature adoption. Sunset unused features. Calculate true cost of complexity |
| HiPPO-Driven Development | Features based on opinions rather than evidence are shaped by politics | Require evidence for all features. Make opportunity validation transparent |
| All-or-Nothing Thinking | Large releases delay feedback and increase risk | Slice horizontally. Ship walking skeleton first. Embrace incremental delivery |

---

## Quality Checklist

Before proceeding to journey mapping, verify:

- [ ] Each feature has a job story (When..., I want..., So I can...)
- [ ] Each feature has at least one piece of evidence
- [ ] Success criteria is measurable and time-bound
- [ ] In-scope capabilities are listed (3-5 items)
- [ ] Out-of-scope exclusions are explicit (2+ items)
- [ ] Riskiest assumption is identified with a test
- [ ] Feature traces back to vision success criteria
- [ ] STATUS is set and dates are populated
- [ ] No [REPLACE] placeholders remaining
- [ ] Feature set reviewed for coherence with vision

---

## Examples

### Complete Feature Discovery Session

**Agent:** Let's discover features from your vision. First, let me review your planning/vision.org to understand the outcomes we're aiming for.

*[Agent reads vision.org]*

**Agent:** I see your success criteria include:
- "Developers complete first deployment in under 5 minutes"
- "50% reduction in time spent on configuration"

Let's translate these into behavior-focused outcomes. The first one is already behavior-focused. For the second, what behavior would change if configuration time dropped?

**User:** Developers would spend more time on actual coding instead of setup.

**Agent:** Good. So our outcomes are:
1. Time-to-first-deployment under 5 minutes
2. Developers spend proportionally more time coding vs configuring

Now let's discover opportunities. What prevents users from deploying quickly today?

**User:** They have to configure a lot of stuff manually - CI/CD, secrets, environment variables. It's confusing and error-prone.

**Agent:** Let's write that as a job story. "When I'm setting up a new project, I want to skip the configuration boilerplate, so I can start deploying immediately."

Do you have evidence this is a real problem?

**User:** I've experienced it myself, and I saw three GitHub issues asking for simpler setup.

**Agent:** Good. Let's capture:
- interview (self): Personal experience with configuration complexity
- support-ticket: GitHub issues #X, #Y, #Z requesting simpler setup

What other opportunities might drive these outcomes?

**User:** Error messages during deployment are cryptic. People spend hours debugging things that should be obvious.

**Agent:** Job story: "When deployment fails, I want clear error messages that tell me what's wrong and how to fix it, so I can resolve issues quickly without searching Stack Overflow."

Any evidence?

**User:** The GitHub issues mention confusion about error messages.

**Agent:** Great. Now let's prioritize. We have:
1. Configuration complexity (strong evidence, high impact)
2. Cryptic error messages (some evidence, medium impact)

Which should we address first?

**User:** Configuration complexity - it's the first thing users encounter.

**Agent:** Let's brainstorm solutions for configuration complexity:

1. Obvious: Wizard-based setup with step-by-step prompts
2. Minimal: Zero-config with sensible defaults and auto-detection
3. Creative: Generate configuration from code inspection

Which appeals to you? What are the trade-offs?

**User:** Zero-config feels right for our vision of "just works." The wizard still requires effort.

**Agent:** What's the riskiest assumption with zero-config?

**User:** That our defaults work for most projects. Some projects might need custom configuration.

**Agent:** Good insight. Let's note that assumption with a test: "Validate that sensible defaults work for 80%+ of project types by analyzing common configurations in public repos."

Now let's define the feature. What's in scope?

**User:** Auto-detect project type, auto-configure CI/CD, auto-setup secrets management, provide override mechanism for edge cases.

**Agent:** What's explicitly out of scope?

**User:** We won't support on-premise deployment infrastructure. We won't build a configuration GUI.

**Agent:** Success criteria?

**User:** 80% of new projects deploy successfully on first try without any configuration.

**Agent:** Excellent. Let me write this to planning/features.org...

*[Agent creates feature entry with all fields]*

**Agent:** Your feature "Zero-Config Deployment" is documented. It's ready for journey mapping, where we'll design the user experience in detail.

---

## References

- Teresa Torres - Continuous Discovery Habits: Discover Products That Create Customer Value and Business Value
- Teresa Torres - Opportunity Solution Trees: https://www.producttalk.org/opportunity-solution-tree/
- Jeff Patton - User Story Mapping: Discover the Whole Story, Build the Right Product
- Alan Klement - When Coffee and Kale Compete: Jobs-to-be-Done framework
- John Cutler - 12 Signs You're Working in a Feature Factory: https://cutle.fish/blog/12-signs-youre-working-in-a-feature-factory
- Marty Cagan - Inspired: How to Create Tech Products Customers Love

---

## Metadata

- **Domain:** product-discovery
- **Energy:** medium-high
- **Time Estimate:** 60-90 minutes for complete session
- **Prerequisites:** Completed vision-workshop (planning/vision.org exists); access to planning/features.org template
- **Outputs:** planning/features.org with feature entries
- **Next Steps:** Validate riskiest assumptions before heavy investment; use journey-mapping skill for each feature
