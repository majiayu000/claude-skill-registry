---
name: swiftgen-integration
description: "Expert SwiftGen decisions for iOS/tvOS: when type-safe assets add value, template selection trade-offs, organization strategies, and build phase configuration. Use when setting up SwiftGen, choosing templates, or debugging generation issues. Trigger keywords: SwiftGen, type-safe, Asset, L10n, ImageAsset, ColorAsset, FontFamily, swiftgen.yml, structured-swift5, code generation, asset catalog"
version: "3.0.0"
---

# SwiftGen Integration — Expert Decisions

Expert decision frameworks for SwiftGen choices. Claude knows asset catalogs and localization — this skill provides judgment calls for when SwiftGen adds value and configuration trade-offs.

---

## Decision Trees

### When SwiftGen Adds Value

```
Should you use SwiftGen for this project?
├─ > 20 assets/strings
│  └─ YES — Type safety prevents bugs
│     Typos caught at compile time
│
├─ < 10 assets/strings, solo developer
│  └─ MAYBE — Overhead vs. benefit
│     Quick projects may not need it
│
├─ Team project with shared assets
│  └─ YES — Consistency + discoverability
│     Autocomplete reveals available assets
│
├─ Assets change frequently
│  └─ YES — Broken references caught early
│     CI catches missing assets
│
└─ CI/CD pipeline exists
   └─ YES — Validate assets on every build
      Prevents runtime crashes
```

**The trap**: Using SwiftGen on tiny projects or for assets that rarely change. The setup overhead may exceed the benefit.

### Template Selection

```
Which template should you use?
├─ Strings
│  ├─ Hierarchical keys (auth.login.title)
│  │  └─ structured-swift5
│  │     L10n.Auth.Login.title
│  │
│  └─ Flat keys (login_title)
│     └─ flat-swift5
│        L10n.loginTitle
│
├─ Assets (Images)
│  └─ swift5 (default)
│     Asset.Icons.home.image
│
├─ Colors
│  └─ swift5 with enumName param
│     Asset.Colors.primary.color
│
├─ Fonts
│  └─ swift5
│     FontFamily.Roboto.bold.font(size:)
│
└─ Storyboards
   └─ scenes-swift5
      StoryboardScene.Main.initialViewController()
```

### Asset Organization Strategy

```
How should you organize assets?
├─ Small app (< 50 assets)
│  └─ Single Assets.xcassets
│     Feature folders inside catalog
│
├─ Medium app (50-200 assets)
│  └─ Feature-based catalogs
│     Auth.xcassets, Dashboard.xcassets
│     Multiple swiftgen inputs
│
├─ Large app / multi-module
│  └─ Per-module asset catalogs
│     Each module owns its assets
│     Module-specific SwiftGen runs
│
└─ Design system / shared assets
   └─ Separate DesignSystem.xcassets
      Shared across targets
```

### Build Phase Strategy

```
When should SwiftGen run?
├─ Every build
│  └─ Run Script phase (before Compile Sources)
│     Always current, small overhead
│
├─ Only when assets change
│  └─ Input/Output files specified
│     Xcode skips if unchanged
│
├─ Manual only (CI generates)
│  └─ Commit generated files
│     No local SwiftGen needed
│     Risk: generated files out of sync
│
└─ Pre-commit hook
   └─ Lint + generate before commit
      Ensures consistency
```

---

## NEVER Do

### Configuration

**NEVER** hardcode paths without variables:
```yaml
# ❌ Breaks in different environments
strings:
  inputs: /Users/john/Projects/MyApp/Resources/en.lproj/Localizable.strings
  outputs:
    output: /Users/john/Projects/MyApp/Generated/Strings.swift

# ✅ Use relative paths
strings:
  inputs: Resources/en.lproj/Localizable.strings
  outputs:
    output: Generated/Strings.swift
```

**NEVER** forget publicAccess for shared modules:
```yaml
# ❌ Generated code is internal — can't use from other modules
xcassets:
  inputs: Resources/Assets.xcassets
  outputs:
    - templateName: swift5
      output: Generated/Assets.swift
      # Missing publicAccess!

# ✅ Add publicAccess for shared code
xcassets:
  inputs: Resources/Assets.xcassets
  outputs:
    - templateName: swift5
      output: Generated/Assets.swift
      params:
        publicAccess: true  # Accessible from other modules
```

