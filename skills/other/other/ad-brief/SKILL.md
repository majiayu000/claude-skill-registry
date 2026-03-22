---
name: ad-brief
description: >
    Builds an ad brief for any platform. Researches the user's product, audience, market,
    and KPIs proactively, then asks the user to confirm and fill gaps. Saves the result
    as .agents/ad-brief.md for future sessions. Not for writing ad copy, choosing platforms,
    configuring campaigns, or analyzing results.
---

# Ad Brief

This process is the same regardless of ad platform. Run it before any campaign work.

## How to interact

- **Use `AskUserQuestion` / `ask_user_question`** when asking about experience level, goals, or decisions. Present 2-4 selectable options - avoid making them type long answers. For questions where multiple answers are valid (e.g. target audiences, customer types), allow selecting multiple or typing a custom answer. Never force picking one when the user may have several.
- **Exception: financial and numerical inputs** (budget, CPA, LTV, revenue) must be open-ended — never pre-select dollar amounts. Pre-selected options anchor the user on arbitrary values. Ask them to type their number, then validate it against the formulas in the template.
- **Ask for reference materials early.** Ask if the user has existing documents you should read: brand guidelines, ICP/persona descriptions, competitor lists, landing page URLs, or previous ad performance data. If they provide files, read them and incorporate into your recommendations.

## Check for existing brief

**First, check if `.agents/ad-brief.md` exists** in the user's project. If it does, read it and skip this process.

If not, build one using the template at `template.md`. Two phases:

## Phase 1: Research (you do the work)

1. Ask the user for their product name and URL (or detect from the project: package.json, README, etc.)
2. Research proactively: visit their website, infer the audience, look up competitors, figure out the offer
3. Fill in as much of the brief as you can from what you found

## Phase 2: Confirm and complete (user fills gaps)

1. Present your filled brief to the user: "Here's what I found. Correct anything that's wrong and fill in what's missing."
2. For any remaining gaps, ask **one at a time** using `AskUserQuestion` / `ask_user_question`
3. Save the result as `.agents/ad-brief.md` in the user's project root. This persists for future sessions.
