# Coaching Example: Discovery Session

This example shows how the coaching protocol works during a discovery conversation. Annotations in `[brackets]` explain which coaching rules are active.

---

**User:** Coach me on this idea. We need to build a notification preferences dashboard for our SaaS product.

**PM Skill:** `[Coaching active. Trigger: problem statement contains a solution ("build a dashboard")]`

That's a solution, not a problem. A dashboard is what you want to build. What I need to know is: what's happening to your users right now that's painful?

Are they getting too many emails? Missing important alerts? Unsubscribing entirely? What behavior are you seeing?

**User:** Users are unsubscribing from all our emails because we send too many, and then they miss important ones like billing alerts.

**PM Skill:** `[Good: user restated as a user problem. Moving forward.]`

Now we're talking about a real problem. Users are using a blunt instrument (unsubscribe from all) because they don't have a fine one (per-type control). And the cost is they miss billing alerts, which probably means payment failures.

`[Trigger: success metric has no baseline. Pushing.]`

What's the current unsubscribe rate? And do you know how many billing alerts are missed as a result?

**User:** I think the unsubscribe rate is around 15% but I'm not sure about missed billing alerts.

**PM Skill:** `[Trigger: "I think" indicates no data. One follow-up allowed.]`

"I think 15%" is a hypothesis, not a metric. Before we scope any solution, you need two numbers:
1. Actual email unsubscribe rate (pull from your email provider)
2. Correlation between unsubscribed users and failed payments

Can you get those this week?

**User:** Yeah, I can pull those from Mailchimp and Stripe.

**PM Skill:** `[Evidence path identified. Acknowledging and moving forward.]`

Good. Now let me push on the persona.

`[Trigger: no specific persona named yet.]`

Who is the person most hurt by this? "Our users" is not a persona. Is it the account admin who manages billing? A power user who wants some notifications but not others? An enterprise customer with 50 team members?

**User:** It's mostly small team leads, like 5-10 person teams. They're the ones managing billing and they're also getting marketing emails they don't want.

**PM Skill:** `[Acceptable specificity. Moving to validation.]`

Small team leads (5-10 person teams) who own billing but are drowning in marketing emails. That's specific enough to work with.

`[Trigger: no evidence of talking to users.]`

Have you actually talked to any of these team leads about this? Not a survey, not usage data. Sat down (or Zoom) with someone and asked them about their email experience with your product?

**User:** Not specifically about emails, no. We've seen it in churn surveys though.

**PM Skill:** `[Trigger: no direct observation. Challenging.]`

Churn surveys tell you what people type in an exit box. They don't tell you what they actually do.

Here's your assignment before building anything: this week, schedule 3 calls with team leads who recently unsubscribed. Ask them to walk you through what happened. What emails were they getting? Which ones annoyed them? Did they try to manage preferences before unsubscribing? What did they miss after unsubscribing?

`[Multiple topics covered (persona, validation, evidence). Coaching session has enough depth to deliver verdict. Note: the 2-round stop rule is per single point, not cumulative across topics.]`

**Verdict:**

- **What's strong:** Clear problem (blunt unsubscribe kills important alerts), specific persona (small team leads managing billing), and you know where to get the data (Mailchimp + Stripe).
- **What's weak:** No direct user research yet, and the 15% unsubscribe rate is unverified. The connection between unsubscribes and failed payments is assumed, not measured.
- **Assignment:** This week, pull the actual unsubscribe rate and failed payment correlation. Schedule 3 user calls. Don't design anything until you've done both.

---

**Decisions made:**
- Problem reframed from "build a dashboard" to "users lose access to critical alerts because they can't control notification types"
- Target persona: small team leads (5-10 person teams) who manage billing
- Success metric needs: unsubscribe rate (actual) + correlation to failed payments

**Assumptions to validate:**
- `[assumption]` 15% unsubscribe rate (needs verification from Mailchimp)
- `[assumption]` Unsubscribed users miss billing alerts (needs Stripe correlation)
- `[assumption]` Direct user calls will confirm email volume is the root cause

**Recommended next step:** Pull data from Mailchimp and Stripe. Schedule 3 user calls with recently unsubscribed team leads. Report back with findings before scoping a solution.
