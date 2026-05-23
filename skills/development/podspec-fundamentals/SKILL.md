---
name: cocoapods-podspec-fundamentals
description: Use when creating or modifying CocoaPods podspec files. Covers required attributes, file patterns, dependencies, and platform specifications for iOS, macOS, tvOS, watchOS, and visionOS projects.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# CocoaPods - Podspec Fundamentals

Essential patterns for creating and maintaining podspec files that define CocoaPods libraries.

## Required Attributes

Every podspec must include these attributes:

```ruby
Pod::Spec.new do |spec|
  # Identity
  spec.name         = 'MyLibrary'
  spec.version      = '1.0.0'

  # Metadata
  spec.license      = { :type => 'MIT', :file => 'LICENSE' }
  spec.homepage     = 'https://github.com/username/MyLibrary'
  spec.authors      = { 'Your Name' => 'email@example.com' }
  spec.summary      = 'Brief description under 140 characters'

  # Source
  spec.source       = { :git => 'https://github.com/username/MyLibrary.git', :tag => spec.version.to_s }

  # Platform Support
  spec.ios.deployment_target = '13.0'
  spec.osx.deployment_target = '10.15'
end
```

## Platform Specifications

### Current Platform Support (2024)

```ruby
# iOS (iPhone, iPad)
spec.ios.deployment_target = '13.0'

# macOS (Mac computers)
spec.osx.deployment_target = '10.15'

# tvOS (Apple TV)
spec.tvos.deployment_target = '13.0'

# watchOS (Apple Watch)
spec.watchos.deployment_target = '6.0'

# visionOS (Apple Vision Pro) - Added in CocoaPods 1.15.0+
spec.visionos.deployment_target = '1.0'
```

### Multi-Platform Support

```ruby
# Simple approach - all platforms same version
spec.platform = :ios, '13.0'

# Recommended - specify per platform
spec.ios.deployment_target = '13.0'
spec.osx.deployment_target = '10.15'
spec.tvos.deployment_target = '13.0'
spec.watchos.deployment_target = '6.0'
```

## Source File Patterns

### Basic Source Files

```ruby
# All Swift and Objective-C files in Source directory
spec.source_files = 'Source/**/*.{swift,h,m}'

# Public headers only
spec.public_header_files = 'Source/**/*.h'

# Private/internal headers
spec.private_header_files = 'Source/**/*Private.h'

# Exclude specific files or directories
spec.exclude_files = 'Source/**/Internal/*', 'Source/**/Tests/*'
```

### Platform-Specific Source Files

```ruby
# iOS-only files
spec.ios.source_files = 'Source/iOS/**/*.swift'

# macOS-only files
spec.osx.source_files = 'Source/macOS/**/*.swift'

# Shared files across all platforms
spec.source_files = 'Source/Shared/**/*.swift'
```

## Resource Management

### Resource Bundles (Recommended)

```ruby
# Recommended - avoids name collisions
spec.resource_bundles = {
  'MyLibrary' => [
    'Resources/**/*.{png,jpg,xcassets,storyboard,xib}',
    'Resources/**/*.xcprivacy'  # Privacy manifests (iOS 17+)
  ]
}
```

### Direct Resources (Legacy)

```ruby
# Legacy approach - can cause name collisions
spec.resources = 'Assets/**/*'

# Platform-specific resources
spec.ios.resources = 'Assets/iOS/**/*'
spec.osx.resources = 'Assets/macOS/**/*'
```

## Dependencies

### CocoaPods Dependencies

```ruby
# Any version
spec.dependency 'Alamofire'

# Specific version
spec.dependency 'SwiftyJSON', '5.0.0'

# Version range (optimistic operator - recommended)
spec.dependency 'RxSwift', '~> 6.0'  # >= 6.0, < 7.0

# Minimum version
spec.dependency 'SnapKit', '>= 5.0'

# Platform-specific dependency
spec.ios.dependency 'UIKit'
spec.osx.dependency 'AppKit'
```

### System Frameworks and Libraries

```ruby
# System frameworks
spec.frameworks = 'UIKit', 'Foundation', 'CoreGraphics'

# Platform-specific frameworks
spec.ios.frameworks = 'UIKit', 'CoreLocation'
spec.osx.frameworks = 'AppKit', 'CoreData'

# System libraries
spec.libraries = 'z', 'sqlite3'

# Weak frameworks (optional at runtime)
spec.weak_frameworks = 'UserNotifications'
```

## Vendored Frameworks

### XCFramework Support (Modern)

```ruby
# Single XCFramework
spec.vendored_frameworks = 'MyFramework.xcframework'

# Multiple frameworks
spec.vendored_frameworks = 'Frameworks/*.xcframework', 'Frameworks/*.framework'

# Platform-specific
spec.ios.vendored_frameworks = 'Frameworks/iOS/*.xcframework'
spec.osx.vendored_frameworks = 'Frameworks/macOS/*.framework'
```

