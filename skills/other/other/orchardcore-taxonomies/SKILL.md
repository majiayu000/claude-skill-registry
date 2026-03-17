---
name: orchardcore-taxonomies
description: Skill for creating and managing taxonomies in Orchard Core. Covers taxonomy creation, taxonomy terms, taxonomy fields, and taxonomy-based content organization.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Taxonomies - Prompt Templates

## Create and Manage Taxonomies

You are an Orchard Core expert. Generate taxonomy definitions, terms, and taxonomy field configurations.

### Guidelines

- Enable `OrchardCore.Taxonomies` to use taxonomy features.
- A Taxonomy is a content item of type `Taxonomy` that contains terms.
- Terms are hierarchical content items within a taxonomy.
- Use `TaxonomyField` on content types to allow categorization.
- Taxonomies can be flat (tags) or hierarchical (categories).
- Terms can have custom content parts and fields.
- Use `TermPart` for content items that serve as taxonomy terms.

### Enabling Taxonomy Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Taxonomies"
      ],
      "disable": []
    }
  ]
}
```

### Creating a Taxonomy via Recipe

```json
{
  "steps": [
    {
      "name": "Content",
      "data": [
        {
          "ContentItemId": "{{TaxonomyId}}",
          "ContentType": "Taxonomy",
          "DisplayText": "{{TaxonomyName}}",
          "Latest": true,
          "Published": true,
          "TitlePart": {
            "Title": "{{TaxonomyName}}"
          },
          "AliasPart": {
            "Alias": "{{taxonomy-alias}}"
          },
          "TaxonomyPart": {
            "Terms": [
              {
                "ContentItemId": "{{TermId1}}",
                "ContentType": "{{TermContentType}}",
                "DisplayText": "{{TermName1}}",
                "TitlePart": {
                  "Title": "{{TermName1}}"
                }
              },
              {
                "ContentItemId": "{{TermId2}}",
                "ContentType": "{{TermContentType}}",
                "DisplayText": "{{TermName2}}",
                "TitlePart": {
                  "Title": "{{TermName2}}"
                }
              }
            ],
            "TermContentType": "{{TermContentType}}"
          }
        }
      ]
    }
  ]
}
```

### Hierarchical Terms (Nested)

```json
{
  "ContentItemId": "term-parent",
  "ContentType": "Category",
  "DisplayText": "Parent Category",
  "TitlePart": {
    "Title": "Parent Category"
  },
  "Terms": [
    {
      "ContentItemId": "term-child-1",
      "ContentType": "Category",
      "DisplayText": "Child Category 1",
      "TitlePart": {
        "Title": "Child Category 1"
      }
    },
    {
      "ContentItemId": "term-child-2",
      "ContentType": "Category",
      "DisplayText": "Child Category 2",
      "TitlePart": {
        "Title": "Child Category 2"
      }
    }
  ]
}
```

### Attaching TaxonomyField to a Content Type

```csharp
_contentDefinitionManager.AlterPartDefinition("BlogPost", part => part
    .WithField("Categories", field => field
        .OfType("TaxonomyField")
        .WithDisplayName("Categories")
        .WithSettings(new TaxonomyFieldSettings
        {
            TaxonomyContentItemId = "{{TaxonomyContentItemId}}",
            Unique = false,
            LeavesOnly = false
        })
        .WithPosition("0")
    )
    .WithField("Tags", field => field
        .OfType("TaxonomyField")
        .WithDisplayName("Tags")
        .WithEditor("Tags")
        .WithSettings(new TaxonomyFieldSettings
        {
            TaxonomyContentItemId = "{{TagsTaxonomyContentItemId}}"
        })
        .WithPosition("1")
    )
);
```

### Querying by Taxonomy Terms in Liquid

```liquid
{% assign items = Content | where: "Content.BlogPost.Categories.TermContentItemIds", "contains", termId %}
```

### Displaying Taxonomy Terms

```liquid
{% for termId in Model.ContentItem.Content.BlogPost.Categories.TermContentItemIds %}
    {% assign term = termId | content_item %}
    <span class="badge">{{ term.DisplayText }}</span>
{% endfor %}
```

### Custom Term Content Type

Create a custom term type with additional fields:

```csharp
_contentDefinitionManager.AlterTypeDefinition("Category", type => type
    .DisplayedAs("Category")
    .Stereotype("Term")
    .WithPart("TitlePart")
    .WithPart("Category", part => part
        .WithPosition("1")
    )
);

_contentDefinitionManager.AlterPartDefinition("Category", part => part
    .WithField("Icon", field => field
        .OfType("TextField")
        .WithDisplayName("Icon CSS Class")
        .WithPosition("0")
    )
    .WithField("Description", field => field
        .OfType("TextField")
        .WithDisplayName("Description")
        .WithEditor("TextArea")
        .WithPosition("1")
    )
);
```
