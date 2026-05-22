---
name: lexical-editor-image-management
description: Implement Lexical Editor with automatic image management using Laravel Observers. Converts base64 images to file storage, deletes unused images, and handles cleanup. Use when building WYSIWYG editors with rich content, managing media uploads in editors, implementing automatic image optimization, or setting up Observer-based storage management for rich text editors.
---

# Lexical Editor Image Management

Complete guide for implementing Lexical Editor with automatic image management using a **reusable Trait approach**. This skill transforms base64 images from rich text editors into optimized storage files and automatically cleans up unused images.

## When to use this Skill

Use this Skill when you need to:
- Implement Lexical Editor or similar WYSIWYG editors with image uploads
- Convert base64 images to actual file storage
- Automatically delete unused images from storage
- Manage media files in rich text content
- Optimize storage usage in Laravel applications
- Build reusable image lifecycle management across multiple models
- Handle cleanup of old images when content is updated or deleted

## Quick Start (Trait Approach - Recommended)

### Step 1: Install Lexical Editor Package

```bash
composer require malzariey/filament-lexical-editor
```

### Step 2: Create RichEditorMedia Model & Migration

```bash
php artisan make:model RichEditorMedia -m
```

**Migration:**
```php
Schema::create('rich_editor_media', function (Blueprint $table) {
    $table->id();
    $table->string('model_type');
    $table->unsignedBigInteger('model_id');
    $table->string('field_name');
    $table->string('file_path');
    $table->string('disk')->default('public');
    $table->timestamps();
    $table->index(['model_type', 'model_id']);
});
```

**Model:**
```php
class RichEditorMedia extends Model
{
    protected $fillable = ['model_type', 'model_id', 'field_name', 'file_path', 'disk'];

    public function model(): MorphTo
    {
        return $this->morphTo();
    }
}
```

### Step 3: Create HasRichEditorMedia Trait

Create `app/Models/Concerns/HasRichEditorMedia.php`:

See [references/trait-implementation.md](./references/trait-implementation.md) for complete trait code.

### Step 4: Create Observer for RichEditorMedia

```php
// app/Observers/RichEditorMediaObserver.php
class RichEditorMediaObserver
{
    public function deleted(RichEditorMedia $media): void
    {
        if ($media->file_path && Storage::disk($media->disk)->exists($media->file_path)) {
            Storage::disk($media->disk)->delete($media->file_path);
        }
    }
}
```

Register in `AppServiceProvider`:
```php
RichEditorMedia::observe(RichEditorMediaObserver::class);
```

### Step 5: Apply Trait to Model

```php
use App\Models\Concerns\HasRichEditorMedia;

class Product extends Model
{
    use HasRichEditorMedia;
    
    protected array $richEditorFields = ['description']; // Fields using Lexical Editor
}
```

### Step 6: Configure Filament Resource

```php
use Malzariey\FilamentLexicalEditor\LexicalEditor;

LexicalEditor::make('description')
    ->label('Mô tả')
    ->helperText('Ảnh paste/upload sẽ tự lưu ra file, không lưu base64 vào DB.')
    ->columnSpanFull()
```

## How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│        Lexical Editor (Filament Admin)              │
│  - User paste/upload image in editor                │
│  - Image embedded as base64 in HTML                 │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│      HasRichEditorMedia Trait (Model)               │
│  - bootHasRichEditorMedia() registers events        │
│  - saving: convertBase64ImagesToFiles()             │
│  - saved: cleanupRemovedRichEditorImages()          │
│  - saved: syncRichEditorMedia()                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│      File Storage (Dated directories)               │
│  storage/app/public/uploads/{model}/content/Y/m/d/  │
│  - product-lexical-1734123456-abc12345.jpg          │
│  - product-lexical-1734123457-def67890.png          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│      RichEditorMedia Table (Tracking)               │
│  - Tracks all images per model/field                │
│  - Enables orphan detection & bulk cleanup          │
└─────────────────────────────────────────────────────┘
```

### Workflow Events

1. **updating**: Snapshot old content for comparison
2. **saving**: Convert all base64 images to storage files
3. **saved**: 
   - Compare old/new content and delete unused images
   - Sync tracking table with current images
4. **deleted/forceDeleted**: Clean up all associated files

## Implementation Details

### Base64 Conversion Process

The trait scans content for base64 images using regex pattern:
```
data:image/(png|jpg|jpeg|gif|webp|svg+xml);base64,{data}
```

For each match:
1. Extract MIME type (png, jpg, gif, webp, svg)
2. Decode base64 data to binary
3. Validate size (max 5MB)
4. Generate unique filename: `{model}-lexical-{timestamp}-{random8}.{ext}`
5. Save to dated directory: `uploads/{model}/content/Y/m/d/`
6. Replace base64 string with `/storage/...` URL

Example:
```html
<!-- Before (base64) -->
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA...">

