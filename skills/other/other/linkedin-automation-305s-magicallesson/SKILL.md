---
name: LinkedIn Automation
description: Automate LinkedIn marketing, lead generation, content publishing, and professional networking
version: 1.0.0
author: Claude Office Skills
category: social-media
tags:
  - linkedin
  - b2b
  - networking
  - lead-generation
  - content
department: marketing
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: social-mcp
  tools:
    - linkedin_post
    - linkedin_message
    - linkedin_analytics
    - linkedin_leads
capabilities:
  - Content publishing
  - Lead generation
  - Network building
  - Analytics tracking
input:
  - Post content
  - Connection criteria
  - Message templates
  - Campaign settings
output:
  - Published posts
  - Lead lists
  - Engagement metrics
  - Network growth
languages:
  - en
related_skills:
  - twitter-automation
  - social-publisher
  - ads-copywriter
---

# LinkedIn Automation

Comprehensive skill for automating LinkedIn marketing and B2B lead generation.

## Core Workflows

### 1. Content Pipeline

```
LINKEDIN CONTENT FLOW:
┌─────────────────┐
│  Content Plan   │
│  - Topics       │
│  - Calendar     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Create Post    │
│  - Text         │
│  - Visual       │
│  - Document     │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Optimize      │
│  - Hook         │
│  - Hashtags     │
│  - CTA          │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Schedule      │
│  - Best time    │
│  - Frequency    │
└────────┬────────┘
         ▼
┌─────────────────┐
│    Engage       │
│  - Comments     │
│  - DMs          │
└─────────────────┘
```

### 2. Lead Generation Flow

```yaml
lead_gen_workflow:
  search:
    filters:
      - industry: "Software"
      - company_size: "51-200"
      - title_contains: ["CEO", "CTO", "VP"]
      - location: "San Francisco Bay Area"
      
  qualify:
    criteria:
      - has_recent_activity: true
      - mutual_connections: "> 3"
      - engagement_score: "> 50"
      
  outreach:
    sequence:
      - action: connect
        message: connection_request
      - wait: 2_days
      - action: message
        template: intro_message
      - wait: 3_days
      - action: follow_up
        template: value_add
```

## Content Templates

### Post Formats

```yaml
post_templates:
  story_post:
    format: |
      {{hook_line}}
      
      ↓
      
      {{story_paragraph_1}}
      
      {{story_paragraph_2}}
      
      {{lesson_learned}}
      
      {{call_to_action}}
      
      ---
      ♻️ Repost if this resonated
      🔔 Follow for more insights
      
    example: |
      I got rejected 47 times before landing my dream job.
      
      ↓
      
      Each rejection felt like a punch to the gut.
      But I kept going.
      
      Here's what changed everything:
      I stopped trying to "impress" and started being authentic.
      
      The 48th interview? I got 2 offers.
      
      Lesson: Rejection is redirection, not the end.
      
      ---
      ♻️ Repost if this resonated
      🔔 Follow @profile for career tips

  list_post:
    format: |
      {{title}}
      
      {{point_1}}
      {{point_2}}
      {{point_3}}
      {{point_4}}
      {{point_5}}
      
      {{wrap_up}}
      
      Which one is most important to you? 👇
      
  carousel:
    slides:
      - cover: hook_title
      - slides: [content_1, content_2, content_3]
      - cta: follow_cta
    design:
      size: "1080x1350"
      format: "pdf"
```

### Engagement Templates

```yaml
engagement_templates:
  comment_responses:
    thanks:
      - "Thanks for sharing your perspective, {{name}}!"
      - "Great point, {{name}}. I hadn't considered that angle."
      - "Appreciate you adding to the conversation, {{name}}!"
      
    question:
      - "Great question! {{answer}}"
      - "I'd say {{answer}}. What's your take?"
      
  proactive_comments:
    value_add:
      - "This is spot on. I'd add that {{insight}}..."
      - "Love this perspective. In my experience, {{experience}}..."
      - "Couldn't agree more. The key is {{key_point}}..."
```

## Outreach Automation

### Connection Requests

```yaml
connection_templates:
  mutual_connection:
    message: |
      Hi {{first_name}},
      
      I noticed we're both connected to {{mutual}}. 
      I'm impressed by your work at {{company}}.
      
      Would love to connect and learn more about 
      what you're building.
      
      Best,
      {{my_name}}
      
  shared_interest:
    message: |
      Hi {{first_name}},
      
      I came across your post about {{topic}} and 
      found it really insightful.
      
      I'm also passionate about {{topic}} and would 
      love to connect.
      
      Looking forward to learning from you!
```

### Message Sequences

