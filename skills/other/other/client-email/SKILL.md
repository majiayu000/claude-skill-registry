---
name: client-email
description: >-
  Draft client-facing emails for legal services — cover notes for contract
  deliverables, redline summaries, deal status updates, and follow-ups.
  Use when composing or revising outbound emails to clients about legal
  work product. Triggers on "draft reply," "email to client," "cover note,"
  "write back to," or any outbound email accompanying a legal deliverable.
license: MIT
metadata:
  author: open-agreements
  version: "0.1.0"
---

# client-email

Style and formatting rules for drafting client-facing emails that accompany legal work product — contract redlines, new drafts, deal summaries, and follow-ups.

## Security model

- This skill is **guidance only** — it does not send emails, call APIs, or access external systems.
- All output is draft text for the user to review and send manually.
- Do not include credentials, API keys, or passwords in email body text, even if the user asks.

## When to use

Apply these rules when drafting or revising an outbound email from a lawyer or legal services provider to a client. Designed for emails that accompany deliverables (revised contracts, redlines, memos) or communicate legal analysis to non-lawyer business clients.

Do NOT apply to internal emails, emails to opposing counsel, or marketing copy.

## Email structure

The numbered-list structure below is for substantive cover notes with multiple topics. Short emails with a single paragraph of content should be written naturally without numbered items.

```
[Cover line: 1-3 sentences. Bold and name any open decision / action item
so the reader sees it immediately without reading further.
E.g., "the **one open item (indemnity cap)** that needs your input."]

1. **Declarative heading that conveys the takeaway.** Discussion.

**_a. Bold-italic lettered sub-item_**_._ Discussion of sub-point.
**_b. Another sub-item_**_._ Discussion.

2. **Another declarative heading.** Discussion. Not every item needs sub-points.

3. **Third heading.** And so forth.

[Short closing line]

[Name]

__________________

[1] Footnote text with citations and links.
```

## Formatting rules

1. **No markdown headings (###).** They render too large in Outlook and Gmail. Use **bold lead-in text** on numbered items instead.

2. **Lead-ins are declarative statements, not questions.** The reader should get the main point just from scanning the bold text. The heading alone should convey the takeaway.
   - Good: "Limitation of liability capped at 12 months of fees; mutual carve-outs added."
   - Bad: "What did we do about the liability cap?"

3. **Sub-items are lettered and bold-italic.** Format: `**_a. Lead-in_**_._` — bold-italic, lettered a/b/c/d, period outside the formatting. Lettered items are easier for the recipient to reference in a reply ("let's go with option c"). Bold-italic gives more visual weight than italic alone.

4. **Footnotes for legal sourcing.** Use `[1]` markers in body text. Place footnote text at the bottom after a `__________________` separator (not `---`, which renders as a full-width horizontal rule in Outlook that looks like a message separator). Each footnote should include a direct quote from the source, a proper citation, and a clickable link so the client can verify without taking your word for it.

## Tone and voice

5. **Concise.** Prefer one tight paragraph per numbered item over multiple paragraphs. Cut filler.

6. **Professional but direct.** Not stiff. Slightly conversational — "here's," "your call," "happy to" are fine. Avoid legalese in the email body; save technical precision for the document itself.

7. **No title block by default.** Sign off with just your name. Add a title block manually for first-contact situations where the recipient doesn't know you yet.

## Client relationship principles

8. **Surface action items in the cover line.** If there's an open decision or action item, bold it and name it specifically in the opening sentence. The reader shouldn't have to hunt for what they need to do.

9. **Defer on business decisions.** When presenting options that are the client's call (pricing, deal terms, strategy), frame as "a few ways to think about it" rather than directives. Use language like "defer to you" or "happy to [do X] once you decide." The lawyer advises; the client decides.

10. **Service-oriented closings on action items.** Offer to do the work rather than assigning it back. "Am happy to fill in the fields" not "fill in the fields." Signal that you're there to execute, not just advise.

11. **Signal proposals as proposals.** When the deliverable includes something the client hasn't explicitly requested (e.g., a new contract provision, an alternative structure), use language like "pencilled in" or "placeholder" to make clear it's a proposal they can accept, reject, or modify — not a unilateral decision made on their behalf.

12. **Keep procedural detail in footnotes.** Legislative history, amendment timelines, and procedural detail belong in footnotes (if included at all). The body text should give the client the practical conclusion, not the sausage-making. Business clients want to know what it means for them, not how the law got there.

## Example

> **Note:** The following is an entirely fictional example created to
> illustrate the formatting rules above. All names, companies, facts,
> and legal citations are invented. Any resemblance to actual persons,
> entities, or matters is coincidental.

```
Jane,

Attached is the revised supply agreement for Acme Corp along with a
redline against their last draft. Here's a summary of our changes and
the **one open item (liability cap amount)** that needs your input.

1. **Indemnity narrowed to third-party claims only.** Their draft
covered "any claim arising from the products," which was overbroad.
We've pencilled in language limiting the indemnity to claims brought
by third parties — not internal disputes between Acme and Doe
Industries.

2. **Liability cap amount — your call.** Their draft was uncapped.
We've bracketed a placeholder. A few ways to think about it:

**_a. Match the contract value_**_._ Cap at total fees under the
purchase order — typical for deals this size.

**_b. Multiple of annual spend_**_._ If this is a multi-year
relationship, a 1-2x annual spend cap gives more room.

**_c. Uncapped for the indemnity only_**_._ Some suppliers expect
product liability indemnity to remain uncapped even when general
liability is capped. Depends on your risk appetite.

3. **Governing law changed to match your other vendor agreements.**
Their form defaulted to State X. We changed to State Y to keep your
vendor portfolio consistent (e.g., your Apex Inc. and Globe Ltd.
agreements are both State Y).[1]

4. **Fixed a stale cross-reference in Section 8.** The termination
clause referenced "Section 12" — should have been Section 9.
Corrected.

Am happy to fill in the cap amount once you decide, or we can
discuss on a call.

John

__________________

[1] State Y's statute of limitations for contract claims is six years.
See State Y Com. Code § 2-725 ("An action for breach of any contract
for sale must be commenced within [six] years after the cause of action
has accrued."). Full text: https://example.com/state-y-ucc-2-725
```
