---
name: dcode:jtbd-copy
description: Use when writing or reviewing UI copy - rewrites labels, CTAs, helpers, and placeholders through a Jobs to Be Done lens so every element reflects the user's actual goal, not the system's internal model.
---

# JTBD Copy

Rewrite UI copy so every element reflects the user's job, not the feature's structure.

**For designers who think:** "This form says 'Custom message'... but what is the user actually doing here?"

## Core Principle

UI copy that mirrors the system's model ("Submit form", "Custom message field") forces users to translate. Copy that mirrors the user's job ("Send this to your client", "Personal note") makes the next step feel obvious.

## When to Use

- Writing copy for a new feature
- Reviewing existing UI for clarity
- A form, flow, or page feels functional but cold
- Users drop off or hesitate mid-flow
- Copy was written by engineers and needs a design pass

## The Framework

### 1. State the Job

Before touching any copy, write one sentence: **"The user is trying to [job]."**

Example: "The user is trying to get their client set up on a product so they can earn their commission."

This sentence becomes the filter for every word on the screen.

### 2. Audit Every Element

Walk through each UI element and ask: **"Does this reflect the job, or the system?"**

| Element type | System-framed | Job-framed |
|--------------|---------------|------------|
| **Header** | (none) or feature name | What the user is doing: "Send this to your client" |
| **Field label** | Database column: "Custom message" | User's action: "Personal note" |
| **Placeholder** | Prescribed copy | Helpful prompt: "Add a message to include..." |
| **Helper text** | (none) | Why it matters: "Builds trust and shows this comes from you" |
| **Info text** | Dense legal, buried | Simplified, surfaced: "Your client will create an account and complete checkout." |
| **Primary CTA** | Generic: "Submit" | Job completion: "Send to client" |
| **Secondary CTA** | Equal visual weight | Demoted: "Copy link instead" (text link) |

### 3. Apply the Hierarchy

Not all elements need the same treatment:

1. **Header** -- Frame the job. This is the "you are here" signal.
2. **Primary CTA** -- Name the outcome, not the action. "Get my results" not "Submit."
3. **Helper text** -- Explain *why* this field matters to the job, not what format to use.
4. **Labels** -- Use the user's language, not the system's field names.
5. **Secondary actions** -- Demote anything that isn't the main job path.

### 4. Check for Cognitive Gaps

A cognitive gap is where the user's mental context shifts without warning. Common gaps:

| Gap | Symptom | Fix |
|-----|---------|-----|
| **Context switch** | Pricing summary → blank form | Add a header framing the next step |
| **Missing "why"** | Field with no helper text | Add helper explaining why this matters to the job |
| **Equal-weight CTAs** | Two buttons, unclear priority | Demote the secondary path visually |
| **Legal dump** | Dense terms at the bottom | Simplify and move up, or progressive disclosure |

## Instructions

### When writing new copy:

1. **State the job** in one sentence.
2. **Write the header first.** It frames everything below.
3. **Write the primary CTA.** Name the outcome.
4. **Fill in labels and helpers.** Each one should connect back to the job.
5. **Demote secondary actions.** Text links, not buttons.
6. **Read the flow aloud.** Does it sound like someone helping you get a job done, or a system asking for inputs?

### When reviewing existing copy:

1. **State the job.** If you can't, that's the first problem.
2. **Build a table.** List every UI element with its current copy.
3. **Flag system-framed copy.** Anything that describes the feature instead of the job.
4. **Propose rewrites.** Show before/after for each element.
5. **Highlight cognitive gaps.** Where does the user lose the thread?

Output format for reviews:

```
Job: "[user's job statement]"

| Element | Current | Proposed | Why |
|---------|---------|----------|-----|
| Header | (none) | "Send this to your client" | Frames the job |
| Field | "Custom message" | "Personal note" | User's language |
| Helper | (none) | "Builds trust and shows this comes from you" | Connects to job |
| CTA | "Submit" | "Send to client" | Names the outcome |
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Job is too vague ("use the product") | Narrow to the specific flow: "get my client set up" |
| Rewrite is longer than original | JTBD copy should be *clearer*, not wordier. Cut ruthlessly. |
| Helper text explains the field format | Explain why the field matters to the job instead |
| Every CTA is outcome-framed | Some actions are just actions. "Cancel" is fine as "Cancel." |
| Forgot to demote secondary paths | If there are two equal buttons, one is lying about its importance |
