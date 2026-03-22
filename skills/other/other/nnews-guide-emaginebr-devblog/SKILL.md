---
name: nnews-guide
description: Guides how to integrate the NNews NuGet package for consuming the NNews CMS API in a .NET 8 project. Use when the user wants to consume articles, categories, tags, images, or AI-powered content generation from the NNews API.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Task
---

# NNews NuGet Package Integration Guide

You are an expert assistant that helps developers integrate the **NNews** NuGet package for consuming the NNews CMS API in .NET 8 projects.

## Input

The user may provide a specific question or context as argument: `$ARGUMENTS`

If no argument is provided, present a complete overview of the NNews integration.

When the user asks about NNews, use this knowledge base to provide accurate, contextual guidance.

---

## NNews — Data Transfer Objects

**Install:** `dotnet add package NNews`

### NNewsSetting

```csharp
public class NNewsSetting
{
    public string ApiUrl { get; set; } = string.Empty;  // NNews API base URL
}
```

### ArticleInfo

```csharp
public class ArticleInfo
{
    public long ArticleId { get; set; }
    public long CategoryId { get; set; }
    public long? AuthorId { get; set; }
    public string? ImageName { get; set; }       // Max 560 chars
    public string Title { get; set; }            // Required, max 255 chars
    public string Content { get; set; }          // Required
    public int Status { get; set; }              // 0=Draft, 1=Published, 2=Archived, 3=Scheduled
    public int ContentType { get; set; } = 2;    // 1=PlainText, 2=Html, 3=MarkDown
    public DateTime DateAt { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    public CategoryInfo? Category { get; set; }
    public List<TagInfo> Tags { get; set; } = new();
    public List<RoleInfo> Roles { get; set; } = new();
}
```

### ArticleInsertedInfo

```csharp
public class ArticleInsertedInfo
{
    public long CategoryId { get; set; }            // Required
    public long? AuthorId { get; set; }
    public string? ImageName { get; set; }          // Max 560 chars
    public string Title { get; set; }               // Required, max 255 chars
    public string Content { get; set; }             // Required
    public int Status { get; set; }                 // 0=Draft, 1=Published, 2=Archived, 3=Scheduled
    public int ContentType { get; set; } = 2;       // Default: Html
    public DateTime DateAt { get; set; }            // Required
    public string TagList { get; set; } = string.Empty;  // Comma-separated tags
    public List<string> Roles { get; set; } = new();     // Role slugs
}
```

### ArticleUpdatedInfo

```csharp
public class ArticleUpdatedInfo
{
    public long ArticleId { get; set; }
    public long CategoryId { get; set; }
    public long? AuthorId { get; set; }
    public string? ImageName { get; set; }
    public string Title { get; set; }
    public string Content { get; set; }
    public int Status { get; set; }
    public int ContentType { get; set; } = 2;
    public DateTime DateAt { get; set; }
    public string TagList { get; set; } = string.Empty;
    public List<string> Roles { get; set; } = new();
}
```

### CategoryInfo

```csharp
public class CategoryInfo
{
    public long CategoryId { get; set; }
    public long? ParentId { get; set; }      // For hierarchical categories
    public string Title { get; set; }        // Required, max 240 chars
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    public int ArticleCount { get; set; }    // Read-only counter
}
```

### TagInfo

```csharp
public class TagInfo
{
    public long TagId { get; set; }
    public string Title { get; set; }        // Required, max 120 chars
    public string? Slug { get; set; }        // Max 120 chars
    public int ArticleCount { get; set; }    // Read-only counter
}
```

### RoleInfo

```csharp
public class RoleInfo
{
    public string Slug { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
}
```

### PagedResult<T>

```csharp
public class PagedResult<T>
{
    public IList<T> Items { get; set; } = new List<T>();
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalCount { get; set; }
    public int TotalPages { get; set; }
    public bool HasPrevious => Page > 1;
    public bool HasNext => Page < TotalPages;
}
```

### AI DTOs

```csharp
// Request for AI content generation
public class AIArticleRequest
{
    public long? ArticleId { get; set; }
    public string Prompt { get; set; }              // Required, 10-2000 chars
    public bool GenerateImage { get; set; } = false;
}

// Response from AI generation
public class AIArticleResponse
{
    public string Title { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public long CategoryId { get; set; }
    public string TagList { get; set; } = string.Empty;
    public string? ImagePrompt { get; set; }
}

// Response from AI article update
public class AIArticleUpdateResponse
{
    public long ArticleId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public long CategoryId { get; set; }
    public string TagList { get; set; } = string.Empty;
    public string? ImagePrompt { get; set; }
}

// Category summary for AI context
public class AICategorySummary
{
    public long CategoryId { get; set; }
    public string Title { get; set; } = string.Empty;
    public long? ParentId { get; set; }
}
```

