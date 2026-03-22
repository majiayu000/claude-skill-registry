---
name: social-publisher
description: "Multi-platform social media publishing automation - schedule, post, and track content across TikTok, Instagram, YouTube, LinkedIn, and more"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: marketing
tags:
  - social-media
  - publishing
  - automation
  - content-distribution
department: Marketing

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4

mcp:
  server: social-media-mcp
  tools:
    - tiktok_upload
    - instagram_publish
    - youtube_upload
    - linkedin_post
    - twitter_post

capabilities:
  - multi_platform_publishing
  - content_scheduling
  - caption_optimization
  - hashtag_management
  - analytics_tracking

languages:
  - en
  - zh

related_skills:
  - tiktok-marketing
  - content-writer
  - image-generation
---

# Social Publisher

Automate multi-platform social media publishing with intelligent scheduling, platform-specific optimization, and centralized content management. Based on n8n workflows like PostPulse.

## Overview

This skill enables:
- One-click publishing to multiple platforms
- Platform-specific caption optimization
- Automated scheduling workflows
- Content tracking and analytics
- AI-powered caption generation

---

## Supported Platforms

| Platform | Content Types | Best Posting Times |
|----------|---------------|-------------------|
| TikTok | Video (9:16) | 7am, 12pm, 7pm |
| Instagram | Reels, Posts, Stories | 11am-1pm, 7-9pm |
| YouTube | Shorts, Videos | 2-4pm (Thu-Sat) |
| LinkedIn | Posts, Articles, Videos | 8-10am (Tue-Thu) |
| Twitter/X | Text, Images, Video | 9am, 12pm, 5pm |
| Facebook | Posts, Reels, Stories | 1-4pm |
| Threads | Text, Images | 7am-9am |
| Pinterest | Pins, Idea Pins | 8-11pm (Sat) |

---

## Publishing Workflow

### Workflow: Google Drive → Multi-Platform

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Google Drive │───▶│ Detect New   │───▶│ Generate     │
│ (Video)      │    │ File         │    │ AI Captions  │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
         ┌─────────────────────────────────────┼─────────────────────────────────────┐
         │                                     │                                     │
         ▼                                     ▼                                     ▼
┌──────────────┐                    ┌──────────────┐                    ┌──────────────┐
│ TikTok       │                    │ Instagram    │                    │ YouTube      │
│ (Casual)     │                    │ (Polished)   │                    │ (SEO-rich)   │
└──────────────┘                    └──────────────┘                    └──────────────┘
         │                                     │                                     │
         └─────────────────────────────────────┼─────────────────────────────────────┘
                                               │
                                               ▼
                                    ┌──────────────┐
                                    │ Track in     │
                                    │ Airtable     │
                                    └──────────────┘
```

### n8n Configuration

```yaml
workflow: "Multi-Platform Video Publisher"

trigger:
  type: google_drive
  event: file_created
  folder: "/Ready to Publish"
  file_types: [mp4, mov]

steps:
  1. get_video_metadata:
      extract: [filename, duration, size]
      
  2. generate_captions:
      provider: openai
      model: gpt-4
      prompts:
        tiktok: |
          Create a TikTok caption for video: {filename}
          Style: Casual, trendy, emoji-friendly
          Include: 3-5 hashtags
          Max: 100 characters
          
        instagram: |
          Create an Instagram Reel caption for: {filename}
          Style: Engaging, slightly longer
          Include: Story element, 5-10 hashtags
          Max: 150 characters (first line hook)
          
        youtube: |
          Create a YouTube Shorts title and description
          Title: SEO-optimized, engaging (60 chars)
          Description: Keywords, 2-3 sentences
          
        linkedin: |
          Create a professional LinkedIn post for: {filename}
          Style: Professional, thought leadership
          Include: Industry insights, CTA
          
  3. publish_parallel:
      tiktok:
        caption: "{tiktok_caption}"
        schedule: optimal_time
        
      instagram:
        type: reel
        caption: "{instagram_caption}"
        cover_image: auto_detect
        
      youtube:
        type: short
        title: "{youtube_title}"
        description: "{youtube_description}"
        visibility: public
        
      linkedin:
        content: "{linkedin_caption}"
        visibility: public
        
  4. track_results:
      platform: airtable
      base: "Content Tracker"
      record:
        video_name: "{filename}"
        platforms: [tiktok, instagram, youtube, linkedin]
        publish_time: "{timestamp}"
        status: "published"
        links: ["{tiktok_url}", "{ig_url}", "{yt_url}", "{li_url}"]
        
  5. notify:
      slack:
        channel: "#content-published"
        message: |
          ✅ Video published to all platforms!
          📹 {filename}
          🔗 TikTok: {tiktok_url}
          🔗 Instagram: {ig_url}
          🔗 YouTube: {yt_url}
          🔗 LinkedIn: {li_url}