### Generated Code Usage

**NEVER** use string literals alongside SwiftGen:
```swift
// ❌ Defeats the purpose
let icon = UIImage(named: "home")  // String literal!
let title = NSLocalizedString("auth.login.title", comment: "")  // String literal!

// ✅ Use generated constants everywhere
let icon = Asset.Icons.home.image
let title = L10n.Auth.Login.title
```

**NEVER** modify generated files:
```swift
// ❌ Changes will be overwritten
// Generated/Assets.swift
enum Asset {
    enum Icons {
        static let home = ImageAsset(name: "home")

        // My custom addition  <- WILL BE DELETED ON NEXT RUN
        static let customIcon = ImageAsset(name: "custom")
    }
}

// ✅ Extend in separate file
// Extensions/Asset+Custom.swift
extension Asset.Icons {
    // Extensions survive regeneration
}
```

### Build Phase

**NEVER** put SwiftGen after Compile Sources:
```bash
# ❌ Generated files don't exist when compiling
Build Phases order:
1. Compile Sources  <- Fails: Assets.swift doesn't exist!
2. Run Script (SwiftGen)

# ✅ Generate before compiling
Build Phases order:
1. Run Script (SwiftGen)  <- Generates Assets.swift
2. Compile Sources         <- Now Assets.swift exists
```

**NEVER** skip SwiftGen availability check:
```bash
# ❌ Build fails if SwiftGen not installed
swiftgen config run  # Error: command not found

# ✅ Check availability, warn instead of fail
if which swiftgen >/dev/null; then
  swiftgen config run --config "$SRCROOT/swiftgen.yml"
else
  echo "warning: SwiftGen not installed, skipping code generation"
fi
```

### Version Control

**NEVER** commit generated files without good reason:
```bash
# ❌ Merge conflicts, stale files
git add Generated/Assets.swift
git add Generated/Strings.swift

# ✅ Gitignore generated files
# .gitignore
Generated/
*.generated.swift

# Exception: If CI doesn't run SwiftGen, commit generated files
# But then add pre-commit hook to keep them fresh
```

**NEVER** leave swiftgen.yml uncommitted:
```bash
# ❌ Team members can't regenerate
.gitignore
swiftgen.yml  <- WRONG!

# ✅ Commit configuration
git add swiftgen.yml
git add Resources/  # Source assets
```

### String Keys

**NEVER** use inconsistent key conventions:
```
# ❌ Mixed conventions — confusing
"LoginTitle" = "Log In";
"login.button" = "Sign In";
"AUTH_ERROR" = "Error";

# ✅ Consistent hierarchical keys
"auth.login.title" = "Log In";
"auth.login.button" = "Sign In";
"auth.error.generic" = "Error";
```

---

## Essential Patterns

### Complete swiftgen.yml

```yaml
# swiftgen.yml

## Strings (Localization)
strings:
  inputs:
    - Resources/en.lproj/Localizable.strings
  outputs:
    - templateName: structured-swift5
      output: Generated/Strings.swift
      params:
        publicAccess: true
        enumName: L10n

## Assets (Images)
xcassets:
  - inputs:
      - Resources/Assets.xcassets
    outputs:
      - templateName: swift5
        output: Generated/Assets.swift
        params:
          publicAccess: true

## Colors
colors:
  - inputs:
      - Resources/Colors.xcassets
    outputs:
      - templateName: swift5
        output: Generated/Colors.swift
        params:
          publicAccess: true
          enumName: ColorAsset

## Fonts
fonts:
  - inputs:
      - Resources/Fonts/
    outputs:
      - templateName: swift5
        output: Generated/Fonts.swift
        params:
          publicAccess: true
```

### SwiftUI Convenience Extensions

```swift
// Extensions/SwiftGen+SwiftUI.swift

import SwiftUI

// Image extension
extension Image {
    init(asset: ImageAsset) {
        self.init(asset.name, bundle: BundleToken.bundle)
    }
}

// Color extension
extension Color {
    init(asset: ColorAsset) {
        self.init(asset.name, bundle: BundleToken.bundle)
    }
}

// Font extension
extension Font {
    static func custom(_ fontConvertible: FontConvertible, size: CGFloat) -> Font {
        fontConvertible.swiftUIFont(size: size)
    }
}

// Usage
struct ContentView: View {
    var body: some View {
        VStack {
            Image(asset: Asset.Icons.home)
                .foregroundColor(Color(asset: Asset.Colors.primary))

            Text(L10n.Home.title)
                .font(.custom(FontFamily.Roboto.bold, size: 24))
        }
    }
}
```

