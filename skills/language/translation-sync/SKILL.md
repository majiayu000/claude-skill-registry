---
name: translation-sync
description: Expert assistant for managing Finnish/English content translations in the KR92 Bible Voice project. Use when syncing topic translations, managing translation cache, validating translation completeness, or importing/exporting CSV translations.
---

# Translation Sync

## Capabilities
- Sync topic translations between Finnish and English
- Manage term translation cache
- Validate translation completeness
- Export/import CSV for bulk updates
- Identify missing translations

## Translation Tables

### term_translations (bible_schema)
Caches Finnish ↔ English term translations for search:
```sql
term_fi TEXT
main_term_en TEXT
synonyms_en TEXT[]
ai_main_term_en TEXT
ai_synonyms_en TEXT[]
source TEXT -- 'topic', 'ai', 'manual'
```

### topical_topics (bible_schema)
Topic names in both languages:
```sql
slug TEXT -- English slug
name_en TEXT -- English name
name_fi TEXT -- Finnish name (can be null)
slug_fi TEXT -- Finnish slug (can be null)
is_core BOOLEAN
```

## Usage Examples

### Example 1: Find Missing Topic Translations
**User:** "Find all topics that don't have Finnish translations"

**Assistant:**
```sql
-- Find topics without Finnish translation
SELECT
  id,
  slug,
  name_en,
  name_fi,
  slug_fi,
  CASE
    WHEN name_fi IS NULL AND slug_fi IS NULL THEN 'Both missing'
    WHEN name_fi IS NULL THEN 'Name missing'
    WHEN slug_fi IS NULL THEN 'Slug missing'
  END AS missing_fields
FROM bible_schema.topical_topics
WHERE name_fi IS NULL OR slug_fi IS NULL
ORDER BY is_core DESC, name_en;

-- Count statistics
SELECT
  COUNT(*) as total_topics,
  COUNT(name_fi) as translated_topics,
  COUNT(*) - COUNT(name_fi) as missing_translations,
  ROUND(100.0 * COUNT(name_fi) / COUNT(*), 2) as percent_translated
FROM bible_schema.topical_topics;
```

### Example 2: Bulk Update Topics from CSV
**User:** "Import topic translations from CSV file"

**Assistant:**

First, create CSV format:
```csv
slug,name_fi,slug_fi
forgiveness,anteeksianto,anteeksianto
grace,armo,armo
salvation,pelastus,pelastus
faith,usko,usko
love,rakkaus,rakkaus
```

Then, SQL to import:
```sql
-- Create temporary table for import
CREATE TEMP TABLE topic_translations_import (
  slug TEXT,
  name_fi TEXT,
  slug_fi TEXT
);

-- Import CSV (via Supabase Dashboard or psql)
\copy topic_translations_import FROM 'translations.csv' CSV HEADER;

-- Update topics with translations
UPDATE bible_schema.topical_topics t
SET
  name_fi = i.name_fi,
  slug_fi = i.slug_fi
FROM topic_translations_import i
WHERE t.slug = i.slug;

-- Report on updates
SELECT
  COUNT(*) as updated_count
FROM bible_schema.topical_topics t
JOIN topic_translations_import i ON t.slug = i.slug;

-- Clean up
DROP TABLE topic_translations_import;
```

TypeScript implementation for admin panel:
```typescript
// Component for CSV import
import { useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export const TopicTranslationImporter = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<any[]>([]);
  const { toast } = useToast();

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    setFile(selectedFile);

    // Parse CSV for preview
    const text = await selectedFile.text();
    const lines = text.split('\n').filter(l => l.trim());
    const headers = lines[0].split(',');

    const data = lines.slice(1).map(line => {
      const values = line.split(',');
      return {
        slug: values[0],
        name_fi: values[1],
        slug_fi: values[2]
      };
    });

    setPreview(data.slice(0, 5)); // Show first 5 for preview
  };

  const handleImport = async () => {
    if (!file) return;

    try {
      const text = await file.text();
      const lines = text.split('\n').filter(l => l.trim());

      const updates = lines.slice(1).map(line => {
        const [slug, name_fi, slug_fi] = line.split(',');
        return { slug, name_fi, slug_fi };
      });

      // Update in batches
      let updated = 0;
      for (const update of updates) {
        const { error } = await supabase
          .from('topical_topics')
          .update({
            name_fi: update.name_fi,
            slug_fi: update.slug_fi
          })
          .eq('slug', update.slug);

        if (!error) updated++;
      }

      toast({
        title: "Import complete",
        description: `Updated ${updated} topics`
      });
    } catch (error) {
      toast({
        title: "Import failed",
        description: error.message,
        variant: "destructive"
      });
    }
  };

  return (
    <div className="space-y-4">
      <Input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
      />

      {preview.length > 0 && (
        <div>
          <h4>Preview (first 5 rows):</h4>
          <pre className="bg-gray-100 p-2 rounded">
            {JSON.stringify(preview, null, 2)}
          </pre>
        </div>
      )}

      <Button onClick={handleImport} disabled={!file}>
        Import Translations
      </Button>
    </div>
  );
};
```

### Example 3: Sync Term Translations
**User:** "Add term translation to cache"

**Assistant:**
```typescript
// Function to add/update term translation
async function addTermTranslation(
  termFi: string,
  mainTermEn: string,
  synonymsEn: string[],
  source: 'manual' | 'ai' | 'topic'
) {
  const { data, error } = await supabase.rpc('upsert_term_translation', {
    p_term_fi: termFi,
    p_main_term_en: mainTermEn,
    p_synonyms_en: synonymsEn,
    p_source: source
  });

  if (error) throw error;
  return data;
}

// Usage
await addTermTranslation('armo', 'grace', ['mercy', 'favor'], 'manual');
await addTermTranslation('rakkaus', 'love', ['charity', 'affection'], 'manual');
await addTermTranslation('pelastus', 'salvation', ['redemption'], 'manual');
```

