---
name: text-rich-content
description: SwiftUI Text rendering, AttributedString, native Markdown support, and rich text editing. Use when user asks about Text, Markdown, AttributedString, rich text, TextEditor, text formatting, or localization.
allowed-tools: Bash, Read, Write, Edit
---

# SwiftUI Text and Rich Content

Comprehensive guide to SwiftUI text rendering, AttributedString, native Markdown support, and rich text editing for iOS 26 development.

## Prerequisites

- iOS 15+ for AttributedString (iOS 26 recommended for rich text editing)
- Xcode 26+

---

## Basic Text

### Text View Fundamentals

```swift
// Simple text
Text("Hello, World!")

// Multi-line text (automatic)
Text("This is a longer piece of text that will automatically wrap to multiple lines when it exceeds the available width.")

// Verbatim (no localization)
Text(verbatim: "user_name")  // Won't look up in Localizable.strings
```

### Font Modifiers

```swift
Text("Hello")
    .font(.largeTitle)
    .font(.title)
    .font(.title2)
    .font(.title3)
    .font(.headline)
    .font(.subheadline)
    .font(.body)
    .font(.callout)
    .font(.caption)
    .font(.caption2)
    .font(.footnote)

// Custom font
Text("Custom")
    .font(.custom("Helvetica Neue", size: 24))
    .font(.system(size: 20, weight: .bold, design: .rounded))

// Dynamic type with relative size
Text("Scaled")
    .font(.body.leading(.loose))
```

### Text Styling

```swift
Text("Styled Text")
    .fontWeight(.bold)
    .italic()
    .underline()
    .underline(color: .blue)
    .strikethrough()
    .strikethrough(color: .red)
    .kerning(2)          // Letter spacing
    .tracking(2)         // Similar to kerning
    .baselineOffset(10)  // Vertical offset
    .textCase(.uppercase)
    .textCase(.lowercase)
```

### Text Truncation and Lines

```swift
Text("Long text that might need truncation...")
    .lineLimit(2)
    .lineLimit(1...3)    // Range (iOS 16+)
    .truncationMode(.tail)    // .head, .middle, .tail
    .allowsTightening(true)   // Reduce spacing before truncating
    .minimumScaleFactor(0.5)  // Scale down to fit
```

### Text Alignment

```swift
Text("Aligned text")
    .multilineTextAlignment(.leading)
    .multilineTextAlignment(.center)
    .multilineTextAlignment(.trailing)

// Frame alignment for single line
Text("Single")
    .frame(maxWidth: .infinity, alignment: .leading)
```

---

## Native Markdown Support

### Automatic Markdown Rendering

SwiftUI Text views automatically render Markdown:

```swift
// Basic Markdown in Text
Text("**Bold**, *italic*, and ~~strikethrough~~")
Text("Visit [Apple](https://apple.com)")
Text("`inline code` looks different")

// Combined formatting
Text("This is **bold and *italic* together**")
```

### Supported Markdown Syntax

```swift
// Emphasis
Text("*italic* or _italic_")
Text("**bold** or __bold__")
Text("***bold italic***")

// Strikethrough
Text("~~deleted~~")

// Code
Text("`monospace`")

// Links
Text("[Link Text](https://example.com)")

// Soft breaks
Text("Line one\nLine two")
```

### Markdown from Variables

```swift
// String interpolation with AttributedString
let markdownString = "**Important:** Check the [documentation](https://docs.example.com)"

// Option 1: Direct (for literals only)
Text("**Bold** text")

// Option 2: AttributedString for variables
if let attributed = try? AttributedString(markdown: markdownString) {
    Text(attributed)
}
```

---

## AttributedString

### Creating AttributedString

```swift
// From plain string
var attributed = AttributedString("Hello World")

// From Markdown
let markdown = try? AttributedString(markdown: "**Bold** and *italic*")

// From localized string
let localized = AttributedString(localized: "greeting_message")
```

### Applying Attributes

```swift
var text = AttributedString("Hello World")

// Whole string attributes
text.font = .title
text.foregroundColor = .blue
text.backgroundColor = .yellow

// Range-based attributes
if let range = text.range(of: "World") {
    text[range].font = .title.bold()
    text[range].foregroundColor = .red
}
```

### Available Attributes

