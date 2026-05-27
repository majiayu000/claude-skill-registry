---
name: bible-lookup-helper
description: Expert assistant for Bible reference lookups and RPC function usage in the KR92 Bible Voice project. Use when fetching Bible verses, generating verse lookups, validating references, working with OSIS format, or choosing optimal lookup patterns.
---

# Bible Lookup Helper

## Capabilities
- Generate correct RPC function calls for Bible lookups
- Validate OSIS reference formats
- Suggest optimal lookup patterns (verse vs chapter vs range)
- Provide book name aliases and normalization
- Convert between different reference formats

## Usage Examples

### Example 1: Generate RPC call for single verse
**User:** "How do I fetch John 3:16 in Finnish?"
**Assistant:**
```typescript
const { data } = await supabase.rpc('get_verse_by_ref', {
  p_ref_book: 'John',
  p_chapter: 3,
  p_verse: 16,
  p_version_code: 'finstlk201',
  p_language_code: 'fi'
});
```

### Example 2: Generate RPC call for chapter
**User:** "Get all verses from Genesis chapter 1"
**Assistant:**
```typescript
const { data: verses } = await supabase.rpc('get_chapter_by_ref', {
  p_ref_book: 'Genesis',
  p_chapter: 1,
  p_version_code: 'finstlk201',
  p_language_code: 'fi'
});
```

### Example 3: Validate reference format
**User:** "Is '1. Joh.4:8' a valid reference?"
**Assistant:** Yes, this is valid. It follows the Finnish format for numbered books:
- Book: 1. Johannes (1 John)
- Chapter: 4
- Verse: 8

Alternative valid formats:
- `1 Joh.4:8` (without period after number)
- `1.Joh.4:8` (no space)
- `1 John 4:8` (English)

### Example 4: Convert reference formats
**User:** "Convert 'Joh.3:16' to OSIS format"
**Assistant:** OSIS format: `John.3.16`

Finnish formats accepted:
- `Joh.3:16` (with colon)
- `Joh.3.16` (with period)
- `Johannes 3:16` (full name)

## Available RPC Functions

### Single Verse
```sql
get_verse_by_ref(p_ref_book, p_chapter, p_verse, p_version_code, p_language_code)
→ {osis, text_content, verse_id}
```

### Full Chapter
```sql
get_chapter_by_ref(p_ref_book, p_chapter, p_version_code, p_language_code)
→ [{book_code, book_name, chapter_number, verse_number, osis, text_content, verse_id, version_code}]
```

### Verse Range
```sql
get_verses_by_ref(p_ref_book, p_chapter, p_verses[], p_version_code, p_language_code)
→ Same as chapter but filtered
```

### Verse Study (with Strong's)
```sql
get_verse_study_data(p_version_code, p_book_name, p_chapter, p_verse)
→ Full study data including KJV Strong's tags
```

### Text Search
```sql
search_text(p_query, p_version_code, p_limit)
search_text_extended(p_query, p_version_code, p_limit)
→ [{book_name, chapter_number, verse_number, osis, text_content, verse_id}]
```

## Supported Bible Versions

| Code | Name | Language |
|------|------|----------|
| `finstlk201` | Pyhä Raamattu (STLK 2017) - DEFAULT | Finnish |
| `finpr_finn` | Pyhä Raamattu (1933/1938) | Finnish |
| `KJV` | King James Version with Strong's | English |

## Book Name Aliases

The system recognizes multiple formats:
- **Finnish:** Joh, Johannes, Johanneksen evankeliumi
- **English:** John, Jn, Gospel of John
- **Numbered books:** 1. Joh, 1 Joh, 1Joh, 1 John
- **Moses books:** 1. Moos, 1 Moos, Gen, Genesis

## Best Practices

1. **Always use RPC functions** - Never query tables directly
2. **Default version** - Use `finstlk201` for Finnish content
3. **Cache results** - Use React Query to cache lookups
4. **Preload** - Load next chapter for better UX
5. **Error handling** - Check for empty results
6. **OSIS format** - Use for cross-version references

## Performance Tips

- Single verse: ~20ms
- Full chapter: ~50ms
- Text search: ~100ms
- Use indexed fields for best performance
- Limit search results with `p_limit` parameter

## Reference Format Patterns

### Valid Formats
- `Book.Chapter:Verse` - e.g., `Joh.3:16`
- `Book.Chapter.Verse` - e.g., `Joh.3.16`
- `Book Chapter:Verse` - e.g., `John 3:16`
- `Number. Book.Chapter:Verse` - e.g., `1. Joh.4:8`

### Range Formats
- `Book.Chapter:Verse-Verse` - e.g., `Joh.3:16-17`
- `Book.Chapter:Verse-Chapter:Verse` - e.g., `Joh.3:16-4:2`

## Related Documentation
- See `Docs/05-DEV.md` for detailed lookup patterns
- See `Docs/03-API.md` for complete API reference
