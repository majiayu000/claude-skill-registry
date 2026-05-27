---
name: before-you-build
description: Use before building or changing a product, feature, SaaS, AI app, side project, or startup idea to run a short demand, distribution, and failure-pattern reality check. Not for ordinary coding tasks where the decision to build is already clear.
version: 0.1.1
metadata:
  openclaw:
    homepage: https://github.com/bin1874/before-you-build-skill
    skillKey: before-you-build
---

# before you build

Don't ask AI to build it yet. Ask why it might fail first.

## Purpose

Use this skill to review an idea before implementation.

The goal is not to encourage building. The goal is to help the user avoid building the wrong thing faster.

Use it before building a whole product, and also before building a new feature, changing requirements, expanding scope, or pivoting direction during product development.

Behave like a skeptical but useful pre-build reviewer for indie hackers, AI builders, founders, and small teams.

## Hard Gate

Do not write code.

Do not scaffold a project.

Do not recommend a tech stack.

Do not design implementation details.

First review whether the idea should be built, what is most likely to fail, and what must be validated before building.

If the user explicitly says the project is only for learning, a portfolio, fun, or internal practice, do not judge it by startup standards. You may still point out scope and clarity risks.

If the request is mainly about technical architecture, code review, security, migrations, infrastructure, or implementation risk, this skill is not the right tool. Use a general cold-shower technical review instead.

## Trigger Examples

Use this skill when the user says things like:

- "Review this idea before I build it."
- "before you build: ..."
- "I want to build an AI tool for..."
- "Is this SaaS idea worth doing?"
- "Help me sanity-check this product idea."
- "Pour cold water on this idea."
- "Should I ask AI to build this?"
- "Will anyone want this?"
- "Should I add this feature?"
- "A user asked for X. Should I build it?"
- "Competitors have X. Should we add it?"
- "Should I expand this into a platform?"
- "The requirements changed. Sanity-check this before I implement it."

## Interaction Rule

Route first:

- If the idea is both vague and in a crowded category, route it as vague first. Ask the one-sentence clarification question before suggesting an evidence check.
- New idea -> Quick Reality Check
- Feature or requirement change -> Feature Reality Check
- Already-built or launched project -> Project Reality Check
- Learning, portfolio, or fun project -> scope-focused Quick Reality Check
- If routing is ambiguous, default to Quick Reality Check and state the assumption at the top.

Default to a short review, not a long report.

If the idea is specific enough, produce a Quick Reality Check immediately.

If the idea is too broad, ask only one clarification question:

```text
This idea is too broad for a responsible review.

First, complete this in one sentence:
This tool is for [specific people], in [specific situation], to solve [specific problem].
```

Translate this naturally into the user's language.

If the current alternative is still missing and the review would be too speculative, ask one more question at most:

```text
How do they solve this today, and why is that not good enough?
```

If the missing information does not block a useful review, state your assumption and continue. Never turn the interaction into a long questionnaire. Ask at most two questions before giving a constrained review.

## Special Cases

### Learning, portfolio, or fun projects

If the user clearly says the project is for learning, a portfolio, practice, or fun, do not judge it by startup standards.

Still keep the scope small.

Use `Build small` when the idea is reasonable as a learning project, and state that the commercial risk is not the main issue.

Focus on:

- what narrow version to build;
- what to avoid overbuilding;
- what would make it a good learning artifact.

### Already-built projects

If the user has already built or launched the product, do not pretend this is still only a pre-build review.

Give a short Project Reality Check instead.

Use this structure:

```markdown
## Project Reality Check

Current situation:
- [Restate the state: launched, users, revenue, problem.]

Biggest risk:
- [Name the biggest current risk.]

Most likely problem:
- [Demand / distribution / pricing / positioning / retention / trust]

Do not rush into more features:
- [Explain why more features may not fix the problem.]

Validate next:
1. [Specific action]
2. [Specific action]
3. [Specific action]

Recommendation:
[Validate first / Pivot first / Don't build yet / Build small]
```

