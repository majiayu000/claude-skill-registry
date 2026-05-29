---
name: media-asset-management
description: Use when designing digital asset management systems, media libraries, upload pipelines, or asset metadata schemas. Covers media storage patterns, file organization, metadata extraction, and media APIs for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Media Asset Management

Guidance for designing digital asset management systems, media libraries, and upload pipelines for headless CMS.

## When to Use This Skill

- Designing media library architecture
- Implementing file upload pipelines
- Planning asset metadata schemas
- Configuring storage providers
- Building media search and filtering

## Media Asset Model

### Core Entity

```csharp
public class MediaItem
{
    public Guid Id { get; set; }

    // File information
    public string FileName { get; set; } = string.Empty;
    public string Extension { get; set; } = string.Empty;
    public string MimeType { get; set; } = string.Empty;
    public long SizeBytes { get; set; }

    // Storage
    public string StorageProvider { get; set; } = string.Empty;
    public string StoragePath { get; set; } = string.Empty;
    public string PublicUrl { get; set; } = string.Empty;

    // Organization
    public Guid? FolderId { get; set; }
    public MediaFolder? Folder { get; set; }
    public List<string> Tags { get; set; } = new();

    // Metadata
    public MediaMetadata Metadata { get; set; } = new();

    // Audit
    public string UploadedBy { get; set; } = string.Empty;
    public DateTime UploadedUtc { get; set; }
    public DateTime? ModifiedUtc { get; set; }
}

public class MediaMetadata
{
    // Common
    public string? Title { get; set; }
    public string? Description { get; set; }
    public string? Alt { get; set; }
    public string? Caption { get; set; }
    public string? Credit { get; set; }

    // Image-specific
    public int? Width { get; set; }
    public int? Height { get; set; }
    public string? ColorSpace { get; set; }

    // Document-specific
    public int? PageCount { get; set; }
    public string? Author { get; set; }

    // Video-specific
    public TimeSpan? Duration { get; set; }
    public string? Codec { get; set; }
    public int? Bitrate { get; set; }

    // EXIF/XMP
    public Dictionary<string, string> ExifData { get; set; } = new();
}

public class MediaFolder
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Path { get; set; } = string.Empty;
    public Guid? ParentId { get; set; }
    public List<MediaFolder> Children { get; set; } = new();
}
```

## Storage Architecture

### Storage Provider Abstraction

```csharp
public interface IMediaStorageProvider
{
    string ProviderName { get; }

    Task<string> UploadAsync(Stream stream, string path, string contentType);
    Task<Stream> DownloadAsync(string path);
    Task DeleteAsync(string path);
    Task<bool> ExistsAsync(string path);
    string GetPublicUrl(string path);
}

// Azure Blob Storage
public class AzureBlobStorageProvider : IMediaStorageProvider
{
    public string ProviderName => "AzureBlob";

    public async Task<string> UploadAsync(
        Stream stream, string path, string contentType)
    {
        var blobClient = _containerClient.GetBlobClient(path);

        await blobClient.UploadAsync(stream, new BlobHttpHeaders
        {
            ContentType = contentType,
            CacheControl = "public, max-age=31536000"
        });

        return path;
    }

    public string GetPublicUrl(string path)
    {
        return $"{_containerClient.Uri}/{path}";
    }
}

// AWS S3
public class S3StorageProvider : IMediaStorageProvider
{
    public string ProviderName => "S3";

    public async Task<string> UploadAsync(
        Stream stream, string path, string contentType)
    {
        var request = new PutObjectRequest
        {
            BucketName = _bucketName,
            Key = path,
            InputStream = stream,
            ContentType = contentType,
            CannedACL = S3CannedACL.PublicRead
        };

        await _s3Client.PutObjectAsync(request);
        return path;
    }
}

// Local file system
public class LocalStorageProvider : IMediaStorageProvider
{
    public string ProviderName => "Local";

    public async Task<string> UploadAsync(
        Stream stream, string path, string contentType)
    {
        var fullPath = Path.Combine(_basePath, path);
        Directory.CreateDirectory(Path.GetDirectoryName(fullPath)!);

        await using var fileStream = File.Create(fullPath);
        await stream.CopyToAsync(fileStream);

        return path;
    }
}
```

### Path Generation

