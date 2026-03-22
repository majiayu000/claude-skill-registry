---
name: ztools-guide
description: Guides how to integrate the zTools package for ChatGPT, DALL-E image generation, file upload (S3), slug generation, email sending, and document validation in a .NET 8 project. Use when the user wants to use AI features, upload files, generate slugs, send emails, or understand zTools integration.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Task
---

# zTools Integration Guide

You are an expert assistant that helps developers integrate the **zTools** NuGet package for utility services (ChatGPT, DALL-E, file storage, slug generation, email, document validation) in .NET 8 Web API projects.

## Input

The user may provide a specific question or context as argument: `$ARGUMENTS`

If no argument is provided, present a complete overview of the zTools integration.

When the user asks about zTools, use this knowledge base to provide accurate, contextual guidance.

---

## zTools — Data Transfer Objects

**Install:** `dotnet add package zTools --version 0.3.1`

### Settings

```csharp
public class zToolsetting { public string ApiUrl { get; set; } }
public class ChatGPTSetting { public string ApiUrl; public string ApiKey; public string Model; }
public class MailerSendSetting { /* MailerSend API config */ }
public class S3Setting { /* S3 bucket, credentials, endpoint config */ }
```

### ChatGPT DTOs

```csharp
public class ChatMessage
{
    public string Role { get; set; }     // "system", "user", or "assistant"
    public string Content { get; set; }
}

public class ChatGPTRequest { public string Model; public List<ChatMessage> Messages; }
public class ChatGPTResponse { public List<ChatGPTChoice> Choices; public ChatGPTUsage Usage; }
public class ChatGPTMessageRequest { public string Message; }
public class ChatGPTErrorResponse { /* Error handling */ }
```

### DALL-E DTOs

```csharp
public class DallERequest
{
    public string Prompt { get; set; }    // Image description
    public string Model { get; set; }     // "dall-e-3"
    public string Size { get; set; }      // "1024x1024", "1024x1792", "1792x1024"
    public string Quality { get; set; }   // "standard" or "hd"
    public string Style { get; set; }     // "vivid" or "natural"
}

public class DallEResponse { public List<DallEImageData> Data; }
public class DallEImageData { public string Url; public string RevisedPrompt; }
```

### Email DTOs

```csharp
public class MailerInfo { /* Email composition and sending */ }
public class MailerRecipientInfo { /* Recipient info */ }
public class MailerErrorInfo { /* Error handling */ }
```

---

## zTools — Anti-Corruption Layer

**Install:** `dotnet add package zTools --version 0.3.1`

### IChatGPTClient

```csharp
public interface IChatGPTClient
{
    Task<string> SendMessageAsync(string question);
    Task<string> SendConversationAsync(List<ChatMessage> messages);
    Task<DallEResponse> GenerateImageAdvancedAsync(DallERequest request);
}
```

### IStringClient

```csharp
public interface IStringClient
{
    Task<string> GenerateSlugAsync(string text);  // "Hello World!" -> "hello-world"
}
```

### IFileClient

```csharp
public interface IFileClient
{
    Task<string> UploadFileAsync(string bucketName, IFormFile file);   // Returns file name
    Task<string> GetFileUrlAsync(string bucketName, string fileName); // Returns public URL
}
```

### IMailClient / IDocumentClient

```csharp
public interface IMailClient { /* Email validation and sending via MailerSend */ }
public interface IDocumentClient { /* CPF/CNPJ validation */ }
```

Implementations: `ChatGPTClient`, `StringClient`, `FileClient`, `MailClient`, `DocumentClient`.

---

## Step-by-Step Integration

### 1. Configure appsettings.json

```json
{
  "zTools": {
    "ApiURL": "http://localhost:5001"
  }
}
```

Docker: use `"ApiURL": "http://ztools-api:80"`.

### 2. Register Services (DI)

