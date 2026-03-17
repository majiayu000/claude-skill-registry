---
name: compare-architectures
description: Generate and compare multiple architecture options (minimal, moderate, full modernization) with comprehensive trade-offs analysis across cost, timeline, risk, performance, and maintainability dimensions. Use when evaluating multiple architectural approaches or deciding between modernization strategies with different cost/risk trade-offs.
acceptance:
  - three_options_generated: "Three distinct architecture options created (minimal, moderate, full)"
  - trade_offs_analyzed: "Each option includes cost, timeline, risk, performance, maintainability analysis"
  - recommendation_provided: "Clear recommendation based on user constraints with justification"
  - comparison_matrix: "Side-by-side comparison matrix for easy evaluation"
  - next_steps_defined: "Implementation roadmap outlined for recommended option"
inputs:
  current_architecture:
    type: string
    required: false
    description: "Path to current architecture document or textual description of existing system"
  new_requirements:
    type: string
    required: true
    description: "User's goals, ideas, and new requirements to be incorporated"
  constraints:
    type: object
    required: false
    description: "Timeline, budget, team size, expertise constraints"
    default: {}
  comparison_dimensions:
    type: array
    required: false
    description: "Dimensions to compare (cost, timeline, risk, performance, maintainability, scalability, security)"
    default: ["cost", "timeline", "risk", "maintainability"]
  project_type:
    type: string
    required: false
    description: "frontend | backend | fullstack (auto-detected if not provided)"
outputs:
  comparison_created:
    type: boolean
    description: "Whether comparison document was successfully created"
  comparison_location:
    type: string
    description: "File path to comparison document (docs/architecture-comparison-{timestamp}.md)"
  options_count:
    type: number
    description: "Number of architecture options generated (always 3)"
  recommended_option:
    type: string
    description: "Which option is recommended (minimal | moderate | full)"
  recommendation_confidence:
    type: number
    description: "Confidence in recommendation (0-100)"
telemetry:
  emit: "skill.compare-architectures.completed"
  track:
    - project_type
    - options_count
    - recommended_option
    - recommendation_confidence
    - comparison_dimensions
    - duration_ms
    - comparison_location
---

# Compare Architectures Skill

## Purpose

Generate three distinct architecture options with comprehensive trade-offs analysis to help users make informed decisions about system modernization or design. Each option represents a different investment level (minimal, moderate, full) with detailed cost, timeline, risk, and quality analysis.

**Core Principles:**
- Present 3 viable options (not 1 perfect solution)
- Honest trade-offs analysis (no "best" option without context)
- Evidence-based estimates (cost, timeline, risk)
- Clear recommendation with justification
- Actionable next steps for chosen option

## Prerequisites

- Understanding of current system (if brownfield)
- Clear new requirements or goals
- User constraints known (timeline, budget, team)
- workspace/ directory exists for output storage

---

## Workflow

### Step 1: Analyze Current State & Requirements

**Action:** Understand current architecture and new requirements to create meaningful options.

**Key Activities:**

1. **Load Current Architecture (if brownfield)**
   ```bash
   # If current_architecture path provided
   python .claude/skills/bmad-commands/scripts/read_file.py \
     --path {current_architecture} \
     --output json

   # Extract:
   # - Current technology stack
   # - Architecture patterns
   # - Known limitations/pain points
   # - Production readiness score (if from analyze-architecture)
   ```

   If current architecture is textual description, parse for:
   - Technology stack (languages, frameworks, databases)
   - Architecture type (monolith, microservices, etc.)
   - Scale indicators (users, data volume, traffic)
   - Pain points mentioned

2. **Parse New Requirements**

   Extract from `new_requirements`:
   - **Functional changes:** New features, capabilities, integrations
   - **Non-functional changes:** Performance, scalability, security needs
   - **Business goals:** Why these changes matter, expected outcomes
   - **Success criteria:** How to measure success

   Example parsing:
   ```
   Input: "Add real-time chat, support 10K concurrent users, mobile app needed"

   Parsed:
   - Functional: Real-time chat feature, mobile support
   - Non-functional: Scale to 10K concurrent (performance requirement)
   - Technical implications: Need WebSocket/SSE, mobile framework
   ```