### Static Libraries

```ruby
# Vendored static libraries
spec.vendored_libraries = 'Libraries/*.a'

# With public headers
spec.vendored_libraries = 'Libraries/libMyLib.a'
spec.public_header_files = 'Headers/**/*.h'
```

## Compiler and Linker Flags

```ruby
# Compiler flags
spec.compiler_flags = '-Wno-deprecated-declarations'

# Linker flags
spec.xcconfig = {
  'OTHER_LDFLAGS' => '-ObjC',
  'ENABLE_BITCODE' => 'NO'
}

# ARC support (per file pattern)
spec.requires_arc = true
spec.requires_arc = 'Source/**/*.m'  # Only specific files

# Files that don't use ARC
spec.requires_arc = false
```

## Swift Support

### Swift Version

```ruby
# Swift version (required for Swift libraries)
spec.swift_versions = ['5.5', '5.6', '5.7', '5.8', '5.9']

# Or specify single version
spec.swift_version = '5.9'
```

### Module Map

```ruby
# Custom module map
spec.module_map = 'Source/module.modulemap'

# Module name (if different from pod name)
spec.module_name = 'MyCustomModule'
```

## Version Management

### Semantic Versioning

```ruby
# MAJOR.MINOR.PATCH
spec.version = '1.2.3'

# Pre-release versions
spec.version = '2.0.0-beta.1'
spec.version = '1.0.0-rc.1'

# Use tag from git source
spec.source = { :git => 'https://github.com/username/MyLibrary.git', :tag => spec.version.to_s }
```

## Best Practices

### File Organization

```
MyLibrary/
├── MyLibrary.podspec
├── LICENSE
├── README.md
├── Source/
│   ├── Core/
│   ├── Extensions/
│   └── Utilities/
├── Resources/
│   ├── Assets.xcassets
│   └── PrivacyInfo.xcprivacy
└── Tests/
    └── MyLibraryTests/
```

### Common Patterns

```ruby
Pod::Spec.new do |spec|
  spec.name         = 'MyLibrary'
  spec.version      = '1.0.0'
  spec.summary      = 'A brief description'
  spec.description  = 'A longer description that provides more detail'

  spec.homepage     = 'https://github.com/username/MyLibrary'
  spec.license      = { :type => 'MIT', :file => 'LICENSE' }
  spec.authors      = { 'Your Name' => 'email@example.com' }
  spec.source       = { :git => 'https://github.com/username/MyLibrary.git', :tag => spec.version.to_s }

  # Platform support
  spec.ios.deployment_target = '13.0'
  spec.osx.deployment_target = '10.15'

  # Swift version
  spec.swift_versions = ['5.7', '5.8', '5.9']

  # Source files
  spec.source_files = 'Source/**/*.{swift,h,m}'

  # Resources
  spec.resource_bundles = {
    'MyLibrary' => ['Resources/**/*']
  }

  # Dependencies
  spec.dependency 'Alamofire', '~> 5.0'

  # Frameworks
  spec.frameworks = 'Foundation'
  spec.ios.frameworks = 'UIKit'
  spec.osx.frameworks = 'AppKit'
end
```

## Anti-Patterns

### Don't

❌ Use direct resources (causes name collisions)

```ruby
spec.resources = 'Assets/**/*'  # BAD
```

❌ Omit platform deployment targets

```ruby
# Missing deployment target - will use CocoaPods default
```

❌ Include test files in main source

```ruby
spec.source_files = '**/*.swift'  # Includes test files!
```

❌ Use absolute paths

```ruby
spec.source_files = '/Users/username/MyLibrary/Source/**/*'  # BAD
```

### Do

✅ Use resource bundles

```ruby
spec.resource_bundles = { 'MyLibrary' => ['Resources/**/*'] }
```

✅ Specify platform targets explicitly

```ruby
spec.ios.deployment_target = '13.0'
```

✅ Exclude test files

```ruby
spec.source_files = 'Source/**/*.swift'
spec.exclude_files = 'Tests/**/*'
```

✅ Use relative paths from repo root

```ruby
spec.source_files = 'Source/**/*.swift'
```

## Validation

### Local Validation

```bash
# Quick validation (skips build)
pod lib lint --quick

# Full validation with build
pod lib lint

# Allow warnings
pod lib lint --allow-warnings

# Skip tests
pod lib lint --skip-tests
```

### Publishing Validation

```bash
# Validate for publishing
pod spec lint

# With specific Swift version
pod spec lint --swift-version=5.9
```

## Related Skills

- cocoapods-subspecs-organization
- cocoapods-test-specs
- cocoapods-privacy-manifests
- cocoapods-publishing-workflow