```swift
var text = AttributedString("Styled")

// Typography
text.font = .body
text.foregroundColor = .primary
text.backgroundColor = .clear

// Text decoration
text.strikethroughStyle = .single
text.strikethroughColor = .red
text.underlineStyle = .single
text.underlineColor = .blue

// Spacing
text.kern = 2.0           // Character spacing
text.tracking = 1.0       // Similar to kern
text.baselineOffset = 5   // Vertical offset

// Links
text.link = URL(string: "https://apple.com")

// Accessibility
text.accessibilityLabel = "Custom label"
text.accessibilitySpeechSpellsOutCharacters = true
```

### Combining AttributedStrings

```swift
var greeting = AttributedString("Hello ")
greeting.font = .title

var name = AttributedString("World")
name.font = .title.bold()
name.foregroundColor = .blue

let combined = greeting + name
Text(combined)
```

### Iterating Over Runs

```swift
let attributed = try? AttributedString(markdown: "**Bold** and *italic*")

// Iterate through styled runs
for run in attributed?.runs ?? [] {
    print("Text: \(attributed?[run.range] ?? "")")
    print("Font: \(run.font ?? .body)")
}
```

---

## Markdown Parsing Options

### Basic Parsing

```swift
let source = "# Heading\n**Bold** text"

// Default parsing
let attributed = try? AttributedString(markdown: source)

// With options
let options = AttributedString.MarkdownParsingOptions(
    interpretedSyntax: .inlineOnlyPreservingWhitespace
)
let parsed = try? AttributedString(markdown: source, options: options)
```

### Interpreted Syntax Options

```swift
// Full Markdown (default)
.interpretedSyntax: .full

// Inline only (no block elements)
.interpretedSyntax: .inlineOnly

// Inline, preserving whitespace
.interpretedSyntax: .inlineOnlyPreservingWhitespace
```

### Handling Parse Errors

```swift
do {
    let attributed = try AttributedString(markdown: source)
    // Use attributed string
} catch {
    // Fallback to plain text
    let plain = AttributedString(source)
}
```

### Custom Attribute Scopes

```swift
// Define custom attributes
enum MyAttributes: AttributeScope {
    let customHighlight: CustomHighlightAttribute
}

struct CustomHighlightAttribute: CodableAttributedStringKey {
    typealias Value = Bool
    static let name = "customHighlight"
}

// Extend AttributeScopes
extension AttributeScopes {
    var myAttributes: MyAttributes.Type { MyAttributes.self }
}

// Use custom attributes
var text = AttributedString("Highlighted")
text.customHighlight = true
```

---

## Rich Text Editing (iOS 26)

### TextEditor with AttributedString

iOS 26 introduces first-class rich text editing:

```swift
struct RichTextEditor: View {
    @State private var content = AttributedString("Edit me with **formatting**")
    @State private var selection = AttributedTextSelection()

    var body: some View {
        TextEditor(text: $content, selection: $selection)
            .textEditorStyle(.plain)
    }
}
```

### AttributedTextSelection

```swift
struct FormattingEditor: View {
    @State private var content = AttributedString()
    @State private var selection = AttributedTextSelection()

    var body: some View {
        VStack {
            // Formatting toolbar
            HStack {
                Button("Bold") { toggleBold() }
                Button("Italic") { toggleItalic() }
                Button("Underline") { toggleUnderline() }
            }

            TextEditor(text: $content, selection: $selection)
        }
    }

    func toggleBold() {
        content.transformAttributes(in: selection.range) { container in
            // Toggle bold
            if container.font?.isBold == true {
                container.font = container.font?.removingBold()
            } else {
                container.font = container.font?.bold()
            }
        }
    }

    func toggleItalic() {
        content.transformAttributes(in: selection.range) { container in
            if container.font?.isItalic == true {
                container.font = container.font?.removingItalic()
            } else {
                container.font = container.font?.italic()
            }
        }
    }

    func toggleUnderline() {
        content.transformAttributes(in: selection.range) { container in
            if container.underlineStyle != nil {
                container.underlineStyle = nil
            } else {
                container.underlineStyle = .single
            }
        }
    }
}
```

### Built-in Keyboard Shortcuts

iOS 26 TextEditor supports standard keyboard shortcuts:
- ⌘B - Bold
- ⌘I - Italic
- ⌘U - Underline

### Font Resolution Context

```swift
TextEditor(text: $content, selection: $selection)
    .environment(\.fontResolutionContext, FontResolutionContext(
        defaultFont: .body,
        defaultForegroundColor: .primary
    ))
```

---

