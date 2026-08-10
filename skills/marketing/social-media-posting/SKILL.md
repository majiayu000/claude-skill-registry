---
name: social-media-posting
description: Create, adapt, and schedule social media content across platforms with platform-specific formatting, engagement hooks, and strategic posting cadence. Use when the user requests social media posting or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Social Media Posting

This skill enables an AI agent to create and manage social media content across major platforms — Twitter/X, LinkedIn, Instagram, and Facebook. The agent adapts messaging to each platform's unique format constraints, audience expectations, and algorithmic preferences. It handles copy writing, hashtag strategy, scheduling, and content calendar creation to maintain a consistent and engaging social media presence.

## Workflow

1. **Define the campaign objective and audience.** Clarify the goal for the social content: brand awareness, engagement, lead generation, event promotion, or product launch. Identify the target audience segment and which platforms they are most active on. A B2B product launch prioritizes LinkedIn and Twitter/X, while a D2C brand focuses on Instagram and Facebook.

2. **Draft platform-adapted copy.** Write distinct versions of each message tailored to platform constraints and norms. Twitter/X posts use concise hooks within 280 characters with 1–3 hashtags. LinkedIn posts can run 1,300+ characters with paragraph breaks, professional tone, and no more than 3–5 hashtags. Instagram captions support up to 2,200 characters and rely heavily on hashtags (up to 30) and emoji for discoverability. Facebook posts perform best at 40–80 words with a direct question or call-to-action.

3. **Craft engagement hooks and CTAs.** Open every post with an attention-grabbing first line — a surprising statistic, a bold claim, or a direct question. The first line is the only part visible before "see more" on most platforms. End with a clear call-to-action: comment, share, click link, or tag someone. Use line breaks and whitespace to improve readability on mobile.

4. **Build a hashtag and mention strategy.** Research trending and niche hashtags relevant to the content topic. On Twitter/X, use 1–3 targeted hashtags inline. On LinkedIn, place 3–5 hashtags at the end of the post. On Instagram, use a mix of high-volume (>500K posts), medium (50K–500K), and niche (<50K) hashtags for maximum reach. Tag relevant accounts, partners, or influencers to extend organic visibility.

5. **Schedule posts at optimal times.** Use platform engagement data to determine the best posting windows. General benchmarks: Twitter/X peaks at 8–10 AM and 12–1 PM weekdays; LinkedIn performs best Tuesday–Thursday 7–9 AM; Instagram engagement peaks Wednesday and Friday 11 AM–1 PM; Facebook sees highest reach Tuesday–Friday 9 AM–12 PM. Adjust for the target audience's timezone and test alternative windows quarterly.

6. **Create a weekly content calendar.** Plan 5–7 days of posts in advance, balancing content types: educational (40%), engaging/entertaining (30%), promotional (20%), and community/UGC (10%). Assign each post a platform, publish time, copy, media asset requirements, and campaign tag for tracking.

## Usage

Provide the agent with the campaign goal, key message, target platforms, and any brand voice guidelines. The agent returns platform-specific post copy, hashtags, scheduling recommendations, and a weekly calendar.

**Prompt:** `Create a social media campaign for the launch of our new AI writing assistant. Target platforms: Twitter/X, LinkedIn, and Instagram. Launch date: March 15. Tone: professional but approachable.`

## Examples

### Example 1: Multi-Platform Product Launch Campaign

**Request:** Announce the launch of "FocusFlow," a productivity app for remote workers, across Twitter/X, LinkedIn, and Instagram.

**Twitter/X (278 characters):**
```
Remote work is amazing — until your focus disappears by 10 AM.

We built FocusFlow to fix that.

🎯 Smart time blocking
📊 Distraction tracking
⚡ Deep work streaks

Free for the first 1,000 users → focusflow.app

#RemoteWork #Productivity
```

**LinkedIn (642 characters):**
```
After 2 years of remote work, our team noticed a pattern: the hardest part isn't collaboration — it's protecting deep focus time.

So we built FocusFlow.

It's a lightweight productivity app that helps remote workers:
→ Block time for deep work automatically
→ Track and reduce digital distractions
→ Build streaks that reinforce daily focus habits

We're opening it up to the first 1,000 users for free.

If you lead a distributed team or struggle with context switching, I'd love your feedback.

Try it here: focusflow.app

#ProductLaunch #RemoteWork #Productivity #DeepWork #FocusFlow
```

