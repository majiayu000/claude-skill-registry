---
name: summon
description: Use when developing applications with the Summon Kotlin Multiplatform UI framework. Provides patterns, conventions, and guidance for components, state management, modifiers, routing, SSR, and cross-platform code.
---

# Summon Framework Development Skill

You are assisting with development using **Summon**, a Kotlin Multiplatform UI framework for building web applications
with Jetpack Compose-like declarative syntax.

## Quick Reference

**Package namespace**: `codes.yousef.summon`
**Current version**: 0.6.3.0
**Targets**: Browser (JS/WASM) and JVM (SSR)

## Core Patterns

### Component Pattern

```kotlin
@Composable
fun MyComponent(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier()
) {
    val renderer = LocalPlatformRenderer.current
    // Use renderer methods, not direct DOM manipulation
}
```

### State Management

```kotlin
// Direct access
val counter = remember { mutableStateOf(0) }
counter.value = counter.value + 1

// Property delegation (preferred)
var counter by remember { mutableStateOf(0) }
counter++

// Destructuring
val (count, setCount) = remember { mutableStateOf(0) }
setCount(count + 1)
```

### Modifier Pattern (Type-safe CSS)

```kotlin
Modifier()
    .padding(16.px)
    .backgroundColor(Color.Blue)
    .borderRadius(8.px)
    .display(Display.Flex)
    .alignItems(AlignItems.Center)
    .onClick { /* handler */ }
```

### Routing

```kotlin
// Static route
route("/about") { AboutPage() }

// Dynamic parameter
route("/users/[id]") { params ->
    val userId = params.getInt("id")
    UserPage(userId)
}

// Catch-all
route("/docs/[...slug]") { params ->
    DocsPage(params["slug"])
}
```

### Effects and Lifecycle

```kotlin
@Composable
fun MyComponent() {
    onMount { println("Component mounted") }
    onDispose { println("Component disposed") }

    effectWithDeps(dependency) {
        // Runs when dependency changes
    }
}
```

### SSR with Hydration

```kotlin
val renderer = PlatformRenderer()
val html = renderer.renderComposableRoot(hydrate = true) { MyApp() }
```

## Key Guidelines

1. **Use type-safe Modifiers** - Never use raw CSS strings; use the Modifier API with type-safe enums
2. **Don't manipulate DOM directly** - Use renderer methods and composable functions
3. **Add @JsName annotations** - Required for public APIs to ensure consistent naming in minified JS
4. **Don't capture mutable state in lambdas** - Use wrapper functions when passing callbacks to renderers
5. **Use getPlatformRenderer()** - For reliable renderer access in JS contexts
6. **Platform-specific code** - Keep in appropriate source sets (commonMain, jvmMain, jsMain, wasmJsMain)

## Source Set Hierarchy

```
commonMain
    └── webMain (shared JS + WASM code)
            ├── jsMain (browser JS)
            └── wasmJsMain (WebAssembly)
```

## Common Build Commands

```bash
# Build all
./gradlew build

# Run JVM tests (excludes slow tests)
./gradlew :summon-core:jvmTest

# Run JS tests
./gradlew :summon-core:jsNodeTest

# Development run (JS with hot reload)
./gradlew jsBrowserDevelopmentRun

# Publish locally
./gradlew publishLocal
```

## Component Categories

| Category   | Location                | Examples                                 |
|------------|-------------------------|------------------------------------------|
| Display    | `components.display`    | Text, Image, Icon, Badge                 |
| Input      | `components.input`      | TextField, Button, Checkbox, Select      |
| Layout     | `components.layout`     | Row, Column, Box, Grid, Card, LazyColumn |
| Feedback   | `components.feedback`   | Alert, Modal, Toast, Loading, Progress   |
| Navigation | `components.navigation` | Link, TabLayout, Dropdown                |
| Forms      | `components.forms`      | Form, FormField, validation              |

## Common Pitfalls

1. **WASM cache staleness** - Run `./gradlew clean` if WASM builds behave unexpectedly
2. **JS minification issues** - Always add `@JsName` to public functions
3. **State in lambdas** - Don't capture mutable state directly in renderer callbacks
4. **Missing hydration** - SSR requires proper hydration setup for interactivity

## Documentation References

- `llms.txt` - Condensed LLM documentation
- `llms-full.txt` - Full API documentation
- `CLAUDE.md` - Detailed AI assistant guidance
- `docs/` - User documentation