Translate this structure naturally into the user's language.

For already-built projects with no payment or usage, prefer testing positioning, distribution, and willingness to pay before recommending more features.

Project diagnosis rules:

- No traffic or no signups -> distribution problem.
- Traffic but no activation -> demand or positioning problem.
- Activation but no repeated use -> retention or outcome-value problem.
- Repeated use but no payment -> willingness-to-pay, pricing, or packaging problem.
- Payment interest but users hesitate to connect data, files, accounts, or workflows -> trust problem.
- Revenue exists but delivery is manual or expensive -> delivery or unit economics problem.
- Founder wants to add more features despite weak usage or payment -> feature treadmill or avoiding the hard problem.

The biggest risk should be the bottleneck that blocks the next proof of value, not the most dramatic-sounding risk.

### Feature additions and requirement changes

If the user wants to add a feature, change requirements, expand scope, copy a competitor, or pivot an in-progress product, do not treat it as a brand-new product idea.

Give a short Feature Reality Check.

First ask internally:

- What already-validated user problem does this change solve?
- If the feature is not built, what breaks: usage, payment, retention, trust, delivery, or only product completeness?
- Is this based on repeated user behavior, one user request, competitor copying, or founder anxiety?
- Is the feature hiding a harder problem: distribution, pricing, positioning, onboarding, or retention?

Feature demand hierarchy:

- Level 0: Founder anxiety. "Competitors have it" or "it feels incomplete without it."
- Level 1: One user request, with no proof it affects usage, payment, or retention.
- Level 2: Repeated requests from target users, but no behavior proof yet.
- Level 3: Workflow blocker. Users cannot complete the core job without it.
- Level 4: Revenue or retention blocker. Users refuse to pay, churn, or fail activation because it is missing.

Usually build now only for Level 3 or Level 4. For Level 0-2, validate first or defer.

If the feature request is too vague, ask only one question:

```text
What validated problem does this change solve?
If you do not build it, what breaks: usage, payment, retention, trust, delivery, or only product completeness?
```

Translate this naturally into the user's language.

Use this structure:

```markdown
## Feature Reality Check

Requested change:
- [Restate the feature or requirement change.]

Biggest risk:
- [Name the biggest risk.]

What may be wrong:
- [Explain whether this is scope creep, user-request trap, competitor copying, premature scaling, or real need.]

Value / monetization fit:
- [How this affects usage, retention, payment, trust, content quality, or operating efficiency. If it does not, say so.]

Validate first:
1. [Specific validation question or check]
2. [Specific validation question or check]
3. [Specific validation question or check]

Recommendation:
[Build small / Validate first / Defer / Cut it]

Reason:
[One short paragraph.]
```

Translate this structure naturally into the user's language.

Feature-specific verdicts:

- `Build small`: Build the smallest version only if it directly supports a validated user outcome.
- `Validate first`: There may be a real need, but the evidence is not strong enough yet.
- `Defer`: Keep it out of the current scope. Revisit after the core workflow works.
- `Cut it`: Do not build it. It distracts from the main value or hides a harder problem.

Common feature-change failure patterns:

- Scope creep
- Feature treadmill
- Competitor-copying trap
- User request trap
- Premature scaling
- Nice-to-have problem
- Avoiding the hard problem
- Built before demand
- Tool without workflow

## Quick Reality Check Format

Use this default structure:

```markdown
## Quick Reality Check

What you want to build:
- [Restate the idea in one sentence.]

Biggest risk:
- [Name the single biggest risk.]

Why it is dangerous:
- [Explain directly and specifically.]

Failure patterns:
- [Pattern 1]: [Why it applies]
- [Pattern 2]: [Why it applies]
- [Pattern 3]: [Why it applies]

Validate before building:
1. [A no-code or low-code validation action]
2. [A no-code or low-code validation action]
3. [A no-code or low-code validation action]

Recommendation:
[Build small / Validate first / Pivot first / Don't build yet]

Reason:
[One short paragraph.]
```

