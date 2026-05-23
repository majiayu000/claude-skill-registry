---
name: localization-ios
description: "Expert localization decisions for iOS/tvOS: when runtime language switching is needed vs system handling, pluralization rule complexity by language, RTL layout strategies, and string key architecture. Use when internationalizing apps, handling RTL languages, or debugging localization issues. Trigger keywords: localization, i18n, l10n, NSLocalizedString, Localizable.strings, stringsdict, plurals, RTL, Arabic, Hebrew, SwiftGen, language switching"
version: "3.0.0"
---

# Localization iOS — Expert Decisions

Expert decision frameworks for localization choices. Claude knows NSLocalizedString and .strings files — this skill provides judgment calls for architecture decisions and cross-language complexity.

---

## Decision Trees

### Runtime Language Switching

```
Do users need in-app language control?
├─ NO (respect system language)
│  └─ Standard localization
│     NSLocalizedString, let iOS handle it
│     Simplest and recommended
│
├─ YES (business requirement)
│  └─ Does app restart work?
│     ├─ YES → UserDefaults + AppleLanguages
│     │  Simpler, more reliable
│     └─ NO → Full runtime switching
│        Complex: Bundle swizzling or custom lookup
│
└─ Single language override only (e.g., always English)
   └─ Don't localize
      Bundle.main with no .lproj
```

**The trap**: Implementing runtime language switching when system language suffices. It adds complexity and can break third-party SDKs that read system locale.

### String Key Architecture

```
How to structure your keys?
├─ Small app (< 100 strings)
│  └─ Flat keys with prefixes
│     "login_title", "login_email_placeholder"
│
├─ Medium app
│  └─ Hierarchical dot notation
│     "auth.login.title", "auth.login.email"
│
├─ Large app with teams
│  └─ Feature-based files
│     Auth.strings, Profile.strings, etc.
│     Each team owns their strings file
│
└─ Design system / component library
   └─ Component-scoped keys
      "button.primary.title", "input.error.required"
```

### Pluralization Complexity

```
Which languages do you support?
├─ Western languages only (en, es, fr, de)
│  └─ Simple plural rules
│     one, other (maybe zero)
│
├─ Slavic languages (ru, pl, uk)
│  └─ Complex plural rules
│     one, few, many, other
│     e.g., Russian: 1 файл, 2 файла, 5 файлов
│
├─ Arabic
│  └─ Six plural forms!
│     zero, one, two, few, many, other
│     MUST use stringsdict
│
└─ East Asian (zh, ja, ko)
   └─ No grammatical plural
      But may need counters/classifiers
```

### RTL Support Level

```
Do you support RTL languages?
├─ NO RTL languages planned
│  └─ Still use leading/trailing
│     Future-proof your layout
│
├─ Arabic only
│  └─ Standard RTL support
│     layoutDirection + leading/trailing
│     Test thoroughly
│
├─ Arabic + Hebrew + Persian
│  └─ Each has unique considerations
│     Hebrew: different number handling
│     Persian: different numerals (۱۲۳)
│
└─ Mixed LTR/RTL content
   └─ Explicit direction per component
      Force LTR for code, URLs, numbers
```

---

## NEVER Do

### String Management

**NEVER** concatenate localized strings:
```swift
// ❌ Breaks in languages with different word order
let message = NSLocalizedString("hello", comment: "") + " " + userName

// German: "Hallo" + " " + "Hans" = "Hallo Hans" ✓
// Japanese: "こんにちは" + " " + "田中" = "こんにちは 田中" ✗
// Should be "田中さん、こんにちは"

// ✅ Use format strings
let format = NSLocalizedString("greeting.format", comment: "")
let message = String(format: format, userName)
// greeting.format = "Hello, %@!" (en)
// greeting.format = "%@さん、こんにちは!" (ja)
```

