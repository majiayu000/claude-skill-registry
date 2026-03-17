---
name: i18n-seo-localizer
description: Research and generate SEO-optimized localized pages for new languages. Keywords are validated through multi-dimensional analysis including Autocomplete, Top 30 competitor analysis, and market-specific search engines (Baidu for China, Naver for Korea, Yandex for Russia, Google for others). Use when (1) creating new localized content for additional languages, (2) researching keywords for target locales, or (3) validating keyword mappings.
---

# i18n SEO Localizer

Creates SEO-optimized localized pages through **researched keywords**, not translations.

## Core Philosophy

> **Every keyword must be researched and validated, not translated.**

Same concept, different expressions per language:
- EN: "AI image generator"
- ZH: "AI绘画" (not "AI图像生成器")
- DE: "KI-Bildgenerator" (KI, not AI!)
- RU: "Нейросеть для генерации картинок" (neural network, not AI!)

**Why:** Direct translation produces low-volume keywords that users don't actually search.

---

## Quick Start

### Check Keyword Coverage

```bash
# List existing keyword files
ls .claude/skills/i18n-seo-localizer/data/

# Expected files for 14 locales
keywords-base.json (en), keywords-zh.json, keywords-zh-TW.json,
keywords-ja.json, keywords-ko.json, keywords-de.json, keywords-es.json,
keywords-fr.json, keywords-pt.json, keywords-it.json, keywords-ar.json,
keywords-id.json, keywords-ru.json, keywords-hi.json
```

**If keyword file exists**: Read and apply keywords directly

**If keyword file missing**: Run keyword research workflow (see Phase 1 below)

---

## Three-Phase Workflow

### Phase 1: Keyword Research

**MANDATORY before generating any localized content.**

**High-level steps:**
1. Select appropriate search engine for target market (see search-engines-config.md)
2. Generate 3-5 candidate keywords
3. Multi-dimensional validation (5 metrics, 100-point system):
   - Search results volume (15%)
   - Top 30 competitor analysis (30%)
   - Autocomplete ranking (30%) ⭐ Most important
   - Related searches (20%)
   - Language naturalness (5%)
4. Document decision in keywords-{locale}.json with scores

**See [keyword-research-workflow.md](./references/keyword-research-workflow.md) for complete workflow.**

#### Search Engine Selection

**CRITICAL:** Use the search engine your target market actually uses.

- **zh (China):** 百度 (Baidu) + 百度指数 - NOT Google
- **ko (Korea):** Naver + Naver DataLab (primary)
- **ru (Russia):** Yandex + Yandex Wordstat
- **Others:** Google (appropriate TLD)

**See [search-engines-config.md](./references/search-engines-config.md) for complete mapping.**

#### Keyword File Format

**Required fields:**
- Basic: source, primary, alternatives, reasoning, validated, validatedDate
- Extended: semanticVariants, relatedTerms, longTail, usageGuidelines, antiPatterns, goodExamples
- Validation: validationMethod, searchEngine, searchEngineMarket, validationScores

**⚠️ Extended fields are REQUIRED** to prevent keyword stuffing.

**See [keyword-template.md](./references/keyword-template.md) for complete template.**

---

### Phase 2: Content Generation

After keywords validated:

1. **Read keyword file** for target locale
2. **Apply keywords** according to usageGuidelines:
   - Title: primary keyword (max 1x)
   - H1: primary or semanticVariants (max 1x)
   - H2: alternatives/semanticVariants/longTail (max 3x, must vary)
   - Body: diverse strategy (30% primary, 40% semanticVariants, 30% relatedTerms)
   - Alt text: semanticVariants or relatedTerms (max 1x per image)
3. **Check character limits** from keyword file
4. **Use commonPhrases** for CTAs
5. **Follow SEO guidelines**: See [02-seo-guidelines.md](./references/02-seo-guidelines.md)
6. **Consider cultural notes** from keyword file

---

### Phase 3: Validation

1. Run build: `pnpm build`
2. Verify keywords properly placed
3. Check character limits per language
4. Test on target locale

---

## Important Rules

1. **NEVER translate keywords** - always research with market data
2. **ALWAYS check keyword file first** before generating content
3. **USE correct search engine** for target market:
   - ❌ google.com.cn does NOT exist
   - ✅ Use Baidu for China, Naver for Korea, Yandex for Russia
4. **VALIDATE with multi-dimensional analysis**:
   - Top 30 competitor analysis (not just Top 10)
   - Autocomplete ranking (real user behavior)
   - Related searches validation
   - Include validation scores in keyword file
5. **DOCUMENT all decisions** with search engine used and validation scores
6. **CHECK Top 30 competitors** across three tiers
7. **USE usageGuidelines** to prevent keyword stuffing
8. **RESPECT characterLimits** per language
9. **RECORD searchEngine and searchEngineMarket** in all keyword entries