### Build Phase Script

```bash
#!/bin/bash

# Xcode Build Phase: Run Script
# Move BEFORE "Compile Sources"

set -e

# Check if SwiftGen is installed
if ! which swiftgen >/dev/null; then
  echo "warning: SwiftGen not installed. Install via: brew install swiftgen"
  exit 0
fi

# Navigate to project root
cd "$SRCROOT"

# Create output directory if needed
mkdir -p Generated

# Run SwiftGen
echo "Running SwiftGen..."
swiftgen config run --config swiftgen.yml

echo "SwiftGen completed successfully"
```

**Input Files** (for incremental builds):
```
$(SRCROOT)/swiftgen.yml
$(SRCROOT)/Resources/Assets.xcassets
$(SRCROOT)/Resources/en.lproj/Localizable.strings
$(SRCROOT)/Resources/Colors.xcassets
$(SRCROOT)/Resources/Fonts
```

**Output Files**:
```
$(SRCROOT)/Generated/Assets.swift
$(SRCROOT)/Generated/Strings.swift
$(SRCROOT)/Generated/Colors.swift
$(SRCROOT)/Generated/Fonts.swift
```

### Multi-Module Setup

```yaml
# Module: DesignSystem/swiftgen.yml
xcassets:
  - inputs:
      - Sources/DesignSystem/Resources/Colors.xcassets
    outputs:
      - templateName: swift5
        output: Sources/DesignSystem/Generated/Colors.swift
        params:
          publicAccess: true  # Must be public for cross-module

# Module: Feature/swiftgen.yml
strings:
  - inputs:
      - Sources/Feature/Resources/en.lproj/Feature.strings
    outputs:
      - templateName: structured-swift5
        output: Sources/Feature/Generated/Strings.swift
        params:
          publicAccess: false  # Internal to module
          enumName: Strings
```

---

## Quick Reference

### Template Options

| Asset Type | Template | Output |
|------------|----------|--------|
| Images | swift5 | Asset.Category.name.image |
| Colors | swift5 | Asset.Colors.name.color |
| Strings | structured-swift5 | L10n.Category.Subcategory.key |
| Strings (flat) | flat-swift5 | L10n.keyName |
| Fonts | swift5 | FontFamily.Name.weight.font(size:) |
| Storyboards | scenes-swift5 | StoryboardScene.Name.viewController |

### Common Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| publicAccess | Public access level | true for shared modules |
| enumName | Custom enum name | L10n, Asset, Colors |
| allValues | Include allValues array | true for debugging |
| preservePath | Keep folder structure | true for fonts |

### File Structure

```
Project/
├── swiftgen.yml           # Configuration (commit)
├── Resources/
│   ├── Assets.xcassets    # Images (commit)
│   ├── Colors.xcassets    # Colors (commit)
│   ├── Fonts/             # Custom fonts (commit)
│   └── en.lproj/
│       └── Localizable.strings  # Strings (commit)
└── Generated/             # Output (gitignore)
    ├── Assets.swift
    ├── Colors.swift
    ├── Fonts.swift
    └── Strings.swift
```

### Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "No such module" | Generated before adding to target | Add to target membership |
| Build fails | Run Script after Compile | Move before Compile Sources |
| Stale generated code | Missing input/output files | Specify all inputs/outputs |
| Wrong bundle | Multi-target project | Use correct BundleToken |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| String literals for assets | Bypasses type safety | Use generated constants |
| Modified generated files | Changes get overwritten | Use extensions instead |
| Run Script after Compile | Files don't exist | Move before Compile Sources |
| No availability check | Build fails without SwiftGen | Add `which swiftgen` check |
| Committed generated files | Merge conflicts, staleness | Gitignore, generate on build |
| Missing publicAccess | Can't use across modules | Add publicAccess: true |
| Mixed key conventions | Inconsistent L10n structure | Use hierarchical keys |
