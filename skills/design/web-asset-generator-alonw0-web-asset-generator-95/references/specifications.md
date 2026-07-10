# Web Asset Specifications and Best Practices

## Favicon Specifications

### Standard Sizes
- **16x16px**: Classic favicon size, shown in browser tabs
- **32x32px**: Standard browser favicon, taskbar icons
- **96x96px**: Google TV favicon
- **favicon.ico**: Multi-resolution ICO file (contains 16x16 and 32x32)

### Best Practices
- Use simple, recognizable designs that work at small sizes
- Ensure good contrast for visibility
- Test how the icon looks on both light and dark backgrounds
- Avoid too much detail - it won't be visible at 16x16

## App Icons (PWA/Mobile)

### Sizes
- **180x180px**: Apple touch icon (iOS Safari)
- **192x192px**: Android Chrome icon
- **512x512px**: Android Chrome high-res icon, PWA splash screens

### Best Practices
- Use square images with no transparency (or solid background)
- Avoid text that becomes unreadable at smaller sizes
- Design should be recognizable as your brand
- Consider safe area: iOS rounds corners, Android may apply masks

## Open Graph (Social Media Meta Images)

### Primary Sizes
- **1200x630px** (1.91:1 ratio): Facebook, LinkedIn, WhatsApp, most platforms
- **1200x675px** (16:9 ratio): Twitter summary card with large image
- **1200x1200px** (1:1 ratio): Square variant for some contexts

### Platform-Specific Notes

#### Facebook
- Recommended: 1200x630px
- Minimum: 600x315px
- Ratio: 1.91:1
- File size: <8MB
- Shown in news feed, shared posts, link previews

#### Twitter
- Summary card large image: 1200x675px (16:9)
- Summary card: 1200x1200px (1:1)
- Minimum: 300x157px
- File size: <5MB
- Use `twitter:card` meta tag to specify card type

#### WhatsApp
- Uses Open Graph tags (same as Facebook)
- Recommended: 1200x630px
- Shows preview when link is shared

#### LinkedIn
- Recommended: 1200x627px
- Minimum: 1200x628px
- Aspect ratio: 1.91:1

### Content Best Practices
- Keep important content in the "safe zone" (center 80% of image)
- Use large, readable text (minimum 60pt font)
- Include your logo or branding
- Avoid clutter - less is more for social sharing
- Test on both desktop and mobile previews
- Use high-contrast colors for readability
- Consider how image looks in small previews

### Text Guidelines
- Maximum ~40 characters per line for readability
- Use 2-3 lines of text maximum
- Font size: 80-120px for 1200px width
- Leave breathing room around text

## HTML Implementation

### Favicon HTML Tags
```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/android-chrome-512x512.png">
```

### Open Graph Meta Tags
```html
<!-- Basic Open Graph -->
<meta property="og:title" content="Your Page Title">
<meta property="og:description" content="Your page description">
<meta property="og:image" content="https://yoursite.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Description of the image">
<meta property="og:url" content="https://yoursite.com/page">
<meta property="og:type" content="website">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Your Page Title">
<meta name="twitter:description" content="Your page description">
<meta name="twitter:image" content="https://yoursite.com/twitter-image.png">
<meta name="twitter:image:alt" content="Description of the image">
```

## File Format Guidelines

### For Favicons and Icons
- **Format**: PNG with transparency
- **Color mode**: RGBA
- **Optimization**: Use PNG optimization (e.g., pngquant)
- **ICO file**: For favicon.ico, include 16x16 and 32x32 sizes

### For Open Graph Images
- **Format**: PNG or JPEG
- **PNG**: Better for graphics with text, logos, flat colors
- **JPEG**: Better for photos, complex images
- **File size**: Keep under 1MB for fast loading
- **Color mode**: RGB (not CMYK)

## Color Considerations

### Contrast
- Ensure sufficient contrast for readability (WCAG AA minimum 4.5:1)
- Test on various backgrounds (light mode, dark mode)

### Brand Colors
- Use brand colors consistently across assets
- Consider how colors appear at different sizes
- Test color visibility in small icons

## Testing Your Assets

### Tools
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

### Checklist
- [ ] View favicon in browser tab at 100% and 200% zoom
- [ ] Test Open Graph preview on target platforms
- [ ] Check mobile rendering
- [ ] Verify image loads quickly
- [ ] Confirm text is readable at all sizes
- [ ] Test with various link sharing methods

## Common Pitfalls to Avoid

1. **Too much detail in small icons**: Simplify designs for favicons
2. **Text too small**: Use large fonts (80px+) for Open Graph images
3. **Forgetting safe zones**: Keep content away from edges
4. **Wrong aspect ratios**: Using 1:1 image for 1.91:1 requirement causes cropping
5. **Large file sizes**: Optimize images to reduce load time
6. **Absolute URLs**: Use absolute URLs for Open Graph images (https://...)
7. **Missing alt text**: Always provide descriptive alt text for accessibility
8. **Not testing**: Always test how assets appear on actual platforms
