---
name: fosmvvm-leaf-view-generator
description: Generate Leaf templates (Views) for FOSMVVM WebApps. Use when creating HTML views that render ViewModels - both full-page templates and fragments for HTML-over-the-wire updates.
---

# FOSMVVM Leaf View Generator

Generate Leaf templates that render ViewModels for web clients.

> **Architecture context:** See [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md)

---

## The View Layer for WebApps

In FOSMVVM, Leaf templates are the **View** in M-V-VM for web clients:

```
Model → ViewModel → Leaf Template → HTML
              ↑           ↑
        (localized)  (renders it)
```

**Key principle:** The ViewModel is already localized when it reaches the template. The template just renders what it receives.

---

## Core Principle: View-ViewModel Alignment

**The Leaf filename should match the ViewModel it renders.**

```
Sources/
  {ViewModelsTarget}/
    ViewModels/
      {Feature}ViewModel.swift        ←──┐
      {Entity}CardViewModel.swift     ←──┼── Same names
                                          │
  {WebAppTarget}/                         │
    Resources/Views/                      │
      {Feature}/                          │
        {Feature}View.leaf            ────┤  (renders {Feature}ViewModel)
        {Entity}CardView.leaf         ────┘  (renders {Entity}CardViewModel)
```

This alignment provides:
- **Discoverability** - Find the template for any ViewModel instantly
- **Consistency** - Same naming discipline as SwiftUI
- **Maintainability** - Changes to ViewModel are reflected in template location

---

## Two Template Types

### Full-Page Templates

Render a complete page with layout, navigation, CSS/JS includes.

```
{Feature}View.leaf
├── Extends base layout
├── Includes <html>, <head>, <body>
├── Renders {Feature}ViewModel
└── May embed fragment templates for components
```

**Use for:** Initial page loads, navigation destinations.

### Fragment Templates

Render a single component - no layout, no page structure.

```
{Entity}CardView.leaf
├── NO layout extension
├── Single root element
├── Renders {Entity}CardViewModel
├── Has data-* attributes for state
└── Returned to JS for DOM swapping
```

**Use for:** Partial updates, HTML-over-the-wire responses.

---

## The HTML-Over-The-Wire Pattern

For dynamic updates without full page reloads:

```
JS Event → WebApp Route → ServerRequest.processRequest() → Controller
                                                              ↓
                                                          ViewModel
                                                              ↓
HTML ← JS DOM swap ← WebApp returns ← Leaf renders ←────────┘
```

**The WebApp route:**
```swift
app.post("move-{entity}") { req async throws -> Response in
    let body = try req.content.decode(Move{Entity}Request.RequestBody.self)
    let serverRequest = Move{Entity}Request(requestBody: body)
    guard let response = try await serverRequest.processRequest(baseURL: app.serverBaseURL) else {
        throw Abort(.internalServerError)
    }

    // Render fragment template with ViewModel
    return try await req.view.render(
        "{Feature}/{Entity}CardView",
        ["card": response.viewModel]
    ).encodeResponse(for: req)
}
```

**JS receives HTML and swaps it into the DOM** - no JSON parsing, no client-side rendering.

---

## When to Use This Skill

- Creating a new page template (full-page)
- Creating a new card, row, or component template (fragment)
- Adding data attributes for JS event handling
- Troubleshooting Localizable types not rendering correctly
- Setting up templates for HTML-over-the-wire responses

---

## Key Patterns

### Pattern 1: Data Attributes for State

Fragments must embed all state that JS needs for future actions:

```html
<div class="{entity}-card"
     data-{entity}-id="#(card.id)"
     data-status="#(card.status)"
     data-category="#(card.category)"
     draggable="true">
```

**Rules:**
- `data-{entity}-id` for the primary identifier
- `data-{field}` for state values (kebab-case)
- Store **raw values** (enum cases), not localized display names
- JS reads these to build ServerRequest payloads

```javascript
const request = {
    {entity}Id: element.dataset.{entity}Id,
    newStatus: targetColumn.dataset.status
};
```

### Pattern 2: Localizable Types in Leaf

FOSMVVM's `LeafDataRepresentable` conformance handles Localizable types automatically.

**In templates, just use the property:**
```html
<span class="date">#(card.createdAt)</span>
<!-- Renders: "Dec 27, 2025" (localized) -->
```

**If Localizable types render incorrectly** (showing `[ds: "2", ls: "...", v: "..."]`):
1. Ensure FOSMVVMVapor is imported
2. Check `Localizable+Leaf.swift` exists with conformances
3. Clean build: `swift package clean && swift build`

### Pattern 3: Display Values vs Identifiers

