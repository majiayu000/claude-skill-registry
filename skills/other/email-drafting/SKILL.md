---
name: email-drafting
description: Draft a professional, audience-aware email or reply with calibrated tone and a clear call to action. Use when the user needs one message, response, follow-up, support note, or meeting request; use sales-email-sequences for a coordinated multi-touch outbound campaign.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Email Drafting

This skill enables an AI agent to compose professional, context-appropriate emails across a variety of scenarios. The agent analyzes the purpose, audience, and tone requirements, then produces a complete email with subject line, body, and call to action. It supports common email types including cold outreach, follow-up sequences, customer support responses, internal status updates, and meeting requests.

## Workflow

1. **Identify the email type and objective.** Determine the category of the email — cold outreach, follow-up, customer support reply, internal update, or meeting request. Each type has different structural expectations. A cold outreach email prioritizes a compelling hook, while a support response leads with empathy and resolution. Clarify the single desired outcome: a scheduled call, an acknowledged resolution, an informed team, etc.

2. **Profile the recipient and calibrate tone.** Gather details about the recipient: name, title, company, relationship history, and any previous interactions. Use this context to select the appropriate tone — formal for executive outreach, conversational for peer updates, empathetic for complaint responses, or urgent when time-sensitive action is required. Apply personalization tokens such as `{{first_name}}`, `{{company}}`, and `{{pain_point}}` when drafting templates.

3. **Compose the subject line.** Write a subject line that is specific, concise (under 60 characters), and action-oriented. Avoid generic phrases like "Quick question" or "Touching base." Instead, reference a concrete benefit or context point, e.g., "Cut your onboarding time by 40% — here's how" or "Follow-up: action items from Thursday's standup."

4. **Draft the email body with clear structure.** Follow a proven structure: opening hook (1-2 sentences establishing relevance), body (2-3 short paragraphs delivering the core message with supporting evidence or context), and closing with a single, unambiguous call to action. Keep paragraphs under 3 sentences. Use bullet points for lists of items or benefits. Avoid walls of text.

5. **Add signature and formatting polish.** Include an appropriate sign-off ("Best regards," for formal, "Thanks," for casual, "Cheers," for friendly) followed by the sender's name, title, and contact info. Review the draft for grammar, spelling, and readability. Ensure the email can be scanned in under 30 seconds.

6. **Review against checklist and deliver.** Verify the email meets these criteria: subject line is compelling, tone matches the audience, the CTA is clear and singular, the email is under 200 words for outreach or under 300 words for detailed responses, and no placeholder tokens remain unresolved. Output the final email in a ready-to-send format.

## Usage

Provide the agent with the email type, recipient details, purpose, key points to include, and desired tone. The agent will return a complete email with subject line, body, and signature.

**Prompt format:**

~~~
Draft a [type] email to [recipient details].
Purpose: [what you want to achieve]
Key points: [information to include]
Tone: [formal / casual / empathetic / urgent]
~~~

## Examples

### Example 1: Cold Outreach Email

**Input:**

~~~
Draft a cold outreach email to Sarah Chen, VP of Engineering at Cloudstream Inc.
Purpose: Introduce our API monitoring platform and book a 15-minute demo.
Key points: Their engineering blog mentions scaling challenges; our tool reduces incident response time by 60%.
Tone: Professional but conversational.
~~~

**Output:**

~~~
Subject: Reducing incident response time at Cloudstream

Hi Sarah,

I read your recent post on scaling Cloudstream's microservices architecture — the challenges you described around observability gaps resonated with several of our customers who faced similar growing pains.

We built Watchdog specifically for engineering teams navigating that transition. Our API monitoring platform provides real-time anomaly detection and automated root-cause analysis. Teams using Watchdog have cut their mean incident response time by 60%, which typically saves 10+ engineering hours per week.

Would you be open to a 15-minute walkthrough? I can show you how Watchdog would map onto Cloudstream's stack. Here's a link to grab a time that works: [calendar link]

Best regards,
Alex Rivera
Account Executive, Watchdog
alex@watchdog.io | (555) 234-5678
~~~

### Example 2: Customer Support Response to a Complaint

**Input:**

~~~
Draft a customer support response to Marcus Webb who is upset about being double-charged for his subscription renewal.
Purpose: Acknowledge the error, confirm the refund, and retain the customer.
Key points: Refund of $49.99 will appear within 3-5 business days; root cause was a billing system migration.
Tone: Empathetic and reassuring.
~~~

**Output:**

~~~
Subject: Your refund for the duplicate charge has been processed

Hi Marcus,

I'm truly sorry about the duplicate charge on your account — I completely understand how frustrating that must be, and I want to assure you that we've already taken care of it.

We've processed a full refund of $49.99 to your original payment method. You should see the credit reflected within 3-5 business days. The duplicate charge was caused by a one-time issue during our billing system migration, and our engineering team has deployed a fix to ensure this doesn't happen again.

Your subscription remains fully active and unaffected. As a thank-you for your patience, I've also applied a 15% discount to your next renewal.

If you have any other questions or concerns, please don't hesitate to reply to this email — I'm happy to help.

Warm regards,
Jamie Torres
Customer Support, BrightSaaS
~~~

## Best Practices

- **One call to action per email.** Multiple CTAs dilute urgency and reduce response rates. Choose the single most important next step and make it unmissable.
- **Front-load the most important information.** Recipients often scan only the first two sentences. Lead with relevance — why should they care right now?
- **Match paragraph length to formality.** Formal emails can tolerate slightly longer paragraphs; casual outreach should use 1-2 sentence paragraphs with generous whitespace.
- **Personalize beyond the name.** Reference a recent achievement, shared connection, or specific pain point. Generic personalization ("I see you work at Acme") feels robotic.
- **Use time-bounded CTAs when appropriate.** "Would Thursday or Friday afternoon work?" outperforms "Let me know when you're free" because it reduces decision friction.
- **Proofread for tone as well as grammar.** Read the email aloud to catch phrases that sound condescending, pushy, or overly casual for the context.

## Edge Cases

- **Unknown recipient name.** When the recipient's name is unavailable, use a role-based greeting ("Hi there" or "Hello, Marketing Team") rather than "To whom it may concern," which reads as impersonal.
- **Emotionally charged complaints.** For angry or frustrated customers, avoid defensive language. Lead with validation ("I understand why that's frustrating") before explaining the resolution. Never blame the customer.
- **Multi-recipient emails.** When addressing a group, ensure the CTA specifies who should take action. Diffusion of responsibility leads to no one responding.
- **Follow-up after no response.** Reference the original email briefly and add new value (a relevant case study, a deadline, or a simplified ask) rather than simply bumping the thread.
- **Legal or compliance-sensitive content.** Flag emails that may involve contracts, NDAs, financial disclosures, or regulatory language for human review before sending.