## Text Interpolation

### Format Styles

```swift
// Numbers
Text("Count: \(count)")
Text("Price: \(price, format: .currency(code: "USD"))")
Text("Percentage: \(value, format: .percent)")
Text("Decimal: \(number, format: .number.precision(.fractionLength(2)))")

// Dates
Text("Date: \(date, format: .dateTime)")
Text("Day: \(date, format: .dateTime.day().month().year())")
Text("Time: \(date, format: .dateTime.hour().minute())")

// Relative dates
Text(date, style: .relative)   // "2 hours ago"
Text(date, style: .timer)      // "2:30:00"
Text(date, style: .date)       // "June 15, 2025"
Text(date, style: .time)       // "3:30 PM"
Text(date, style: .offset)     // "+2 hours"

// Date ranges
Text(startDate...endDate)

// Lists
Text(names, format: .list(type: .and))  // "Alice, Bob, and Charlie"

// Measurements
Text(distance, format: .measurement(width: .abbreviated))
```

### Person Name Components

```swift
let name = PersonNameComponents(givenName: "John", familyName: "Doe")
Text(name, format: .name(style: .long))
```

### ByteCount

```swift
Text(fileSize, format: .byteCount(style: .file))
```

---

## Localization

### LocalizedStringKey

```swift
// Automatic localization lookup
Text("welcome_message")  // Looks up in Localizable.strings

// With interpolation
Text("greeting_\(username)")  // "greeting_%@" in strings file

// Explicit localized string
Text(LocalizedStringKey("settings_title"))
```

### String Catalogs (.xcstrings)

Modern localization uses String Catalogs:

```swift
// In String Catalog (Localizable.xcstrings)
// Key: "items_count"
// English: "%lld items"
// French: "%lld éléments"

Text("items_count \(count)")
```

### Pluralization

```swift
// In String Catalog, define variants:
// "items_count" with plural variants:
// - zero: "No items"
// - one: "1 item"
// - other: "%lld items"

Text("items_count \(count)")
```

### AttributedString Localization

```swift
// Localized with attributes
let attributed = AttributedString(localized: "formatted_message")
Text(attributed)
```

---

## Text Selection

### Enabling Selection

```swift
Text("Selectable text that users can copy")
    .textSelection(.enabled)

// Disable selection
Text("Not selectable")
    .textSelection(.disabled)
```

### Selection on Lists

```swift
List(items) { item in
    Text(item.content)
        .textSelection(.enabled)
}
```

---

## TextField and SecureField

### Basic TextField

```swift
@State private var text = ""

TextField("Placeholder", text: $text)

// With prompt
TextField("Username", text: $username, prompt: Text("Enter username"))

// Axis for multiline
TextField("Description", text: $description, axis: .vertical)
    .lineLimit(3...6)
```

### TextField Styles

```swift
TextField("Input", text: $text)
    .textFieldStyle(.automatic)
    .textFieldStyle(.plain)
    .textFieldStyle(.roundedBorder)
```

### SecureField

```swift
SecureField("Password", text: $password)
```

### Formatting TextField

```swift
// Number input
TextField("Amount", value: $amount, format: .currency(code: "USD"))

// Date input
TextField("Date", value: $date, format: .dateTime)

// Custom format
TextField("Phone", value: $phone, format: PhoneNumberFormat())
```

### TextField Focus

```swift
@FocusState private var isFocused: Bool

TextField("Input", text: $text)
    .focused($isFocused)

Button("Focus") {
    isFocused = true
}
```

### Keyboard Types

```swift
TextField("Email", text: $email)
    .keyboardType(.emailAddress)
    .textContentType(.emailAddress)
    .autocapitalization(.none)
    .autocorrectionDisabled()

TextField("Phone", text: $phone)
    .keyboardType(.phonePad)
    .textContentType(.telephoneNumber)

TextField("URL", text: $url)
    .keyboardType(.URL)
    .textContentType(.URL)
```

### Submit Actions

```swift
TextField("Search", text: $query)
    .onSubmit {
        performSearch()
    }
    .submitLabel(.search)

// Submit labels: .done, .go, .join, .next, .return, .search, .send
```

---

## Label

### Basic Label

```swift
Label("Settings", systemImage: "gear")
Label("Document", image: "doc-icon")

// Custom label
Label {
    Text("Custom")
        .font(.headline)
} icon: {
    Image(systemName: "star.fill")
        .foregroundStyle(.yellow)
}
```

