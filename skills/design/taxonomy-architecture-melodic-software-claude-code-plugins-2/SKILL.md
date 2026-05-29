---
name: taxonomy-architecture
description: Use when designing category hierarchies, tag systems, faceted classification, or vocabulary management for content organization. Covers flat vs hierarchical taxonomies, term relationships, multi-taxonomy content, and taxonomy APIs for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Taxonomy Architecture

Guidance for designing taxonomy systems for content classification, including categories, tags, and faceted navigation.

## When to Use This Skill

- Designing category hierarchies for content
- Implementing tagging systems
- Planning faceted search and filtering
- Creating controlled vocabularies
- Migrating taxonomy structures between CMS platforms

## Taxonomy Types

### Flat Taxonomy (Tags)

Best for user-generated, flexible classification.

```csharp
public class Tag
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public int UsageCount { get; set; }
}

public class ContentTag
{
    public Guid ContentItemId { get; set; }
    public Guid TagId { get; set; }
    public int Order { get; set; }
}
```

**Use Cases:**

- Blog post tags
- Product keywords
- User-generated labels
- Folksonomy systems

### Hierarchical Taxonomy (Categories)

Best for structured, controlled classification.

```csharp
public class Category
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public string? Description { get; set; }

    // Hierarchy
    public Guid? ParentId { get; set; }
    public Category? Parent { get; set; }
    public List<Category> Children { get; set; } = new();

    // Materialized path for efficient queries
    public string Path { get; set; } = string.Empty; // e.g., "/tech/programming/csharp"
    public int Depth { get; set; }
    public int Order { get; set; }
}
```

**Use Cases:**

- Product categories (Electronics > Phones > Smartphones)
- Document classification
- Geographic hierarchies
- Organizational structures

### Multi-Taxonomy System

Support multiple independent taxonomies.

```csharp
public class Taxonomy
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public TaxonomyType Type { get; set; } // Flat, Hierarchical
    public bool AllowMultiple { get; set; } = true;
    public bool IsRequired { get; set; }
    public List<string> ApplicableContentTypes { get; set; } = new();
}

public class TaxonomyTerm
{
    public Guid Id { get; set; }
    public Guid TaxonomyId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;

    // For hierarchical taxonomies
    public Guid? ParentTermId { get; set; }
    public string? Path { get; set; }
    public int Depth { get; set; }
    public int Order { get; set; }

    // Metadata
    public Dictionary<string, object?> Metadata { get; set; } = new();
}

public enum TaxonomyType
{
    Flat,       // Tags, keywords
    Hierarchical, // Categories with parent/child
    Faceted     // Multi-dimensional classification
}
```

## Hierarchy Patterns

### Adjacency List (Simple)

```sql
CREATE TABLE Categories (
    Id UNIQUEIDENTIFIER PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,
    ParentId UNIQUEIDENTIFIER NULL REFERENCES Categories(Id),
    [Order] INT NOT NULL DEFAULT 0
);

-- Query children (one level)
SELECT * FROM Categories WHERE ParentId = @parentId ORDER BY [Order];

-- Recursive CTE for full tree
WITH CategoryTree AS (
    SELECT Id, Name, ParentId, 0 AS Depth
    FROM Categories WHERE ParentId IS NULL
    UNION ALL
    SELECT c.Id, c.Name, c.ParentId, ct.Depth + 1
    FROM Categories c
    INNER JOIN CategoryTree ct ON c.ParentId = ct.Id
)
SELECT * FROM CategoryTree;
```

### Materialized Path (Fast Reads)

```sql
CREATE TABLE Categories (
    Id UNIQUEIDENTIFIER PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,
    Path NVARCHAR(1000) NOT NULL, -- '/root/parent/child'
    Depth INT NOT NULL,
    [Order] INT NOT NULL
);

CREATE INDEX IX_Categories_Path ON Categories(Path);

-- Query all descendants
SELECT * FROM Categories WHERE Path LIKE '/electronics/phones/%';

-- Query ancestors
SELECT * FROM Categories
WHERE '/electronics/phones/smartphones' LIKE Path + '%'
ORDER BY Depth;
```

### Nested Set (Complex but Powerful)

```sql
CREATE TABLE Categories (
    Id UNIQUEIDENTIFIER PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,
    Lft INT NOT NULL,  -- Left boundary
    Rgt INT NOT NULL,  -- Right boundary
    Depth INT NOT NULL
);

-- Query all descendants
SELECT * FROM Categories
WHERE Lft > @parentLft AND Rgt < @parentRgt
ORDER BY Lft;

-- Query ancestors
SELECT * FROM Categories
WHERE Lft < @childLft AND Rgt > @childRgt
ORDER BY Lft;
```

## Faceted Classification

### Facet Design