```csharp
using zTools.ACL;
using zTools.ACL.Interfaces;
using zTools.DTO.Settings;

services.Configure<zToolsetting>(configuration.GetSection("zTools"));
services.AddHttpClient();

// Register only the clients you need
services.AddScoped<IChatGPTClient, ChatGPTClient>();   // ChatGPT + DALL-E
services.AddScoped<IStringClient, StringClient>();      // Slug generation
services.AddScoped<IFileClient, FileClient>();          // File upload/retrieval
services.AddScoped<IMailClient, MailClient>();           // Email sending
services.AddScoped<IDocumentClient, DocumentClient>();   // Document validation
```

---

## Usage Examples

### ChatGPT — Simple Question

```csharp
public async Task<string> AskQuestion(string question)
{
    return await _chatGPTClient.SendMessageAsync(question);
}
```

### ChatGPT — Conversation with System Prompt

```csharp
using zTools.DTO.ChatGPT;

public async Task<string> GenerateContent(string userPrompt)
{
    var messages = new List<ChatMessage>
    {
        new ChatMessage { Role = "system", Content = "You are a content writer. Return only valid JSON." },
        new ChatMessage { Role = "user", Content = userPrompt }
    };

    var response = await _chatGPTClient.SendConversationAsync(messages);

    // Clean markdown wrapper if present
    var clean = response.Trim();
    if (clean.StartsWith("```json"))
    {
        clean = clean.Substring(7);
        if (clean.EndsWith("```"))
            clean = clean.Substring(0, clean.Length - 3);
        clean = clean.Trim();
    }

    return clean;
}
```

### ChatGPT — Multi-turn Conversation

```csharp
var messages = new List<ChatMessage>
{
    new ChatMessage { Role = "system", Content = "You are a helpful assistant." },
    new ChatMessage { Role = "user", Content = "What is .NET?" },
    new ChatMessage { Role = "assistant", Content = ".NET is a free, open-source developer platform..." },
    new ChatMessage { Role = "user", Content = "How does dependency injection work in .NET?" }
};
var response = await _chatGPTClient.SendConversationAsync(messages);
```

### DALL-E 3 — Image Generation

```csharp
public async Task<string?> GenerateImage(string description)
{
    var request = new DallERequest
    {
        Prompt = description,
        Model = "dall-e-3",
        Size = "1024x1024",
        Quality = "standard",
        Style = "vivid"
    };

    var response = await _chatGPTClient.GenerateImageAdvancedAsync(request);

    if (response?.Data == null || !response.Data.Any())
        return null;

    return response.Data.First().Url;  // Temporary URL — must persist!
}
```

### DALL-E 3 — Generate, Download and Upload to S3

> **Important**: DALL-E returns temporary URLs. Always download and re-upload to your own storage.

```csharp
public async Task<string?> GenerateAndUploadImage(string imagePrompt)
{
    // 1. Generate image
    var imageResponse = await _chatGPTClient.GenerateImageAdvancedAsync(new DallERequest
    {
        Prompt = imagePrompt, Model = "dall-e-3",
        Size = "1024x1024", Quality = "standard", Style = "vivid"
    });

    if (imageResponse?.Data == null || !imageResponse.Data.Any())
        return null;

    var imageUrl = imageResponse.Data.First().Url;
    if (string.IsNullOrWhiteSpace(imageUrl)) return null;

    // 2. Download temporary image
    var imageBytes = await _httpClient.GetByteArrayAsync(imageUrl);

    // 3. Upload to S3
    var fileName = $"ai-generated-{Guid.NewGuid()}.png";
    using var stream = new MemoryStream(imageBytes);
    IFormFile formFile = new FormFileWrapper(stream, fileName, "image/png");

    var uploadedName = await _fileClient.UploadFileAsync("MyBucket", formFile);
    return await _fileClient.GetFileUrlAsync("MyBucket", uploadedName);
}
```

### File Upload — Controller

```csharp
[Route("api/[controller]")]
[ApiController]
public class ImageController : ControllerBase
{
    private readonly IFileClient _fileClient;
    public ImageController(IFileClient fileClient) { _fileClient = fileClient; }

