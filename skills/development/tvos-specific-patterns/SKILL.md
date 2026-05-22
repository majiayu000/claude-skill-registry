---
name: tvos-specific-patterns
description: "Expert tvOS decisions for iOS developers: when to use custom focus effects vs system defaults, Siri Remote gesture trade-offs, Top Shelf content strategies, and 10-foot UI adaptation patterns. Use when building tvOS apps, debugging focus issues, or designing TV-optimized interfaces. Trigger keywords: tvOS, Focus Engine, @FocusState, isFocused, focusable, focusSection, Siri Remote, Top Shelf, TVTopShelfContentProvider, 10-foot UI, CardButtonStyle, large cards"
version: "3.0.0"
---

# tvOS Specific Patterns — Expert Decisions

Expert decision frameworks for tvOS choices. Claude knows @FocusState and SwiftUI basics — this skill provides judgment calls for focus architecture, remote handling, and TV-optimized UI trade-offs.

---

## Decision Trees

### Focus Management Strategy

```
How complex is your focus navigation?
├─ Linear list/grid navigation
│  └─ System focus handling
│     Default behavior, no custom code needed
│
├─ Multiple focus sections with priority
│  └─ .focusSection() grouping
│     Group related elements, system handles within
│
├─ Custom initial focus on appear
│  └─ @FocusState + .onAppear
│     Set focused item programmatically
│
├─ Complex conditional focus logic
│  └─ .prefersDefaultFocus() + @FocusState
│     Combine for sophisticated control
│
└─ Focus must follow data changes
   └─ Bind @FocusState to data model
      Update focus when selection changes
```

**The trap**: Overriding focus behavior when system defaults work fine. Custom focus logic adds complexity and can break expected navigation patterns.

### Custom Focus Effect Decision

```
Should you create custom focus effects?
├─ Standard card/button scaling
│  └─ Use .buttonStyle(.card)
│     Apple's built-in TV-appropriate effect
│
├─ Need subtle highlight
│  └─ .isFocused environment
│     Opacity/border changes only
│
├─ Complex parallax/tilt effects
│  └─ Custom view with rotation3DEffect
│     Only for hero content, not lists
│
└─ Media-browsing app (Netflix-like)
   └─ Custom focus with content preview
      Scale + shadow + metadata reveal
```

### Top Shelf Content Strategy

```
What content should appear in Top Shelf?
├─ Personalized content (continue watching)
│  └─ TVTopShelfCarouselContent with .actions style
│     Play and display actions per item
│
├─ Browse/discovery content
│  └─ TVTopShelfSectionedContent
│     Multiple categories with items
│
├─ Single featured item
│  └─ TVTopShelfCarouselContent single item
│     Hero image with actions
│
├─ Time-sensitive content
│  └─ Update via background refresh
│     Schedule updates, cache for speed
│
└─ User not logged in
   └─ Promotional content + CTA
      Drive app opens and registration
```

### Siri Remote Gesture Selection

```
Which gesture for this interaction?
├─ Primary action (play, select)
│  └─ Tap (click center)
│     .onTapGesture or Button
│
├─ Secondary action (info, options)
│  └─ Long press
│     Context menu or info overlay
│
├─ Content navigation (carousel)
│  └─ Swipe left/right
│     DragGesture with threshold
│
├─ Volume/scrubbing
│  └─ Swipe up/down
│     System handles in video player
│
└─ Cancel/back
   └─ Menu button
      .onExitCommand handler
```

---

## NEVER Do

### Focus Management

**NEVER** fight the Focus Engine:
```swift
// ❌ Trying to manually manage all focus
struct BadNavigation: View {
    @State private var selectedIndex = 0

    var body: some View {
        HStack {
            ForEach(0..<items.count) { index in
                ItemView(item: items[index])
                    .opacity(selectedIndex == index ? 1 : 0.5)  // Fake focus
            }
        }
        .onMoveCommand { direction in
            // Manual index management — reinventing Focus Engine!
            switch direction {
            case .left: selectedIndex = max(0, selectedIndex - 1)
            case .right: selectedIndex = min(items.count - 1, selectedIndex + 1)
            default: break
            }
        }
    }
}

// ✅ Let Focus Engine handle it
struct GoodNavigation: View {
    @FocusState private var focusedItem: Item.ID?

    var body: some View {
        HStack {
            ForEach(items) { item in
                ItemView(item: item)
                    .focusable()
                    .focused($focusedItem, equals: item.id)
            }
        }
    }
}
```

