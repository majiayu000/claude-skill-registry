---
name: atomic-design-ios
description: "Expert Atomic Design decisions for iOS/tvOS: when component hierarchy adds value vs overkill, atom vs molecule boundary judgment, design token management trade-offs, and component reusability patterns. Use when structuring design systems, deciding component granularity, or organizing component libraries. Trigger keywords: Atomic Design, atoms, molecules, organisms, templates, component library, design system, design tokens, reusability, composition"
version: "3.0.0"
---

# Atomic Design iOS — Expert Decisions

Expert decision frameworks for Atomic Design choices in SwiftUI. Claude knows view composition — this skill provides judgment calls for when component hierarchy adds value and how to define boundaries.

---

## Decision Trees

### Do You Need Atomic Design?

```
How large is your design system?
├─ Small (< 10 components)
│  └─ Skip formal hierarchy
│     Simple "Components" folder is fine
│
├─ Medium (10-30 components)
│  └─ Consider Atoms + Molecules
│     Skip Organisms/Templates if not needed
│
└─ Large (30+ components, multiple teams)
   └─ Full Atomic Design hierarchy
      Atoms → Molecules → Organisms → Templates
```

**The trap**: Atomic Design for a 5-screen app. The overhead of categorization exceeds the benefit.

### Atom vs Molecule Boundary

```
Does this component combine multiple distinct elements?
├─ NO (single visual element)
│  └─ Atom
│     Button, TextField, Badge, Icon, Label
│
└─ YES (2+ elements that work together)
   └─ Can these elements be used independently?
      ├─ YES → Molecule (SearchBar = Icon + TextField + Button)
      └─ NO → Still Atom (password field with toggle is one unit)
```

### Component Extraction Decision

```
Will this be used in multiple places?
├─ NO (one-off)
│  └─ Don't extract
│     Inline in parent view
│
├─ YES (2-3 places)
│  └─ Extract as local component
│     Same file or sibling file
│
└─ YES (4+ places or cross-feature)
   └─ Extract to design system
      Full Atom/Molecule treatment
```

### Design Token Scope

```
What type of value?
├─ Color
│  └─ Is it semantic or brand?
│     ├─ Semantic (error, success) → Color.error, Color.success
│     └─ Brand (primary, accent) → Color.brandPrimary
│
├─ Spacing
│  └─ Use named scale (xs, sm, md, lg, xl)
│     Never magic numbers
│
├─ Typography
│  └─ Use semantic names (body, heading, caption)
│     Map to Font.body, Font.heading
│
└─ Corner radius, shadows
   └─ Named tokens if used consistently
      Radius.card, Shadow.elevated
```

---

## NEVER Do

### Component Design

**NEVER** create atoms that know about app state:
```swift
// ❌ Atom depends on app-level state
struct PrimaryButton: View {
    @EnvironmentObject var authManager: AuthManager

    var body: some View {
        Button(action: action) {
            if authManager.isLoading { ProgressView() }
            else { Text(title) }
        }
    }
}

// ✅ Atom receives all state as parameters
struct PrimaryButton: View {
    let title: String
    let action: () -> Void
    var isLoading: Bool = false

    var body: some View {
        Button(action: action) {
            if isLoading { ProgressView() }
            else { Text(title) }
        }
    }
}
```

**NEVER** hardcode values in components:
```swift
// ❌ Magic numbers everywhere
struct Card: View {
    var body: some View {
        content
            .padding(16)  // Magic number
            .background(Color(hex: "#FFFFFF"))  // Hardcoded
            .cornerRadius(12)  // Magic number
    }
}

// ✅ Use design tokens
struct Card: View {
    var body: some View {
        content
            .padding(Spacing.md)
            .background(Color.surface)
            .cornerRadius(Radius.card)
    }
}
```

**NEVER** create components with too many parameters:
```swift
// ❌ Too many parameters — hard to use
struct ComplexButton: View {
    let title: String
    let subtitle: String?
    let icon: String?
    let iconPosition: IconPosition
    let size: Size
    let style: Style
    let isLoading: Bool
    let isEnabled: Bool
    let hasBorder: Bool
    let cornerRadius: CGFloat
    // ... 10 more parameters
}

// ✅ Split into focused variants
struct PrimaryButton: View { ... }
struct SecondaryButton: View { ... }
struct IconButton: View { ... }
struct LoadingButton: View { ... }
```

### Hierarchy Mistakes

**NEVER** skip levels in composition:
```swift
// ❌ Template directly uses atoms (no molecules/organisms)
struct ProductListTemplate: View {
    var body: some View {
        ForEach(products) { product in
            // Building organism inline from atoms
            HStack {
                AsyncImage(url: product.imageURL)
                VStack {
                    Text(product.name).font(.headline)
                    Text("$\(product.price)").foregroundColor(.blue)
                }
                Button("Add") { }
            }
        }
    }
}

// ✅ Template uses organisms
struct ProductListTemplate: View {
    var body: some View {
        ForEach(products) { product in
            ProductCard(product: product, onAddToCart: { })
        }
    }
}
```

**NEVER** put business logic in design system components:
```swift
// ❌ Organism fetches data
struct UserCard: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        Card {
            // Uses viewModel.user
        }
        .onAppear { viewModel.load() }
    }
}

// ✅ Organism is purely presentational
struct UserCard: View {
    let user: User
    let onTap: () -> Void

    var body: some View {
        Card {
            // Uses passed-in user
        }
    }
}
```

