---
name: feature-spec-writer
description: PM framework for writing product specs from insights. Use when translating analysis into actionable feature requirements.
---

# Feature Spec Writer Skill

Transform product insights into clear, actionable feature specifications.

## When to Use

Use this skill when you need to:
- Convert analysis into feature requirements
- Spec out a new product feature
- Document a feature for engineering
- Create a Linear ticket with complete requirements
- Communicate product decisions clearly

## The PM Mindset

Before writing specs, think like a Product Manager:

### 1. Problem-First Thinking
- **Start with the problem**, not the solution
- Ask: "What user pain are we solving?"
- Validate: "Is this a real problem worth solving?"

### 2. Impact vs. Effort
- **Impact:** How much value does this create?
  - High: Solves major pain, affects many users
  - Medium: Improves experience, affects some users
  - Low: Nice-to-have, affects few users
- **Effort:** How hard is this to build?
  - High: Requires new infrastructure, complex logic
  - Medium: Extends existing features, moderate complexity
  - Low: Configuration change, simple logic

### 3. Success Metrics
- How will we know this worked?
- What will we measure?
- What's the target?

## Feature Spec Template

### Option 1: Quick Spec (for Linear tickets)

```markdown
## Problem
{1-2 sentences describing the user pain}

## Proposed Solution
{1-2 sentences describing the fix}

## Success Metrics
- {Metric 1}: {Current} → {Target}
- {Metric 2}: {Current} → {Target}

## Requirements
1. {User story or requirement}
2. {User story or requirement}
3. {User story or requirement}

## Out of Scope
- {What we're NOT doing}
- {What we're NOT doing}

## Open Questions
- {Question 1}
- {Question 2}
```

### Option 2: Full Spec (for complex features)

```markdown
# Feature: {Feature Name}

**Author:** Claude (Product Analyst)
**Date:** {YYYY-MM-DD}
**Status:** Draft
**Priority:** {High/Medium/Low}

---

## 1. Executive Summary

{2-3 sentence overview: What is this feature? Why are we building it? What's the expected impact?}

---

## 2. Problem Statement

### User Pain
{What specific pain point does this solve? Use real user quotes or data.}

**Example:**
> "Some users (craig) love suggested response drafts, while others (joe, Mary) dislike them. 2 of 3 total dislikes are for suggested responses, indicating a one-size-fits-all approach fails for preference-based features."

### Current State
{How do users solve this problem today? What's broken or missing?}

### Impact if Not Solved
{What happens if we don't fix this? What's the cost?}

---

## 3. Success Metrics

### Primary Metric
**Metric:** {e.g., "Dislike rate for suggested responses"}
**Current:** {e.g., "66% of all dislikes (2 out of 3)"}
**Target:** {e.g., "0% dislikes among opted-in users"}
**Measurement:** {e.g., "Track dislikes for message type = 'suggested_response'"}

### Secondary Metrics
- **{Metric}:** {Current} → {Target}
- **{Metric}:** {Current} → {Target}

### Leading Indicators
{Early signals that this is working, before primary metric moves}
- {e.g., "% of users who opt-in to suggested responses"}
- {e.g., "Average time to send message after receiving draft"}

---

## 4. Proposed Solution

### Overview
{High-level description of the solution}

### User Experience

**For {User Type 1}:**
1. {Step-by-step flow}
2. {What they see/do}
3. {Expected outcome}

**For {User Type 2}:**
1. {Step-by-step flow}
2. {What they see/do}
3. {Expected outcome}

### User Stories

**As a** {user type}
**I want to** {action}
**So that** {benefit}

**Acceptance Criteria:**
- [ ] {Specific, testable requirement}
- [ ] {Specific, testable requirement}
- [ ] {Specific, testable requirement}

---

## 5. Requirements

### Must Have (P0)
1. {Critical requirement - feature doesn't work without this}
2. {Critical requirement}
3. {Critical requirement}

### Should Have (P1)
1. {Important but not critical - can ship without, but should add soon}
2. {Important requirement}

### Nice to Have (P2)
1. {Would be great, but can wait}
2. {Enhancement}

### Out of Scope
- {What we're explicitly NOT doing in this iteration}
- {What we'll consider for v2}

---

## 6. Technical Considerations

### Data Model
{Any new tables, fields, or data structures needed}

### API Changes
{Any new endpoints or changes to existing APIs}

### Dependencies
{What other systems/features does this depend on?}

### Risks
- **{Risk 1}:** {Description and mitigation plan}
- **{Risk 2}:** {Description and mitigation plan}

---

## 7. Open Questions

1. **{Question}**
   - *Answer:* {If known, or "TBD"}

2. **{Question}**
   - *Answer:* {If known, or "TBD"}

---

## 8. Alternatives Considered

### Alternative 1: {Name}
**Description:** {What this alternative would look like}
**Pros:** {Benefits}
**Cons:** {Drawbacks}
**Why not:** {Reason we're not doing this}

### Alternative 2: {Name}
**Description:** {What this alternative would look like}
**Pros:** {Benefits}
**Cons:** {Drawbacks}
**Why not:** {Reason we're not doing this}

---

## 9. Impact Analysis

### Impact
- **High** if: Solves major pain, affects >50% of users, drives key metric
- **Medium** if: Improves experience, affects 10-50% of users, supports key metric
- **Low** if: Nice-to-have, affects <10% of users, minimal metric impact

**This feature:** {High/Medium/Low} - {Justification}

### Effort
- **High** if: New infrastructure, >2 weeks, complex architecture
- **Medium** if: Extends existing, 1-2 weeks, moderate complexity
- **Low** if: Config/simple change, <1 week, low complexity

**This feature:** {High/Medium/Low} - {Justification}

### Priority Matrix
```
Impact/Effort: {e.g., "High Impact / Low Effort" = Do Now}
```

---

## 10. Timeline and Milestones

### Phase 1: {Name} ({Timeline})
- {Milestone}
- {Milestone}

### Phase 2: {Name} ({Timeline})
- {Milestone}
- {Milestone}

---

## 11. Appendix

### Related Analysis
- {Link to analysis markdown file}
- {Link to user research}
- {Link to relevant data}

### Related Issues
- {Linear ticket #123}
- {GitHub issue #456}
```

