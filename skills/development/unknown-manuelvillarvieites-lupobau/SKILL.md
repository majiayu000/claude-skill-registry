---
name: website-builder
description: Website sitemap generation workflow. Analyzes requirements, delegates to sitemap-analyst agent, generates sitemap with shadcn-ui-blocks component selections. Use when planning website architecture, structuring pages, selecting components, or requesting sitemap/page structure planning.
version: 2.0.0
dependencies: sitemap-analyst agent, shadcn-ui-blocks skill, sitemap-pages skill
allowed-tools: Read
---

# Website Sitemap Generator

Generates website architecture with intelligent shadcn-ui-blocks component selection. Output: Markdown sitemap with copy-paste pnpm commands.

---

## WORKFLOW

**Triggered by:** User request for website sitemap/architecture planning

**References:** `.claude/docs/prompts/website-build/01-sitemap.md`

### Process

1. **Gather Requirements**
   - Business name, industry, target audience
   - Goals and objectives
   - Required pages (homepage, about, services, contact, etc.)
   - Brand voice and values

2. **Delegate to sitemap-analyst Agent**
   - Agent model: `sonnet` (architecture/reasoning)
   - Agent reads:
     - `.claude/skills/sitemap-pages/` → Page templates
     - `.claude/skills/shadcn-ui-blocks/docs/` → Block descriptions
   - Agent matches sections to **best-fit blocks** (NOT sequential)
   - Agent generates `pnpm dlx shadcn add` commands

3. **Output**
   - File: `.claude/planning/[project]/sitemap.md`
   - Format: Markdown
   - Contains:
     - Page structure (routes, sections)
     - Selected shadcn-ui-blocks with reasons
     - Copy-paste ready pnpm commands
     - Internal linking strategy
     - User journeys

### Example Sitemap Output

```markdown
# Sitemap: Local Studios

## 1. Homepage (/)
**Template:** sitemap-pages/pages/homepage.md

### Sections

**Hero Section**
- Block: @shadcnblocks/hero-18
- Reason: Clean CTA with background video support
- Command: `pnpm dlx shadcn add @shadcnblocks/hero-18`

**Features Grid**
- Block: @shadcnblocks/feature-12
- Reason: Icon-based 3-column layout, perfect for services
- Command: `pnpm dlx shadcn add @shadcnblocks/feature-12`
```

---

## Next Steps

After receiving sitemap.md, user should:

1. **Execute Commands**
   - Run each `pnpm dlx shadcn add` command
   - Downloads shadcn-ui-blocks to project

2. **Manual Integration**
   - Insert downloaded blocks into page files
   - Create `global.css` with theme/colors

3. **Optional Workflows** (separate prompts):
   - `02-unsplash.md` → Integrate stock images
   - `03-animation.md` → Add mikroanimations
   - `04-seo.md` → SEO optimization
   - `05-midjourney.md` → Generate AI image prompts

---

## Keywords to Trigger This Skill

Primary: sitemap, website architecture, page structure, website planning
Secondary: site structure, information architecture, component selection, page planning

---

## Integration Summary

| Component | Purpose |
|-----------|---------|
| sitemap-analyst | Generates sitemap with block selections (Model: sonnet) |
| sitemap-pages | Provides page templates/structures |
| shadcn-ui-blocks | 929 pre-built components library |

---

## Example Request Triggers

- "Create a sitemap for my website"
- "Plan website architecture"
- "Generate page structure with component selections"
- "Help me structure my site pages"
- "Build a sitemap with shadcn blocks"

---

## Output Artifact

User receives:

`.claude/planning/[project]/sitemap.md` containing:
- Page hierarchy (routes, sections)
- Selected shadcn-ui-blocks with reasons
- Copy-paste ready `pnpm dlx shadcn add` commands
- Internal linking strategy
- User journey mapping

---

**Note:** This skill now focuses ONLY on sitemap generation. SEO, animations, and image integration are handled by separate optional workflow prompts.