---

## NNews — Anti-Corruption Layer (ACL)

### IArticleClient

```csharp
public interface IArticleClient
{
    Task<PagedResult<ArticleInfo>> GetAllAsync(long? categoryId = null, int? status = null, int page = 1, int pageSize = 10, CancellationToken cancellationToken = default);
    Task<PagedResult<ArticleInfo>> ListByCategoryAsync(long categoryId, int page = 1, int pageSize = 10, CancellationToken cancellationToken = default);
    Task<PagedResult<ArticleInfo>> ListByRolesAsync(int page = 1, int pageSize = 10, CancellationToken cancellationToken = default);
    Task<PagedResult<ArticleInfo>> ListByTagAsync(string tagSlug, int page = 1, int pageSize = 10, CancellationToken cancellationToken = default);
    Task<PagedResult<ArticleInfo>> SearchAsync(string keyword, int page = 1, int pageSize = 10, CancellationToken cancellationToken = default);
    Task<ArticleInfo> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<ArticleInfo> CreateAsync(ArticleInsertedInfo article, CancellationToken cancellationToken = default);
    Task<ArticleInfo> UpdateAsync(ArticleUpdatedInfo article, CancellationToken cancellationToken = default);
    Task DeleteAsync(int id, CancellationToken cancellationToken = default);
}
```

### IArticleAIClient

```csharp
public interface IArticleAIClient
{
    Task<ArticleInfo> CreateWithAIAsync(string prompt, bool generateImage = false, CancellationToken cancellationToken = default);
    Task<ArticleInfo> UpdateWithAIAsync(int articleId, string prompt, bool generateImage = false, CancellationToken cancellationToken = default);
}
```

### ICategoryClient

```csharp
public interface ICategoryClient
{
    Task<IList<CategoryInfo>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<IList<CategoryInfo>> ListByParentAsync(long? parentId = null, CancellationToken cancellationToken = default);
    Task<CategoryInfo> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<CategoryInfo> CreateAsync(CategoryInfo category, CancellationToken cancellationToken = default);
    Task<CategoryInfo> UpdateAsync(CategoryInfo category, CancellationToken cancellationToken = default);
    Task DeleteAsync(int id, CancellationToken cancellationToken = default);
}
```

### ITagClient

```csharp
public interface ITagClient
{
    Task<IList<TagInfo>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<IList<TagInfo>> ListByRolesAsync(CancellationToken cancellationToken = default);
    Task<TagInfo> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<TagInfo> CreateAsync(TagInfo tag, CancellationToken cancellationToken = default);
    Task<TagInfo> UpdateAsync(TagInfo tag, CancellationToken cancellationToken = default);
    Task DeleteAsync(int id, CancellationToken cancellationToken = default);
    Task MergeTagsAsync(long sourceTagId, long targetTagId, CancellationToken cancellationToken = default);
}
```

### IImageClient

```csharp
public interface IImageClient
{
    Task<string> UploadImageAsync(IFormFile file, CancellationToken cancellationToken = default);
}
```

### ITenantResolver

```csharp
public interface ITenantResolver
{
    string TenantId { get; }
    string ConnectionString { get; }
    string JwtSecret { get; }
}
```

---

## NNews REST API Endpoints

All endpoints are prefixed by the controller name (e.g., `/Article`, `/Category`). Authenticated endpoints require a Bearer JWT token. Tenant is resolved via `X-Tenant-Id` header or JWT `tenant_id` claim.

### Article (`/Article`)

| Method | Route | Query Params | Body | Auth | Response |
|--------|-------|-------------|------|------|----------|
| GET | `/Article` | `categoryId?`, `status?`, `page`, `pageSize` | — | Yes | `PagedResult<ArticleInfo>` |
| GET | `/Article/ListByCategory` | `categoryId`, `page`, `pageSize` | — | No | `PagedResult<ArticleInfo>` |
| GET | `/Article/ListByRoles` | `page`, `pageSize` | — | No | `PagedResult<ArticleInfo>` |
| GET | `/Article/ListByTag` | `tagSlug`, `page`, `pageSize` | — | No | `PagedResult<ArticleInfo>` |
| GET | `/Article/Search` | `keyword`, `page`, `pageSize` | — | No | `PagedResult<ArticleInfo>` |
| GET | `/Article/{id}` | — | — | No | `ArticleInfo` |
| POST | `/Article` | — | `ArticleInsertedInfo` | Yes | `ArticleInfo` (201) |
| POST | `/Article/insertWithAI` | — | `AIArticleRequest` | Yes | `ArticleInfo` (201) |
| PUT | `/Article` | — | `ArticleUpdatedInfo` | Yes | `ArticleInfo` |
| PUT | `/Article/updateWithAI` | — | `AIArticleRequest` | Yes | `ArticleInfo` |
| DELETE | `/Article/{id}` | — | — | Yes | 204 No Content |