---

## Supported Languages

| Code | Language | Country Code | Priority | Key Insight |
|------|----------|--------------|----------|-------------|
| zh | Simplified Chinese | CN | T1 | 口语化简洁 |
| zh-TW | Traditional Chinese | TW | T2 | Taiwan/HK market |
| ja | Japanese | JP | T1 | イラスト vs 画像 |
| ko | Korean | KR | T1 | Tech-savvy |
| de | German | DE | T1 | KI not AI |
| es | Spanish | ES | T2 | LATAM + Spain |
| pt | Portuguese | BR | T2 | Brazil focus |
| fr | French | FR | T2 | Growing |
| it | Italian | IT | T3 | European |
| ar | Arabic | SA | T2 | RTL + مجاني |
| id | Indonesian | ID | T2 | Gratis critical |
| ru | Russian | RU | T2 | Нейросеть term |
| hi | Hindi | IN | T3 | Hinglish mix |

**See [01-language-profiles.md](./references/01-language-profiles.md) for detailed profiles.**

---

## Integration with Other Skills

### shipany-page-builder

When generating pages:
1. Read keyword mapping for target locale
2. Pass primary/alternatives to page builder
3. Page builder applies keywords per usageGuidelines

### auto-i18n

Automatically uses keyword mappings when localizing existing English pages.

---

## Technical Requirements

**Always use explicit locale in `getTranslations()` calls.**

See `.claude/skills/shipany-page-builder/references/04-i18n-best-practices.md`

---

## File Structure

```
.claude/skills/i18n-seo-localizer/
├── SKILL.md                      # This file
├── references/
│   ├── keyword-research-workflow.md  # 5-metric validation workflow
│   ├── search-engines-config.md      # Market-specific search engines
│   ├── keyword-template.md           # JSON template and fields
│   ├── 01-language-profiles.md       # Per-language guidelines
│   └── 02-seo-guidelines.md          # SEO requirements
└── data/
    ├── keywords-base.json        # English base
    ├── keywords-zh.json          # Simplified Chinese
    ├── keywords-zh-TW.json       # Traditional Chinese
    └── [12 more locale files]
```

---

## Adding a New Language

1. Check search-engines-config.md for correct search engine
2. Create keywords-{locale}.json using template
3. Research all keywords from keywords-base.json
4. Validate with multi-dimensional analysis (5 metrics)
5. Record searchEngine and validationScores in each entry
6. Add language profile to references/01-language-profiles.md
7. Document cultural notes
8. Register locale in src/config/locale/index.ts

---

## Common Workflows

### Scenario 1: Research New Keyword for Existing Locale

```
1. Check references/search-engines-config.md for correct search engine
2. Read references/keyword-research-workflow.md
3. Generate 3-5 candidates
4. Multi-dimensional validation (100-point system):
   a. Search results volume (relative comparison)
   b. Top 30 competitor analysis (three-tier weighting)
   c. Autocomplete ranking (multiple prefix tests)
   d. Related searches check
   e. Language naturalness assessment
5. Calculate total score and tier consistency bonus
6. Document in keywords-{locale}.json with:
   - searchEngine (e.g., "baidu", "naver")
   - searchEngineMarket (e.g., "中国大陆")
   - validationScores object
```

### Scenario 2: Add New Locale

```
1. Check search-engines-config.md for target market
2. Create data/keywords-{locale}.json from template
3. For each keyword in keywords-base.json:
   a. Run keyword research workflow
   b. Use correct search engine for validation
   c. Perform 5-metric validation
   d. Document with all required fields including:
      - searchEngine
      - searchEngineMarket
      - validationScores
4. Add language profile to references/
5. Test with sample content
6. Register in project config
```

---

## Reference Documents

**Keyword Research:**
- [keyword-research-workflow.md](./references/keyword-research-workflow.md) - Multi-dimensional validation workflow
- [search-engines-config.md](./references/search-engines-config.md) - Market-specific search engines
- [keyword-template.md](./references/keyword-template.md) - JSON template with all fields

**Language Guidance:**
- [01-language-profiles.md](./references/01-language-profiles.md) - Per-language characteristics
- [02-seo-guidelines.md](./references/02-seo-guidelines.md) - SEO requirements

**Read these documents AS NEEDED during workflow execution.**

---

## Execution Pattern

```
User request → Check keyword file exists
  ↓                     ↓
  No                   Yes
  ↓                     ↓
Research workflow   Read & apply keywords
  ↓                     ↓
Select search     Generate content
engine (Baidu/        ↓
Naver/Google)    Build & validate
  ↓
Multi-dimensional
validation (5 metrics)
  ↓
Document with scores
```
