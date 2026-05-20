---
name: Podcast Automation
description: Automate podcast production workflows including recording, editing, publishing, and distribution
version: 1.0.0
author: Claude Office Skills
category: multimedia
tags:
  - podcast
  - audio
  - content
  - distribution
  - marketing
department: content
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: media-mcp
  tools:
    - podcast_publish
    - audio_process
    - rss_generate
    - distribution_sync
capabilities:
  - Episode publishing
  - Audio processing
  - RSS feed management
  - Multi-platform distribution
input:
  - Audio files
  - Episode metadata
  - Show notes
  - Distribution settings
output:
  - Published episodes
  - RSS feeds
  - Analytics reports
  - Marketing assets
languages:
  - en
related_skills:
  - youtube-automation
  - transcription-automation
  - social-publisher
---

# Podcast Automation

Comprehensive skill for automating podcast production and distribution.

## Core Workflows

### 1. Production Pipeline

```
PODCAST PRODUCTION FLOW:
┌─────────────────┐
│    Planning     │
│  - Topics       │
│  - Guests       │
│  - Schedule     │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Recording     │
│  - Audio        │
│  - Video (opt)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│    Editing      │
│  - Clean audio  │
│  - Add intro    │
│  - Mastering    │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Production    │
│  - Show notes   │
│  - Transcript   │
│  - Chapters     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Distribution   │
│  - RSS          │
│  - Platforms    │
│  - Social       │
└─────────────────┘
```

### 2. Episode Configuration

```yaml
episode_config:
  metadata:
    title: "{{episode_title}}"
    episode_number: "{{number}}"
    season: "{{season}}"
    description: "{{description}}"
    
  audio:
    file: "episode_{{number}}.mp3"
    format: mp3
    bitrate: 128kbps
    sample_rate: 44100
    
  settings:
    explicit: false
    episode_type: full  # full, trailer, bonus
    
  chapters:
    - start: "00:00:00"
      title: "Introduction"
    - start: "00:02:30"
      title: "Main Topic"
    - start: "00:45:00"
      title: "Q&A"
    - start: "00:55:00"
      title: "Wrap Up"
      
  links:
    - title: "Show Notes"
      url: "{{show_notes_url}}"
    - title: "Guest's Website"
      url: "{{guest_url}}"
```

## Audio Processing

### Processing Pipeline

```yaml
audio_processing:
  input:
    format: wav
    channels: stereo
    
  processing:
    - step: noise_reduction
      threshold: -30db
      
    - step: normalization
      target_lufs: -16
      
    - step: compression
      ratio: 4:1
      threshold: -20db
      
    - step: eq
      preset: voice_enhance
      
    - step: add_intro
      file: "intro.mp3"
      fade_in: 2s
      
    - step: add_outro
      file: "outro.mp3"
      fade_out: 3s
      
  output:
    format: mp3
    bitrate: 128kbps
    filename: "{{show}}_E{{number}}.mp3"
```

### Mastering Template

```yaml
mastering_config:
  loudness:
    target: -16 LUFS
    range: 8 LU
    true_peak: -1 dBTP
    
  eq_settings:
    high_pass: 80Hz
    presence_boost: +2dB @ 3kHz
    air: +1dB @ 12kHz
    
  dynamics:
    compressor:
      ratio: 3:1
      attack: 10ms
      release: 100ms
    limiter:
      ceiling: -1dB
```

## Show Notes Template

### Episode Notes

```yaml
show_notes_template:
  format: markdown
  
  structure: |
    # {{episode_title}}
    
    ## Episode {{number}} | Season {{season}}
    
    **Published:** {{publish_date}}
    **Duration:** {{duration}}
    
    ## Summary
    {{summary}}
    
    ## Guest
    {{#if guest}}
    **{{guest.name}}** - {{guest.title}}
    - Website: {{guest.website}}
    - Twitter: {{guest.twitter}}
    - LinkedIn: {{guest.linkedin}}
    {{/if}}
    
    ## Timestamps
    {{#each chapters}}
    - {{this.start}} - {{this.title}}
    {{/each}}
    
    ## Key Takeaways
    {{#each takeaways}}
    - {{this}}
    {{/each}}
    
    ## Resources Mentioned
    {{#each resources}}
    - [{{this.title}}]({{this.url}})
    {{/each}}
    
    ## Subscribe
    - [Apple Podcasts]({{apple_url}})
    - [Spotify]({{spotify_url}})
    - [RSS Feed]({{rss_url}})
```

## RSS Feed Management

### Feed Configuration

