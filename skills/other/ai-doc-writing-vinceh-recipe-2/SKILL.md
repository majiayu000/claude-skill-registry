---
name: ai-doc-writing
description: This skill should be used when writing, reviewing, or refactoring documentation that will be consumed as AI context. Optimizes documentation for LLM comprehension using principles of completeness, efficiency, and zero fluff—replacing prose with structured data, enforcing heading hierarchy, detecting meta-commentary, and validating that examples serve a purpose.
---

# AI-Optimized Documentation Writing

## Overview

Documentation consumed by AI has fundamentally different requirements than human-facing docs. LLMs process documentation at passage-level (phrase chunks), build mental models from heading structure, and are confused by meta-commentary, synonym variation, and narrative prose.

This skill provides:
1. **Style principles** for writing AI-context docs (completeness + efficiency + zero fluff)
2. **Fluff detector** (automated checker for common violations)
3. **Refactoring patterns** for converting verbose docs to AI-optimized structure

**When to use:** Writing, reviewing, or refactoring any documentation intended for AI consumption (setup guides, architecture docs, API references, workflow guides, configuration specs).

---

## Core Principles

**Completeness:** Every critical piece of information must be present. No assumptions about reader background.

**Efficiency:** Only essential information. No explanations of design choices, meta-commentary, or justifications.

**Zero Fluff:** No meta-commentary ("Updated!", "We added..."), conversational language ("You'll want to..."), transition phrases ("As mentioned..."), or redundant restatements.

---

## Writing Workflow

### 1. Choose Document Structure

Pick the format that best serves the content:
- **Bullets + structured data** for facts, relationships, configuration
- **Code blocks** for examples that show non-obvious behavior
- **Numbered steps** for workflows with clear sequence
- **Heading hierarchy** (H2 → H3 → H4, never skip levels)

### 2. Fill Content by Category

**Configuration/Relationships:** Use YAML/code blocks, not prose
```yaml
**Fallback chain:**
- ja → en
- ko → en
- zh-tw → zh-cn → en
```

**Procedures:** Numbered steps with inputs/outputs
```
1. Load recipe with eager-loaded associations
2. Instantiate RecipeTranslator
3. For each language, call translator.translate_recipe()
4. Apply translations via apply_translations()
```

**Behavior:** Code examples only when they show edge cases/counterintuitive behavior
```ruby
I18n.with_locale(:ja) { recipe.name }  # Falls back to 'en' if translation missing
```

### 3. Run Fluff Detector

Before committing:
```bash
python3 scripts/fluff-detector.py your-doc.md
```

Detector catches:
- Meta-commentary: "Last Updated", "We fixed", "UPDATED!"
- Conversational language: "You'll want to", "Gotchas", "TLDR"
- Heading hierarchy violations: H2 → H4 (skipped H3)
- Synonym variation: Multiple terms for same concept
- Transition phrases: "As mentioned", "Additionally"
- Redundant restatement: Explaining old way + new way

### 4. Address Violations

**Meta-commentary:** Remove entirely. Just describe current state.
- ❌ "We recently migrated to Mobility"
- ✅ "Backend: Table (Mobility gem)"

**Conversational language:** Convert to imperative structure.
- ❌ "For those who want to understand how this works..."
- ✅ "**How it works:** [structure content]"

**Hierarchy violations:** Insert missing heading level.
- ❌ `## Configuration` → `#### Translation Tables`
- ✅ `## Configuration` → `### Translation System` → `#### Translation Tables`

**Synonym variation:** Replace all with single consistent term.
- ❌ "Mobility (i18n gem, translation system, locale handler)"
- ✅ "Mobility (the translation system)"

**Redundant restatement:** Keep only the version that's clearest.
- ❌ "Previously JSONB, now translation tables. Translation tables are better because..."
- ✅ "**Storage:** Dedicated translation tables (UUID foreign keys, locale-scoped uniqueness)"

### 5. Validate Examples

Examples should reveal non-obvious behavior. If example just restates description, remove it.

**✅ Include:** Shows edge case/counterintuitive behavior
```ruby
# Fallback behavior when translation missing
I18n.with_locale(:ja) { recipe.name }  # Returns English translation
```

**❌ Exclude:** Restates description
```ruby
# To read a translation, use I18n.with_locale
I18n.with_locale(:ja) { recipe.name }
```

---

## Reference: Style Guide

See `references/style-guide.md` for:
- Detailed patterns (good vs bad for each doc type)
- Complete fluff checklist
- Common mistakes and fixes
- Self-check before committing

---

## Tool: Fluff Detector

Automated checker for common violations.

**Usage:**
```bash
# Check single file
python3 scripts/fluff-detector.py documentation.md

# Check multiple files
python3 scripts/fluff-detector.py doc1.md doc2.md doc3.md
```

**Output:** Lists line numbers with violation type and content snippet

**Catches:**
- Meta-commentary (errors—blocking)
- Conversational language (warnings)
- Heading hierarchy violations (warnings)
- Transition phrases (warnings)
- Redundant restatement patterns (warnings)

---

## Refactoring Patterns

### Pattern 1: Prose → Bullets + Structure

**Before:**
```
Mobility is configured with several important plugins. The fallbacks plugin
handles missing translations gracefully by falling back to the fallback locale.
We've configured the fallback chain so that Japanese falls back to English.
```

**After:**
```
**Plugins:** fallbacks, reader, writer, query, cache, locale_accessors

**Fallback chain:**
- ja → en
```

### Pattern 2: Narrative → Steps + Outputs

**Before:**
```
When a recipe is created, the system triggers a background job called
TranslateRecipeJob. This job instantiates the RecipeTranslator service and
then calls the translate method for each language. Finally, it updates the
recipe's translations_completed flag.
```

**After:**
```
**Trigger:** Recipe creation (background job)

**Process:**
1. Instantiate RecipeTranslator
2. For each language [ja, ko, zh-tw, zh-cn, es, fr]:
   - Call translator.translate_recipe(recipe, lang)
   - Apply translations via apply_translations()
3. Set recipe.translations_completed = true
```

### Pattern 3: Multiple terms → Single consistent term

**Before:**
```
The system uses the Mobility gem (also known as the i18n library or translation system)
to manage translations (also called locales or language variants).
```

**After:**
```
Mobility manages translations across 6 languages.
```

---

## Checklist: Before Committing Docs

- [ ] Run fluff detector: `python3 scripts/fluff-detector.py file.md`
- [ ] No meta-commentary (dates, "we fixed", "updated!")
- [ ] No conversational language ("You'll want to", "Gotchas")
- [ ] Heading hierarchy strict (H2 → H3 → H4, no skips)
- [ ] One term used consistently (no synonyms)
- [ ] Examples only show non-obvious behavior
- [ ] All information is essential (no "nice to know")
- [ ] Structured data for relationships/config (not prose)
- [ ] Each bullet is atomic (independent idea)

---

## Examples

See provided before/after examples in this skill documentation for patterns:
- Configuration documentation
- Workflow documentation
- Data structure documentation
- Procedure documentation
- Fluff examples (what to detect and remove)

