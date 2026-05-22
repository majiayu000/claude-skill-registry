---
name: solid-swift
description: SOLID principles for Swift 6 and SwiftUI (iOS 26+). Apple recommended patterns, @Observable, actors, Preview-driven development.
---

# SOLID Swift - Apple Best Practices 2025

## Current Date (CRITICAL)

**Today: January 2026** - ALWAYS use the current year for your searches.
Search with "2025" or "2026", NEVER with past years.

## MANDATORY: Research Before Coding

**CRITICAL: Check today's date first, then search documentation and web BEFORE writing any code.**

### Priority Order (2026)

1. ⭐ **Apple Docs MCP** (PRIMARY) - Official Apple documentation with WWDC 2014-2025
   - Search SwiftUI, UIKit, Foundation, CoreData, ARKit docs
   - Get framework details and symbol information
   - Search WWDC sessions with transcripts (offline access)
   - Access Apple sample code
   - See: `mcp-tools/apple-docs-mcp.md`

2. **Context7** (SECONDARY) - For third-party libraries and community packages
   - Use only if Apple Docs MCP doesn't have the answer
   - Good for SPM packages, community libraries

3. **Exa web search** (TERTIARY) - Latest trends and blog posts
   - Use with current year for newest patterns
   - Community tutorials and articles

### Build Validation (NEW 2026)

4. ⭐ **XcodeBuildMCP** (MANDATORY after code changes)
   - Build project to validate changes
   - Inspect build errors autonomously
   - Clean builds when needed
   - See: `mcp-tools/xcode-build-mcp.md`

```text
WORKFLOW (2026):
1. Check date
2. Apple Docs MCP: Search API/WWDC (current year)
3. If not found → Context7 → Exa web search
4. Apply latest patterns
5. Code implementation
6. XcodeBuildMCP: Build to validate
7. Fix errors if any → Rebuild
```

**Search queries (replace YYYY with current year):**

**Apple Docs MCP**:
- `SwiftUI [component] YYYY`
- `[Framework] new APIs`
- WWDC sessions: `[topic] WWDC YYYY`

**Exa web search** (if Apple Docs insufficient):
- `Swift [feature] YYYY best practices`
- `SwiftUI [component] YYYY tutorial`

Never assume - always verify current APIs and patterns exist for the current year.

---

## Codebase Analysis (MANDATORY)

**Before ANY implementation:**
1. Explore project structure to understand architecture
2. Read existing related files to follow established patterns
3. Identify naming conventions, coding style, and patterns used
4. Understand data flow and dependencies

**Continue implementation by:**
- Following existing patterns and conventions
- Matching the coding style already in place
- Respecting the established architecture
- Integrating with existing services/components

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. Search existing codebase for similar functionality
2. Check shared locations: `Core/Extensions/`, `Core/Utilities/`, `Core/Protocols/`
3. If similar code exists → extend/reuse instead of duplicate

**When creating new code:**
- Extract repeated logic (3+ occurrences) into shared helpers
- Place shared utilities in `Core/Utilities/`
- Use Extensions for type enhancements
- Document reusable functions with `///`

---

## Absolute Rules (MANDATORY)

### 1. Files < 150 lines

- **Split at 120 lines** - Never exceed 150
- Views < 80 lines (extract subviews at 30+)
- ViewModels < 100 lines
- Services < 100 lines
- Models < 50 lines

### 2. Protocols Separated

```text
Sources/
├── Protocols/           # Protocols ONLY
│   ├── UserServiceProtocol.swift
│   └── AuthProviderProtocol.swift
├── Services/            # Implementations
│   └── UserService.swift
├── ViewModels/          # @Observable classes
│   └── UserViewModel.swift
└── Views/               # SwiftUI Views
    └── UserView.swift
```

### 3. Swift Documentation Mandatory

```swift
/// Fetches user by ID from remote API.
///
/// - Parameter id: User unique identifier
/// - Returns: User if found, nil otherwise
/// - Throws: `NetworkError` on connection failure
func fetchUser(id: String) async throws -> User?
```

### 4. Preview-Driven Development (Apple)

Every View MUST have a `#Preview`:

```swift
#Preview {
    UserProfileView(user: .preview)
}

#Preview("Loading State") {
    UserProfileView(user: nil)
}
```

---

