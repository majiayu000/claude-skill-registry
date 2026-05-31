---
name: user-flows-and-guided-paths
description: Related features and tasks — such as purchase flows, onboarding, or multi-step configuration — should be designed as natural, guided paths that feel coherent and fit the product hierarchy. Use wizards for complex sequential tasks. Use when designing flows, onboarding, checkout, setup sequences, or any multi-step user journey.
metadata:
  priority: 7
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "flow"
      - "wizard"
      - "onboarding"
      - "checkout"
      - "steps"
      - "multi-step"
      - "guided"
      - "purchase flow"
      - "setup"
retrieval:
  aliases:
    - user flow
    - wizard pattern
    - onboarding flow
    - checkout flow
    - guided steps
    - multi-step form
  intents:
    - design a purchase flow
    - build an onboarding sequence
    - create a wizard
    - guide the user through complex setup
    - connect related features into a path
  examples:
    - design the checkout flow for this shop
    - build a wizard for project setup
    - make this onboarding feel natural
---

# User Flows and Guided Paths

Related features that belong together should be experienced as a single coherent journey — not as separate screens the user has to navigate between manually. A well-designed flow feels inevitable: each step leads naturally to the next, the user always knows where they are and what comes next, and the path fits the product's information hierarchy.

## When to Guide vs. When to Let Users Explore

| Scenario | Pattern |
|---|---|
| Linear process with a clear end goal (checkout, signup, setup) | Guided step-by-step flow or wizard |
| Complex task that benefits from breaking into stages | Wizard with progress indicator |
| Feature discovery across an existing product | Contextual tooltips or coach marks |
| User returning to complete something they started | Resume prompt with clear re-entry point |
| Open-ended exploration (dashboard, settings) | Free navigation — do not force a flow |

Only guide when the task genuinely has a natural order. Forcing a wizard onto a non-sequential task frustrates users who already know what they want.

## The Wizard Pattern

Use a wizard when:
- The task has 3 or more sequential steps
- Later steps depend on decisions made in earlier steps
- Doing all steps on one screen would overwhelm the user

### Wizard anatomy

```
[Step indicator: 1 of 4]

Step title

  [Form content for this step]

[Back]  [Continue →]
```

**Step indicator:** Always show the user where they are in the sequence and how many steps remain. A progress bar or numbered steps both work — numbered steps are clearer when step names are meaningful.

**Back navigation:** Always available. Users must be able to go back and change earlier decisions without losing their progress on later steps.

**Forward navigation:** Disabled until the current step is complete. Validate on Continue, not on Submit at the end.

**Exit path:** Make it clear how to abandon the flow without losing partial progress. Autosave drafts where possible.

### Step design principles
- One primary decision or input group per step — don't overfill steps
- Step titles should describe the user's goal, not the system's: "Your delivery address" not "Address input"
- Optional steps should be clearly marked and skippable
- The final step should show a summary before committing

## Purchase and Conversion Flows

Purchase flows have an additional constraint: every unnecessary step reduces conversion. Design for the shortest path to completion.

- Collect only what is required at each stage — defer optional information
- Show a persistent order summary so the user always sees what they are buying
- Surface trust signals near payment steps (security badges, return policy)
- Confirmation step before payment: show total, delivery, items — one last review
- Post-purchase: immediate confirmation with clear next steps ("Your order is confirmed. We'll email you when it ships.")

## Fitting Flows into the Product Hierarchy

A guided path should feel like it belongs to the product — not like it has opened a separate experience.

- The visual style, typography, and components inside a flow should match the rest of the product
- Navigation chrome (sidebar, top nav) can be hidden during a flow to reduce distraction, but the brand header should remain visible
- After completing a flow, return the user to a meaningful place in the hierarchy — not to a generic home screen
- Deep-linking into a flow should work: a user who arrives at step 3 via email link should see step 3, not step 1

## Review Checklist

- [ ] Does the flow have a clear start, a logical step order, and a definite end?
- [ ] Is a progress indicator visible at every step?
- [ ] Can the user go back to any previous step without losing later progress?
- [ ] Is each step focused on one decision or input group?
- [ ] Are step titles written in user language, describing their goal?
- [ ] Does the final step show a summary before the irreversible action?
- [ ] After completion, does the user land somewhere meaningful in the product?
- [ ] Does the flow visual style match the rest of the product?