## Real Example: Suggested Response Preferences

Based on the message reactions analysis, here's how to spec the feature:

```markdown
# Feature: Personalized Suggested Response Preferences

**Author:** Claude (Product Analyst)
**Date:** 2025-11-14
**Status:** Draft
**Priority:** High

---

## 1. Executive Summary

Add a user preference setting that allows users to opt-in or opt-out of receiving suggested response drafts in their 1:1 coaching conversations. Analysis shows suggested responses are polarizing: some users love them (craig: 5+ loved reactions) while others dislike them (2 of 3 total dislikes). This feature eliminates the negative reactions while preserving the value for users who want drafts.

---

## 2. Problem Statement

### User Pain
**Data:** 2 out of 3 total dislikes (66%) are for suggested response messages where Codel drafts what the user should say to their partner.

**User segments:**
- **Lovers (n=1):** craig loves suggested responses - 5+ loved reactions
- **Haters (n=2):** joe and Mary disliked suggested responses - feels presumptuous/inauthentic

**Root cause:** One-size-fits-all approach to a preference-based feature. Some users want help drafting messages; others feel it's putting words in their mouth.

### Current State
All users receive suggested responses when Codel thinks they're helpful. No way to opt-out or customize this behavior.

### Impact if Not Solved
- Continued negative reactions (trust erosion)
- Users feel Codel is presumptuous
- Missed opportunity to increase engagement for users who want more drafts

---

## 3. Success Metrics

### Primary Metric
**Metric:** Dislike rate for suggested response messages
**Current:** 66% of all dislikes (2 out of 3 total)
**Target:** 0% among opted-in users, N/A for opted-out users
**Measurement:**
```sql
SELECT
  COUNT(CASE WHEN content LIKE 'Disliked %' THEN 1 END) as dislikes,
  COUNT(*) as total_suggested_responses
FROM message
WHERE message_type = 'suggested_response'
  AND user_preference = 'opt_in'