```

---

## Platform-Specific Optimization

### Caption Adaptation

```yaml
caption_templates:
  original: "5 productivity hacks that changed my life"
  
  tiktok:
    style: casual, trendy
    output: "POV: you discover these 5 hacks 🤯 #productivity #lifehacks #fyp"
    
  instagram:
    style: engaging, story-driven
    output: |
      These 5 hacks literally changed how I work 💡
      
      Save this for later ⬇️
      
      #productivity #lifehacks #worksmarter #motivation #tips
    
  youtube:
    title: "5 Productivity Hacks That Will Change Your Life"
    description: |
      Discover the top productivity hacks used by successful professionals.
      
      In this video:
      00:00 Introduction
      00:15 Hack #1
      ...
      
      Subscribe for more productivity tips!
      
  linkedin:
    style: professional, insightful
    output: |
      After years of optimizing my workflow, these 5 strategies consistently deliver results:
      
      1. [Hack with professional context]
      2. [Hack with business application]
      ...
      
      Which productivity strategy has made the biggest impact for you?
      
  twitter:
    style: concise, punchy
    output: "5 productivity hacks that actually work (thread 🧵)"
```

### Hashtag Strategy by Platform

```yaml
hashtags:
  tiktok:
    count: 3-5
    mix: [trending, niche, branded]
    placement: end_of_caption
    examples: ["#fyp", "#viral", "#productivity"]
    
  instagram:
    count: 5-15
    mix: [high_volume, medium, niche]
    placement: end_or_comment
    examples: ["#productivity", "#worklife", "#tips"]
    
  youtube:
    count: 3-5 in title area
    placement: description
    style: keyword-focused
    
  linkedin:
    count: 3-5
    placement: end_of_post
    style: professional
    examples: ["#leadership", "#productivity", "#careeradvice"]
    
  twitter:
    count: 1-2
    placement: inline_or_end
    examples: ["#productivity"]
```

---

## Scheduling Strategy

### Content Calendar Template

```yaml
weekly_schedule:
  monday:
    - platform: linkedin
      time: 8:00 AM
      content_type: thought_leadership
      
    - platform: tiktok
      time: 7:00 PM
      content_type: educational
      
  tuesday:
    - platform: instagram
      time: 12:00 PM
      content_type: reel
      
    - platform: twitter
      time: 9:00 AM
      content_type: thread
      
  wednesday:
    - platform: youtube
      time: 3:00 PM
      content_type: short
      
    - platform: linkedin
      time: 10:00 AM
      content_type: article
      
  thursday:
    - platform: tiktok
      time: 12:00 PM
      content_type: trend
      
    - platform: instagram
      time: 7:00 PM
      content_type: carousel
      
  friday:
    - platform: all
      time: varies
      content_type: engagement_post
```

### Batch Publishing

```yaml
batch_workflow:
  name: "Weekly Content Batch"
  
  input:
    folder: "/Content/Week-{week_number}"
    videos: 7
    
  process:
    1. sort_by_type:
        educational: [mon, wed, fri]
        entertainment: [tue, thu]
        promotional: [sat]
        community: [sun]
        
    2. assign_platforms:
        each_video:
          primary: auto_detect_best_fit
          secondary: [remaining_platforms]
          
    3. generate_all_captions:
        batch_size: 7
        parallel: true
        
    4. schedule:
        distribution: optimal_times
        gap_between: minimum_4_hours
        
    5. queue_for_review:
        send_to: content_manager
        deadline: 24_hours_before_first_post
