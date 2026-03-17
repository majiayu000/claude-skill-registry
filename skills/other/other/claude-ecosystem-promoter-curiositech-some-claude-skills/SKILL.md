---
name: claude-ecosystem-promoter
description: Marketing and promotion specialist for Claude ecosystem technology - MCP servers, skills, plugins, and agents. Expert in community engagement, registry submissions, content marketing, and developer relations. Activate on 'promote MCP', 'share skill', 'market plugin', 'launch agent', 'developer marketing', 'MCP registry'. NOT for creating MCPs/skills (use agent-creator), general marketing (use content-marketer), or SEO optimization (use seo-visibility-expert).
allowed-tools: Read,Write,Edit,Glob,Grep,Bash,mcp__firecrawl__firecrawl_search,mcp__brave-search__brave_web_search,WebFetch,mcp__fetch__fetch
category: Business & Monetization
tags:
  - marketing
  - community
  - mcp
  - developer-relations
  - promotion
pairs-with:
  - skill: seo-visibility-expert
    reason: SEO for skill/MCP discoverability
  - skill: agent-creator
    reason: Create the things you promote
---

# Claude Ecosystem Promoter

Marketing specialist for Claude ecosystem technology. Transform your MCP servers, skills, plugins, and agents from hidden gems into widely-adopted tools.

## Quick Start

```
User: "I built an MCP server for Notion, how do I get people to use it?"

Claude Ecosystem Promoter:
1. Audit readiness (README, docs, installation ease)
2. Submit to Official MCP Registry (primary)
3. List on aggregators (Smithery, Glama, PulseMCP)
4. Post to Reddit (r/ClaudeAI, r/mcp)
5. Create demo content (video, GIF, screenshots)
6. Engage in Discord communities
7. Write launch post (dev.to, Medium, LinkedIn)
```

**Result**: Multi-channel launch reaching 50K+ potential users

## The Promotion Landscape (2025)

### Tier 1: Official Channels (Must-Do)

| Channel | Audience | Submission |
|---------|----------|------------|
| **MCP Registry** | All MCP clients | GitHub PR to modelcontextprotocol/registry |
| **anthropics/skills** | Claude Code users | GitHub PR (official skills only) |
| **modelcontextprotocol/servers** | Reference implementations | GitHub PR |

### Tier 2: Community Registries (High Impact)

| Registry | Focus | How to Submit |
|----------|-------|---------------|
| **Smithery.ai** | Hosted MCP servers | Dashboard submission |
| **Glama.ai** | 12K+ MCP directory | "Add Server" button |
| **PulseMCP.com** | Newsletter + directory | Submit via site |
| **SkillsMP.com** | 2300+ Claude skills | Aggregates from GitHub |
| **MCPMarket.com** | MCP marketplace | Submit via site |

### Tier 3: Reddit Communities (Engagement)

| Subreddit | Members | Best For |
|-----------|---------|----------|
| **r/ClaudeAI** | 150K+ | Skills, plugins, general Claude tools |
| **r/mcp** | Growing | MCP-specific showcases |
| **r/ClaudeCode** | Growing | Development workflows |
| **r/LocalLLaMA** | 400K+ | Self-hosted/local MCP servers |
| **r/artificial** | 1M+ | Broader AI audience |

### Tier 4: Awesome Lists (SEO + Discovery)

| Repository | Focus |
|------------|-------|
| **travisvn/awesome-claude-skills** | Claude skills curation |
| **ComposioHQ/awesome-claude-skills** | Community skills |
| **punkpeye/awesome-mcp-servers** | MCP server collection |
| **wong2/awesome-mcp-servers** | Popular MCP list |

### Tier 5: Content Platforms

| Platform | Content Type | Audience |
|----------|--------------|----------|
| **YouTube** | Tutorials, demos | Visual learners |
| **dev.to** | Technical posts | Developers |
| **Medium** | Launch stories | Broader tech |
| **LinkedIn** | Professional updates | Enterprise |
| **X/Twitter** | Quick updates, threads | Tech community |
| **Discord** | Community engagement | Active users |

## Launch Checklist

### Pre-Launch (Quality Gate)

- [ ] **README.md** is comprehensive with:
  - Clear problem statement
  - Installation (one-liner preferred)
  - Quick start example
  - Screenshots/GIFs
  - Configuration options
- [ ] **License** is permissive (MIT, Apache 2.0)
- [ ] **Working demo** or example project
- [ ] **Video walkthrough** (2-5 minutes)
- [ ] **Social preview image** (1200x630px)

### Launch Day

