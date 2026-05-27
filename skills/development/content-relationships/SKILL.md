---
name: content-relationships
description: Use when designing references between content items, content picker fields, many-to-many relationships, or bidirectional links. Covers relationship types, reference integrity, eager/lazy loading, and relationship APIs for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Content Relationships

Guidance for designing and implementing relationships between content items in headless CMS architectures.

## When to Use This Skill

- Adding content picker fields to content types
- Designing author-article relationships
- Implementing related content features
- Building content hierarchies (parent/child pages)
- Managing bidirectional relationships
- Handling reference integrity on delete

## Relationship Types

### One-to-Many (Parent Reference)

```csharp
// Article has one Author
public class Article
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;

    // Foreign key to Author
    public Guid AuthorId { get; set; }
    public Author? Author { get; set; }
}

public class Author
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;

    // Navigation property (inverse)
    public List<Article> Articles { get; set; } = new();
}
```

### Many-to-Many (Junction Table)

```csharp
// Article has many Categories, Category has many Articles
public class Article
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public List<ArticleCategory> ArticleCategories { get; set; } = new();
}

public class Category
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<ArticleCategory> ArticleCategories { get; set; } = new();
}

public class ArticleCategory
{
    public Guid ArticleId { get; set; }
    public Article Article { get; set; } = null!;

    public Guid CategoryId { get; set; }
    public Category Category { get; set; } = null!;

    // Optional: relationship metadata
    public int Order { get; set; }
    public bool IsPrimary { get; set; }
}

// EF Core configuration
modelBuilder.Entity<ArticleCategory>()
    .HasKey(ac => new { ac.ArticleId, ac.CategoryId });
```

### Self-Referential (Hierarchy)

```csharp
// Page hierarchy
public class Page
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;

    public Guid? ParentId { get; set; }
    public Page? Parent { get; set; }
    public List<Page> Children { get; set; } = new();

    // Computed path for efficient queries
    public string Path { get; set; } = string.Empty;
    public int Depth { get; set; }
}
```

### Polymorphic References (Any Content Type)

```csharp
// Reference to any content item
public class ContentReference
{
    public Guid ReferencingItemId { get; set; }
    public string ReferencingItemType { get; set; } = string.Empty;

    public Guid ReferencedItemId { get; set; }
    public string ReferencedItemType { get; set; } = string.Empty;

    public string RelationshipType { get; set; } = string.Empty; // "related", "featured", "see-also"
    public int Order { get; set; }
}

// Usage: Article references Product, Page, or another Article
```

## Content Picker Field Pattern

### Generic Content Picker

```csharp
public class ContentPickerField
{
    // Allowed content types for this picker
    public List<string> AllowedContentTypes { get; set; } = new();

    // Selected content item IDs
    public List<Guid> ContentItemIds { get; set; } = new();

    // Min/max selection
    public int? MinItems { get; set; }
    public int? MaxItems { get; set; }

    // Display options
    public bool ShowContentType { get; set; } = true;
    public string DisplayTemplate { get; set; } = "{Title}";
}

// Stored in JSON column
public class ArticleExtensions
{
    public ContentPickerField? RelatedArticles { get; set; }
    public ContentPickerField? FeaturedProducts { get; set; }
}
```

### Resolved References for API

```csharp
public class ContentPickerFieldDto
{
    public List<Guid> ContentItemIds { get; set; } = new();

    // Optionally include resolved items
    public List<ContentItemSummary>? Items { get; set; }
}

public class ContentItemSummary
{
    public Guid Id { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public string DisplayText { get; set; } = string.Empty;
    public string? Url { get; set; }
    public string? ThumbnailUrl { get; set; }
}
```

## Relationship Loading Strategies

### Eager Loading

```csharp
// Load relationships with initial query
public async Task<Article?> GetArticleWithRelationsAsync(Guid id)
{
    return await _context.Articles
        .Include(a => a.Author)
        .Include(a => a.ArticleCategories)
            .ThenInclude(ac => ac.Category)
        .FirstOrDefaultAsync(a => a.Id == id);
}
```

### Explicit Loading

```csharp
// Load relationships on demand
public async Task LoadAuthorAsync(Article article)
{
    await _context.Entry(article)
        .Reference(a => a.Author)
        .LoadAsync();
}

public async Task LoadCategoriesAsync(Article article)
{
    await _context.Entry(article)
        .Collection(a => a.ArticleCategories)
        .Query()
        .Include(ac => ac.Category)
        .LoadAsync();
}
```

### Projection for API