**Instagram Caption (with image post):**
```
Your focus is your superpower. 🎯

Meet FocusFlow — the app that helps remote workers protect their deep work time and eliminate distractions.

✨ What you get:
→ Smart time blocking that adapts to your schedule
→ Real-time distraction tracking
→ Focus streaks to keep you motivated

Link in bio to get early access (free for the first 1,000 users!)

.
.
.
#focusflow #productivitytips #remotework #deepwork #focustime
#workfromhome #timemanagement #productivityhacks #remoteworklife
#startuplife #techlaunches #newapp #wfhlife #digitalwellbeing
```

### Example 2: Weekly Social Media Content Calendar

**Request:** Plan one week of posts for a B2B marketing agency's LinkedIn and Twitter/X accounts.

| Day | Platform | Type | Topic | Post Summary | Time |
|-----|----------|------|-------|-------------|------|
| Mon | LinkedIn | Educational | SEO tip | "3 on-page SEO fixes that take 10 minutes and move the needle" | 8:00 AM ET |
| Mon | Twitter/X | Engagement | Industry poll | "What's the #1 channel driving leads for your B2B in 2025?" (poll) | 12:00 PM ET |
| Tue | LinkedIn | Case study | Client win | "How we helped [client] increase organic traffic 140% in 90 days" | 7:30 AM ET |
| Tue | Twitter/X | Educational | Thread | "5 LinkedIn ad mistakes we see in every audit (thread)" | 9:00 AM ET |
| Wed | LinkedIn | Thought leadership | Industry trend | "AI won't replace marketers. Marketers who use AI will." | 8:00 AM ET |
| Wed | Twitter/X | Engaging | Meme/humor | Relatable marketing meme with commentary | 1:00 PM ET |
| Thu | LinkedIn | Promotional | Service highlight | "Our Q2 content strategy sprint is open for 3 clients" | 7:30 AM ET |
| Thu | Twitter/X | Community | Retweet + comment | Amplify a client's post with added insight | 10:00 AM ET |
| Fri | LinkedIn | Educational | Carousel | "The anatomy of a LinkedIn post that gets 10K impressions" | 8:00 AM ET |
| Fri | Twitter/X | Engagement | Question | "What's one marketing tool you can't live without? I'll go first:" | 11:00 AM ET |

## Best Practices

- **Lead with a hook in the first line.** On every platform, only the first 1–2 lines are visible before truncation. Use a bold statement, number, or question to stop the scroll. Avoid starting with "We're excited to announce" — that's a scroll-past.
- **Adapt tone and format per platform.** LinkedIn rewards professional storytelling and data-driven insights. Twitter/X rewards conciseness and wit. Instagram rewards visual quality and community engagement. Never cross-post identical copy.
- **Post consistently rather than frequently.** Three high-quality posts per week outperform daily low-effort posts. Algorithms reward engagement rate (likes + comments / impressions), not raw volume.
- **Use native content over external links when possible.** Platform algorithms deprioritize posts with outbound links. Post the content natively (text, images, carousels) and add the link in the first comment or as "link in bio" on Instagram.
- **Engage in the first 30 minutes after posting.** Reply to every comment and engage with related content immediately after publishing. Early engagement signals tell the algorithm to distribute the post more widely.
- **Track performance weekly and iterate.** Monitor impressions, engagement rate, link clicks, and follower growth per platform. Double down on content types and topics that outperform benchmarks and retire underperforming formats.

## Edge Cases

- **Character limit overflows.** Twitter/X hard-limits at 280 characters (URLs count as 23 characters regardless of length). If the message is too long, split into a thread with a clear "(1/3)" format and hook the first tweet to encourage thread reads.
- **Platform API rate limits and outages.** When posting programmatically, respect rate limits (Twitter/X: 300 tweets/3 hours, LinkedIn: 100 shares/day). Implement retry logic with exponential backoff and queue failed posts for rescheduling.
- **Regulated industries.** Financial services, healthcare, and legal social posts may require compliance review and disclaimers. Build an approval workflow and pre-approved template library to maintain velocity without compliance risk.
- **Crisis or sensitive news events.** Pause all scheduled promotional posts during major crises or tragedies. Review the queue and hold anything that could appear tone-deaf. Resume with empathetic or neutral content first.
- **Hashtag hijacking or misuse.** Monitor trending hashtags before using them. A hashtag that appears relevant may have been co-opted for a political or controversial topic. Always check the current conversation around a hashtag before including it.
