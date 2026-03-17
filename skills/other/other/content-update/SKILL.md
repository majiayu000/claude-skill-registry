---
name: content-update
description: |
  Streamlined bilingual content updates for young-personal-site.
  Auto-activates on content modification keywords with dual-language consistency checks.
activation-keywords: [更新內容, 新增專案, 加作品, 修改文案, 翻譯, update content, add project, speaking event]
priority: high
allowed-tools: [Read, Edit, Write, Bash, Grep, Glob]
---

# Content Update Skill

## Purpose
Ensure bilingual content consistency when updating website content.

**Prevents**: Missing translations, broken images, inconsistent keys
**Ensures**: Synchronized zh-TW/en content, optimized images, tested updates

---

## Content Locations

| Type | Translation Path | Component | Images |
|------|-----------------|-----------|--------|
| Projects | `projects.items[]` | `app/[locale]/projects/page.tsx` | `public/images/projects/` |
| Speaking | `speaking.events[]` | `app/[locale]/speaking/page.tsx` | `public/images/speaking/` |
| About | `about.*` | `app/[locale]/about/page.tsx` | - |
| Services | `services.*` | `app/[locale]/services/page.tsx` | - |

---

## Core Workflow

### 1. Add New Project

```yaml
Steps:
  1. Gather info: name, description, category, image, year (both languages)
  2. Update messages/zh-TW.json → projects.items[]
  3. Update messages/en.json → projects.items[]
  4. Add image to public/images/projects/ (< 500KB, optimized)
  5. Verify: keys match, paths identical
  6. Test: npm run dev → check both /zh-TW/projects and /en/projects
  7. Commit: "feat: add [project name]"
```

**Example**:
```json
// messages/zh-TW.json
{
  "projects": {
    "items": [
      {
        "title": "Duotopia 多鄰國風格學習平台",
        "description": "仿照 Duolingo 的遊戲化學習平台",
        "category": "教育科技",
        "image": "/images/projects/duotopia-banner.jpg",
        "year": "2024"
      }
    ]
  }
}

// messages/en.json (mirror structure)
{
  "projects": {
    "items": [
      {
        "title": "Duotopia - Gamified Learning Platform",
        "description": "A Duolingo-inspired gamified learning platform",
        "category": "EdTech",
        "image": "/images/projects/duotopia-banner.jpg",
        "year": "2024"
      }
    ]
  }
}
```

### 2. Add Speaking Event

```yaml
Steps:
  1. Gather: name, date, location, description, type, image (both languages)
  2. Update speaking.events[] in both translation files
  3. Add slug to app/[locale]/speaking/[slug]/page.tsx validSlugs array
  4. Add image to public/images/speaking/
  5. Test: list page + detail page (both languages)
  6. Commit: "feat: add [event name] speaking event"
```

### 3. Update About/Services Content

```yaml
Steps:
  1. Identify section: about.hero, about.intro, services.consulting, etc.
  2. Update both zh-TW.json and en.json
  3. Test: /zh-TW/about and /en/about
  4. Commit: "docs: update [section] content"
```

---

## Translation Guidelines

### Terminology Consistency
```
教育科技 = EdTech
企業內訓 = Corporate Training
工作坊 = Workshop
演講 = Talk/Speech
顧問服務 = Consulting Services
```

### Tone Standards
- **zh-TW**: 專業但親和 (Professional yet approachable)
- **en**: Professional and clear

### Image Optimization
```yaml
Requirements:
  - File size: < 500KB
  - Format: JPEG (photos, 80-85% quality), PNG (logos/graphics)
  - Dimensions: Max 1920px width, min 800px width
  - Naming: Descriptive (duotopia-banner.jpg, not IMG_1234.jpg)
  - Aspect ratio: 16:9 or 4:3
```

---

## Validation Checklist

**Before committing**:
```markdown
Content:
- [ ] zh-TW translation complete
- [ ] en translation complete
- [ ] Keys match exactly in both files
- [ ] Image paths identical

Images:
- [ ] Optimized (< 500KB)
- [ ] Correct directory (public/images/[type]/)
- [ ] Paths match translation files

Testing:
- [ ] npm run dev successful
- [ ] zh-TW page displays correctly
- [ ] en page displays correctly
- [ ] Language switcher works
- [ ] Images load properly
- [ ] Mobile responsive
- [ ] npm run build passes

Deployment:
- [ ] Clear commit message
- [ ] Push to main (auto-deploys to Vercel)
```

---

## Common Scenarios

### Quick Text Fix
```
User: "修改關於頁面的自我介紹"
→ Read both translation files
→ Update zh-TW intro
→ Update en intro (ask user or translate)
→ Test both languages
→ Commit: "docs: update about page intro"
```

### Bulk Project Addition
```
User: "新增 3 個專案：A, B, C"
→ Gather info for all 3 (batch)
→ Update zh-TW.json (add all 3)
→ Update en.json (add all 3)
→ Add images
→ Test all projects
→ Commit: "feat: add projects A, B, and C"
```

### Image Optimization
```
User: "專案圖片太大"
→ Identify large images (> 500KB)
→ Optimize (80-85% JPEG quality)
→ Verify paths unchanged
→ Commit: "perf: optimize project images"
```

---

## Anti-Patterns

### ❌ Updating Only One Language
```json
// zh-TW.json has new project, en.json missing → English version breaks
```

### ❌ Mismatched Image Paths
```json
// zh-TW: "/images/project-banner.jpg"
// en: "/images/projects/banner.jpg" → Image missing in one language
```

### ❌ Inconsistent Keys
```json
// zh-TW: projects.list[]
// en: projects.items[] → Translation system breaks
```

---

## Integration

- **i18n-sync**: Validates translation consistency after updates
- **design-improvement**: Content + design updates together
- **deploy-check**: Pre-deployment content verification

---

**Version**: v1.1 | **Updated**: 2025-12-31
**Project**: young-personal-site
