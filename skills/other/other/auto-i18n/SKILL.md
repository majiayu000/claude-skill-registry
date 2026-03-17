---
name: auto-i18n
description: "自动将**已有英文页面**国际化到目标语言。输入：英文页面路径和目标语言区域。执行关键词研究（使用已验证的语言区域数据，而非翻译）、带反堆砌检测的内容生成、质量审核和站点地图更新。使用场景：(1) 为已有英文页面创建新的国际化内容，(2) 用户说'将此页面国际化/翻译到[语言]'或'i18n for [locale]'，(3) 用户提供页面路径 + 语言区域，(4) 批量生成多语言版本。**不要用于：**(a) 审计/检查现有国际化内容（用 i18n-content-audit），(b) 创建全新页面（用 shipany-page-builder），(c) 优化英文源页面SEO（用 shipany-page-builder 或其他SEO技能），(d) 修复国际化内容的质量问题（用 i18n-content-audit --fix）。**核心功能：**创建新的国际化内容，不是审计或优化已有内容。"
---

# Auto i18n - Automated Page Internationalization

## 🚨 BLOCKING REQUIREMENTS - Execute in Order

**You MUST complete each checkpoint before proceeding to the next. Do NOT skip any step.**

### ✅ CHECKPOINT 1: Load Validated Keywords (MANDATORY FIRST STEP)

**BLOCKING REQUIREMENT:** You MUST read the keyword data file BEFORE doing ANYTHING else.

```bash
Read: .claude/skills/i18n-seo-localizer/data/keywords-{locale}.json
# OR: .codex/skills/i18n-seo-localizer/data/keywords-{locale}.json
```

**Confirm completion by stating:**
"✅ CHECKPOINT 1 COMPLETE: Loaded keywords for {locale}, found {N} keywords for {topic}"

**If file not found:** STOP and alert user that keyword file is missing.

**Complete workflow:** See [references/phase-1-research.md](references/phase-1-research.md) - MUST read and execute ALL steps.

---

### ✅ CHECKPOINT 2: Generate Content with Validated Keywords

**BLOCKING REQUIREMENT:** Content generation is MULTI-STEP, NOT single-shot.

**Step 2.1: Generate Headings FIRST**
- H1: MUST contain primary keyword (one-vote veto rule)
- H2: 2-4 headings with keywords, primary ≤50%
- H3: Optional, primary ≤30%

**Step 2.2: Self-Verify Headings IMMEDIATELY**
State: "H1 check: [pass/fail], H2 distribution: [X/4 with keywords, Y% primary]"

**Step 2.3: Generate Body Content**
Only proceed after headings are verified.

**Confirm completion by stating:**
"✅ CHECKPOINT 2 COMPLETE: Generated {word_count} words, density {X}%"

**Complete workflow:** See [references/phase-2-generate.md](references/phase-2-generate.md) - MUST read and execute ALL steps.

---

### ✅ CHECKPOINT 3: Run Quality Validation

**BLOCKING REQUIREMENT:** MUST run anti-stuffing detection script.

```bash
python scripts/check_keyword_quality.py \
  --file {generated_file} \
  --keyword {primary_keyword} \
  --locale {locale}
```

**If script fails:** Auto-rewrite (max 3 times). Do NOT bypass this check.

**Confirm completion by stating:**
"✅ CHECKPOINT 3 COMPLETE: Quality check passed, all gates green"

**Complete workflow:** See [references/phase-3-review.md](references/phase-3-review.md) - MUST read and execute ALL steps.

---

### ✅ CHECKPOINT 4: Update Sitemap Config (MANDATORY)

**BLOCKING REQUIREMENT:** MUST update sitemap-config.ts.

Update `localeLastmod` for the target locale to today's date.

**Confirm completion by stating:**
"✅ CHECKPOINT 4 COMPLETE: Updated sitemap-config.ts for {locale}"

---

## 📋 Quick Reference

**Supported Locales:** zh, zh-TW, ja, ko, de, es, fr, pt, it, ar, id, ru, hi

**SEO Standards:** See `../_shared/references/seo-standards.md`

**Safety Constraints:**
- ✅ Only modify: Target locale JSON files, sitemap-config.ts
- ❌ Do NOT modify: UI components, routing, layouts, other language files

**Content Exclusions:**
- ❌ Do NOT include: metadata.keywords, footer.friendLinks, backlinks

---

## 🔄 Complete Workflow Documentation

**Phase 1 (Research):** [references/phase-1-research.md](references/phase-1-research.md)
**Phase 2 (Generate):** [references/phase-2-generate.md](references/phase-2-generate.md)
**Phase 3 (Review):** [references/phase-3-review.md](references/phase-3-review.md)

**Examples:** [references/examples.md](references/examples.md)
**Troubleshooting:** [references/troubleshooting.md](references/troubleshooting.md)

---

## ⚠️ Core Principle

> **Every keyword must be researched and validated, not translated.**

Direct translation is FORBIDDEN. Machine-translated keywords have 5-10x lower search volume.

**Why:** "AI image generator" → "AI绘画" (NOT "AI图像生成器")

---

**Last Updated:** 2026-02-03