**NEVER** use .focusable() without visual feedback:
```swift
// ❌ User can't see what's focused
Text("Invisible Focus")
    .focusable()  // Focusable but no visual change!

// ✅ Always show focus state
struct FocusableText: View {
    @Environment(\.isFocused) var isFocused

    var body: some View {
        Text("Visible Focus")
            .scaleEffect(isFocused ? 1.1 : 1.0)
            .animation(.easeInOut(duration: 0.2), value: isFocused)
            .focusable()
    }
}
```

**NEVER** animate focus changes slowly:
```swift
// ❌ Laggy feel — focus must be instant
.animation(.easeInOut(duration: 0.5), value: isFocused)  // Too slow!

// ✅ Quick transitions (200ms or less)
.animation(.easeInOut(duration: 0.2), value: isFocused)
```

### Remote Handling

**NEVER** use complex gestures on tvOS:
```swift
// ❌ Siri Remote doesn't support these
.gesture(
    MagnificationGesture()  // No pinch on Siri Remote!
)

.gesture(
    RotationGesture()  // No rotation on Siri Remote!
)

// ✅ Stick to supported gestures
.onTapGesture { }
.onLongPressGesture { }
.gesture(DragGesture())  // Swipe detection
```

**NEVER** ignore the Menu button:
```swift
// ❌ User trapped in screen
struct PlayerView: View {
    var body: some View {
        VideoPlayer(player: player)
        // No way to exit!
    }
}

// ✅ Always handle exit
struct PlayerView: View {
    @Environment(\.dismiss) var dismiss

    var body: some View {
        VideoPlayer(player: player)
            .onExitCommand {
                dismiss()
            }
    }
}
```

### UI Layout

**NEVER** use iOS-sized touch targets:
```swift
// ❌ Way too small for TV
Button("Play") { }
    .frame(width: 44, height: 44)  // iOS size

// ✅ TV-appropriate sizes (minimum 80pt, prefer 100+)
Button("Play") { }
    .frame(minWidth: 200, minHeight: 80)
    .buttonStyle(.card)
```

**NEVER** use small text on TV:
```swift
// ❌ Unreadable from 10 feet
Text("Description")
    .font(.caption)  // ~11pt — can't read!

Text("Details")
    .font(.footnote)  // ~13pt — still too small

// ✅ Use legible sizes
Text("Description")
    .font(.title3)  // Minimum for body text

Text("Title")
    .font(.system(size: 48, weight: .bold))  // Hero content
```

**NEVER** forget edge insets:
```swift
// ❌ Content touches screen edges
ScrollView {
    LazyVGrid(columns: columns) {
        // Content starts at edge — looks cramped
    }
}

// ✅ Use proper TV margins (40-60pt minimum)
ScrollView {
    LazyVGrid(columns: columns) {
        ForEach(items) { item in
            ItemView(item: item)
        }
    }
    .padding(60)  // TV safe area
}
```

### Top Shelf

**NEVER** use low-resolution images:
```swift
// ❌ Blurry on 4K TV
item.setImageURL(thumbnailURL, for: .screenScale1x)  // Only 1x

// ✅ Provide all resolutions
item.setImageURL(url1x, for: .screenScale1x)
item.setImageURL(url2x, for: .screenScale2x)  // Essential for Retina
```

**NEVER** return empty Top Shelf for logged-out users:
```swift
// ❌ Wasted promotional space
override func loadTopShelfContent(completionHandler: @escaping (TVTopShelfContent?) -> Void) {
    if !isLoggedIn {
        completionHandler(nil)  // Empty!
        return
    }
    // ...
}

// ✅ Show promotional content
override func loadTopShelfContent(completionHandler: @escaping (TVTopShelfContent?) -> Void) {
    if !isLoggedIn {
        completionHandler(createPromotionalContent())  // Drive engagement
        return
    }
    // ...
}
```

---

## Essential Patterns

### Focus-Aware Card Component

