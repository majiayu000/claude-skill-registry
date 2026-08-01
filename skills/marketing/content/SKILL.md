---
name: content
description: 'Department: Content'
---

# Content Department Skill

**Skill**: content
**Department**: Content
**Version**: 1.0.0

---

## 📖 Description

The **Content Department** is your expert team for all content creation needs. From blog posts to social media, newsletters to video scripts, our content agents create, optimize, and publish engaging content across all platforms.

Whether you need a single blog post or a full content strategy, the Content Department has you covered.

---

## 🎯 When to Use

Use this skill when you need to:

- 📝 **Write blog posts or articles**
- 🐦 **Create social media content**
- 📧 **Send newsletters**
- 🎬 **Produce video scripts**
- 📄 **Create landing page copy**
- 📚 **Write whitepapers or case studies**
- 🛍️ **Write product descriptions**
- 📰 **Create press releases**

---

## 👥 Agents in This Department

1. **Content Lead** - Coordinates the team and manages workflows
2. **Writer Agent** - Creates initial drafts and content
3. **Editor Agent** - Reviews, optimizes, and polishes
4. **Publisher Agent** - Formats and publishes to platforms

---

## 🛠️ Tools Available

- **filesystem-mcp**: Read/write content files, manage content directory
- **database-mcp**: Store and retrieve content from database
- **browser-mcp**: Preview content, test on websites
- **website-mcp**: Publish to WordPress, Ghost, custom sites
- **email-mcp**: Send newsletters via email providers

---

## 📋 Common Tasks

### Create Blog Post
```
→ "Write a blog post about [topic]"
→ "Create a 1500-word article about [subject]"
→ "Write how-to guide for [process]"
```

### Create Social Media
```
→ "Create LinkedIn post about [topic]"
→ "Write Twitter thread about [subject]"
→ "Generate Instagram captions for [product]"
```

### Newsletter
```
→ "Prepare this week's newsletter"
→ "Create email announcing [event/product]"
→ "Write newsletter about [topic]"
```

### Video/Audio
```
→ "Write YouTube video script about [topic]"
→ "Create podcast show notes for [episode]"
→ "Generate video description for [video]"
```

---

## 💡 Examples

### Example 1: Blog Post
```
You: "skill:content, write a blog post about the future of AI"

Claude:
I'll create a comprehensive blog post about AI's future.
Let me research current trends, write an engaging article,
optimize it for SEO, and prepare it for publishing.

[Researches → Writes → Optimizes → Saves to database]
```

### Example 2: Social Media Campaign
```
You: "skill:content, create LinkedIn and Twitter posts for my product launch"

Claude:
I'll create platform-optimized content for LinkedIn (professional)
and Twitter (concise with hashtags).

[Creates content for both platforms → Saves]
```

### Example 3: Newsletter
```
You: "skill:content, send monthly newsletter with our top articles"

Claude:
I'll gather your top performing content, create a compelling
newsletter narrative, and prepare it for sending to your subscribers.

[Aggregates content → Writes newsletter → Prepares for sending]
```

---

## ⚡ Quick Commands

| Command | Description |
|---------|-------------|
| `skill:content, write [type] about [topic]` | Create content |
| `skill:content, optimize [content_id]` | SEO optimize |
| `skill:content, publish [content_id] to [platforms]` | Publish content |
| `skill:content, create social posts for [content_id]` | Create social versions |

---

## 🔧 Configuration

### Default Settings
```yaml
content:
  tone: professional
  length: medium
  seo_optimization: true
  publish_immediately: false
  platforms: [website]
```

### Customization
Specify preferences in your request:
- `tone`: professional, casual, friendly, technical
- `length`: short, medium, long
- `seo_optimization`: true/false
- `publish_immediately`: true/false

---

## 📊 Department Stats

- **Content Created**: [Tracked in database]
- **Avg. Engagement**: [Analytics integrated]
- **SEO Score**: [Optimization tracking]
- **Success Rate**: 98%+

---

## 🎓 Best Practices

1. **Be Specific**: Provide topic, audience, and goals
2. **Include Keywords**: Share important keywords for SEO
3. **Set Tone**: Professional, casual, technical?
4. **Specify Length**: Short, medium, or long-form?
5. **Add Context**: Any brand guidelines or style preferences?

---

## 🔗 Related Skills

- **business**: For business documents and operations
- **design**: For visual content and branding
- **marketing**: For promotional and ad content
- **dev**: For technical documentation

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-14 | Initial release |

---

## 🆘 Troubleshooting

**Content not publishing?**
- Check platform credentials are configured
- Verify content is approved
- Check rate limits on platforms

**SEO score low?**
- Add more relevant keywords
- Improve readability
- Add internal/external links

**Writer's block?**
- Provide more context about topic
- Ask for outline first
- Break into smaller sections

---

*Part of Agentic Creator OS - MCP-Native Edition*
*For support, see department documentation*