```

---

## Analytics Integration

### Cross-Platform Tracking

```yaml
tracking_fields:
  per_post:
    - post_id
    - platform
    - publish_time
    - content_type
    - caption
    - hashtags
    - views (24h, 48h, 7d)
    - likes
    - comments
    - shares
    - saves
    - profile_visits
    - follower_change
    
  aggregated:
    - total_reach
    - engagement_rate
    - best_performing_content
    - optimal_posting_times
    - audience_growth
```

### Performance Dashboard

```markdown
# Weekly Social Media Report

## Overview
| Platform | Posts | Reach | Engagement | Followers |
|----------|-------|-------|------------|-----------|
| TikTok | 7 | 150K | 8.5% | +500 |
| Instagram | 5 | 45K | 4.2% | +200 |
| YouTube | 3 | 25K | 6.1% | +150 |
| LinkedIn | 5 | 15K | 3.8% | +75 |

## Top Performing Content
1. TikTok: "5 productivity hacks" - 45K views, 12% engagement
2. Instagram: "Day in my life" - 18K views, 5.5% engagement
3. YouTube: "Tutorial video" - 12K views, 8% engagement

## Insights
- Best day: Thursday (2x average engagement)
- Best time: 7pm (highest reach)
- Best content type: Educational (3x shares)

## Next Week Recommendations
- Create more educational content
- Post 2x on Thursdays
- Test 7pm posting time across all platforms
```

---

## Output Example

**Request**: "I have a video about remote work tips. Create captions for all platforms."

**Output**:

```markdown
# Multi-Platform Captions: Remote Work Tips

## TikTok
```
POV: you finally master working from home 🏠💻

These 3 tips changed everything for me ⬇️

#remotework #wfh #productivityhacks #workfromhome #fyp
```

## Instagram Reel
```
3 years of remote work taught me these game-changers 🚀

The fake commute one? Actually life-changing.

Save this for your next WFH day 📌

.
.
.
#remotework #workfromhome #productivitytips #wfhlife #careeradvice #worklifebalance #homeoffice #remoteworker #digitalnomad #productivity
```

## YouTube Short
**Title**: "3 Remote Work Tips That Actually Work"

**Description**:
```
Master working from home with these proven productivity tips.

After 3 years of remote work, these strategies have made the biggest difference in my daily routine and output.

⏰ Timestamps:
0:00 - Intro
0:05 - Tip 1: The Fake Commute
0:20 - Tip 2: Time Blocking
0:35 - Tip 3: Shutdown Ritual

Subscribe for more productivity content!

#shorts #remotework #productivity
```

## LinkedIn
```
3 years of remote work. Here's what actually moves the needle:

1️⃣ The Fake Commute
A 10-minute walk before work signals to your brain that it's time to focus. Sounds simple, but it's been transformative for my morning productivity.

2️⃣ Time Blocking (with Buffer)
Schedule focus time AND buffer time. Back-to-back calls without breaks is a recipe for burnout.

3️⃣ The Shutdown Ritual
When you close your laptop, verbally say "shutdown complete." This cognitive boundary helps separate work from personal time.

What's your best remote work tip?

#remotework #productivity #worklifebalance #leadership
```

## Twitter/X
```
3 remote work tips that actually work:

1. Take a "fake commute" - walk around the block before starting
2. Time block with 15-min buffers between calls
3. Say "shutdown complete" when you close your laptop

The last one sounds weird but it's a game-changer for mental boundaries.
```

---

**Recommended Posting Schedule:**
- TikTok: Thursday 7pm
- Instagram: Friday 12pm
- YouTube: Saturday 3pm
- LinkedIn: Tuesday 9am
- Twitter: Wednesday 12pm
```

---

*Social Publisher Skill - Part of Claude Office Skills*
