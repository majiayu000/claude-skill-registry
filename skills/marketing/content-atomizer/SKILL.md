---
name: content-atomizer
description: |
  Take one piece of long-form content and atomize it into 10-20 platform-specific posts across 8 platforms (Twitter/X, LinkedIn, Instagram, Reddit, TikTok, YouTube, Threads, Bluesky). Turns blog posts, podcasts, videos, and newsletters into native social content for each platform. Use this skill whenever someone has existing content they want to distribute — even if they don't say 'atomize' explicitly. Triggers include: 'repurpose this', 'turn this into posts', 'social content from my blog', 'I wrote an article and want to promote it', 'cross-post this', 'content distribution', 'break this down for social', 'I have a podcast episode', 'turn this video into clips', 'make social posts from this', 'content calendar from this article', or any request to get more mileage from existing content.
category: distribution
tier: must-have
reads:
  - brand/voice-profile.md
  - brand/audience.md
writes:
  - marketing/social/{source-slug}/
depends-on:
  - brand-voice
triggers:
  - repurpose
  - atomize
  - turn this into posts
  - social content from
  - content repurposing
  - break this down
  - social posts from blog
  - distribute this
allowed-tools: []
---

# Content Atomizer

You take one piece of long-form content and extract 10-20 standalone social posts, each native to its target platform. Not lazy copy-paste with different character counts — genuine reformatting that makes each post feel like it was written platform-first.

## On Activation

1. Read `brand/voice-profile.md` — maintain consistent voice across platforms
2. Read `brand/audience.md` — know which platforms matter and how the audience behaves on each
3. Load `references/platform-specs.md` for the quick reference table, then load individual platform files from `references/platforms/` as needed (linkedin.md, twitter.md, instagram.md, tiktok.md, youtube.md, threads.md, bluesky.md, reddit.md)
4. Accept the source content (blog post, newsletter, video transcript, podcast transcript)
5. If no source provided, check `marketing/content/` for recent articles

### Zero Context (No Brand Files)

If brand files don't exist, the skill still works:

- **No voice-profile.md**: Write in a clear, professional default voice. Ask the user for 2-3 adjectives describing their brand tone.
- **No audience.md**: Default to all platforms. Ask which platforms matter most to them.
- The skill always works — brand files enhance, never gate.

---

## Brand Integration

Brand files shape how content gets adapted per platform:

- **voice-profile.md** → Each platform gets the same voice in different registers. Twitter gets punchy voice (short, sharp). LinkedIn gets authoritative voice (complete thoughts, data). Reddit gets authentic voice (conversational, no marketing speak). The voice DNA stays constant; the register shifts.
- **audience.md** → Watering holes from the audience profile determine which platforms to prioritize. If your audience lives on Twitter and Reddit, don't waste time on Instagram carousels.

---

## The Atomization Process

### Step 1: Extract Raw Material

Read the source content and extract:

- **Key insights**: 3-5 original ideas or arguments
- **Quotable lines**: Sentences that stand alone as wisdom
- **Stats/data points**: Any numbers, percentages, results
- **Stories/anecdotes**: Narrative moments that create emotional connection
- **Contrarian takes**: Opinions that challenge conventional wisdom
- **Step-by-step processes**: Any how-to sequences
- **Lists**: Any grouped items (tools, tips, mistakes, etc.)

Tag each extraction with its type. This is your raw material inventory.

### Step 2: Map to Platforms

Each extraction type maps naturally to specific platforms and formats:

| Extraction Type | Twitter/X | LinkedIn | Instagram | Reddit | TikTok | YouTube | Threads | Bluesky |
|----------------|-----------|----------|-----------|--------|--------|---------|---------|---------|
| Key insight | Single tweet | Text post | Carousel slide | Comment/post | Hot take (15s) | Short (30s) | Single post | Single post |
| Quotable line | Quote tweet | Text post with context | Quote graphic caption | — | Green screen | — | Quote-post | Thoughtful take |
| Stats/data | Data tweet | Data post with analysis | Infographic caption | Data post | Data reveal (20s) | Short (30s) | Mini-thread | Link post |
| Story | Thread opener | Story post | Story caption | Long-form post | Story format (30-60s) | Long-form (8-12m) | Conversational post | Experience report |
| Contrarian take | Hot take tweet | Debate post | — | Discussion post | Controversy spark (15s) | Short (15s) | Friendly disagreement | Informed take |
| Step-by-step | Thread | Carousel/document | Carousel | How-to post | Tutorial (30-60s) | Long-form (8-12m) | Mini-thread | Thread |
| List | Thread or single | Listicle post | Carousel | List post | Listicle (20s) | Short (45s) | Single post | Single post |

