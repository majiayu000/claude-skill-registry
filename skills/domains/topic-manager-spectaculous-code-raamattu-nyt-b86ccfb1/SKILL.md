---
name: topic-manager
description: Expert assistant for managing biblical topics in the KR92 Bible Voice project. Use when (1) creating/editing topics and their Finnish translations, (2) managing topic relations (related, opposite, broader, narrower), (3) validating Finnish translations and pronunciations with Voikko/Omorfi, (4) reviewing topics marked with qa_status='unchecked', (5) bulk updating topic translations, (6) managing topic aliases and synonyms, or (7) fixing incorrectly translated Finnish topic names.
---

# Topic Manager

Manage biblical topics: names, translations, relations, aliases, and QA validation.

## Quick Reference

Read these context files first:
- `Docs/context/db-schema-short.md` - Table structures
- `apps/raamattu-nyt/src/lib/topicEditorUtils.ts` - TypeScript API utilities

## Database Schema

### topical_topics (bible_schema)
```sql
id UUID PRIMARY KEY
name_en TEXT NOT NULL          -- English topic name
name_fi TEXT                   -- Finnish translation
slug TEXT UNIQUE NOT NULL      -- URL slug (English)
slug_fi TEXT                   -- Finnish URL slug
parent_id UUID                 -- Broader topic (hierarchy)
qa_status qa_status_enum       -- 'unchecked', 'ok', 'needs_review'
is_core BOOLEAN                -- Important/featured topic
is_biblical BOOLEAN            -- Biblical vs modern term
semantic_field TEXT            -- Semantic category
semantic_field_fi TEXT         -- Finnish semantic field
semantic_field_en TEXT         -- English semantic field
usage_context TEXT             -- How term is used
usage_context_fi TEXT          -- Finnish context
usage_context_en TEXT          -- English context
nuance_fi TEXT                 -- Finnish nuance
nuance_en TEXT                 -- English nuance
```

### topical_relations (bible_schema)
```sql
source_topic_id UUID           -- Source topic
target_topic_id UUID           -- Target topic
relation_type TEXT             -- 'related', 'opposite', 'synonym'
is_bidirectional BOOLEAN       -- TRUE for opposite/synonym
```

### topical_aliases (bible_schema)
```sql
topic_id UUID
alias TEXT                     -- Display text
alias_norm TEXT                -- Normalized (lowercase, no diacritics)
lang TEXT                      -- 'fi' or 'en'
alias_type TEXT                -- 'synonym', 'abbrev', 'variant', 'old_term', 'misspelling'
qa_status qa_status_enum       -- 'unchecked', 'ok', 'needs_review'
source TEXT                    -- 'manual', 'ai', 'import'
```

### topical_references (bible_schema)
```sql
topic_id UUID
osis_start TEXT                -- Start verse (e.g., 'Gen.1.1')
osis_end TEXT                  -- End verse (for ranges)
relevance_score INTEGER        -- 1-5 relevance
```

## Common Operations

### Find Topics Needing Review
```sql
-- Topics with unchecked qa_status
SELECT id, name_en, name_fi, qa_status
FROM bible_schema.topical_topics
WHERE qa_status = 'unchecked'
ORDER BY is_core DESC, name_en
LIMIT 50;

-- Topics without Finnish translation
SELECT id, name_en, slug
FROM bible_schema.topical_topics
WHERE name_fi IS NULL
ORDER BY is_core DESC, name_en;
```

### Update Topic Translation
```sql
UPDATE bible_schema.topical_topics
SET
  name_fi = 'suomenkielinen nimi',
  slug_fi = 'suomenkielinen-slug',
  qa_status = 'ok'
WHERE id = 'uuid-here';
```

### Create Topic Relation
```sql
-- Related topic (one-way)
INSERT INTO bible_schema.topical_relations
  (source_topic_id, target_topic_id, relation_type, is_bidirectional)
VALUES ('source-uuid', 'target-uuid', 'related', false);

-- Opposite (bidirectional)
INSERT INTO bible_schema.topical_relations
  (source_topic_id, target_topic_id, relation_type, is_bidirectional)
VALUES ('source-uuid', 'target-uuid', 'opposite', true);
```

### Set Topic Hierarchy
```sql
-- Set parent (broader term)
UPDATE bible_schema.topical_topics
SET parent_id = (SELECT id FROM bible_schema.topical_topics WHERE slug = 'parent-slug')
WHERE slug = 'child-slug';
```

### Add Topic Alias
```sql
INSERT INTO bible_schema.topical_aliases
  (topic_id, alias, alias_norm, lang, alias_type, source, qa_status)
VALUES (
  'topic-uuid',
  'Vaihtoehtoinen nimi',
  'vaihtoehtoinen nimi',
  'fi',
  'synonym',
  'manual',
  'ok'
);
```