<!-- After (file URL) -->
<img src="/storage/uploads/products/content/2025/12/11/product-lexical-1734123456-abc12345.png">
```

### Image Cleanup Strategy

The trait intelligently tracks images:
- **snapshotRichEditorContent()**: Captures old content before update
- **extractImagePathsFromContent()**: Parses HTML, data-url, and JSON formats
- **cleanupRemovedRichEditorImages()**: Deletes images no longer in content

This prevents accidental deletion of images still in use while cleaning up removed images.

## Storage Structure

```
storage/app/public/
└── uploads/
    ├── products/
    │   └── content/
    │       └── 2025/12/11/
    │           ├── product-lexical-1734123456-abc12345.jpg
    │           └── product-lexical-1734123457-def67890.png
    └── articles/
        └── content/
            └── 2025/12/11/
                └── article-lexical-1734123458-ghi12345.jpg
```

Benefits of dated directory structure:
- Track which images belong to which model
- Prevent accidental deletion of shared images
- Organize cleanup commands by type

## Best Practices

### 1. Image Naming Convention

Use descriptive prefixes for different contexts:
```php
// Post model
$filename = 'lexical-' . time() . '-' . uniqid() . '.' . $extension;

// ServicePost model
$filename = 'service-lexical-' . time() . '-' . uniqid() . '.' . $extension;

// Custom models
$filename = 'custom-lexical-' . time() . '-' . uniqid() . '.' . $extension;
```

### 2. Directory Organization

Separate storage directories by model:
```php
// In Observer
$path = 'uploads/content/' . $filename;              // For Post
$path = 'uploads/service-content/' . $filename;     // For ServicePost
$path = 'uploads/custom-content/' . $filename;      // For custom models
```

### 3. Logging and Monitoring

Always log important operations:
```php
Log::info("Converted base64 image to storage: {$filePath}");
Log::info("Deleted unused content image: {$imagePath}");
Log::error("Failed to convert base64 image: " . $e->getMessage());
```

### 4. Error Handling

Implement graceful error handling:
```php
try {
    // Convert base64 to file
    $filePath = $this->saveBase64AsFile($base64Data, $extension);
} catch (\Exception $e) {
    Log::error("Conversion failed: " . $e->getMessage());
    // Continue processing other images
    continue;
}
```

### 5. Soft Deletes

Consider using soft deletes for safety:
```php
// In Model
use SoftDeletes;

// Allow recovery of deleted models and their images
public function restore()
{
    // Restore images from backup if available
}
```

## Advanced Usage

### Multiple Image Formats

Support different image types:
```php
$supported = ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg+xml'];

// In regex pattern
preg_match_all('/data:image\/(png|jpg|jpeg|gif|webp|svg\+xml);base64,/i', $content);
```

### Image Validation

Validate before saving:
```php
private function validateImage(string $base64Data, string $extension): bool
{
    $imageData = base64_decode($base64Data);
    
    // Check file size (max 5MB)
    if (strlen($imageData) > 5 * 1024 * 1024) {
        throw new \Exception("Image exceeds 5MB limit");
    }
    
    // Verify MIME type
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mime = finfo_buffer($finfo, $imageData);
    finfo_close($finfo);
    
    if (!str_starts_with($mime, 'image/')) {
        throw new \Exception("Invalid image file");
    }
    
    return true;
}
```

### Automatic Resizing

Resize large images:
```php
use Intervention\Image\Facades\Image;

