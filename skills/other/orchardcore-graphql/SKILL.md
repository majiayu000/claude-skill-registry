---
name: orchardcore-graphql
description: Skill for configuring and using the GraphQL API in Orchard Core. Covers GraphQL queries, custom types, content type querying, and GraphQL schema customization.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core GraphQL - Prompt Templates

## Configure and Use GraphQL API

You are an Orchard Core expert. Generate GraphQL queries and custom type definitions for Orchard Core.

### Guidelines

- Enable `OrchardCore.Apis.GraphQL` to expose a GraphQL endpoint at `/api/graphql`.
- Content types are automatically exposed as GraphQL types.
- Use the GraphiQL interface at `/admin/graphql` for query exploration.
- Custom GraphQL types can extend the schema for custom data.
- GraphQL queries support filtering, sorting, and pagination.
- Authentication and authorization apply to GraphQL queries.
- Use `WhereInput` types for filtering content items.

### Enabling GraphQL Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Apis.GraphQL"
      ],
      "disable": []
    }
  ]
}
```

### Basic Content Query

```graphql
{
  blogPost {
    contentItemId
    displayText
    createdUtc
    publishedUtc
    titlePart {
      title
    }
    autoroutePart {
      path
    }
    htmlBodyPart {
      html
    }
  }
}
```

### Query with Filtering

```graphql
{
  blogPost(where: {displayText_contains: "orchard"}) {
    contentItemId
    displayText
    publishedUtc
  }
}
```

### Query with Pagination

```graphql
{
  blogPost(first: 10, skip: 0, orderBy: {publishedUtc: DESC}) {
    contentItemId
    displayText
    publishedUtc
  }
}
```

### Query Specific Content Item

```graphql
{
  contentItem(contentItemId: "{{ContentItemId}}") {
    contentItemId
    contentType
    displayText
    publishedUtc
    ... on BlogPost {
      titlePart {
        title
      }
      htmlBodyPart {
        html
      }
    }
  }
}
```

### Query Content Items by Status

```graphql
{
  blogPost(status: PUBLISHED) {
    contentItemId
    displayText
    publishedUtc
  }
}

{
  blogPost(status: DRAFT) {
    contentItemId
    displayText
    modifiedUtc
  }
}

{
  blogPost(status: LATEST) {
    contentItemId
    displayText
    latest
    published
  }
}
```

### Custom GraphQL Object Type

```csharp
using GraphQL.Types;
using OrchardCore.Apis.GraphQL;
using OrchardCore.ContentManagement;

public sealed class MyPartQueryObjectType : ObjectGraphType<MyPart>
{
    public MyPartQueryObjectType()
    {
        Name = "MyPart";

        Field(x => x.MyField)
            .Description("My custom field.");
        Field(x => x.MyNumber)
            .Description("A numeric value.");
    }
}
```

### Custom GraphQL Input Type

```csharp
using GraphQL.Types;

public sealed class MyPartInputObjectType : InputObjectGraphType<MyPart>
{
    public MyPartInputObjectType()
    {
        Name = "MyPartInput";

        Field(x => x.MyField, nullable: true)
            .Description("Filter by my custom field.");
    }
}
```

### Custom GraphQL Filter

```csharp
using OrchardCore.ContentManagement.GraphQL.Queries;

public sealed class MyPartIndexAliasProvider : IIndexAliasProvider
{
    private static readonly IndexAlias[] _aliases = new[]
    {
        new IndexAlias
        {
            Alias = "myPart",
            Index = nameof(MyPartIndex),
            IndexType = typeof(MyPartIndex)
        }
    };

    public IEnumerable<IndexAlias> GetAliases()
    {
        return _aliases;
    }
}
```

### Registering Custom GraphQL Types

```csharp
using OrchardCore.Apis;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddObjectGraphType<MyPart, MyPartQueryObjectType>();
        services.AddInputObjectGraphType<MyPart, MyPartInputObjectType>();
        services.AddScoped<IIndexAliasProvider, MyPartIndexAliasProvider>();
    }
}
```

### Querying with Liquid and GraphQL

Execute GraphQL queries from Liquid templates:

```liquid
{% graphql query: "{ blogPost(first: 5, orderBy: {publishedUtc: DESC}) { displayText, autoroutePart { path } } }" %}
{% for post in graphql.blogPost %}
    <a href="{{ post.autoroutePart.path }}">{{ post.displayText }}</a>
{% endfor %}
```

### Authentication for GraphQL

GraphQL queries respect Orchard Core permissions. For API access:

```bash
# Query with API key
curl -X POST https://example.com/api/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {{token}}" \
  -d '{"query": "{ blogPost { displayText } }"}'
```