```csharp
public class Facet
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public FacetType Type { get; set; }
    public List<FacetValue> Values { get; set; } = new();
}

public class FacetValue
{
    public Guid Id { get; set; }
    public Guid FacetId { get; set; }
    public string Value { get; set; } = string.Empty;
    public string? DisplayValue { get; set; }
    public int Order { get; set; }
}

public enum FacetType
{
    SingleSelect,   // Radio buttons
    MultiSelect,    // Checkboxes
    Range,          // Price range, date range
    Boolean,        // Yes/No
    Hierarchy       // Nested options
}

// Product with facets
public class ProductFacets
{
    public List<Guid> BrandIds { get; set; } = new();
    public List<Guid> ColorIds { get; set; } = new();
    public decimal? PriceMin { get; set; }
    public decimal? PriceMax { get; set; }
    public bool? InStock { get; set; }
}
```

### Faceted Search Query

```csharp
public class FacetedSearchQuery
{
    public string? SearchTerm { get; set; }
    public Dictionary<string, List<string>> Facets { get; set; } = new();
    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 20;
}

public class FacetedSearchResult<T>
{
    public List<T> Items { get; set; } = new();
    public int TotalCount { get; set; }
    public Dictionary<string, List<FacetCount>> FacetCounts { get; set; } = new();
}

public class FacetCount
{
    public string Value { get; set; } = string.Empty;
    public string DisplayValue { get; set; } = string.Empty;
    public int Count { get; set; }
    public bool IsSelected { get; set; }
}
```

## Taxonomy API Design

### REST Endpoints

```text
GET    /api/taxonomies                    # List all taxonomies
GET    /api/taxonomies/{id}               # Get taxonomy with terms
GET    /api/taxonomies/{id}/terms         # List terms (flat or tree)
GET    /api/taxonomies/{id}/terms/{termId} # Get single term

# Hierarchical navigation
GET    /api/categories                    # Root categories
GET    /api/categories/{id}/children      # Child categories
GET    /api/categories/{id}/ancestors     # Breadcrumb path
GET    /api/categories/{id}/descendants   # Full subtree

# Content by taxonomy
GET    /api/articles?category={slug}
GET    /api/articles?tags=tag1,tag2
GET    /api/products?facets[brand]=apple&facets[color]=black
```

### GraphQL Schema

```graphql
type Taxonomy {
  id: ID!
  name: String!
  slug: String!
  type: TaxonomyType!
  terms(parentId: ID): [TaxonomyTerm!]!
  termTree: [TaxonomyTerm!]!
}

type TaxonomyTerm {
  id: ID!
  name: String!
  slug: String!
  path: String
  depth: Int!
  parent: TaxonomyTerm
  children: [TaxonomyTerm!]!
  contentCount: Int!
}

type Query {
  taxonomies: [Taxonomy!]!
  taxonomy(id: ID, slug: String): Taxonomy
  categoryByPath(path: String!): TaxonomyTerm
}
```

## Best Practices

### Naming Conventions

| Pattern | Example | Use For |
| ------- | ------- | ------- |
| Singular | Category, Tag | Entity names |
| Plural | Categories, Tags | Collection endpoints |
| Slug format | `web-development` | URL-safe identifiers |
| Path format | `/tech/web/frontend` | Hierarchical paths |

### Performance Optimization

```csharp
// Cache taxonomy trees (they change infrequently)
public class TaxonomyCacheService
{
    private readonly IMemoryCache _cache;
    private readonly TimeSpan _cacheDuration = TimeSpan.FromMinutes(30);

    public async Task<List<TaxonomyTerm>> GetTermTreeAsync(Guid taxonomyId)
    {
        var cacheKey = $"taxonomy:tree:{taxonomyId}";

        if (!_cache.TryGetValue(cacheKey, out List<TaxonomyTerm>? tree))
        {
            tree = await BuildTermTreeAsync(taxonomyId);
            _cache.Set(cacheKey, tree, _cacheDuration);
        }

        return tree!;
    }

    public void InvalidateCache(Guid taxonomyId)
    {
        _cache.Remove($"taxonomy:tree:{taxonomyId}");
    }
}
```

### Content Count Denormalization

```csharp
// Update counts when content is published/unpublished
public class ContentPublishedHandler : INotificationHandler<ContentPublishedEvent>
{
    public async Task Handle(ContentPublishedEvent notification, CancellationToken ct)
    {
        // Increment term counts
        foreach (var termId in notification.TaxonomyTermIds)
        {
            await _termRepository.IncrementCountAsync(termId);
        }
    }
}
```

## Related Skills

- `content-type-modeling` - Attaching taxonomies to content types
- `content-relationships` - Term-to-content relationships
- `headless-api-design` - Taxonomy API endpoints
