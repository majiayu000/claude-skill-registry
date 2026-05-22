---
name: laravel-medialibrary
description: Manage media files (images, PDFs, videos) in Laravel using Spatie's Media Library. Handle file uploads, store files on any filesystem (S3, local), generate image conversions (thumbnails, responsive images), manage file metadata with custom properties, and serve files with automatic URL generation. Use when implementing file upload functionality, image processing, media collections, responsive images, or file management in Laravel applications.
---

# Laravel Media Library

Comprehensive file management package for Laravel that associates files with Eloquent models. Handles uploads, storage on any filesystem, image conversions, metadata, and responsive images.

## Quick Start

**1. Install and Setup**

```bash
composer require spatie/laravel-medialibrary
php artisan migrate
php artisan vendor:publish --provider="Spatie\MediaLibrary\MediaLibraryServiceProvider" --tag="config"
```

**2. Add to Model**

```php
use Spatie\MediaLibrary\HasMedia;
use Spatie\MediaLibrary\InteractsWithMedia;

class Article extends Model implements HasMedia
{
    use InteractsWithMedia;
    
    public function registerMediaCollections(): void
    {
        $this->addMediaCollection('images')->singleFile();
        $this->addMediaCollection('gallery');
    }
    
    public function registerMediaConversions(?Media $media = null): void
    {
        $this->addMediaConversion('thumb')
            ->width(150)
            ->height(150);
    }
}
```

**3. Upload Files**

```php
// From request
$article->addMedia($request->file('image'))
    ->toMediaCollection('images');

// From URL
$article->addMediaFromUrl('https://example.com/photo.jpg')
    ->toMediaCollection('gallery');

// From base64
$article->addMediaFromBase64($base64String)
    ->toMediaCollection('images');
```

**4. Get Media**

```php
// Get media URLs
$article->getFirstMediaUrl('images'); // original
$article->getFirstMediaUrl('images', 'thumb'); // conversion

// Get media items
$media = $article->getMedia('gallery');
$firstImage = $article->getFirstMedia('images');

// Check if has media
if ($article->hasMedia('gallery')) {
    // do something
}
```

## Collections & Storage

**Define Collections with Validation**

```php
public function registerMediaCollections(): void
{
    // Single file collection
    $this->addMediaCollection('avatar')
        ->singleFile()
        ->acceptsMimeTypes(['image/jpeg', 'image/png']);
    
    // Keep only 5 latest files
    $this->addMediaCollection('photos')
        ->onlyKeepLatest(5);
    
    // Custom disk (S3)
    $this->addMediaCollection('videos')
        ->useDisk('s3');
    
    // With fallback image
    $this->addMediaCollection('thumbnail')
        ->useFallbackUrl('/images/default.png');
    
    // Custom validation
    $this->addMediaCollection('documents')
        ->acceptsFile(function ($file) {
            return $file->size < 5000000;
        })
        ->acceptsMimeTypes(['application/pdf']);
}
```

**Specify Disk During Upload**

```php
$article->addMedia($request->file('video'))
    ->toMediaCollection('videos', 's3'); // s3 disk
```

## Image Conversions

**Define Conversions**

```php
public function registerMediaConversions(?Media $media = null): void
{
    // Basic resize
    $this->addMediaConversion('thumb')
        ->width(150)
        ->height(150);
    
    // Crop and format
    $this->addMediaConversion('hero')
        ->crop(1200, 600)
        ->format('webp')
        ->quality(90);
    
    // Collection-specific
    $this->addMediaConversion('preview')
        ->performOnCollections('gallery', 'images');
    
    // Keep original format
    $this->addMediaConversion('large')
        ->width(1920)
        ->keepOriginalImageFormat();
    
    // Non-queued (sync)
    $this->addMediaConversion('sync-thumb')
        ->width(100)
        ->nonQueued();
}
```

**Regenerate Conversions**

```bash
# All conversions
php artisan media-library:regenerate

# For specific model
php artisan media-library:regenerate --model="App\Models\Article"

# Specific IDs
php artisan media-library:regenerate --ids=1,2,3 --model="App\Models\Article"

# Only certain conversions
php artisan media-library:regenerate --only=thumb,large
```

## Responsive Images

**Enable Responsive Images**

