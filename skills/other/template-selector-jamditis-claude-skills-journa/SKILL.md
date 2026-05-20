---
name: template-selector
description: Choose the correct CLAUDE.md or LESSONS.md template for journalism projects. Use when starting a new project, setting up documentation, or unsure which template category fits best. Provides decision trees and selection guidance for 6 journalism-focused template types.
---

# Template selector

Match projects to the correct template category. Don't guess—use the decision tree.

## Quick reference

| Project type | Template category |
|-------------|-------------------|
| Newsroom AI tool, fact-checker | editorial-tool |
| Conference, summit, workshop | event-website |
| Newsletter, podcast, blog | publication |
| Investigation, data journalism | research-project |
| CMS workflow, syndication | content-pipeline |
| Historical collection, archive | digital-archive |

## Decision tree

```
Is it for journalism/publishing?
├── Yes →
│   ├── Has specific end date/event? → event-website
│   ├── Ongoing content series? → publication
│   ├── Historical/preservation? → digital-archive
│   ├── Newsroom tool/AI? → editorial-tool
│   ├── CMS/automation? → content-pipeline
│   └── Investigation with scope? → research-project
│
└── No (general software) →
    Use general template or another collection
```

## Detailed category descriptions

### editorial-tool
**Use when:** Building newsroom tools, writing assistants, fact-checkers, AI-powered research tools, moderation systems, workflow automation for journalists

**Not for:** Generic productivity tools, non-journalism software

**Signs it's an editorial tool:**
- Primary users are journalists, editors, or producers
- Helps with a specific editorial workflow step
- Requires accuracy/trust for publication decisions

### event-website
**Use when:** Building sites for conferences, summits, workshops, or events with specific dates

**Not for:** Ongoing content, organization websites without events, event management software (that's editorial-tool)

**Signs it's an event website:**
- Has a specific event date (or date range)
- Registration/attendance is involved
- Content includes speakers, schedule, venue info

### publication
**Use when:** Building newsletters, podcasts, blogs, magazines, or ongoing content series with regular publishing schedule

**Not for:** One-off articles, static content sites, CMSes that power publications (that's editorial-tool)

**Signs it's a publication:**
- Regular publishing cadence (daily, weekly, monthly)
- Growing subscriber/reader base
- Consistent voice and format

### research-project
**Use when:** Building investigative journalism projects, data journalism, analysis with defined scope and end date

**Not for:** Ongoing research operations, general data analysis, tools that support research (that's editorial-tool)

**Signs it's a research project:**
- Answers a specific question or hypothesis
- Has a defined end point (publication date)
- Involves data collection, analysis, and findings

### content-pipeline
**Use when:** Building CMS workflows, publishing automation, content syndication systems, feed aggregators, cross-posting tools

**Not for:** Manual publishing workflows, single-site content management, publications themselves

**Signs it's a content pipeline:**
- Automates content movement between systems
- Transforms content formats
- Handles scheduling and distribution

### digital-archive
**Use when:** Building historical collections, preservation projects, research databases, document repositories

**Not for:** Active news sites, CMS platforms, search engines

**Signs it's a digital archive:**
- Primary focus is preservation
- Collection has defined scope (time period, topic)
- Users are researchers, historians, or the public seeking historical content

## Common mistakes

| Project | Wrong choice | Right choice | Why |
|---------|-------------|--------------|-----|
| Newsletter dashboard | editorial-tool | publication | It's about the publication, not the tech |
| AI fact-checker | research-project | editorial-tool | It's a tool, not a one-off investigation |
| Event registration system | event-website | editorial-tool | It's a tool that serves events |
| Podcast website | content-pipeline | publication | It's a publication, not automation |
| Document search tool | digital-archive | editorial-tool | It's a tool, not the archive itself |
| FOIA tracking system | research-project | editorial-tool | It's a tool that supports research |

## The litmus test

If you're still unsure, ask:

1. **Is this a tool that helps journalists do X, or is this X itself?**
   - Tool → editorial-tool
   - The thing itself → other categories

2. **Does it have a specific end date?**
   - Yes, event dates → event-website
   - Yes, publication date → research-project
   - No, ongoing → publication, content-pipeline, or digital-archive

3. **Is preservation the primary goal?**
   - Yes → digital-archive
   - No → other categories

## Using templates

### For project memory (CLAUDE.md)
1. Identify project category using decision tree above
2. Copy appropriate template from `project-memory/templates/`
3. Fill in bracketed placeholders with your specifics
4. Delete sections that don't apply
5. Add project-specific gotchas as you discover them

### For retrospectives (LESSONS.md)
1. Identify project category
2. Copy appropriate template from `project-retrospective/templates/`
3. Fill in as the project progresses or at completion
4. Be specific about failures—that's the valuable part

## Template locations

```
claude-skills-journalism/
├── project-memory/templates/
│   ├── editorial-tool.md
│   ├── event-website.md
│   ├── publication.md
│   ├── research-project.md
│   ├── content-pipeline.md
│   └── digital-archive.md
│
└── project-retrospective/templates/
    ├── editorial-tool.md
    ├── event.md
    ├── publication.md
    └── research-project.md
```

---

*Pick the specific template that fits. "General" is a last resort.*
