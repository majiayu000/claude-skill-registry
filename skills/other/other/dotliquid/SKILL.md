---
name: dotliquid
description: >
  Guidance for DotLiquid template engine for .NET.
  USE FOR: safe user-generated templates, email templates, CMS content rendering, sandboxed template execution, report generation from data models.
  DO NOT USE FOR: Razor-based server-side views (use ASP.NET Razor), logic-heavy templates requiring full C# (use Scriban or Razor), compiled template performance-critical paths.
license: MIT
metadata:
  displayName: DotLiquid
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "DotLiquid Official Website"
    url: "https://www.dotliquid.org"
  - title: "DotLiquid GitHub Repository"
    url: "https://github.com/dotliquid/dotliquid"
  - title: "DotLiquid NuGet Package"
    url: "https://www.nuget.org/packages/DotLiquid"
---

# DotLiquid

## Overview

DotLiquid is a .NET port of the Liquid template engine originally created by Shopify. It provides a secure, sandboxed template rendering system where templates cannot execute arbitrary code, making it ideal for user-generated content, email templates, and CMS rendering. Templates use `{{ variable }}` for output and `{% tag %}` for control flow.

DotLiquid supports two rendering modes: by default, it uses a safe model where only explicitly registered types and properties are accessible from templates. This prevents untrusted templates from accessing sensitive data or calling arbitrary methods.

Install via NuGet:
```
dotnet add package DotLiquid
```

## Basic Template Rendering

Parse a template string and render it with a hash of values. Templates are compiled once and can be rendered multiple times with different data.

```csharp
using DotLiquid;

// Simple variable substitution
var template = Template.Parse("Hello, {{ name }}! You have {{ count }} new messages.");
var output = template.Render(Hash.FromAnonymousObject(new { name = "Alice", count = 5 }));
// Output: "Hello, Alice! You have 5 new messages."

// Reuse the compiled template with different data
var output2 = template.Render(Hash.FromAnonymousObject(new { name = "Bob", count = 12 }));
```

## Control Flow and Iteration

DotLiquid supports `if`/`elsif`/`else`, `unless`, `for` loops, and `case`/`when` for branching logic inside templates.

```csharp
using DotLiquid;

var invoiceTemplate = Template.Parse(@"
Invoice #{{ invoice.number }}
Date: {{ invoice.date | date: '%B %d, %Y' }}

{% for item in invoice.items %}
  {{ item.name }} - {{ item.quantity }} x ${{ item.price }} = ${{ item.total }}
{% endfor %}

{% if invoice.discount > 0 %}
  Discount: -${{ invoice.discount }}
{% endif %}

Total: ${{ invoice.grand_total }}
{% if invoice.paid %}
  Status: PAID
{% else %}
  Status: UNPAID - Due by {{ invoice.due_date | date: '%m/%d/%Y' }}
{% endif %}
");

var result = invoiceTemplate.Render(Hash.FromAnonymousObject(new
{
    invoice = new
    {
        number = "INV-2025-001",
        date = DateTime.Now,
        items = new[]
        {
            new { name = "Widget A", quantity = 3, price = 10.00, total = 30.00 },
            new { name = "Widget B", quantity = 1, price = 25.00, total = 25.00 }
        },
        discount = 5.00,
        grand_total = 50.00,
        paid = false,
        due_date = DateTime.Now.AddDays(30)
    }
}));
```

## Custom Filters

Filters transform output values. Register custom filters by creating a static class with static methods that DotLiquid calls during rendering.

```csharp
using DotLiquid;

public static class CustomFilters
{
    public static string Truncate(string input, int length)
    {
        if (string.IsNullOrEmpty(input) || input.Length <= length)
            return input;
        return input[..length] + "...";
    }

    public static string Currency(decimal input, string symbol = "$")
    {
        return $"{symbol}{input:N2}";
    }

    public static string Pluralize(int count, string singular, string plural)
    {
        return count == 1 ? singular : plural;
    }
}

// Register filters globally
Template.RegisterFilter(typeof(CustomFilters));

var template = Template.Parse(
    "{{ description | truncate: 50 }} - {{ price | currency }} " +
    "({{ qty }} {{ qty | pluralize: 'item', 'items' }})");

var output = template.Render(Hash.FromAnonymousObject(new
{
    description = "A very long product description that should be truncated for display",
    price = 29.99m,
    qty = 3
}));
```