### Example 4: Export Topics to CSV
**User:** "Export all topics with their translations to CSV"

**Assistant:**
```typescript
// Export topics to CSV
async function exportTopicsToCSV() {
  const { data: topics, error } = await supabase
    .from('topical_topics')
    .select('slug, name_en, name_fi, slug_fi, is_core')
    .order('name_en');

  if (error) throw error;

  // Create CSV content
  const headers = ['slug', 'name_en', 'name_fi', 'slug_fi', 'is_core'];
  const rows = topics.map(t => [
    t.slug,
    t.name_en,
    t.name_fi || '',
    t.slug_fi || '',
    t.is_core ? 'true' : 'false'
  ]);

  const csv = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n');

  // Download file
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `topics-export-${new Date().toISOString().split('T')[0]}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

// Component
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";

export const TopicExporter = () => {
  return (
    <Button onClick={exportTopicsToCSV} variant="outline">
      <Download className="h-4 w-4 mr-2" />
      Export Topics CSV
    </Button>
  );
};
```

### Example 5: Validate Translation Completeness
**User:** "Check translation quality and completeness"

**Assistant:**
```sql
-- Translation Quality Report
WITH stats AS (
  SELECT
    COUNT(*) as total,
    COUNT(name_fi) as has_fi_name,
    COUNT(slug_fi) as has_fi_slug,
    COUNT(CASE WHEN name_fi IS NOT NULL AND slug_fi IS NOT NULL THEN 1 END) as fully_translated,
    COUNT(CASE WHEN is_core = true THEN 1 END) as total_core,
    COUNT(CASE WHEN is_core = true AND name_fi IS NOT NULL THEN 1 END) as core_translated
  FROM bible_schema.topical_topics
)
SELECT
  total as "Total Topics",
  fully_translated as "Fully Translated",
  has_fi_name as "Has Finnish Name",
  has_fi_slug as "Has Finnish Slug",
  total_core as "Core Topics",
  core_translated as "Core Translated",
  ROUND(100.0 * fully_translated / total, 2) || '%' as "Completion %",
  ROUND(100.0 * core_translated / total_core, 2) || '%' as "Core Completion %"
FROM stats;

-- Find problematic translations
SELECT
  slug,
  name_en,
  name_fi,
  slug_fi,
  is_core,
  CASE
    WHEN name_fi IS NULL THEN 'Missing Finnish name'
    WHEN slug_fi IS NULL THEN 'Missing Finnish slug'
    WHEN LENGTH(name_fi) < 2 THEN 'Finnish name too short'
    WHEN name_fi = name_en THEN 'Not translated (same as English)'
    ELSE 'OK'
  END as issue
FROM bible_schema.topical_topics
WHERE
  name_fi IS NULL
  OR slug_fi IS NULL
  OR LENGTH(name_fi) < 2
  OR name_fi = name_en
ORDER BY is_core DESC, name_en;
```

## Translation Workflow

### 1. Export Current State
```bash
# Export topics for translation
SELECT slug, name_en, name_fi, slug_fi
FROM bible_schema.topical_topics
WHERE name_fi IS NULL
ORDER BY is_core DESC, name_en;
```

### 2. Translate Content
- Use Google Sheets or Excel
- Finnish column for name_fi
- Create URL-safe slug_fi (lowercase, no spaces)

### 3. Import Translations
```sql
-- Via CSV import (see Example 2)
```

### 4. Validate Import
```sql
-- Check for issues after import
SELECT COUNT(*) FROM bible_schema.topical_topics WHERE name_fi IS NULL;
SELECT COUNT(*) FROM bible_schema.topical_topics WHERE slug_fi IS NULL;
```

## AI-Assisted Translation

Use Edge Function for batch translation:
```typescript
// Edge Function: topic-translations
async function batchTranslateTopics(topics: string[]) {
  const results = [];

  for (const topic of topics) {
    const { data } = await supabase.functions.invoke('translate-search-term', {
      body: {
        term: topic,
        direction: 'en-fi',
        forceAI: true
      }
    });

    results.push({
      original: topic,
      translated: data.translated
    });
  }

  return results;
}
```

## Translation Best Practices

### Finnish Translation Guidelines
1. **Accuracy** - Maintain theological accuracy
2. **Natural Finnish** - Use natural Finnish expressions
3. **Consistency** - Keep consistent with existing translations
4. **Slugs** - Use lowercase, no spaces, URL-safe characters
5. **Length** - Keep reasonably short for UI display

### Common Finnish Translations
| English | Finnish | Slug |
|---------|---------|------|
| Grace | Armo | armo |
| Faith | Usko | usko |
| Love | Rakkaus | rakkaus |
| Salvation | Pelastus | pelastus |
| Forgiveness | Anteeksianto | anteeksianto |
| Hope | Toivo | toivo |
| Prayer | Rukous | rukous |
| Worship | Ylistys | ylistys |

## Admin Panel Integration

The translations can be managed via:
- `AdminTopicsPage` - Topic translations
- `AdminTranslationsPage` - Term translations

See `Docs/07-ADMIN-GUIDE.md` for admin panel usage.

## Related Documentation
- See `Docs/07-ADMIN-GUIDE.md` for admin features
- See `Docs/03-API.md` for term_translations table
- See `Docs/06-AI-ARCHITECTURE.md` for AI translation
