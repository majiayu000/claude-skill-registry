---
name: product-search-scoring
description: Advanced product search system with keyword scoring, Vietnamese text normalization, multi-field matching, and search result ranking. USE WHEN implementing search functionality, adding keyword scoring to products, optimizing search algorithm, or improving search relevance.
---
## When to Activate This Skill

- User says "tìm kiếm sản phẩm", "search products", "implement search"
- Task involves search algorithm or keyword matching
- Need to add scoring/ranking to search results
- Improving search relevance or performance
- Implementing Vietnamese text search with accent handling
- Adding search analytics or trending keywords

## Core Architecture

### 3-Component System

**Component 1: Text Normalization**
- Remove Vietnamese accents (à, á, ả... → a)
- Convert to lowercase
- Strip special characters
- Normalize whitespace

**Component 2: Keyword Processing**
- Split search input into individual terms
- Filter stop words (từ, của, với, theo, etc.)
- Remove empty terms
- Maintain search index for fast lookup

**Component 3: Query Building & Sorting**
- Multi-field search (name, brand, type, tags)
- Multiple filter criteria (category, price, tags)
- Relevance-based sorting
- Pagination support

## Cache Strategy

Implement caching to prevent repeated searches:

```php
// Generate cache key from filters
protected function makeCacheKey(array $filters): string
{
    return 'product_filter_ids:' . md5(json_encode($filters));
}

// Cache product IDs from filter query
$cacheKey = $this->makeCacheKey($filters);
$cacheTtl = ProductCacheService::SHORT_CACHE_TTL; // e.g., 300 seconds

$allProductIds = Cache::remember($cacheKey, $cacheTtl, function () use ($filters) {
    $idQuery = Product::query()->select('products.id');
    $this->applyFilters($idQuery, $filters);
    $this->applySort($idQuery, $filters['sort']);
    return $idQuery->pluck('products.id')->all();
});
```

## Search Index Field

Maintain a denormalized `search_index` column on products:

```php
// In Product model migration or observer
$searchIndex = StringHelper::normalizeForSearch(
    implode(' ', [
        $product->name,
        $product->brand,
        $product->type,
        $product->tags->pluck('name')->join(' ')
    ])
);

$product->update(['search_index' => $searchIndex]);
```

## Keyword Highlighting

Display found keywords highlighted in results:

```php
public static function highlightSearchTerm(string $text, string $searchTerm): string
{
    if (empty($searchTerm)) return e($text);

    $searchTerms = self::splitSearchTerms($searchTerm);
    $highlighted = $text;

    foreach ($searchTerms as $term) {
        $pattern = '/(' . preg_quote($term, '/') . ')/i';
        $highlighted = preg_replace($pattern, 
            '<mark class="bg-yellow-200">$1</mark>', 
            $highlighted
        );
    }

    return $highlighted;
}
```

## Common Patterns

### Pattern 1: Simple Text Search
User searches "giày nike" → Find products with name containing both terms

### Pattern 2: Category Filter + Search
User filters by "Tất, vớ" + searches "cotton" → Show cotton socks/stockings

### Pattern 3: Brand Filter + Sort
User selects "Nike" brand + sorts by price ascending → Show Nike products cheapest first

### Pattern 4: Multi-filter
User selects type + brand + tags + searches → Combine all filters with AND/OR logic

## Key Principles

1. **Normalize Vietnamese text** - Accent removal essential for accurate matching
2. **Filter stop words** - Remove common Vietnamese words to improve relevance
3. **Use search_index** - Denormalize search field for performance
4. **Cache aggressively** - Cache filter results by normalized filter key
5. **Multi-field search** - Search across name, brand, type, tags
6. **Flexible filtering** - Support category, brand, price, tag filters
7. **Pagination-friendly** - Cache IDs, then fetch only needed records

## Scoring Improvements (Advanced)

For production, consider these enhancements:

- **Exact match boost**: Higher score if full search term matches product name
- **Field weighting**: Name match worth more than tag match
- **Freshness**: Newer products ranked higher when relevance is equal
- **Popularity**: Track search term frequency for trending keywords
- **User behavior**: Click-through rate and sales indicate relevance

## Critical Requirements

- ⚠️ Always normalize Vietnamese text (accents cause 90% of missed matches)
- ⚠️ Update search_index when product name/brand/type changes
- ⚠️ Cache search queries (major performance bottleneck)
- ✅ Support multiple filter combinations
- ✅ Handle pagination efficiently

## Related Skills

- **image-management**: Use for product images in search results
- **filament-rules**: For admin panel to manage products
- **database-backup**: Before migrating to add search_index column

## Supplementary Resources

For comprehensive implementation guide: `read .claude/skills/workflows/product-search-scoring/CLAUDE.md`


---

## References

**Implementation Steps:** `read .claude/skills/workflows/product-search-scoring/references/implementation-steps.md`
