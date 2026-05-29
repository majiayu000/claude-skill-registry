---
name: swift-app-icons
description: App icons, SF Symbols, and launch screens for iOS/macOS/watchOS/visionOS. Use when adding app icons, using SF Symbols, configuring launch screens, or setting up Asset Catalogs.
user-invocable: false
---

# Swift App Icons & Assets

## App Icon Requirements

### Single-Size Mode (Xcode 15+, Recommended)

Provide ONE 1024x1024 PNG. Xcode generates all sizes automatically.

**Asset Catalog structure:**
```
AppIcon.appiconset/
├── Contents.json
└── AppIcon.png (1024x1024)
```

### iOS 26 Dark & Tinted Icons

```json
{
  "images": [
    { "idiom": "universal", "platform": "ios", "size": "1024x1024", "filename": "icon-light.png" },
    { "appearances": [{"appearance": "luminosity", "value": "dark"}],
      "idiom": "universal", "platform": "ios", "size": "1024x1024", "filename": "icon-dark.png" },
    { "appearances": [{"appearance": "luminosity", "value": "tinted"}],
      "idiom": "universal", "platform": "ios", "size": "1024x1024", "filename": "icon-tinted.png" }
  ]
}
```

**Design rules:**
- **Dark**: Gradient `#313131` → `#141414`, transparent background
- **Tinted**: Grayscale, black background, 100%→60% opacity gradient

## SF Symbols

```swift
// Basic usage
Image(systemName: "cloud.sun.bolt.fill")
    .font(.largeTitle)
    .foregroundStyle(.blue)

// Multi-color (original)
Image(systemName: "thermometer.sun.fill")
    .renderingMode(.original)

// Palette mode
Image(systemName: "person.3.fill")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.red, .green, .blue)

// In Label
Label("Settings", systemImage: "gear")

// Accessibility
Image(systemName: "play.circle")
    .accessibilityLabel(String(localized: "button.play"))
```

## Launch Screen

### Option 1: Info.plist (Modern, No Storyboard)

```xml
<key>UILaunchScreen</key>
<dict>
    <key>UIImageName</key>
    <string>LaunchImage</string>
    <key>UIColorName</key>
    <string>LaunchBackgroundColor</string>
</dict>
```

### Option 2: SwiftUI Document Apps

```swift
DocumentGroupLaunchScene("App Name") {
    NewDocumentButton("Create")
} background: {
    Image(.launchBackground)
        .resizable()
        .scaledToFill()
        .ignoresSafeArea()
}
```

## Asset Catalog Colors

```swift
// Load from Assets.xcassets
let brandColor = Color("BrandPrimary")
let bgColor = UIColor(named: "BackgroundColor")
```

## Platform-Specific Sizes

| Platform | Master Size | Notes |
|----------|-------------|-------|
| iOS/iPadOS | 1024x1024 | Square, auto-rounded |
| macOS | 1024x1024 | .icns generated |
| watchOS | 1024x1024 | Circular mask |
| visionOS | 1024x1024 | 3 layers for parallax |

## Best Practices

- **No transparency** - Alpha must be 1.0
- **No manual corners** - System applies mask
- **Simple design** - Readable at 29x29
- **PNG format** - sRGB or Display P3
- **Test all sizes** - Use Simulator
