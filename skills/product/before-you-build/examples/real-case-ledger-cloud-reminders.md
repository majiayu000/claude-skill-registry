# Real Case Example: Ledger Cloud Reminders

Based on the public Before You Build case:
https://beforeyoubuild.fyi/en/cases/ledger-cloud-reminders

This example does not reproduce the full case. It turns the public case into a skill usage scenario.

## Prompt

```text
before you build: I want to build a developer tool that sends reminders for scheduled cloud tasks and infra operations. The problem is clear to me because I keep forgetting them. Should I build it?
```

## Public Case Background

The public Ledger Cloud Reminders case is useful because the pain can be real for the builder. That does not automatically mean a product exists.

For developer and operations tools, the hardest risk is often not implementation. It is adoption: setup friction, trust, existing workflows, and whether the reminder is important enough to install another tool.

## What The Skill Should Notice

- The founder's own pain is a signal, but not enough.
- Developers may already use calendars, issue trackers, monitoring, incident tools, cron dashboards, or chat alerts.
- A reminder tool may be too small as a standalone product unless it sits inside an existing workflow.
- Trust matters because missed reminders can create operational risk.
- The first validation should test installation and repeated use, not just positive feedback.

## Good Output Shape

```markdown
## Quick Reality Check

What you want to build:
- A developer reminder tool for scheduled cloud tasks and infra operations.

Biggest risk:
- The problem may be real but too narrow, too low-frequency, or already handled inside tools developers trust.

Most likely failure patterns:
- Personal pain mistaken for market pull
- Tool without workflow
- Setup friction
- Trust and reliability burden

Validate before building:
1. Find 10 developers or small teams who missed a cloud task in the last 60 days.
2. Ask what system failed: memory, calendar, issue tracker, monitoring, chat alert, or ownership.
3. Offer a manual reminder service in Slack or email for 2 weeks before building a full product.
4. Measure whether users keep using it after the first reminder, not whether they like the idea.

Recommendation:
Validate first
```

## Why This Example Helps

It shows the skill handling a problem that may be personally painful and technically buildable, while still challenging adoption, workflow fit, and trust before implementation.