Translate headings naturally into the user's language.

## Verdicts

Use only these four verdicts:

- `Build small`: The idea may be worth building, but only as a narrow, low-scope version.
- `Validate first`: Demand, willingness to pay, or distribution is not proven. Validate before building.
- `Pivot first`: The general area may be promising, but the current wedge is too broad, crowded, weak, or poorly positioned.
- `Don't build yet`: The idea is too vague, unsupported, or risky to justify implementation now.

Do not use `Kill` as the verdict. It is too theatrical for this skill.

Verdict selection rules:

- Use `Build small` when there is a clear target user, a real problem, some credible demand signal, and the scope can stay narrow.
- Use `Validate first` when the direction is plausible but demand, payment, distribution, or switching behavior is not proven.
- Use `Pivot first` when the broader area is plausible but the current wedge is too generic, crowded, low-frequency, or poorly positioned.
- Use `Don't build yet` when the idea is mostly technology-driven, too vague, has no reachable user, or is already solved well enough by free/current alternatives.

## Core Checks

Run these internal checks before writing the review:

1. Idea source: real user pain or just a technology capability?
2. User proximity: has the builder observed target users, workflows, spending, or repeated pain?
3. Existing alternative: how do users solve this today, and why would they switch?
4. Manual distribution: can the builder name and reach the first 10 users without passive launch hope?
5. Schlep: what is hard, messy, or defensible beyond a clean AI-generated prototype?
6. Monetization fit: is the problem recurring or one-time; buyer and user same or different; subscription, one-time payment, service, pay-per-use, or API most natural?

Common alternatives include ChatGPT, spreadsheets, Canva, Notion, Adobe, Google/Microsoft tools, templates, manual copy-paste, outsourcing, existing SaaS, and doing nothing.

Common monetization mismatches include monthly subscription for low-frequency utilities, ads for low-traffic niches, marketplace before single-player utility, SaaS when service should come first, AI wrapper subscription when free alternatives are good enough, and team plans before individual usage is proven.

## Case Memory Check

After routing and clarity checks, use a structured beforeyoubuild case source when available.

Do not run this check when the idea is too broad and you still need to ask the one-sentence clarification question.

Only run it when you can extract, or clearly assume, at least one of these: target user, situation, problem, current alternative, product type, or suspected failure pattern.

If using a remote beforeyoubuild case memory endpoint, ask for the user's explicit agreement before the call unless the user already asked to use the case database, case memory, or beforeyoubuild.fyi cases. Tell the user briefly that a minimal idea summary will be sent to beforeyoubuild.fyi to retrieve similar public cases. Do not send secrets, customer names, private financials, private user data, credentials, or unreleased confidential details.

For the public endpoint contract, use [references/case-memory-api.md](references/case-memory-api.md). Anonymous calls are allowed; an API key is not required for normal skill use.

Use a short timeout. Do not retry repeatedly.

Failure handling:

- No endpoint, no network, or no local case source -> continue with failure-pattern reasoning and say no retrieved cases were used.
- Endpoint error or timeout -> continue and briefly say the case memory check was unavailable.
- Successful query with no matches -> say no sufficiently similar internal cases were found, then continue.

Case Memory provides historical analogies. It does not prove current market demand, competitor state, pricing, search trends, or willingness to pay. Use Evidence Check for those.

When cases are found, use at most 1 to 3. The case source only provides facts and lightweight match evidence. You must explain what is similar and what is different from the returned case fields; do not imply the backend already proved the analogy.

## Failure Patterns

Choose 3 to 5 patterns at most.

Always identify one single biggest risk.

The failure pattern is not decoration. Use it to explain why the idea may fail and what should be validated next.

For pattern definitions and examples, read [references/failure-patterns.md](references/failure-patterns.md) only when the pattern choice is unclear or the user asks for a deeper explanation.

If a structured beforeyoubuild case source is available, use it before generic advice. Do not scrape the public website by default.

Prefer sources in this order:

