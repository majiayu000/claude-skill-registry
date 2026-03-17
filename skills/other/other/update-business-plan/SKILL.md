---
name: update-business-plan
description: Update Business Plan based on scan evidence, card reflections, and strategic decisions.
---

# Update Business Plan

Extract learnings from completed cards, scan evidence, and strategic decisions to update the corresponding Business Plan. Keeps business strategy aligned with execution reality.

## Operating Mode

**READ + WRITE (BUSINESS PLANS ONLY)**

**Allowed:**
- Read card reflection stage docs (`reflect.agent.md`)
- Read scan results from `docs/business-os/scans/`
- Update business plan files (`strategy/<BIZ>/plan.user.md` and `.agent.md`)
- Commit plan updates with agent identity

**Not allowed:**
- Modifying cards or ideas
- Creating new business plans (only updates existing plans)
- Changing business catalog (businesses.json)

## Inputs

**Required:**
- Business code (e.g., `BRIK`, `SKYL`, `PLAT`)

**Optional:**
- Source: `reflection` (from card) or `scan` (from repo scan) or `manual` (Pete-provided insights)
- Card ID: If updating from specific card reflection

## Business Plan Structure

Business plans are located at: `docs/business-os/strategy/<BIZ>/plan.user.md` and `plan.agent.md`

### Sections to Update