```csharp
// Only load what's needed for the response
public async Task<ArticleDto?> GetArticleDtoAsync(Guid id)
{
    return await _context.Articles
        .Where(a => a.Id == id)
        .Select(a => new ArticleDto
        {
            Id = a.Id,
            Title = a.Title,
            AuthorName = a.Author!.Name,
            Categories = a.ArticleCategories
                .Select(ac => ac.Category.Name)
                .ToList()
        })
        .FirstOrDefaultAsync();
}
```

## Bidirectional Relationships

### Maintaining Both Directions

```csharp
public class RelatedContent
{
    public Guid SourceId { get; set; }
    public Guid TargetId { get; set; }
    public string RelationType { get; set; } = string.Empty;
    public bool IsBidirectional { get; set; }
}

public class ContentRelationshipService
{
    public async Task AddRelationshipAsync(
        Guid sourceId,
        Guid targetId,
        string relationType,
        bool bidirectional = true)
    {
        // Add forward relationship
        await _repository.AddAsync(new RelatedContent
        {
            SourceId = sourceId,
            TargetId = targetId,
            RelationType = relationType,
            IsBidirectional = bidirectional
        });

        // Add reverse relationship if bidirectional
        if (bidirectional)
        {
            await _repository.AddAsync(new RelatedContent
            {
                SourceId = targetId,
                TargetId = sourceId,
                RelationType = GetReverseType(relationType),
                IsBidirectional = true
            });
        }
    }

    private string GetReverseType(string type) => type switch
    {
        "parent-of" => "child-of",
        "child-of" => "parent-of",
        "references" => "referenced-by",
        _ => type // symmetric relationships like "related-to"
    };
}
```

## Reference Integrity

### Delete Behaviors

```csharp
public enum ReferenceDeleteBehavior
{
    Restrict,    // Prevent delete if referenced
    Cascade,     // Delete referencing items
    SetNull,     // Clear the reference
    NoAction     // Leave orphans (handle in app)
}

// EF Core configuration
modelBuilder.Entity<Article>()
    .HasOne(a => a.Author)
    .WithMany(a => a.Articles)
    .HasForeignKey(a => a.AuthorId)
    .OnDelete(DeleteBehavior.Restrict);
```

### Orphan Detection

```csharp
public class OrphanDetectionService
{
    public async Task<List<ContentReference>> FindOrphanReferencesAsync()
    {
        // Find references where target no longer exists
        return await _context.ContentReferences
            .Where(r => !_context.ContentItems
                .Any(c => c.Id == r.ReferencedItemId))
            .ToListAsync();
    }

    public async Task<List<ContentItem>> FindUnreferencedContentAsync(
        string contentType)
    {
        // Find content not referenced by anything
        var referencedIds = await _context.ContentReferences
            .Where(r => r.ReferencedItemType == contentType)
            .Select(r => r.ReferencedItemId)
            .Distinct()
            .ToListAsync();

        return await _context.ContentItems
            .Where(c => c.ContentType == contentType)
            .Where(c => !referencedIds.Contains(c.Id))
            .ToListAsync();
    }
}
```

## API Design for Relationships

### REST Patterns

```text
# Include related in single request
GET /api/articles/{id}?include=author,categories

# Nested resources
GET /api/articles/{id}/author
GET /api/articles/{id}/categories
GET /api/authors/{id}/articles

# Relationship management
POST   /api/articles/{id}/relationships/categories
DELETE /api/articles/{id}/relationships/categories/{categoryId}
PUT    /api/articles/{id}/relationships/author
```

### Response with Includes

```json
{
  "data": {
    "id": "article-123",
    "type": "Article",
    "attributes": {
      "title": "My Article"
    },
    "relationships": {
      "author": {
        "data": { "id": "author-456", "type": "Author" }
      },
      "categories": {
        "data": [
          { "id": "cat-1", "type": "Category" },
          { "id": "cat-2", "type": "Category" }
        ]
      }
    }
  },
  "included": [
    {
      "id": "author-456",
      "type": "Author",
      "attributes": { "name": "Jane Doe" }
    },
    {
      "id": "cat-1",
      "type": "Category",
      "attributes": { "name": "Technology" }
    }
  ]
}
```

### GraphQL Relationships

```graphql
type Article {
  id: ID!
  title: String!
  author: Author!
  categories: [Category!]!
  relatedArticles(first: Int): [Article!]!
}

type Query {
  article(id: ID!): Article

  # Reverse lookup
  articlesByAuthor(authorId: ID!): [Article!]!
  articlesByCategory(categoryId: ID!): [Article!]!
}
```

## Related Skills

- `content-type-modeling` - Defining relationship fields
- `dynamic-schema-design` - Storing references in JSON
- `headless-api-design` - Relationship API endpoints
