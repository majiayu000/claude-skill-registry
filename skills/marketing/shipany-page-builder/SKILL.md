---
name: shipany-page-builder
description: "创建**全新动态页面**或优化现有页面的 SEO（主要针对英文或初始页面）。输入：关键词、路由/路径、参考内容。使用场景：(1) 从简短规格创建全新页面（关键词、路由、参考内容），(2) 增强现有页面内容以改善 SEO（添加章节、改进文案、扩展 FAQ），(3) 用户说'创建页面'、'优化页面 SEO'、'添加章节'，(4) 为新功能或产品创建落地页，(5) 创建英文源页面（后续可用 auto-i18n 国际化）。**不要用于：**(a) 国际化工作流（用 auto-i18n 创建或 i18n-content-audit 审计），(b) 审计现有i18n内容质量（用 i18n-content-audit），(c) 修复已有i18n页面的关键词问题（用 i18n-content-audit --fix），(d) 批量翻译页面（用 auto-i18n）。**核心功能：**创建新页面和内容优化，支持英文和非i18n场景，不处理国际化工作流。"
---

# ShipAny Page Builder (Dynamic Pages)

## 🚨 BLOCKING REQUIREMENTS - Execute in Order

**Two modes available:**
- **Create New Page:** Build from scratch with keywords and route
- **Optimize Existing Page:** Enhance SEO, add sections, improve copy

**You MUST complete each checkpoint before proceeding. Do NOT skip any step.**

---

## 📝 PRE-EXECUTION: Normalize Input

**BLOCKING REQUIREMENT:** MUST normalize user request into structured input first.

Extract and confirm:
- `route`: `/features/ai-image-generator`
- `slug`: `features/ai-image-generator`
- `keywords`: ["AI image generator", "create AI art", ...]
- `locale`: en (or zh, ja, ko, etc.)
- `mode`: create-new OR optimize-existing

**Confirm by stating:**
"📝 INPUT NORMALIZED: route={route}, slug={slug}, {N} keywords, locale={locale}, mode={mode}"

**Input guide:** See [references/00-guide.md](references/00-guide.md)

---

## ✅ CHECKPOINT 1: Load and Validate Keywords

**BLOCKING REQUIREMENT:** For non-EN pages, MUST load validated keywords FIRST.

**For EN pages:** Skip to Checkpoint 2

**For non-EN pages (zh, ja, ko, etc.):**
```bash
Read: .claude/skills/i18n-seo-localizer/data/keywords-{locale}.json
# OR: .codex/skills/i18n-seo-localizer/data/keywords-{locale}.json
```

**Extract validated keywords:**
- `primary` → Use in: Title, H1, Meta description
- `alternatives` → Use in: H2s, body content, FAQ
- `semanticVariants`, `relatedTerms`, `longTail` → Use for diversity

**If keyword NOT found in data file:**
1. ⛔ STOP - Do not generate with guessed keywords
2. Research using cumulative SERP analysis
3. Add to keywords-{locale}.json
4. Then proceed

**Confirm completion by stating:**
"✅ CHECKPOINT 1 COMPLETE: Loaded validated keywords for {locale}, primary='{keyword}', {N} alternatives"

---

## ✅ CHECKPOINT 2: Generate/Optimize Content with SEO Standards

**BLOCKING REQUIREMENT:** Content MUST follow unified SEO standards.

**SEO Standards:** See `../_shared/references/seo-standards.md` for complete requirements.

**Quick requirements:**
- **Word count:** EN 800+, ZH 500+, JA/KO 600+, European 800+
- **Keyword density:** ZH 2.0-3.0%, EN/European 1.8-2.5%, JA/KO 2.0-2.8%
- **H1 rule (one-vote veto):** MUST contain primary keyword
- **H2 distribution:** 2-4 with keywords, primary ≤50%
- **H3 distribution:** Primary ≤30% (recommended, not blocking)

**Generation steps:**
1. **Generate headings FIRST**
   - H1 (1): Must contain primary keyword
   - H2 (2-4): Mix of primary + variants
   - H3 (0-6): Mostly variants
2. **Self-verify headings immediately**
3. **Generate body content** (based on verified headings)
4. **Create sections** (hero, benefits, features, FAQ, CTA)
5. **Optimize metadata** (title, description)

**For new pages:** Create multi-locale JSON files

**For existing pages:** Modify JSON to enhance content

**Confirm completion by stating:**
"✅ CHECKPOINT 2 COMPLETE: Generated {word_count} words, density {X}%, H1 check: pass"

