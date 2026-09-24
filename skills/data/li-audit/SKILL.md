---
name: li-audit
description: >-
  Post-mortem on what the user has already published - which posts actually
  worked, why, and what to stop doing. Use when the user pastes their LinkedIn
  analytics or past posts and asks "what's working", "why did this flop", "read
  my analytics", "audit my content", or wants to know what to double down on.
---

# li-audit

The only honest source of what works for an account is that account. Every
rule in every LinkedIn guide, including the ones in this pack, is a prior. The
user's own last 30 posts are the evidence.

## Input

Ask for whichever the user has:

- The post analytics export (LinkedIn: Analytics -> Content -> Export). CSV.
- Or a screenshot per post with impressions, reactions, comments, reposts.
- Or just the posts and their reaction counts, which is enough for a first
  pass.

Also read `~/.claude/linkedin/log.md` if it exists, since it records which
hook formula each post used.

## What to actually measure

Raw impressions are the least useful number on the page, because they are
mostly a function of how many people already follow the user. Compute these
instead, and show the working:

| metric | how | what it tells you |
| --- | --- | --- |
| **Engagement rate** | (reactions + comments + reposts) / impressions | whether the post earned its reach |
| **Comment ratio** | comments / reactions | whether it started something or just got a nod |
| **Reach multiple** | impressions / follower count | whether it travelled past the existing audience |
| **Save/send rate** | if available | the strongest single predictor of future reach |

Rank by engagement rate and reach multiple, not impressions. A post with 900
impressions and 40 comments beat the one with 12,000 impressions and 6.

## Then find the pattern

With the top 5 and bottom 5 side by side, look for what actually separates
them, and be willing to conclude something the user will not like:

- Hook formula. Which numbers from `hooks.json` are in the top 5?
- Format. Text, document, image, video.
- Length.
- Theme.
- Day and time - check this **last**, and only if the other four show nothing.
  It is almost never the cause, and it is where people want it to be.
- First-hour comments. Posts the user replied to inside an hour versus not.

State the finding as a claim with the evidence attached, and say how confident
it is. With 30 posts you can see a pattern; with 6 you cannot, and you should
say that instead of inventing one.

## Output

```
AUDIT  ·  31 posts  ·  Jun 12 - Sep 5

TOP 5 BY ENGAGEMENT RATE
  8.1%  #3  Mistake      "$18,000 is what no contract cost me"      1,940 imp
  6.4%  #20 Walk-Away    "I fired my highest-paying client"         2,210 imp
  ...

BOTTOM 5
  0.4%  #5  List         "7 tools every founder needs"             11,400 imp
  ...

WHAT THE DATA SAYS
1. Posts where you were the one who looked bad: mean 6.2% vs 1.1% for
   everything else. n=6. This is your strongest signal and it is not close.
2. Tool listicles get impressions and nothing else. High reach, no comments,
   no leads. Three of your bottom five.
3. Day of week shows nothing. Your Tuesday mean and your Friday mean are
   inside the noise. Stop optimising it.

STOP: listicles about tools.
DO MORE: the ones with a cost you paid, and a number.
```

Then hand the conclusions to `/li-plan` so next week's plan is built on the
user's own evidence rather than on defaults.