### Design Token Mistakes

**NEVER** use platform colors directly:
```swift
// ❌ Hardcoded system colors
.foregroundColor(.blue)
.background(Color(.systemGray6))

// ✅ Semantic tokens that can be themed
.foregroundColor(Color.interactive)
.background(Color.surfaceSecondary)
```

**NEVER** duplicate token definitions:
```swift
// ❌ Same value defined in multiple places
struct Card { let cornerRadius: CGFloat = 12 }
struct Button { let cornerRadius: CGFloat = 12 }
struct TextField { let cornerRadius: CGFloat = 12 }

// ✅ Single source of truth
enum Radius {
    static let sm: CGFloat = 4
    static let md: CGFloat = 8
    static let lg: CGFloat = 12
}

struct Card { ... .cornerRadius(Radius.lg) }
```

---

## Essential Patterns

### Token System Structure

```swift
// Spacing tokens
enum Spacing {
    static let xs: CGFloat = 4
    static let sm: CGFloat = 8
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32
}

// Color tokens (support dark mode)
extension Color {
    // Semantic
    static let textPrimary = Color("TextPrimary")
    static let textSecondary = Color("TextSecondary")
    static let surface = Color("Surface")
    static let surfaceSecondary = Color("SurfaceSecondary")

    // Brand
    static let brandPrimary = Color("BrandPrimary")
    static let brandAccent = Color("BrandAccent")

    // Feedback
    static let success = Color("Success")
    static let warning = Color("Warning")
    static let error = Color("Error")
}

// Typography tokens
extension Font {
    static let displayLarge = Font.system(size: 34, weight: .bold)
    static let heading1 = Font.system(size: 28, weight: .bold)
    static let heading2 = Font.system(size: 22, weight: .semibold)
    static let bodyLarge = Font.system(size: 17)
    static let bodyRegular = Font.system(size: 15)
    static let caption = Font.system(size: 13)
}
```

### Composable Atom Pattern

```swift
// Atom with sensible defaults and overrides
struct PrimaryButton: View {
    let title: String
    let action: () -> Void
    var isLoading: Bool = false
    var isEnabled: Bool = true
    var size: Size = .regular

    enum Size {
        case small, regular, large

        var padding: EdgeInsets {
            switch self {
            case .small: return EdgeInsets(horizontal: Spacing.sm, vertical: Spacing.xs)
            case .regular: return EdgeInsets(horizontal: Spacing.md, vertical: Spacing.sm)
            case .large: return EdgeInsets(horizontal: Spacing.lg, vertical: Spacing.md)
            }
        }

        var font: Font {
            switch self {
            case .small: return .caption
            case .regular: return .bodyRegular
            case .large: return .heading2
            }
        }
    }

    var body: some View {
        Button(action: action) {
            Group {
                if isLoading {
                    ProgressView()
                } else {
                    Text(title).font(size.font)
                }
            }
            .frame(maxWidth: .infinity)
            .padding(size.padding)
        }
        .background(isEnabled ? Color.brandPrimary : Color.textSecondary)
        .foregroundColor(.white)
        .cornerRadius(Radius.md)
        .disabled(!isEnabled || isLoading)
    }
}
```

### Molecule with Slot Pattern

```swift
// Generic molecule with customizable slots
struct Card<Content: View, Footer: View>: View {
    let content: Content
    let footer: Footer?

    init(
        @ViewBuilder content: () -> Content,
        @ViewBuilder footer: () -> Footer
    ) {
        self.content = content()
        self.footer = footer()
    }

    var body: some View {
        VStack(alignment: .leading, spacing: Spacing.md) {
            content

            if let footer = footer {
                Divider()
                footer
            }
        }
        .padding(Spacing.md)
        .background(Color.surface)
        .cornerRadius(Radius.lg)
        .shadow(color: .black.opacity(0.1), radius: 4, y: 2)
    }
}

// Convenience initializer without footer
extension Card where Footer == EmptyView {
    init(@ViewBuilder content: () -> Content) {
        self.content = content()
        self.footer = nil
    }
}
```

---

## Quick Reference

### When to Extract Components

| Scenario | Action |
|----------|--------|
| Used once | Keep inline |
| Used 2-3 times in same feature | Local extraction |
| Used across features | Design system component |
| Complex but single-use | Extract for readability only |

### Component Classification

| Level | Examples | Knows About |
|-------|----------|-------------|
| Atom | Button, TextField, Icon, Badge | Nothing external |
| Molecule | SearchBar, FormInput, Card | Atoms only |
| Organism | NavigationBar, ProductCard, UserList | Atoms + Molecules |
| Template | ListPageLayout, FormLayout | Organisms |

### Design Token Categories

| Category | Token Examples |
|----------|----------------|
| Spacing | xs, sm, md, lg, xl |
| Color | textPrimary, surface, brandPrimary, error |
| Typography | displayLarge, heading1, body, caption |
| Radius | sm, md, lg, full |
| Shadow | subtle, elevated, prominent |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Atom uses @EnvironmentObject | Knows too much | Pass state as params |
| 10+ parameters on component | Too flexible | Split into variants |
| Magic numbers in components | Not themeable | Use tokens |
| Template builds from atoms | Skipping levels | Use molecules/organisms |
| Different corner radius per component | Inconsistency | Token system |
| Component fetches data | Wrong layer | Presentational only |