## Finnish Translation Validation

### QA Status Values
- `unchecked` - Not reviewed yet (default for imports)
- `ok` - Verified correct
- `needs_review` - Flagged for human review

### Common Finnish Issues
1. **Wrong translation** - Check with Voikko/Omorfi
2. **Missing diacritics** - ä, ö must be correct
3. **Compound words** - Finnish compounds may be written together
4. **Capitalization** - Finnish doesn't capitalize most terms

### Voikko/Omorfi Integration

For Finnish morphological validation, use these tools:

**Option 1: UralicNLP (Python)**
```python
# pip install uralicnlp
from uralicnlp import uralicApi

# Check if word is valid Finnish
def is_valid_finnish(word):
    analyses = uralicApi.analyze(word, "fin")
    return len(analyses) > 0

# Get lemma (base form)
def get_lemma(word):
    analyses = uralicApi.analyze(word, "fin")
    if analyses:
        return analyses[0][0]  # First analysis, lemma
    return word
```

**Option 2: libvoikko (Python)**
```python
# pip install libvoikko
import libvoikko

voikko = libvoikko.Voikko("fi")

def is_valid_finnish(word):
    return voikko.spell(word)

def analyze_word(word):
    return voikko.analyze(word)

def get_suggestions(word):
    if not voikko.spell(word):
        return voikko.suggest(word)
    return []
```

**Option 3: API-based (no local install)**
```typescript
// Use Edge Function to call external API
async function validateFinnish(word: string) {
  const response = await fetch(
    `https://api.kielitoimistonsanakirja.fi/api/search?word=${encodeURIComponent(word)}`
  );
  return response.ok;
}
```

### Validation Script
See `scripts/validate_finnish.py` for batch validation of topic translations.

## Bulk Operations

### Export for Translation
```sql
-- Export untranslated topics to CSV format
SELECT
  slug,
  name_en,
  COALESCE(name_fi, '') as name_fi,
  COALESCE(slug_fi, '') as slug_fi,
  is_core
FROM bible_schema.topical_topics
WHERE name_fi IS NULL OR qa_status = 'unchecked'
ORDER BY is_core DESC, name_en;
```

### Import Translations
```sql
-- Create temp table
CREATE TEMP TABLE topic_import (
  slug TEXT,
  name_fi TEXT,
  slug_fi TEXT
);

-- Import (via \copy or Supabase)
-- Update topics
UPDATE bible_schema.topical_topics t
SET
  name_fi = i.name_fi,
  slug_fi = i.slug_fi,
  qa_status = 'ok'
FROM topic_import i
WHERE t.slug = i.slug;
```

### Mark Topics as Reviewed
```sql
-- Mark single topic
UPDATE bible_schema.topical_topics
SET qa_status = 'ok'
WHERE id = 'uuid';

-- Batch mark by criteria
UPDATE bible_schema.topical_topics
SET qa_status = 'ok'
WHERE qa_status = 'unchecked'
AND name_fi IS NOT NULL
AND LENGTH(name_fi) > 2;
```

## Relation Types

| Type | Direction | Use Case |
|------|-----------|----------|
| `related` | One-way | Topic A relates to B |
| `opposite` | Bidirectional | Antonyms (e.g., good ↔ evil) |
| `synonym` | Bidirectional | Same concept, different name |
| `broader` | Uses parent_id | Hierarchy (parent topic) |
| `narrower` | Reverse of parent_id | Hierarchy (child topics) |

## QA Workflow

1. **Query unchecked topics** - Start with high-value (is_core=true)
2. **Validate Finnish** - Use Voikko/UralicNLP to check spelling
3. **Review translation** - Ensure theological accuracy
4. **Check relations** - Verify related/opposite links make sense
5. **Mark as reviewed** - Set qa_status='ok'

## Integration with Other Skills

| Task | Delegate To |
|------|-------------|
| Schema changes | `supabase-migration-writer` |
| Admin UI changes | `admin-panel-builder` |
| Bulk CSV operations | `translation-sync` |
| AI-assisted translations | `ai-prompt-manager` |
| Finding topic code | `code-wizard` |

## TypeScript API

Key functions in `apps/raamattu-nyt/src/lib/topicEditorUtils.ts`:
- `fetchTopicById(id)` - Get topic details
- `updateTopic(id, updates, token)` - Update topic
- `createAlias(topicId, alias, lang, type, token)` - Add alias
- `createRelation(source, target, type, token)` - Create relation
- `setTopicParent(topicId, parentId, token)` - Set hierarchy
- `searchSimilarTopics(query, excludeId)` - Find duplicates
- `mergeTopicAsSynonym(primary, duplicate, token)` - Merge topics