private function optimizeImage(string $path): void
{
    $image = Image::make(storage_path('app/public/' . $path));
    
    // Resize if larger than 1920px
    if ($image->width() > 1920) {
        $image->resize(1920, null, ['aspect_ratio' => true]);
    }
    
    // Compress and save as WebP
    $image->save(str_replace($path, '.webp', $path), 75);
}
```

### Cleanup Command

Create a command to clean unused images:
```bash
php artisan make:command ImagesCleanUnused
```

See [cleanup-command.md](./cleanup-command.md) for complete implementation.

## Common Issues and Solutions

### Issue 1: Images Not Converting

**Symptom**: Base64 images remain in content instead of being saved

**Solutions**:
- Verify Observer is registered in `EventServiceProvider`
- Check storage permissions: `chmod -R 775 storage/app/public/`
- Verify `public` disk is configured in `config/filesystems.php`
- Check logs for conversion errors: `tail -f storage/logs/laravel.log`

### Issue 2: Images Not Displaying

**Symptom**: Images saved but not visible in frontend

**Solutions**:
- Run storage symlink: `php artisan storage:link`
- Verify `storage/app/public` directory exists
- Check file permissions: `chmod -R 755 storage/app/public/uploads/`
- Verify public URL in `config/app.php`

### Issue 3: Orphaned Files

**Symptom**: Old images remain in storage after deletion

**Solutions**:
- Verify `deleted()` event is firing: Add logging
- Check `handleContentImages()` logic for content extraction
- Run cleanup command: `php artisan images:clean-unused --dry-run`
- Manually delete orphaned files: Find files modified before X days

### Issue 4: Observer Not Running

**Symptom**: Model events not triggering

**Solutions**:
```bash
# Clear configuration cache
php artisan config:clear

# Clear application cache
php artisan cache:clear

# Verify Observer is registered
php artisan tinker
>>> Post::getObservableEvents()
```

## Testing

### Unit Testing

```php
public function test_base64_converts_to_file()
{
    $post = Post::create([
        'name' => 'Test Post',
        'content' => '<img src="data:image/png;base64,iVBORw0...">',
    ]);
    
    $this->assertStringContainsString('/storage/uploads/content/', $post->content);
    $this->assertStringNotContainsString('data:image/png;base64', $post->content);
}

public function test_old_image_deleted_on_update()
{
    $post = Post::create(['name' => 'Test', 'image' => 'old.jpg']);
    
    Storage::disk('public')->put('old.jpg', 'dummy content');
    
    $post->update(['image' => 'new.jpg']);
    
    Storage::disk('public')->assertMissing('old.jpg');
}
```

### Feature Testing

```php
public function test_image_cleanup_on_content_update()
{
    $post = Post::create([
        'content' => '<img src="/storage/uploads/content/image1.jpg">
                      <img src="/storage/uploads/content/image2.jpg">',
    ]);
    
    $post->update([
        'content' => '<img src="/storage/uploads/content/image1.jpg">',
    ]);
    
    // image2.jpg should be deleted
    Storage::disk('public')->assertMissing('uploads/content/image2.jpg');
}
```

## Related Resources

- [Observer Implementation Guide](./observer-implementation.md)
- [Cleanup Command Setup](./cleanup-command.md)
- [Frontend Integration](./frontend-integration.md)
- [Troubleshooting Guide](./troubleshooting.md)

## Examples

See [EXAMPLES.md](./EXAMPLES.md) for:
- Complete working Observer class
- Filament Resource configuration
- Cleanup command implementation
- Real-world use cases

## References

- [Laravel Observers Documentation](https://laravel.com/docs/eloquent#observers)
- [Filament File Upload](https://filamentphp.com/docs/3.x/forms/fields/file-upload)
- [Lexical Editor Official](https://lexical.dev/)
- [Malzariey Filament Lexical Editor](https://github.com/malzariey/filament-lexical-editor)

## Validation Checklist

Before deploying to production:

- [ ] Observers registered in `EventServiceProvider`
- [ ] Storage permissions set correctly (775)
- [ ] Storage symlink created: `php artisan storage:link`
- [ ] Base64 regex pattern tested with sample content
- [ ] Image cleanup logic verified with test data
- [ ] Logging configured and monitored
- [ ] Cleanup command scheduled in Kernel.php
- [ ] Backup system in place before cleanup
- [ ] File size limits enforced
- [ ] Image format validation in place

## Output Format

When implementing this Skill, I will:

1. Analyze your current model structure
2. Generate complete Observer class with all lifecycle hooks
3. Provide Filament Resource configuration
4. Create cleanup command if needed
5. Set up logging and monitoring
6. Include comprehensive error handling
7. Provide testing examples
8. Document storage structure
9. Create troubleshooting guide

This ensures a production-ready image management system with automatic cleanup and error recovery.