ViewModels should provide both raw values (for data attributes) and localized strings (for display). For enum localization, see the [Enum Localization Pattern](../fosmvvm-viewmodel-generator/SKILL.md#enum-localization-pattern).

```swift
@ViewModel
public struct {Entity}CardViewModel {
    public let id: ModelIdType              // For data-{entity}-id
    public let status: {Entity}Status       // Raw enum for data-status
    public let statusDisplay: LocalizableString  // Localized (stored, not @LocalizedString)
}
```

```html
<div data-status="#(card.status)">           <!-- Raw: "queued" for JS -->
    <span class="badge">#(card.statusDisplay)</span>  <!-- Localized: "In Queue" -->
</div>
```

### Pattern 4: Fragment Structure

Fragments are minimal - just the component:

```html
<!-- {Entity}CardView.leaf -->
<div class="{entity}-card"
     data-{entity}-id="#(card.id)"
     data-status="#(card.status)">

    <div class="card-content">
        <p class="text">#(card.contentPreview)</p>
    </div>

    <div class="card-footer">
        <span class="creator">#(card.creatorName)</span>
        <span class="date">#(card.createdAt)</span>
    </div>
</div>
```

**Rules:**
1. NO `#extend("base")` - fragments don't use layouts
2. **Single root element** - makes DOM swapping clean
3. All required state in data-* attributes
4. Localized values from ViewModel properties

### Pattern 5: Full-Page Structure

Full pages extend a base layout:

```html
<!-- {Feature}View.leaf -->
#extend("base"):
#export("content"):

<div class="{feature}-container">
    <header class="{feature}-header">
        <h1>#(viewModel.title)</h1>
    </header>

    <main class="{feature}-content">
        #for(card in viewModel.cards):
        #extend("{Feature}/{Entity}CardView")
        #endfor
    </main>
</div>

#endexport
#endextend
```

### Pattern 6: Conditional Rendering

```html
#if(card.isHighPriority):
<span class="priority-badge">#(card.priorityLabel)</span>
#endif

#if(card.assignee):
<div class="assignee">
    <span class="name">#(card.assignee.name)</span>
</div>
#else:
<div class="unassigned">#(card.unassignedLabel)</div>
#endif
```

### Pattern 7: Looping with Embedded Fragments

```html
<div class="column" data-status="#(column.status)">
    <div class="column-header">
        <h3>#(column.displayName)</h3>
        <span class="count">#(column.count)</span>
    </div>

    <div class="column-cards">
        #for(card in column.cards):
        #extend("{Feature}/{Entity}CardView")
        #endfor

        #if(column.cards.count == 0):
        <div class="empty-state">#(column.emptyMessage)</div>
        #endif
    </div>
</div>
```

---

## File Organization

```
Sources/{WebAppTarget}/Resources/Views/
├── base.leaf                          # Base layout (all pages extend this)
├── {Feature}/
│   ├── {Feature}View.leaf             # Full page → {Feature}ViewModel
│   ├── {Entity}CardView.leaf          # Fragment → {Entity}CardViewModel
│   ├── {Entity}RowView.leaf           # Fragment → {Entity}RowViewModel
│   └── {Modal}View.leaf               # Fragment → {Modal}ViewModel
└── Shared/
    ├── HeaderView.leaf                # Shared components
    └── FooterView.leaf
```

---

## Leaf Built-in Functions

Leaf provides useful functions for working with arrays:

```html
<!-- Count items -->
#if(count(cards) > 0):
<p>You have #count(cards) cards</p>
#endif

<!-- Check if array contains value -->
#if(contains(statuses, "active")):
<span class="badge">Active</span>
#endif
```

### Loop Variables

Inside `#for` loops, Leaf provides progress variables:

```html
#for(item in items):
    #if(isFirst):<span class="first">#endif
    #(item.name)
    #if(!isLast):, #endif
#endfor
```

| Variable | Description |
|----------|-------------|
| `isFirst` | True on first iteration |
| `isLast` | True on last iteration |
| `index` | Current iteration (0-based) |

### Array Index Access

Direct array subscripts (`array[0]`) are not documented in Leaf. For accessing specific elements, pre-compute in the ViewModel:

```swift
public let firstCard: CardViewModel?

public init(cards: [CardViewModel]) {
    self.cards = cards
    self.firstCard = cards.first
}
```

---

## Codable and Computed Properties

Swift's synthesized `Codable` only encodes **stored properties**. Since ViewModels are passed to Leaf via Codable encoding, computed properties won't be available.

```swift
// Computed property - NOT encoded by Codable, invisible in Leaf
public var hasCards: Bool { !cards.isEmpty }

// Stored property - encoded by Codable, available in Leaf
public let hasCards: Bool
```

If you need a derived value in a Leaf template, calculate it in `init()` and store it:

```swift
public let hasCards: Bool
public let cardCount: Int

public init(cards: [CardViewModel]) {
    self.cards = cards
    self.hasCards = !cards.isEmpty
    self.cardCount = cards.count
}
```

---

## Common Mistakes

### Missing Data Attributes

```html
<!-- BAD - JS can't identify this element -->
<div class="{entity}-card">

<!-- GOOD - JS reads data-{entity}-id -->
<div class="{entity}-card" data-{entity}-id="#(card.id)">
```

### Storing Display Names Instead of Identifiers

```html
<!-- BAD - localized string can't be sent to server -->
<div data-status="#(card.statusDisplayName)">

<!-- GOOD - raw enum value works for requests -->
<div data-status="#(card.status)">
```

### Using Layout in Fragments

```html
<!-- BAD - fragment should not extend layout -->
#extend("base"):
#export("content"):
<div class="card">...</div>
#endexport
#endextend

<!-- GOOD - fragment is just the component -->
<div class="card">...</div>
```

### Hardcoding Text

```html
<!-- BAD - not localizable -->
<span class="status">Queued</span>

<!-- GOOD - ViewModel provides localized value -->
<span class="status">#(card.statusDisplayName)</span>
```

### Concatenating Localized Values

```html
<!-- BAD - breaks RTL languages and locale-specific word order -->
#(conversation.messageCount) #(conversation.messagesLabel)

<!-- GOOD - ViewModel composes via @LocalizedSubs -->
#(conversation.messageCountDisplay)
```

Template-level concatenation assumes left-to-right order. Use `@LocalizedSubs` in the ViewModel so YAML can define locale-appropriate ordering:

```yaml
en:
  ConversationViewModel:
    messageCountDisplay: "%{messageCount} %{messagesLabel}"
ar:
  ConversationViewModel:
    messageCountDisplay: "%{messagesLabel} %{messageCount}"
```

### Formatting Dates in Templates

```html
<!-- BAD - hardcoded format, not locale-aware, concatenation issue -->
<span>#(content.createdPrefix) #date(content.createdAt, "MMM d, yyyy")</span>

<!-- GOOD - LocalizableDate handles locale formatting, @LocalizedSubs composes -->
<span>#(content.createdDisplay)</span>
```

Use `LocalizableDate` in the ViewModel - it formats according to user locale. If combining with a prefix, use `@LocalizedSubs`:

```swift
public let createdAt: LocalizableDate

@LocalizedSubs(\.createdPrefix, \.createdAt)
public var createdDisplay
```

### Mismatched Filenames

```
<!-- BAD - filename doesn't match ViewModel -->
ViewModel: UserProfileCardViewModel
Template:  ProfileCard.leaf

<!-- GOOD - aligned names -->
ViewModel: UserProfileCardViewModel
Template:  UserProfileCardView.leaf
```

---

## Generation Process

### Step 1: Identify the ViewModel

What ViewModel does this template render?
- `{Feature}ViewModel` → Full-page template
- `{Entity}CardViewModel` → Card fragment
- `{Entity}RowViewModel` → Row fragment

### Step 2: Determine Template Type

| ViewModel Purpose | Template Type | Has Layout? |
|-------------------|---------------|-------------|
| Page content | Full-page | Yes |
| List item / Card | Fragment | No |
| Modal content | Fragment | No |
| Inline component | Fragment | No |

### Step 3: Map ViewModel Properties to Template

| Property | Template Usage |
|----------|----------------|
| `id` | `data-{entity}-id="#(vm.id)"` |
| Raw enum | `data-{field}="#(vm.field)"` |
| `LocalizedString` | Display text: `#(vm.displayName)` |
| `LocalizedDate` | Formatted date: `#(vm.createdAt)` |
| Nested ViewModel | Embed fragment or access properties |

### Step 4: Generate Template

Use [reference.md](reference.md) templates as starting point.

### Step 5: Verify

1. Filename matches ViewModel name
2. Data attributes have all state JS needs
3. Localizable types render correctly (not as debug output)
4. Single root element for fragments
5. No layout extension for fragments

---

## Collaboration Protocol

1. **Identify the ViewModel** - What are we rendering?
2. **Full-page or fragment?** - Determines structure
3. **List data attributes needed** - What state does JS need?
4. **Generate template** - Get feedback
5. **Show WebApp route** - How the template gets rendered

---

## See Also

- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - Full architecture
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - Creates the ViewModels this skill renders
- [fosmvvm-serverrequest-generator](../fosmvvm-serverrequest-generator/SKILL.md) - Creates requests that return ViewModels
- [reference.md](reference.md) - Complete template examples

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-24 | Initial Kairos-specific skill |
| 2.0 | 2025-12-27 | Generalized for FOSMVVM, added View-ViewModel alignment principle, full-page templates, architecture connection |
| 2.1 | 2026-01-08 | Added Leaf Built-in Functions section (count, contains, loop variables). Clarified Codable/computed properties. Corrected earlier false claims about #count() not working. |
| 2.2 | 2026-01-19 | Updated Pattern 3 to use stored LocalizableString for dynamic enum displays; linked to Enum Localization Pattern. Added anti-patterns for concatenating localized values and formatting dates in templates. |