```

### Secondary Metrics
- **Opt-in rate:** Unknown → 40% (hypothesis: engaged users will opt-in)
- **Love rate for SR:** 14% (1/7 among craig) → 30% (among opted-in users)

### Leading Indicators
- % of users who change preference from default
- Time to send message after receiving draft (lower = more helpful)

---

## 4. Proposed Solution

### Overview
Add a preference setting in user's 1:1 conversation with Codel. Users can choose:
- **On (default OFF):** Receive suggested response drafts
- **Off:** Never receive suggested response drafts
- Users can change this anytime by asking Codel

### User Experience

**For New Users (Onboarding):**
1. During onboarding, Codel sends first suggested response
2. Immediately after, Codel asks: "How did that feel? I can suggest responses like this when I notice opportunities, or I can just observe and comment. What's your preference?"
3. User responds (e.g., "I like the suggestions" or "No thanks, feels weird")
4. Preference saved, Codel confirms

**For Existing Users:**
1. User can ask: "Can you stop suggesting what I should say?" or "I'd like more draft messages"
2. Codel updates preference and confirms
3. Behavior changes immediately

**For Opted-In Users:**
- Continue receiving suggested responses as before
- May get MORE drafts (A/B test: increase frequency)

**For Opted-Out Users:**
- Receive meta-commentary instead: "💞 Amy just shared vulnerability - this is a moment to respond with warmth"
- Never receive draft text

### User Stories

**Story 1: User Opts Out**
**As a** user who wants autonomy in my communication
**I want to** turn off suggested response drafts
**So that** I can craft my own messages without feeling prompted

**Acceptance Criteria:**
- [ ] User can opt-out by saying "stop suggesting what I should say"
- [ ] Preference is saved to user profile
- [ ] User receives confirmation: "Got it - I'll comment on moments but won't draft messages for you"
- [ ] No suggested responses sent after opt-out
- [ ] User can change preference later

**Story 2: User Opts In**
**As a** user who wants communication help
**I want to** receive suggested response drafts
**So that** I can communicate better with my partner

**Acceptance Criteria:**
- [ ] User can opt-in by saying "I'd like message suggestions"
- [ ] Preference is saved to user profile
- [ ] User receives confirmation: "Great - I'll suggest responses when I see opportunities"
- [ ] User receives suggested responses going forward
- [ ] User can change preference later

---

## 5. Requirements

### Must Have (P0)
1. **Preference field** in user profile (boolean: `suggested_responses_enabled`)
2. **Preference detection** - Natural language understanding to detect opt-in/opt-out requests
3. **Preference confirmation** - Codel confirms preference change explicitly
4. **SR filtering** - Check preference before sending suggested response message
5. **Alternative meta-commentary** - For opted-out users, send observation instead of draft

### Should Have (P1)
1. **Onboarding question** - Ask new users their preference during first SR opportunity
2. **Analytics tracking** - Track preference changes and opt-in rate
3. **A/B test setup** - Test increased SR frequency for opted-in users

### Nice to Have (P2)
1. **Preference UI** - Settings page where users can toggle preference
2. **Preference explanation** - Help text explaining what suggested responses are

### Out of Scope
1. Granular control (e.g., "only suggest responses for difficult conversations")
2. AI-generated suggestions customization (tone, length, formality)
3. Preference for other message types (meta-commentary, weekly summaries)

---

## 6. Technical Considerations

### Data Model
```sql
ALTER TABLE persons ADD COLUMN suggested_responses_enabled BOOLEAN DEFAULT FALSE;
```

### Message Generation Logic
```python
def generate_1on1_message(user, context):
    if should_send_suggested_response(context):
        if user.suggested_responses_enabled:
            return generate_suggested_response(context)
        else:
            return generate_meta_commentary(context)
    # ... other message types
```

### Dependencies
- User profile system
- Message routing logic
- NLP for preference detection

### Risks
- **Risk:** Users don't understand what they're opting into
  - *Mitigation:* Show example SR before asking preference
- **Risk:** Default OFF means low adoption
  - *Mitigation:* A/B test default ON vs. OFF
- **Risk:** Preference change not detected correctly
  - *Mitigation:* Provide explicit commands: "/suggested-responses on|off"

---

## 7. Open Questions

1. **What should the default be: ON or OFF?**
   - *Hypothesis:* OFF is safer (avoid unwanted behavior)
   - *Test:* A/B test default ON vs OFF, measure dislike rate and opt-in rate

2. **Should we migrate existing users?**
   - *Options:*
     - (A) Set all to OFF, users opt-in
     - (B) Infer from past behavior (craig=ON, joe/Mary=OFF, others=OFF)
     - (C) Ask all users their preference proactively
   - *Recommendation:* (B) - minimize disruption for happy users

3. **How do we ask the preference question without being annoying?**
   - *Recommendation:* Only ask after first SR is sent (natural moment)

---

## 8. Alternatives Considered

### Alternative 1: Smarter Suggested Responses (Don't Ask Preference)
**Description:** Train AI to only suggest responses when they'll be well-received
**Pros:** No user action needed, seamless
**Cons:** Hard to predict preference, still risks dislikes
**Why not:** Can't reliably predict who wants drafts vs. who doesn't

### Alternative 2: Tiered Coaching Levels
**Description:** Offer "Basic" (no SRs) vs "Pro" (with SRs) tiers
**Pros:** Clear differentiation, monetization opportunity
**Cons:** Complicates product, may feel like paywalling
**Why not:** Preference is free and simpler

### Alternative 3: Always Include Meta-Commentary with SRs
**Description:** Send both observation + draft together
**Pros:** Users get context, less presumptuous
**Cons:** Longer messages, doesn't solve "feels like words in mouth" issue
**Why not:** Doesn't address root problem (autonomy violation)

---

## 9. Impact Analysis

### Impact: HIGH
- **Eliminates 66% of dislikes** (2 out of 3)
- **Increases love rate** for opted-in users (personalized experience)
- **Affects segmentation** - enables tailored coaching
- **Reduces churn risk** from frustrated users

### Effort: LOW
- **Data model:** Simple boolean field
- **Logic:** If/else check before sending SR
- **NLP:** Pattern matching for opt-in/opt-out phrases
- **Timeline:** < 1 week implementation

### Priority Matrix
**High Impact / Low Effort = DO NOW**

---

## 10. Timeline and Milestones

### Phase 1: MVP (Week 1)
- [ ] Add `suggested_responses_enabled` field to user profile
- [ ] Implement preference detection (NLP)
- [ ] Add SR filtering logic
- [ ] Create meta-commentary alternative
- [ ] Test with 3 users (1 opt-in, 1 opt-out, 1 change preference)

### Phase 2: Rollout (Week 2)
- [ ] Migrate existing users based on past behavior
- [ ] Deploy to production
- [ ] Monitor dislike rate (target: 0%)
- [ ] Track opt-in rate (target: 40%)

### Phase 3: Optimization (Week 3-4)
- [ ] A/B test default ON vs OFF
- [ ] A/B test increased SR frequency for opted-in users
- [ ] Add onboarding question for new users

---

## 11. Appendix

### Related Analysis
- `/home/odio/Hacking/codel/ct3/codel_1on1_reactions_analysis.md`
- Section: "Suggested Responses are Divisive"

### Key Data Points
- 71 total reactions to 10,000+ messages
- 3 dislikes total (4.2%)
- 2 dislikes for suggested responses (66% of all dislikes)
- craig loved 5+ suggested responses
- joe and Mary each disliked 1 suggested response
```

