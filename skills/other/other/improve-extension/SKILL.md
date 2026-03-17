---
name: improve-extension
description: Guide for improving the Auctionet extension over time — adding quality rules, tuning AI prompts, improving cataloging accuracy, and evolving extension capabilities. Use when the user wants to make the extension smarter or better at its job.
argument-hint: [area to improve]
---

# Improving the Auctionet Extension

Use this skill to systematically improve the extension's cataloging quality, AI accuracy, and user experience. Focus on: `$ARGUMENTS`

## Improvement Areas

### 1. Quality Rules (`modules/core/quality-rules-engine.js`)

The rules engine scores items on completeness and accuracy. To add a new rule:

1. **Identify the pattern** — what cataloging mistake are you catching?
2. **Check existing rules** — read `quality-rules-engine.js` to avoid duplicates
3. **Add the rule** with:
   - Clear warning message in Swedish
   - Appropriate severity (critical/high/medium/low)
   - Inline hint text that helps the cataloger fix it
   - Category-specific applicability if relevant
4. **Update scoring weights** if the new rule affects overall quality score
5. **Test** against real Auctionet listings to verify false positive rate

**Rule anatomy:**
```javascript
{
  id: 'vague-condition',
  check: (data) => /bruksslitage|bruksskick/i.test(data.condition),
  warning: 'Vagt skick — beskriv specifik typ av slitage',
  severity: 'high',
  field: 'condition',
  categories: 'all'  // or ['furniture', 'art', ...]
}
```

### 2. AI Prompts (`modules/refactored/ai-rules-system/ai-rules-config.json`)

The centralized rules config controls all AI behavior. To improve prompts:

**Key prompt locations:**
- `systemPrompts.core` — base personality and forbidden language
- `systemPrompts.titleCorrect` — minimal title correction mode
- `systemPrompts.addItems` — quick cataloging enhancement
- `systemPrompts.freetextParser` — parsing unstructured text into fields
- `systemPrompts.textEnhancement` — combining image + text analysis
- `categoryRules.*` — per-category overrides (weapons, watches, jewelry, etc.)

**Prompt improvement checklist:**
- [ ] Does the prompt produce correct output for 10+ real items?
- [ ] Are there false positives where the AI "improves" correct text into something wrong?
- [ ] Is the forbidden language list comprehensive enough?
- [ ] Are anti-hallucination rules specific enough for the category?
- [ ] Is the temperature right? (lower = more consistent, higher = more creative)

**Model-specific tuning:**
Different models in `categoryRules.freetextParser.valuationRules`:
- `claude-sonnet-4-20250514` — advanced multi-step reasoning
- `default` — conservative fallback
Add new model-specific configs when switching models.

### 3. Brand & Spelling Validation

**Brand corrections** (`ai-rules-config.json` → `brandCorrections`):
- Maps common misspellings to correct brand names
- Add new entries when catalogers consistently misspell brands

**Swedish spellchecker** (`modules/swedish-spellchecker.js`):
- Custom dictionary of auction terms that standard spellcheckers flag incorrectly
- Add terms that get false-flagged (e.g., "fanerad", "intarsia", "proveniens")

**Artist corrections** — same pattern as brand corrections for artist names.

### 4. Market Analysis Accuracy

**Search term generation** (`modules/ai-search-query-generator.js`):
- Improve how the AI extracts optimal search terms from item data
- Key: balance between too specific (no results) and too broad (irrelevant results)

**Relevance filtering** (`modules/api-manager.js` → Haiku calls):
- When market data has high spread, Haiku validates relevance
- Improve the filtering prompt to reduce false positives/negatives

**Term processing** (`modules/core/term-processor.js`):
- Handles conflict resolution between overlapping search terms
- Improve deduplication and term ranking logic

### 5. Category Detection

**Current detection** — extracts from title keywords and Auctionet category field.
**Improvement opportunities:**
- Better mapping of Swedish terms to categories
- Use image analysis to supplement text-based detection
- Add new category-specific rules as patterns emerge

### 6. Condition Quality Nudging

Based on the condition quality report (31.7% vague conditions):
- **Expand suggestion chips** — more category-specific alternatives
- **Add severity scoring** — standalone "bruksslitage" scores lower than "bruksslitage, repor"
- **Track improvement** — measure if vague condition usage decreases over time
- **New vague terms** — monitor for new vague patterns in other languages (German, Danish, Spanish)

## How to Test Improvements

### Manual Testing Workflow
1. Navigate to an Auctionet admin item edit page
2. Enter test data in fields
3. Observe quality score, inline hints, market data
4. Verify AI suggestions are accurate and not hallucinated
5. Check that undo reverts all changes cleanly

### Key Test Cases
- Empty item (all fields blank) — should show low score, helpful hints
- Well-cataloged item — should show high score, minimal suggestions
- Item with "bruksslitage" condition — should flag and suggest alternatives
- Art with artist in title — should detect and offer "Flytta" action
- Item with misspelled brand — should catch and suggest correction
- Weapons/historical items — should NOT add fabricated historical context

### Performance Testing
- AI calls should resolve within 5–10 seconds
- Quality scoring should update within 3 seconds of typing
- Market data should load within 8 seconds
- No visible UI lag during scoring updates

## Extension Architecture for Changes

### Where things live
```
New quality rule       → modules/core/quality-rules-engine.js
New AI prompt          → modules/refactored/ai-rules-system/ai-rules-config.json
New brand correction   → ai-rules-config.json → brandCorrections
New forbidden word     → ai-rules-config.json → forbiddenWords
New category handler   → modules/item-type-handlers.js
New spellcheck term    → modules/swedish-spellchecker.js
New search strategy    → modules/ai-search-query-generator.js + ai-search-rules.js
Market display change  → modules/dashboard-manager-v2.js
Valuation logic change → modules/valuation-request-assistant.js
```

### Patterns to follow
- **Dependency injection** — pass dependencies via setters, not global state
- **Debounced updates** — 3-second delay after typing before analysis
- **HTML escaping** — always use `escapeHTML()` for DOM insertions
- **Anti-hallucination** — AI never invents data not in source
- **Prompt caching** — mark system prompts with `cache_control: { type: 'ephemeral' }`

## Continuous Improvement Ideas

### Short-term
- Add more category-specific condition suggestions
- Improve search term extraction for uncommon item types
- Add validation for common Swedish date formatting errors
- Better handling of multi-language listings

### Medium-term
- Track which AI suggestions catalogers accept vs reject (quality signal)
- Build a feedback loop: rejected suggestions → prompt refinement
- Add OCR-like capabilities for reading stamps and hallmarks in images
- Cross-auction-house quality benchmarking

### Long-term
- Learn from high-performing auction houses (0% vague conditions)
- Predictive valuation based on seasonal market trends
- Automated translation quality checking
- Integration with external art databases for artist verification
