---
name: dynamic-schema-design
description: Use when implementing flexible content schemas using EF Core JSON columns, `OwnsOne().ToJson()` patterns, or designing dynamic field storage that avoids migrations. Covers JSON column configuration, LINQ querying of JSON properties, indexing strategies, and schema evolution patterns for headless CMS architectures.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Dynamic Schema Design with EF Core JSON Columns

Guidance for implementing flexible content schemas using EF Core JSON columns, enabling dynamic custom fields without database migrations.

## When to Use This Skill

- Designing custom field storage for CMS content types
- Implementing dynamic properties that vary per content instance
- Avoiding frequent database migrations for schema changes
- Querying JSON data with LINQ in EF Core
- Planning indexing strategies for JSON columns
- Migrating from EAV (Entity-Attribute-Value) to JSON storage

## EF Core JSON Column Fundamentals

### Basic Configuration (.NET 10 / EF Core 10)

```csharp
// Entity with JSON-stored custom fields
public class ContentItem
{
    public Guid Id { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public DateTime CreatedUtc { get; set; }

    // JSON column for dynamic fields
    public CustomFieldsData CustomFields { get; set; } = new();
}

// Owned entity stored as JSON
public class CustomFieldsData
{
    public Dictionary<string, object?> Fields { get; set; } = new();
    public Dictionary<string, FieldMetadata> Metadata { get; set; } = new();
}

public class FieldMetadata
{
    public string FieldType { get; set; } = string.Empty;
    public bool IsRequired { get; set; }
    public string? DisplayName { get; set; }
}
```

### DbContext Configuration

```csharp
public class ContentDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ContentItem>(entity =>
        {
            entity.HasKey(e => e.Id);

            // Configure JSON column with ToJson()
            entity.OwnsOne(e => e.CustomFields, builder =>
            {
                builder.ToJson();
            });
        });
    }
}
```

## JSON Column Patterns

### Pattern 1: Typed Custom Fields

Best for when field schemas are known at compile time.

```csharp
// Strongly-typed custom fields
public class ArticleFields
{
    public string? Subtitle { get; set; }
    public List<string> Tags { get; set; } = new();
    public AuthorInfo? Author { get; set; }
    public int? ReadTimeMinutes { get; set; }
    public bool IsFeatured { get; set; }
}

public class AuthorInfo
{
    public Guid AuthorId { get; set; }
    public string DisplayName { get; set; } = string.Empty;
    public string? Bio { get; set; }
}

// Entity using typed fields
public class Article
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;

    public ArticleFields Fields { get; set; } = new();
}

// Configuration
modelBuilder.Entity<Article>(entity =>
{
    entity.OwnsOne(e => e.Fields, builder =>
    {
        builder.ToJson();
        builder.OwnsOne(f => f.Author);
    });
});
```

### Pattern 2: Dynamic Property Bag

Best for fully dynamic schemas where fields vary per instance.

```csharp
public class DynamicContent
{
    public Guid Id { get; set; }
    public string ContentType { get; set; } = string.Empty;

    // Flexible property bag
    public JsonDocument? Properties { get; set; }
}

// Alternative using Dictionary
public class FlexibleContent
{
    public Guid Id { get; set; }
    public string ContentType { get; set; } = string.Empty;

    public Dictionary<string, JsonElement> Fields { get; set; } = new();
}
```

### Pattern 3: Hybrid Approach (Recommended)

Combine fixed columns for common fields with JSON for extensions.

```csharp
public class ContentItem
{
    // Fixed columns (indexed, frequently queried)
    public Guid Id { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string? Slug { get; set; }
    public ContentStatus Status { get; set; }
    public DateTime CreatedUtc { get; set; }
    public DateTime? PublishedUtc { get; set; }

    // JSON column for type-specific and custom fields
    public ContentExtensions Extensions { get; set; } = new();
}

public class ContentExtensions
{
    // Part-specific data stored as nested JSON
    public TitlePartData? TitlePart { get; set; }
    public SeoPartData? SeoPart { get; set; }
    public MediaPartData? MediaPart { get; set; }

    // Fully dynamic custom fields
    public Dictionary<string, object?> CustomFields { get; set; } = new();
}
```

