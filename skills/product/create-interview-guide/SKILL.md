---
name: create-interview-guide
description: Generate a Mom Test interview guide with warm-up, core, and closing questions when the user asks to prepare for customer interviews, user research, or discovery calls
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[topic or hypothesis to explore]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: hiring, interviews, process
---

# Create Interview Guide

## Overview

Generate a structured customer interview guide based on The Mom Test (Rob Fitzpatrick). Every question is designed to extract truthful signal about past behavior, real pain, and actual workflows — not hypothetical opinions or compliments. The guide includes a "Bad vs Good" column so the interviewer can self-correct in real time, and "What to listen for" cues so they know what signal to capture.

## Workflow

1. **Read product context** — Scan `.chalk/docs/product/` for the product profile (`0_product_profile.md`), existing JTBD canvases, research syntheses, and any prior interview guides. Check `.chalk/docs/product/` for research synthesis docs to avoid re-asking already-answered questions. If no product context exists, work from what the user provides.

2. **Parse the research goal** — Extract from `$ARGUMENTS` the topic, hypothesis, or area of exploration. If the user provides a vague topic (e.g., "onboarding"), ask one round of clarifying questions: Who are we interviewing? What decisions will this research inform? What do we already believe is true?

3. **Identify the interview persona** — Determine who will be interviewed based on product context or user input. Note their likely context, role, and relationship to the problem space. This shapes the warm-up questions and the vocabulary used throughout.

4. **Generate warm-up questions (5 questions)** — These build rapport and establish context. They ask about the person's role, daily workflow, and general environment. No product-related questions yet. Purpose: make the interviewee comfortable and give the interviewer context to ask better follow-up questions.

5. **Generate core questions (8-12 questions)** — These are the heart of the interview. Every question must pass all Mom Test rules:
   - Asks about **past behavior**, not hypothetical futures
   - Asks for **specifics** (last time, specific instance), not generalizations
   - Focuses on **their life and problems**, not your idea or solution
   - Contains **no leading language** that telegraphs the "right" answer
   - Each question includes a "Bad vs Good" comparison and a "What to listen for" note

6. **Generate closing questions (3 questions)** — These capture referrals, uncover what was missed, and establish follow-up permission. Include: "Who else should I talk to?", "What should I have asked that I didn't?", and a permission-to-follow-up question.

7. **Add interviewer briefing notes** — Include a short section on interview conduct: how to handle silence, how to follow up on interesting answers, when to deviate from the script, and how to avoid accidentally pitching.

8. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

9. **Write the file** — Save to `.chalk/docs/product/<n>_interview_guide_<topic_slug>.md`.

10. **Confirm** — Tell the user the guide was created, share the file path, and highlight the 2-3 most critical core questions that will generate the highest-signal answers.

## Interview Guide Structure

```markdown
# Interview Guide: <Topic>

Last updated: <YYYY-MM-DD> (Initial draft)

Target persona: <who we are interviewing and their context>
Research goal: <what decisions this will inform>
Estimated duration: 30-45 minutes

## Mom Test Rules (Quick Reference)

1. Talk about their life, not your idea
2. Ask about specifics in the past, not hypotheticals about the future
3. Talk less, listen more
4. No pitching — if you catch yourself explaining your solution, stop
5. Compliments are noise, not signal — redirect to facts

## Warm-up Questions (5 min)

Purpose: Build rapport, understand their context. Do not mention the product or problem yet.

| # | Question | What to listen for |
|---|----------|--------------------|
| W1 | ... | ... |
| W2 | ... | ... |
| W3 | ... | ... |
| W4 | ... | ... |
| W5 | ... | ... |

## Core Questions (20-30 min)

Purpose: Extract signal about real behavior, pain, and workflows.

| # | Bad Version (Don't Ask) | Good Version (Ask This) | What to Listen For |
|---|-------------------------|-------------------------|--------------------|
| C1 | ... | ... | ... |
| C2 | ... | ... | ... |
| ... | ... | ... | ... |

### Follow-up Prompts

Use these when an interviewee gives an interesting but vague answer:
- "Can you walk me through the last time that happened?"
- "What did you do next?"
- "How much time/money did that cost you?"
- "You mentioned [X] — what made that particularly painful?"
- "What happened after that?"
- "Why did you choose that approach over alternatives?"

## Closing Questions (5 min)

| # | Question | What to listen for |
|---|----------|--------------------|
| CL1 | Who else deals with this problem that I should talk to? | Network mapping — strong signal if they enthusiastically name people |
| CL2 | What should I have asked you that I didn't? | Blind spots in your research framing |
| CL3 | Would it be okay if I followed up with you as we learn more? | Engagement level — eagerness to stay involved signals real pain |

## Interviewer Briefing

### Before the interview
- Review this guide but do not memorize it — conversations should feel natural
- Set up recording (with permission) so you can focus on listening
- Have a note-taking template ready with columns: timestamp, quote, theme

### During the interview
- **Silence is your friend** — count to 5 before filling a pause; they often add the most valuable detail after a pause
- **Follow the energy** — if they light up or get frustrated about a topic, go deeper there even if it is off-script
- **Deflect compliments** — if they say "That sounds great!", respond with "Thanks — but tell me more about how you handle this today"
- **Anchor to specifics** — if they generalize ("usually", "sometimes"), ask "Can you tell me about a specific time?"
- **Never pitch** — if you catch yourself explaining how your product works, stop immediately and ask another question

### After the interview
- Write up notes within 1 hour while memory is fresh
- Highlight 3-5 verbatim quotes that were most surprising or informative
- Tag each quote with a theme for later synthesis
- Note what you expected to hear vs. what you actually heard
```

## Output

- **File**: `.chalk/docs/product/<n>_interview_guide_<topic_slug>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# Interview Guide: <Topic>`
- **Second line**: `Last updated: <YYYY-MM-DD> (Initial draft)`

## Anti-patterns

- **Hypothetical questions ("Would you use X?")** — People are terrible at predicting their future behavior. "Would you pay for this?" gets you polite lies. "How much did you spend last month trying to solve this?" gets you truth. Every question must reference past or current behavior.
- **Leading questions** — "Don't you think it would be better if...?" telegraphs the answer. The interviewee will agree to be polite. Strip all opinion from your questions. Ask "How do you handle X today?" not "Isn't handling X really annoying?"
- **Pitching during research** — The moment you explain your solution, the interview becomes a sales call. The interviewee switches from telling you their truth to reacting to your idea. If they ask what you are building, say "I'll tell you at the end — right now I want to learn from your experience."
- **Asking about the future** — "How would you want this to work?" generates fantasy, not data. People design solutions based on what they can imagine, not what they actually need. Ask about the last time they struggled instead.
- **Generic questions without specificity** — "Do you have problems with X?" gets a yes/no. "Walk me through the last time you dealt with X" gets a story with details, emotions, and workarounds — the raw material of product insight.
- **Interviewing only friendly users** — Friendly users tell you what you want to hear. Include skeptics, churned users, and people who chose a competitor. The most uncomfortable interviews produce the most valuable signal.
- **Treating the guide as a rigid script** — The guide is a safety net, not a straitjacket. The best interviews follow the interviewee's energy. If they reveal something unexpected in question 3, abandon questions 4-7 and dig into what they just said.
- **No "What to listen for" guidance** — Without this, interviewers miss signal. A question about workflow should note "Listen for workarounds, manual steps, and emotional language — these indicate unmet needs."
