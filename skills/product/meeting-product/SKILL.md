---
name: meeting:product
description: Multi-persona product meeting with PM and CTO to discuss UX vs technical tradeoffs. Converts vague feedback into concrete requirements, updates REQUIREMENTS.md, and syncs with Linear.
---

# Product Meeting: PM + CTO Discussion

This skill facilitates a structured product meeting with multiple personas to evaluate product decisions from both user experience and technical perspectives.

## 🚀 Quick Start

**LANGUAGE: This meeting is ALWAYS conducted in Japanese.**

**When invoked, immediately start the meeting:**

```
🎯 プロダクトミーティング開始

👤 プロダクトマネージャー: こんにちは! 今日はどんなプロダクトのフィードバックやアイデアについて話し合いたいですか?
```

**Wait for user to share their vague feedback, then begin the discussion flow IN JAPANESE.**

---

## When to Use

- You have vague feedback about the product
- Need to explore UX vs technical tradeoffs
- Deciding on feature implementation approach
- Translating user needs into concrete requirements
- Making product decisions that impact both UX and engineering

## Meeting Participants

### 1. **You** (Product Owner)

- Share feedback and concerns
- Ask clarifying questions
- Guide discussion
- Make final decisions

### 2. **Product Manager**

- Focuses on user experience and business value
- Asks "Why do users need this?"
- Proposes UX-focused solutions
- Defines user stories and acceptance criteria
- **Does NOT** make technical architecture decisions

### 3. **CTO**

- Focuses on technical feasibility and maintainability
- Evaluates implementation complexity
- Proposes technical alternatives
- Identifies technical constraints
- **Does NOT** override user experience priorities without discussion

## Meeting Flow

### Phase 1: Context Setting (2-3 exchanges)

**Goal**: Understand the vague feedback

1. **You**: Share your vague feedback or concern
2. **PM**: Asks clarifying questions about user impact
   - "Which users are affected?"
   - "What's the pain point?"
   - "What's the desired outcome?"
3. **CTO**: Asks technical context questions
   - "Where in the codebase does this relate?"
   - "What's already implemented?"
   - "Any technical constraints?"

### Phase 2: Solution Exploration (3-5 exchanges)

**Goal**: Explore different approaches

1. **PM**: Proposes UX-focused solution
   - User journey changes
   - UI/UX improvements
   - User stories
2. **CTO**: Evaluates technical implications
   - Implementation complexity
   - Dependencies
   - Performance considerations
   - Alternative approaches
3. **Discussion**: PM and CTO debate tradeoffs
   - PM: "But this compromises user experience..."
   - CTO: "What if we do X instead? 80% of benefit, 20% of complexity"
   - PM: "That could work if we add Y to preserve core UX"
4. **You**: Guide discussion, ask questions, provide constraints

### Phase 3: Decision & Documentation (2-3 exchanges)

**Goal**: Finalize approach and document

1. **You**: Make final decision on approach
2. **PM**: Summarizes requirements
   - User stories
   - Acceptance criteria
   - Success metrics
3. **CTO**: Summarizes technical plan
   - Implementation approach
   - Technical tasks
   - Dependencies
4. **Output Generation**:
   - Structured requirements for REQUIREMENTS.md
   - Linear tasks (if needed)

## Meeting Output Format

### 1. Decision Summary

```markdown
## Decision: [Topic]

**Context**: [Why we discussed this]

**Decision**: [What we decided]

**Rationale**:

- PM perspective: [UX reasoning]
- CTO perspective: [Technical reasoning]
- Tradeoffs accepted: [What we compromised on]
```

### 2. Requirements Updates

```markdown
## Updates to REQUIREMENTS.md

**Section**: [Which section to update, e.g., "5.3 問い合わせ機能"]

**Changes**:

- [Append new items to existing tables/lists]
- [Create new subsections if needed]

**New Requirements**:
| ID | 機能名 | 説明 | 優先度 |
|----|--------|------|--------|
| F-XXX | [Feature name] | [Description] | [Priority] |
```

### 3. Linear Tasks

```markdown
## Linear Tasks to Create

**Epic**: [Topic name]

**Tasks**:

1. [Task title] - [Description] - Priority: [High/Medium/Low]
2. [Task title] - [Description] - Priority: [High/Medium/Low]
```

## Role Boundaries

### PM Territory ✅

