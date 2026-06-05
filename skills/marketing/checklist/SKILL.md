---
name: checklist
description: Surface the right marketing checklist for any task. Covers content, SEO, ads, email, press, landing pages, launches, and technical audits. 17+ checklists indexed by task type.
---

# /checklist — The QA Gatekeeper

Surface the right checklist for any marketing task. The harness includes 17+ validation checklists — this skill maps your task to the right one and walks you through it interactively.

## Arguments

Required:
- **task**: What you're doing. Free-form — the skill maps it to the right checklist.

Examples:
- `/checklist publish a blog post`
- `/checklist launch meta ads`
- `/checklist send cold email campaign`
- `/checklist technical SEO audit`
- `/checklist launch a new product`
- `/checklist press release`

## The Skill

### Step 1: Map Task to Checklist

Match the task description against the checklist index:

| Task Keywords | Checklist File | Category |
|--------------|---------------|----------|
| blog, article, content, publish | `knowledge/checklists/content-checklist.md` | Content |
| SEO, search, ranking, optimization | `knowledge/checklists/seo-checklist.md` | SEO |
| technical SEO, crawl, audit, screaming frog | `knowledge/checklists/technical-seo-audit-sop.md` | Technical SEO |
| security, htaccess, CSP, hack | `knowledge/checklists/SEO Expert-technical-seo-checklist.md` | Technical SEO |
| meta ads, facebook, instagram, fb | `knowledge/checklists/meta-advertising-checklist.md` | Ads |
| paid, ads, PPC, campaign, google ads | `knowledge/checklists/paid-acquisition-checklist.md` | Ads |
| tiktok, TikTok Shop | `knowledge/checklists/tiktok-checklist.md` | Ads/Social |
| email, newsletter, lifecycle, drip | `knowledge/checklists/email-checklist.md` | Email |
| press, PR, media, press release | `knowledge/checklists/pr-checklist.md` | PR |
| sales page, landing page, conversion | `knowledge/checklists/perception-engineering-checklist.md` | Conversion |
| landing page, messaging, copy | `knowledge/checklists/landing-page-messaging-checklist.md` | Conversion |
| content brief, brief | `knowledge/checklists/content-brief-checklist.md` | Planning |
| fintech, payment, financial app | `knowledge/checklists/fintech-design-checklist.md` | Design |
| business model, B2B, SaaS, DTC | `knowledge/checklists/business-model-checklist.md` | Strategy |
| 2026, readiness, planning | `knowledge/checklists/2026-readiness-checklist.md` | Strategy |
| patent, research | `knowledge/checklists/patent-research-checklist.md` | Research |

If no match, show all available checklists and ask user to pick.

### Step 2: Load the Checklist

Read the matched checklist file from the knowledge base.

### Step 3: Interactive Walkthrough

Present each checklist item one at a time for the user to confirm:

```
CHECKLIST: {checklist name}
══════════════════════════════════════

Item 1 of {N}:
  [ ] {checklist item description}

  Status? (pass / fail / skip / na)
```

Track progress as user responds:

```
Progress: 8/24 items checked
  ✓ Pass:  6
  ✗ Fail:  1  ← "Missing meta description"
  ○ Skip:  1
  — N/A:   0
```

### Step 4: Generate Report

After all items are checked:

```
CHECKLIST REPORT — {checklist name}
══════════════════════════════════════

Date:     {today}
Result:   {PASS / FAIL}
Score:    {passed}/{total applicable} ({pct}%)

PASSED (6):
  ✓ Title tag present and under 60 characters
  ✓ H1 hierarchy correct
  ✓ Internal links present (3+)
  ...

FAILED (1):
  ✗ Meta description missing
    Fix: Add a meta description of 150-160 characters targeting the primary keyword.

SKIPPED (1):
  ○ Schema markup (manual check required)

RECOMMENDATION:
  Fix 1 failing item before publishing.
  Run: /content-gate {file} for automated scoring.
```

### Step 5: Offer Fixes

For each failing item, offer to fix automatically if applicable:
- Content issues → "Want me to write the meta description?"
- SEO issues → "Want me to add the missing internal link?"
- Compliance issues → "Load the policy reference for details"

## Available Checklists (Full Index)

### Content & Copy
1. **Content Checklist** — Final review before publishing any content
2. **Content Brief Checklist** — Validates brief completeness before writing
3. **Perception Engineering Checklist** — Persuasive messaging and decision installation
4. **Landing Page Messaging Checklist** — 7-phase landing page validation

### SEO
5. **SEO Checklist** — Core SEO validation (on-page, technical, links)
6. **Technical SEO Audit SOP** — Screaming Frog crawl with dev ticket templates
7. **SEO Expert Technical SEO Checklist** — Security hardening, htaccess, CSP, hack recovery

### Advertising
8. **Meta Advertising Checklist** — Meta/FB/IG campaign launch, learning phase, optimization
9. **Paid Acquisition Checklist** — Cross-platform paid campaign launch and optimization
10. **TikTok Checklist** — TikTok Shop content and ad validation

### Email
11. **Email Checklist** — Email program setup and campaign validation

### PR
12. **PR Checklist** — Press release distribution validation

### Strategy
13. **Business Model Checklist** — Model-specific marketing validation
14. **2026 Readiness Checklist** — Infrastructure and strategy readiness

### Design
15. **Fintech Design Checklist** — B2C fintech app design validation

### Research
16. **Patent Research Checklist** — Google patent research methodology

### Ad Platform Compliance (via /ad-copy)
17. **Google Ads Policy** — harness/references/google-ads-policy-reference.md
18. **Meta Ads Policy** — harness/references/meta-ads-rules.md
19. **TikTok Ads Policy** — harness/references/tiktok-ads-policy-reference.md
(+ 6 more platform policies)

## Error Handling

- **No matching checklist**: Show full index, ask user to pick
- **Checklist file missing**: "Checklist '{name}' not found. Available checklists: {list}"

## Chain State

**Standalone:** Works independently for any task
**Pairs with:** `/content-gate` (automated scoring), `/ad-copy` (compliance checking)
