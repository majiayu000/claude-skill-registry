---
name: fixed-appetite-product-cycles
description: Replace open-ended time estimates with fixed "appetites" to prevent scope creep. Use this when projects consistently miss deadlines, teams feel burnt out by endless sprints, or product development feels bloated and slow.
---

# Fixed-Appetite Product Cycles

Stop asking "How long will this take?" and start asking "How much is this worth to us?" By setting a fixed budget (an appetite) rather than a variable estimate, you force teams to find the simplest, most effective version of a feature that fits within a set timeframe.

## The Shape Up Framework

### 1. Set the Appetite
Instead of estimating work, decide how much time you are willing to spend on a problem. 
- **Small Batch:** 1–2 weeks for minor tweaks or small features.
- **Big Batch:** Up to 6 weeks for significant features or infrastructure.
- **The Hard Limit:** Never commit to a project longer than 6 weeks. If it’s bigger, break it down or "shape" it into a smaller version.

### 2. Form Small Teams
Assign work to the smallest possible unit: **one designer and one engineer.**
- Small teams reduce communication overhead and meetings.
- They have full autonomy to "trade concessions"—reducing the scope of the "how" to meet the deadline of the "what."

### 3. The "Circuit Breaker" Rule
If a project is not finished within its allotted 6-week cycle, it is canceled by default.
- This prevents "zombie projects" that drain morale for months.
- If the feature is truly important, it can be re-shaped and re-pitched for a future cycle, but it does not get an automatic extension.

### 4. Use Hill Charts for Progress
Move away from linear checklists or "percent complete" metrics, which are often lies. Track work based on two phases:
- **Uphill (Figuring it out):** You are still pushing against uncertainty. You don't yet know all the tasks required.
- **Downhill (Execution):** You have solved the unknowns. You can see the finish line and just need to put in the hours.

### 5. Mandatory Cool-Down
After every 6-week cycle, schedule a **2-week cool-down.**
- No scheduled projects or pitches.
- Teams use this time to fix bugs, explore new ideas, or handle administrative tasks.
- This prevents "sprint exhaustion" and allows leaders time to "shape" the work for the next cycle.

---

## Execution Guide

1.  **Shape the Pitch:** Before the cycle starts, a lead "shapes" the work by defining boundaries, rough sketches, and what is *out* of scope. Do not provide a 50-page spec; provide a "fat marker" sketch.
2.  **The Betting Table:** Leaders look at the shaped pitches and "bet" their 6-week cycle on the ones with the highest perceived value.
3.  **The Hand-off:** Give the team the pitch and the 6-week deadline. They are responsible for discovering the tasks and defining the work.
4.  **Trade Concessions:** As the deadline nears, the team must aggressively cut "nice-to-have" details to ensure the "must-have" core is polished and shipped.

---

## Examples

**Example 1: Adding a "Thank You" Note Feature**
- **Context:** A PM wants to add personalized thank-you notes for customers.
- **Input:** "I think we need a full HTML editor for notes."
- **Application of Appetite:** The leader says, "We have a 1-week appetite for this." 
- **Output:** The team realizes an HTML editor is too complex for 1 week. They instead ship a plain-text field with three pre-set templates. It solves 90% of the need in 10% of the time.

**Example 2: Updating the Billing System**
- **Context:** The internal billing system is slow and needs an overhaul.
- **Input:** "This is a 6-month project."
- **Application of Appetite:** The leader says, "We only bet in 6-week increments. What is the most critical 6-week version of this?"
- **Output:** The team identifies that 80% of the slowness comes from one specific database query. They spend 6 weeks refactoring only that part. The system becomes "fast enough" without a total rewrite.

---

## Common Pitfalls

- **Breaking the Circuit Breaker:** Granting "just one more week" to a failing project. This destroys the integrity of the system and teaches the team that deadlines don't matter.
- **Over-specifying the Work:** If you give a team a list of 50 sub-tasks, you’ve removed their ability to trade concessions. They will focus on checking boxes instead of shipping the best version that fits the time.
- **Skipping Cool-Downs:** Moving immediately from one 6-week cycle to the next leads to burnout and prevents long-term strategic "shaping" of the product.
- **Promising "By End of Year":** Avoid long-term promises. The further away the date, the easier it is to promise, and the more likely you are to be wrong. Only commit to the next 6 weeks.