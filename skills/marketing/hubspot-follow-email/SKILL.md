---
name: hubspot-follow-email
description: >-
  DRAFT. Use when drafting HubSpot marketing or follow-up emails for GTM events,
  nurture, or post-event sequences. Templates + structure + anti-slop rules.
  Not installed by deepline skills.
---

# HubSpot follow / marketing email (DRAFT)

## When to use

- Event invite or reminder in HubSpot Marketing Email
- Post-event follow-up to registrants / no-shows / attendees
- Nurture that references a real system or artifact (not vague AI hype)

## Non-negotiables

- One primary CTA. Secondary link optional, not three competing buttons.
- Personalization tokens must exist in the HubSpot list/properties — do not invent tokens.
- No fabricated metrics, customer logos, or case studies.
- Draft in markdown first; paste into HubSpot only after human edit.
- Prefer creating a **HubSpot draft** (not send) unless explicitly asked to schedule/send.

## Inputs

| Input | Required |
| --- | --- |
| Goal (invite / reminder / post-event / nurture) | yes |
| Audience list or segment definition | yes |
| Offer / CTA URL | yes |
| Brand voice / prior email to match | no |
| Proof points (only if verified) | no |

## Flow

1. **Classify** the email: invite | reminder | day-of | post-attend | post-no-show | nurture.
2. **Pick template** from `templates/` matching the class.
3. **Fill** placeholders; strip unused optional blocks.
4. **Lint** against `references/anti-slop.md`.
5. **Deliver** as HubSpot draft (or markdown in Drive) — do not send unasked.
6. **QA**: subject ≤50 chars preferred; preview text set; mobile-safe short paragraphs; unsubscribe footer present.

## Output

- Subject + preview text
- Body (markdown)
- Suggested HubSpot properties / personalization tokens used
- Send-time suggestion (timezone aware) — suggestion only

## Pair with

- `luma-event-campaign` for invite copy that matches social/DM
- `event-ops-score-and-door` for post-event show/no-show branches
