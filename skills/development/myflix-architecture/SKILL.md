---
name: myflix-architecture
description: MyFlix project architecture patterns, module structure, and coding conventions for the Jellyfin client
---

# MyFlix Architecture Skill

## When to Use
Apply this skill when creating new features, refactoring code, or understanding codebase structure.

## Project Structure

```
myflix/
├── app-tv/                    # Android TV application
│   └── src/main/java/dev/jausc/myflix/tv/
│       ├── MainActivity.kt
│       ├── MyFlixApp.kt
│       ├── TvPreferences.kt
│       └── ui/
│           ├── components/    # HeroSection, MediaCard, NavigationRail, etc.
│           ├── screens/       # HomeScreen, DetailScreen, PlayerScreen, etc.
│           ├── theme/         # Colors.kt, Theme.kt
│           └── util/          # DynamicColorExtractor
├── app-mobile/                # Mobile application
│   └── src/main/java/dev/jausc/myflix/mobile/
│       ├── MainActivity.kt
│       ├── MobilePreferences.kt
│       ├── service/           # PlaybackService, PlaybackServiceConnection
│       └── ui/
│           ├── components/    # HeroSection, MediaCard, NavigationMenu
│           ├── screens/       # HomeScreen, DetailScreen, etc.
│           └── theme/
├── core/
│   ├── common/                # Shared utilities & models
│   │   └── HeroContentBuilder.kt, LibraryFinder.kt, JellyfinModels.kt
│   ├── network/               # JellyfinClient (Ktor-based API)
│   ├── data/                  # AppState
│   ├── player/                # ExoPlayer + MPV integration
│   └── seerr/                 # Jellyseerr integration
└── ui/
    ├── common/                # Shared theme colors
    ├── mobile/                # Mobile UI components
    └── tv/                    # TV UI components
```

## Package Naming
- Base: `dev.jausc.myflix`
- TV: `dev.jausc.myflix.tv`
- Mobile: `dev.jausc.myflix.mobile`
- Core: `dev.jausc.myflix.core.{module}`

## State Management Pattern

### Screen-Level State (Current Pattern)
```kotlin
@Composable
fun FeatureScreen(jellyfinClient: JellyfinClient) {
    val scope = rememberCoroutineScope()
    var items by remember { mutableStateOf<List<JellyfinItem>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var refreshTrigger by remember { mutableStateOf(0) }

    LaunchedEffect(refreshTrigger) {
        isLoading = true
        jellyfinClient.clearCache()
        jellyfinClient.getItems()
            .onSuccess { items = it }
            .onFailure { errorMessage = it.message }
        isLoading = false
    }
    
    // Trigger refresh
    scope.launch { refreshTrigger++ }
}
```

## API Client Pattern

```kotlin
// API calls return Result<T>
jellyfinClient.getLatestMovies(libraryId, limit = 12)
    .onSuccess { movies -> /* handle */ }
    .onFailure { error -> /* handle */ }

// Image URLs (WebP format, optimized sizes)
jellyfinClient.getPrimaryImageUrl(itemId, imageTag, maxWidth = 400)
jellyfinClient.getBackdropUrl(itemId, backdropTag, maxWidth = 1920)

// Cache management
jellyfinClient.clearCache()
jellyfinClient.invalidateCache("resume", "nextup")
```

## Output Format
ALWAYS provide code as **zip files** with:
- Unique names: `myflix-{feature}-{date}-{time}.zip`
- Directory structure matching git repo root
- Complete git commit message