**Status filter values:** `0` = Draft, `1` = Published, `2` = Archived, `3` = Scheduled

### Category (`/Category`)

| Method | Route | Query Params | Body | Auth | Response |
|--------|-------|-------------|------|------|----------|
| GET | `/Category` | — | — | Yes | `IList<CategoryInfo>` |
| GET | `/Category/listByParent` | `roles?`, `parentId?` | — | No | `IList<CategoryInfo>` |
| GET | `/Category/{id}` | — | — | No | `CategoryInfo` |
| POST | `/Category` | — | `CategoryInfo` | Yes | `CategoryInfo` (201) |
| PUT | `/Category` | — | `CategoryInfo` | Yes | `CategoryInfo` |
| DELETE | `/Category/{id}` | — | — | Yes | 204 No Content |

### Tag (`/Tag`)

| Method | Route | Query Params | Body | Auth | Response |
|--------|-------|-------------|------|------|----------|
| GET | `/Tag` | — | — | Yes | `IList<TagInfo>` |
| GET | `/Tag/ListByRoles` | — | — | No | `IList<TagInfo>` |
| GET | `/Tag/{id}` | — | — | No | `TagInfo` |
| POST | `/Tag` | — | `TagInfo` | Yes | `TagInfo` (201) |
| PUT | `/Tag` | — | `TagInfo` | Yes | `TagInfo` |
| DELETE | `/Tag/{id}` | — | — | Yes | 204 No Content |
| POST | `/Tag/merge/{sourceTagId}/{targetTagId}` | — | — | Yes | 200 OK |

### Image (`/Image`)

| Method | Route | Query Params | Body | Auth | Response |
|--------|-------|-------------|------|------|----------|
| POST | `/Image/uploadImage` | — | `IFormFile` (multipart, max 100MB) | Yes | `string` (image URL) |

---

## Multi-Tenancy

NNews supports multi-tenancy via the `X-Tenant-Id` HTTP header.

### TenantHeaderHandler

A `DelegatingHandler` that automatically adds the `X-Tenant-Id` header to all outgoing HTTP requests. It reads the tenant ID from the configuration key `Tenant:DefaultTenantId`.

### TenantResolver

Implements `ITenantResolver`. Reads tenant configuration from:
- `Tenant:DefaultTenantId` — the default tenant ID
- `Tenants:{TenantId}:ConnectionString` — database connection string
- `Tenants:{TenantId}:JwtSecret` — JWT secret for the tenant

---

## Step-by-Step Integration

### 1. Install Package

```bash
dotnet add package NNews
```

### 2. Configure appsettings.json

```json
{
  "NNews": {
    "ApiUrl": "http://localhost:5007"
  },
  "Tenant": {
    "DefaultTenantId": "my-tenant"
  }
}
```

Docker: use `"ApiUrl": "http://nnews-api:80"`.

### 3. Register Services (DI)

```csharp
using NNews.ACL;
using NNews.ACL.Interfaces;
using NNews.ACL.Handlers;
using NNews.ACL.Services;
using NNews.DTO.Settings;

// Settings
services.Configure<NNewsSetting>(configuration.GetSection("NNews"));

// Tenant resolver
services.AddScoped<ITenantResolver, TenantResolver>();

// Register TenantHeaderHandler for automatic X-Tenant-Id header
services.AddTransient<TenantHeaderHandler>();

// Register HttpClients with TenantHeaderHandler
services.AddHttpClient<IArticleClient, ArticleClient>()
    .AddHttpMessageHandler<TenantHeaderHandler>();

services.AddHttpClient<IArticleAIClient, ArticleAIClient>()
    .AddHttpMessageHandler<TenantHeaderHandler>();

services.AddHttpClient<ICategoryClient, CategoryClient>()
    .AddHttpMessageHandler<TenantHeaderHandler>();

services.AddHttpClient<ITagClient, TagClient>()
    .AddHttpMessageHandler<TenantHeaderHandler>();

services.AddHttpClient<IImageClient, ImageClient>()
    .AddHttpMessageHandler<TenantHeaderHandler>();
```

### 4. Register Only What You Need

If you only need to read articles (e.g., a public blog frontend), register only the necessary clients:

```csharp
services.Configure<NNewsSetting>(configuration.GetSection("NNews"));
services.AddTransient<TenantHeaderHandler>();

services.AddHttpClient<IArticleClient, ArticleClient>()
    .AddHttpMessageHandler<TenantHeaderHandler>();

services.AddHttpClient<ICategoryClient, CategoryClient>()
    .AddHttpMessageHandler<TenantHeaderHandler>();

services.AddHttpClient<ITagClient, TagClient>()
    .AddHttpMessageHandler<TenantHeaderHandler>();
```

---

## Usage Examples

### List Articles (Paginated)

```csharp
public class BlogService
{
    private readonly IArticleClient _articleClient;

    public BlogService(IArticleClient articleClient)
    {
        _articleClient = articleClient;
    }

    public async Task<PagedResult<ArticleInfo>> GetLatestArticles(int page = 1, int pageSize = 12)
    {
        return await _articleClient.GetAllAsync(page: page, pageSize: pageSize);
    }

    public async Task<PagedResult<ArticleInfo>> GetPublishedArticles(int page = 1, int pageSize = 12)
    {
        // Filter by status: 0=Draft, 1=Published, 2=Archived, 3=Scheduled
        return await _articleClient.GetAllAsync(status: 1, page: page, pageSize: pageSize);
    }
}
```

### List Articles by Category

```csharp
public async Task<PagedResult<ArticleInfo>> GetByCategory(long categoryId, int page = 1)
{
    return await _articleClient.ListByCategoryAsync(categoryId, page: page, pageSize: 10);
}
```

### List Articles by Tag

```csharp
public async Task<PagedResult<ArticleInfo>> GetByTag(string tagSlug, int page = 1)
{
    return await _articleClient.ListByTagAsync(tagSlug, page: page, pageSize: 10);
}
```

### Search Articles

```csharp
public async Task<PagedResult<ArticleInfo>> Search(string keyword, int page = 1)
{
    return await _articleClient.SearchAsync(keyword, page: page, pageSize: 10);
}
```

### Get Single Article

```csharp
public async Task<ArticleInfo> GetArticle(int id)
{
    return await _articleClient.GetByIdAsync(id);
}
```

### Create Article

```csharp
public async Task<ArticleInfo> CreateArticle()
{
    var article = new ArticleInsertedInfo
    {
        Title = "My First Article",
        Content = "<p>Hello World!</p>",
        CategoryId = 1,
        Status = 1,           // Published
        ContentType = 2,       // Html
        DateAt = DateTime.UtcNow,
        TagList = "dotnet,csharp,webapi",
        Roles = new List<string> { "admin", "editor" }
    };

    return await _articleClient.CreateAsync(article);
}
```

### Update Article

```csharp
public async Task<ArticleInfo> UpdateArticle(long articleId)
{
    var article = new ArticleUpdatedInfo
    {
        ArticleId = articleId,
        Title = "Updated Title",
        Content = "<p>Updated content</p>",
        CategoryId = 1,
        Status = 1,
        ContentType = 2,
        DateAt = DateTime.UtcNow,
        TagList = "dotnet,updated"
    };

    return await _articleClient.UpdateAsync(article);
}
```

### Delete Article

```csharp
public async Task DeleteArticle(int articleId)
{
    await _articleClient.DeleteAsync(articleId);
}
```

### Create Article with AI

```csharp
public async Task<ArticleInfo> CreateWithAI(string prompt, bool withImage = false)
{
    return await _articleAIClient.CreateWithAIAsync(prompt, generateImage: withImage);
}

// Example usage:
// var article = await CreateWithAI("Write an article about clean architecture in .NET 8", withImage: true);
```

### Update Article with AI

```csharp
public async Task<ArticleInfo> UpdateWithAI(int articleId, string prompt)
{
    return await _articleAIClient.UpdateWithAIAsync(articleId, prompt, generateImage: false);
}
```

### Category Management

```csharp
public async Task CategoryExamples()
{
    // List all categories
    var categories = await _categoryClient.GetAllAsync();

    // List root categories (no parent)
    var rootCategories = await _categoryClient.ListByParentAsync(parentId: null);

    // List subcategories
    var subCategories = await _categoryClient.ListByParentAsync(parentId: 1);

    // Create category
    var newCategory = await _categoryClient.CreateAsync(new CategoryInfo
    {
        Title = "Technology",
        ParentId = null  // Root category
    });

    // Create subcategory
    var subCategory = await _categoryClient.CreateAsync(new CategoryInfo
    {
        Title = "Web Development",
        ParentId = newCategory.CategoryId
    });

    // Delete category
    await _categoryClient.DeleteAsync((int)newCategory.CategoryId);
}
```