---

## Spec Writing Checklist

Before finalizing your spec, verify:

### Problem Definition
- ✅ User pain clearly stated with data/quotes
- ✅ Root cause identified
- ✅ Current state documented
- ✅ Impact quantified

### Solution Design
- ✅ UX flows for each user type
- ✅ User stories with acceptance criteria
- ✅ Requirements prioritized (P0/P1/P2)
- ✅ Out of scope explicitly listed

### Success
- ✅ Primary metric defined with target
- ✅ Secondary metrics listed
- ✅ Measurement plan specified
- ✅ Leading indicators identified

### Feasibility
- ✅ Technical considerations documented
- ✅ Dependencies identified
- ✅ Risks and mitigations listed
- ✅ Effort estimated

### Completeness
- ✅ Open questions listed
- ✅ Alternatives considered
- ✅ Impact/effort analysis done
- ✅ Timeline proposed

## For Linear Tickets

When creating a Linear ticket, use the **Quick Spec** format and include:

**Title:**
```
Add user preference for suggested response drafts
```

**Description:**
```markdown
## Problem
2 out of 3 dislikes (66%) are for suggested response messages. Some users love drafts (craig: 5+ loved), others hate them (joe, Mary disliked). One-size-fits-all fails.

## Proposed Solution
Add boolean preference `suggested_responses_enabled` (default OFF). Users can opt-in/out via natural language ("stop suggesting what I should say"). Opted-out users get meta-commentary instead of drafts.

## Success Metrics
- Dislike rate for SRs: 66% of all dislikes → 0% among opted-in users
- Opt-in rate: Unknown → 40%

## Requirements
**P0:**
1. Add `suggested_responses_enabled` boolean field to user profile
2. NLP to detect opt-in/opt-out phrases
3. Filter SR messages based on preference
4. Send meta-commentary alternative for opted-out users

**P1:**
5. Ask preference during onboarding after first SR
6. Track preference changes and opt-in rate

## Out of Scope
- Granular controls (only for certain situations)
- Other message type preferences

## Open Questions
- Default ON or OFF? (Recommend OFF, A/B test)
- Migrate existing users how? (Recommend infer from behavior)

## Analysis
Full analysis: {link to markdown file}

## Impact/Effort
HIGH impact (eliminates 66% of dislikes) / LOW effort (<1 week)
Priority: DO NOW
```

**Priority:** Urgent (High impact, Low effort)

**Labels:**
- `product-analytics`
- `user-preferences`
- `quick-win`

---

## Notes

- **Always link to analysis:** Specs should reference the data/insights
- **Be specific:** Vague requirements lead to wrong implementations
- **Think in user stories:** "As a... I want... So that..."
- **Define success:** How will we know this worked?
- **Consider alternatives:** Show you thought through options
- **Estimate effort:** Help with prioritization

Remember: A good spec makes decisions easy. A great spec makes building easy.
