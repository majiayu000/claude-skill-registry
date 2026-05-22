---
name: swift-i18n
description: Automatic internationalization for Swift/SwiftUI apps. Use when writing ANY user-facing text - always localize with String Catalogs, LocalizedStringResource, and proper pluralization patterns.
user-invocable: false
---

# Swift Internationalization (i18n)

## MANDATORY: All User-Facing Text Must Be Localized

Every string displayed to users MUST use localization APIs. Never hardcode strings.

## Modern APIs (Swift 5.7+)

### String(localized:) - Swift Code

```swift
// Basic usage with comment for translators
let title = String(
    localized: "home.welcome.title",
    defaultValue: "Welcome",
    comment: "Main screen welcome title"
)

// In Swift Packages - ALWAYS specify bundle
let text = String(localized: "feature.title", bundle: .module)
```

### LocalizedStringResource - Type-Safe (Swift 5.9+)

```swift
extension LocalizedStringResource {
    enum App {
        enum Home {
            static let title = LocalizedStringResource(
                "app.home.title",
                defaultValue: "Home",
                comment: "Navigation title for home screen"
            )
            static func itemCount(_ count: Int) -> LocalizedStringResource {
                LocalizedStringResource(
                    "app.home.itemCount",
                    defaultValue: "\(count) items",
                    comment: "Item count with pluralization"
                )
            }
        }
    }
}

// Usage
Text(LocalizedStringResource.App.Home.title)
```

### SwiftUI Text - Automatic Localization

```swift
// Literal strings ARE localized automatically
Text("home.title")
Button("button.save") { }

// String variables are NOT localized - wrap them!
let key = "home.title"
Text(LocalizedStringKey(key)) // Required for variables
```

## Pluralization

```swift
// Number in text triggers plural rules
Text("You have \(count) items")
// xcstrings: "You have %lld items" with plural variations
```

## Date/Number Formatting

```swift
Text(date, style: .date)
Text(price, format: .currency(code: "EUR"))
Text(count, format: .number)
```

## Key Naming Convention

```
module.screen.element.property
```

Examples:
- `app.home.title`
- `auth.login.button.submit`
- `profile.settings.toggle.notifications`

## Anti-Patterns

```swift
// NEVER DO THIS
Text("Welcome")              // Hardcoded
let msg = "Hello \(name)"    // String interpolation outside Text
Text(msg)                    // Variable not localized

// ALWAYS DO THIS
Text("welcome.message")
Text("greeting.hello \(name)")
Text(LocalizedStringKey(dynamicKey))
```

## Preview Multi-Locale Testing

```swift
#Preview("English") {
    ContentView()
        .environment(\.locale, Locale(identifier: "en"))
}

#Preview("French") {
    ContentView()
        .environment(\.locale, Locale(identifier: "fr"))
}
```