```yaml
rss_feed:
  channel:
    title: "{{podcast_name}}"
    description: "{{podcast_description}}"
    language: "en-us"
    copyright: "© 2024 {{company}}"
    author: "{{host_name}}"
    owner:
      name: "{{owner_name}}"
      email: "{{owner_email}}"
    image:
      url: "{{artwork_url}}"
      width: 3000
      height: 3000
    categories:
      - "Business"
      - "Technology"
    explicit: false
    
  itunes:
    type: episodic  # or serial
    complete: false
    
  items:
    - title: "{{episode.title}}"
      description: "{{episode.description}}"
      enclosure:
        url: "{{audio_url}}"
        length: "{{file_size}}"
        type: "audio/mpeg"
      pubDate: "{{publish_date}}"
      duration: "{{duration}}"
      explicit: false
      episode: "{{number}}"
      season: "{{season}}"
```

## Distribution

### Platform Distribution

```yaml
distribution_platforms:
  primary:
    - platform: apple_podcasts
      api: podcasts_connect
      auto_publish: true
      
    - platform: spotify
      api: spotify_for_podcasters
      auto_publish: true
      
  secondary:
    - google_podcasts
    - amazon_music
    - stitcher
    - overcast
    - pocket_casts
    - castbox
    
  video:
    - platform: youtube
      type: full_episode
      thumbnail: auto_generate
      
    - platform: youtube
      type: clips
      count: 3-5
      duration: 60s
```

### Social Distribution

```yaml
social_promotion:
  on_publish:
    - platform: twitter
      posts:
        - type: announcement
          text: |
            🎙️ New Episode!
            
            {{episode.title}}
            
            {{teaser}}
            
            Listen now: {{link}}
            
        - type: clip
          audio_clip: 60s
          timestamp: best_moment
          
    - platform: linkedin
      text: |
        Excited to share our latest episode!
        
        {{episode.title}}
        
        Key takeaways:
        {{takeaways}}
        
        Link in comments 👇
        
    - platform: instagram
      type: carousel
      slides:
        - cover_image
        - quote_1
        - quote_2
        - cta
```

## Analytics Dashboard

```
PODCAST ANALYTICS - LAST 30 DAYS
═══════════════════════════════════════

DOWNLOADS: 45,230 (+12%)
UNIQUE LISTENERS: 28,450

BY EPISODE:
┌─────────────────────────────────────┬───────────┐
│ Episode                              │ Downloads │
├─────────────────────────────────────┼───────────┤
│ E45: Interview with CEO             │ 8,450     │
│ E44: Industry Trends 2024           │ 6,230     │
│ E43: Behind the Scenes              │ 5,890     │
└─────────────────────────────────────┴───────────┘

BY PLATFORM:
Apple Podcasts  ████████████████ 52%
Spotify         ██████████░░░░░░ 32%
Google          ████░░░░░░░░░░░░ 8%
Other           ███░░░░░░░░░░░░░ 8%

LISTENER RETENTION:
0-25%    ████████████████████ 100%
25-50%   ██████████████████░░ 89%
50-75%   ██████████████░░░░░░ 72%
75-100%  ████████████░░░░░░░░ 58%

GEOGRAPHY:
United States   ████████████████ 65%
United Kingdom  ████░░░░░░░░░░░░ 12%
Canada          ███░░░░░░░░░░░░░ 8%
Australia       ██░░░░░░░░░░░░░░ 5%
```

## Guest Management

### Guest Workflow

```yaml
guest_workflow:
  outreach:
    template: |
      Hi {{guest_name}},
      
      I'm the host of {{podcast_name}}, a podcast about {{topic}}.
      
      I'd love to have you on to discuss {{proposed_topic}}.
      
      Our audience is {{audience_description}}.
      
      Would you be interested?
      
  scheduling:
    tool: calendly
    duration: 60_minutes
    buffer: 15_minutes
    
  pre_interview:
    send_days_before: 3
    includes:
      - recording_guide
      - topic_outline
      - tech_requirements
      - consent_form
      
  post_interview:
    - send_thank_you
    - share_publish_date
    - provide_promotional_assets
    - request_share
```

## Monetization

### Revenue Streams

```yaml
monetization:
  sponsorships:
    placements:
      - pre_roll: 15-30s
      - mid_roll: 60s
      - post_roll: 15s
    pricing:
      cpm: 25  # per 1000 downloads
      
  premium_content:
    platform: patreon
    tiers:
      - name: "Supporter"
        price: 5
        benefits:
          - ad_free_episodes
          - bonus_content
      - name: "Premium"
        price: 15
        benefits:
          - all_supporter
          - exclusive_episodes
          - community_access
          
  affiliate:
    programs:
      - amazon_associates
      - product_partnerships
    disclosure: required
```

## Best Practices

1. **Consistent Schedule**: Same day/time each week
2. **Quality Audio**: Invest in good equipment
3. **Show Notes**: Detailed and SEO-optimized
4. **Transcripts**: Accessibility and SEO
5. **Promotion**: Multi-platform marketing
6. **Engage Listeners**: Respond to feedback
7. **Analytics**: Track and improve
8. **Guest Prep**: Well-prepared interviews