## Querying JSON Columns

### LINQ Queries on JSON Properties

```csharp
// Query nested JSON property
var featuredArticles = await context.Articles
    .Where(a => a.Fields.IsFeatured == true)
    .ToListAsync();

// Query nested object property
var articlesByAuthor = await context.Articles
    .Where(a => a.Fields.Author!.AuthorId == authorId)
    .ToListAsync();

// Query array contains
var taggedArticles = await context.Articles
    .Where(a => a.Fields.Tags.Contains("technology"))
    .ToListAsync();

// Order by JSON property
var orderedArticles = await context.Articles
    .OrderByDescending(a => a.Fields.ReadTimeMinutes)
    .ToListAsync();
```

### Raw SQL for Complex JSON Queries

```csharp
// SQL Server JSON_VALUE
var results = await context.ContentItems
    .FromSqlRaw(@"
        SELECT * FROM ContentItems
        WHERE JSON_VALUE(Extensions, '$.CustomFields.rating') > 4
    ")
    .ToListAsync();

// PostgreSQL jsonb operators
var results = await context.ContentItems
    .FromSqlRaw(@"
        SELECT * FROM ""ContentItems""
        WHERE ""Extensions""->>'CustomFields'->>'category' = 'tech'
    ")
    .ToListAsync();
```

## Indexing Strategies

### Computed Columns for Frequently Queried JSON Properties

```sql
-- SQL Server: Add computed column
ALTER TABLE ContentItems
ADD Status AS JSON_VALUE(Extensions, '$.status') PERSISTED;

-- Create index on computed column
CREATE INDEX IX_ContentItems_Status ON ContentItems(Status);
```

### PostgreSQL GIN Index for JSONB

```sql
-- Index entire JSON column
CREATE INDEX IX_ContentItems_Extensions ON "ContentItems"
USING GIN ("Extensions");

-- Index specific path
CREATE INDEX IX_ContentItems_Tags ON "ContentItems"
USING GIN (("Extensions"->'CustomFields'->'tags'));
```

### EF Core Migration for Computed Column

```csharp
migrationBuilder.Sql(@"
    ALTER TABLE ContentItems
    ADD ComputedStatus AS JSON_VALUE(Extensions, '$.SeoPart.noIndex') PERSISTED;

    CREATE INDEX IX_ContentItems_ComputedStatus
    ON ContentItems(ComputedStatus);
");
```

## Schema Evolution

### Adding New Fields

No migration required - just update the class and serialize:

```csharp
// Before
public class ArticleFields
{
    public string? Subtitle { get; set; }
}

// After - no migration needed
public class ArticleFields
{
    public string? Subtitle { get; set; }
    public string? Summary { get; set; }  // New field
    public List<string> RelatedLinks { get; set; } = new();  // New field
}
```

### Handling Missing/Null Properties

```csharp
// Use nullable types with defaults
public class ContentFields
{
    public string? OptionalField { get; set; }
    public int RequiredWithDefault { get; set; } = 0;
    public List<string> CollectionWithDefault { get; set; } = new();
}

// Query with null handling
var items = await context.ContentItems
    .Where(c => c.Extensions.CustomFields != null
             && c.Extensions.CustomFields.ContainsKey("rating"))
    .ToListAsync();
```

### Data Migration for Schema Changes

```csharp
// Background job to migrate existing data
public async Task MigrateContentSchema(ContentDbContext context)
{
    var batchSize = 100;
    var skip = 0;

    while (true)
    {
        var items = await context.ContentItems
            .OrderBy(c => c.Id)
            .Skip(skip)
            .Take(batchSize)
            .ToListAsync();

        if (!items.Any()) break;

        foreach (var item in items)
        {
            // Transform old schema to new
            if (item.Extensions.CustomFields.TryGetValue("old_field", out var value))
            {
                item.Extensions.CustomFields["new_field"] = value;
                item.Extensions.CustomFields.Remove("old_field");
            }
        }

        await context.SaveChangesAsync();
        skip += batchSize;
    }
}
```

## Performance Considerations

### When to Use JSON Columns

