---
name: cocoapods-subspecs-organization
description: Use when organizing complex CocoaPods libraries into subspecs. Covers modular architecture, dependency management between subspecs, and default subspecs patterns for better code organization and optional features.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# CocoaPods - Subspecs Organization

Organize complex libraries into modular subspecs for better maintainability and optional features.

## What Are Subspecs?

Subspecs allow you to split a pod into logical modules that can be installed independently or as a group.

### Benefits

- **Modularity**: Separate core functionality from optional features
- **Selective Installation**: Users install only what they need
- **Reduced Dependencies**: Optional features don't force unnecessary dependencies
- **Better Organization**: Clear separation of concerns

## Basic Subspec Pattern

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MyLibrary'
  spec.version = '1.0.0'

  # Main spec has no source files - all in subspecs
  spec.default_subspecs = 'Core'

  # Core subspec - installed by default
  spec.subspec 'Core' do |core|
    core.source_files = 'Source/Core/**/*.swift'
    core.frameworks = 'Foundation'
  end

  # Optional feature subspec
  spec.subspec 'Networking' do |networking|
    networking.source_files = 'Source/Networking/**/*.swift'
    networking.dependency 'MyLibrary/Core'  # Depends on Core
    networking.dependency 'Alamofire', '~> 5.0'
  end

  # Another optional feature
  spec.subspec 'UI' do |ui|
    ui.source_files = 'Source/UI/**/*.swift'
    ui.dependency 'MyLibrary/Core'
    ui.ios.frameworks = 'UIKit'
    ui.osx.frameworks = 'AppKit'
  end
end
```

## Dependency Patterns

### Subspec Dependencies

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MySDK'

  # Foundation layer
  spec.subspec 'Core' do |core|
    core.source_files = 'Source/Core/**/*.swift'
  end

  # Networking depends on Core
  spec.subspec 'Networking' do |net|
    net.source_files = 'Source/Networking/**/*.swift'
    net.dependency 'MySDK/Core'
    net.dependency 'Alamofire', '~> 5.0'
  end

  # Analytics depends on Core and Networking
  spec.subspec 'Analytics' do |analytics|
    analytics.source_files = 'Source/Analytics/**/*.swift'
    analytics.dependency 'MySDK/Core'
    analytics.dependency 'MySDK/Networking'
  end
end
```

### External Dependencies Per Subspec

```ruby
spec.subspec 'SQLite' do |sqlite|
  sqlite.source_files = 'Source/SQLite/**/*.swift'
  sqlite.dependency 'MyLibrary/Core'
  sqlite.dependency 'SQLite.swift', '~> 0.14'
  sqlite.libraries = 'sqlite3'
end

spec.subspec 'Realm' do |realm|
  realm.source_files = 'Source/Realm/**/*.swift'
  realm.dependency 'MyLibrary/Core'
  realm.dependency 'RealmSwift', '~> 10.0'
end
```

## Default Subspecs

### Single Default Subspec

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MyLibrary'

  # When users do: pod 'MyLibrary'
  # Only Core is installed
  spec.default_subspecs = 'Core'

  spec.subspec 'Core' do |core|
    core.source_files = 'Source/Core/**/*.swift'
  end

  spec.subspec 'Extensions' do |ext|
    ext.source_files = 'Source/Extensions/**/*.swift'
    ext.dependency 'MyLibrary/Core'
  end
end
```

### Multiple Default Subspecs

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MySDK'

  # When users do: pod 'MySDK'
  # Both Core and Networking are installed
  spec.default_subspecs = 'Core', 'Networking'

  spec.subspec 'Core' do |core|
    core.source_files = 'Source/Core/**/*.swift'
  end

  spec.subspec 'Networking' do |net|
    net.source_files = 'Source/Networking/**/*.swift'
    net.dependency 'MySDK/Core'
  end

  spec.subspec 'Analytics' do |analytics|
    analytics.source_files = 'Source/Analytics/**/*.swift'
    analytics.dependency 'MySDK/Core'
    # Optional - not installed by default
  end
end
```

## Platform-Specific Subspecs