## Apple Architecture 2025

### Recommended: @Observable + Services

```text
Sources/
├── App/
│   └── MyApp.swift
├── Features/                # Feature modules
│   ├── Auth/
│   │   ├── Views/
│   │   ├── ViewModels/
│   │   ├── Services/
│   │   └── Protocols/
│   └── Profile/
├── Core/                    # Shared
│   ├── Services/
│   ├── Models/
│   ├── Protocols/
│   └── Extensions/
└── Resources/
```

### @Observable over ObservableObject

```swift
// ❌ OLD - ObservableObject
class UserViewModel: ObservableObject {
    @Published var user: User?
}

// ✅ NEW - @Observable (iOS 17+)
@Observable
final class UserViewModel {
    var user: User?
    var isLoading = false

    private let service: UserServiceProtocol

    init(service: UserServiceProtocol) {
        self.service = service
    }
}
```

---

## SOLID Principles for Swift

Each principle has detailed code examples:

**See [references/solid-patterns.md](references/solid-patterns.md)** for comprehensive Swift implementations:
- **S** - Single Responsibility: View, ViewModel, Service patterns
- **O** - Open/Closed: Protocol-based extensibility
- **L** - Liskov Substitution: Protocol implementation guarantees
- **I** - Interface Segregation: Small, focused protocols
- **D** - Dependency Inversion: Service injection patterns

Also includes concurrency patterns: actors, @MainActor, Sendable types, structured concurrency.

---

## Swift 6 Concurrency

Complete patterns in [references/solid-patterns.md](references/solid-patterns.md):
- **Actor** for shared state protection
- **@MainActor** for UI updates
- **Sendable** types for concurrent safety
- **Structured Concurrency** with async/let for parallel operations

---

## SwiftUI Templates

Complete working templates available in [references/solid-patterns.md](references/solid-patterns.md):
- **View**: < 80 lines with subviews and #Preview
- **ViewModel**: < 100 lines with @MainActor and @Observable
- **Protocol**: UserServiceProtocol with documentation
- **Service**: URLSession-based implementation

---

## Localization (MANDATORY)

All user-facing text MUST use String Catalogs:

```swift
// ✅ GOOD - Localized
Text("profile.welcome.title")
Button("button.save") { }

// With interpolation
Text("profile.greeting \(user.name)")

// ❌ BAD - Hardcoded
Text("Welcome!")
Button("Save") { }
```

Key naming: `module.screen.element`

---

## iOS 26 / WWDC 2025

### Liquid Glass Design

```swift
.glassBackgroundEffect()
.liquidGlass()
```

### SwiftUI Performance

- 6x faster list loading
- 16x faster updates on macOS
- Use SwiftUI Performance Instrument

### 3D Layouts (visionOS)

```swift
SpatialLayout {
    Model3D(named: "object")
}
```

---

## Response Guidelines

1. **Research first** - MANDATORY: Search Context7 + Exa before ANY code
2. **Show complete code** - Working examples, not snippets
3. **Explain decisions** - Why this pattern over alternatives
4. **Include previews** - Always add #Preview for views
5. **Handle errors** - Never ignore, always handle gracefully
6. **Consider accessibility** - VoiceOver, Dynamic Type
7. **Document code** - /// for public APIs

---

## Anti-Patterns & Violations

**Common mistakes and their fixes in [references/anti-patterns.md](references/anti-patterns.md)**:
- Single Responsibility violations (views doing too much)
- Open/Closed violations (hardcoded auth logic)
- Interface Segregation (bloated protocols)
- Dependency Inversion (hardcoded service dependencies)
- Architecture violations (mixed protocols/implementations)
- Concurrency violations (@MainActor, Sendable issues)
- File size violations (> 150 lines)

---

## Forbidden

- ❌ Coding without researching docs first (ALWAYS research)
- ❌ Using outdated APIs without checking current year docs
- ❌ Files > 150 lines
- ❌ Protocols in implementation files
- ❌ ObservableObject (use @Observable)
- ❌ Completion handlers (use async/await)
- ❌ Missing #Preview
- ❌ Hardcoded strings (use String Catalogs)
- ❌ Force unwrap without validation
- ❌ Missing /// documentation
- ❌ Views > 80 lines without extraction
- ❌ Non-Sendable types in async contexts