| Scenario | Use JSON Column | Use Regular Column |
| -------- | --------------- | ------------------ |
| Frequently filtered/sorted | No | Yes |
| Rarely queried, display only | Yes | No |
| Variable per content type | Yes | No |
| Fixed across all instances | No | Yes |
| Part of unique constraint | No | Yes |
| Full-text search needed | Consider | Yes |

### Best Practices

```text
DO:
- Use hybrid approach (fixed + JSON)
- Index frequently queried JSON paths
- Use typed DTOs when schema is known
- Validate JSON structure in application layer
- Use pagination for large JSON arrays

DON'T:
- Store large binary data in JSON
- Use JSON for foreign key relationships
- Rely solely on JSON queries for performance-critical paths
- Store deeply nested hierarchies (flatten when possible)
- Skip schema validation for user-supplied data
```

## Serialization Configuration

### System.Text.Json Options

```csharp
services.AddDbContext<ContentDbContext>(options =>
{
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        // Configure JSON serialization
    });
});

// Custom JsonSerializerOptions
public static class JsonDefaults
{
    public static JsonSerializerOptions ContentOptions { get; } = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        Converters =
        {
            new JsonStringEnumConverter(JsonNamingPolicy.CamelCase)
        }
    };
}
```

### Custom Type Converters

```csharp
// For complex types not directly serializable
public class PolymorphicFieldConverter : JsonConverter<object>
{
    public override object? Read(ref Utf8JsonReader reader,
        Type typeToConvert, JsonSerializerOptions options)
    {
        using var doc = JsonDocument.ParseValue(ref reader);
        var root = doc.RootElement;

        // Determine type from discriminator
        if (root.TryGetProperty("$type", out var typeElement))
        {
            var typeName = typeElement.GetString();
            // Resolve and deserialize appropriate type
        }

        return root.Clone();
    }

    public override void Write(Utf8JsonWriter writer,
        object value, JsonSerializerOptions options)
    {
        JsonSerializer.Serialize(writer, value, value.GetType(), options);
    }
}
```

## Content Part JSON Storage

### Storing Multiple Parts in Single JSON Column

```csharp
public class ContentItem
{
    public Guid Id { get; set; }
    public string ContentType { get; set; } = string.Empty;

    // All parts stored in single JSON column
    public ContentParts Parts { get; set; } = new();
}

public class ContentParts
{
    public TitlePart? Title { get; set; }
    public BodyPart? Body { get; set; }
    public AutoroutePart? Autoroute { get; set; }
    public PublishLaterPart? PublishLater { get; set; }
    public SeoMetaPart? SeoMeta { get; set; }

    // Extension point for custom parts
    public Dictionary<string, JsonElement> CustomParts { get; set; } = new();
}

// Part definitions
public record TitlePart(string Title, string? DisplayTitle = null);
public record BodyPart(string Html, string? PlainText = null);
public record AutoroutePart(string Path, bool IsCustom = false);
public record PublishLaterPart(DateTime? ScheduledUtc, string? TimeZone = null);
public record SeoMetaPart(string? MetaTitle, string? MetaDescription, bool NoIndex = false);
```

## Validation Patterns

### Fluent Validation for JSON Fields

```csharp
public class ContentItemValidator : AbstractValidator<ContentItem>
{
    public ContentItemValidator(IContentTypeRegistry typeRegistry)
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(200);

        RuleFor(x => x.Extensions)
            .SetValidator(new ContentExtensionsValidator(typeRegistry));
    }
}

public class ContentExtensionsValidator : AbstractValidator<ContentExtensions>
{
    public ContentExtensionsValidator(IContentTypeRegistry typeRegistry)
    {
        When(x => x.SeoPart != null, () =>
        {
            RuleFor(x => x.SeoPart!.MetaTitle)
                .MaximumLength(60)
                .When(x => x.SeoPart?.MetaTitle != null);

            RuleFor(x => x.SeoPart!.MetaDescription)
                .MaximumLength(160)
                .When(x => x.SeoPart?.MetaDescription != null);
        });
    }
}
```

## Related Skills

- `content-type-modeling` - Content Type hierarchy and composition
- `content-versioning` - Version history with JSON snapshots
- `headless-api-design` - API contracts for JSON-based content
