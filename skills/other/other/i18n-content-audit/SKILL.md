---
name: i18n-content-audit
description: "审计和优化**已有国际化内容**的 SEO/GEO 合规性。两种模式：(1) 仅报告（默认，无 --fix 标志）：生成审计报告但不修改文件，适合想先审查建议的场景；(2) 报告 + 修复（--fix 标志）：生成报告并自动应用优化，适合自动修复质量问题的场景。输入：语言区域和页面路径。输出：包含关键词分析、质量评分和建议的综合报告。使用场景：(1) 审查现有国际化内容质量，(2) 用户说'audit/optimize/check SEO/review i18n quality'，(3) 验证内容是否符合质量标准，(4) 审计由 auto-i18n 创建的内容，(5) 修复关键词堆砌/密度问题。**不要用于：**(a) 创建新的国际化内容（用 auto-i18n），(b) 首次国际化英文页面（用 auto-i18n），(c) 审计英文源页面（用其他SEO审计技能），(d) 创建全新页面（用 shipany-page-builder）。**核心功能：**检查和优化已有i18n内容，不是创建新内容。"
---

# i18n Content Audit - SEO & GEO Content Optimization

## 🚨 BLOCKING REQUIREMENTS - Execute in Order

**Two modes available:**
- **Report-Only (default):** Audit and report, no file modifications
- **Report + Fix (`--fix`):** Audit, report, and automatically apply optimizations

**You MUST complete each checkpoint before proceeding. Do NOT skip any step.**

---

## 🔹 REPORT-ONLY MODE (Default)

### ✅ CHECKPOINT 1: Load Validated Keywords & Analyze Content

**BLOCKING REQUIREMENT:** You MUST read the keyword data file BEFORE analyzing content.

```bash
Read: .claude/skills/i18n-seo-localizer/data/keywords-{locale}.json
# OR: .codex/skills/i18n-seo-localizer/data/keywords-{locale}.json
```

**Then read target content:**
```bash
Read: src/config/locale/messages/{locale}/{page-path}.json
```

**Confirm completion by stating:**
"✅ CHECKPOINT 1 COMPLETE: Loaded keywords and content for {locale}/{page}, extracted {N} current keywords"

**Complete workflow:** See [references/phase-1-analyze.md](references/phase-1-analyze.md) - MUST read and execute ALL steps.

---

### ✅ CHECKPOINT 2: Evaluate Quality Across All Dimensions

**BLOCKING REQUIREMENT:** Evaluate ALL quality dimensions, do NOT skip any.

**Evaluate in order:**
1. **Title & Description** - Length, keyword placement, readability
2. **E-E-A-T Score** - Target ≥ 18/27
3. **GEO Score** - Target ≥ 30/40
4. **Keyword Density** - Within language-specific healthy range
5. **Word Count** - Meets minimum for target language
6. **Seven Sweeps** - Clarity, flow, engagement
7. **Content Exclusions** - No forbidden elements

**Confirm completion by stating:**
"✅ CHECKPOINT 2 COMPLETE: Evaluated all dimensions, overall grade: {A/B/C/D/F}"

**Complete workflow:** See [references/phase-2-evaluate.md](references/phase-2-evaluate.md) - MUST read and execute ALL steps.

**Scoring methodology:** See [references/scoring-guide.md](references/scoring-guide.md)

---

### ✅ CHECKPOINT 3: Generate Comprehensive Report

**BLOCKING REQUIREMENT:** Report MUST include all required sections.

**Required report sections:**
1. Executive Summary (Overall Grade)
2. Keyword Analysis (current vs validated)
3. Title & Description Audit
4. E-E-A-T Assessment (with score)
5. GEO Assessment (with score)
6. Seven Sweeps Results
7. Content Exclusion Check
8. Action Items (priority order)
9. Recommended Rewrites
10. Next Steps

**Confirm completion by stating:**
"✅ CHECKPOINT 3 COMPLETE: Generated comprehensive report with {N} recommendations"

**Report template:** See [references/phase-3-report.md](references/phase-3-report.md) - MUST follow template structure.

---

### ✅ CHECKPOINT 4: Provide Optimization Recommendations

**BLOCKING REQUIREMENT:** Recommendations MUST be specific and actionable.

**Deliverables:**
- Optimized title and description (exact text)
- Section-by-section improvements (specific changes)
- Implementation priority (high/medium/low)
- Expected impact estimation (traffic, ranking)

**Confirm completion by stating:**
"✅ CHECKPOINT 4 COMPLETE: Provided {N} actionable recommendations"

**Complete workflow:** See [references/phase-4-recommend.md](references/phase-4-recommend.md) - MUST read and execute ALL steps.

---

## 🔸 REPORT + FIX MODE (`--fix` flag)

**Execute Checkpoints 1-4 first, then proceed to Checkpoint 5.**

### ✅ CHECKPOINT 5: Apply Optimizations (Only with --fix)

**BLOCKING REQUIREMENT:** MUST apply ALL recommended fixes, not selective.

**Fix steps (in order):**
1. Keyword rewriting (using validated data)
2. Title & Description optimization
3. Content optimization (E-E-A-T, GEO)
4. Copy quality refinement (Seven Sweeps)
5. Content exclusion cleanup
6. Apply changes to JSON file
7. Update sitemap-config.ts
8. Verify build passes
9. Generate fix summary

**Confirm completion by stating:**
"✅ CHECKPOINT 5 COMPLETE: Applied all fixes, build passes, {N} improvements made"

**Complete workflow:** See [references/phase-5-fix.md](references/phase-5-fix.md) - MUST read and execute ALL steps.

---

## 📋 Quick Reference

**SEO Standards:** See `../_shared/references/seo-standards.md`

**Quality Targets:**
- Word count: EN 800+, ZH 500+, JA/KO 600+, European 800+
- Keyword density: ZH 2.0-3.0%, EN/European 1.8-2.5%, JA/KO 2.0-2.8%
- E-E-A-T: ≥ 18/27
- GEO: ≥ 30/40

**Content Exclusions:**
- ❌ Do NOT include: metadata.keywords, footer.friendLinks, backlinks

**Complete checklist:** See [references/audit-checklist.md](references/audit-checklist.md)

---

## 🔄 Complete Workflow Documentation

**Phase 1 (Analyze):** [references/phase-1-analyze.md](references/phase-1-analyze.md)
**Phase 2 (Evaluate):** [references/phase-2-evaluate.md](references/phase-2-evaluate.md)
**Phase 3 (Report):** [references/phase-3-report.md](references/phase-3-report.md)
**Phase 4 (Recommend):** [references/phase-4-recommend.md](references/phase-4-recommend.md)
**Phase 5 (Fix):** [references/phase-5-fix.md](references/phase-5-fix.md) - Only with `--fix` flag

**Examples:** [references/examples.md](references/examples.md)
**Troubleshooting:** [references/troubleshooting.md](references/troubleshooting.md)

---

## 🆚 Skill Comparison

| Aspect | `/auto-i18n` | `/i18n-content-audit` | `/i18n-content-audit --fix` |
|--------|--------------|----------------------|----------------------------|
| Purpose | Create new content | Audit existing content | Audit + optimize content |
| Input | EN page + target locale | Existing locale page | Existing locale page |
| Output | New JSON file | Audit report only | Report + modified file |
| Modifies Files | Yes (creates new) | ❌ No | ✅ Yes (updates existing) |
| When to Use | New language support | Review before optimizing | Auto-fix quality issues |

---

**Last Updated:** 2026-02-03
