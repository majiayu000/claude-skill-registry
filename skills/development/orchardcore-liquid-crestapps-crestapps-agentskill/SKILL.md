---
name: orchardcore-liquid
description: Skill for using Liquid templates in Orchard Core. Covers Liquid syntax, Orchard Core-specific filters and tags, shape rendering, content access, and Liquid best practices.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Liquid - Prompt Templates

## Write Liquid Templates

You are an Orchard Core expert. Generate Liquid templates using Orchard Core-specific tags, filters, and conventions.

### Guidelines

- Orchard Core extends Liquid with custom tags, filters, and objects.
- Liquid templates use `.liquid` file extension in the `Views/` folder.
- Access content item data through `Model.ContentItem`.
- Use `{% shape %}` tag to render shapes.
- Use `{% zone %}` tag to render zone content.
- Use `{% resources %}` tag to include CSS/JS resources.
- Liquid templates can be used in content fields (via Liquid Part) and display templates.
- Always prefer Liquid filters for safe HTML output.

### Global Objects

Available global objects in Orchard Core Liquid templates:

```liquid
{{ Site.SiteName }}           - Site name
{{ Site.BaseUrl }}            - Site base URL
{{ Site.Culture }}            - Current culture
{{ Culture.Name }}            - Current culture name (e.g., "en-US")
{{ User.Identity.Name }}      - Current user name
{{ Request.Path }}            - Current request path
{{ Request.QueryString }}     - Query string
```

### Content Item Access

```liquid
{{ Model.ContentItem.ContentType }}           - Content type name
{{ Model.ContentItem.DisplayText }}           - Display text
{{ Model.ContentItem.ContentItemId }}         - Unique content item ID
{{ Model.ContentItem.ContentItemVersionId }}  - Version ID
{{ Model.ContentItem.PublishedUtc }}          - Published date
{{ Model.ContentItem.CreatedUtc }}           - Created date
{{ Model.ContentItem.ModifiedUtc }}          - Modified date
{{ Model.ContentItem.Owner }}                - Owner user ID
{{ Model.ContentItem.Author }}               - Author user name
```

### Accessing Content Parts and Fields

```liquid
<!-- Access a part directly -->
{{ Model.ContentItem.Content.TitlePart.Title }}
{{ Model.ContentItem.Content.AutoroutePart.Path }}
{{ Model.ContentItem.Content.HtmlBodyPart.Html }}

<!-- Access fields on a custom part -->
{{ Model.ContentItem.Content.BlogPost.Subtitle.Text }}
{{ Model.ContentItem.Content.BlogPost.Image.Paths[0] }}
{{ Model.ContentItem.Content.BlogPost.PublishDate.Value }}
```

### Orchard Core Liquid Tags

```liquid
<!-- Render a zone -->
{% zone "Header" %}
{% zone "Content" %}
{% zone "Footer" %}

<!-- Render a shape -->
{% shape "ShapeName" %}
{% shape "ShapeName", property1: "value1", property2: "value2" %}

<!-- Include resources -->
{% resources type: "HeadMeta" %}
{% resources type: "HeadLink" %}
{% resources type: "Stylesheet" %}
{% resources type: "FooterScript" %}

<!-- Include CSS/JS -->
{% style src: "~/MyTheme/css/site.css" %}
{% script src: "~/MyTheme/js/site.js" at: "Foot" %}

<!-- Localization -->
{% t "Hello World" %}
{% t "Welcome, {0}!" User.Identity.Name %}

<!-- Content rendering -->
{% contentitem id: "content-item-id" %}
{% contentitem alias: "my-alias" %}

<!-- Menu rendering -->
{% shape "Menu", alias: "main-menu" %}
```

### Orchard Core Liquid Filters

```liquid
<!-- String filters -->
{{ "my-slug" | slugify }}              - URL-friendly slug
{{ text | markdownify }}               - Markdown to HTML
{{ text | sanitize_html }}             - Sanitize HTML content

<!-- Date filters -->
{{ Model.ContentItem.PublishedUtc | local }}               - Convert to local time
{{ Model.ContentItem.PublishedUtc | date: "%B %d, %Y" }}   - Format date
{{ "now" | date: "%Y" }}                                   - Current year

<!-- Content filters -->
{{ "alias" | content_item_id }}        - Get content item ID from alias
{{ contentItemId | content_item }}     - Load content item by ID
{{ Model | shape_render }}             - Render a shape

<!-- Media/URL filters -->
{{ path | asset_url }}                 - Generate asset URL
{{ path | href }}                      - Generate full URL

<!-- User/Permission filters -->
{{ User | has_permission: "ViewContent" }}     - Check permission
{{ User | is_in_role: "Administrator" }}       - Check role membership
{{ User | user_id }}                           - Get user ID

<!-- JSON filters -->
{{ object | json }}                    - Serialize to JSON
{{ jsonString | jsonparse }}           - Parse JSON string

<!-- Collection filters -->
{{ array | where: "Property", "Value" }}       - Filter collection
{{ array | order_by: "Property" }}             - Sort collection
{{ array | group_by: "Property" }}             - Group collection
```

### Shape Rendering

```liquid
<!-- Render the Content zone of a content item -->
{{ Model.Content | shape_render }}

<!-- Render specific parts -->
{{ Model.Content.TitlePart | shape_render }}
{{ Model.Content.BodyPart | shape_render }}
```

### Conditional Rendering

```liquid
{% if Model.ContentItem.Content.BlogPost.Featured.Value == true %}
    <span class="badge">Featured</span>
{% endif %}

{% if User | has_permission: "EditContent" %}
    <a href="{{ Model.ContentItem | edit_url }}">Edit</a>
{% endif %}

{% unless Model.ContentItem.Content.BlogPost.Image.Paths == empty %}
    <img src="{{ Model.ContentItem.Content.BlogPost.Image.Paths[0] | asset_url }}" />
{% endunless %}
```

### Iteration

```liquid
{% for item in Model.ContentItems %}
    <article>
        <h2>{{ item.DisplayText }}</h2>
        <time>{{ item.PublishedUtc | date: "%B %d, %Y" }}</time>
    </article>
{% endfor %}
```

### Liquid in Content Fields (LiquidPart)

When using `LiquidPart` attached to a content type, the template has access to:

```liquid
{{ ContentItem }}          - The current content item
{{ ContentItem.DisplayText }}
{{ ContentItem.Content.MyPart.MyField.Text }}
```

### Creating a Custom Liquid Filter

```csharp
using Fluid;
using Fluid.Values;

public sealed class MyLiquidFilter : ILiquidFilter
{
    public ValueTask<FluidValue> ProcessAsync(FluidValue input, FilterArguments arguments, LiquidTemplateContext context)
    {
        var inputString = input.ToStringValue();
        var result = inputString.ToUpperInvariant();
        return new ValueTask<FluidValue>(new StringValue(result));
    }
}
```

Register the filter:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddLiquidFilter<MyLiquidFilter>("my_filter");
    }
}
```

### Creating a Custom Liquid Tag

```csharp
using Fluid;
using Fluid.Ast;

public sealed class MyTagStatement : Statement
{
    public override async ValueTask<Completion> WriteToAsync(
        TextWriter writer,
        TextEncoder encoder,
        TemplateContext context)
    {
        await writer.WriteAsync("Custom tag output");
        return Completion.Normal;
    }
}
```