    [RequestSizeLimit(100_000_000)]
    [HttpPost("upload")]
    [Authorize]
    public async Task<ActionResult<string>> Upload(IFormFile file)
    {
        if (file == null || file.Length == 0)
            return BadRequest("No file uploaded");

        var fileName = await _fileClient.UploadFileAsync("MyBucket", file);
        var url = await _fileClient.GetFileUrlAsync("MyBucket", fileName);
        return Ok(url);
    }
}
```

### Slug Generation with Collision Detection

```csharp
public async Task<string> GenerateUniqueSlug(string title, Func<string, bool> slugExists)
{
    string slug;
    int counter = 0;
    do
    {
        slug = await _stringClient.GenerateSlugAsync(title);
        if (counter > 0) slug += counter.ToString();  // "my-slug", "my-slug1", "my-slug2"
        counter++;
    } while (slugExists(slug));
    return slug;
}
```

### FormFileWrapper (for programmatic uploads)

```csharp
internal class FormFileWrapper : IFormFile
{
    private readonly Stream _stream;
    private readonly string _fileName;
    private readonly string _contentType;

    public FormFileWrapper(Stream stream, string fileName, string contentType)
    { _stream = stream; _fileName = fileName; _contentType = contentType; }

    public string ContentType => _contentType;
    public string ContentDisposition => $"form-data; name=\"file\"; filename=\"{_fileName}\"";
    public IHeaderDictionary Headers => new HeaderDictionary();
    public long Length => _stream.Length;
    public string Name => "file";
    public string FileName => _fileName;

    public void CopyTo(Stream target) => _stream.CopyTo(target);
    public Task CopyToAsync(Stream target, CancellationToken ct = default) => _stream.CopyToAsync(target, ct);
    public Stream OpenReadStream() => _stream;
}
```

---

## Common Patterns

### AI Content Generation with Structured JSON

```csharp
public async Task<MyDto> GenerateWithAI(string prompt)
{
    var messages = new List<ChatMessage>
    {
        new ChatMessage { Role = "system", Content = "Return ONLY valid JSON: {\"title\":\"\",\"body\":\"\",\"tags\":\"\"}" },
        new ChatMessage { Role = "user", Content = prompt }
    };
    var response = await _chatGPTClient.SendConversationAsync(messages);

    // Strip markdown wrapper, then deserialize
    var clean = response.Trim();
    if (clean.StartsWith("```json")) { clean = clean[7..]; if (clean.EndsWith("```")) clean = clean[..^3]; clean = clean.Trim(); }

    return JsonSerializer.Deserialize<MyDto>(clean, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
}
```

### Combined AI + Image + Storage Pipeline

```csharp
public async Task<ArticleResult> CreateArticleWithAI(string prompt, bool withImage)
{
    var content = await GenerateWithAI(prompt);

    string? imageUrl = null;
    if (withImage && !string.IsNullOrEmpty(content.ImagePrompt))
        imageUrl = await GenerateAndUploadImage(content.ImagePrompt);

    var slug = await _stringClient.GenerateSlugAsync(content.Title);

    return new ArticleResult { Title = content.Title, Content = content.Body, Slug = slug, ImageUrl = imageUrl };
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| ChatGPT returns empty | zTools API unreachable | Verify `zTools:ApiURL` in appsettings |
| DALL-E URL expired | Temporary URLs not persisted | Download and re-upload to S3 via `IFileClient` |
| `GenerateSlugAsync` empty | Empty input | Validate input before calling |
| File upload fails | File too large | Add `[RequestSizeLimit]` to controller |
| DI error | Missing registration | Add `services.AddScoped<IChatGPTClient, ChatGPTClient>()` |
| JSON wrapped in markdown | ChatGPT formatting | Strip `` ```json `` / `` ``` `` before deserializing |
| Slug collision | Duplicate in DB | Use retry loop with counter suffix |

---

## Response Guidelines

1. **Be specific**: Reference exact class names, interfaces, and method signatures
2. **Show code**: Include working examples based on the patterns above
3. **Context-aware**: If in NNews project, reference existing files (ArticleAIService.cs, ImageController.cs, TagService.cs)
4. **Minimal changes**: Only suggest what's needed for the user's question
5. **DALL-E**: Always remind about temporary URLs needing persistence via `IFileClient`
