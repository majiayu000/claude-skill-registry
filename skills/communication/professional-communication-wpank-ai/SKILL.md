---
name: professional-communication
model: standard
description: Write effective professional messages for software teams. Use when drafting emails, Slack/Teams messages, meeting agendas, status updates, or translating technical concepts for non-technical audiences. Triggers on email, slack, teams, message, meeting agenda, status update, stakeholder communication, escalation, jargon translation.
---

# Professional Communication

Write clear, effective professional messages that get read and acted upon.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install professional-communication
```


## WHAT This Skill Does

Routes you to ready-to-use templates and translation guides for professional technical communication.

## WHEN To Use

- Drafting emails (status updates, requests, escalations, introductions)
- Writing Slack/Teams messages
- Preparing meeting agendas or summaries
- Translating technical concepts for non-technical audiences
- Any written communication to teammates, managers, or stakeholders

## Core Principle

**Key message first. Scannable format. Clear action requested.**

Every professional message answers: What do you need to know? Why does it matter? What action (if any) is needed?

## Quick Reference: Message Structure

```
Subject: [Topic]: [Specific Purpose]

[1-2 sentences: key point or request upfront]

**Context:** (if needed)
- Bullet points, not paragraphs

**Action Needed:**
- Specific request with timeline
```

## Route to References

| Task | Load This Reference |
|------|---------------------|
| Writing any email | **MANDATORY**: Load [`references/email-templates.md`](references/email-templates.md) |
| Explaining technical concepts to non-technical people | **MANDATORY**: Load [`references/jargon-simplification.md`](references/jargon-simplification.md) |
| Running or preparing for meetings | **MANDATORY**: Load [`references/meeting-structures.md`](references/meeting-structures.md) |
| Async/remote team communication | Load [`references/remote-async-communication.md`](references/remote-async-communication.md) |

## The Four Rules

1. **Subject lines tell the story** - "Project X: Decision Needed by Friday" beats "Question"
2. **Bullets over paragraphs** - Nobody reads walls of text
3. **Specific asks** - "Please review by Thursday" beats "Let me know"
4. **Match the channel** - Chat for quick/informal, Email for records/formal

## NEVER

- Send a message without a clear purpose in the first sentence
- Use "Just checking in" without context (include what you're checking on)
- Write paragraphs when bullets would work
- Bury the ask at the bottom
- Use jargon with non-technical audiences
- Send walls of text in chat (use threads)
- Reply-all unnecessarily
- Use passive voice when active is clearer ("We decided" not "It was decided")