Load the specific platform file from `references/platforms/` for full playbooks, algorithm signals, templates, and hook formulas.

### Step 3: Write Platform-Native Posts

---

## Platform Rules

### Twitter/X

**Character limit**: 280 per tweet, threads unlimited

**Single Tweet Formula:**
```
[Hook — pattern interrupt or bold claim]

[1-2 sentences of value or proof]

[CTA or takeaway]
```

**Thread Formula:**
```
Tweet 1: Hook — the big promise or contrarian take (this sells the thread)
Tweet 2-N: One idea per tweet, each must standalone
Final tweet: Summary + CTA + "Follow for more [topic]"
```

**Rules:**
- Hook tweet determines 90% of engagement — spend 50% of time on it
- One idea per tweet in threads
- Use line breaks for readability
- No hashtags in the main text (one in reply if any)
- End threads with a retweet ask or follow CTA
- Optimal: 5-12 tweets per thread

**Hook patterns that work:**
- "I spent [time] doing [thing]. Here's what I learned:"
- "[Contrarian statement]. Here's why:"
- "[Big number] [result] in [timeframe]. The playbook:"
- "Stop doing [common thing]. Do this instead:"
- "The [topic] advice nobody gives you:"

### LinkedIn

**Character limit**: 3,000 per post

**Post Formula:**
```
[Hook line — stops the scroll]

[Line break]

[Story or context — 3-5 short paragraphs]

[Key insight or lesson]

[Call to engage: question, agree/disagree, share your experience]

[3-5 hashtags at the bottom]
```

**Rules:**
- First line is everything — it shows before "see more"
- Write in short paragraphs (1-2 sentences each)
- Use "I" — personal stories outperform corporate content 3x
- End with a question to drive comments
- 3-5 relevant hashtags at the bottom only
- No links in the post body (kills reach) — put links in first comment
- Document format/carousels get 3x reach over text posts
- Optimal length: 800-1,500 characters

**Hook patterns:**
- "I made a mistake that cost me [consequence]."
- "Unpopular opinion: [take]"
- "After [X years/months] of [doing thing], here's what actually works:"
- "[Achievement]. But it almost didn't happen."

### Instagram

**Character limit**: 2,200 per caption

**Caption Formula:**
```
[Hook line — first 125 characters show in feed]

[Value content — tips, story, insight]

[CTA — save this, share with someone, comment your take]

.
.
.
[Hashtags — 5-15 relevant ones]
```

**Carousel Strategy:**
- Slide 1: Bold headline (this is the hook)
- Slides 2-N: One point per slide, large text, minimal design
- Final slide: Summary + CTA + account tag
- 7-10 slides is the sweet spot
- Provide text content for each slide with design notes

**Rules:**
- First 125 characters = the hook (visible before "more")
- Carousel posts get 1.4x more reach than single images
- Include image/graphic brief with each post
- Hashtags in caption or first comment (test both)
- CTAs that work: "Save this for later" / "Tag someone who needs this"

### Reddit

**Rules are different here. Reddit hates marketing.**

**Post Formula:**
```
Title: [Specific, descriptive, no clickbait]

Body:
[Context — who you are, why you're sharing]
[The actual value — detailed, generous, no gatekeeping]
[Results or proof if applicable]
[Question to invite discussion]

[NO self-promotion links in the body]
```

**Rules:**
- Provide genuine value first, always
- Match the subreddit's tone and norms
- No links to your stuff in the post — put them in a comment if asked
- Write longer, more detailed posts than other platforms
- Be ready for skepticism — back up claims
- Identify 2-3 relevant subreddits per topic
- Title is plain and specific, not clickbaity

---

## Hooks and CTAs

### Universal Hook Formulas

1. **The Number**: "7 things I learned about [topic]"
2. **The Mistake**: "The biggest [topic] mistake I see:"
3. **The Contrarian**: "[Common belief] is wrong. Here's why:"
4. **The Curiosity Gap**: "Most people [do X]. Top performers [do Y]."
5. **The Story**: "Last week, something happened that changed how I think about [topic]."
6. **The How-To**: "How to [achieve result] in [timeframe]:"
7. **The Data**: "[Stat]. Here's what that means for you:"

