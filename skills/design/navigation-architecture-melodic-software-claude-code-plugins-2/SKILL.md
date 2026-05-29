---
name: navigation-architecture
description: Use when designing menu systems, breadcrumbs, mega-menus, or navigation APIs. Covers menu hierarchies, dynamic vs static navigation, mobile navigation patterns, and navigation endpoint design for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Navigation Architecture

Guidance for designing menu systems, breadcrumbs, and navigation APIs for headless CMS architectures.

## When to Use This Skill

- Designing primary/secondary navigation
- Implementing breadcrumb trails
- Building mega-menu structures
- Creating mobile navigation patterns
- Designing navigation APIs

## Menu Types

### Primary Navigation

Main site navigation, typically in header.

```csharp
public class Menu
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public MenuLocation Location { get; set; }
    public List<MenuItem> Items { get; set; } = new();
}

public class MenuItem
{
    public Guid Id { get; set; }
    public string Label { get; set; } = string.Empty;

    // Link target (one of these)
    public Guid? PageId { get; set; }
    public string? ExternalUrl { get; set; }
    public string? Anchor { get; set; }

    // Computed URL
    public string Url { get; set; } = string.Empty;

    // Hierarchy
    public Guid? ParentId { get; set; }
    public List<MenuItem> Children { get; set; } = new();
    public int Order { get; set; }

    // Display options
    public bool OpenInNewTab { get; set; }
    public string? Icon { get; set; }
    public string? CssClass { get; set; }
}

public enum MenuLocation
{
    Primary,
    Secondary,
    Footer,
    Sidebar,
    Utility,
    Mobile
}
```

### Mega Menu

Complex navigation with multiple columns and featured content.

```csharp
public class MegaMenuItem : MenuItem
{
    // Mega menu specific
    public bool IsMegaMenu { get; set; }
    public int Columns { get; set; } = 4;

    // Featured content
    public Guid? FeaturedContentId { get; set; }
    public string? FeaturedImageUrl { get; set; }
    public string? Description { get; set; }

    // Column groups
    public List<MenuColumn> MenuColumns { get; set; } = new();
}

public class MenuColumn
{
    public string? Heading { get; set; }
    public List<MenuItem> Items { get; set; } = new();
}
```

### Footer Navigation

```csharp
public class FooterMenu
{
    public List<FooterSection> Sections { get; set; } = new();
    public List<MenuItem> LegalLinks { get; set; } = new();
    public List<SocialLink> SocialLinks { get; set; } = new();
}

public class FooterSection
{
    public string Heading { get; set; } = string.Empty;
    public List<MenuItem> Links { get; set; } = new();
}

public class SocialLink
{
    public string Platform { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public string? Icon { get; set; }
}
```

## Breadcrumbs

### Breadcrumb Generation

```csharp
public class BreadcrumbService
{
    public async Task<List<Breadcrumb>> GetBreadcrumbsAsync(Page page)
    {
        var breadcrumbs = new List<Breadcrumb>
        {
            new Breadcrumb { Label = "Home", Url = "/" }
        };

        // Walk up the page hierarchy
        var ancestors = await GetAncestorsAsync(page);
        foreach (var ancestor in ancestors)
        {
            breadcrumbs.Add(new Breadcrumb
            {
                Label = ancestor.Title,
                Url = ancestor.Path
            });
        }

        // Current page (no link)
        breadcrumbs.Add(new Breadcrumb
        {
            Label = page.Title,
            Url = null,
            IsCurrent = true
        });

        return breadcrumbs;
    }
}

public class Breadcrumb
{
    public string Label { get; set; } = string.Empty;
    public string? Url { get; set; }
    public bool IsCurrent { get; set; }
}
```

### Structured Data for SEO

```csharp
public class BreadcrumbSchemaGenerator
{
    public string GenerateJsonLd(List<Breadcrumb> breadcrumbs, string baseUrl)
    {
        var items = breadcrumbs.Select((b, i) => new
        {
            @type = "ListItem",
            position = i + 1,
            name = b.Label,
            item = b.Url != null ? $"{baseUrl}{b.Url}" : null
        }).ToList();

        var schema = new
        {
            @context = "https://schema.org",
            @type = "BreadcrumbList",
            itemListElement = items
        };

        return JsonSerializer.Serialize(schema);
    }
}
```

## Dynamic vs Static Menus

### Dynamic Menu (Page-Based)

