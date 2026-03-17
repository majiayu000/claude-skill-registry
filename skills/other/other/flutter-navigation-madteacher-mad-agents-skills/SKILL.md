---
name: flutter-navigation
description: Comprehensive guide for Flutter navigation and routing including Navigator API, go_router, deep linking, passing/returning data, and web-specific navigation. Use when implementing screen transitions, configuring routing systems, setting up deep links, handling browser history, or managing navigation state in Flutter applications.
metadata:
  author: Stanislav [MADTeacher] Chernyshev
  version: "1.0"
---

# Flutter Navigation

## Overview

Implement navigation and routing in Flutter applications across mobile and web platforms. Choose the right navigation approach, configure deep linking, manage data flow between screens, and handle browser history integration.

## Choosing an Approach

### Use Navigator API (Imperative) When:
- Simple apps without deep linking requirements
- Single-screen to multi-screen transitions
- Basic navigation stacks
- Quick prototyping

Example: `assets/navigator_basic.dart`

### Use go_router (Declarative) When:
- Apps requiring deep linking (iOS, Android, Web)
- Web applications with browser history support
- Complex navigation patterns with multiple Navigator widgets
- URL-based navigation needed
- Production applications with scalable architecture

Example: `assets/go_router_basic.dart`

### Avoid Named Routes
Flutter team does NOT recommend named routes. They have limitations:
- Cannot customize deep link behavior
- No browser forward button support
- Always pushes new routes regardless of current state

## Common Tasks

### Pass Data Between Screens

**With Navigator:**
```dart
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => DetailScreen(item: myItem)),
);
```

**With go_router:**
```dart
context.push('/details?id=123');
// Extract: final id = state.uri.queryParameters['id'];
```

Example: `assets/passing_data.dart`

### Return Data From Screens

```dart
final result = await Navigator.push(
  context,
  MaterialPageRoute<String>(builder: (context) => SelectionScreen()),
);
if (!context.mounted) return;
```

Example: `assets/returning_data.dart`

### Configure Deep Linking

**Android:** Configure `AndroidManifest.xml` intent filters
**iOS:** Configure `Info.plist` for Universal Links
**Web:** Automatic with go_router, choose URL strategy

For detailed setup: `references/deep-linking.md`

### Web URL Strategy

**Hash (default):** `example.com/#/path` - no server config needed
**Path:** `example.com/path` - cleaner URLs, requires server config

For server setup: `references/web-navigation.md`

## Navigation Methods

### go_router Navigation
- `context.go('/path')` - replace current route
- `context.push('/path')` - add to stack
- `context.pop()` - go back

### Navigator Navigation
- `Navigator.push()` - add route to stack
- `Navigator.pop()` - remove route from stack

## Advanced Topics

**Route Guards:** Implement authentication redirects
**Nested Routes:** Create shell routes with shared UI
**Error Handling:** Handle 404 and navigation errors
**Multiple Navigators:** Manage independent navigation stacks

For advanced patterns: `references/go_router-guide.md`

## Decision Guide

Use [navigation-patterns.md](references/navigation-patterns.md) for:
- Complete comparison of navigation approaches
- Deep linking behavior by platform
- Web-specific considerations
- Common patterns and anti-patterns