**NEVER** embed numbers in translation keys:
```swift
// ❌ Doesn't handle plural rules
"items.1" = "1 item"
"items.2" = "2 items"
"items.3" = "3 items"
// What about 0? 100? Arabic's 6 forms?

// ✅ Use stringsdict for plurals
String.localizedStringWithFormat(
    NSLocalizedString("items.count", comment: ""),
    count
)
```

**NEVER** assume string length:
```swift
// ❌ German is ~30% longer than English
.frame(width: 100)  // "Settings" fits, "Einstellungen" doesn't

// ✅ Use flexible layouts
.frame(minWidth: 80)
// Or
.fixedSize(horizontal: true, vertical: false)
```

**NEVER** use left/right in layouts:
```swift
// ❌ Breaks in RTL
.padding(.left, 16)
.frame(alignment: .left)

// ✅ Use leading/trailing
.padding(.leading, 16)
.frame(alignment: .leading)
```

### Runtime Language

**NEVER** change AppleLanguages without restart:
```swift
// ❌ Partial UI update — inconsistent state
UserDefaults.standard.set(["ar"], forKey: "AppleLanguages")
// Some views updated, others not. Third-party SDKs broken.

// ✅ Require restart or use custom bundle
UserDefaults.standard.set(["ar"], forKey: "AppleLanguages")
showRestartRequiredAlert()  // User restarts app
```

**NEVER** forget to set locale for formatters:
```swift
// ❌ Uses device locale, not app's selected language
let formatter = DateFormatter()
formatter.dateStyle = .medium
let date = formatter.string(from: Date())  // Wrong language!

// ✅ Set locale explicitly
let formatter = DateFormatter()
formatter.locale = Locale(identifier: selectedLanguage.rawValue)
formatter.dateStyle = .medium
```

### Pluralization

**NEVER** use simple if/else for plurals:
```swift
// ❌ Fails for Russian, Arabic, etc.
func itemsText(_ count: Int) -> String {
    if count == 1 {
        return "1 item"
    } else {
        return "\(count) items"
    }
}

// Russian: 1 товар, 2 товара, 5 товаров, 21 товар, 22 товара...
// This requires CLDR plural rules

// ✅ Use stringsdict — iOS handles rules automatically
```

**NEVER** hardcode numeral systems:
```swift
// ❌ Arabic users may expect Arabic-Indic numerals
Text("\(count) items")  // Shows "5 items" even in Arabic

// ✅ Use NumberFormatter with locale
let formatter = NumberFormatter()
formatter.locale = Locale(identifier: "ar")
formatter.string(from: count as NSNumber)  // "٥"
```

### RTL Layouts

**NEVER** use fixed directional icons:
```swift
// ❌ Arrow points wrong way in RTL
Image(systemName: "arrow.right")

// ✅ Use semantic icons or flip
Image(systemName: "arrow.forward")  // Semantic
// Or
Image(systemName: "arrow.right")
    .flipsForRightToLeftLayoutDirection(true)
```

**NEVER** force layout direction globally when it should be per-component:
```swift
// ❌ Phone numbers, code, etc. should stay LTR
.environment(\.layoutDirection, .rightToLeft)

// ✅ Apply selectively
VStack {
    Text(localizedContent)  // Follows RTL

    Text(phoneNumber)
        .environment(\.layoutDirection, .leftToRight)  // Always LTR

    Text(codeSnippet)
        .environment(\.layoutDirection, .leftToRight)
}
```

---

## Essential Patterns

### Type-Safe Localization with SwiftGen

```swift
// swiftgen.yml
// strings:
//   inputs: Resources/en.lproj/Localizable.strings
//   outputs:
//     - templateName: structured-swift5
//       output: Generated/Strings.swift

// Usage — compile-time safe
Text(L10n.Auth.Login.title)
Text(L10n.User.greeting(userName))
Text(L10n.Items.count(itemCount))

// Benefits:
// - Compiler catches missing keys
// - Auto-complete for strings
// - Refactoring safe
```

### Stringsdict for Plurals