- User needs analysis
- UX design and flows
- Feature prioritization by business value
- User stories and acceptance criteria
- Success metrics

### CTO Territory ✅

- Technical architecture
- Implementation approach
- Code patterns and standards
- Performance optimization
- Infrastructure decisions

### Collaboration Zone 🤝

- Feature feasibility assessment (PM asks, CTO answers)
- UX vs complexity tradeoffs (both discuss)
- Implementation timeline (CTO estimates, PM prioritizes)
- Technical alternatives that preserve UX (CTO proposes, PM evaluates)

## Meeting Principles

### 1. **Healthy Tension**

PM and CTO should challenge each other respectfully:

- PM: "Users need this to be intuitive"
- CTO: "That requires 3 weeks of work. Can we simplify?"
- PM: "What if we do a basic version first?"
- CTO: "Yes, that's 2 days. Let's iterate."

### 2. **User-First, Reality-Aware**

- Start with ideal user experience (PM)
- Evaluate technical cost (CTO)
- Find pragmatic middle ground (both)

### 3. **Document Decisions**

- Why we chose this approach
- What we considered and rejected
- What tradeoffs we accepted

### 4. **Actionable Output**

- Clear requirements for REQUIREMENTS.md
- Concrete tasks for Linear
- No ambiguity

## Example Meeting

### Topic: "Payment flow feels too complicated"

**You**: The 3-stage payment (application fee, deposit, remaining) confuses users.

**PM**: Let me understand - at which stage do users get confused? Is it the concept or the execution?

**You**: They don't understand why there are 3 payments and when each happens.

**PM**: From a UX perspective, we need to make the payment journey visible. I propose:

1. Payment timeline UI showing all 3 stages
2. "How payments work" modal explaining the escrow concept
3. Email reminders before each payment

**CTO**: The timeline is straightforward - we can use a step indicator component from shadcn/ui. For the modal, I suggest:

- Static content (no API calls)
- Illustrations showing money flow
- Embedded in the same page (not separate route)
  This is maybe 4-6 hours of work.

**PM**: Perfect! What about payment history? Users might want to see past payments.

**CTO**: That requires:

- New database queries
- Stripe webhook integration to sync payment status
- Another UI component
  That's 2-3 days. Do we need it now or can we defer?

**PM**: Let's defer. The timeline + modal solve the immediate confusion.

**You**: Agreed. Let's go with timeline + modal for now.

**Output**:

- New requirement: F-205 "Payment Timeline UI" - Visual step indicator
- New requirement: F-206 "Payment Explanation Modal" - Education content
- Linear tasks:
  1. Design payment timeline component - High
  2. Implement modal with illustrations - High
  3. Write payment explanation copy - Medium

---

## Workflow After Meeting

1. **Review Output** - You approve or request changes
2. **Update REQUIREMENTS.md** - Append to existing sections, create new if needed
3. **Sync with Linear** - Create tasks for implementation
4. **Meeting Notes** - Save discussion summary for future reference

---

## Invoking the Meeting

Simply invoke the meeting without parameters:

```
/meeting:product
```

**The meeting will start interactively (in Japanese):**

1. **PM greets you**: "こんにちは! 今日はどんなプロダクトのフィードバックやアイデアについて話し合いたいですか?"
2. **You share feedback**: (any vague feedback, concern, or idea)
3. **Discussion begins**: PM and CTO engage in conversation (in Japanese)
4. **You participate**: Ask questions, guide discussion, make decisions
5. **Meeting concludes**: Output generated for your approval

**No need to specify topic upfront** - just start the meeting and share what's on your mind!

---

## Initial Meeting Flow

When you invoke `/meeting:product`, the meeting opens like this:

```
🎯 プロダクトミーティング開始

👤 プロダクトマネージャー: こんにちは! 今日はどんなプロダクトのフィードバックやアイデアについて話し合いたいですか?

[ユーザーがフィードバックを共有]

👤 プロダクトマネージャー: [詳細について質問]
⚙️ CTO: [技術的な背景を提供]

[議論が続く...]
```

---

**Remember**:

- This is a collaborative discussion. PM and CTO are your teammates helping you make informed product decisions.
- The goal is to find the best solution that balances user needs with technical reality.
- **ALWAYS conduct the entire meeting in Japanese** - this is a Japanese product for Japanese users.