```csharp
public class DynamicMenuService
{
    public async Task<Menu> GenerateFromPagesAsync(
        int maxDepth = 2,
        bool publishedOnly = true)
    {
        var pages = await _pageRepository.GetPublishedPagesAsync();

        var rootPages = pages
            .Where(p => p.ParentId == null && p.ShowInNavigation)
            .OrderBy(p => p.Order);

        var menu = new Menu
        {
            Name = "Main Navigation",
            Slug = "main",
            Location = MenuLocation.Primary
        };

        foreach (var page in rootPages)
        {
            var item = await BuildMenuItemAsync(page, pages, 1, maxDepth);
            menu.Items.Add(item);
        }

        return menu;
    }

    private async Task<MenuItem> BuildMenuItemAsync(
        Page page,
        IEnumerable<Page> allPages,
        int currentDepth,
        int maxDepth)
    {
        var item = new MenuItem
        {
            Id = page.Id,
            Label = page.NavigationTitle ?? page.Title,
            PageId = page.Id,
            Url = page.Path,
            Order = page.Order
        };

        if (currentDepth < maxDepth)
        {
            var children = allPages
                .Where(p => p.ParentId == page.Id && p.ShowInNavigation)
                .OrderBy(p => p.Order);

            foreach (var child in children)
            {
                var childItem = await BuildMenuItemAsync(
                    child, allPages, currentDepth + 1, maxDepth);
                item.Children.Add(childItem);
            }
        }

        return item;
    }
}
```

### Static Menu (CMS-Managed)

```csharp
public class StaticMenuService
{
    public async Task<Menu> GetMenuAsync(string slug)
    {
        var menu = await _menuRepository.GetBySlugAsync(slug);
        if (menu == null) return null!;

        // Resolve page URLs for page-linked items
        foreach (var item in menu.Items.SelectMany(FlattenItems))
        {
            if (item.PageId.HasValue)
            {
                var page = await _pageRepository.GetAsync(item.PageId.Value);
                item.Url = page?.Path ?? "#";
            }
        }

        return menu;
    }

    private IEnumerable<MenuItem> FlattenItems(MenuItem item)
    {
        yield return item;
        foreach (var child in item.Children.SelectMany(FlattenItems))
        {
            yield return child;
        }
    }
}
```

## Navigation API

### REST Endpoints

```text
GET /api/menus                    # List all menus
GET /api/menus/{slug}             # Get menu by slug
GET /api/menus/location/{location} # Get menu by location
GET /api/breadcrumbs?path=/about  # Get breadcrumbs for path
```

### Menu Response

```json
{
  "data": {
    "id": "menu-123",
    "name": "Main Navigation",
    "slug": "main",
    "location": "Primary",
    "items": [
      {
        "id": "item-1",
        "label": "Products",
        "url": "/products",
        "children": [
          {
            "id": "item-2",
            "label": "Software",
            "url": "/products/software",
            "children": []
          },
          {
            "id": "item-3",
            "label": "Hardware",
            "url": "/products/hardware",
            "children": []
          }
        ]
      },
      {
        "id": "item-4",
        "label": "About",
        "url": "/about",
        "children": []
      },
      {
        "id": "item-5",
        "label": "Contact",
        "url": "/contact",
        "children": []
      }
    ]
  }
}
```

### Breadcrumb Response

```json
{
  "data": [
    { "label": "Home", "url": "/" },
    { "label": "Products", "url": "/products" },
    { "label": "Software", "url": "/products/software" },
    { "label": "Enterprise Suite", "url": null, "isCurrent": true }
  ],
  "jsonLd": "<script type=\"application/ld+json\">...</script>"
}
```

## Mobile Navigation Patterns

### Hamburger Menu

```csharp
public class MobileMenuConfig
{
    public bool UseHamburger { get; set; } = true;
    public HamburgerStyle Style { get; set; } = HamburgerStyle.SlideIn;
    public int MaxVisibleItems { get; set; } = 5;
    public bool ShowSearch { get; set; } = true;
}

public enum HamburgerStyle
{
    SlideIn,    // Slides from side
    Overlay,    // Full screen overlay
    Dropdown    // Drops down from header
}
```

### Responsive Navigation Strategy

| Breakpoint | Navigation Style |
| ---------- | ---------------- |
| Desktop (>1024px) | Full horizontal menu with dropdowns |
| Tablet (768-1024px) | Condensed menu, mega-menu collapses |
| Mobile (<768px) | Hamburger menu, accordion submenus |

## Best Practices

### Menu Design

```text
DO:
- Limit primary nav to 5-7 items
- Use clear, action-oriented labels
- Keep hierarchy shallow (2-3 levels max)
- Highlight current page/section
- Make menus keyboard-accessible

DON'T:
- Create deep nested menus
- Use vague labels like "More" or "Misc"
- Hide important pages in submenus
- Forget mobile users
```

### Performance

```csharp
// Cache menus - they change infrequently
public class CachedMenuService
{
    private readonly IMemoryCache _cache;
    private readonly TimeSpan _cacheDuration = TimeSpan.FromMinutes(30);

    public async Task<Menu> GetMenuAsync(string slug)
    {
        var cacheKey = $"menu:{slug}";

        if (!_cache.TryGetValue(cacheKey, out Menu? menu))
        {
            menu = await _menuRepository.GetBySlugAsync(slug);
            _cache.Set(cacheKey, menu, _cacheDuration);
        }

        return menu!;
    }
}
```

## Related Skills

- `page-structure-design` - Page hierarchy for navigation
- `url-routing-patterns` - URL structure for menu links
- `headless-api-design` - Navigation API endpoints