```php
// In collection
public function registerMediaCollections(): void
{
    $this->addMediaCollection('images')
        ->withResponsiveImages();
}

// In conversion
public function registerMediaConversions(?Media $media = null): void
{
    $this->addMediaConversion('hero')
        ->width(1920)
        ->withResponsiveImages();
}

// During upload
$article->addMedia($request->file('image'))
    ->withResponsiveImages()
    ->toMediaCollection('images');
```

**Get Responsive URLs**

```php
$media = $article->getFirstMedia('images');

// Get srcset attribute
$srcset = $media->getSrcset();
$heroSrcset = $media->getSrcset('hero');

// Check if available
if ($media->hasResponsiveImages()) {
    echo $media->getUrl();
}
```

## Custom Properties & Metadata

**Store and Retrieve Metadata**

```php
// Upload with custom properties
$article->addMedia($request->file('file'))
    ->withCustomProperties([
        'author' => 'John Doe',
        'tags' => ['important', 'archived'],
        'version' => '1.0'
    ])
    ->toMediaCollection('documents');

// Set/update properties
$media = $article->getFirstMedia('documents');
$media->setCustomProperty('reviewed', true)
    ->setCustomProperty('reviewer', 'Jane Smith')
    ->save();

// Get properties
$author = $media->getCustomProperty('author');
$default = $media->getCustomProperty('status', 'pending');

// Check exists
if ($media->hasCustomProperty('approved')) {
    // do something
}

// Remove property
$media->forgetCustomProperty('draft')->save();
```

## Multiple Files & Batch Operations

**Multiple Uploads**

```php
// Specific keys from request
$fileAdders = $article->addMultipleMediaFromRequest(['image1', 'image2']);
foreach ($fileAdders as $adder) {
    $adder->toMediaCollection('gallery');
}

// All files from request
$allAdders = $article->addAllMediaFromRequest();
foreach ($allAdders as $key => $adder) {
    $adder->toMediaCollection('uploads');
}

// Single file from request key
$article->addMediaFromRequest('featured_image')
    ->toMediaCollection('images');
```

**Update & Delete Media**

```php
// Update media
$media = Media::find(1);
$media->name = 'New Name';
$media->setCustomProperty('status', 'active');
$media->save();

// Update collection
$newArray = [
    ['id' => 1, 'name' => 'First', 'custom_properties' => ['order' => 1]],
    ['id' => 2, 'name' => 'Second', 'custom_properties' => ['order' => 2]],
];
$article->updateMedia($newArray, 'gallery');

// Clear collection
$article->clearMediaCollection('gallery');

// Delete specific media
$article->deleteMedia(1); // by ID
$article->deleteMedia($media); // by object

// Move to another model
$newMedia = $media->move($product, 'photos');

// Copy to another model
$copied = $media->copy($product, 'photos');
```

## Advanced Features

**Filtering Media**

```php
// Filter by custom property
$featured = $article->getMedia('gallery', function ($media) {
    return $media->getCustomProperty('featured') === true;
});

// Filter by mime type
$pdfs = $article->getMedia('documents', function ($media) {
    return $media->mime_type === 'application/pdf';
});

// Filter by date
$recent = $article->getMedia('images', function ($media) {
    return $media->created_at->isAfter(now()->subDays(7));
});
```

**Stream & Download**

```php
// Download response
Route::get('/media/{media}/download', function (Media $media) {
    return $media->toResponse(request());
});

// Inline display
Route::get('/media/{media}/view', function (Media $media) {
    return $media->toInlineResponse(request());
});

// Stream with custom chunk size
Route::get('/media/{media}/stream', function (Media $media) {
    return $media
        ->setStreamChunkSize(2 * 1024 * 1024)
        ->toResponse(request());
});
```

**ZIP Downloads**

```php
use Spatie\MediaLibrary\Support\MediaStream;

// Single collection
Route::get('/article/{article}/photos.zip', function (Article $article) {
    return MediaStream::create('photos.zip')
        ->addMedia($article->getMedia('photos'));
});

// Multiple collections
Route::get('/article/{article}/all.zip', function (Article $article) {
    return MediaStream::create('all.zip')
        ->addMedia($article->getMedia('images'))
        ->addMedia($article->getMedia('documents'));
});
```

**Email Attachments**

```php
class InvoiceMail extends Mailable
{
    public function build()
    {
        return $this->view('emails.invoice')
            ->attach($this->article->getFirstMedia('invoices')->toMailAttachment());
    }
}

// With conversion
$mail->attach($media->mailAttachment('pdf-preview'));
```