3. **Identify Constraints**

   From `constraints` parameter:
   - **Timeline:** How soon is this needed? (weeks, months, year)
   - **Budget:** Cost sensitivity (low, moderate, high)
   - **Team size:** How many developers available?
   - **Team expertise:** Current skill set, willingness to learn new tech
   - **Risk tolerance:** Conservative (low risk) vs. aggressive (innovation)

   **Default assumptions if not provided:**
   - Timeline: Moderate (3-6 months)
   - Budget: Moderate
   - Team: Small (2-5 developers)
   - Expertise: Moderate (willing to learn)
   - Risk tolerance: Moderate

4. **Detect Project Type (if not provided)**

   Based on current architecture and requirements:
   - **Frontend:** UI/UX dominant, client-side changes
   - **Backend:** API/services/data dominant
   - **Fullstack:** Both frontend and backend changes

**Output:** Comprehensive context for option generation

**See:** `references/requirement-analysis.md` for detailed parsing techniques

---

### Step 2: Generate Three Architecture Options

**Action:** Create three distinct options representing different investment/change levels.

**Option Generation Strategy:**

#### Option A: Minimal Changes (Lowest Risk, Fastest)

**Philosophy:** Keep what works, fix what's broken, add minimally.

**Approach:**
- **Technology:** Stick with current stack, upgrade versions
- **Architecture:** Minimal pattern changes, targeted fixes
- **Scope:** Address critical pain points only, defer nice-to-haves
- **Integration:** Bolt-on new features to existing architecture
- **Migration:** No migration, incremental additions

**Typical Characteristics:**
- Timeline: 2-6 weeks
- Cost: $ (1x baseline)
- Risk: Low (minimal changes, proven tech)
- Team impact: Minimal learning curve
- Technical debt: May increase slightly (tactical over strategic)

**Example (Real-time Chat Requirement):**
```markdown
## Option A: Minimal Changes - Bolt-on Chat

**Approach:** Add Socket.IO to existing Express backend, embed chat widget in current UI.

**Technology Stack:**
- Keep: Current React frontend, Express backend, PostgreSQL
- Add: Socket.IO (WebSocket), Redis (pub/sub)

**Architecture:**
- Chat service as separate Express route
- Shared PostgreSQL for messages
- Redis for pub/sub between server instances

**Changes Required:**
- Add Socket.IO endpoints to Express (~500 LOC)
- Add chat UI component to React (~300 LOC)
- Add Redis for horizontal scaling (~100 LOC)

**Pros:**
✅ Fast implementation (3-4 weeks)
✅ Low risk (minimal changes)
✅ No migration needed
✅ Team knows the stack

**Cons:**
❌ Not optimal architecture for real-time
❌ May have scaling challenges >5K users
❌ Technical debt increases
❌ Shared database could become bottleneck

**Cost:** $15K-$25K (developer time)
**Timeline:** 3-4 weeks
**Risk:** Low
```

---

#### Option B: Moderate Refactor (Balanced Approach)

**Philosophy:** Strategic improvements, selective modernization, set up for future.

**Approach:**
- **Technology:** Mix of current + modern (gradual migration)
- **Architecture:** Improve patterns, introduce new where needed
- **Scope:** Address current needs + position for future growth
- **Integration:** Refactor key areas, new services for new features
- **Migration:** Incremental (strangler fig pattern)

**Typical Characteristics:**
- Timeline: 2-4 months
- Cost: $$ (2-3x baseline)
- Risk: Medium (some new tech, planned migration)
- Team impact: Moderate learning (new patterns/tools)
- Technical debt: Reduced overall (strategic improvements)

