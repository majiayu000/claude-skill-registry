---
name: create-portfolio
description: Creates professional portfolio project entries with achievement-focused content showcasing impact and technical depth. Use when adding new projects, documenting work accomplishments, or showcasing professional experience. Generates content using strong action verbs and quantifiable metrics.
---

# Portfolio Project Creation

Creates portfolio entries at `content/portfolio/project-slug/index.md` with professional, achievement-focused messaging.

## When to Use

Activate when users ask to:
- Add a new project to their portfolio
- Showcase professional work or accomplishments
- Document a completed project with technical details
- Create a case study for client work

## Required Information

Gather before generating content:

| Field | Format | Example |
|-------|--------|---------|
| **title** | String | "E-commerce Platform Redesign" |
| **client** | String | "Acme Corporation" |
| **description** | String (SEO) | "Full-stack redesign increasing conversions 40%" |
| **technologies** | Array | ["React", "Node.js", "PostgreSQL"] |
| **completion_date** | YYYY-MM | "2024-11" |
| **category** | See categories | "Web Development" |

## Optional Information

| Field | Format | Notes |
|-------|--------|-------|
| **github_url** | URL | Must be valid GitHub URL |
| **live_url** | URL | Must be valid HTTP/HTTPS URL |
| **challenges** | Array | Problems faced during project |
| **solutions** | Array | How challenges were addressed |
| **outcomes** | Array | Results and achievements |
| **metrics** | Array | Quantifiable impact data |

## Categories

Use one of these standard categories:
- Web Development
- Mobile Development
- Backend Development
- DevOps
- Data Engineering
- Software Development

## Writing Style

### Action Verbs (Required)

Start achievement statements with strong verbs:

| Primary | Secondary |
|---------|-----------|
| Led | Architected |
| Developed | Designed |
| Implemented | Built |
| Achieved | Optimized |
| Delivered | Scaled |

### Quantify Impact

Transform vague statements into measurable achievements:

| Avoid | Use Instead |
|-------|-------------|
| "Improved performance" | "Reduced load time by 40%" |
| "Many users" | "Served 10,000+ users" |
| "High volume" | "Processed 1M+ transactions daily" |
| "Faster delivery" | "Reduced deployment time from 2 hours to 15 minutes" |

### Tone Guidelines

**Do:**
- Highlight impact and technical depth
- Use metrics and quantifiable results
- Showcase problem-solving skills
- Demonstrate value delivered to clients
- Write with professional confidence

**Avoid:**
- Being overly modest or downplaying achievements
- Vague statements without specifics
- Listing responsibilities without outcomes
- Excessive technical jargon for non-technical audiences

## Generation Process

### Step 1: Gather Requirements

Ask for all required fields. For optional fields, prompt:
- "Were there specific challenges you overcame?"
- "What measurable outcomes did you achieve?"
- "Do you have a GitHub repository or live demo?"

### Step 2: Create Hugo Bundle

Generate `content/portfolio/{slug}/index.md`:

```yaml
---
title: "{title}"
date: {YYYY-MM-DD}  # Today's date
draft: true         # Always start as draft
description: "{description}"
client: "{client}"
technologies:
  - Technology1
  - Technology2
completion_date: "{YYYY-MM}"
category: "{category}"
github_url: "{optional}"
live_url: "{optional}"
---
```

### Step 3: Generate Content Sections

Structure the markdown body:

1. **Opening paragraph** - Achievement-focused overview using action verbs
2. **Project Overview** - Context and scope
3. **Challenges** (if provided) - Problems addressed
4. **Technical Solution** (if provided) - How challenges were solved
5. **Technical Implementation** - Technologies and architecture
6. **Outcomes** - Results with metrics
7. **Technologies** - Bulleted list of tech stack

### Step 4: Validate

Run validation:
```bash
node scripts/validate-portfolio-frontmatter.js
```

**Validation checks:**
- All required frontmatter fields present
- Date format: YYYY-MM-DD
- Completion date format: YYYY-MM
- Technologies is an array
- Category is a string
- URLs are valid format (if provided)
- No use of deprecated `demo_url` (use `live_url` instead)

### Step 5: Review

**Never auto-publish.** Always:
1. Present the complete draft to the user
2. Get explicit approval before changing `draft: false`
3. Offer to make revisions based on feedback

## Example Output

```markdown
---
title: "Analytics Dashboard Platform"
date: 2024-12-26
draft: true
description: "Real-time analytics platform processing 1M+ events daily with sub-second query performance"
client: "DataTech Solutions"
technologies:
  - React
  - TypeScript
  - PostgreSQL
  - Redis
completion_date: "2024-11"
category: "Web Development"
github_url: "https://github.com/example/analytics-dashboard"
live_url: "https://demo.example.com"
---

**Led** the development and delivery of a high-performance analytics dashboard for DataTech Solutions, achieving sub-second query response times while processing over 1 million events daily.

## Project Overview

Delivered a comprehensive real-time analytics platform enabling stakeholders to visualize key business metrics through interactive dashboards with customizable widgets.

## Challenges

- **Challenge 1:** Legacy system processed queries in 15+ seconds - implemented comprehensive analysis and strategic planning.
- **Challenge 2:** Data pipeline bottlenecks during peak hours - developed scalable ingestion architecture.

## Technical Solution

- **Implemented** Redis caching layer reducing database load by 70%
- **Architected** event-driven pipeline handling 10x traffic spikes
- **Designed** materialized views for complex aggregations

## Technical Implementation

This project leverages modern technologies and architectural patterns:

- **React** - Component-based dashboard UI
- **TypeScript** - Type-safe frontend development
- **PostgreSQL** - Time-series data storage
- **Redis** - Real-time caching layer

## Outcomes

- **Achieved** sub-second query performance (down from 15+ seconds)
- **Delivered** 99.9% uptime over 6 months of production use
- **Implemented** self-service dashboard creation reducing support tickets by 60%

### Key Metrics

- **Query Performance:** 15s to 200ms - 98% improvement
- **Daily Events:** 1M+ processed with zero data loss
- **User Adoption:** 500+ active users within first month

## Technologies

- **React**
- **TypeScript**
- **PostgreSQL**
- **Redis**
```

## Voice Learning

Record user feedback to improve future content generation:

```bash
# Update style documentation
# Location: .cody/project/library/style-docs/portfolio-style.json

# Fields to update based on feedback:
# - vocabulary: Add effective action verbs
# - dos: Add successful patterns
# - donts: Add patterns to avoid
```

## File Locations

| Purpose | Path |
|---------|------|
| Portfolio content | `content/portfolio/` |
| Validation script | `scripts/validate-portfolio-frontmatter.js` |
| Style documentation | `.cody/project/library/style-docs/portfolio-style.json` |
| Portfolio Agent | `src/agents/portfolio/portfolio-agent.ts` |
| Agent config | `src/agents/config/agent-config.ts` |

## Common Validation Errors

| Error | Resolution |
|-------|------------|
| Missing required field | Add the field to frontmatter |
| Invalid date format | Use YYYY-MM-DD for date |
| Invalid completion_date | Use YYYY-MM format |
| technologies not array | Convert to YAML array format |
| Use demo_url | Replace with live_url |