## Registering Safe Types (Drop Classes)

For security, DotLiquid does not expose CLR objects directly. Use `Drop` classes or register safe types to control what template authors can access.

```csharp
using DotLiquid;
using System.Collections.Generic;

public class ProductDrop : Drop
{
    private readonly Product _product;

    public ProductDrop(Product product)
    {
        _product = product;
    }

    public string Name => _product.Name;
    public decimal Price => _product.Price;
    public string Category => _product.Category;

    // Methods accessible in templates
    public string FormattedPrice() => $"${_product.Price:N2}";
}

// Alternatively, register types as safe for direct access
Template.RegisterSafeType(typeof(Product), new[] { "Name", "Price", "Category" });

// Using Drop in a template
var template = Template.Parse("{{ product.name }} costs {{ product.formatted_price }}");
var hash = Hash.FromAnonymousObject(new { product = new ProductDrop(myProduct) });
var output = template.Render(hash);
```

## Custom Tags

Create custom tags by inheriting from `Tag` for block-level template constructs.

```csharp
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using DotLiquid;

public class HighlightTag : Tag
{
    private string _cssClass = "highlight";

    public override void Initialize(string tagName, string markup, List<string> tokens)
    {
        base.Initialize(tagName, markup, tokens);
        var match = Regex.Match(markup.Trim(), @"class:\s*""(\w+)""");
        if (match.Success)
            _cssClass = match.Groups[1].Value;
    }

    public override void Render(Context context, TextWriter result)
    {
        result.Write($"<span class=\"{_cssClass}\">");
        RenderAll(NodeList, context, result);
        result.Write("</span>");
    }
}

// Register the custom tag
Template.RegisterTag<HighlightTag>("highlight");

// Use in template: {% highlight class: "important" %}This is highlighted{% endhighlight %}
```

## DotLiquid vs Other Template Engines

| Feature | DotLiquid | Scriban | Handlebars.NET | Razor |
|---------|-----------|---------|----------------|-------|
| Sandboxed execution | Yes (default) | Optional | No | No |
| User-generated templates | Excellent | Good | Good | Dangerous |
| Full C# expressions | No | Yes | No | Yes |
| Logic-free philosophy | Yes | No | Yes | No |
| Performance | Good | Excellent | Good | Excellent |
| Template syntax | Liquid/Shopify | Liquid-like | Mustache | HTML+C# |

## Integrating with Dependency Injection

Wrap template rendering in a service for clean DI integration.

```csharp
using System.Threading.Tasks;
using DotLiquid;

public interface ITemplateRenderer
{
    string Render(string templateSource, object model);
}

public class LiquidTemplateRenderer : ITemplateRenderer
{
    public LiquidTemplateRenderer()
    {
        Template.RegisterFilter(typeof(CustomFilters));
    }

    public string Render(string templateSource, object model)
    {
        var template = Template.Parse(templateSource);
        var hash = Hash.FromAnonymousObject(model);
        return template.Render(hash);
    }
}

// Registration
// builder.Services.AddSingleton<ITemplateRenderer, LiquidTemplateRenderer>();
```

## Best Practices

1. **Cache compiled `Template` instances** by calling `Template.Parse` once and reusing the result across renders, since parsing is the most expensive step.
2. **Use `Drop` classes for domain models** instead of `RegisterSafeType` when you need to control exactly which properties and methods are exposed to templates.
3. **Register custom filters in a startup path** (e.g., application initialization) rather than per-request, since `Template.RegisterFilter` is a global static operation.
4. **Validate template syntax before storing user templates** by wrapping `Template.Parse` in a try/catch for `SyntaxException` and returning errors to the user.
5. **Use `Hash.FromAnonymousObject`** for simple data but switch to `Hash.FromDictionary` when building data dynamically from multiple sources.
6. **Prefer DotLiquid naming conventions** (snake_case in templates mapped to PascalCase in C#) by configuring `Template.NamingConvention = new RubyNamingConvention()`.
7. **Limit template execution time** in user-facing scenarios by setting `Template.DefaultMaxIterations` to prevent infinite loops in user-authored templates.
8. **Avoid embedding business logic in templates** -- keep templates focused on presentation and move calculations into the model or filter layer.
9. **Use the `include` tag with registered file systems** for template composition instead of duplicating template fragments.
10. **Test templates with edge cases** including null values, empty collections, and missing keys to ensure templates degrade gracefully without crashing.