**Example (Real-time Chat Requirement):**
```markdown
## Option B: Moderate Refactor - Dedicated Chat Service

**Approach:** Extract chat as microservice with modern real-time stack, keep core app.

**Technology Stack:**
- Keep: React frontend, Express API, PostgreSQL (core)
- New: Node.js + Socket.IO (chat service), MongoDB (chat messages), Redis (caching)

**Architecture:**
- Chat microservice (separate deployment)
- Event-driven communication (message bus)
- Dedicated database for chat (MongoDB)
- API gateway pattern for routing

**Changes Required:**
- Build chat microservice (~2K LOC)
- Integrate with existing auth (JWT sharing)
- Update frontend to connect to chat service
- Set up API gateway (Kong/Express Gateway)

**Pros:**
✅ Scales well (dedicated service)
✅ Better real-time performance
✅ Reduces technical debt
✅ Positions for future microservices
✅ Team learns modern patterns

**Cons:**
❌ More complex deployment
❌ Need to learn microservices patterns
❌ Operational overhead (monitoring, debugging)
⚠️  Migration period (running both)

**Cost:** $40K-$60K (developer time + infrastructure)
**Timeline:** 2-3 months
**Risk:** Medium
```

---

#### Option C: Full Modernization (Highest Quality, Longest Timeline)

**Philosophy:** Do it right, invest for long-term, modern best practices.

**Approach:**
- **Technology:** Modern stack, latest frameworks and tools
- **Architecture:** Best practices, scalable patterns from day 1
- **Scope:** Solve current needs + future-proof for 3-5 years
- **Integration:** Complete redesign, greenfield opportunity
- **Migration:** Phased complete migration or parallel run

**Typical Characteristics:**
- Timeline: 4-8 months
- Cost: $$$ (4-6x baseline)
- Risk: High (major changes, new tech, migration complexity)
- Team impact: Significant learning (new ecosystem)
- Technical debt: Near zero (clean slate)

**Example (Real-time Chat Requirement):**
```markdown
## Option C: Full Modernization - Real-time First Architecture

**Approach:** Rebuild as real-time-first app with modern fullstack framework.

**Technology Stack:**
- Frontend: Next.js 15 (React 19, server components)
- Backend: tRPC + WebSocket, serverless functions
- Database: PostgreSQL (main) + Redis (cache/pub-sub)
- Real-time: Ably or Pusher (managed real-time infrastructure)
- Mobile: React Native (shared components with web)

**Architecture:**
- Fullstack monorepo (Turborepo)
- Real-time-first design (WebSocket primary, HTTP fallback)
- Serverless functions (auto-scaling)
- CDN edge functions for global performance
- Mobile + web from single codebase

**Changes Required:**
- Complete rebuild of frontend in Next.js (~8K LOC)
- Backend as tRPC API + WebSocket (~4K LOC)
- Real-time infrastructure setup (Ably/Pusher)
- Mobile app (React Native, ~3K LOC)
- Data migration from old to new system

**Pros:**
✅ Modern, maintainable codebase
✅ Excellent real-time performance
✅ Scales to 100K+ users easily
✅ Mobile + web unified
✅ Easy to hire developers (popular stack)
✅ Near-zero technical debt

**Cons:**
❌ Long timeline (4-6 months)
❌ High cost (significant investment)
❌ Team needs to learn new stack
❌ Complex migration from old system
❌ Risk of over-engineering

**Cost:** $120K-$180K (developer time + services)
**Timeline:** 4-6 months
**Risk:** High
```

---

### Step 3: Perform Trade-offs Analysis

**Action:** Compare options across key dimensions to enable informed decision.

**Key Dimensions:**

#### 1. Cost Analysis

**Components:**
- **Development time:** Developer hours × hourly rate
- **Infrastructure:** Hosting, services, licenses
- **Migration:** Data migration, parallel running, cutover
- **Training:** Team learning curve, external training
- **Opportunity cost:** What else could team work on?

**Comparison Matrix:**

| Dimension | Option A: Minimal | Option B: Moderate | Option C: Full |
|-----------|-------------------|-------------------|----------------|
| **Development** | 2-3 dev-weeks | 8-12 dev-weeks | 20-26 dev-weeks |
| **Infrastructure** | +$50/mo | +$200/mo | +$500/mo |
| **Migration** | None | $5K-$10K | $15K-$25K |
| **Training** | None | Moderate | Significant |
| **Total Cost** | $15K-$25K | $40K-$60K | $120K-$180K |

---

#### 2. Timeline Analysis