```swift
struct TVCard<Content: View>: View {
    @Environment(\.isFocused) private var isFocused
    let content: () -> Content

    var body: some View {
        content()
            .scaleEffect(isFocused ? 1.1 : 1.0)
            .shadow(
                color: .black.opacity(isFocused ? 0.3 : 0),
                radius: isFocused ? 20 : 0,
                y: isFocused ? 10 : 0
            )
            .animation(.spring(response: 0.3, dampingFraction: 0.7), value: isFocused)
            .focusable()
    }
}

// Usage
TVCard {
    VStack {
        AsyncImage(url: movie.posterURL) { image in
            image.resizable().aspectRatio(contentMode: .fill)
        } placeholder: {
            Rectangle().fill(Color.gray.opacity(0.3))
        }
        .frame(width: 300, height: 450)
        .cornerRadius(12)

        Text(movie.title)
            .font(.headline)
    }
}
```

### Focus Section Navigation

```swift
struct TVHomeView: View {
    var body: some View {
        ScrollView {
            VStack(spacing: 40) {
                // Hero section — gets initial focus
                heroSection
                    .focusSection()

                // Continue watching — separate focus group
                sectionView(title: "Continue Watching", items: continueWatching)
                    .focusSection()

                // Recommendations — separate focus group
                sectionView(title: "For You", items: recommendations)
                    .focusSection()
            }
        }
    }

    private func sectionView(title: String, items: [Movie]) -> some View {
        VStack(alignment: .leading, spacing: 16) {
            Text(title)
                .font(.title2)
                .padding(.leading, 60)

            ScrollView(.horizontal, showsIndicators: false) {
                LazyHStack(spacing: 30) {
                    ForEach(items) { item in
                        TVCard {
                            MoviePoster(movie: item)
                        }
                    }
                }
                .padding(.horizontal, 60)
            }
        }
    }
}
```

### Top Shelf Provider

```swift
class ContentProvider: TVTopShelfContentProvider {
    override func loadTopShelfContent() async -> TVTopShelfContent? {
        do {
            let items = try await fetchContent()
            return TVTopShelfCarouselContent(style: .actions, items: items)
        } catch {
            return createFallbackContent()
        }
    }

    private func fetchContent() async throws -> [TVTopShelfCarouselItem] {
        let movies = try await API.fetchFeatured()

        return movies.prefix(10).map { movie in
            let item = TVTopShelfCarouselItem(identifier: movie.id)

            item.setImageURL(movie.posterURL(size: .x1), for: .screenScale1x)
            item.setImageURL(movie.posterURL(size: .x2), for: .screenScale2x)

            item.title = movie.title
            item.subtitle = "\(movie.year) • \(movie.genre)"

            // Deep links
            item.displayAction = TVTopShelfAction(url: URL(string: "myapp://movie/\(movie.id)")!)
            item.playAction = TVTopShelfAction(url: URL(string: "myapp://play/\(movie.id)")!)

            return item
        }
    }
}
```

---

## Quick Reference

### Focus Modifiers

| Modifier | Purpose |
|----------|---------|
| .focusable() | Make view focusable |
| .focused($state, equals:) | Bind to FocusState |
| .focusSection() | Group related focusable items |
| .prefersDefaultFocus() | Set preferred initial focus |
| .onExitCommand | Handle Menu button |
| .onPlayPauseCommand | Handle Play/Pause |
| .onMoveCommand | Handle directional input |

### TV Size Guidelines

| Element | Minimum Size |
|---------|--------------|
| Button/Card | 200 × 80 pt |
| Poster card | 300 × 450 pt |
| Hero banner | Full width × 800 pt |
| Body text | title3 (20pt) |
| Title text | title (28pt) |
| Edge padding | 60 pt |

### Top Shelf Content Types

| Style | Use Case |
|-------|----------|
| Carousel (.actions) | Featured with play buttons |
| Carousel (.details) | Info-focused items |
| Sectioned | Multiple categories |
| Inset | Banner-style single item |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Manual index tracking for focus | Reinventing Focus Engine | Use @FocusState |
| .focusable() without visual change | User can't see focus | Add isFocused styling |
| Slow focus animations (>200ms) | Laggy navigation feel | Use quick transitions |
| 44×44 buttons | Too small for TV | Minimum 200×80 |
| .caption/.footnote text | Unreadable at distance | Use .title3 minimum |
| No .onExitCommand handler | User trapped in screen | Always handle Menu |
| Complex gestures (pinch/rotate) | Not supported by Siri Remote | Use tap/swipe only |
| Empty Top Shelf for logged-out | Wasted promotional space | Show promo content |