```ruby
Pod::Spec.new do |spec|
  spec.name = 'CrossPlatformLib'

  # Shared core
  spec.subspec 'Core' do |core|
    core.source_files = 'Source/Core/**/*.swift'
    core.frameworks = 'Foundation'
  end

  # iOS-only subspec
  spec.subspec 'iOS' do |ios|
    ios.source_files = 'Source/iOS/**/*.swift'
    ios.dependency 'CrossPlatformLib/Core'
    ios.ios.deployment_target = '13.0'
    ios.ios.frameworks = 'UIKit'
  end

  # macOS-only subspec
  spec.subspec 'macOS' do |macos|
    macos.source_files = 'Source/macOS/**/*.swift'
    macos.dependency 'CrossPlatformLib/Core'
    macos.osx.deployment_target = '10.15'
    macos.osx.frameworks = 'AppKit'
  end
end
```

## Resource Bundles in Subspecs

```ruby
spec.subspec 'UI' do |ui|
  ui.source_files = 'Source/UI/**/*.swift'

  # Each subspec can have its own resource bundle
  ui.resource_bundles = {
    'MyLibrary_UI' => [
      'Resources/UI/**/*.{png,jpg,xcassets}',
      'Resources/UI/**/*.{storyboard,xib}'
    ]
  }

  ui.dependency 'MyLibrary/Core'
end

spec.subspec 'Themes' do |themes|
  themes.source_files = 'Source/Themes/**/*.swift'

  themes.resource_bundles = {
    'MyLibrary_Themes' => ['Resources/Themes/**/*']
  }

  themes.dependency 'MyLibrary/UI'
end
```

## Common Subspec Patterns

### Core + Optional Features

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MyFramework'
  spec.default_subspecs = 'Core'

  # Required core functionality
  spec.subspec 'Core' do |core|
    core.source_files = 'Source/Core/**/*.swift'
  end

  # Optional: JSON serialization
  spec.subspec 'JSON' do |json|
    json.source_files = 'Source/JSON/**/*.swift'
    json.dependency 'MyFramework/Core'
    json.dependency 'SwiftyJSON', '~> 5.0'
  end

  # Optional: XML support
  spec.subspec 'XML' do |xml|
    xml.source_files = 'Source/XML/**/*.swift'
    xml.dependency 'MyFramework/Core'
  end

  # Optional: Networking
  spec.subspec 'Networking' do |net|
    net.source_files = 'Source/Networking/**/*.swift'
    net.dependency 'MyFramework/Core'
    net.dependency 'Alamofire', '~> 5.0'
  end
end
```

### Layered Architecture

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MySDK'

  # Layer 1: Foundation
  spec.subspec 'Foundation' do |foundation|
    foundation.source_files = 'Source/Foundation/**/*.swift'
  end

  # Layer 2: Data (depends on Foundation)
  spec.subspec 'Data' do |data|
    data.source_files = 'Source/Data/**/*.swift'
    data.dependency 'MySDK/Foundation'
  end

  # Layer 3: Domain (depends on Data)
  spec.subspec 'Domain' do |domain|
    domain.source_files = 'Source/Domain/**/*.swift'
    domain.dependency 'MySDK/Data'
  end

  # Layer 4: Presentation (depends on Domain)
  spec.subspec 'Presentation' do |presentation|
    presentation.source_files = 'Source/Presentation/**/*.swift'
    presentation.dependency 'MySDK/Domain'
    presentation.ios.frameworks = 'UIKit'
  end
end
```

### Protocol + Implementations

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MyStorage'

  # Protocol definitions
  spec.subspec 'Core' do |core|
    core.source_files = 'Source/Core/**/*.swift'
  end

  # UserDefaults implementation
  spec.subspec 'UserDefaults' do |ud|
    ud.source_files = 'Source/UserDefaults/**/*.swift'
    ud.dependency 'MyStorage/Core'
  end

  # Keychain implementation
  spec.subspec 'Keychain' do |keychain|
    keychain.source_files = 'Source/Keychain/**/*.swift'
    keychain.dependency 'MyStorage/Core'
    keychain.dependency 'KeychainAccess', '~> 4.0'
  end

  # SQLite implementation
  spec.subspec 'SQLite' do |sqlite|
    sqlite.source_files = 'Source/SQLite/**/*.swift'
    sqlite.dependency 'MyStorage/Core'
    sqlite.libraries = 'sqlite3'
  end
end
```

## User Installation Patterns

### Installing Default Subspecs

```ruby
# Installs default subspecs only
pod 'MyLibrary'
```

### Installing Specific Subspecs

```ruby
# Install only Core
pod 'MyLibrary/Core'

