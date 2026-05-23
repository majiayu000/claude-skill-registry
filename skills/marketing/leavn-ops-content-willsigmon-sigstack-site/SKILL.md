---
name: Leavn Ops: Content Marketing Skill
description: Use this skill when creating devotional content, social media posts, or video scripts for Leavn marketing.
allowed-tools: Read, Grep, Bash
---

# Leavn Ops: Content Marketing Skill

Use this skill when creating devotional content, social media posts, or video scripts for Leavn marketing.

## CLI Commands Available

```bash
# Generate content calendar
leavn-ops content calendar --weeks 4

# Generate social posts for a topic
leavn-ops content social --topic "finding peace" --platform all

# Generate video script
leavn-ops content video --topic "morning prayer" --duration 30
```

## Content Best Practices

### Devotional Writing
1. **Scripture First**: Every devotional should be anchored in a specific Bible passage
2. **Relatable Opening**: Start with a universal human experience
3. **Practical Application**: Include 2-3 actionable takeaways
4. **Prayer Closing**: End with a short prayer or reflection prompt
5. **Length**: 300-500 words (2-3 minute read)

### Social Media Strategy

#### Twitter/X
- Thread format works best (3-5 tweets)
- Lead with a hook or question
- Include 1 Scripture per thread
- End with engagement prompt (poll, question)
- Hashtags: #Faith #DailyDevotional #Leavn

#### Instagram
- Carousel posts (5-7 slides) for educational content
- Quote cards for Scripture
- Behind-the-scenes Stories
- Reels for testimonials or tips
- Caption: Hook + story + CTA + hashtags (20-30)

#### Facebook
- Longer form acceptable (200-300 words)
- Question prompts drive engagement
- Share community testimonials
- Link to app in comments (not post)

### Video Content
- **Hook**: First 3 seconds must grab attention
- **Value**: Deliver insight quickly (no fluff)
- **CTA**: Clear call-to-action at end
- **Duration**: 15-60 seconds for Reels/TikTok/Shorts
- **Captions**: Always include (80% watch muted)

## Image Generation Prompts

### Quote Cards
```
Minimalist quote card, elegant serif typography,
soft gradient background (amber to cream),
Scripture verse about [topic], high contrast,
Instagram square format, professional design
```

### Hero Images
```
Cinematic [scene description], warm golden hour lighting,
spiritual atmosphere, peaceful mood, 4K quality,
suitable for app marketing, [topic] theme
```

### Video Thumbnails
```
Eye-catching YouTube thumbnail style,
bold text overlay "[Topic]", warm colors,
human emotion, high contrast, professional
```

## Content Calendar Themes

Rotate weekly themes for variety:
1. **Prayer** - Types of prayer, prayer practices
2. **Gratitude** - Thankfulness, counting blessings
3. **Peace** - Finding calm, trusting God
4. **Hope** - Future promises, overcoming fear
5. **Love** - God's love, loving others
6. **Faith** - Trusting God, belief stories
7. **Community** - Fellowship, serving others
8. **Wisdom** - Proverbs, decision-making

## Integration with Other Tools

After generating content with `leavn-ops content`:
1. Use DALL-E/Midjourney for images (prompts included in output)
2. Use ElevenLabs for audio versions
3. Schedule with Buffer/Later/native schedulers
4. Track performance in analytics

## Output Location
All content is saved to: `~/.local/share/leavn-ops/outputs/`