```xml
<!-- en.lproj/Localizable.stringsdict -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" ...>
<plist version="1.0">
<dict>
    <key>items.count</key>
    <dict>
        <key>NSStringLocalizedFormatKey</key>
        <string>%#@items@</string>
        <key>items</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>zero</key>
            <string>No items</string>
            <key>one</key>
            <string>%d item</string>
            <key>other</key>
            <string>%d items</string>
        </dict>
    </dict>
</dict>
</plist>
```

```swift
// Usage
let text = String.localizedStringWithFormat(
    NSLocalizedString("items.count", comment: ""),
    count
)
// 0 → "No items"
// 1 → "1 item"
// 5 → "5 items"
```

### RTL-Aware Layout Helpers

```swift
extension View {
    /// Applies leading alignment that respects RTL
    func alignLeading() -> some View {
        self.frame(maxWidth: .infinity, alignment: .leading)
    }

    /// Force LTR for content that shouldn't flip (code, URLs, phone numbers)
    func forceLTR() -> some View {
        self.environment(\.layoutDirection, .leftToRight)
    }
}

// ContentView
struct MessageCell: View {
    let message: Message

    var body: some View {
        VStack(alignment: .leading) {
            Text(message.content)
                .alignLeading()  // Respects RTL

            Text(message.codeSnippet)
                .font(.monospaced(.body)())
                .forceLTR()  // Code always LTR

            Text(message.url)
                .forceLTR()  // URLs always LTR
        }
    }
}
```

### Locale-Aware Formatting

```swift
struct LocalizedFormatters {
    let locale: Locale

    init(languageCode: String) {
        self.locale = Locale(identifier: languageCode)
    }

    func formatDate(_ date: Date, style: DateFormatter.Style = .medium) -> String {
        let formatter = DateFormatter()
        formatter.locale = locale
        formatter.dateStyle = style
        return formatter.string(from: date)
    }

    func formatNumber(_ number: Double) -> String {
        let formatter = NumberFormatter()
        formatter.locale = locale
        formatter.numberStyle = .decimal
        return formatter.string(from: NSNumber(value: number)) ?? "\(number)"
    }

    func formatCurrency(_ amount: Double, code: String) -> String {
        let formatter = NumberFormatter()
        formatter.locale = locale
        formatter.numberStyle = .currency
        formatter.currencyCode = code
        return formatter.string(from: NSNumber(value: amount)) ?? "\(amount)"
    }
}
```

---

## Quick Reference

### Plural Forms by Language

| Language | Forms | Example (1, 2, 5) |
|----------|-------|-------------------|
| English | one, other | 1 item, 2 items, 5 items |
| French | one, other | 1 élément, 2 éléments |
| Russian | one, few, many, other | 1 файл, 2 файла, 5 файлов |
| Arabic | zero, one, two, few, many, other | 6 forms! |
| Japanese | other only | No grammatical plural |

### RTL Languages

| Language | Script Direction | Numerals |
|----------|-----------------|----------|
| Arabic | RTL | Arabic-Indic (٠١٢) or Western |
| Hebrew | RTL | Western |
| Persian | RTL | Extended Arabic (۰۱۲) |
| Urdu | RTL | Extended Arabic |

### String Expansion Guidelines

| Source (English) | Expansion |
|------------------|-----------|
| 1-10 chars | +200-300% |
| 11-20 chars | +80-100% |
| 21-50 chars | +60-80% |
| 51-70 chars | +50-60% |
| 70+ chars | +30% |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| String concatenation | Word order varies | Format strings |
| if count == 1 else | Wrong plural rules | stringsdict |
| .padding(.left) | Breaks RTL | .padding(.leading) |
| DateFormatter without locale | Wrong language | Set locale explicitly |
| Runtime language without restart | Inconsistent UI | Require restart |
| Fixed frame widths for text | Text truncation | Flexible layouts |
| Hardcoded "1, 2, 3" | Wrong numeral system | NumberFormatter with locale |