```csharp
public class MediaPathGenerator
{
    public string GeneratePath(string fileName, PathStrategy strategy)
    {
        var ext = Path.GetExtension(fileName);
        var name = Path.GetFileNameWithoutExtension(fileName);
        var safeName = Slugify(name);

        return strategy switch
        {
            PathStrategy.DateBased => $"{DateTime.UtcNow:yyyy/MM/dd}/{safeName}-{Guid.NewGuid():N}{ext}",
            PathStrategy.HashBased => $"{ComputeHash(fileName)[..2]}/{ComputeHash(fileName)[2..4]}/{Guid.NewGuid():N}{ext}",
            PathStrategy.Flat => $"{Guid.NewGuid():N}{ext}",
            PathStrategy.OriginalName => $"{safeName}-{DateTime.UtcNow:yyyyMMddHHmmss}{ext}",
            _ => throw new ArgumentOutOfRangeException()
        };
    }
}

public enum PathStrategy
{
    DateBased,      // 2025/01/15/image-abc123.jpg
    HashBased,      // ab/cd/abc123.jpg
    Flat,           // abc123.jpg
    OriginalName    // my-image-20250115103045.jpg
}
```

## Upload Pipeline

### Upload Service

```csharp
public class MediaUploadService
{
    public async Task<MediaItem> UploadAsync(
        Stream stream,
        string fileName,
        string contentType,
        UploadOptions? options = null)
    {
        options ??= new UploadOptions();

        // Validate
        ValidateFile(fileName, contentType, stream.Length, options);

        // Generate path
        var path = _pathGenerator.GeneratePath(fileName, options.PathStrategy);

        // Process (resize, optimize)
        var processedStream = await ProcessMediaAsync(stream, contentType, options);

        // Upload to storage
        var storagePath = await _storageProvider.UploadAsync(
            processedStream, path, contentType);

        // Extract metadata
        var metadata = await ExtractMetadataAsync(processedStream, contentType);

        // Create record
        var mediaItem = new MediaItem
        {
            Id = Guid.NewGuid(),
            FileName = fileName,
            Extension = Path.GetExtension(fileName),
            MimeType = contentType,
            SizeBytes = processedStream.Length,
            StorageProvider = _storageProvider.ProviderName,
            StoragePath = storagePath,
            PublicUrl = _storageProvider.GetPublicUrl(storagePath),
            FolderId = options.FolderId,
            Tags = options.Tags ?? new List<string>(),
            Metadata = metadata,
            UploadedBy = _currentUser.UserId,
            UploadedUtc = DateTime.UtcNow
        };

        await _repository.AddAsync(mediaItem);

        // Raise event
        await _mediator.Publish(new MediaUploadedEvent(mediaItem));

        return mediaItem;
    }

    private void ValidateFile(
        string fileName, string contentType, long size, UploadOptions options)
    {
        // Check file size
        if (size > options.MaxFileSizeBytes)
            throw new MediaValidationException($"File exceeds maximum size of {options.MaxFileSizeBytes} bytes");

        // Check allowed types
        if (options.AllowedMimeTypes?.Any() == true &&
            !options.AllowedMimeTypes.Contains(contentType))
            throw new MediaValidationException($"File type {contentType} is not allowed");

        // Check extension
        var ext = Path.GetExtension(fileName).ToLowerInvariant();
        if (options.BlockedExtensions?.Contains(ext) == true)
            throw new MediaValidationException($"File extension {ext} is blocked");
    }
}

public class UploadOptions
{
    public Guid? FolderId { get; set; }
    public List<string>? Tags { get; set; }
    public PathStrategy PathStrategy { get; set; } = PathStrategy.DateBased;
    public long MaxFileSizeBytes { get; set; } = 10 * 1024 * 1024; // 10MB
    public List<string>? AllowedMimeTypes { get; set; }
    public List<string>? BlockedExtensions { get; set; }
    public bool ExtractMetadata { get; set; } = true;
    public ImageProcessingOptions? ImageOptions { get; set; }
}
```

### Metadata Extraction

```csharp
public class MetadataExtractor
{
    public async Task<MediaMetadata> ExtractAsync(Stream stream, string contentType)
    {
        var metadata = new MediaMetadata();

        if (contentType.StartsWith("image/"))
        {
            await ExtractImageMetadataAsync(stream, metadata);
        }
        else if (contentType.StartsWith("video/"))
        {
            await ExtractVideoMetadataAsync(stream, metadata);
        }
        else if (contentType == "application/pdf")
        {
            await ExtractPdfMetadataAsync(stream, metadata);
        }

        return metadata;
    }

    private async Task ExtractImageMetadataAsync(Stream stream, MediaMetadata metadata)
    {
        using var image = await Image.LoadAsync(stream);

        metadata.Width = image.Width;
        metadata.Height = image.Height;

        // Extract EXIF
        if (image.Metadata.ExifProfile != null)
        {
            foreach (var value in image.Metadata.ExifProfile.Values)
            {
                metadata.ExifData[value.Tag.ToString()] = value.GetValue()?.ToString() ?? "";
            }
        }
    }
}
```