### Tag Management

```csharp
public async Task TagExamples()
{
    // List all tags
    var tags = await _tagClient.GetAllAsync();

    // List tags filtered by user roles
    var roleTags = await _tagClient.ListByRolesAsync();

    // Create tag
    var newTag = await _tagClient.CreateAsync(new TagInfo { Title = "C#" });

    // Merge tags (move all articles from source to target, then delete source)
    await _tagClient.MergeTagsAsync(sourceTagId: 5, targetTagId: 2);

    // Delete tag
    await _tagClient.DeleteAsync((int)newTag.TagId);
}
```

### Image Upload

```csharp
[HttpPost("upload")]
[Authorize]
public async Task<ActionResult<string>> UploadImage(IFormFile file)
{
    if (file == null || file.Length == 0)
        return BadRequest("No file uploaded");

    var imageUrl = await _imageClient.UploadImageAsync(file);
    return Ok(imageUrl);
}
```

### Controller Example — Blog API

```csharp
using Microsoft.AspNetCore.Mvc;
using NNews.ACL.Interfaces;
using NNews.DTO;

[Route("api/[controller]")]
[ApiController]
public class BlogController : ControllerBase
{
    private readonly IArticleClient _articleClient;
    private readonly ICategoryClient _categoryClient;
    private readonly ITagClient _tagClient;

    public BlogController(
        IArticleClient articleClient,
        ICategoryClient categoryClient,
        ITagClient tagClient)
    {
        _articleClient = articleClient;
        _categoryClient = categoryClient;
        _tagClient = tagClient;
    }

    [HttpGet("articles")]
    public async Task<ActionResult<PagedResult<ArticleInfo>>> GetArticles(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 12,
        [FromQuery] long? categoryId = null,
        [FromQuery] int? status = null)
    {
        var result = await _articleClient.GetAllAsync(categoryId, status, page, pageSize);
        return Ok(result);
    }

    [HttpGet("articles/{id}")]
    public async Task<ActionResult<ArticleInfo>> GetArticle(int id)
    {
        var article = await _articleClient.GetByIdAsync(id);
        return Ok(article);
    }

    [HttpGet("articles/search")]
    public async Task<ActionResult<PagedResult<ArticleInfo>>> Search(
        [FromQuery] string keyword,
        [FromQuery] int page = 1)
    {
        var result = await _articleClient.SearchAsync(keyword, page);
        return Ok(result);
    }

    [HttpDelete("articles/{id}")]
    public async Task<IActionResult> DeleteArticle(int id)
    {
        await _articleClient.DeleteAsync(id);
        return NoContent();
    }

    [HttpGet("categories")]
    public async Task<ActionResult<IList<CategoryInfo>>> GetCategories()
    {
        var categories = await _categoryClient.GetAllAsync();
        return Ok(categories);
    }

    [HttpGet("tags")]
    public async Task<ActionResult<IList<TagInfo>>> GetTags()
    {
        var tags = await _tagClient.GetAllAsync();
        return Ok(tags);
    }
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| HTTP 500 on all requests | NNews API unreachable | Verify `NNews:ApiUrl` in appsettings |
| HTTP 401 Unauthorized | Missing or invalid auth token | Ensure Bearer token is forwarded or endpoint is public |
| Empty `PagedResult` | Wrong tenant or no data | Check `Tenant:DefaultTenantId` configuration |
| DI error for `IArticleClient` | Missing registration | Add `services.AddHttpClient<IArticleClient, ArticleClient>()` |
| Missing `X-Tenant-Id` header | `TenantHeaderHandler` not registered | Add `.AddHttpMessageHandler<TenantHeaderHandler>()` |
| `NNewsSetting.ApiUrl` empty | Missing configuration section | Add `"NNews": { "ApiUrl": "..." }` to appsettings |
| `CreateAsync` returns error | Missing required fields | Ensure `Title`, `Content`, `CategoryId`, and `DateAt` are set |
| Tags not applied | Wrong format | Use comma-separated string in `TagList` (e.g., `"tag1,tag2,tag3"`) |

---

## Response Guidelines

1. **Be specific**: Reference exact class names, interfaces, and method signatures
2. **Show code**: Always include working code examples based on the patterns above
3. **Context-aware**: If the user is working in a project that consumes NNews, reference their existing DI setup and configuration
4. **Minimal changes**: Only suggest what's needed for the user's specific question
5. **Multi-tenancy**: Always remind about configuring `Tenant:DefaultTenantId` and registering `TenantHeaderHandler`
6. **Prerequisites**: Mention required NuGet package and configuration if starting fresh