**Factors:**
- **Planning:** Requirements, design, architecture
- **Development:** Implementation time
- **Testing:** QA, performance, security
- **Migration:** Data migration, cutover, validation
- **Stabilization:** Bug fixes, monitoring, optimization

**Comparison Matrix:**

| Phase | Option A: Minimal | Option B: Moderate | Option C: Full |
|-------|-------------------|-------------------|----------------|
| **Planning** | 1 week | 2 weeks | 3 weeks |
| **Development** | 2-3 weeks | 8-10 weeks | 16-20 weeks |
| **Testing** | 1 week | 2 weeks | 4 weeks |
| **Migration** | None | 1 week | 2-3 weeks |
| **Stabilization** | 1 week | 2 weeks | 3 weeks |
| **Total Timeline** | 3-4 weeks | 2-3 months | 4-6 months |

---

#### 3. Risk Analysis

**Risk Categories:**
- **Technical risk:** New tech, complex patterns, unknowns
- **Migration risk:** Data loss, downtime, bugs
- **Team risk:** Skill gaps, learning curve, velocity drop
- **Business risk:** Opportunity cost, market timing, competition

**Scoring (0-100, higher = riskier):**

| Risk Type | Option A: Minimal | Option B: Moderate | Option C: Full |
|-----------|-------------------|-------------------|----------------|
| **Technical** | 20 (known tech) | 50 (some new) | 75 (major changes) |
| **Migration** | 10 (no migration) | 40 (incremental) | 70 (big bang) |
| **Team** | 15 (no learning) | 45 (moderate learn) | 65 (steep curve) |
| **Business** | 25 (low impact) | 35 (moderate) | 55 (high impact) |
| **Overall Risk** | **Low (18)** | **Medium (43)** | **High (66)** |

---

#### 4. Performance & Scalability

**Metrics:**
- **Latency:** Response time (p50, p95, p99)
- **Throughput:** Requests per second
- **Concurrency:** Concurrent users supported
- **Scalability:** Horizontal/vertical scaling capability

**Comparison:**

| Metric | Option A: Minimal | Option B: Moderate | Option C: Full |
|--------|-------------------|-------------------|----------------|
| **Latency** | Good (<200ms) | Very Good (<100ms) | Excellent (<50ms) |
| **Concurrency** | ~5K users | ~25K users | ~100K+ users |
| **Scalability** | Limited (vertical) | Good (horizontal) | Excellent (elastic) |
| **Score** | 60/100 | 80/100 | 95/100 |

---

#### 5. Maintainability & Technical Debt

**Factors:**
- **Code quality:** Readability, structure, patterns
- **Technical debt:** Shortcuts, compromises, legacy code
- **Team velocity:** How fast can team add features later?
- **Hiring:** How easy to find developers?

**Comparison:**

| Factor | Option A: Minimal | Option B: Moderate | Option C: Full |
|--------|-------------------|-------------------|----------------|
| **Code Quality** | Fair (adds debt) | Good (improves) | Excellent (clean) |
| **Tech Debt** | +10% increase | -20% reduction | -90% reduction |
| **Future Velocity** | Slows over time | Maintains | Accelerates |
| **Hiring** | Moderate | Good | Excellent |
| **Score** | 50/100 | 75/100 | 95/100 |

---

### Step 4: Generate Recommendation

**Action:** Recommend the best option based on user constraints and provide justification.

**Recommendation Logic:**