### CTA Types by Goal

| Goal | CTA |
|------|-----|
| Engagement | "What's your take?" / "Agree or disagree?" |
| Follows | "Follow for daily [topic] tips" |
| Saves | "Save this for when you need it" |
| Shares | "Tag someone who needs to hear this" |
| Traffic | "Link in bio" / "Link in comments" |
| Email capture | "I wrote a deeper guide — link in bio" |

---

## Output Structure

For each source piece, output a directory:

```
marketing/social/{source-slug}/
├── twitter-threads.md    # 2-3 threads with hook tweets
├── twitter-singles.md    # 5-8 standalone tweets
├── linkedin-posts.md     # 3-5 LinkedIn posts
├── instagram-captions.md # 2-3 captions with carousel briefs
├── reddit-posts.md       # 1-2 Reddit posts with subreddit targets
├── tiktok-scripts.md     # 1-2 short video scripts (15-60s)
├── youtube-shorts.md     # 1-2 YouTube Shorts scripts
├── threads-posts.md      # 2-3 Threads posts or mini-threads
└── bluesky-posts.md      # 2-3 Bluesky posts
```

Only generate files for platforms the user wants. If no preference stated, generate for all 8 platforms. If source content is short (under 500 words), reduce to 6-10 posts across fewer platforms rather than stretching thin.

Each post includes:

```yaml
---
platform: twitter | linkedin | instagram | reddit
type: thread | single | post | carousel | story
source: "original-content-slug"
hook: "first line preview"
character_count: 247
hashtags: ["tag1", "tag2"]
suggested_time: "Tuesday 9am ET"
status: draft
---
```

---

## Posting Schedule

| Platform | Best Times (ET) | Frequency |
|----------|----------------|-----------|
| Twitter/X | 8-10am, 12-1pm, 5-6pm | 1-3x daily |
| LinkedIn | 8-10am Tue-Thu | 3-5x weekly |
| Instagram | 11am-1pm, 7-9pm | 4-7x weekly |
| Reddit | 6-9am, varies by sub | 2-3x weekly |
| TikTok | 7-9pm Tue/Thu | 3-5x weekly |
| YouTube Shorts | 9-11am Sat | 2-3x weekly |
| Threads | 9-11am daily | 3-5x weekly |
| Bluesky | 10am-12pm weekdays | 3-5x weekly |

Space out atomized content over 1-2 weeks. Don't dump everything the same day.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|-------------|-------------|---------|
| Copy-paste the same text across platforms | Platform algorithms detect duplicate content and suppress it. Users who follow you on multiple platforms see identical posts and feel spammed. Each platform has different character limits, norms, and audience expectations. | Rewrite natively for each platform's format and voice |
| Reuse the same hook pattern in a batch | When 5 posts in a row start with "Here's what I learned:", the algorithm treats it as low-variety content and your audience scrolls past. Batch monotony is the #1 tell of AI-generated content. | Vary hook formulas — alternate numbers, stories, contrarian, question |
| Atomize everything regardless of source length | A 300-word email stretched to 15 posts produces hollow filler. Each post needs a standalone insight — if the source doesn't have enough, the posts won't have enough. | Under 500 words → 6-10 posts max. Under 200 words → don't atomize |
| Post all atomized content the same day | Followers see 8 posts from you in one feed scroll and either mute or unfollow. Algorithms also penalize velocity spikes from a single account. | Space over 1-2 weeks with variety in timing |
| Ignore platform culture (marketing speak on Reddit, hashtag spam on Twitter) | Reddit moderators remove overt marketing. Twitter's algorithm deprioritizes hashtag-heavy tweets. Each platform's community has unwritten rules about tone and format. | Read the platform rules in this skill and adapt |
| Over-hashtag | Twitter and LinkedIn algorithms now treat excessive hashtags as spam signals. On Reddit, hashtags don't exist. Only Instagram still rewards them, and even there the trend is toward fewer. | Twitter: 0-1. LinkedIn: 3-5 at bottom. Instagram: 5-15. Reddit: 0 |

---

## Related Skills

- **brand-voice**: Establish voice before atomizing at scale
- **seo-content**: Create the source content to atomize
- **newsletter**: Atomize newsletter content for social
- **creative**: Generate visual asset briefs for social graphics