1. **Strategy** (What we're focusing on)
   - New opportunities validated through fact-finding
   - Strategic direction changes
   - Priority shifts

2. **Risks** (What could go wrong)
   - Emerging risks discovered during execution
   - Blocked cards and systemic issues
   - Technical debt accumulation

3. **Opportunities** (Ideas worth pursuing)
   - Validated ideas from completed Fact-finding
   - Market observations from scans
   - Customer feedback themes

4. **Learnings** (Append-only log)
   - What worked / what didn't from completed cards
   - Process improvements
   - Technical discoveries
   - Business insights

5. **Metrics** (How we're measuring success)
   - KPI updates based on shipped features
   - Performance impact of completed work
   - Business outcome measurements

## Workflow

### 1. Identify Update Source

**From Card Reflection:**
```typescript
const reader = createRepoReader(repoRoot);
const card = await reader.getCard(cardId);
const reflectDoc = await reader.getStageDoc(cardId, "reflect");

// Extract from reflect.agent.md:
// - Decisions made
// - Risks discovered
// - Learnings captured
// - Metrics/outcomes
```

**From Repo Scan:**
```typescript
const scanResults = JSON.parse(
  await fs.readFile("docs/business-os/scans/last-scan.json", "utf-8")
);

// Analyze:
// - Cards blocked (emerging risks)
// - Cards completed (learnings, metrics)
// - Ideas patterns (opportunities)
```

**From Manual Input:**
```typescript
// Pete provides:
// - Strategic decision
// - Market observation
// - Customer feedback theme
```

### 2. Extract Structured Information

Parse reflection or scan for:

**Decisions:**
- Strategic pivots
- Approach changes
- Priority adjustments

**Risks:**
- Blockers encountered
- Technical challenges
- Resource constraints
- Market changes

**Opportunities:**
- Validated ideas (positive fact-finding results)
- Customer requests
- Technical capabilities unlocked

**Learnings:**
- What worked well
- What didn't work
- Process improvements
- Technical insights

**Metrics:**
- Performance improvements
- Business outcomes (conversion, revenue, engagement)
- User feedback scores

### 3. Read Current Business Plan

```typescript
const planPath = `docs/business-os/strategy/${businessCode}/plan.user.md`;
const currentPlan = matter(await fs.readFile(planPath, "utf-8"));
```

Understand current strategy to integrate updates coherently.

### 4. Draft Plan Updates

**Strategy Section:**
```markdown
## Strategy

### Current Focus (Updated 2026-01-28)

1. **User Authentication** (Priority: High)
   - Status: Fact-finding complete, positive validation
   - Outcome: 82% of users want accounts feature
   - Next: Move to planning phase
   - Impact: Projected 15-20% reduction in booking abandonment

2. **Guide Offline Mode** (Priority: Medium)
   - Status: New opportunity from user research
   - Validation: 45% of users request offline access
   - Next: Create card, begin fact-finding

3. **Performance Optimization** (Priority: High)
   - Status: Completed (BRIK-ENG-0005)
   - Outcome: Page load improved 200ms (from 1.2s to 1.0s)
   - Impact: Bounce rate reduced by 8%
```

**Risks Section:**
```markdown
## Risks

### Active Risks

- **GDPR Compliance** (Severity: High, Added: 2026-01-28)
  - Source: Card BRIK-ENG-0001 blocked on legal review
  - Impact: Delays user auth feature by 1-2 weeks
  - Mitigation: Legal review in progress, backup plan if negative

- **Platform Auth Compatibility** (Severity: Medium, Added: 2026-01-28)
  - Source: Technical fact-finding on BRIK-ENG-0001
  - Impact: May require custom auth implementation
  - Mitigation: Architecture spike planned
```

**Opportunities Section:**
```markdown
## Opportunities

### Validated (Ready for Cards)

- **Guide Offline Mode**
  - Evidence: User research (45% request), customer-input
  - Value: Reduce support load, enable international travelers
  - Effort: Medium (service worker + cache strategy)
  - Recommend: Create card, prioritize for Q2

### Under Investigation

- **Mobile App Push Notifications**
  - Source: Scan detected user feedback themes
  - Status: Need fact-finding to validate demand
  - Next: Survey users, check technical feasibility
```

**Learnings Section:**
```markdown
## Learnings

### 2026-01-28: User Authentication Feature

- **What worked:**
  - Early user research prevented building unwanted features
  - Platform auth reuse saved 2 weeks of development
  - Fact-finding phase caught GDPR issue before build

- **What didn't work:**
  - Initial scope too broad (social login + email)
  - Legal review not started early enough
  - Performance testing delayed fact-finding exit

- **Process improvements:**
  - Start legal review during fact-finding, not planning
  - Scope to MVP first, add features incrementally
  - Performance baselines at start of fact-finding

- **Technical insights:**
  - Platform auth works with Brikette (confirmed via spike)
  - Social login adds 40% complexity vs email-only
  - Auth overhead: <50ms on booking flow
```

**Metrics Section:**
```markdown
## Metrics

### Booking Flow (Updated 2026-01-28)

- **Completion Rate:** 68% → 72% (+4pp)
  - Source: Performance optimization (BRIK-ENG-0005)
  - Measurement: Google Analytics, 30-day rolling average
  - Target: 75% by end of Q1

- **Page Load Time:** 1.2s → 1.0s (-200ms)
  - Source: Performance optimization (BRIK-ENG-0005)
  - Measurement: Real User Monitoring (RUM)
  - Target: <900ms by end of Q2

- **Support Tickets:** Baseline established (52/month)
  - Next: Track impact of offline mode and user auth
  - Target: Reduce by 20% (10 tickets/month) with self-service
```

### 5. Merge Updates into Plan

**Rules:**
- **Strategy:** Replace or append to current focus items
- **Risks:** Add new risks, update status of existing risks
- **Opportunities:** Add validated opportunities, archive investigated ones
- **Learnings:** Append-only (never delete learnings)
- **Metrics:** Update existing metrics, add new tracked metrics

**Dual-audience mirroring:**
- `.user.md`: Human-readable, narrative format
- `.agent.md`: Structured, data-oriented, includes evidence links

### 6. Commit Changes

```typescript
const writer = createRepoWriter(repoRoot);

await writer.updateFile(
  `docs/business-os/strategy/${businessCode}/plan.user.md`,
  updatedUserContent,
  CommitIdentities.agent
);

await writer.updateFile(
  `docs/business-os/strategy/${businessCode}/plan.agent.md`,
  updatedAgentContent,
  CommitIdentities.agent
);
```

Commit message:
```
Update BRIK business plan: User auth learnings + new risks

- Strategy: Add user auth to current focus (fact-finding complete)
- Risks: GDPR compliance blocker, platform auth compatibility
- Opportunities: Guide offline mode validated (45% user demand)
- Learnings: User auth fact-finding insights
- Metrics: Booking completion +4pp from perf optimization

Source: Card BRIK-ENG-0001 reflection + scan SCAN-2026-01-28
```

## Evidence Requirements

Every plan update must include:

- **Source:** Card ID, scan timestamp, or manual decision reference
- **Evidence type:** customer-input, measurement, repo-diff, experiment, etc.
- **Data:** Specific numbers, quotes, or file references
- **Date:** When evidence was gathered

## Integration with Other Skills

- **After `/work-idea`:** Update Opportunities section with new validated ideas
- **After `/propose-lane-move` to Done:** Trigger reflection and plan update
- **After `/scan-repo`:** Aggregate scan findings into plan updates
- **After `/ideas-go-faster`:** Sweep reads plans and flags gaps/staleness — use this skill to act on sweep recommendations for plan bootstrapping or updates
- **Before planning sessions:** Review plan to inform priority decisions

## Example Session

```
User: /update-business-plan BRIK --card BRIK-ENG-0001

Agent:
Updating BRIK business plan from card BRIK-ENG-0001 reflection...

[Reading reflection stage doc]
Card: BRIK-ENG-0001 (User Authentication)
Lane: Reflected
Completed: 2026-01-28

[Extracting structured information]
✓ Decisions: Scope to email-only (defer social login)
✓ Risks: GDPR compliance (1-2 week delay)
✓ Opportunities: None (feature on hold pending legal)
✓ Learnings: 3 insights captured
✓ Metrics: No impact yet (feature not shipped)

[Reading current business plan]
Plan: docs/business-os/strategy/BRIK/plan.user.md
Last updated: 2026-01-15

[Drafting updates]
Strategy section:
  + User Authentication (Priority: High, blocked on legal)

Risks section:
  + GDPR Compliance (Severity: High)
  + Platform Auth Compatibility (Severity: Medium)

Learnings section:
  + 2026-01-28: User Authentication Feature
    - Early user research prevented scope creep
    - Legal review should start during fact-finding
    - Platform auth integration confirmed

[Merging into plan.user.md and plan.agent.md]
✓ Strategy updated
✓ Risks added (2 new)
✓ Learnings appended
✓ Metrics unchanged (no shipped features yet)

[Committing changes]
✓ Commit: Update BRIK business plan (user auth learnings)
✓ Agent identity used

Done! Plan updated. Pete can review diff:
  git show HEAD -- docs/business-os/strategy/BRIK/plan.user.md
```

## Frequency Recommendations

- **After card reflection:** Update plan with learnings (every completed card)
- **After scans:** Aggregate findings into plan (weekly scans)
- **Before planning sessions:** Comprehensive review and update (monthly)
- **Strategic decisions:** Immediate plan update (ad-hoc)

## Error Handling

- **Plan not found:** Create from template (ask Pete first)
- **Malformed reflection:** Skip update, log warning
- **Conflicting updates:** Ask Pete to resolve manually
- **No meaningful updates:** Skip commit, report "no changes"

## Phase 0 Constraints

- Pete reviews all plan changes (no blind merges)
- Agent identity for all plan commits
- Single business context (one plan at a time)
- Manual trigger only (no automated plan updates)

## Success Metrics

- Plan freshness: Updated within 1 week of card completion
- Learning capture: ≥80% of reflected cards update plan
- Review time: Pete reviews plan diffs in <10 minutes
- Plan accuracy: Plan reflects current strategy (validated monthly)
