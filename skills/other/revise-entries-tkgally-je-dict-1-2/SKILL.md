---
name: revise-entries
description: Checklist for revising existing je-dict-1 entries to v2 quality standards. Use when improving existing entries rather than creating new ones.
---

# Entry Revision Checklist

Use this checklist when revising existing entries to bring them up to the v2 specification standards.

## High Priority Revisions (Do First)

### For ALL Entries - Furigana

- [ ] **All kanji have furigana** in headword, examples, AND notes
- [ ] Verify: `python3 build/verify_furigana.py <entry_id>` shows "✓ OK"
- [ ] Pay special attention to idioms, collocations, and kanji variants in notes

### For ALL Entries - Notes Formatting

- [ ] **Line breaks**: Separate multiple topics with blank lines
- [ ] **Bullet points**: Use `- ` for lists of 2+ items
- [ ] **Section headers**: Use clear labels like `COMMON PATTERNS:`, `TRANSITIVITY:`

See the `vocabulary-notes` skill for complete formatting guidelines.

### For ALL Verb Entries

- [ ] **Transitivity**: Add transitivity type ({自動詞|じどうし}/{他動詞|たどうし})
- [ ] **Pair verb**: Identify and link the transitive/intransitive pair
- [ ] **Aspect notes**: Explain what ている means for this verb
- [ ] **Particle patterns**: Show which particles the verb takes (が/を/に)
- [ ] **Collocations**: Add 2-3 common noun pairings

### For ALL Particle Entries

- [ ] **Predicate list**: Add explicit list of verbs/adjectives requiring this particle
- [ ] **Contrast section**: Compare with commonly confused particles
- [ ] **Information structure**: Explain new vs. old information (for が/は)
- [ ] **Fixed patterns**: List grammatical patterns using this particle

### For Depth Consistency

- [ ] **Compare similar entries**: Check that similar words have similar depth
- [ ] **Match the best**: If one verb has excellent aspect notes, add them to all verbs
- [ ] **No outliers**: No entry should be significantly more or less detailed than peers

## Medium Priority Revisions (Do Second)

### For ALL Entries - Example Requirements

**See `example-sentences` skill for complete guidelines.**

- [ ] **Minimum examples**: 5 per sense (basic/core) or 3 per sense (general)
- [ ] **Progressive length**: Examples go from short → long within each sense
- [ ] **Vocabulary restrictions** (basic tier): Examples 1-2 use basic vocab only; examples 3-5 use basic+core only
- [ ] **Vocabulary restrictions** (core tier): Examples 1-2 use basic+core vocab only
- [ ] **Sense coverage**: All senses have adequate examples

### For ALL Entries - General

- [ ] **Register label**: Add Casual/Neutral/Formal where relevant
- [ ] **Fixed phrase**: Include at least one high-frequency collocation

### For Verb Entries

- [ ] **Negative usage**: Note when the verb is NOT used
- [ ] **Keigo links**: Add honorific alternatives for common verbs

### For Adjective Entries

- [ ] **Forms**: Add adverbial form (〜く/〜に) and noun form (〜さ) where natural
- [ ] **Conjugation**: Add negative, te-form, past
- [ ] **Similar words**: Add distinctions from semantic neighbors

### For Noun Entries

- [ ] **Collocations**: Add common verb pairings
- [ ] **Scope**: Clarify if meaning differs from English equivalent

### For Counter Entries

- [ ] **Full pattern**: Add complete 1-10 counting table
- [ ] **Irregulars**: Highlight all irregular readings
- [ ] **Sound changes**: Explain rendaku/sokuon patterns

## Low Priority Revisions (Do Last)

- [ ] **Kanji notes**: When to use kanji vs. hiragana
- [ ] **Cultural notes**: Expand where significant
- [ ] **Keigo references**: Link to honorific forms for very common verbs

## Revision Process

### Step 1: Audit Entry Type
1. List all entries of one type (e.g., all verbs)
2. Identify entries missing HIGH PRIORITY information
3. Rank by importance/frequency

### Step 2: Batch Revisions
1. Work through one entry type at a time
2. Add the same information type to all entries that need it
3. This ensures consistency

### Step 3: Quality Check
1. Compare revised entries with peers
2. Ensure consistent depth and structure
3. Verify all checklist items are addressed

## Learner Pitfall Callouts

When adding notes, consider adding callout boxes for common mistakes:

```
LEARNER PITFALL:
{知|し}る = learning a fact for the first time
{知|し}っている = already knowing
→ Use {知|し}っている for "I know"
```

High-value pitfall topics:
- ている with state verbs (知る, 持つ, 結婚する)
- が vs. は confusion
- Transitive/intransitive pair confusion
- Counter irregularities
- Potential form particle (が vs. を)

## Entries Needing Special Attention

Based on evaluation findings, prioritize these entry categories:

### Verbs with Non-Obvious ている
- {知|し}る → {知|し}っている (state: "know")
- {持|も}つ → {持|も}っている (state: "have")
- {住|す}む → {住|す}んでいる (state: "live at")
- {結婚|けっこん}する → {結婚|けっこん}している (state: "be married")
- {死|し}ぬ → {死|し}んでいる (state: "be dead")

### Common Transitive/Intransitive Pairs
- {開|あ}く/{開|あ}ける, {閉|し}まる/{閉|し}める
- {始|はじ}まる/{始|はじ}める, {終|お}わる/{終|お}える
- {出|で}る/{出|だ}す, {入|はい}る/{入|い}れる
- {付|つ}く/{付|つ}ける, {消|き}える/{消|け}す
- {割|わ}れる/{割|わ}る, {壊|こわ}れる/{壊|こわ}す

### Particles (ALL need depth review)
- が - predicate list, は contrast
- は - topic vs. subject, contrastive use
- を - motion verbs, potential form alternation
- に - location vs. で, indirect object, time
- で - action location, means, reason

## Updating Timestamps When Revising

**IMPORTANT**: When revising an entry, update the `modified` timestamp to the current UTC time.

Run this command to get the correct timestamp:
```bash
python3 build/get_timestamp.py
```

Then update only the `modified` field (keep `created` unchanged):
```json
"metadata": {
  "created": "2026-01-05T08:30:00Z",   // Keep original
  "modified": "2026-01-12T10:52:00Z",  // Update to current UTC
  ...
}
```

This ensures the entry appears in the "Recent" page with the correct revision date.

## Final Steps After Revisions

After revising entries, run these commands:

```bash
python3 build/validate.py           # Validate all entries
python3 build/verify_furigana.py <entry_ids...>  # Verify furigana coverage
python3 build/update_indexes.py     # Update indexes
python3 build/build_flat.py         # Rebuild website (REQUIRED for GitHub Pages)
git add entries/ docs/ *.json PROJECT_STATUS.md
git commit -m "Revise entries to v2 standards"
git push
```

The `build_flat.py` step is critical - without it, changes won't appear on the live site.

Check for:
- Schema compliance
- **Furigana on all kanji** - use `python3 build/verify_furigana.py` to confirm
- No broken cross-references