## Media Library Features

### Folder Management

```csharp
public class MediaFolderService
{
    public async Task<MediaFolder> CreateFolderAsync(string name, Guid? parentId = null)
    {
        var folder = new MediaFolder
        {
            Id = Guid.NewGuid(),
            Name = name,
            ParentId = parentId,
            Path = await BuildPathAsync(name, parentId)
        };

        await _repository.AddAsync(folder);
        return folder;
    }

    public async Task<List<MediaFolder>> GetFolderTreeAsync()
    {
        var folders = await _repository.GetAllAsync();
        return BuildTree(folders.Where(f => f.ParentId == null));
    }
}
```

### Media Search

```csharp
public class MediaSearchService
{
    public async Task<PagedResult<MediaItem>> SearchAsync(MediaSearchQuery query)
    {
        var queryable = _context.MediaItems.AsQueryable();

        // Filter by folder
        if (query.FolderId.HasValue)
        {
            queryable = queryable.Where(m => m.FolderId == query.FolderId);
        }

        // Filter by type
        if (!string.IsNullOrEmpty(query.MediaType))
        {
            queryable = query.MediaType switch
            {
                "image" => queryable.Where(m => m.MimeType.StartsWith("image/")),
                "video" => queryable.Where(m => m.MimeType.StartsWith("video/")),
                "document" => queryable.Where(m =>
                    m.MimeType == "application/pdf" ||
                    m.MimeType.Contains("document")),
                _ => queryable
            };
        }

        // Filter by tags
        if (query.Tags?.Any() == true)
        {
            queryable = queryable.Where(m =>
                query.Tags.All(t => m.Tags.Contains(t)));
        }

        // Search text
        if (!string.IsNullOrEmpty(query.SearchText))
        {
            var search = query.SearchText.ToLower();
            queryable = queryable.Where(m =>
                m.FileName.ToLower().Contains(search) ||
                m.Metadata.Title!.ToLower().Contains(search) ||
                m.Metadata.Description!.ToLower().Contains(search));
        }

        // Apply sorting
        queryable = query.SortBy switch
        {
            "name" => queryable.OrderBy(m => m.FileName),
            "date" => queryable.OrderByDescending(m => m.UploadedUtc),
            "size" => queryable.OrderByDescending(m => m.SizeBytes),
            _ => queryable.OrderByDescending(m => m.UploadedUtc)
        };

        return await queryable.ToPagedResultAsync(query.Page, query.PageSize);
    }
}

public class MediaSearchQuery
{
    public Guid? FolderId { get; set; }
    public string? MediaType { get; set; }
    public List<string>? Tags { get; set; }
    public string? SearchText { get; set; }
    public string? SortBy { get; set; }
    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 20;
}
```

## Media API

### Endpoints

```text
POST   /api/media/upload              # Upload single file
POST   /api/media/upload/bulk         # Bulk upload
GET    /api/media                     # List/search media
GET    /api/media/{id}                # Get media item
DELETE /api/media/{id}                # Delete media
PATCH  /api/media/{id}                # Update metadata

# Folders
GET    /api/media/folders             # Get folder tree
POST   /api/media/folders             # Create folder
DELETE /api/media/folders/{id}        # Delete folder
```

### Media Response

```json
{
  "data": {
    "id": "media-123",
    "fileName": "hero-image.jpg",
    "mimeType": "image/jpeg",
    "sizeBytes": 245678,
    "url": "https://cdn.example.com/media/2025/01/15/hero-image-abc123.jpg",
    "metadata": {
      "title": "Homepage Hero",
      "alt": "Team working together",
      "width": 1920,
      "height": 1080
    },
    "folder": {
      "id": "folder-456",
      "name": "Homepage",
      "path": "/Marketing/Homepage"
    },
    "tags": ["hero", "homepage", "team"],
    "uploadedBy": "user-789",
    "uploadedUtc": "2025-01-15T10:30:00Z"
  }
}
```

## Related Skills

- `image-optimization` - Image processing and optimization
- `cdn-media-delivery` - CDN configuration and delivery
- `content-type-modeling` - Media fields in content types