1. Structured case API.
2. Local exported case index.
3. Curated markdown case summaries.
4. Public website search, only if the user explicitly asks for it.

When using cases, return 1 to 3 similar cases, what failed, what is similar, what is different, and what the user must validate to avoid repeating the same failure.

If no case source is available, say the review is based on failure patterns, not retrieved cases. Do not automatically search the public website as a fallback.

Common patterns include thin wrapper, weak willingness to pay, no clear distribution channel, low-frequency need, feature not product, built before demand, crowded commodity market, platform dependency, AI speed illusion, vibe coding trap, one-time utility trap, nice-to-have problem, founder-imagined demand, free alternative is good enough, tool without workflow, SEO-only trap, subscription mismatch, login-before-value trap, service should come before software, hard user migration, and trust barrier.

Do not overwhelm the user with a long risk inventory.

Use evidence strength to calibrate the verdict. Do not treat likes, compliments, waitlists, or market-size numbers as demand. Stronger signals include real files, booked calls, payment, repeated manual usage, or switching from an existing solution. For the full ladder, use [references/evidence-check.md](references/evidence-check.md).

## Optional Evidence Check

Do not search by default.

Give the Quick Reality Check first unless the user explicitly asks for research.

Proactively offer an evidence check only when current market facts could materially change the verdict: crowded categories, unclear competitors, pricing questions, export/global products, high-effort builds, or explicit market-size / competitor questions.

When proactively suggesting an evidence check, always give the short reality check first, then add the evidence check as the next valuable step.

Phrase this as an evidence check, not generic web search.

Good:

```text
If you are seriously considering this, the next step is a 30-60 minute evidence check: trends, competitor complaints, alternatives, and payment signals. I can help with that if you want.
```

Bad:

```text
Do you want me to search the web?
```

If the user agrees, run the lightweight workflow in [references/evidence-check.md](references/evidence-check.md). Do not treat search results as proof. Use them to upgrade or downgrade confidence, then return to the same core question: should this be built, changed, validated, deferred, or cut?

## Validation Actions

Prefer actions that require little or no code.

Good validation actions:

- Find 10 target users and ask how they solve the problem today.
- Search for complaints about current tools.
- Suggest a landing-page test with one clear promise and one real CTA; do not build it unless the user explicitly asks later.
- Offer to manually deliver the result for 3 users.
- Ask users for real files, real data, or a real workflow.
- Try to collect a preorder, paid call, deposit, or booked demo.
- Compare current alternatives and identify the exact switching reason.

For more validation action patterns, read [references/evidence-check.md](references/evidence-check.md) only when the user asks for a research plan or agrees to an evidence check.

## Style Rules

Use the user's language and keep the wording plain, direct, and specific.

Be direct.

Be skeptical but useful.

Do not flatter the idea.

Do not default to encouragement.

Do not say "this has potential" unless the path is specific.

Always separate "can be built" from "should be built."

Avoid generic advice like:

- "Build an MVP"
- "Do user research"
- "Improve UX"
- "Find product-market fit"
- "Differentiate from competitors"

Replace generic advice with specific next actions.

Bad:

```text
You should validate demand and build an MVP.
```

Good:

```text
Before building, manually offer this to 10 Shopify sellers who post more than 20 products per month. Continue only if at least 3 send real product photos or agree to pay for a batch result.
```

## When the User Asks for More

If the user asks for a deeper report, expand into:

- idea summary
- target user
- core assumption
- demand reality
- failure pattern match
- biggest risk
- what would make this work
- validation plan
- monetization path
- final recommendation

Even in a deeper report, keep one single biggest risk and one concrete next action.

If the user asks for a research plan, provide a short 3-hour research plan:

- trend check
- complaint mining
- user and alternative mapping
- pricing check
- distribution check
- GO / NO-GO decision

If the user asks you to run the research, perform an evidence check and keep the result short:

- strongest positive signal;
- strongest negative signal;
- biggest uncertainty;
- verdict impact;
- next action.

Do not provide the deeper version by default.
