---
name: url-routing-patterns
description: Use when designing URL structures, slug generation, SEO-friendly URLs, redirects, or localized URL patterns. Covers route configuration, URL rewriting, canonical URLs, and routing APIs for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# URL Routing Patterns

Guidance for designing URL structures, slug generation, and routing strategies for headless CMS architectures.

## When to Use This Skill

- Designing SEO-friendly URL structures
- Implementing slug generation
- Configuring redirect management
- Planning localized URL patterns
- Building routing APIs

## URL Structure Patterns

### Hierarchical URLs (Page-Based)

```text
/                           # Home
/about                      # About page
/about/team                 # Team (child of About)
/about/team/leadership      # Leadership (grandchild)
/products                   # Products listing
/products/software          # Software category
/products/software/crm      # Specific product
```

### Content Type URLs (Collection-Based)

```text
/blog                       # Blog listing
/blog/2025/01/my-article    # Blog post with date
/blog/my-article            # Blog post without date

/docs                       # Documentation home
/docs/getting-started       # Doc section
/docs/getting-started/install # Doc page

/team/jane-doe              # Team member profile
/portfolio/project-alpha    # Portfolio item
```

### Hybrid URLs

```text
/products/software/crm      # Category > Product
/blog/technology/ai-trends  # Category > Post
/help/faq/billing           # Section > Topic
```

## Slug Generation

### Slug Service

```csharp
public class SlugService
{
    public string GenerateSlug(string text, SlugOptions? options = null)
    {
        options ??= new SlugOptions();

        var slug = text
            .ToLowerInvariant()
            .Normalize(NormalizationForm.FormD);

        // Remove diacritics
        slug = new string(slug
            .Where(c => CharUnicodeInfo.GetUnicodeCategory(c)
                != UnicodeCategory.NonSpacingMark)
            .ToArray());

        // Replace spaces and invalid chars
        slug = Regex.Replace(slug, @"[^a-z0-9\s-]", "");
        slug = Regex.Replace(slug, @"\s+", "-");
        slug = Regex.Replace(slug, @"-+", "-");
        slug = slug.Trim('-');

        // Enforce max length
        if (slug.Length > options.MaxLength)
        {
            slug = slug.Substring(0, options.MaxLength).TrimEnd('-');
        }

        return slug;
    }

    public async Task<string> GenerateUniqueSlugAsync(
        string text,
        string contentType,
        Guid? excludeId = null)
    {
        var baseSlug = GenerateSlug(text);
        var slug = baseSlug;
        var counter = 1;

        while (await SlugExistsAsync(slug, contentType, excludeId))
        {
            slug = $"{baseSlug}-{counter}";
            counter++;
        }

        return slug;
    }
}

public class SlugOptions
{
    public int MaxLength { get; set; } = 100;
    public bool AllowUnicode { get; set; } = false;
    public string Separator { get; set; } = "-";
}
```

### Autoroute Patterns

```csharp
public class AutorouteSettings
{
    public string Pattern { get; set; } = string.Empty;
    public bool AllowCustom { get; set; } = true;
    public bool ShowHomepageOption { get; set; }
}

// Pattern examples:
// "{ContentType}/{Slug}"           -> /article/my-title
// "{Category.Slug}/{Slug}"         -> /technology/my-article
// "blog/{CreatedUtc.Year}/{Slug}"  -> /blog/2025/my-article
// "{Parent.Path}/{Slug}"           -> /about/team/leadership

public class AutorouteService
{
    public string GeneratePath(ContentItem item, string pattern)
    {
        var path = pattern;

        // Replace tokens
        path = path.Replace("{Slug}", item.Slug);
        path = path.Replace("{ContentType}", item.ContentType.ToLower());
        path = path.Replace("{CreatedUtc.Year}", item.CreatedUtc.Year.ToString());
        path = path.Replace("{CreatedUtc.Month}",
            item.CreatedUtc.Month.ToString("00"));

        // Handle relationships
        if (path.Contains("{Category.Slug}") && item.CategoryId.HasValue)
        {
            var category = _categoryRepository.Get(item.CategoryId.Value);
            path = path.Replace("{Category.Slug}", category?.Slug ?? "uncategorized");
        }

        // Handle parent path
        if (path.Contains("{Parent.Path}") && item.ParentId.HasValue)
        {
            var parent = _contentRepository.Get(item.ParentId.Value);
            path = path.Replace("{Parent.Path}", parent?.Path ?? "");
        }

        // Normalize path
        path = "/" + path.Trim('/').ToLowerInvariant();
        return path;
    }
}
```

## Redirect Management

### Redirect Types

```csharp
public class Redirect
{
    public Guid Id { get; set; }
    public string FromPath { get; set; } = string.Empty;
    public string ToPath { get; set; } = string.Empty;
    public RedirectType Type { get; set; }
    public bool IsRegex { get; set; }
    public bool PreserveQueryString { get; set; }
    public DateTime? ExpiresUtc { get; set; }
}

public enum RedirectType
{
    Permanent = 301,    // Moved permanently (SEO transfers)
    Temporary = 302,    // Found (temporary redirect)
    SeeOther = 303,     // See other (POST to GET)
    TemporaryRedirect = 307, // Temporary (preserves method)
    PermanentRedirect = 308  // Permanent (preserves method)
}
```

### Automatic Redirect on Slug Change