- [ ] Submit to Official MCP Registry
- [ ] Post to r/ClaudeAI with [Showcase] tag
- [ ] Post to r/mcp
- [ ] Tweet/post on X with relevant hashtags
- [ ] Submit to Smithery.ai
- [ ] Submit to Glama.ai

### Week 1

- [ ] Write dev.to launch post
- [ ] Submit PRs to awesome lists
- [ ] Engage with comments/feedback
- [ ] Post demo video to YouTube
- [ ] Share in relevant Discord servers

### Ongoing

- [ ] Respond to GitHub issues promptly
- [ ] Post updates for major releases
- [ ] Collect and share user testimonials
- [ ] Cross-promote with complementary tools

## Content Templates

### Reddit Post Template

```markdown
# [Showcase] Tool Name - One-line description

**Problem**: What pain point does this solve?

**Solution**: Brief explanation of your tool

**Demo**: [Link to video/GIF]

**Install**:
```
npx @your-org/mcp-server
```

**GitHub**: [link]

**What's next**: Roadmap items, looking for feedback on X

Happy to answer questions!
```

### Tweet/X Thread Template

```
1/ Just launched [Tool Name] - [one-liner]

Here's what it does and why you might want it: 🧵

2/ The problem: [Pain point in 280 chars]

3/ The solution: [Your approach]

4/ Quick demo: [GIF or video link]

5/ Get started:
- GitHub: [link]
- Install: [one-liner]

6/ What's next: [roadmap]

Feedback welcome! What features would you find useful?
```

### dev.to Post Structure

```markdown
# I Built [Tool] to Solve [Problem] - Here's How

## The Problem
[2-3 paragraphs on the pain point]

## Existing Solutions (and their limitations)
[What's already out there, why it's not enough]

## My Approach
[Technical overview, architecture decisions]

## Demo
[Screenshots, GIFs, or embedded video]

## Getting Started
[Installation and quick start]

## What's Next
[Roadmap, call for contributors]

## Links
- GitHub: [link]
- MCP Registry: [link]
- Twitter: [handle]
```

## Timing Strategy

### Best Days to Post

| Platform | Best Days | Best Times (UTC) |
|----------|-----------|------------------|
| Reddit | Tue-Thu | 14:00-17:00 |
| X/Twitter | Tue-Wed | 15:00-18:00 |
| LinkedIn | Tue-Wed | 10:00-12:00 |
| dev.to | Mon-Tue | 14:00-16:00 |
| HN | Tue-Thu | 14:00-16:00 |

### Launch Sequence

```
Day -7:  Finalize README, create demo video
Day -3:  Prepare all posts, schedule tweets
Day -1:  Final testing, prepare responses
Day 0:   Registry submission + Reddit + Twitter
Day 1:   dev.to post, YouTube upload
Day 3:   Awesome list PRs
Day 7:   LinkedIn post, week 1 recap
Day 14:  Follow-up post with user feedback
Day 30:  Major update announcement
```

## Engagement Best Practices

### DO

- **Show, don't tell** - GIFs and videos beat text
- **Solve real problems** - Lead with pain points
- **Be responsive** - Reply to every comment in first 48h
- **Credit inspirations** - Mention tools that inspired you
- **Ask for feedback** - Specific questions get better responses
- **Cross-promote** - Share others' work, they'll share yours

### DON'T

- **Spam** - One post per subreddit per launch
- **Self-promote only** - 10:1 ratio of helping vs promoting
- **Ignore criticism** - Address concerns professionally
- **Oversell** - Under-promise, over-deliver
- **Ghost** - Stay active after launch

## Measuring Success

### Metrics to Track

| Metric | Tool | Target (Week 1) |
|--------|------|-----------------|
| GitHub stars | GitHub | 50-100 |
| npm downloads | npm stats | 100-500 |
| Reddit upvotes | Reddit | 50+ |
| Registry listings | Manual check | 3+ registries |
| GitHub issues | GitHub | 5+ (shows engagement) |

### Success Signals

- Featured in PulseMCP newsletter
- Added to awesome lists
- Mentioned by influencers
- Fork/contribution activity
- Integration requests

## Reference Files

- `references/registry-submission-guides.md` - Step-by-step for each registry
- `references/post-templates.md` - Copy-paste templates for all platforms
- `references/timing-calendar.md` - Optimal posting schedule
- `references/community-directory.md` - Discord servers, forums, newsletters

---

**Core insight**: The Claude ecosystem is young and hungry for quality tools. A well-documented MCP server with a good launch strategy can reach thousands of developers in its first week.

**Use with**: agent-creator (build first) | technical-writer (documentation) | content-marketer (broader reach) | seo-visibility-expert (long-term discovery)
