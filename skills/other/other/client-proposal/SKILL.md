---
name: client-proposal
description: Write a professional client proposal from a brief. Sections include Executive Summary, Understanding Your Challenge, Our Approach, Scope of Work, Timeline, Investment, and Next Steps. Confident, specific, closes with clear CTA. 2-4 pages. Use when user needs a "proposal", "client pitch document", or "project proposal".
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Client Proposal Writer

**Purpose:** Write a professional, conversion-focused proposal that demonstrates understanding of the client's challenge and presents a clear path to results. The proposal should feel like it was written specifically for this client (because it was).

## When to Activate

Use this skill when:
- User needs a client proposal or pitch document
- User has project details and wants a formal proposal
- User mentions "proposal", "pitch deck", or "project pitch"

## Required Input

- **Client name and business**
- **The challenge/project** (what they need)
- **Proposed solution** (what the user will deliver)
- **Deliverables** (specific outputs)
- **Timeline** (estimated)
- **Pricing** (or pricing range)
- **Any context from discovery calls or emails**

## Structure

### Cover / Header
```
[User's Business Name]

PROPOSAL FOR: [Client Name]
[Project Title]
[Date]

Prepared by: [User Name from USER.md]
```

### Section 1: Executive Summary (100-150 words)
One paragraph that captures: the problem, the solution, the expected outcome, and the investment. A busy executive should get the full picture from this alone.

### Section 2: Understanding Your Challenge (200-300 words)
Demonstrate that you understand their situation better than they do. Reflect their pain points back to them, show insight into the root cause, and frame the opportunity.

**Rules:**
- Use their language (from the brief or discovery call)
- Show insight, not just repetition
- Connect the challenge to a business impact (money, time, reputation)

### Section 3: Our Approach (200-300 words)
Explain HOW you'll solve the problem. Focus on methodology, not just deliverables.

**Include:**
- Your process (high-level steps)
- Why this approach works
- What makes your approach different
- How you'll keep them in the loop

### Section 4: Scope of Work (Variable)

| # | Deliverable | Description | Timeline |
|---|------------|-------------|----------|
| 1 | [Deliverable] | [What it includes] | [When] |
| 2 | [Deliverable] | [What it includes] | [When] |
| 3 | [Deliverable] | [What it includes] | [When] |

**Include:**
- Numbered deliverables with clear descriptions
- What IS included
- What is NOT included (sets boundaries)

### Section 5: Timeline

```
Phase 1: [Name] — Week 1-2
[What happens in this phase]

Phase 2: [Name] — Week 3-4
[What happens]

Phase 3: [Name] — Week 5-6
[What happens]

Estimated completion: [Date]
```

### Section 6: Investment

| Item | Price |
|------|-------|
| [Core service] | $[X] |
| [Additional if applicable] | $[X] |
| **Total** | **$[X]** |

**Payment terms:**
- [Deposit/milestone structure]
- [Payment methods accepted]

**Optional:** Include payment plans or retainer pricing

### Section 7: Next Steps (50-100 words)
Clear CTA — what happens if they say yes.

```
Ready to move forward? Here's what happens next:

1. Reply to this proposal or sign below
2. I'll send the agreement and invoice for the deposit
3. We kick off [start date] with [first step]

Questions? [Contact method]
```

## Output Format

```markdown
# [Project Title]
## Proposal for [Client Name]

**Prepared by:** [User Name]
**Date:** [Date]

---

### Executive Summary
[Paragraph]

---

### Understanding Your Challenge
[Content]

---

### Our Approach
[Content]

---

### Scope of Work
[Deliverables table]

**Included:** [List]
**Not included:** [List]

---

### Timeline
[Phase breakdown]

---

### Investment
[Pricing table + payment terms]

---

### Next Steps
[CTA]
```

## Quality Checklist

- [ ] Executive summary stands alone (full picture in one paragraph)
- [ ] "Understanding" section uses client's language and shows insight
- [ ] Approach explains WHY, not just WHAT
- [ ] Scope of work is specific with clear deliverables
- [ ] "Not included" boundaries are set
- [ ] Timeline is realistic with milestones
- [ ] Pricing is clear with payment terms
- [ ] Next steps have a clear, easy CTA
- [ ] Tone is confident and professional (not desperate)
- [ ] Based entirely on user-provided information (no fabrication)