```python
def recommend_option(constraints, user_priorities):
    # Score each option based on constraints
    scores = {
        "minimal": 0,
        "moderate": 0,
        "full": 0
    }

    # Timeline constraint
    if constraints.timeline == "urgent" (<2 months):
        scores["minimal"] += 40
        scores["moderate"] += 20
        scores["full"] += 0
    elif constraints.timeline == "moderate" (2-6 months):
        scores["minimal"] += 20
        scores["moderate"] += 40
        scores["full"] += 20
    else:  # Long-term (>6 months)
        scores["minimal"] += 10
        scores["moderate"] += 30
        scores["full"] += 40

    # Budget constraint
    if constraints.budget == "tight":
        scores["minimal"] += 40
        scores["moderate"] += 15
        scores["full"] += 0
    elif constraints.budget == "moderate":
        scores["minimal"] += 20
        scores["moderate"] += 40
        scores["full"] += 15
    else:  # generous
        scores["minimal"] += 10
        scores["moderate"] += 25
        scores["full"] += 40

    # Risk tolerance
    if constraints.risk_tolerance == "conservative":
        scores["minimal"] += 30
        scores["moderate"] += 20
        scores["full"] += 5
    elif constraints.risk_tolerance == "moderate":
        scores["minimal"] += 15
        scores["moderate"] += 35
        scores["full"] += 20
    else:  # aggressive
        scores["minimal"] += 5
        scores["moderate"] += 20
        scores["full"] += 40

    # User priorities
    if user_priorities.includes("long_term_quality"):
        scores["full"] += 20
        scores["moderate"] += 10
    if user_priorities.includes("speed_to_market"):
        scores["minimal"] += 20
        scores["moderate"] += 10
    if user_priorities.includes("scale_for_growth"):
        scores["full"] += 15
        scores["moderate"] += 10

    # Return highest scoring option
    return max(scores, key=scores.get)
```

**Recommendation Format:**

```markdown
## My Recommendation: Option B - Moderate Refactor

**Confidence:** 85% (High)

**Why This Option:**

Given the constraints:
- Timeline: 3-4 months (moderate)
- Budget: $40K-$60K (moderate)
- Risk tolerance: Medium (willing to invest strategically)
- Priorities: Scale for growth + reduce technical debt

**Option B (Moderate Refactor) is the best fit because:**

1. **Balanced Investment:**
   - Not too fast/cheap (Option A would hit limits soon)
   - Not too slow/expensive (Option C might be over-engineering)
   - $40K-$60K is reasonable for 2-3 month project

2. **Addresses Core Needs:**
   - Solves real-time chat requirement properly (dedicated service)
   - Scales to 25K users (covers the 10K + growth trajectory)
   - Sets up for future microservices (if needed)

3. **Manageable Risk:**
   - Team can learn gradually (not all at once like Option C)
   - Incremental migration (lower risk than big bang)
   - Proven patterns (microservices, event-driven)

4. **Future-Proof:**
   - Reduces technical debt (20% improvement)
   - Easier to hire (modern but not bleeding edge)
   - Positions for growth (can add more services later)

**When to Consider Alternatives:**

- **Choose Option A if:** Timeline is critical (<6 weeks), budget is very tight (<$30K)
- **Choose Option C if:** Planning for 100K+ users, have 6+ months, budget >$120K
```

**Confidence Scoring:**

- **High (80-100%):** Clear constraints, obvious best choice
- **Medium (60-79%):** Trade-offs close, depends on priorities
- **Low (<60%):** Need more information, similar options

---

### Step 5: Create Comparison Document

**Action:** Generate comprehensive comparison document with all options, trade-offs, and recommendation.

**Document Structure:**