```yaml
outreach_sequence:
  - step: 1
    type: connection_request
    template: mutual_connection
    
  - step: 2
    trigger: connection_accepted
    delay: 2_days
    type: message
    template: |
      Thanks for connecting, {{first_name}}!
      
      I'm curious - what's the biggest challenge 
      you're facing with {{pain_point}} right now?
      
  - step: 3
    trigger: no_response
    delay: 5_days
    type: message
    template: |
      Hi {{first_name}},
      
      Just wanted to share this {{resource_type}} 
      on {{topic}} - thought you might find it useful:
      
      {{resource_link}}
      
      No strings attached, just thought of you!
      
  - step: 4
    trigger: response_received
    type: personalized
    action: manual_follow_up
```

## Company Page Management

### Page Content Strategy

```yaml
company_page:
  content_pillars:
    - thought_leadership: 40%
    - company_culture: 25%
    - product_updates: 20%
    - industry_news: 15%
    
  posting_schedule:
    frequency: 5_per_week
    best_times:
      - "08:00"
      - "12:00"
      - "17:30"
    best_days:
      - tuesday
      - wednesday
      - thursday
      
  employee_advocacy:
    enabled: true
    suggested_posts: weekly
    gamification: true
```

### Showcase Pages

```yaml
showcase_pages:
  - name: "{{Product}} Solutions"
    focus: product_specific_content
    audience: target_buyers
    
  - name: "{{Company}} Careers"
    focus: employer_branding
    audience: potential_candidates
```

## LinkedIn Ads

### Campaign Types

```yaml
ad_campaigns:
  sponsored_content:
    objective: lead_generation
    format: single_image
    targeting:
      job_titles: ["Marketing Manager", "CMO"]
      company_size: ["51-200", "201-500"]
      industries: ["Software", "SaaS"]
    budget: 100_per_day
    
  message_ads:
    objective: conversions
    sender: sales_rep
    template: |
      Hi {{first_name}},
      
      I noticed {{company}} is growing rapidly. 
      Many similar companies are using {{product}} 
      to {{benefit}}.
      
      Would you be open to a quick chat?
      
      {{cta_button}}
      
  lead_gen_forms:
    fields:
      - first_name
      - last_name
      - email
      - company
      - job_title
    offer: "Download our free guide"
```

## Analytics Dashboard

```
LINKEDIN ANALYTICS - LAST 30 DAYS
═══════════════════════════════════════

PROFILE:
Views:        2,450 (+18%)
Connections:  +156
Search Appearances: 892

POST PERFORMANCE:
┌────────────────────────────────────────┬────────┬────────┐
│ Post                                    │ Impr.  │ Eng.   │
├────────────────────────────────────────┼────────┼────────┤
│ "The hiring mistake I made..."         │ 45,230 │ 8.2%   │
│ "5 lessons from 10 years..."           │ 32,450 │ 6.8%   │
│ Product announcement                    │ 12,340 │ 3.2%   │
└────────────────────────────────────────┴────────┴────────┘

ENGAGEMENT:
Likes:        1,234
Comments:     456
Shares:       89
Saves:        234

AUDIENCE GROWTH:
Week 1: +45  ████████████░░░░
Week 2: +52  ██████████████░░
Week 3: +38  ██████████░░░░░░
Week 4: +21  █████░░░░░░░░░░░

COMPANY PAGE:
Followers:    8,450 (+320)
Page Views:   4,230
Post Reach:   125,000
```

## Lead Management

### Lead Scoring

```yaml
lead_scoring:
  criteria:
    profile_completeness:
      photo: 5
      headline: 5
      summary: 10
      
    engagement:
      liked_post: 5
      commented: 15
      shared: 20
      dm_response: 25
      
    fit:
      title_match: 20
      company_size_match: 15
      industry_match: 10
      
  tiers:
    hot: "> 75"
    warm: "50-75"
    cold: "< 50"
```

### CRM Integration

```yaml
crm_sync:
  triggers:
    - new_connection
    - message_received
    - lead_form_submitted
    
  mapping:
    linkedin_url: crm_linkedin_field
    company: crm_company
    title: crm_job_title
    
  actions:
    create_contact: true
    add_to_sequence: true
    notify_owner: true
```

## Best Practices

1. **Consistency**: Post 3-5 times per week
2. **Value First**: Give before you ask
3. **Engage Authentically**: Real comments, not generic
4. **Optimize Profile**: Photo, headline, summary
5. **Use Hooks**: First line must grab attention
6. **Storytelling**: Personal stories perform best
7. **Hashtags**: 3-5 relevant hashtags
8. **Respond Quickly**: Engage in first hour