**Complete SEO guidelines:** See [references/02-seo-best-practices.md](references/02-seo-best-practices.md)

---

## ✅ CHECKPOINT 3: Run Quality Validation (Gate 0)

**BLOCKING REQUIREMENT:** MUST run anti-stuffing detection script.

```bash
python scripts/check_keyword_quality.py \
  --file {generated_file} \
  --keyword {primary_keyword} \
  --locale {locale}
```

**Checks performed:**
- 🚨 H1 contains primary keyword (one-vote veto)
- 🚨 H2 distribution reasonable (2-4 with keywords, primary ≤50%)
- ℹ️  H3 distribution (primary ≤30%, warning only)
- ✅ Keyword spacing ≥ 50 chars (CN) / 200 chars (EN)
- ✅ Paragraph repetition ≤ 1 per paragraph
- ✅ No unnatural patterns ("X是X", "X的X")
- ✅ Readability ≥ 60

**If detection fails:** Auto-rewrite (max 3 times). Do NOT bypass this check.

**Confirm completion by stating:**
"✅ CHECKPOINT 3 COMPLETE: Quality check passed, exit code 0"

---

## ✅ CHECKPOINT 4: Register Page and Update Config

**BLOCKING REQUIREMENT:** For new pages, MUST register path and update configs.

**For new pages:**

1. **Register message path:**
   ```bash
   python scripts/create_dynamic_page.py {slug} {locale}
   ```
   OR manually update `src/config/locale/index.ts`

2. **Update sitemap config:**
   Add entry to `src/config/sitemap-config.ts`
   See [references/05-sitemap-config.md](references/05-sitemap-config.md)

3. **Configure internal linking (for L2+ pages):**
   Update `internal-links.json` for navigation
   See [references/07-internal-linking.md](references/07-internal-linking.md)

**For existing page optimization:**
- Update sitemap-config.ts `localeLastmod` to today

**Confirm completion by stating:**
"✅ CHECKPOINT 4 COMPLETE: Registered path, updated sitemap and internal links"

---

## ✅ CHECKPOINT 5: Validate Build

**BLOCKING REQUIREMENT:** Build MUST pass without errors.

```bash
pnpm build
```

**Confirm completion by stating:**
"✅ CHECKPOINT 5 COMPLETE: Build passed successfully"

**If build fails:** Fix errors and rebuild. Do NOT mark complete until build passes.

---

## 📋 Quick Reference

**Edit Scope:**
- ✅ Create/modify: Page JSON files, locale index, sitemap config
- ❌ Do NOT touch: Theme blocks, core components, shared utilities, images in `public/`

**Safety Constraints:**
- Only use placeholder images in JSON
- Preserve existing functionality when optimizing
- Do NOT remove functional sections without user approval

**Content Exclusions:**
- ❌ Do NOT include: metadata.keywords, footer.friendLinks, backlinks

**i18n Development (CRITICAL):**
Always use explicit locale in getTranslations():
```typescript
// CORRECT
const t = await getTranslations({ locale, namespace: 'pages.xxx' });
```
See [references/04-i18n-best-practices.md](references/04-i18n-best-practices.md)

---

## 🔄 Complete Workflow Documentation

**Input Guide:** [references/00-guide.md](references/00-guide.md)
**Validation Checklist:** [references/01-checklist.md](references/01-checklist.md)
**SEO Best Practices:** [references/02-seo-best-practices.md](references/02-seo-best-practices.md)
**i18n Development:** [references/04-i18n-best-practices.md](references/04-i18n-best-practices.md)
**Sitemap Config:** [references/05-sitemap-config.md](references/05-sitemap-config.md)
**SEO Quality Pipeline:** [references/06-seo-quality-pipeline.md](references/06-seo-quality-pipeline.md)
**Internal Linking:** [references/07-internal-linking.md](references/07-internal-linking.md)

---

## 🆚 Skill Boundaries

| Task | Use This Skill? | Alternative |
|------|----------------|-------------|
| Create new EN page | ✅ Yes | - |
| Create new non-EN page | ✅ Yes (if keyword validated) | auto-i18n (if translating from EN) |
| Optimize existing EN page | ✅ Yes | - |
| Translate EN → other language | ❌ No | auto-i18n |
| Audit existing i18n content | ❌ No | i18n-content-audit |
| Fix i18n quality issues | ❌ No | i18n-content-audit --fix |

---

**Last Updated:** 2026-02-03