```markdown
# Architecture Options Comparison: [Project Name]

**Date:** [YYYY-MM-DD]
**Prepared For:** [User/Stakeholder]
**Current State:** [Brief summary of existing architecture]
**New Requirements:** [What's being added/changed]

---

## Executive Summary

**Recommendation:** Option B - Moderate Refactor
**Confidence:** 85% (High)

**Why:** Balanced approach that meets the requirements, fits timeline/budget, and positions for future growth without over-engineering.

**Quick Comparison:**

| Factor | Option A | Option B ✅ | Option C |
|--------|----------|------------|----------|
| **Timeline** | 3-4 weeks | 2-3 months | 4-6 months |
| **Cost** | $15K-$25K | $40K-$60K | $120K-$180K |
| **Risk** | Low (18) | Medium (43) | High (66) |
| **Scale** | ~5K users | ~25K users | ~100K+ users |
| **Tech Debt** | +10% | -20% | -90% |

---

## Option A: Minimal Changes

[Detailed description from Step 2]

**Architecture Diagram:**
[ASCII or reference to diagram]

**Technology Stack:**
- [List with justifications]

**Implementation Plan:**
1. [High-level steps]
2. ...

**Pros & Cons:**
✅ [Pros]
❌ [Cons]

**Trade-offs Analysis:**
[Cost, timeline, risk, performance, maintainability details]

---

## Option B: Moderate Refactor ✅ RECOMMENDED

[Detailed description from Step 2]

[Same sections as Option A]

**Why This is Recommended:**
[Recommendation justification from Step 4]

---

## Option C: Full Modernization

[Detailed description from Step 2]

[Same sections as Option A]

---

## Side-by-Side Comparison

### Cost Comparison
[Detailed cost breakdown table]

### Timeline Comparison
[Gantt chart or timeline visualization]

### Risk Comparison
[Risk matrix or scoring table]

### Performance Comparison
[Performance metrics table]

### Maintainability Comparison
[Technical debt and code quality comparison]

---

## Recommendation Details

### Primary Recommendation: Option B

[Full justification from Step 4]

### Alternative Scenarios

**If timeline is critical (<6 weeks):**
→ Choose Option A, plan for Option B later

**If budget is generous (>$120K):**
→ Consider Option C for long-term investment

**If team is risk-averse:**
→ Start with Option A, evaluate results, then consider Option B

---

## Next Steps

### If You Choose Option A (Minimal):
1. [Implementation roadmap]
2. [Key decisions needed]
3. [Timeline with milestones]

### If You Choose Option B (Moderate) ✅:
1. **Week 1-2:** Architecture design finalization
2. **Week 3-4:** Chat microservice development
3. **Week 5-6:** API gateway setup + integration
4. **Week 7-8:** Frontend integration + testing
5. **Week 9-10:** Migration + stabilization

**Key Decisions Needed:**
- Message bus choice (RabbitMQ vs. Kafka vs. AWS SQS)
- API gateway (Kong vs. Express Gateway vs. AWS API Gateway)
- MongoDB hosting (self-managed vs. MongoDB Atlas)

**Success Criteria:**
- Chat supports 10K concurrent users
- p95 latency <100ms
- Zero downtime migration
- No data loss during migration

### If You Choose Option C (Full):
1. [Implementation roadmap]
2. [Key decisions needed]
3. [Timeline with milestones]

---

## Appendices

### Appendix A: Assumptions
- [List all assumptions made]

### Appendix B: Technology Comparison
- [Detailed tech stack comparison]

### Appendix C: Migration Strategy
- [For Option B and C, detailed migration approach]

### Appendix D: Risk Mitigation
- [For each identified risk, mitigation strategies]

---

**Prepared by:** Winston (Architecture Subagent)
**Review Status:** Ready for Stakeholder Review
**Next Action:** Decision on preferred option
```

**File Location:** `docs/architecture-comparison-[timestamp].md`

---

## Reference Files

- `references/requirement-analysis.md` - How to parse and analyze requirements
- `references/option-generation-patterns.md` - Strategies for creating options
- `references/cost-estimation.md` - How to estimate costs accurately
- `references/risk-assessment-framework.md` - Risk scoring methodology
- `references/trade-offs-analysis.md` - Comprehensive trade-offs evaluation

---

## When to Escalate

**Escalate to user when:**
- Requirements are vague or contradictory
- Constraints are unrealistic (timeline too short for scope)
- All options have critical risks
- User priorities conflict (e.g., "fastest AND highest quality")

**Escalate to architects when:**
- Complex architecture patterns needed
- Novel technology choices required
- Compliance/regulatory requirements unclear
- Performance requirements extremely stringent

---

## Success Criteria

A comparison is successful when:

✅ **Three viable options generated:**
- Each option is realistic and implementable
- Clear differentiation between options
- All options address core requirements

✅ **Comprehensive trade-offs:**
- All key dimensions analyzed (cost, timeline, risk, etc.)
- Honest assessment (no "perfect" option)
- Evidence-based estimates

✅ **Clear recommendation:**
- Based on user constraints and priorities
- Well-justified with reasoning
- Confidence level stated

✅ **Actionable next steps:**
- Implementation roadmap for each option
- Key decisions identified
- Success criteria defined

---

*Part of BMAD Enhanced Planning Suite*
