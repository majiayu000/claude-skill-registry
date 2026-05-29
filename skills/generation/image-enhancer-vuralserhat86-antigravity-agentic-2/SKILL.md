---
name: image_enhancer
router_kit: FullStackKit
description: Improves the quality of images, especially screenshots, by enhancing resolution, sharpness, and clarity. Perfect for preparing images for presentations, documentation, or social media posts.
metadata:
  skillport:
    category: auto-healed
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, filters, git, image enhancer, opencv, optimization, processing, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, upscaling, utilities, version control, workflow]
---

# Image Enhancer

This skill takes your images and screenshots and makes them look better—sharper, clearer, and more professional.

## When to Use This Skill

- Improving screenshot quality for blog posts or documentation
- Enhancing images before sharing on social media
- Preparing images for presentations or reports
- Upscaling low-resolution images
- Sharpening blurry photos
- Cleaning up compressed images

## What This Skill Does

1. **Analyzes Image Quality**: Checks resolution, sharpness, and compression artifacts
2. **Enhances Resolution**: Upscales images intelligently
3. **Improves Sharpness**: Enhances edges and details
4. **Reduces Artifacts**: Cleans up compression artifacts and noise
5. **Optimizes for Use Case**: Adjusts based on intended use (web, print, social media)

## How to Use

### Basic Enhancement

```
Improve the image quality of screenshot.png
```

```
Enhance all images in this folder
```

### Specific Improvements

```
Upscale this image to 4K resolution
```

```
Sharpen this blurry screenshot
```

```
Reduce compression artifacts in this image
```

### Batch Processing

```
Improve the quality of all PNG files in this directory
```

## Example

**User**: "Improve the image quality of screenshot-2024.png"

**Output**:
```
Analyzing screenshot-2024.png...

Current specs:
- Resolution: 1920x1080
- Format: PNG
- Quality: Good, but slight blur

Enhancements applied:
✓ Upscaled to 2560x1440 (retina)
✓ Sharpened edges
✓ Enhanced text clarity
✓ Optimized file size

Saved as: screenshot-2024-enhanced.png
Original preserved as: screenshot-2024-original.png
```

**Inspired by:** Lenny Rachitsky's workflow from his newsletter - used for screenshots in his articles

## Tips

- Always keeps original files as backup
- Works best with screenshots and digital images
- Can batch process entire folders
- Specify output format if needed (PNG for quality, JPG for smaller size)
- For social media, mention the platform for optimal sizing

## Common Use Cases

- **Blog Posts**: Enhance screenshots before publishing
- **Documentation**: Make UI screenshots crystal clear
- **Social Media**: Optimize images for Twitter, LinkedIn, Instagram
- **Presentations**: Upscale images for large screens
*Image Enhancer v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [OpenCV Best Practices](https://opencv.org/) & [Lenny's Newsletter](https://www.lennysnewsletter.com/)

### Aşama 1: Pre-processing
- [ ] **Analysis**: Histogram ve çözünürlük analizi yap.
- [ ] **Noise Reduction**: Denoising (Gaussian Blur veya AI tabanlı) uygula.
- [ ] **Format**: Kayıpsız düzenleme için RAW veya PNG formatına çevir.

### Aşama 2: Enhancement
- [ ] **Upscaling**: AI Upscaler (ESRGAN, SwinIR) ile x2 veya x4 çözünürlük artır.
- [ ] **Sharpening**: Unsharp Masking ile kenarları belirginleştir.
- [ ] **Correction**: Renk dengesi ve kontrast ayarlarını optimize et.

### Aşama 3: Output Optimization
- [ ] **Compression**: Web için MozJPEG veya TinyPNG ile sıkıştır (Görsel kaliteyi koruyarak).
- [ ] **Metadata**: Gereksiz EXIF verilerini temizle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Yazılar okunabilir durumda mı (OCR testi)? |
| 2 | Upscaling sonrası "yapaylık" (artifacts) oluştu mu? |
| 3 | Dosya boyutu web kullanımı için uygun mu (<200KB)? |

