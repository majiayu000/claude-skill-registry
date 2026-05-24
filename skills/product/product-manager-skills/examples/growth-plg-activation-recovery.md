# Example: Growth And PLG Activation Recovery

## Scenario

You have signups, trials, and demo requests, but self-serve growth is stalling. You want a diagnosis that separates activation problems from pricing, traffic, and sales noise.

## Prompt

```text
We're a workflow automation SaaS for RevOps teams. Trials grew 40% after a content push, but free-to-paid conversion is flat at 1.8%, only 9% of new users build their first live workflow, and team invites are rare. Diagnose the bottleneck, tell us whether this is a PLG problem or a product problem, and propose a 6-week recovery plan with metrics.
```

## Example Output Excerpt

```text
Diagnosis
- This is not primarily a top-of-funnel problem. More traffic is entering the funnel, but the product is failing to convert intent into first value.
- The bottleneck is activation, not pricing. A 9% "first live workflow" rate means most users never reach the core habit-forming moment.
- You do not yet have a reliable PLG loop. Rare team invites suggest the collaborative expansion path is still aspirational, not real.
- Treat this as a product problem with growth consequences. Do not reprice or widen acquisition until the first-value path is materially stronger.

What "good" activation should mean
- A user connects one data source, launches one workflow, and sees one observable business outcome inside the first session or first day.
- If your activation event does not include a real workflow going live, you are overcounting setup and undercounting value.

6-week recovery plan
1. Fix instrumentation
- Instrument signup -> connection -> draft workflow -> live workflow -> first successful run -> first teammate invite.
- Separate users who start from templates from users who start blank.

2. Remove first-session friction
- Replace blank-canvas onboarding with 3 template-led entry points tied to common RevOps jobs.
- Add a guided "connect source + launch workflow" checklist inside the product, not in email.

3. Create one expansion trigger
- Ask for teammate invite only after the first workflow runs successfully.
- Position the invite around shared visibility or approval, not generic collaboration.

Metrics to watch
- Primary: first live workflow rate from 9% toward 18%+.
- Secondary: median time to first live workflow below 20 minutes.
- Expansion leading indicator: teammate invite rate among activated accounts above 15%.
- Decision metric: activated free-to-paid conversion, not aggregate free-to-paid conversion.

Decision rule
- If activation improves but paid conversion does not, revisit packaging and upgrade trigger design next.
- If activation does not improve, keep effort on product onboarding and job clarity. Do not call this a PLG execution problem yet.
```

## Why This Matters

This example shows the skill making a sharper call than "improve onboarding." It distinguishes PLG symptoms from the underlying product failure, defines activation in outcome terms, and sequences recovery work in the right order.

## Reuse

Reuse this pattern when you need to:

- decide whether a weak self-serve motion is a traffic, pricing, or activation problem
- force activation to be tied to real value instead of setup completion
- build a short recovery plan with decision rules before investing in freemium or paid acquisition