```csharp
public class ContentUpdateHandler
{
    public async Task HandleSlugChangeAsync(
        Guid contentId,
        string oldPath,
        string newPath)
    {
        if (oldPath == newPath) return;

        // Create redirect from old to new
        var redirect = new Redirect
        {
            Id = Guid.NewGuid(),
            FromPath = oldPath,
            ToPath = newPath,
            Type = RedirectType.Permanent,
            PreserveQueryString = true
        };

        await _redirectRepository.AddAsync(redirect);

        // Update any existing redirects pointing to old path
        var existingRedirects = await _redirectRepository
            .GetByToPathAsync(oldPath);

        foreach (var existing in existingRedirects)
        {
            existing.ToPath = newPath;
            await _redirectRepository.UpdateAsync(existing);
        }
    }
}
```

## Localized URLs

### URL Localization Strategies

| Strategy | Example | Pros | Cons |
| -------- | ------- | ---- | ---- |
| Path prefix | `/en/about`, `/fr/about` | Clear, SEO-friendly | Longer URLs |
| Subdomain | `en.site.com`, `fr.site.com` | Separate hosting | Complex setup |
| Query param | `/about?lang=fr` | Simple | Poor SEO |
| Translated slugs | `/about`, `/a-propos` | Natural | Hard to manage |

### Path Prefix Implementation

```csharp
public class LocalizedRoutingService
{
    private readonly string[] _supportedLocales = { "en", "fr", "de", "es" };
    private readonly string _defaultLocale = "en";

    public string GetLocalizedPath(string path, string locale)
    {
        // Remove existing locale prefix
        var cleanPath = RemoveLocalePrefix(path);

        // Add new locale prefix (skip for default)
        if (locale != _defaultLocale)
        {
            return $"/{locale}{cleanPath}";
        }

        return cleanPath;
    }

    public (string path, string locale) ParseLocalizedPath(string requestPath)
    {
        foreach (var locale in _supportedLocales)
        {
            if (requestPath.StartsWith($"/{locale}/") ||
                requestPath == $"/{locale}")
            {
                var path = requestPath.Substring(locale.Length + 1);
                return (string.IsNullOrEmpty(path) ? "/" : path, locale);
            }
        }

        return (requestPath, _defaultLocale);
    }
}
```

### Hreflang Tags

```csharp
public class HreflangService
{
    public List<HreflangTag> GenerateHreflangTags(
        ContentItem content,
        string baseUrl)
    {
        var tags = new List<HreflangTag>();

        // Get all localized versions
        var localizations = _localizationService
            .GetLocalizedVersions(content.Id);

        foreach (var loc in localizations)
        {
            tags.Add(new HreflangTag
            {
                Hreflang = loc.Locale,
                Href = $"{baseUrl}{GetLocalizedPath(content.Path, loc.Locale)}"
            });
        }

        // Add x-default
        tags.Add(new HreflangTag
        {
            Hreflang = "x-default",
            Href = $"{baseUrl}{content.Path}"
        });

        return tags;
    }
}

public class HreflangTag
{
    public string Hreflang { get; set; } = string.Empty;
    public string Href { get; set; } = string.Empty;
}
```

## Canonical URLs

```csharp
public class CanonicalUrlService
{
    public string GetCanonicalUrl(HttpRequest request, ContentItem content)
    {
        var baseUrl = $"{request.Scheme}://{request.Host}";

        // Use content's primary path as canonical
        var canonicalPath = content.PrimaryPath ?? content.Path;

        // Remove query parameters (unless paginated)
        // Normalize trailing slash

        return $"{baseUrl}{canonicalPath}";
    }
}
```

## URL Normalization

```csharp
public class UrlNormalizer
{
    public string Normalize(string url, NormalizationOptions options)
    {
        var uri = new UriBuilder(url);

        // Lowercase path
        uri.Path = uri.Path.ToLowerInvariant();

        // Handle trailing slash
        if (options.TrailingSlash == TrailingSlashBehavior.Remove)
        {
            uri.Path = uri.Path.TrimEnd('/');
        }
        else if (options.TrailingSlash == TrailingSlashBehavior.Add &&
                 !uri.Path.EndsWith('/'))
        {
            uri.Path += '/';
        }

        // Sort query parameters
        if (options.SortQueryParams && !string.IsNullOrEmpty(uri.Query))
        {
            var queryParams = HttpUtility.ParseQueryString(uri.Query);
            var sorted = queryParams.AllKeys
                .OrderBy(k => k)
                .Select(k => $"{k}={queryParams[k]}");
            uri.Query = string.Join("&", sorted);
        }

        return uri.ToString();
    }
}

public class NormalizationOptions
{
    public TrailingSlashBehavior TrailingSlash { get; set; }
    public bool SortQueryParams { get; set; }
    public bool ForceLowercase { get; set; } = true;
}

public enum TrailingSlashBehavior
{
    Remove,
    Add,
    Preserve
}
```

## Routing API

### Endpoints

```text
GET /api/routes/resolve?path=/about/team  # Resolve path to content
GET /api/redirects                        # List redirects
GET /api/sitemap.xml                      # XML sitemap
POST /api/slugs/generate                  # Generate slug from text
POST /api/slugs/validate                  # Check slug availability
```

### Route Resolution Response

```json
{
  "data": {
    "path": "/about/team",
    "contentId": "page-456",
    "contentType": "Page",
    "locale": "en",
    "canonical": "https://example.com/about/team",
    "alternates": [
      { "hreflang": "fr", "href": "https://example.com/fr/a-propos/equipe" },
      { "hreflang": "de", "href": "https://example.com/de/uber-uns/team" }
    ],
    "breadcrumbs": [
      { "label": "Home", "path": "/" },
      { "label": "About", "path": "/about" },
      { "label": "Team", "path": "/about/team" }
    ]
  }
}
```

## Related Skills

- `page-structure-design` - Page hierarchy for URLs
- `navigation-architecture` - Menu links and paths
- `headless-api-design` - Routing API endpoints
