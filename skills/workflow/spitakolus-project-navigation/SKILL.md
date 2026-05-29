---
name: spitakolus-project-navigation
description: Navigate Spitakolus repos correctly. Know which repo you're in, follow deployment rules, find documentation, and align work with the AI Growth Loop vision.
dependencies: []
---

# Spitakolus Project Navigation

## ⚠️ CRITICAL: Which Repo Am I In?

**ALWAYS check first:**
- `flocken-website` → flocken.info (dog app)
- `nastahem` → nastahem.com (real estate)
- `spitakolus` → shared documentation only

**NEVER:**
- Deploy to wrong site
- Put Flocken docs in nastahem (or vice versa)
- Commit without knowing which repo

---

## 🚀 Deployment Rules

### flocken-website
```bash
git push raquel main  # NOT origin!
```
Vercel is connected to RaquelSandblad/flocken-website

### nastahem
```bash
git commit --author="RaquelSandblad <raquel.sandblad@hotmail.com>" -m "msg"
git push origin main
```

### spitakolus
```bash
git push origin main  # Documentation only
```

---

## 📁 Documentation Structure

### Shared (spitakolus)
- `AI_ONBOARDING.md` - Quick start for AI
- `DOCUMENTATION_RULES.md` - How to document
- `tracking/` - GTM, BigQuery, GA4
- `meta-ads/` - Naming conventions
- `development/` - Standards, templates

### Project-specific
Each repo has:
- `README.md` - With warning about which repo
- `DOCUMENTATION_MAP.md` - Complete overview

---

## 🎯 Strategic Vision: AI Growth Loop

**ALL work should align with building toward this vision:**

### The Goal
A fully automated system that:
1. **Collects** performance data from Meta + BigQuery
2. **Analyzes** what's working (copy, images, placements)
3. **Generates** new copy with AI (GPT-4)
4. **Creates** new images with AI (DALL-E/Imagen)
5. **Launches** new ads automatically via Meta API
6. **Pauses** underperforming ads
7. **Reports** results daily

### Implementation Phases

**Phase 1 (Current):** Semi-automated
- Manual copy generation → automated image + ad creation

**Phase 2:** Data-driven
- Automated performance analysis → AI copy generation

**Phase 3:** Fully autonomous
- 95% automated, only weekly human oversight

### When Making Decisions, Ask:
- "Does this move us toward the automated growth loop?"
- "Can this be automated later?"
- "Are we building reusable components?"
- "Is this data being captured for future analysis?"

---

## 📊 Shared Infrastructure

| System | ID | Purpose |
|--------|-----|---------|
| GTM Web | GTM-PD5N4GT3 | Shared container, hostname routing |
| GTM Server | gtm.nastahem.com | Server-side tracking |
| BigQuery | nastahem-tracking | Data warehouse |
| GA4 Flocken | G-7B1SVKL89Q | Flocken analytics |
| GA4 Nästa Hem | G-7N67P0KT0B | Nästa Hem analytics |

---

## ✅ Before Starting Any Task

1. **Verify repo:** Which project am I in?
2. **Pull latest:** `git pull origin main`
3. **Check docs:** Read DOCUMENTATION_MAP.md
4. **Align with vision:** Does this support the growth loop?
5. **Document:** Update docs when done

---

## 🔗 Key URLs

- Flocken: https://flocken.info
- Nästa Hem: https://nastahem.com
- Spitakolus docs: https://github.com/tbinho/spitakolus
