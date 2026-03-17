---
name: orchardcore-media
description: Skill for managing media in Orchard Core. Covers media library configuration, media profiles, image processing, media field usage, and storage providers.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Media - Prompt Templates

## Configure Media Management

You are an Orchard Core expert. Generate configuration and code for managing media in Orchard Core.

### Guidelines

- Enable `OrchardCore.Media` to use the media library.
- Media files are stored under `/media/` by default using the file system.
- Azure Blob Storage and Amazon S3 can be configured as alternative storage providers.
- Media profiles define image processing pipelines (resize, crop, format conversion).
- Use `MediaField` on content types to allow users to attach media files.
- Media processing uses ImageSharp for image transformations.
- Configure allowed file extensions and max file size in media settings.
- Use media tokens in Liquid templates to generate processed image URLs.

### Enabling Media Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Media",
        "OrchardCore.Media.Indexing",
        "OrchardCore.Media.Cache"
      ],
      "disable": []
    }
  ]
}
```

### Media Settings Configuration

```json
{
  "OrchardCore": {
    "OrchardCore_Media": {
      "MaxFileSize": 104857600,
      "AllowedFileExtensions": [
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
        ".svg", ".pdf", ".doc", ".docx", ".mp4"
      ],
      "CdnBaseUrl": "https://cdn.example.com"
    }
  }
}
```

### Azure Blob Storage Configuration

```json
{
  "OrchardCore": {
    "OrchardCore_Media_Azure": {
      "ConnectionString": "{{AzureConnectionString}}",
      "ContainerName": "media",
      "BasePath": "{{TenantName}}"
    }
  }
}
```

### Media Profiles via Recipe

```json
{
  "steps": [
    {
      "name": "MediaProfiles",
      "MediaProfiles": {
        "{{ProfileName}}": {
          "Hint": "{{Description}}",
          "Width": 800,
          "Height": 600,
          "Mode": "Crop",
          "Format": "webp",
          "Quality": 80
        }
      }
    }
  ]
}
```

Processing modes include:
- `Crop` - Crops the image to the exact dimensions.
- `Pad` - Pads the image to fit dimensions.
- `BoxPad` - Pads the image within a box.
- `Max` - Resizes to fit within max dimensions while preserving aspect ratio.
- `Min` - Resizes to fit minimum dimensions.
- `Stretch` - Stretches the image to exact dimensions.

### Using Media in Liquid Templates

```liquid
<!-- Display an image with a media profile -->
<img src="{{ Model.ContentItem.Content.MyPart.Image.Paths[0] | asset_url | append: '?width=400&height=300&rmode=crop' }}" />

<!-- Using a named media profile -->
<img src="{{ Model.ContentItem.Content.MyPart.Image.Paths[0] | asset_url | append: '?profile=thumbnail' }}" />

<!-- Responsive images -->
<img src="{{ Model.ContentItem.Content.MyPart.Image.Paths[0] | asset_url | append: '?width=800' }}"
     srcset="{{ Model.ContentItem.Content.MyPart.Image.Paths[0] | asset_url | append: '?width=400' }} 400w,
             {{ Model.ContentItem.Content.MyPart.Image.Paths[0] | asset_url | append: '?width=800' }} 800w,
             {{ Model.ContentItem.Content.MyPart.Image.Paths[0] | asset_url | append: '?width=1200' }} 1200w" />
```

### Custom Media Processing

```csharp
using OrchardCore.Media.Processing;

public sealed class CustomMediaResizingFilter : IMediaEventHandler
{
    public Task MediaCreatingAsync(MediaCreatingContext context)
    {
        // Custom logic before media is created
        return Task.CompletedTask;
    }
}
```

### Attaching Media Field to Content Type

```csharp
_contentDefinitionManager.AlterPartDefinition("ArticlePart", part => part
    .WithField("FeaturedImage", field => field
        .OfType("MediaField")
        .WithDisplayName("Featured Image")
        .WithSettings(new MediaFieldSettings
        {
            Multiple = false,
            AllowMediaText = true,
            AllowAnchors = true
        })
    )
);
```
