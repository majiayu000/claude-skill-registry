---
name: meeting-followup
description: >
  Automate post-meeting follow-up: search Fireflies for a meeting transcript, generate a structured
  summary with key decisions, discussion points, action items, and next steps, then draft a
  professional follow-up email to all attendees via Gmail. Use this skill whenever the user mentions
  processing a meeting, creating meeting notes, sending a meeting recap, drafting a follow-up email
  after a call, summarizing a meeting, or anything related to post-meeting workflows — even if they
  don't use the word "meeting" explicitly (e.g., "recap my call with Acme", "send notes from the
  standup", "what happened in my sync with the design team and send it out").
---

# Meeting Follow-Up

This skill turns a Fireflies meeting transcript into a structured summary and a ready-to-send Gmail
draft addressed to all attendees. The goal is to close the loop on meetings fast — the user should
be able to say "process my meeting with Acme" and get a polished follow-up draft in their inbox
within a couple of minutes.

## Workflow

### Step 1: Find the meeting

The user will reference a meeting by name, topic, or participants. Use the Fireflies search and
transcript tools to locate it:

- `fireflies_search` — search by keyword, title, or participant email
- `fireflies_get_transcripts` — browse recent meetings with filters

If the search returns multiple matches, present the top 2-3 candidates with their titles and dates
and ask the user which one they mean. Don't guess.

### Step 2: Pull the transcript and summary

Once you've identified the right meeting, fetch both:

- `fireflies_get_transcript` — the full conversation with speakers and timestamps
- `fireflies_get_summary` — Fireflies' own summary, action items, keywords, and overview

Use **both** sources. The Fireflies summary is a good starting point but often misses nuance or
context that matters. The raw transcript lets you catch things the auto-summary didn't.

### Step 3: Identify attendees and their emails

You need email addresses for the follow-up draft. Gather them from multiple sources:

1. **Fireflies transcript metadata** — often includes participant emails
2. **Gmail search** — search for the meeting title or calendar invite to find attendee emails
   (e.g., `subject:"Meeting Title"` or search for the calendar event notification)
3. **Ask the user** — if you can't find emails for some attendees, list who you're missing and ask

The sender's own email (use `gmail_get_profile`) should be excluded from the recipient list.

### Step 4: Generate the structured summary

Organize the summary into these sections. Every section should be concise — this is going in an
email, not a report. Use bullet points within sections.

**Key Decisions**
Concrete decisions that were made. If no clear decisions were reached, say so briefly — don't
manufacture decisions that didn't happen.

**Discussion Points**
The main topics covered, with enough context that someone who missed the meeting understands what
was discussed and where things landed. Group related threads together rather than listing them
chronologically.

**Action Items**
Each action item should have:
- What needs to be done (specific and clear)
- Who owns it (use names from the transcript)
- Due date or timeline if one was mentioned

If no owner or date was stated, note that — it's useful for the follow-up to surface unassigned
items so the team can resolve them.

**Next Steps**
Any agreed-upon follow-ups: next meeting date, milestones, check-in points. If nothing was
explicitly agreed, note that too.

### Step 5: Draft the follow-up email

Compose a brief, professional email. The tone should be warm but efficient — teammates should be
able to scan it in 30 seconds and know exactly what happened and what they need to do.

**Subject line:** "Recap: [Meeting Title] — [Date]"

**Email structure:**

```
Hi everyone,

Here's a quick recap from our [meeting name] on [date].

[Structured summary from Step 4, formatted with bold headers and bullet points using HTML]

Let me know if I missed anything or if any of the action items need adjusting.

Best,
[User's name]
```

Use `text/html` content type so the formatting renders properly in email clients. Keep the HTML
clean and simple — bold headers, unordered lists, standard fonts. No fancy styling.

### Step 6: Create the Gmail draft

Use `gmail_create_draft` to create the draft:
- **To:** all attendee emails (comma-separated), excluding the sender
- **Subject:** the recap subject line
- **Body:** the HTML-formatted email
- **Content type:** `text/html`

After creating the draft, tell the user:
- The draft has been created and is ready for review in Gmail
- List who it's addressed to so they can verify the recipient list
- Mention if there were any attendees whose emails you couldn't find

## Important considerations

**Speaker attribution matters.** When summarizing discussion points and especially action items, use
the actual names from the transcript. "Sarah will handle the vendor outreach" is much more useful
than "one participant will handle outreach."

**Don't over-summarize.** If the meeting was 15 minutes and covered two topics, the summary should
be short. If it was an hour covering eight topics, it can be longer. Match the depth to the meeting.

**Handle missing data gracefully.** If the Fireflies transcript is incomplete or the audio quality
was poor (you'll notice gaps or "[inaudible]" markers), mention this to the user so they know the
summary might have gaps.

**Respect the user's time.** The whole point of this skill is speed. Don't ask unnecessary
clarifying questions. If you have the meeting name and can find it, just go. Only ask when you
genuinely need to disambiguate (multiple matches) or are missing critical info (can't find attendee
emails).