### Label Styles

```swift
Label("Title", systemImage: "star")
    .labelStyle(.automatic)
    .labelStyle(.titleOnly)
    .labelStyle(.iconOnly)
    .labelStyle(.titleAndIcon)
```

---

## Link

### Basic Links

```swift
Link("Apple", destination: URL(string: "https://apple.com")!)

Link(destination: URL(string: "https://apple.com")!) {
    Label("Visit Apple", systemImage: "safari")
}
```

### Links in Text

```swift
// Using Markdown
Text("Visit [our website](https://example.com) for more info")

// Using AttributedString
var text = AttributedString("Visit our website")
if let range = text.range(of: "our website") {
    text[range].link = URL(string: "https://example.com")
    text[range].foregroundColor = .blue
}
Text(text)
```

---

## Privacy Sensitive Content

### Redaction

```swift
Text(sensitiveData)
    .privacySensitive()

// Manual redaction
Text("Hidden Content")
    .redacted(reason: .privacy)
    .redacted(reason: .placeholder)

// Unredacted
Text("Always Visible")
    .unredacted()
```

### Conditional Redaction

```swift
struct ContentView: View {
    @Environment(\.redactionReasons) var redactionReasons

    var body: some View {
        if redactionReasons.contains(.privacy) {
            Text("•••••")
        } else {
            Text(accountBalance, format: .currency(code: "USD"))
        }
    }
}
```

---

## Text Rendering Performance

### Efficient Text Updates

```swift
// GOOD: Separate text views for changing content
VStack {
    Text("Static label:")
    Text("\(dynamicValue)")  // Only this updates
}

// AVOID: Combining static and dynamic in one Text
Text("Static label: \(dynamicValue)")  // Whole text re-renders
```

### Large Text Handling

```swift
// For very long text, use ScrollView
ScrollView {
    Text(veryLongContent)
        .textSelection(.enabled)
}

// Or LazyVStack for segmented content
ScrollView {
    LazyVStack(alignment: .leading) {
        ForEach(paragraphs, id: \.self) { paragraph in
            Text(paragraph)
                .padding(.bottom)
        }
    }
}
```

---

## Accessibility

### VoiceOver Customization

```swift
Text("5 stars")
    .accessibilityLabel("5 out of 5 stars")

Text("$99")
    .accessibilityLabel("99 dollars")

// Heading level
Text("Section Title")
    .accessibilityAddTraits(.isHeader)
```

### Dynamic Type Support

```swift
// Respect user's text size preference
Text("Accessible text")
    .font(.body)  // Scales with Dynamic Type

// Fixed size (use sparingly)
Text("Fixed size")
    .font(.system(size: 14))
    .dynamicTypeSize(.large)  // Cap at large

// Size range
Text("Limited scaling")
    .dynamicTypeSize(.small...(.accessibilityLarge))
```

---

## Best Practices

### 1. Use Semantic Fonts

```swift
// GOOD: Semantic fonts scale with Dynamic Type
.font(.headline)
.font(.body)
.font(.caption)

// AVOID: Fixed sizes unless necessary
.font(.system(size: 16))
```

### 2. Support Markdown for User Content

```swift
// Parse user input as Markdown safely
func renderUserContent(_ input: String) -> Text {
    if let attributed = try? AttributedString(
        markdown: input,
        options: .init(interpretedSyntax: .inlineOnlyPreservingWhitespace)
    ) {
        return Text(attributed)
    }
    return Text(input)
}
```

### 3. Enable Text Selection for Copyable Content

```swift
Text(address)
    .textSelection(.enabled)
```

### 4. Handle Localization Properly

```swift
// Use LocalizedStringKey for user-facing text
Text("button_title")

// Use verbatim for data
Text(verbatim: userGeneratedContent)
```

### 5. Consider Privacy

```swift
Text(sensitiveInfo)
    .privacySensitive()
```

---

## Official Resources

- [Text Documentation](https://developer.apple.com/documentation/swiftui/text)
- [AttributedString Documentation](https://developer.apple.com/documentation/foundation/attributedstring)
- [TextEditor Documentation](https://developer.apple.com/documentation/swiftui/texteditor)
- [Markdown in SwiftUI](https://developer.apple.com/documentation/foundation/attributedstring/markdownparsingoptions)
- [WWDC21: What's new in Foundation](https://developer.apple.com/videos/play/wwdc2021/10109/)