**Render as HTML**

```php
$media = $article->getFirstMedia('images');

// Basic img tag
echo $media->img();

// With conversion
echo $media->img('thumb');

// With attributes
echo $media->img('thumb', ['class' => 'thumbnail', 'loading' => 'lazy']);

// In Blade
{!! $media->img('thumb', ['class' => 'img-fluid']) !!}
```

## Configuration & Customization

**config/media-library.php**

```php
return [
    'disk_name' => env('MEDIA_DISK', 's3'), // S3 by default
    'queue_conversions_by_default' => true, // Queue all conversions
    'queue_name' => 'media-conversions',
    'temporary_url_default_lifetime' => 60, // 1 hour temp URLs
    'path_generator' => CustomPathGenerator::class,
    'url_generator' => CustomUrlGenerator::class,
    'file_namer' => CustomFileNamer::class,
];
```

**Custom Path Generator**

```php
use Spatie\MediaLibrary\Support\PathGenerator\PathGenerator;

class CustomPathGenerator implements PathGenerator
{
    public function getPath(Media $media): string
    {
        return $media->model_type . '/' . $media->model_id . '/';
    }
    
    public function getPathForConversions(Media $media): string
    {
        return $this->getPath($media) . 'conversions/';
    }
}
```

**Custom URL Generator**

```php
use Spatie\MediaLibrary\Support\UrlGenerator\BaseUrlGenerator;

class CustomUrlGenerator extends BaseUrlGenerator
{
    public function getUrl(): string
    {
        return 'https://cdn.example.com/' . $this->getPathRelativeToRoot();
    }
}
```

## Common Patterns

**Model with All Features**

```php
class Product extends Model implements HasMedia
{
    use InteractsWithMedia;
    
    public function registerMediaCollections(): void
    {
        $this->addMediaCollection('thumbnail')
            ->singleFile()
            ->acceptsMimeTypes(['image/jpeg', 'image/png']);
        
        $this->addMediaCollection('gallery')
            ->onlyKeepLatest(10)
            ->withResponsiveImages();
        
        $this->addMediaCollection('manuals')
            ->acceptsMimeTypes(['application/pdf']);
    }
    
    public function registerMediaConversions(?Media $media = null): void
    {
        $this->addMediaConversion('thumb')
            ->width(150)
            ->height(150);
        
        $this->addMediaConversion('hero')
            ->width(1200)
            ->height(600)
            ->withResponsiveImages()
            ->performOnCollections('gallery');
    }
}
```

**Upload & Redirect**

```php
class ProductController extends Controller
{
    public function store(Request $request)
    {
        $product = Product::create($request->validated());
        
        if ($request->hasFile('thumbnail')) {
            $product->addMedia($request->file('thumbnail'))
                ->toMediaCollection('thumbnail');
        }
        
        if ($request->hasFile('images')) {
            foreach ($request->file('images') as $image) {
                $product->addMedia($image)
                    ->toMediaCollection('gallery');
            }
        }
        
        return redirect()->route('products.show', $product);
    }
}
```

**Display Media**

```php
@if($product->hasMedia('thumbnail'))
    <img src="{{ $product->getFirstMediaUrl('thumbnail', 'thumb') }}" 
         srcset="{{ $product->getFirstMedia('thumbnail')->getSrcset() }}"
         alt="{{ $product->name }}"
         loading="lazy">
@endif

@foreach($product->getMedia('gallery') as $photo)
    <img src="{{ $photo->getUrl('hero') }}"
         srcset="{{ $photo->getSrcset('hero') }}"
         alt="{{ $photo->name }}">
@endforeach
```

## Best Practices

- Use **collections** to organize different media types (thumbnail, gallery, documents)
- Define **conversions** in `registerMediaConversions()` for consistent image processing
- Enable **responsive images** for better mobile performance
- Use **custom properties** to store metadata (featured, approved, author, etc.)
- **Queue conversions** for large files to avoid blocking requests
- Use **disk configuration** to store on S3 for production
- **Filter media** programmatically using callbacks for complex queries
- Add **custom validation** in collections to enforce rules
- Use **temporary URLs** for private files (S3 signed URLs)
- Implement **soft deletes** on media when needed

For advanced usage, see [reference.md](reference.md).