# Install Core and Networking
pod 'MyLibrary/Core'
pod 'MyLibrary/Networking'

# Or more concisely
pod 'MyLibrary', :subspecs => ['Core', 'Networking']
```

### Installing All Subspecs

```ruby
# Install everything (not recommended - bloats dependency tree)
# No built-in way - user must list each subspec
```

## Nested Subspecs

```ruby
spec.subspec 'Networking' do |net|
  # Nested subspec: Networking/REST
  net.subspec 'REST' do |rest|
    rest.source_files = 'Source/Networking/REST/**/*.swift'
    rest.dependency 'MyLibrary/Core'
  end

  # Nested subspec: Networking/GraphQL
  net.subspec 'GraphQL' do |graphql|
    graphql.source_files = 'Source/Networking/GraphQL/**/*.swift'
    graphql.dependency 'MyLibrary/Core'
    graphql.dependency 'Apollo', '~> 1.0'
  end
end

# Users install with:
# pod 'MyLibrary/Networking/REST'
# pod 'MyLibrary/Networking/GraphQL'
```

## Best Practices

### Directory Structure

```
MyLibrary/
├── MyLibrary.podspec
├── Source/
│   ├── Core/           # Core subspec
│   ├── Networking/     # Networking subspec
│   ├── UI/            # UI subspec
│   └── Analytics/     # Analytics subspec
├── Resources/
│   ├── Core/
│   ├── UI/
│   └── Analytics/
└── Tests/
    ├── CoreTests/
    ├── NetworkingTests/
    └── UITests/
```

### Naming Conventions

```ruby
# Use clear, descriptive names
spec.subspec 'Networking'  # Good
spec.subspec 'Net'        # Too abbreviated

# Group related functionality
spec.subspec 'UI'
spec.subspec 'UIComponents'
spec.subspec 'UIExtensions'

# Platform suffixes when needed
spec.subspec 'iOS'
spec.subspec 'macOS'
```

### Dependency Guidelines

```ruby
# Keep dependency chains shallow
spec.subspec 'A' do |a|
  a.dependency 'MyLib/Core'  # 1 level - Good
end

spec.subspec 'B' do |b|
  b.dependency 'MyLib/A'  # 2 levels - OK
end

spec.subspec 'C' do |c|
  c.dependency 'MyLib/B'  # 3 levels - Consider flattening
end
```

## Anti-Patterns

### Don't

❌ Create too many small subspecs

```ruby
# Over-granular
spec.subspec 'StringExtensions'
spec.subspec 'ArrayExtensions'
spec.subspec 'DictionaryExtensions'
# Better: Group as 'Extensions'
```

❌ Circular dependencies

```ruby
spec.subspec 'A' do |a|
  a.dependency 'MyLib/B'
end

spec.subspec 'B' do |b|
  b.dependency 'MyLib/A'  # CIRCULAR - Will fail
end
```

❌ Duplicate source files

```ruby
spec.subspec 'Core' do |core|
  core.source_files = 'Source/**/*.swift'  # Includes everything
end

spec.subspec 'Utils' do |utils|
  utils.source_files = 'Source/Utils/**/*.swift'  # DUPLICATE
end
```

### Do

✅ Group related functionality

```ruby
spec.subspec 'Extensions' do |ext|
  ext.source_files = 'Source/Extensions/**/*.swift'
end
```

✅ Use clear dependency hierarchy

```ruby
spec.subspec 'A' do |a|
  a.dependency 'MyLib/Core'
end

spec.subspec 'B' do |b|
  b.dependency 'MyLib/Core'  # Both depend on Core - Good
end
```

✅ Keep source files separate

```ruby
spec.subspec 'Core' do |core|
  core.source_files = 'Source/Core/**/*.swift'
end

spec.subspec 'Utils' do |utils|
  utils.source_files = 'Source/Utils/**/*.swift'
end
```

## Testing Subspecs

```bash
# Lint specific subspec
pod lib lint --include-podspecs=*.podspec

# Test specific subspec in example project
cd Example
pod install
# Then build/run in Xcode
```

## Related Skills

- cocoapods-podspec-fundamentals
- cocoapods-test-specs
- cocoapods-publishing-workflow
