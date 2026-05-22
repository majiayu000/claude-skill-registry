---
name: marketing-business
description: Go-to-market strategy builder with channel selection matrix, budget allocation, and 30-day launch action plan. Use when users need to create marketing strategies or go-to-market plans.
---

# Marketing Business

Marketing and customer acquisition skill that guides users through creating structured go-to-market strategies. Produces actionable GTM plans with channel prioritization, budget allocation, and launch timelines.

## When to Use

- User wants to create a go-to-market strategy
- User needs channel recommendations for their business model
- User wants a 30-day launch action plan
- User needs marketing budget allocation guidance

## Workflows

### Go-to-Market Strategy Builder

Guides user through creating a complete GTM plan based on business model, budget, and target audience.

**Reference Files:**
- `references/go-to-market-framework.md` - Complete GTM workflow with channel scoring, budget allocation rules, and action plan templates
- `references/channel-selection-matrix.md` - Channel scoring data for 8+ business model types

**Output File:** `devforgeai/specs/business/marketing/go-to-market.md`

**Workflow Steps:**

1. **Gather Inputs** via AskUserQuestion:
   - Business model type (SaaS B2B, SaaS B2C, Marketplace, D2C, E-commerce, Subscription, Freemium, Agency)
   - Monthly marketing budget range
   - Target audience description

2. **Channel Selection:**
   - Load `references/channel-selection-matrix.md`
   - Score channels based on business model, budget, and audience
   - Rank minimum 3 channels with rationale
   - Allocate budget percentages (must sum to 100%)

3. **30-Day Launch Plan:**
   - Generate minimum 10 action items
   - Assign to 3 time windows: Days 1-7, Days 8-21, Days 22-30
   - Tag each item with responsible role (founder, marketer, engineer)

4. **Output Generation:**
   - Write complete GTM plan to output file
   - Include 4 required sections: Executive Summary, Channel Strategy, Budget Allocation, 30-Day Launch Plan
   - Validate Markdown structure (ATX headings)

**Edge Cases:**
- Zero budget: Recommend organic-only channels
- Unknown business model: Ask up to 3 clarifying questions
- Existing output file: Prompt before overwrite
- Conflicting model/audience: Detect mismatch and advise

### Positioning & Messaging Framework

Guides user through competitive positioning, value proposition, and messaging hierarchy.

**Reference Files:**
- `references/positioning-strategy.md` - Complete positioning workflow with templates

**Output File:** `devforgeai/specs/marketing/positioning-framework.md`

### Customer Discovery

Guides user through customer interview planning, persona development, and insight synthesis.

**Output File:** `devforgeai/specs/marketing/customer-discovery.md`

### Content Strategy

Guides user through content calendar creation, channel mix, and editorial planning.

**Output File:** `devforgeai/specs/marketing/content-strategy.md`

---

## User Profile Adaptive Pacing

When a user profile is available, read it to adapt the workflow pacing based on experience level.

**Profile Detection (optional - when available):**
1. Check if a user profile exists with business context
2. Detect experience level: beginner, experienced, or first-time user

**Adaptive Behavior:**
- **Beginner / first-time:** Full onboarding with detailed explanations at each step
- **Experienced:** Skip introductory explanations, pre-populate known business context fields, and compress pacing

**Pre-population:** When the user profile contains prior business model, audience, or budget data, pre-populate those fields as defaults so the user can confirm or override rather than re-enter.

**Graceful Degradation (BR-003):** If the user profile is not found or unavailable, fall back to the default full-pacing workflow. The profile is optional and never required. Missing profile data must never cause an error or block the workflow.

---

## Project-Anchored Mode

When invoked with `--mode=project`, anchor marketing artifacts to the current DevForgeAI project:

1. Read context files (read-only, immutable - never write to context paths):
   - `devforgeai/specs/context/tech-stack.md` - Extract product technology for positioning
   - `devforgeai/specs/context/source-tree.md` - Understand product structure

2. Store output artifacts in `devforgeai/specs/marketing/` with timestamped filenames using YYYY-MM-DD format (e.g., `go-to-market-2026-03-05.md`)

Context files are read-only. This skill never writes to `devforgeai/specs/context/` paths.

---

## Session Resume

Before generating new artifacts, detect if a prior session exists by checking for existing output files in the marketing output directory.

**Detection:**
- Check `devforgeai/specs/marketing/` or `devforgeai/specs/business/marketing/` for existing artifacts
- Identify the last completed phase or workflow from prior session progress

**Resume Prompt:**
When a previous session is found, present the user with options via AskUserQuestion:
- **Resume** — Continue from last completed phase
- **Start fresh** — Begin a new session

Prior sessions are never silently overwritten. Always prompt the user before overwriting existing artifacts. Use AskUserQuestion to confirm the user's intent before any modification to prior session data.

---

## On-Demand Reference Loading

Load reference files only when needed:

```
Read(file_path="references/go-to-market-framework.md")
Read(file_path="references/channel-selection-matrix.md")
Read(file_path="references/positioning-strategy.md")
```

---

## Business Rules

- Budget allocation percentages must sum to 100%
- Minimum 3 channels ranked per recommendation
- Minimum 10 action items in 30-day plan
- All action items must have role tags
- Zero-budget input produces organic-only recommendations

## References

- EPIC-075: Marketing & Customer Acquisition
- STORY-539: Go-to-Market Strategy Builder
- STORY-541: Marketing Plan Command & Skill Assembly
